"""Bounded map-selection evidence, including failed scans and false shapes."""
import bisect
import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

from dialogue_cluster_audit import trace_graph
from engine_reference_probe import discover, make_probe
from map_extract import FormatError, discover_lookup, header, pointer, pointer_prefix
from pointer_scan import BASE, index_pointers
from script_extract import WARP_NAMES, decode_script

ROOT = Path(__file__).resolve().parents[1]
SELECTED_MAPS = {99, 101, 107, 111}
VARIANTS = {107, 111}
SETTER_OPCODES = (0x3E, 0x3F, 0x40, 0x41, 0xC4)


def thumb_bl(rom, at):
    if at < 0 or at % 2 or at + 4 > len(rom):
        return None
    hi, lo = struct.unpack_from('<HH', rom, at)
    if hi & 0xF800 != 0xF000 or lo & 0xF800 != 0xF800:
        return None
    relative = ((hi & 0x7FF) << 12) | ((lo & 0x7FF) << 1)
    if relative & 0x400000:
        relative -= 0x800000
    return at + 4 + relative


def calls_in(rom, start, end):
    return [{'offset': at, 'target': target} for at in range(start, min(end, len(rom)) - 3, 2)
            if (target := thumb_bl(rom, at)) is not None]


def scan_map_links(rom):
    lookup = discover_lookup(rom)
    groups = pointer_prefix(rom, lookup['table'], 256)
    slots, banks, inbound = [], [], []
    for group, bank_start in enumerate(groups['targets']):
        bank = pointer_prefix(rom, bank_start)
        banks.append({'group': group, **{k: v for k, v in bank.items() if k != 'targets'}})
        for number, hp in enumerate(bank['targets']):
            slot = {'group': group, 'map': number, 'header': hp,
                    'pointer_site': bank_start + number * 4, 'reachability': 'UNKNOWN'}
            slots.append(slot)
            try:
                header(rom, hp)
                slot['full_header_parser'] = 'passed'
            except (FormatError, struct.error) as exc:
                slot['full_header_parser'] = str(exc)
            for kind in ('warp', 'connection'):
                try:
                    if hp % 4 or hp + 28 > len(rom):
                        raise FormatError('Header span/alignment')
                    control = pointer(rom, hp + (4 if kind == 'warp' else 12), nullable=True)
                    if control is None:
                        slot[kind] = {'status': 'null_pointer', 'pointer_site': hp + (4 if kind == 'warp' else 12)}
                        continue
                    if control % 4 or control + (20 if kind == 'warp' else 8) > len(rom):
                        raise FormatError('Control structure span/alignment')
                    if kind == 'warp':
                        count, stride, field = rom[control + 1], 8, control + 8
                    else:
                        count, stride, field = struct.unpack_from('<i', rom, control)[0], 12, control + 4
                        if not 0 <= count <= 32:
                            raise FormatError('Connection count outside inspected limit 0..32')
                    base = pointer(rom, field, nullable=count == 0)
                    if count and base + count * stride > len(rom):
                        raise FormatError('Array outside ROM')
                    slot[kind] = {'status': 'array_span_parsed', 'control': control, 'count': count,
                                  'array_pointer_site': field, 'array': base,
                                  'array_sha256': hashlib.sha256(rom[base:base + count * stride] if count else b'').hexdigest()}
                    for index in range(count):
                        at = base + index * stride
                        dest_group, dest_map = ((rom[at + 7], rom[at + 6]) if kind == 'warp'
                                                else (rom[at + 8], rom[at + 9]))
                        if dest_group != 3 or dest_map not in SELECTED_MAPS:
                            continue
                        inbound.append({'source_group': group, 'source_map': number, 'header': hp,
                                        'source_pointer_site': slot['pointer_site'], 'kind': kind, 'index': index,
                                        'offset': at, 'destination_group': dest_group, 'destination_map': dest_map,
                                        'destination_warp': rom[at + 5] if kind == 'warp' else None,
                                        'source_evidence': ('validated_header_and_link_span' if slot['full_header_parser'] == 'passed'
                                                            else 'link_span_only_unvalidated_header'),
                                        'raw_hex': rom[at:at + stride].hex(' '), 'reachability': 'UNKNOWN'})
                except (FormatError, struct.error) as exc:
                    slot[kind] = {'status': 'unresolved', 'reason': str(exc)}
    return {'lookup': lookup, 'group_physical_prefix': {k: v for k, v in groups.items() if k != 'targets'},
            'bank_physical_prefixes': banks, 'slots': slots, 'incoming_records': inbound,
            'summary': {'groups_in_physical_prefix': len(groups['targets']), 'candidate_slots': len(slots),
                        'banks_reaching_scan_limit': sum(b['stop'] == 'scan limit' for b in banks),
                        **{kind: {'slot_statuses': dict(sorted(Counter(s[kind]['status'] for s in slots).items())),
                                  'records_in_parsed_spans': sum(s[kind].get('count', 0) for s in slots)}
                           for kind in ('warp', 'connection')},
                        'incoming_candidate_associations_by_target': {f'3:{n}': sum(r['destination_map'] == n for r in inbound) for n in sorted(SELECTED_MAPS)},
                        'incoming_validated_header_associations_by_target': {
                            f'3:{n}': sum(r['destination_map'] == n and r['source_evidence'] == 'validated_header_and_link_span' for r in inbound)
                            for n in sorted(SELECTED_MAPS)}}}


