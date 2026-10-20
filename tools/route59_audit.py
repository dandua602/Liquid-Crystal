"""Route 59 destination links and map-owned progression evidence, read only."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from dialogue_cluster_audit import instruction
from engine_reference_probe import make_probe
from map_extract import FormatError
from script_extract import LOCAL_SPECS, TRANSFERS, WARP_NAMES, catalogue, focus_audit
from warp_graph import MapCatalog, connection_destination, in_layout, warp_destination

ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS = {(6, number) for number in range(28, 32)}
DESTINATION_IDS = {f'{g}:{m}' for g, m in DESTINATIONS}
ROUTE59_SPECS = {
    0x42: ('getplayerxy', (2, 2)), 0x43: ('getpartysize', ()),
    0x6E: ('yesnobox', (1, 1)), 0x6F: ('multichoice', (1, 1, 1, 1)),
    0x70: ('multichoicedefault', (1, 1, 1, 1, 1)),
    0x7D: ('bufferspeciesname', (1, 2)), 0x7F: ('bufferpartymonnick', (1, 2)),
    0x82: ('buffermovename', (1, 2)), 0x90: ('addmoney', (4, 1)),
    0x91: ('removemoney', (4, 1)), 0x92: ('checkmoney', (4, 1)),
    0x93: ('showmoneybox', (1, 1, 1)), 0x94: ('hidemoneybox', (1, 1)),
    0x95: ('updatemoneybox', (1, 1, 1))}
COMMAND_SPECS = {**LOCAL_SPECS, **ROUTE59_SPECS}


def decode_route59(rom, pc):
    result, error = instruction(rom, pc, specs=COMMAND_SPECS)
    if result:
        if result['opcode'] in TRANSFERS:
            result['resume_kind'] = 'assumed_resume_after_script_warp'
        elif result['opcode'] in (0x6E, 0x6F, 0x70):
            result['resume_kind'] = 'assumed_resume_after_choice_ui'
        elif result['opcode'] == 0x9E:
            result['resume_kind'] = 'assumed_resume_after_field_effect'
    return result, error


def script_destination(catalog, ins):
    values = ins['values']
    target = catalog.resolve(values[0], values[1])
    result = {'target_map': target['id'], 'status': 'unresolved',
              'raw_operands': values, 'runtime_execution': 'UNKNOWN'}
    if target['status'] != 'structure_validated':
        result['reason'] = target.get('reason', 'Target map did not validate')
        return result
    if len(values) == 2:
        result['reason'] = 'Hole warp needs current player coordinates or fixed-hole state'
        return result
    index = values[2]
    if index >= 128:
        result['reason'] = 'Nonindexed script warp needs VarGet coordinates; not emulated'
    elif index < len(target['warps']):
        result.update(status='indexed_target_warp_validated', landing=target['warps'][index],
                      landing_coordinates_in_default_layout=in_layout(target['warps'][index], target))
    else:
        result['reason'] = 'Target warp index outside exported count'
    return result


def build(rom, reference, previous):
    digest = hashlib.sha256(rom).hexdigest()
    if previous['source_sha256'] != digest:
        raise FormatError('Stale Route 59 source connectivity inventory')
    catalog = MapCatalog(rom)
    route = catalog.resolve(3, 110)
    old = next((m for m in previous['maps'] if m['id'] == '3:110'), None)
    if old is None or route['status'] != 'structure_validated' or old['header'] != route['header']:
        raise FormatError('Route 59 owner no longer validates')
    found = {(w['destination_group'], w['destination_map']) for w in route['warps']}
    if found != DESTINATIONS:
        raise FormatError('Route 59 outgoing destination set changed')
    rooms = [catalog.resolve(g, n) for g, n in sorted(DESTINATIONS)]
    if any(m['status'] != 'structure_validated' for m in rooms):
        raise FormatError('Selected Route 59 destination did not validate')
    scope = ('Four Route 59 destination maps only: 6:28–6:31. Every event and map-entry association is retained; '
             'all 15 unique roots are traced within 256 instructions, 1,024 states and call depth 8. '
             'No recursive world extraction or runtime-state simulation.')
    scripts = catalogue(rom, {'source_sha256': digest, 'maps': rooms}, focus_maps=DESTINATION_IDS, scope=scope)
    focus = focus_audit(rom, scripts, focus_maps=DESTINATION_IDS, decoder=decode_route59)
    edges = []
    for source in [route] + rooms:
        for kind, rows in [('warp', source['warps']), ('connection', source['connections'])]:
            for link in rows:
                target = catalog.resolve(link['destination_group'], link['destination_map'])
                destination = (warp_destination(link, source, target) if kind == 'warp'
                               else connection_destination(link, source, target))
                edges.append({'id': f"{source['id']}:{kind}:{link['index']}", 'source_map': source['id'],
                              'kind': kind, **link, 'destination': destination, 'reachability': 'UNKNOWN',
                              **({'source_coordinates_in_default_layout': in_layout(link, source)} if kind == 'warp' else {})})
    root_owners = {root['offset']: root['associations'] for root in scripts['roots']}
    transitions = []
    for trace in focus['traces']:
        for ins in trace['selected_gate_transition_native_candidates']:
            if ins['opcode'] not in set(WARP_NAMES) | {0x3C}:
                continue
            transitions.append({'root': trace['root'], 'command': ins['pc'], 'name': ins['name'],
                                'raw_hex': ins['raw_hex'], 'witness': ins['witness'],
                                'owner_associations': root_owners[trace['root']],
                                'destination': script_destination(catalog, ins), 'reachability': 'UNKNOWN'})
    events = [event for m in scripts['maps'] for event in m['events']]
    rom_start = [event for event in events if event['script_target'] == 0]
    used = {n['opcode'] for trace in focus['traces'] for n in trace['instructions']}
    probe = make_probe(reference, rom, used & (set(ROUTE59_SPECS) | {0x3D, 0x9C, 0x25, 0x27}))
    return {'source_sha256': digest, 'reference_sha256': hashlib.sha256(reference).hexdigest(),
            'scope': 'Route 59 plus its four direct destination maps supply static edges. Other map slots are landing/return context only; their outgoing graphs/scripts are not recursively expanded. Default layout validation does not resolve collision, movement, saved flags, map-entry activation or native effects. All gameplay reachability remains UNKNOWN.',
            'interpretation': 'CONFIRMED_IN_ROM: bytes, pointers, structural links and source ownership. STRONGLY_INFERRED: FireRed script/event/native meanings. No authored story or ROM/save changes.',
            'summary': {'new_destination_maps': len(rooms), 'graph_context_maps': len(catalog.maps),
                        'catalogued_event_records': len(events), 'script_associations': scripts['summary']['script_associations'],
                        'unique_script_roots': len(scripts['roots']), 'static_warp_edges': sum(e['kind'] == 'warp' for e in edges),
                        'static_connection_edges': sum(e['kind'] == 'connection' for e in edges),
                        'warp_return_relations': dict(sorted(Counter(e['destination'].get('return_relation', 'unresolved') for e in edges if e['kind'] == 'warp').items())),
                        'ROM_start_script_fields': len(rom_start), 'scripted_transition_instructions': len(transitions),
                        'scripted_transition_owner_associations': sum(len(t['owner_associations']) for t in transitions)},
            'maps': [catalog.maps[k] for k in sorted(catalog.maps)], 'edges': edges,
            'script_catalogue': scripts, 'script_traces': focus, 'scripted_transitions': transitions,
            'ROM_start_fields': rom_start, 'command_handler_probe': probe}


def write_outputs(data):
    (ROOT / 'extracted/maps/route59_destination_audit.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    with (ROOT / 'extracted/maps/route59_links.csv').open('w', newline='') as stream:
        fields = ['source_map', 'kind', 'index', 'offset', 'target_map', 'destination_warp', 'return_relation', 'reachability']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in data['edges']:
            result = {k: row.get(k, '') for k in fields}
            result.update(target_map=row['destination']['target_map'],
                          return_relation=row['destination'].get('return_relation', ''), offset=f"0x{row['offset']:X}")
            writer.writerow(result)
    with (ROOT / 'extracted/scripts/route59_script_associations.csv').open('w', newline='') as stream:
        fields = ['id', 'map_id', 'kind', 'pointer_site', 'script_target', 'activation']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for root in data['script_catalogue']['roots']:
            for a in root['associations']:
                writer.writerow({k: f"0x{a[k]:X}" if k in ('pointer_site', 'script_target') else
                                 json.dumps(a[k], sort_keys=True) if k == 'activation' else a[k] for k in fields})
    maps = {m['id']: m for m in data['maps']}
    traces = {t['root']: t for t in data['script_traces']['traces']}
    lines = ['# Route 59 destination and progression audit', '', f"Source SHA-256: `{data['source_sha256']}`.", '',
             data['scope'], '', data['interpretation'], '', '```json', json.dumps(data['summary'], indent=2), '```', '',
             '## Four destination maps', '', '| Map | Header | Default size | Objects / warps / coordinates / BG | Evidence-based role |', '|---|---|---|---|---|']
    roles = {'6:28': 'Gatehouse between Mandarin City and Route 59', '6:29': 'Black Flute seller house',
             '6:30': 'Underwater passages with emergence scripts', '6:31': 'Mister R introduction/puzzle room; completion unresolved'}
    for key in sorted(DESTINATION_IDS):
        m = maps[key]
        lines.append(f"| {key} | 0x{m['header']:X} | {m['width']}×{m['height']} | "+' / '.join(str(x) for x in m['events']['counts'])+f" | {roles[key]} |")
    lines += ['', 'All four share the ROUTE 59 section label; it is not a unique building name. All inspected default layouts match their native layout-ID slots. The graph retains legacy/dynamic targets separately.', '',
              '```mermaid', 'flowchart LR',
              '  M["Mandarin City · 3:109"] <--> G["Gatehouse · 6:28"]',
              '  G <--> R["Route 59 · 3:110"]',
              '  R <--> H["Seller · 6:29"]',
              '  R --> U["Underwater · 6:30"]',
              '  U -.->|two scripted emergence paths| R',
              '  R <--> P["Mister R room · 6:31"]', '```', '',
              'Arrows summarize encoded links only. The underwater map also has legacy exits; the diagram omits those to keep the progression lead readable.', '',
              '## New map-owned progression evidence', '',
              '- Gatehouse `6:28` warp 0 returns to Mandarin City `3:109` warp 2; warp 1 leads to Route 59 `3:110` warp 3. Both have exact encoded return records. NPC dialogue identifies the Science Complex beyond Route 59 and warns that the area is dangerous.',
              '- Seller `6:29` root `0xA9C566` checks flag `0x5C0`, displays an offer for a Black Flute, checks/removes 50,000 money (`0xC350`), supplies item tuple `0x2A × 1` through callstd 0, and sets flag `0x5C0` on the candidate success branch. The trace retains decline, insufficient-money and inventory-failure branches. Native/standard transaction execution is untested.',
              '- Underwater `6:30` has two distinct emergence roots, `0xAA087D` and `0xAE8C6D`, each owned by six BG records. Both check move operand `0x123`, branch on flag `0x1685` and a prompt result, run field effect `0x25`, wait, then use warpteleport. The commands at `0xAA08C1` / `0xAE8CB1` target Route 59 warps 1 / 4 respectively. Both indexed landings validate. Script conditions, the field effect and wait/resume remain assumptions.',
              '- Room `6:31` map table `0xC0AA14` (tag 2) points to condition table `0xC099F2`: VarGet(`0x5331`) == VarGet(0) selects `0xAE8D7A`. The intro sets operand `0x5331` to 1, shows Mister R dialogue, moves local object 1, then sets its visibility flag `0x5C5` at `0xAE8DB5` and removes it at `0xAE8DB8`. The complete local format trace contains no trainer-battle command. A promised battle in dialogue is not proof that a completion/battle script survives.', '',
              '## Mister R introduction text', '']
    for message in traces[0xAE8D7A]['messages']:
        if message['status'] == 'strict_complete_text':
            lines += [f"`0x{message['offset']:X}`", '', '```text', message['text'], '```', '']
    lines += ['## Structural concerns retained', '',
              '- Four interaction fields contain `0x08000000`, not null `0x00000000`: one object in `6:29`, one in `6:30`, and object 1 plus BG record 4 in `6:31`. They target ROM offset zero (reset-vector data), where this decoder stops at unsupported opcode FE. They remain explicit unresolved script candidates; they are not normalized into valid empty scripts.',
              '- Underwater warp 1 returns to Route 59 warp 2, whose outgoing record enters seller map `6:29`. Its BG emergence scripts instead target Route 59 warps 1/4. Six other underwater warp records point into older DARK CAVE, UNDERSEA CAVERN and ROUTE 34 map slots; their indexed landings validate but returns do not lead to `6:30`. Metatiles/activation must be checked before diagnosing or changing these rows.',
              '- Mister R room warp 1 targets `2:40` (GOLDENROD DEPT. section), whose landing row returns within the older department-store topology. The room retains a 6F shopping sign, Lucky Channel NPC and vending-machine scripts. Warp 2 targets `0:0` with a dynamically encoded return, which remains a supported special pattern rather than an invalid zero tuple.',
              '- Two hidden-item BG unions are exported as data, not script pointers. The coordinate event in `6:30` checks operand `0x4050` against zero and uses specials `0x114` / `0x113`; load script `0x974239` sets operands `0x4060/61/62` to `1/9/12`. Their native effects and current state are unresolved.', '',
              '## Trace and native comparison limits', '', '```json', json.dumps(data['script_traces']['summary'], indent=2), '```', '',
              'New UI/money/buffer command widths use pinned asm/macros/event.inc. The retained native handler-interval probe compares used new commands plus warpteleport, field-effect, special and wait handlers against supplied FireRed; helper code, runtime conditions, task effects and map collision are not emulated. All format edges retain assumptions around UI, standard/native calls, field effects and warp resumes.', '',
              'Next bounded step: audit Mister R room metatiles, movement data and interaction triggers, then search for a puzzle-completion/battle path tied to operand `0x5331` and flag `0x5C5`. Keep this separate from certifying the public beta dead end.', '',
              'Evidence files: `extracted/maps/route59_destination_audit.json`, `route59_links.csv`, and `extracted/scripts/route59_script_associations.csv`. This is a useful publication checkpoint: it adds a map-owned progression lead with tested extraction; no ROM/save changes or playable continuation are produced.']
    (ROOT / 'research/route59_progression.md').write_text('\n'.join(lines) + '\n')


def main():
    rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
    reference = (ROOT / 'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    previous = json.loads((ROOT / 'extracted/maps/controller_connectivity.json').read_text())
    data = build(rom, reference, previous)
    write_outputs(data)
    print(json.dumps({'summary': data['summary'], 'scripts': data['script_traces']['summary'],
                      'handler_comparisons': len(data['command_handler_probe']['handler_comparisons'])}, indent=2))


if __name__ == '__main__':
    main()
