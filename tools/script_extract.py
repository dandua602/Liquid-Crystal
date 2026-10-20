"""Map-bound event references and bounded script-format archaeology, read only."""
import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

from dialogue_cluster_audit import SPECS, instruction, trace_graph
from gba_text_codec import parse
from map_extract import FormatError, u32
from pointer_scan import BASE
from warp_graph import MapCatalog

ROOT = Path(__file__).resolve().parents[1]
MAP_TAGS = {1: 'on_load', 2: 'on_frame_table', 3: 'on_transition',
            4: 'on_warp_into_map_table', 5: 'on_resume', 6: 'on_dive_warp', 7: 'on_return_to_field'}
FOCUS_MAPS = {'3:99', '3:101', '3:107', '3:110', '3:111', '5:93', '5:95', '5:96'}
WARP_NAMES = {0x39: 'warp', 0x3A: 'warpsilent', 0x3B: 'warpdoor', 0x3D: 'warpteleport',
              0x3E: 'setwarp', 0x3F: 'setdynamicwarp', 0x40: 'setdivewarp',
              0x41: 'setholewarp', 0xC4: 'setescapewarp', 0xD1: 'warpspinenter'}
EXTRA_SPECS = {op: (name, (1, 1, 1, 2, 2)) for op, name in WARP_NAMES.items()}
EXTRA_SPECS.update({0x3C: ('warphole', (1, 1)), 0x7C: ('checkpartymove', (2,)),
                    0x1F: ('compare_ptr_to_value', (4, 1)),
                    0x80: ('bufferitemname', (1, 2)), 0x99: ('setflashlevel', (2,)),
                    0x9C: ('dofieldeffect', (2,)), 0x9D: ('setfieldeffectargument', (1, 2)),
                    0x9E: ('waitfieldeffect', (2,)),
                    0x9F: ('setrespawn', (2,)), 0xA7: ('setmaplayoutindex', (2,))})
LOCAL_SPECS = {**SPECS, **EXTRA_SPECS}
TRANSFERS = {0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0xD1}
GATE_OPS = {0x16, 0x17, 0x18, 0x19, 0x1A, 0x1F, 0x21, 0x22, 0x29, 0x2A, 0x2B,
            0x44, 0x45, 0x46, 0x47, 0x60, 0x61, 0x62, 0x7C, 0xA7}


def decode_script(rom, pc):
    result, error = instruction(rom, pc, specs=LOCAL_SPECS)
    if result and result['opcode'] in TRANSFERS:
        result['resume_kind'] = 'assumed_resume_after_script_warp'
    return result, error


def script_field(rom, site):
    word = u32(rom, site)
    if word == 0:
        status, target = 'null', None
    elif BASE <= word < BASE + len(rom):
        status, target = 'ROM_script_candidate', word - BASE
    else:
        status, target = 'non_ROM_script_word', None
    return {'pointer_site': site, 'raw_script_word': word, 'script_target': target, 'script_status': status}


def conditional_table(rom, start, limit=128):
    rows = []
    for index in range(limit):
        at = start + index * 8
        if at < 0 or at + 2 > len(rom):
            return {'entries': rows, 'terminated': False, 'stop_reason': 'out-of-ROM condition header'}
        first = struct.unpack_from('<H', rom, at)[0]
        if first == 0:
            return {'entries': rows, 'terminated': True, 'terminator': at, 'end': at + 2}
        if at + 8 > len(rom):
            return {'entries': rows, 'terminated': False, 'stop_reason': 'truncated condition entry'}
        second = struct.unpack_from('<H', rom, at + 2)[0]
        rows.append({'index': index, 'offset': at, 'operand_1': first, 'operand_2': second,
                     'condition': 'VarGet(operand_1) == VarGet(operand_2); first matching row selected',
                     'raw_hex': rom[at:at + 8].hex(' '), **script_field(rom, at + 4)})
    return {'entries': rows, 'terminated': False, 'stop_reason': 'condition entry scan limit'}