def lz77_extent(rom, start, max_output=0x100000, max_input=0x40000):
    """Validate token geometry without writing decompressed data or source bytes."""
    if start < 0 or start + 4 > len(rom) or rom[start] != 0x10:
        return None
    size = int.from_bytes(rom[start + 1:start + 4], 'little')
    if not 1 <= size <= max_output:
        return None
    at, made = start + 4, 0
    while made < size:
        if at >= len(rom) or at - start >= max_input:
            return None
        flags = rom[at]
        at += 1
        for bit in range(7, -1, -1):
            if made >= size:
                break
            if flags & (1 << bit):
                if at + 2 > len(rom):
                    return None
                token = int.from_bytes(rom[at:at + 2], 'big')
                at += 2
                distance, length = (token & 4095) + 1, (token >> 12) + 3
                if distance > made:
                    return None
                made += min(length, size - made)
            else:
                if at >= len(rom):
                    return None
                at += 1
                made += 1
            if at - start > max_input:
                return None
    return {'start': start, 'end': at, 'declared_output_size': size,
            'sha256': hashlib.sha256(rom[start:at]).hexdigest()}


def catalogue_paths(rom, catalogue):
    evidence, nodes = [], {}
    for root in catalogue['roots']:
        graph = trace_graph(rom, root['offset'], max_instructions=256, max_states=1024, decoder=decode_script)
        nodes.update(graph['nodes'])
        selected = []
        for ins in graph['nodes'].values():
            if ins['opcode'] in set(WARP_NAMES) | {0x3C} and ins['values'][0] == 3 and ins['values'][1] in SELECTED_MAPS:
                selected.append({**ins, 'witness': graph['witness'](ins['pc'])})
        evidence.append({'root': root['offset'], 'association_ids': [a['id'] for a in root['associations']],
                         'instruction_count': len(graph['nodes']), 'state_count': graph['state_count'],
                         'selected_transition_instructions': selected,
                         'frontiers': graph['frontiers'], 'overlaps': graph['overlaps']})
    return {'summary': {'roots': len(evidence), 'unique_instructions': len(nodes),
                        'roots_with_overlaps': sum(bool(e['overlaps']) for e in evidence),
                        'selected_transition_witnesses': sum(len(e['selected_transition_instructions']) for e in evidence),
                        'frontier_reasons': dict(sorted(Counter(f['reason'] for e in evidence for f in e['frontiers']).items()))},
            'roots': evidence}, nodes


