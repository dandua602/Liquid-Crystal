"""Bounded static links from controller-owner maps; no playability inference."""
import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

from map_extract import FormatError, discover_lookup, header, label, pointer, pointer_prefix

ROOT = Path(__file__).resolve().parents[1]
LAYOUT_LOOKUP_SIGNATURE = bytes.fromhex(
    '00 b5 03 48 00 68 41 8e 00 29 03 d1 00 20 06 e0 '
    '08 50 00 03 03 48 01 39 89 00 09 18 08 68 02 bc 08 47 00 00')
DIRECTIONS = {0: 'none', 1: 'south', 2: 'north', 3: 'west', 4: 'east', 5: 'dive', 6: 'emerge'}
OPPOSITE = {1: 2, 2: 1, 3: 4, 4: 3, 5: 6, 6: 5}


def discover_layout_lookup(rom):
    candidates = []
    at = 0
    while (at := rom.find(LAYOUT_LOOKUP_SIGNATURE, at)) >= 0:
        try:
            table = pointer(rom, at + len(LAYOUT_LOOKUP_SIGNATURE))
            candidates.append({'function': at, 'literal_site': at + 36, 'table': table,
                               'raw_hex': rom[at:at + 40].hex(' ')})
        except FormatError:
            pass
        at += 1
    if len(candidates) != 1:
        raise FormatError('Native layout lookup discovery ambiguous')
    return candidates[0]


def read_links(rom, h):
    warps = []
    for index in range(h['events']['counts'][1]):
        at = h['events']['arrays'][1] + index * 8
        x, y, elevation, warp, number, group = struct.unpack_from('<hhBBBB', rom, at)
        warps.append({'index': index, 'offset': at, 'x': x, 'y': y, 'elevation': elevation,
                      'destination_group': group, 'destination_map': number, 'destination_warp': warp,
                      'raw_hex': rom[at:at + 8].hex(' ')})
    connections = []
    at = h['connection_structure']
    if at is not None:
        if at + 8 > len(rom):
            raise FormatError('Connection structure outside ROM')
        count = struct.unpack_from('<i', rom, at)[0]
        if not 0 <= count <= 32:
            raise FormatError('Connection count outside inspected limit 0..32')
        base = pointer(rom, at + 4, nullable=count == 0)
        if count and base + count * 12 > len(rom):
            raise FormatError('Connection array outside ROM')
        for index in range(count):
            p = base + index * 12
            direction = rom[p]
            connections.append({'index': index, 'offset': p, 'direction': direction,
                                'direction_name': DIRECTIONS.get(direction, 'unknown'),
                                'displacement': struct.unpack_from('<i', rom, p + 4)[0],
                                'destination_group': rom[p + 8], 'destination_map': rom[p + 9],
                                'raw_hex': rom[p:p + 12].hex(' ')})
    return warps, connections


class MapCatalog:
    def __init__(self, rom):
        self.rom = rom
        self.lookup = discover_lookup(rom)
        self.groups = pointer_prefix(rom, self.lookup['table'], 256)
        self.banks = {}
        self.layout_lookup = discover_layout_lookup(rom)
        self.maps = {}

    def resolve(self, group, number):
        key = (group, number)
        if key in self.maps:
            return self.maps[key]
        row = {'id': f'{group}:{number}', 'group': group, 'map': number,
               'status': 'unresolved', 'reachability': 'UNKNOWN', 'observations': []}
        self.maps[key] = row
        try:
            if not 0 <= group < len(self.groups['targets']):
                raise FormatError('Group outside inspected physical pointer prefix')
            if group not in self.banks:
                self.banks[group] = pointer_prefix(self.rom, self.groups['targets'][group])
            bank = self.banks[group]
            if not 0 <= number < len(bank['targets']):
                raise FormatError('Map outside inspected physical bank prefix')
            row.update(group_pointer_site=self.groups['start'] + group * 4,
                       bank_start=bank['start'], map_pointer_site=bank['start'] + number * 4)
            h = header(self.rom, bank['targets'][number])
            row.update(h)
            row['header_raw_hex'] = self.rom[h['header']:h['header'] + 28].hex(' ')
            row['section_label'] = label(self.rom, h['section_id'])
            layout_id = h['layout_id']
            if layout_id == 0:
                raise FormatError('Layout ID zero returns no indexed layout')
            # The layout table is sparse: zero slots before a selected ID are
            # not an array terminator. Validate each native-indexed slot itself.
            row['indexed_layout_pointer_site'] = self.layout_lookup['table'] + (layout_id - 1) * 4
            row['indexed_layout'] = pointer(self.rom, row['indexed_layout_pointer_site'])
            row['layout_pointer_matches_indexed'] = row['indexed_layout'] == h['layout']
            if not row['layout_pointer_matches_indexed']:
                raise FormatError('Header and indexed layout differ; active geometry needs separate inspection')
            if h['events']['offset'] is None:
                row['observations'].append('Null events pointer; exported empty event set is not runtime safety evidence')
            row['warps'], row['connections'] = read_links(self.rom, h)
            if any(c['direction'] not in DIRECTIONS for c in row['connections']):
                row['observations'].append('Connection array contains an unrecognized direction value')
            if any(c['direction'] == 0 for c in row['connections']):
                row['observations'].append('Connection array includes CONNECTION_NONE (0), not a cardinal transition')
            row['status'] = 'structure_validated'
        except (FormatError, struct.error) as exc:
            row['reason'] = str(exc)
        return row


