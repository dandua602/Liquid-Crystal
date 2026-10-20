"""Independent native trainer-table lookup, bounded records and battle owners.

Candidate rows are not certified engine counts or unused trainer IDs. Semantic
names/parties are the retained FireRed format, supported by native consumers.
"""
import hashlib
import json
import struct
from pathlib import Path
from gba_text_codec import parse
from map_extract import FormatError,pointer,u32
from mister_r_audit import candidate_owners
from dialogue_cluster_audit import trace_graph
from orange_progression_audit import decoder
ROOT=Path(__file__).resolve().parents[1]
CONSUMERS=[(bytes.fromhex('00 04 00 0c 04 4a 81 00 09 18 c9 00 89 18 89 78 7f 20 08 40 70 47'),24,'trainer encounter-music field; ID times 40'),
           (bytes.fromhex('30 b5 00 04 00 0c 09 06 0c 0e 0a 4d 81 00 09 18 c9 00 4a 19 10 1c 20 30 00 78 a0 42 00 d2 04 1c 00 23 10 78 01 28 1f d0 01 28 05 dc 00 28 08 d0 52 e0'),52,'party-level sum; flags at 0 and count at 32')]


def discover(rom):
    rows=[]
    for signature,literal_delta,role in CONSUMERS:
        at=rom.find(signature)
        if at<0 or rom.find(signature,at+1)>=0:raise FormatError('Trainer native consumer missing/ambiguous')
        table=pointer(rom,at+literal_delta)
        rows.append({'function':at,'literal_site':at+literal_delta,'table':table,'role':role,'raw_hex':rom[at:at+literal_delta+4].hex()})
    if len({r['table']for r in rows})!=1:raise FormatError('Trainer consumers disagree')
    return rows[0]['table'],rows


def party(rom,start,count,flags):
    if flags not in (0,1,2,3)or not 1<=count<=6:raise FormatError('Invalid trainer party flags/count')
    stride=16 if flags&1 else 8
    if start<0 or start+count*stride>len(rom):raise FormatError('Trainer party outside ROM')
    rows=[]
    for i in range(count):
        at=start+stride*i;iv,=struct.unpack_from('<H',rom,at);level=rom[at+2];species=struct.unpack_from('<H',rom,at+4)[0]
        anomalies=[]
        if iv>255:anomalies.append('iv outside reference range')
        if not 1<=level<=100:anomalies.append('level outside reference range')
        if not 1<=species<=411:anomalies.append('species outside reference range')
        row={'offset':at,'iv':iv,'level':level,'species_id':species,'raw_hex':rom[at:at+stride].hex(),'field_anomalies':anomalies}
        if flags&2:row['held_item']=struct.unpack_from('<H',rom,at+6)[0]
        if flags&1:
            moves=struct.unpack_from('<4H',rom,at+(8 if flags&2 else 6))
            if max(moves)>354:anomalies.append('move outside reference range')
            row['move_ids']=list(moves)
        rows.append(row)
    return rows