def raw_script_shapes(rom, incoming, nodes):
    targets = sorted(incoming)
    candidates, graph_cache, lz_cache = [], {}, {}
    for number in sorted(VARIANTS):
        for opcode in sorted(set(WARP_NAMES) | {0x3C}):
            position = 0
            while (at := rom.find(bytes([opcode, 3, number]), position)) >= 0:
                position = at + 1
                ins, error = decode_script(rom, at)
                row = {'offset': at, 'target_map': f'3:{number}', 'opcode': opcode,
                       'instruction_shape': ins, 'decode_error': error,
                       'catalogue_instruction_boundary_match': at in nodes and nodes[at]['opcode'] == opcode,
                       'context_start': max(0, at - 12), 'context_hex': rom[max(0, at - 12):at + 20].hex(' '),
                       'overlapping_ROM_pointer_words': [], 'pointer_target_path_attempts': [],
                       'compressed_stream': None, 'status': 'unvalidated_command_shape'}
                for site in range(max(0, at - 3), at + 3):
                    if site + 4 > len(rom):
                        continue
                    word = struct.unpack_from('<I', rom, site)[0]
                    target = word - BASE
                    if BASE <= word < BASE + len(rom) and site in incoming.get(target, []):
                        row['overlapping_ROM_pointer_words'].append({'offset': site, 'target': target})
                roots = targets[bisect.bisect_left(targets, max(0, at - 512)):bisect.bisect_right(targets, at)]
                row['pointer_target_scan_truncated'] = len(roots) > 128
                for root in roots[:128]:
                    if root not in graph_cache:
                        graph_cache[root] = trace_graph(rom, root, max_instructions=128, max_states=512, decoder=decode_script)
                    graph = graph_cache[root]
                    row['pointer_target_path_attempts'].append({'root': root, 'incoming_pointer_sites': incoming[root],
                                                               'witness': graph['witness'](at),
                                                               'overlaps': graph['overlaps'], 'frontiers': graph['frontiers']})
                # Nearest aligned, ROM-pointer-backed valid stream in a bounded window.
                starts = targets[bisect.bisect_left(targets, max(0, at - 0x40000)):bisect.bisect_right(targets, at)]
                for start in reversed(starts):
                    if start % 4 or rom[start] != 0x10:
                        continue
                    if start not in lz_cache:
                        lz_cache[start] = lz77_extent(rom, start)
                    extent = lz_cache[start]
                    if extent and at + (ins['end'] - at if ins else 3) <= extent['end']:
                        row['compressed_stream'] = {**extent, 'incoming_pointer_sites': incoming[start]}
                        break
                row['context_class'] = ('pointer_backed_LZ77_stream' if row['compressed_stream'] else
                                        'overlapping_ROM_pointer_word' if row['overlapping_ROM_pointer_words'] else
                                        'unresolved_context')
                candidates.append(row)
    return sorted(candidates, key=lambda row: row['offset'])