def map_script_table(rom, start, limit=64):
    if start is None:
        return {'entries': [], 'terminated': True, 'status': 'null map-script pointer'}
    rows = []
    seen = set()
    for index in range(limit):
        at = start + index * 5
        if at < 0 or at >= len(rom):
            return {'entries': rows, 'terminated': False, 'stop_reason': 'out-of-ROM tag'}
        tag = rom[at]
        if tag == 0:
            return {'entries': rows, 'terminated': True, 'terminator': at, 'end': at + 1}
        if at + 5 > len(rom):
            return {'entries': rows, 'terminated': False, 'stop_reason': 'truncated tag entry'}
        row = {'index': index, 'offset': at, 'tag': tag, 'tag_name': MAP_TAGS.get(tag, 'unknown_tag'),
               'first_entry_for_tag': tag not in seen, 'raw_hex': rom[at:at + 5].hex(' '),
               **script_field(rom, at + 1)}
        seen.add(tag)
        if tag in (2, 4) and row['script_target'] is not None:
            row['conditional_table'] = conditional_table(rom, row['script_target'])
        rows.append(row)
        # Unknown nonzero tags still consume five bytes in the reference scan.
    return {'entries': rows, 'terminated': False, 'stop_reason': 'map tag entry scan limit'}


def event_records(rom, m):
    rows = []
    ev = m['events']
    for kind, array_index, stride, delta in [('object', 0, 24, 16), ('coordinate', 2, 16, 12), ('background', 3, 12, 8)]:
        for index in range(ev['counts'][array_index]):
            at = ev['arrays'][array_index] + index * stride
            x, y = struct.unpack_from('<hh' if kind == 'object' else '<HH', rom, at + (4 if kind == 'object' else 0))
            row = {'id': f"{m['id']}:{kind}:{index}", 'map_id': m['id'], 'kind': kind, 'index': index,
                   'offset': at, 'x': x, 'y': y, 'coordinates_in_default_layout': 0 <= x < m['width'] and 0 <= y < m['height'],
                   'raw_hex': rom[at:at + stride].hex(' '), 'reachability': 'UNKNOWN'}
            if kind == 'object':
                row.update(local_id=rom[at], graphics_id=rom[at + 1], object_kind=rom[at + 2],
                           raw_script_word=u32(rom, at + 16), visibility_flag=struct.unpack_from('<H', rom, at + 20)[0])
                if row['object_kind'] == 255:
                    row.update(target_local_id=rom[at + 8], target_map=struct.unpack_from('<H', rom, at + 12)[0],
                               target_group=struct.unpack_from('<H', rom, at + 14)[0], script_target=None,
                               script_status='clone_indirect_unresolved')
                else:
                    row.update(script_field(rom, at + delta))
                    row.update(elevation=rom[at + 8], movement_type=rom[at + 9],
                               trainer_type=struct.unpack_from('<H', rom, at + 12)[0],
                               trainer_range=struct.unpack_from('<H', rom, at + 14)[0])
                    if row['object_kind'] != 0:
                        row['object_kind_note'] = 'unrecognized kind; reference script field retained as candidate'
            elif kind == 'coordinate':
                trigger, value = struct.unpack_from('<HH', rom, at + 6)
                row.update(elevation=rom[at + 4], trigger_operand=trigger, trigger_value_raw=value,
                           trigger_value_compared_low_byte=value & 255, **script_field(rom, at + delta))
                row['activation_reference'] = ('null script: weather trigger' if row['script_target'] is None and row['raw_script_word'] == 0
                                               else 'trigger zero: immediate script' if trigger == 0
                                               else 'VarGet(trigger_operand) == low byte of trigger_value_raw')
            else:
                event_kind = rom[at + 5]
                row.update(elevation=rom[at + 4], background_kind=event_kind, union_word=u32(rom, at + 8))
                if event_kind in (5, 6, 7):
                    row.update(script_target=None, script_status='hidden_item_union_not_script')
                else:
                    row.update(script_field(rom, at + delta))
                    if event_kind > 7:
                        row['background_kind_note'] = 'unknown kind; reference default branch uses script union'
            rows.append(row)
    return rows


