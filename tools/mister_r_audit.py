"""Read-only Mister R room diagnosis, with bounded wider script evidence."""
import bisect
import hashlib
import json
import struct
from collections import Counter, deque
from pathlib import Path

from dialogue_cluster_audit import instruction, trace_graph
from gba_text_codec import encode, fold_case, parse
from map_extract import FormatError, header, pointer, u32
from map_selection_audit import lz77_extent, thumb_bl
from pointer_scan import BASE, classify_operand, index_pointers
from route59_audit import COMMAND_SPECS
from script_extract import event_records, map_script_table
from warp_graph import MapCatalog

ROOT = Path(__file__).resolve().parents[1]
SPECS = {**COMMAND_SPECS, 0xAA: ('createvobject', (1, 1, 2, 2, 1, 1)),
         0xAB: ('turnvobject', (1, 1)), 0xAC: ('opendoor', (2, 2)),
         0xAD: ('closedoor', (2, 2)), 0xAE: ('waitdooranim', ()),
         0xAF: ('setdooropen', (2, 2)), 0xB0: ('setdoorclosed', (2, 2))}
BEHAVIORS = {0x65: 'SOUTH_ARROW_WARP', 0x6E: 'DOWN_RIGHT_STAIR_WARP',
             0x84: 'SIGNPOST', 0x95: 'POWER_PLANT_MACHINE', 0x96: 'TELEPHONE', 0x9E: 'BLINKING_LIGHTS'}


def decoder(rom, pc):
    return instruction(rom, pc, specs=SPECS)


def component(cells, width, height, start):
    """Collision-zero, same-elevation four-neighbor model; no engine simulation."""
    grid = {(cell['x'], cell['y']): cell for cell in cells}
    if start not in grid or grid[start]['collision']:
        return set()
    elevation = grid[start]['elevation']
    seen, queue = {start}, deque([start])
    while queue:
        x, y = queue.popleft()
        for pos in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if pos in seen or not 0 <= pos[0] < width or not 0 <= pos[1] < height:
                continue
            if grid[pos]['collision'] == 0 and grid[pos]['elevation'] == elevation:
                seen.add(pos); queue.append(pos)
    return seen


def room_geometry(rom):
    m = MapCatalog(rom).resolve(6, 31)
    if m['status'] != 'structure_validated':
        raise FormatError('Mister R room no longer validates')
    tilesets = []
    for field in (16, 20):
        at = pointer(rom, m['layout'] + field)
        tilesets.append({'offset': at, 'raw_hex': rom[at:at+24].hex(' '),
                         'attributes': pointer(rom, at+20), 'metatiles': pointer(rom, at+12),
                         'animation_callback_word': u32(rom, at+16)})
    cells = []
    for y in range(m['height']):
        for x in range(m['width']):
            at = m['map_blocks'] + 2 * (y*m['width'] + x)
            word = struct.unpack_from('<H', rom, at)[0]
            tile = word & 0x3FF
            selected = int(tile >= 0x280)
            attr_at = tilesets[selected]['attributes'] + 4 * (tile - 0x280 * selected)
            attr = u32(rom, attr_at)
            cells.append({'x': x, 'y': y, 'offset': at, 'word': word, 'metatile': tile,
                          'collision': (word >> 10) & 3, 'elevation': word >> 12,
                          'attribute_offset': attr_at, 'attribute_word': attr, 'behavior': attr & 0x1FF})
    floor = component(cells, m['width'], m['height'], (12, 14))
    for cell in cells:
        cell['in_floor_component'] = (cell['x'], cell['y']) in floor
        cell['adjacent_to_floor'] = any((cell['x']+dx, cell['y']+dy) in floor for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))
    grid = {(cell['x'], cell['y']): cell for cell in cells}
    ev = event_records(rom, m)
    for event in ev + m['warps']:
        pos = event['x'], event['y']
        event['in_floor_component'] = pos in floor
        event['adjacent_to_floor'] = grid.get(pos, {}).get('adjacent_to_floor', False)
    return {'map': m, 'tilesets': tilesets, 'cells': cells, 'events': ev,
            'map_script_table': map_script_table(rom, m['map_scripts']),
            'model': 'Collision==0 and elevation equal to entry (3), four-neighbor BFS from (12,14). Does not simulate objects, steps, warp activation, layout overrides or native effects.',
            'summary': {'cells': len(cells), 'collision_counts': {str(k):v for k,v in Counter(c['collision'] for c in cells).items()},
                        'floor_component': len(floor), 'nonzero_behavior_cells': sum(c['behavior'] != 0 for c in cells)}}