def native_evidence(rom, reference):
    candidates = [c for c in discover(rom) if not c['contained_in_other_candidate']]
    if len(candidates) != 1:
        raise FormatError('Ambiguous native script-handler table')
    entries = candidates[0]['entries']
    lookup = discover_lookup(rom)
    targets = {lookup['function']: 'native_map_lookup'}
    discoveries = []
    for opcode in SETTER_OPCODES:
        start = (entries[opcode] & ~1) - BASE
        end = min((p & ~1) - BASE for p in entries if (p & ~1) - BASE > start)
        calls = calls_in(rom, start, end)
        if not calls:
            raise FormatError('No BL in destination-setter handler interval')
        # This is a recorded candidate, not an inferred global ABI/dataflow proof.
        target = calls[-1]['target']
        targets[target] = f'last_call_from_handler_{opcode:02X}'
        discoveries.append({'opcode': opcode, 'handler': start, 'handler_end': end, 'calls': calls, 'selected_last_call': calls[-1]})
    # Independently established native intervals from the prior warp investigation.
    for start, end, digest, role in [
            (0x553C8, 0x55468, '19e16e4449b3bb624931ed9c1b5eb81a44d468bfcb47fb143536562ccb890ae7', 'map_warp_wrapper'),
            (0x55454, 0x5546C, '3159d3745bb661398af6cbff017614e4ed474ef907dd5a089d26465a5a1d0aee', 'use_saved_dynamic')]:
        if hashlib.sha256(rom[start:end]).hexdigest() != digest or rom[start:end] != reference[start:end]:
            raise FormatError('Retained native semantics interval changed')
        targets[start] = role
    targets[0x553E8] = 'store_dynamic_return_in_verified_setter_interval'
    sites = []
    for call in calls_in(rom, 0, len(rom)):
        if call['target'] not in targets:
            continue
        at = call['offset']
        constants = []
        for pc in range(max(0, at - 32), at, 2):
            hw = struct.unpack_from('<H', rom, pc)[0]
            if hw & 0xF800 == 0x2000:
                constants.append({'offset': pc, 'kind': 'MOVS_imm8', 'register': (hw >> 8) & 7, 'value': hw & 255})
            elif hw & 0xF800 == 0x4800:
                literal = ((pc + 4) & ~3) + (hw & 255) * 4
                if literal + 4 <= len(rom):
                    constants.append({'offset': pc, 'kind': 'PC_relative_LDR', 'register': (hw >> 8) & 7,
                                      'literal_site': literal, 'value': struct.unpack_from('<I', rom, literal)[0]})
        sites.append({**call, 'role': targets[call['target']], 'context_start': max(0, at - 32),
                      'context_hex': rom[max(0, at - 32):at + 8].hex(' '), 'constant_assignment_shapes': constants,
                      'variant_immediate_shapes': [c for c in constants if c['value'] in VARIANTS],
                      'reachability': 'UNKNOWN'})
    return {'method': 'Thumb-1 BL shapes at every halfword alignment to the independently discovered map lookup, last BL targets in five setter-handler intervals, and checksum-verified prior native wrappers. Previous 32 bytes inspected only for MOVS and PC-relative LDR constant shapes; no register/control-flow analysis. Raw BL shapes can occur in data; indirect calls, computed IDs and RAM writes are outside this probe.',
            'target_discovery': discoveries, 'target_functions': {str(k): v for k, v in sorted(targets.items())},
            'handler_comparison': make_probe(reference, rom, SETTER_OPCODES),
            'call_sites': sites, 'summary': {'BL_shape_sites': len(sites),
                                           'sites_with_variant_constant_shapes': sum(bool(s['variant_immediate_shapes']) for s in sites)}}


def header_pointer_evidence(rom, incoming, scan):
    result = []
    for number in sorted(VARIANTS):
        selected = next(s for s in scan['slots'] if (s['group'], s['map']) == (3, number))
        hp = selected['header']
        rows = []
        for site in incoming.get(hp, []):
            row = {'pointer_site': site, 'target_header': hp,
                   'role': 'native_bank_slot' if site == selected['pointer_site'] else 'unclassified_data_pointer'}
            layout_start = site - 12
            if row['role'] != 'native_bank_slot' and layout_start >= 0 and layout_start + 28 <= len(rom):
                width, height = struct.unpack_from('<ii', rom, layout_start)
                if 0 < width <= 1024 and 0 < height <= 1024:
                    row['layout_shaped_context'] = {'start': layout_start, 'width': width, 'height': height,
                                                    'raw_hex': rom[layout_start:layout_start + 28].hex(' '),
                                                    'field_offset': 12, 'incoming_absolute_pointer_sites': incoming.get(layout_start, []),
                                                    'status': 'shape only; not a certified indexed layout or executable literal'}
            rows.append(row)
        result.append({'map_id': f'3:{number}', 'header': hp, 'references': rows})
    return result