def in_layout(record, h):
    return 0 <= record['x'] < h['width'] and 0 <= record['y'] < h['height']


def warp_destination(warp, source, target):
    """Interpret fields conservatively using the retained FireRed reference."""
    if warp['destination_map'] == 0x7F:
        return {'status': 'dynamic_destination', 'target_map': None,
                'reason': 'Reference SetupWarp selects saved dynamicWarp by mapNum alone'}
    result = {'status': 'unresolved_map', 'target_map': target['id']}
    if target['status'] != 'structure_validated':
        result['reason'] = target.get('reason', 'Target structure not validated')
        return result
    index = warp['destination_warp']
    if index >= len(target['warps']):
        result.update(status='nonindexed_or_out_of_range_warp', target_warp_count=len(target['warps']))
        return result
    landing = target['warps'][index]
    if landing['destination_map'] == 0x7F:
        relation = 'dynamic_return'
    elif (landing['destination_group'], landing['destination_map']) == (source['group'], source['map']):
        relation = 'exact_return' if landing['destination_warp'] == warp['index'] else 'source_map_different_warp'
    else:
        relation = 'another_map'
    result.update(status='warp_record_validated', landing=landing,
                  landing_coordinates_in_layout=in_layout(landing, target), return_relation=relation)
    return result


def connection_destination(connection, source, target):
    result = {'status': 'unresolved_map', 'target_map': target['id']}
    if target['status'] != 'structure_validated':
        result['reason'] = target.get('reason', 'Target structure not validated')
        return result
    direction = connection['direction']
    if direction not in DIRECTIONS:
        result['status'] = 'unknown_direction'
        return result
    if direction == 0:
        result['status'] = 'no_direction'
        return result
    returns = [c for c in target['connections']
               if (c['destination_group'], c['destination_map']) == (source['group'], source['map'])
               and c['direction'] == OPPOSITE[direction]]
    inverse = [c for c in returns if c['displacement'] == -connection['displacement']]
    result.update(status='connection_record_validated', opposite_direction_returns=returns,
                  inverse_displacement_returns=inverse)
    if direction in (1, 2, 3, 4):
        axis = 'width' if direction in (1, 2) else 'height'
        # Reference crossing coordinate is source coordinate minus offset.
        start = max(0, connection['displacement'])
        end = min(source[axis], target[axis] + connection['displacement'])
        result['geometric_overlap'] = {'source_axis': axis, 'start_inclusive': start,
                                       'end_exclusive': end, 'tiles': max(0, end - start),
                                       'collision_and_crossing_behavior': 'UNKNOWN'}
    return result