def movements(rom, geometry):
    trace = trace_graph(rom, 0xAE8D7A, decoder=decoder)
    vectors = {0x10: (0,1), 0x11: (0,-1), 0x12: (-1,0), 0x13: (1,0)}
    labels = {0: 'face_down', 0x10: 'walk_down', 0x11: 'walk_up', 0x12: 'walk_left', 0x13: 'walk_right', 0x60: 'set_invisible', 0xFE: 'step_end'}
    grid = {(c['x'], c['y']): c for c in geometry['cells']}
    pos, result = (12,11), []
    for pc, node in sorted(trace['nodes'].items()):
        if node['opcode'] != 0x4F:
            continue
        start = node['values'][1] - BASE
        row = {'command': pc, 'local_id': node['values'][0], 'movement': start, 'start': list(pos), 'steps': [], 'terminated': False}
        for at in range(start, min(start+128, len(rom))):
            value = rom[at]
            if value not in labels:
                row['stop_reason'] = f'unsupported movement {value:02X}'; break
            if value in vectors:
                dx, dy = vectors[value]; pos = pos[0]+dx, pos[1]+dy
            row['steps'].append({'offset': at, 'opcode': value, 'name': labels[value], 'position': list(pos),
                                 'on_default_floor': grid.get(pos, {}).get('in_floor_component', False)})
            if value == 0xFE:
                row['terminated'] = True; break
        row['end'] = list(pos); row['raw_hex'] = rom[start:start+len(row['steps'])].hex(' ')
        result.append(row)
    return {'root': 0xAE8D7A, 'instructions': list(trace['nodes'].values()), 'frontiers': trace['frontiers'],
            'overlaps': trace['overlaps'], 'movements': result,
            'limits': 'Step endpoints reconstructed from retained movement constants; timing, dynamic collision and NPC visibility are runtime matters.'}


