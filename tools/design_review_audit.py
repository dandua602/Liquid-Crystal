"""Validate a review document against source facts; emits no ROM or scripts."""
import hashlib
import json
import re
from collections import deque
from pathlib import Path
from gba_text_codec import encode
from p001_preflight import DIGEST,START,END

ROOT=Path(__file__).resolve().parents[1]


def reachable(cells,start,blocked):
    if start in blocked or start not in cells:return set()
    seen={start};queue=deque([start])
    while queue:
        x,y=queue.popleft()
        for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if p in cells and p not in blocked and p not in seen:seen.add(p);queue.append(p)
    return seen


def audit(design,rom,geometry,moves_source):
    if hashlib.sha256(rom).hexdigest()!=DIGEST or design['input_rom_sha256']!=DIGEST:raise ValueError('Source mismatch')
    messages={}
    for key,value in design['messages'].items():
        lines=value.split('\n')
        if len(lines)>2 or any(len(s)>32 for s in lines):raise ValueError('Dialogue exceeds conservative review layout')
        messages[key]=len(b'\xfe'.join(encode(s.replace("'",'’'))for s in lines))+1
    text_bytes=sum(messages.values())
    if text_bytes>design['budget']['text_bytes']:raise ValueError('Text budget overflow')
    constants={name:int(value)for name,value in re.findall(r'#define MOVE_(\w+)\s+(\d+)\b',moves_source)}
    party=design['battle']['party']
    if len(party)!=6 or len(party)*16>design['budget']['party_bytes']:raise ValueError('Party budget/count invalid')
    for mon in party:
        if not 1<=mon['species_id']<=251 or not 1<=mon['level']<=100:raise ValueError('Proposed party outside scoped Gen I/II IDs')
        if len(mon['move_ids'])!=4 or len(mon['move_names'])!=4 or any(constants[n]!=v for n,v in zip(mon['move_names'],mon['move_ids'])):raise ValueError('Move identity mismatch')
    objects=[e for e in geometry['events']if e['kind']=='object']
    if design['rock']['local_id']in {e['local_id']for e in objects}:raise ValueError('New object local-ID collision')
    cells={(c['x'],c['y'])for c in geometry['cells']if c['in_floor_component']}
    rock=tuple(design['rock']['position']);intro=geometry.get('intro',{})
    if rock not in cells:raise ValueError('Rock not on tested floor component')
    routes=[]
    for pos in (tuple(design['npc']['scene_position']),tuple(design['npc']['collision_fallback_position'])):
        if pos not in cells or pos==rock:raise ValueError('NPC placement conflicts with puzzle/floor')
        seen=reachable(cells,(12,14),{rock,pos})
        if (20,7)not in seen or (14,9)not in seen:raise ValueError('Proposed actors block exit or clue approach')
        routes.append({'npc':list(pos),'rock':list(rock),'reachable_cells':len(seen),'stair_and_sign_accessible':True})
    for value in (design['state']['solved_retry'],design['state']['completed']):
        if not 3<value<0x4000:raise ValueError('Tagged state is not a safe literal map-table operand')
    if design['hooks']['warp_init_condition_operands']!=[1,1]:raise ValueError('Initializer must not use zero table terminator')
    table_bytes=20+24*(len(objects)+1)+12*5+(5*len(design['hooks']['map_tags'])+1)+10
    if table_bytes!=design['budget']['table_storage_bytes']or table_bytes>design['budget']['event_table_bytes']:raise ValueError('Event-table budget overflow')
    budget=design['budget']
    if sum(budget[k]for k in ['script_bytes','text_bytes','event_table_bytes','party_bytes','reserve_bytes'])!=END-START:raise ValueError('Envelope budget mismatch')
    return {'text_bytes':text_bytes,'text_capacity':budget['text_bytes'],'text_sizes':messages,'party_bytes':96,
            'event_table_bytes':table_bytes,'geometry_routes':routes,'new_object_local_id_available':True,
            'move_ids_match_pinned_reference':True,'tagged_states_below_var_threshold':True}


def main():
    design=json.loads((ROOT/'research/design/p001.json').read_text());rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    diagnosis=json.loads((ROOT/'extracted/maps/mister_r_diagnosis.json').read_text())
    result=audit(design,rom,diagnosis['geometry'],(ROOT/'research/references/include__constants__moves.h').read_text())
    intro_cells={tuple(s['position'])for m in diagnosis['intro']['movements']for s in m['steps']}
    if tuple(design['rock']['position'])in intro_cells:raise ValueError('Proposed rock intersects original intro movement')
    result.update(source_sha256=DIGEST,design_sha256=hashlib.sha256((ROOT/'research/design/p001.json').read_bytes()).hexdigest(),
                  original_intro_path_preserved=True,status='STATIC_REVIEW_CHECKS_PASS; no implementation',
                  limits='Native map-hook behavior, battle balance and complete patched acceptance remain future tests, not established by this document validator.')
    (ROOT/'extracted/maps/design_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