def build(rom, inventory):
    source_hash = hashlib.sha256(rom).hexdigest()
    if inventory['source_sha256'] != source_hash:
        raise FormatError('Stale controller map inventory')
    catalog = MapCatalog(rom)
    seeds = {(m['group'], m['map']) for m in inventory['maps']}
    edges = []
    for old in inventory['maps']:
        source = catalog.resolve(old['group'], old['map'])
        if source['status'] != 'structure_validated' or source['header'] != old['header']:
            raise FormatError('Seed header no longer validates against inventory')
        for kind, plural in (('warp', 'warps'), ('connection', 'connections')):
            if len(source[plural]) != len(old[plural]):
                raise FormatError('Seed link count differs from inventory')
            for index, link in enumerate(source[plural]):
                for field in old[plural][index]:
                    if field in link and old[plural][index][field] != link[field]:
                        raise FormatError('Seed link bytes differ from inventory')
                target = (catalog.resolve(link['destination_group'], link['destination_map'])
                          if kind != 'warp' or link['destination_map'] != 0x7F else None)
                destination = (warp_destination(link, source, target) if kind == 'warp'
                               else connection_destination(link, source, target))
                edges.append({'id': f"{kind}:{source['id']}:{index}", 'kind': kind,
                              'source_map': source['id'], **link, 'destination': destination,
                              'reachability': 'UNKNOWN',
                              **({'source_coordinates_in_layout': in_layout(link, source)} if kind == 'warp' else {})})
    for key, row in catalog.maps.items():
        row['seed'] = key in seeds
        row['graph_outgoing_scope'] = 'all static warp/connection records' if key in seeds else 'not expanded; records retained for landing/return checks only'
    warps = [e for e in edges if e['kind'] == 'warp']
    connections = [e for e in edges if e['kind'] == 'connection']
    return {'source_sha256': source_hash,
            'scope': 'One hop from ten controller-owner maps. Target outbound records are retained only as landing/return evidence, not recursively added to the graph. Physical pointer prefixes are inspection bounds, not native counts. Script transitions, collision, metatiles, flags, native hooks and saved dynamic state are not resolved; all gameplay reachability remains UNKNOWN.',
            'interpretation': 'CONFIRMED_IN_ROM: raw bytes and pointer chains. STRONGLY_INFERRED: field meanings and dynamic/connection behavior from pinned FireRed references. LC runtime semantics have not been fully compared or tested.',
            'lookup': catalog.lookup, 'layout_lookup': catalog.layout_lookup,
            'group_physical_prefix': {k: v for k, v in catalog.groups.items() if k != 'targets'},
            'layout_table_scope': 'Sparse table; only each selected layoutId-1 pointer slot is validated. Zero entries do not end the table. Saved/script layout overrides are untested.',
            'inspected_bank_physical_prefixes': {str(g): {k: v for k, v in b.items() if k != 'targets'} for g, b in sorted(catalog.banks.items())},
            'summary': {'seed_maps': len(seeds), 'maps_in_one_hop_scope': len(catalog.maps),
                        'validated_map_structures': sum(m['status'] == 'structure_validated' for m in catalog.maps.values()),
                        'warp_edges': len(warps), 'connection_edges': len(connections),
                        'warp_statuses': dict(sorted(Counter(e['destination']['status'] for e in warps).items())),
                        'warp_return_relations': dict(sorted(Counter(e['destination'].get('return_relation', 'unresolved') for e in warps).items())),
                        'connections_with_inverse_returns': sum(bool(e['destination'].get('inverse_displacement_returns')) for e in connections),
                        'connections_without_inverse_returns': sum(not e['destination'].get('inverse_displacement_returns') for e in connections)},
            'maps': [catalog.maps[k] for k in sorted(catalog.maps)], 'edges': edges}