def native_flavor(rom, reference):
    dispatch = []
    for behavior, predicate, call, literal, script in [(0x95,0x5A49C,0x6D39A,0x6D3AC,0x1A7684),
                                                    (0x96,0x5A4B0,0x6D3B2,0x6D3C4,0x1A768D),
                                                    (0x9E,0x5A530,0x6D45A,0x6D46C,0x1A76CC)]:
        expected = bytes.fromhex('00 b5 00 06 00 0e') + bytes([behavior, 0x28])
        if rom[predicate:predicate+8] != expected or thumb_bl(rom, call) != predicate or u32(rom, literal) != script + BASE:
            raise FormatError('Native metatile dispatch evidence changed')
        graph = trace_graph(rom, script, decoder=decoder)
        text = [parse(rom, t['target'], strict_english=True) for n in graph['nodes'].values() for t in n['texts']]
        dispatch.append({'behavior': behavior, 'name': BEHAVIORS[behavior], 'predicate': predicate,
                         'predicate_raw_hex': rom[predicate:predicate+20].hex(' '),
                         'predicate_matches_reference': rom[predicate:predicate+20] == reference[predicate:predicate+20],
                         'callsite': call, 'literal_site': literal, 'script': script,
                         'dispatch_raw_hex': rom[call-2:call+22].hex(' '),
                         'dispatch_matches_reference': rom[call-2:call+22] == reference[call-2:call+22],
                         'instructions': list(graph['nodes'].values()), 'frontiers': graph['frontiers'],
                         'text': text, 'script_matches_reference': rom[script:script+9] == reference[script:script+9]})
    standard = []
    for number in (2,3,6):
        at = pointer(rom, 0x160450 + 4*number)
        graph = trace_graph(rom, at, decoder=decoder)
        standard.append({'index': number, 'root': at, 'instructions': list(graph['nodes'].values()), 'frontiers': graph['frontiers']})
    intervals = []
    for start, end, purpose in [(0x58F1C,0x58F48,'attribute bitfield extraction'),
                                (0x59080,0x590D8,'primary/secondary attribute table selection'),
                                (0x70250,0x70274,'secondary tileset animation initialization'),
                                (0x6A180,0x6A1B0,'callstd handler'),
                                (0x697AC,0x697F2,'script context initialization/setup'),
                                (0x69AE4,0x69B28,'global script setup and RAM/table literals'),
                                (0x1229FC,0x122B20,'party field-move selection function')]:
        intervals.append({'start': start, 'end': end, 'purpose': purpose,
                          'raw_hex': rom[start:end].hex(' '), 'sha256': hashlib.sha256(rom[start:end]).hexdigest(),
                          'matches_reference': rom[start:end] == reference[start:end]})
    field_moves = list(struct.unpack_from('<13H',rom,0x45A76E))
    if field_moves != [148,15,19,70,57,249,127,100,91,208,135,230,12] or u32(rom,0x122A7C) != 0x0845A76E:
        raise FormatError('Field-move menu table evidence changed')
    return {'dispatch': dispatch, 'standard_scripts': standard, 'native_intervals': intervals,
            'field_move_menu': {'table':0x45A76E,'literal_site':0x122A7C,'move_ids_then_end_sentinel':field_moves,
                                'raw_hex':rom[0x45A76E:0x45A788].hex(' '), 'iron_tail_id':231,
                                'iron_tail_in_standard_field_move_menu':False,
                                'matches_reference':rom[0x45A76E:0x45A788]==reference[0x45A76E:0x45A788]},
            'limits': 'Local predicates, dispatch, bytecode and selected native intervals corroborated. This is not a complete audit of all native callees or map effects.'}


def candidate_owners(rom, scan):
    owners, conditions, flags = {}, [], []
    for slot in scan['slots']:
        if slot['full_header_parser'] != 'passed':
            continue
        m = header(rom, slot['header']); m['id'] = f"{slot['group']}:{slot['map']}"
        for event in event_records(rom, m):
            if event.get('visibility_flag') == 0x5C5:
                flags.append(event)
            if event['script_target'] is not None:
                owners.setdefault(event['script_target'], []).append({k: event[k] for k in ('id','map_id','kind','pointer_site')})
        for entry in map_script_table(rom, m['map_scripts'])['entries']:
            if not entry['first_entry_for_tag'] or entry['tag'] not in range(1,8):
                continue
            rows = entry['conditional_table']['entries'] if 'conditional_table' in entry else [entry]
            for row in rows:
                if 0x5331 in (row.get('operand_1'), row.get('operand_2')):
                    conditions.append({'map_id': m['id'], 'tag': entry['tag'], **row})
                if row['script_target'] is not None:
                    owners.setdefault(row['script_target'], []).append({'map_id': m['id'], 'kind': 'map_script', 'tag': entry['tag'], 'pointer_site': row['pointer_site']})
    return owners, conditions, flags