def build(rom, reference, catalogue):
    digest = hashlib.sha256(rom).hexdigest()
    if catalogue['source_sha256'] != digest:
        raise FormatError('Stale map-script catalogue')
    incoming = index_pointers(rom)
    scan = scan_map_links(rom)
    paths, nodes = catalogue_paths(rom, catalogue)
    shapes = raw_script_shapes(rom, incoming, nodes)
    native = native_evidence(rom, reference)
    return {'source_sha256': digest, 'reference_sha256': hashlib.sha256(reference).hexdigest(),
            'scope': 'Selected variants 3:107 and 3:111, with 3:101 and 3:99 as comparison destinations. Physical group/bank pointer prefixes only; candidate slots and parsing failures are not a complete world-map certification. Warp and connection spans are parsed separately even when layouts/other arrays fail. Script traces cover only the prior 332 map-owned roots, plus bounded nearby raw-pointer targets for literal command shapes. All runtime reachability remains UNKNOWN.',
            'limits': {'bank_pointer_prefix_limit': 4096, 'connection_count_limit': 32,
                       'catalogue_trace_instructions': 256, 'catalogue_trace_states': 1024,
                       'trace_call_depth': 8,
                       'nearby_pointer_lookback': 512, 'nearby_pointer_roots_per_shape': 128,
                       'nearby_trace_instructions': 128, 'nearby_trace_states': 512,
                       'LZ77_pointer_target_lookback': 0x40000, 'LZ77_output_limit': 0x100000,
                       'native_constant_window_bytes': 32},
            'interpretation': 'CONFIRMED_IN_ROM: raw bytes, pointers, span/token checks and witnessed format paths. STRONGLY_INFERRED: FireRed field/command/native roles. Missing static evidence does not certify unused or unreachable maps.',
            'map_record_scan': scan, 'catalogue_paths': paths, 'raw_script_shapes': shapes,
            'header_pointer_evidence': header_pointer_evidence(rom, incoming, scan), 'native_probe': native,
            'summary': {'incoming_variant_warp_or_connection_associations': sum(r['destination_map'] in VARIANTS for r in scan['incoming_records']),
                        'raw_variant_script_shapes': len(shapes),
                        'raw_shape_contexts': dict(sorted(Counter(s['context_class'] for s in shapes).items())),
                        'shapes_on_catalogued_instruction_boundaries': sum(s['catalogue_instruction_boundary_match'] for s in shapes),
                        'nearby_pointer_format_witnesses_without_overlap': sum(a['witness'] is not None and not a['overlaps'] for s in shapes for a in s['pointer_target_path_attempts']),
                        **native['summary']}}


