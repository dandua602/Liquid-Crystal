"""Targeted native flag5B2 aftermath evidence; no ROM or personal-save changes."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from p002_runtime import OfficeJourney,ROOT,ROM,SOURCE_SAVE,FRONTEND
from progression_runtime import flagwrite
from mister_r_audit import candidate_owners
from dialogue_cluster_audit import trace_graph
from orange_progression_audit import decoder
from script_extract import event_records
from map_extract import header
from warp_graph import MapCatalog
from gba_text_codec import parse
FLAG=0x5B2


def evidence(rom):
    snapshot=json.loads((ROOT/'extracted/maps/map_selection_audit.json').read_text())
    if hashlib.sha256(rom).hexdigest()!=snapshot['source_sha256']:raise ValueError('Wrong source snapshot')
    owners,_,_=candidate_owners(rom,snapshot['map_record_scan']);sites={}
    for op in (0x29,0x2A,0x2B):
        pattern=bytes([op,FLAG&255,FLAG>>8]);hits=[];at=0
        while(at:=rom.find(pattern,at))>=0:hits.append(at);at+=1
        sites[hex(op)]=hits
    roots=set(sites['0x2b'])|{0x9F1564};witnesses={};messages={}
    for root in roots:
        graph=trace_graph(rom,root,decoder=decoder,max_instructions=512,max_states=2048,max_depth=12)
        flag_nodes=[pc for pc,node in graph['nodes'].items()if node['opcode']==0x2B and node['values']==[FLAG]]
        if not flag_nodes:continue
        for pc in flag_nodes:
            row=witnesses.setdefault(pc,{'pc':pc,'owner_associations':[],'roots':[]})
            row['owner_associations']+=owners.get(root,[]);row['roots'].append(root)
        for node in graph['nodes'].values():
            for text in node['texts']:
                p=parse(rom,text['target'],limit=2048)
                if p and p['terminated']:messages[text['target']]=p['plain']
    visibility=[]
    for slot in snapshot['map_record_scan']['slots']:
        if slot['full_header_parser']!='passed':continue
        m=header(rom,slot['header']);m['id']=f"{slot['group']}:{slot['map']}"
        for e in event_records(rom,m):
            if e.get('visibility_flag')==FLAG:visibility.append(e)
    center=MapCatalog(rom).resolve(5,121)
    hostile=next(e for e in event_records(rom,center)if e.get('local_id')==4 and e['kind']=='object')
    return {'source_sha256':hashlib.sha256(rom).hexdigest(),'flag':FLAG,'raw_literal_sites':sites,
            'read_witnesses':list(witnesses.values()),'visibility_owners':visibility,'post_branch_empty_text':{'address':0x9314DA,'text':parse(rom,0x9314DA)['plain']},
            'center_hostile_object':hostile,'messages':[{'offset':at,'text':text}for at,text in sorted(messages.items())],
            'limits':'Literal shapes plus bounded existing map associations/graphs. No direct literal set/clear does not exclude computed/native writers. Candidate duplicate map owners retained; no new writer is authorized by this evidence.'}


def main():
    original=ROOT/'roms/POKEMON Liquid Crystal.gba';data=evidence(original.read_bytes())
    out=ROOT/'extracted/runtime/mandarin_aftermath';out.mkdir(parents=True,exist_ok=True)
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (original,SOURCE_SAVE,ROM)}
    data.update(complete=False,rom_sha256=hashlib.sha256(ROM.read_bytes()).hexdigest(),fixture='Explicit flag5B2 false/true on disposable copies and direct existing dialogue-root invocation; not normal story completion.')
    p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-aftermath-')as directory:
            temp=Path(directory);shutil.copyfile(ROM,temp/'copy.gba');(temp/'copy.sav').write_bytes(SOURCE_SAVE.read_bytes()[:0x20000]);p=OfficeJourney(FRONTEND,temp,out)
            try:
                p.boot()
                for value in (False,True):
                    p.restore();p.enter(3,109,57,21,prefix=flagwrite(FLAG,value));p.finish_event('city_fixture')
                    p.run_root(0x930EB3);target=0x930ED2 if value else 0x930F2A
                    p.until_message(target,'city_after'if value else'city_before');p.finish_event('city_dialogue')
                    p.expect(f'original_city_branch_{value}',p.u32(0x03000F14),target+0x08000000)
                    p.enter(5,121,7,6);p.finish_event('center_fixture')
                    p.expect(f'original_scientist_visibility_{value}',p.has_object(5),not value)
                    p.expect(f'hostile_actor_still_present_{value}',p.has_object(4),True)
                    p.capture('center_after'if value else'center_before')
                    p.run_root(0x9314BB);target=0x9314DA if value else 0x9314DD
                    p.until_message(target,'hostile_after_blank'if value else'hostile_before');p.finish_event('hostile_dialogue')
                    p.expect(f'original_hostile_branch_{value}',p.u32(0x03000F14),target+0x08000000)
                data['complete']=True
            except Exception as error:data['error']=f'{type(error).__name__}: {error}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript)
        data['source_unchanged']=all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h for name,h in hashes.items())
        (out/'aftermath.json').write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:data.get(k)for k in ('complete','error','source_unchanged','raw_literal_sites','limits')},indent=2))


if __name__=='__main__':main()