def catalogue(rom, connectivity, focus_maps=None, scope=None):
    focus_maps = FOCUS_MAPS if focus_maps is None else set(focus_maps)
    digest = hashlib.sha256(rom).hexdigest()
    if connectivity['source_sha256'] != digest:
        raise FormatError('Stale connectivity scope')
    catalog = MapCatalog(rom)
    maps, associations = [], []
    for old in connectivity['maps']:
        m = catalog.resolve(old['group'], old['map'])
        if m['status'] != 'structure_validated' or m['header'] != old['header']:
            raise FormatError('Connectivity-scope map no longer validates')
        events = event_records(rom, m)
        table = map_script_table(rom, m['map_scripts'])
        maps.append({'id': m['id'], 'header': m['header'], 'section_label': m['section_label']['text'],
                     'events_structure': m['events'], 'map_scripts_pointer': m['map_scripts'],
                     'events': events, 'map_script_table': table, 'reachability': 'UNKNOWN'})
        for event in events:
            if event['script_target'] is not None:
                associations.append({'id': event['id'], 'map_id': m['id'], 'kind': event['kind'],
                                     'pointer_site': event['pointer_site'], 'script_target': event['script_target'],
                                     'event_offset': event['offset'], 'activation': {k: event[k] for k in
                                         ('visibility_flag', 'trigger_operand', 'trigger_value_raw', 'trigger_value_compared_low_byte', 'background_kind') if k in event}})
        for entry in table['entries']:
            if entry['tag'] not in MAP_TAGS or not entry['first_entry_for_tag']:
                continue
            conditional = entry.get('conditional_table')
            candidates = conditional['entries'] if conditional is not None else [entry]
            for c in candidates:
                if c['script_target'] is None:
                    continue
                associations.append({'id': f"{m['id']}:map_entry:{entry['index']}" + (f":condition:{c['index']}" if conditional else ''),
                                     'map_id': m['id'], 'kind': 'map_entry', 'tag': entry['tag'], 'tag_name': entry['tag_name'],
                                     'entry_offset': entry['offset'], 'pointer_site': c['pointer_site'], 'script_target': c['script_target'],
                                     'activation': {k: c[k] for k in ('operand_1', 'operand_2', 'condition') if k in c}})
    root_owners = {}
    for a in associations:
        root_owners.setdefault(a['script_target'], []).append(a)
    roots = [{'offset': target, 'associations': owners, 'focus_scope': any(o['map_id'] in focus_maps for o in owners),
              'reachability': 'UNKNOWN'} for target, owners in sorted(root_owners.items())]
    comparisons = []
    by_id = {m['id']: m for m in maps}
    for a, b in [('3:101', '3:107'), ('3:99', '3:111')]:
        if a not in by_id or b not in by_id:
            continue
        first, second = by_id[a], by_id[b]
        comparisons.append({'maps': [a, b], 'same_map_script_pointer': first['map_scripts_pointer'] == second['map_scripts_pointer'],
                            'event_record_counts': [len(first['events']), len(second['events'])],
                            'event_record_raw_differences': [i for i, (x, y) in enumerate(zip(first['events'], second['events'])) if x['raw_hex'] != y['raw_hex']],
                            'interpretation': 'Byte/association comparison only; map IDs remain distinct and runtime selection is UNKNOWN'})
    return {'source_sha256': digest, 'scope': scope if scope is not None else 'All event/script pointer fields and map-script tables in the 32-slot connectivity scope. All associations preserved. Focused format traces only for Route 54/Science Complex, comparison maps and direct cave destinations; no recursive world or full progression extraction.',
            'interpretation': 'CONFIRMED_IN_ROM: bytes, pointer chains and associations. STRONGLY_INFERRED: field roles and execution rules from pinned FireRed. No runtime accessibility or unused-content certification.',
            'limits': {'map_script_entries_per_map': 64, 'conditional_entries_per_table': 128,
                       'instructions_per_focus_root': 256, 'states_per_focus_root': 1024, 'call_depth': 8},
            'summary': {'map_slots': len(maps), 'event_records': sum(len(m['events']) for m in maps),
                        'event_kinds': dict(sorted(Counter(e['kind'] for m in maps for e in m['events']).items())),
                        'event_script_statuses': dict(sorted(Counter(e['script_status'] for m in maps for e in m['events']).items())),
                        'script_associations': len(associations), 'unique_script_roots': len(roots),
                        'map_entry_script_associations': sum(a['kind'] == 'map_entry' for a in associations),
                        'unknown_map_script_tag_records': sum(e['tag'] not in MAP_TAGS for m in maps for e in m['map_script_table']['entries']),
                        'unterminated_map_tables': sum(not m['map_script_table']['terminated'] for m in maps)},
            'alias_comparisons': comparisons, 'maps': maps, 'roots': roots}