def write_outputs(data):
    (ROOT / 'extracted/maps/map_selection_audit.json').write_text(json.dumps(data, indent=2) + '\n')
    with (ROOT / 'extracted/maps/map_selection_incoming.csv').open('w', newline='') as stream:
        fields = ['source_group', 'source_map', 'kind', 'index', 'offset', 'destination_group', 'destination_map', 'destination_warp', 'source_evidence', 'reachability']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in data['map_record_scan']['incoming_records']:
            writer.writerow({k: f"0x{row[k]:X}" if k == 'offset' else row[k] for k in fields})
    lines = ['# Map variant selection audit', '', f"Source SHA-256: `{data['source_sha256']}`.", '',
             data['scope'], '', data['interpretation'], '', '```json', json.dumps(data['summary'], indent=2), '```', '',
             '## What the wider record scan establishes', '',
             'Native table discovery yields 43 pointer-prefix groups and 1,504 candidate slots. Some slots are malformed, dummy or possible physical-prefix overrun candidates; the scan preserves their individual failures. It does not certify 1,504 real maps. Layout validation is recorded separately so a bad layout cannot suppress a readable warp/connection span.', '',
             'No parsed literal warp/connection record in that scope targets `3:107` or `3:111`. Among sources with validated headers, three associations target `3:99` and six target `3:101`, including an additional `5:132` warp outside the prior 32-map cohort. Eight additional weak matches to `3:99` all reuse bytes at `0x170C7E` through the same unsuitable header `0x3525E4` in overlapping physical-prefix tails of groups 35–42; they are retained as unvalidated span evidence, not certified maps or warps. The large span-record total includes unsuitable candidates and is not a count of real game warps.', '',
             '```json', json.dumps(data['map_record_scan']['summary'], indent=2), '```', '',
             '| Candidate source | Kind | Record | Destination | Source evidence |', '|---|---|---|---|---|']
    for row in data['map_record_scan']['incoming_records']:
        lines.append(f"| {row['source_group']}:{row['source_map']} | {row['kind']} | 0x{row['offset']:X} | 3:{row['destination_map']} | {row['source_evidence']} |")
    lines += ['', '## Literal script-shape triage', '',
              'The all-byte scan covers the retained ordinary script warp/destination-setter opcodes, including the shorter warphole form. Fourteen raw `opcode, group=3, map=107/111` shapes occur. Eight lie wholly in pointer-backed well-formed LZ77 token streams; two overlap ROM pointer words at `0x6F036C` and `0x6F0388` (each points to `0x6F033F`); four contexts remain unclassified. Stream/pointer evidence is recorded without assuming that data can never be aliased deliberately.', '',
              'None is an instruction boundary reached in the bounded 332-root catalogue search, or by the bounded nearby incoming-pointer-target searches. The catalogue paths decode 3,717 unique instruction candidates, with explicit unsupported/non-ROM frontiers. The four unclassified contexts are not silently rejected or promoted to scripts.', '',
              '| Raw offset | Opcode | Destination | Context |', '|---|---|---|---|']
    for row in data['raw_script_shapes']:
        lines.append(f"| 0x{row['offset']:X} | 0x{row['opcode']:02X} | {row['target_map']} | {row['context_class']} |")
    lines += ['', '## Header pointers and native evidence', '',
              'Route 54 variant header `0xC24978` has one all-alignment absolute ROM pointer, its native bank slot `0xC2B0B4`. Science Complex header `0xC313D0` has bank slot `0xC2B0C4` plus a data pointer at `0xC32A2C`. The latter is +12 inside a layout-shaped fragment beginning `0xC32A20` (68×42); no absolute ROM pointer to that fragment was found. This supplies data-geometry evidence, without a validated native code-literal use or indexed alternate-layout identity.', '',
              data['native_probe']['method'], '',
              'The setter target `0x5538C` comes from the last BL in the independently found setwarp handler; it is not guessed from the original FireRed address. Five setter-handler intervals compare equal to supplied FireRed. This supports local decoding, not every caller/callee behavior. There are 56 BL-shape sites to the selected lookup/setter/wrapper targets. Their prior 32 bytes contain no immediate/literal value 107 or 111 in the limited MOVS/LDR probe. Computed map IDs, nonlocal register assignments, alternative/native hooks and RAM data remain unresolved.', '',
              '## Conclusion and next step', '',
              'The inspected static topology selects the original Route 54/Route 53 IDs, while the two variants have no supported literal entry in this bounded audit. This supports treating them as candidate disconnected copies for further research; neither is certified unused, broken or runtime-unreachable. No map ID is removed or repurposed.', '',
              'Next bounded step: expand the Orange map inventory from Route 59’s outgoing links and catalogue the destination entry scripts, to follow surviving progression toward the beta dead end.', '',
              'Full evidence: `extracted/maps/map_selection_audit.json` and `map_selection_incoming.csv`; retained semantics in `research/warp_semantics_notes.md`, `src/scrcmd.c:719–865` and `asm/macros/event.inc`. All original source bytes remain untouched.']
    (ROOT / 'research/map_variant_selection.md').write_text('\n'.join(lines) + '\n')


def main():
    rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
    reference = (ROOT / 'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    catalogue = json.loads((ROOT / 'extracted/scripts/map_script_catalogue.json').read_text())
    data = build(rom, reference, catalogue)
    write_outputs(data)
    print(json.dumps({'summary': data['summary'], 'record_scan': data['map_record_scan']['summary'],
                      'catalogue_paths': data['catalogue_paths']['summary']}, indent=2))


if __name__ == '__main__':
    main()