def wider_search(rom, scan):
    incoming = index_pointers(rom); targets = sorted(incoming)
    owners, conditions, flags = candidate_owners(rom, scan)
    folded = fold_case(rom)
    keywords, blocks = {}, {}
    for term in ('Mister R', 'puzzle'):
        needle, hits, at = fold_case(encode(term)), [], 0
        while (at := folded.find(needle, at)) >= 0:
            hits.append(at); at += 1
        keywords[term] = hits
        for hit in hits:
            starts = targets[bisect.bisect_left(targets,max(0,hit-2500)):bisect.bisect_right(targets,hit)]
            accepted = []
            for start in starts:
                text = parse(rom,start,limit=3000,strict_english=True)
                if text and text['terminated'] and not text['issues'] and text['end'] > hit:
                    accepted.append((start,text))
            if accepted:
                start, text = accepted[0]
                row = blocks.setdefault(start,{'offset':start,'text':text['text'],'end':text['end'],'hits':[], 'incoming_pointer_sites': incoming[start], 'command_candidates':[]})
                row['hits'].append({'term':term,'offset':hit})
    commands = {}
    for start, block in blocks.items():
        for site in incoming[start]:
            shape = classify_operand(rom,site)
            pc = shape.get('command_offset')
            if pc is None:
                continue
            pc = int(pc,16); node,error = decoder(rom,pc)
            if not node or not any(t['target']==start for t in node['texts']):
                continue
            row = {'command':pc,'instruction':node,'owner_witnesses':[]}
            block['command_candidates'].append(row); commands.setdefault(pc,[]).append(row)
    state_hits, shapes = {}, {}
    for label,value,ops in [('operand_5331',0x5331,{0x16,0x17,0x18,0x19,0x1A,0x21,0x22}),
                            ('flag_5C5',0x5C5,{0x29,0x2A,0x2B})]:
        hits,at = [],0
        while (at := rom.find(struct.pack('<H',value),at)) >= 0:
            hits.append({'offset':at,'context_start':max(0,at-8),'context_hex':rom[max(0,at-8):at+12].hex(' ')});at+=1
        state_hits[label]=hits
        for hit in hits:
            for pc in (hit['offset']-1,hit['offset']-3):
                if pc < 0 or rom[pc] not in ops:
                    continue
                node,error=decoder(rom,pc)
                if node and any(site==hit['offset'] and val==value for site,val in zip(node['operand_offsets'],node['values'])):
                    shapes.setdefault(pc,{'instruction':node,'label':label,'owner_witnesses':[]})
    at=0
    while (at:=rom.find(bytes.fromhex('7c e7 00'),at))>=0:
        node,error=decoder(rom,at)
        shapes[at]={'instruction':node,'label':'iron_tail_checkpartymove','owner_witnesses':[]};at+=1
    frontier_counts, traced, observed = Counter(),0,set()
    for root, associations in sorted(owners.items()):
        graph=trace_graph(rom,root,max_instructions=256,max_states=1024,max_depth=8,decoder=decoder)
        traced+=1; observed.update(graph['nodes'])
        frontier_counts.update(f['reason'] for f in graph['frontiers'])
        for pc in set(graph['nodes']) & (set(commands)|set(shapes)):
            witness={'root':root,'associations':associations,'path':graph['witness'](pc)}
            for row in commands.get(pc,[]):row['owner_witnesses'].append(witness)
            if pc in shapes:shapes[pc]['owner_witnesses'].append(witness)
    lz_cache={}
    for pc,row in shapes.items():
        row['compressed_stream']=None
        starts=targets[bisect.bisect_left(targets,max(0,pc-0x40000)):bisect.bisect_right(targets,pc)]
        for start in reversed(starts):
            if start%4 or rom[start]!=0x10:continue
            if start not in lz_cache:lz_cache[start]=lz77_extent(rom,start)
            extent=lz_cache[start]
            if extent and row['instruction']['end']<=extent['end']:
                row['compressed_stream']={**extent,'incoming_pointer_sites':incoming[start]};break
        row['classification']=('map_owned_format_witness' if row['owner_witnesses'] else
                               'pointer_backed_LZ77_stream' if row['compressed_stream'] else 'unresolved_raw_shape')
    return {'keywords':keywords,'referenced_complete_blocks':list(blocks.values()),
            'state_raw_hits':state_hits,'state_command_shapes':[r for r in shapes.values() if r['label']!='iron_tail_checkpartymove'],
            'iron_tail_checkmove_shapes':[r for r in shapes.values() if r['label']=='iron_tail_checkpartymove'],
            'state_condition_owners':conditions,'visibility_flag_owners':flags,
            'summary':{'candidate_owner_roots_traced':traced,'unique_instruction_candidates':len(observed),
                       'frontier_reasons':dict(sorted(frontier_counts.items())),
                       'keyword_hits':{k:len(v) for k,v in keywords.items()},'referenced_complete_blocks':len(blocks),
                       'state_command_shape_classes':dict(Counter(r['classification'] for r in shapes.values()))},
            'limits':'Owners come from prior native-table physical-prefix slots whose full header parser passed, including overlapping tails. This is a candidate-owner search, not a certified world map. Each root is bounded to 256 instructions/1024 states/depth 8; all frontiers counted. Text start search uses incoming ROM pointers within 2500 bytes. Raw hits and unsupported contexts are retained; computed IDs, unindexed data and indirect/native execution can escape this search.'}