def focus_audit(rom, data, focus_maps=None, decoder=None):
    focus_maps = FOCUS_MAPS if focus_maps is None else set(focus_maps)
    decoder = decode_script if decoder is None else decoder
    traces = []
    for root in data['roots']:
        if not any(a['map_id'] in focus_maps for a in root['associations']):
            continue
        graph = trace_graph(rom, root['offset'], max_instructions=256, max_states=1024, decoder=decoder)
        selected = []
        messages = {}
        for n in sorted(graph['nodes'].values(), key=lambda n: n['pc']):
            for reference in n['texts']:
                target = reference['target']
                if target not in messages:
                    p = parse(rom, target, strict_english=True) if 0 <= target < len(rom) else None
                    valid = bool(p and p['terminated'] and not p['issues'])
                    messages[target] = {'offset': target, 'status': 'strict_complete_text' if valid else 'unparsed_or_incomplete',
                                        'references': []}
                    if valid:
                        messages[target].update(text=p['text'], plain_text=p['plain'], end=p['end'],
                                                sha256=hashlib.sha256(rom[target:p['end']]).hexdigest())
                messages[target]['references'].append({'command': n['pc'], **reference})
            if n['opcode'] not in GATE_OPS | set(WARP_NAMES) | {0x3C, 0x23, 0x24, 0x25, 0x26}:
                continue
            record = {**n, 'witness': graph['witness'](n['pc'])}
            if n['opcode'] in WARP_NAMES or n['opcode'] == 0x3C:
                v = n['values']
                record['destination_encoding'] = {'group': v[0], 'map': v[1],
                                                   'warp_id': v[2] if len(v) > 2 else None,
                                                   'x_operand': v[3] if len(v) > 3 else None,
                                                   'y_operand': v[4] if len(v) > 4 else None,
                                                   'runtime_resolution': 'UNKNOWN; VarGet coordinates, setters and native warp execution not simulated'}
            selected.append(record)
        traces.append({'root': root['offset'], 'association_ids': [o['id'] for o in root['associations']],
                       'instructions': sorted(graph['nodes'].values(), key=lambda n: n['pc']),
                       'edges': list({(e['source'], e['target'], e['kind']): e for e in graph['edges']}.values()),
                       'selected_gate_transition_native_candidates': selected,
                       'messages': list(messages.values()),
                       'frontiers': graph['frontiers'], 'instruction_overlaps': graph['overlaps'],
                       'state_count': graph['state_count'], 'reachability': 'UNKNOWN'})
    nodes = {n['pc']: n for t in traces for n in t['instructions']}
    return {'source_sha256': data['source_sha256'], 'focus_map_ids': sorted(focus_maps), 'limits': data['limits'],
            'method': 'Stack-aware bounded format traces from map-owned references. Both condition outcomes retained. Standard/native/battle/warp returns are assumptions; condition values, collision and saved state are not simulated. Unsupported opcodes stop paths and remain frontiers. Shared roots and shared physical records preserve every owner association.',
            'summary': {'focus_roots': len(traces), 'unique_instruction_candidates': len(nodes),
                        'transition_or_destination_setter_instructions': sum(n['opcode'] in set(WARP_NAMES) | {0x3C} for n in nodes.values()),
                        'layout_setter_instructions': sum(n['opcode'] == 0xA7 for n in nodes.values()),
                        'unique_strict_complete_messages': len({m['offset'] for t in traces for m in t['messages'] if m['status'] == 'strict_complete_text'}),
                        'instruction_overlap_records': sum(len(t['instruction_overlaps']) for t in traces),
                        'frontier_reasons': dict(sorted(Counter(f['reason'] for t in traces for f in t['frontiers']).items()))},
            'traces': traces}