def record(rom,table,index):
    at=table+index*40
    if at<0 or at+40>len(rom):raise FormatError('Trainer record outside ROM')
    name=parse(rom,at+4,limit=12,strict_english=True)
    if not name or not name['terminated']or name['issues']or not name['plain'].strip():raise FormatError('No complete nonempty trainer name')
    flags=rom[at];count=rom[at+32];target=pointer(rom,at+36)
    return {'id':index,'offset':at,'name':name['plain'],'party_flags':flags,'trainer_class':rom[at+1],
            'sprite':rom[at+3],'double_battle':bool(rom[at+24]),'ai_flags':u32(rom,at+28),
            'battle_items':list(struct.unpack_from('<4H',rom,at+16)),'party_count':count,'party_target':target,
            'party':party(rom,target,count,flags),'raw_hex':rom[at:at+40].hex()}


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();ref=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    table,native=discover(rom);reference,ref_native=discover(ref);records=[];failures=[];names=[]
    for index in range(1024):
        name=parse(rom,table+index*40+4,limit=12,strict_english=True)
        if name and name['terminated'] and not name['issues']:names.append({'id':index,'name':name['plain'],'offset':table+index*40+4})
        try:records.append(record(rom,table,index))
        except FormatError as error:failures.append({'id':index,'offset':table+index*40,'reason':str(error)})
    scan=json.loads((ROOT/'extracted/maps/map_selection_audit.json').read_text());owners,_,_=candidate_owners(rom,scan['map_record_scan'])
    battles={}
    for root,associations in owners.items():
        graph=trace_graph(rom,root,decoder=decoder,max_instructions=1024,max_states=4096,max_depth=12)
        for pc,n in graph['nodes'].items():
            if n['opcode']!=0x5C:continue
            row=battles.setdefault(pc,{'command':pc,'mode':n['values'][0],'trainer_id':n['values'][1],'roots':[],'candidate_owners':[]})
            row['roots'].append(root);row['candidate_owners']+=associations
    relevant=[row for row in records if any(t in row['name'].lower()for t in ('mister','rudy','danny','zane'))]
    result={'source_sha256':hashlib.sha256(rom).hexdigest(),'table':table,'native_consumers':native,'reference_table':reference,'reference_native_consumers':ref_native,
            'native_party_strides':{'offset':0x7FE96,'end_exclusive':0x7FF2C,'raw_hex':rom[0x7FE96:0x7FF2C].hex(),'matches_reference':rom[0x7FE96:0x7FF2C]==ref[0x7FE96:0x7FF2C],'stride_by_flags':[8,16,8,16]},
            'scope':'1024 physical candidate trainer rows; no engine-enforced count inferred. Script owners from the 4037-root candidate map scan, bounded to 1024 instructions/4096 states/depth12. Shared/conditional paths are not actual encounter proof.',
            'records':records,'bounded_name_candidates':names,'failed_candidate_rows':failures,'battles':list(sorted(battles.values(),key=lambda r:r['command'])),'named_story_records':relevant,
            'limits':'No supported name or room-owned battle links Mister R or Rudy to a future trainer team in this scope. Unnamed records, computed IDs, unindexed data and native paths remain possible; no global absence or free trainer-ID certificate.'}
    out=ROOT/'extracted/trainers';out.mkdir(parents=True,exist_ok=True);(out/'trainer_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Trainer assets and missing battle evidence','',result['scope'],'',result['limits'],'',f'Independent native consumers agree on trainer table `0x{table:X}` (reference ROM: `0x{reference:X}`), stride 40. Their literal sites and byte signatures are retained in the JSON.', '',f'{len(records)} candidate rows have complete names, bounded party arrays; field anomalies remain recorded; {len(failures)} failed candidates remain visible. This is not a trainer count or a free-ID list.','', '| ID | Name | Party count | Levels | Record |','|---:|---|---:|---|---|']
    for row in relevant:lines.append(f"| {row['id']} | {row['name']} | {row['party_count']} | "+', '.join(str(m['level'])for m in row['party'])+f" | 0x{row['offset']:X} |")
    lines += ['', 'The Mandarin encounter at script 0x9041B3 uses trainer 899, named Elite, rather than a recovered Mister R team. The police rescue uses trainer 912, also Elite. The laboratory uses trainer 837, named 4 Mister G. These IDs must not be silently reused as the promised warehouse battle.', '', 'Native party loops at 0x7FEA4/0x7FECA/0x7FEF0/0x7FF16 use row strides 8/16/8/16 for flags 0/1/2/3. The no-item forms include ABI trailing padding; treating their member lengths as strides 6/14 misaligns later Pokémon.', '', 'No supported trainer-battle command exists in the room 6:31 introduction path. There is no validated Mister R or Rudy named record in these candidate rows. The promised future team remains unrecovered; inventing one would be NEWLY_AUTHORED and requires a separate reviewed design.']
    (ROOT/'research/trainer_asset_findings.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'table':hex(table),'validated_candidate_rows':len(records),'failed_rows':len(failures),'battle_command_sites':len(battles),'story_records':[(r['id'],r['name'])for r in relevant]},indent=2))


if __name__=='__main__':main()