def draw_svg(geometry, path):
    scale=22; width=geometry['map']['width']; height=geometry['map']['height']
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width*scale}" height="{(height+3)*scale}" viewBox="0 0 {width*scale} {(height+3)*scale}">',
           '<rect width="100%" height="100%" fill="#101827"/>',
           '<style>text{font:11px monospace;fill:white}</style>']
    for c in geometry['cells']:
        color='#d7e4f2' if c['in_floor_component'] else '#293648'
        if c['behavior']:color='#dc9d38' if not c['collision'] else '#67552f'
        parts.append(f'<rect x="{c["x"]*scale}" y="{c["y"]*scale}" width="21" height="21" fill="{color}"><title>({c["x"]},{c["y"]}) collision {c["collision"]}; behavior 0x{c["behavior"]:02X}</title></rect>')
    for event in geometry['events']+geometry['map']['warps']:
        label=('W'+str(event['index'])) if 'kind' not in event else ('O' if event['kind']=='object' else 'B')+str(event['index'])
        parts.append(f'<text x="{event["x"]*scale+1}" y="{event["y"]*scale+15}">{label}</text>')
    parts += [f'<text x="8" y="{(height+1)*scale}">74 connected floor tiles · amber = nonzero behavior · W warp / O object / B BG event</text>',
              f'<text x="8" y="{(height+2)*scale}">Default collision model; object visibility, native effects and movement not simulated.</text>','</svg>']
    path.write_text('\n'.join(parts)+'\n')


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    reference=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    scan=json.loads((ROOT/'extracted/maps/map_selection_audit.json').read_text())
    digest=hashlib.sha256(rom).hexdigest()
    if scan['source_sha256']!=digest:raise FormatError('Stale map selection audit')
    geometry=room_geometry(rom)
    data={'source_sha256':digest,'reference_sha256':hashlib.sha256(reference).hexdigest(),
          'geometry':geometry,'intro':movements(rom,geometry),'native_flavor':native_flavor(rom,reference),
          'wider_search':wider_search(rom,scan['map_record_scan']),
          'conclusion':'Strong evidence of an unfinished local puzzle/battle in the default room: introduction removes Mister R, accessible behavior dispatch is flavor text, and no completion handler is established. This does not certify the exact beta dead end or normal gameplay reachability.'}
    sign=trace_graph(rom,0x96D9E6,decoder=decoder)
    data['damaged_sign']={'root':0x96D9E6,'instructions':list(sign['nodes'].values()),'frontiers':sign['frontiers'],
                          'messages':[parse(rom,t['target'],strict_english=True) for n in sign['nodes'].values() for t in n['texts']]}
    (ROOT/'extracted/maps/mister_r_diagnosis.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    draw_svg(geometry,ROOT/'extracted/maps/mister_r_collision.svg')
    print(json.dumps({'geometry':geometry['summary'],'search':data['wider_search']['summary']},indent=2))


if __name__=='__main__':main()