def write_outputs(data, focus):
    base = ROOT / 'extracted/scripts'
    base.mkdir(exist_ok=True)
    (base / 'map_script_catalogue.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (base / 'route54_science_script_audit.json').write_text(json.dumps(focus, ensure_ascii=False, indent=2) + '\n')
    with (base / 'map_script_associations.csv').open('w', newline='') as stream:
        fields = ['map_id', 'kind', 'id', 'pointer_site', 'script_target', 'activation']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for root in data['roots']:
            for a in root['associations']:
                writer.writerow({k: (f"0x{a[k]:X}" if k in ('pointer_site', 'script_target') else
                                     json.dumps(a[k], sort_keys=True) if k == 'activation' else a[k]) for k in fields})
    lines = ['# Orange candidate map script catalogue', '', f"Source SHA-256: `{data['source_sha256']}`.", '',
             data['scope'], '', data['interpretation'], '', '```json', json.dumps(data['summary'], indent=2), '```', '',
             '## Per-map records', '', '| Map | Section label | Objects / coordinates / BG | Map-script tags |', '|---|---|---|---|']
    for m in data['maps']:
        kinds = Counter(e['kind'] for e in m['events'])
        tags = ', '.join(f"{e['tag']} ({e['tag_name']})" for e in m['map_script_table']['entries']) or 'none'
        lines.append(f"| {m['id']} | {m['section_label']} | {kinds['object']} / {kinds['coordinate']} / {kinds['background']} | {tags} |")
    lines += ['', '## Interpretation limits', '',
              'Object visibility flags, coordinate trigger operands and BG facing kinds are exported, not solved. BG kinds 5/6/7 contain hidden-item data and are not treated as script pointers. Object clones are explicitly unresolved if encountered; none are silently interpreted as normal objects.', '',
              'Map-script tags use 5-byte entries ending only at tag zero. Unknown nonzero tags are retained and skipped by that format; they are not used as script roots. Only the first entry for a requested tag is selected in the reference. Types 2/4 point to 8-byte condition rows ending at a zero first operand; each compares VarGet of both operands. Coordinate events instead compare the low byte of their raw index operand. Runtime LC handlers have not all been verified.', '',
              '## Focused traces', '', focus['method'], '', '```json', json.dumps(focus['summary'], indent=2), '```', '',
              'Trace evidence: `extracted/scripts/route54_science_script_audit.json`. All instruction bytes, control edges, stop frontiers, owner association IDs and witness paths to selected state/transition/native candidates are retained. An unsupported opcode or assumed native return is not a game bug.', '',
              'Pinned structure/execution references: `include/global.fieldmap.h`; `src/script.c:382–486`; `src/field_control_avatar.c:463–519,1025–1063`; `src/event_object_movement.c:1312–1341,2509–2516`; `asm/macros/map.inc`; `asm/macros/event.inc`. Full provenance and hashes are in `research/references/manifest.json`.']
    (ROOT / 'research/orange_script_inventory.md').write_text('\n'.join(lines) + '\n')
    write_focus_findings(data, focus)


def write_focus_findings(data, focus):
    gate = next(t for t in focus['traces'] if t['root'] == 0xA7094D)
    lines = ['# Route 54 and Science Complex: script ownership findings', '',
             f"Source SHA-256: `{data['source_sha256']}`.", '',
             'CONFIRMED_IN_ROM: records, bytes, exact reuse and pointer ownership. STRONGLY_INFERRED: opcode/event semantics from pinned FireRed references. No emulator/playthrough, active save state or map-selection proof.', '',
             '## Shared Route 54 gate', '',
             'Both `3:101` and `3:107` have the same map-script table at `0x721A70`. Tag 2 points to conditional table `0x721D62`; its first row is operands `0x5305`, `0x0000` and script `0xA7094D`. The reference compares VarGet of both operands, then selects the first matching row.', '',
             'The bounded path at `0xA7094D` sets operand `0x5305` to 1; moves object 6; removes object 6 at `0xA7099A`; moves object 5; removes object 5 at `0xA709BF`; sets flag `0x52E` at `0xA709C2`; then releases/ends. Both maps have local IDs 5/6 with visibility flag `0x52E`, at `(7,21)` and `(8,21)`. Their own script fields are null, while the map frame-script supplies this candidate blocker-removal event.', '',
             'This gate is shared by both map IDs. It does not by itself explain which Route 54 variant is entered in gameplay. No warp or layout setter occurs in this complete local format path; movement, standard message routines and engine execution remain untested.', '',
             'Dialogue referenced by that path:', '']
    for message in gate['messages']:
        if message['status'] == 'strict_complete_text':
            lines += [f"`0x{message['offset']:X}`", '', '```text', message['text'], '```', '']
    lines += ['## Reused Science Complex event data', '',
              'Slots `3:99` (ROUTE 53 section) and `3:111` (SCIENCE COMPLEX section) have distinct map identities and layouts but the same map-script pointer `0x720AB4`. Their 14 object records and six BG records are byte-identical. This reuse is preserved as separate owner associations, not evidence that either slot is unused.', '',
              'Object local IDs 1–8 and 10 carry visibility flag `0x513`; ID 9 carries `0x51C`; IDs 11–14 carry `0x542`. The ordinary script at `0xA60DC3` is owned by both maps and by cave `5:93` object 1; it branches on flag `0x513` to two message paths. This adds map ownership to previously observed Mister G/Nexus state, without establishing the active state of an uploaded save.', '',
              'The six BG records comprise two null script fields, two Route 53 signposts pointing to `0xA24A7B`, and controllers `0xAD3E2C` / `0xAD3E52`. The signposts still name Route 53 in both map slots. Controller shutdown/status paths use the previously catalogued Nexus state (including flags `0x514` and `0x544`), with no new flag allocation or behavior change.', '',
              '## Limits of the transition search', '',
              f"The focused search traces {focus['summary']['focus_roots']} unique roots owned by eight focus maps, from {data['summary']['unique_script_roots']} roots catalogued across 32 map slots. It decodes {focus['summary']['unique_instruction_candidates']} unique instruction candidates. No explicit script-warp/destination setter or layout setter was decoded in that bounded subset.", '',
              'This does not prove those transitions absent: the shared load script at `0x8C457D` enters global helpers and stops at unsupported commands; native/standard calls and battle/wait resumes are assumptions. Other catalogued roots and native/map-selection paths have not been traced. Each frontier remains in the JSON. The earlier asymmetric warp/connection records still require caller and entry-route investigation.', '',
              '```json', json.dumps(focus['summary'], indent=2), '```', '',
              '## Alias checks', '', '```json', json.dumps(data['alias_comparisons'], indent=2), '```', '',
              'All 555 exported event coordinates fit the inspected default layouts; saved/script layout overrides and actual accessibility remain unknown. Five hidden-item unions are retained without fabricating script pointers. Fourteen unknown map-script tags are exported, including eight encountered by the bounded scan from `0:0`; none become script roots.', '',
              'Next bounded step: trace script and native references that select Route 54 `3:107` and Science Complex `3:111`, preserving the distinction between raw pointer occurrences, executable transition operands and actual playable entry.', '',
              'Full evidence: `extracted/scripts/map_script_catalogue.json`, `map_script_associations.csv` and `route54_science_script_audit.json`. No ROM/save bytes changed; no content certified unused, broken or runtime-unreachable.']
    (ROOT / 'research/route54_science_script_findings.md').write_text('\n'.join(lines) + '\n')


def main():
    rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
    connectivity = json.loads((ROOT / 'extracted/maps/controller_connectivity.json').read_text())
    data = catalogue(rom, connectivity)
    focus = focus_audit(rom, data)
    write_outputs(data, focus)
    print(json.dumps({'catalogue': data['summary'], 'focus': focus['summary']}, indent=2))


if __name__ == '__main__':
    main()