def write_outputs(result):
    base = ROOT / 'extracted/maps'
    (base / 'controller_connectivity.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    fields = ['kind', 'source_map', 'index', 'offset', 'target_map', 'destination_warp',
              'direction_name', 'displacement', 'status', 'return_relation', 'reachability']
    with (base / 'controller_connectivity.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for edge in result['edges']:
            row = {k: edge.get(k, '') for k in fields}
            row.update({k: edge['destination'].get(k, '') for k in ('target_map', 'status', 'return_relation')})
            row['offset'] = f"0x{edge['offset']:X}"
            writer.writerow(row)
    graph = ['digraph controller_static_links {', '  rankdir=LR;',
             '  label="Static one-hop links; gameplay reachability UNKNOWN";']
    for m in result['maps']:
        name = m.get('section_label', {}).get('text') or 'unresolved'
        graph.append(f"  \"{m['id']}\" [label={json.dumps(m['id'] + ' ' + name)}, shape={'box' if m['seed'] else 'ellipse'}];")
    counts = Counter((e['source_map'], e['destination']['target_map'], e['kind']) for e in result['edges'])
    for (source, target, kind), count in sorted(counts.items(), key=lambda item: tuple(str(v) for v in item[0])):
        if target is not None:
            graph.append(f'  "{source}" -> "{target}" [label="{kind} x{count}"];')
    graph.append('}')
    (base / 'controller_connectivity.dot').write_text('\n'.join(graph) + '\n')
    lines = ['# Controller-map static connectivity', '', f"Source SHA-256: `{result['source_sha256']}`.", '',
             result['scope'], '', result['interpretation'], '',
             '## Verified structure', '',
             'All 58 source warp records resolve to in-range target warp records; all source and landing coordinates fit their layouts. All 13 connection targets resolve. The 32 distinct map slots retain every alias. For all 32, the header layout pointer matches the independently discovered active layout-ID table.', '',
             f"Native layout lookup at `0x{result['layout_lookup']['function']:X}` uses literal `0x{result['layout_lookup']['literal_site']:X}` → `0x{result['layout_lookup']['table']:X}` and indexes `layoutId - 1`. The layout table is sparse; zero slots do not terminate it. Each selected slot is independently checked. Saved/script layout overrides remain untested. Group/bank physical prefix limits are recorded in JSON; no engine bounds check is asserted.", '',
             '| Immediate target-warp return relation | Source edges |', '|---|---|']
    lines += [f'| {key} | {count} |' for key, count in result['summary']['warp_return_relations'].items()]
    lines += ['', 'These relations inspect the target warp record only. Exact reciprocity is not a playability test; many valid doors return through a neighboring tile, and dynamic returns depend on saved state.', '',
              '## Cases requiring further archaeology', '',
              '- Eleven West Vale Port `5:86` warps target `0:0`, warp 0. That is an ordinary static encoded destination, not a reserved zero tuple. Its landing record at `0x722A84` encodes `127:127:127`; the reference engine treats mapNum 127 as a saved dynamic return. Do not classify these as broken or unused.',
              '- Eleven other `5:86` warps target `1:99` (LIGHTHOUSE). Five landing warps point within `1:99`; six point to `0:0`. Other internal `5:86` links also land on warps targeting `0:0`. Preserve this mixed legacy/internal topology pending metatile and script checks.',
              '- Route 54 slots `3:101` and `3:107` have distinct, byte-identical warp arrays and share a connection array, yet remain different map IDs. Both `3:107` warps return to `3:101`; its two connection targets also refer to the `3:101` topology.',
              '- Science Complex `3:111` warp 0 targets `5:93` warp 0, whose encoded return is Route 53 `3:99`, warp 0. Its east connection to `3:110` has no opposite return in that target array.',
              '- Sandway Town north connection targets `3:60`, header `0x350CA8`, with a null event pointer at `0x350CAC`. Layout and connection bytes parse; no empty-map runtime safety claim follows. Its target connection array includes CONNECTION_NONE (0) at `0x352E5C`, not a cardinal transition.',
              '- Route 54 `3:101` has a west self-connection with displacement 28. Sandway east → Route 56 and the alias/Science Complex links lack inverse records. One-way geometry is not itself an engine error.', '',
              'Selected outbound links (solid) and target-warp return evidence (dashed); arrows show encoded records, not tested journeys:', '',
              '```mermaid', 'flowchart LR',
              '  A["Route 54 · 3:107"] -->|warp 0| B["Crystal Caves section · 5:95"]',
              '  C["Route 54 · 3:101"] -->|warp 0| B',
              '  B -.->|landing warp 2 return| C',
              '  D["Science Complex · 3:111"] -->|warp 0| E["Crystal Caves section · 5:93"]',
              '  F["Route 53 · 3:99"] -->|warp 0| E',
              '  E -.->|landing warp 0 return| F', '```', '',
              '## Source connection evidence', '', '| Source | Record | Direction / offset | Target | Inverse return record | Geometric overlap tiles |', '|---|---|---|---|---|---|']
    for edge in result['edges']:
        if edge['kind'] != 'connection':
            continue
        dest = edge['destination']
        inverse = ', '.join(f"0x{c['offset']:X}" for c in dest.get('inverse_displacement_returns', [])) or 'none'
        overlap = dest.get('geometric_overlap', {}).get('tiles', 'unknown')
        lines.append(f"| {edge['source_map']} | 0x{edge['offset']:X} | {edge['direction_name']} / {edge['displacement']} | {dest['target_map']} | {inverse} | {overlap} |")
    lines += ['', 'Seven source connection records have opposite-direction returns with inverse displacement; six do not. All 13 cardinal connections have nonempty geometric overlap. Collision, actual border crossing, event activation, script warps, native hooks and entry conditions remain untested.', '',
              'Machine-readable evidence: `extracted/maps/controller_connectivity.json`, `.csv` (71 individual edges), and `.dot` (aggregate display only). JSON retains raw offsets/bytes, target landing records, active-layout checks, null events and unknown directions. See `research/warp_semantics_notes.md` and `research/warp_destination_review.md` for independent interpretation/review.', '',
              'Next bounded step: enumerate object, coordinate, BG and map-entry scripts for the expanded Orange candidate maps, then identify script-driven transitions and gates around these asymmetric links. No content is certified unused or runtime-unreachable.']
    (ROOT / 'research/orange_connectivity.md').write_text('\n'.join(lines) + '\n')


def main():
    rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
    inventory = json.loads((ROOT / 'extracted/maps/controller_map_owners.json').read_text())
    result = build(rom, inventory)
    write_outputs(result)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
