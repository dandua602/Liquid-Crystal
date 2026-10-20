"""Bounded Office Block continuation evidence; no ROM changes or authored patch."""
import hashlib
import json
import shutil
import struct
import tempfile
from pathlib import Path
from p001_runtime import PatchJourney,ROOT,ROM,SOURCE_SAVE,FRONTEND
from warp_graph import MapCatalog
from script_extract import event_records
from dialogue_cluster_audit import trace_graph
from orange_progression_audit import decoder
from progression_runtime import flagwrite


def audit(rom):
    c=MapCatalog(rom);city=c.resolve(3,109);room=c.resolve(5,123);warehouse=c.resolve(6,31)
    door=next(e for e in event_records(rom,city)if e['kind']=='background'and(e['x'],e['y'])==(54,16))
    sign=next(e for e in event_records(rom,city)if e['kind']=='background'and(e['x'],e['y'])==(56,17))
    bank=c.banks[6];bank['end_exclusive']=bank['start']+len(bank['targets'])*4
    return {'source_sha256':hashlib.sha256(rom).hexdigest(),'evidence_class':'CONFIRMED_IN_ROM byte/layout links; source dialogue does not specify exact passage geometry',
            'office_door':door,'office_sign':sign,'office_warp':city['warps'][8],
            'doorway_objects':[e for e in event_records(rom,city)if e['kind']=='object'and(e['x'],e['y'])in [(54,16),(54,17)]],
            'group6':{'pointer_site':c.groups['start']+6*4,'bank':bank['start'],'physical_prefix_entries':len(bank['targets']),'next_word_hex':rom[bank['end_exclusive']:bank['end_exclusive']+4].hex(),
                      'retained_legacy_header_failures':[{'map':n,'reason':c.resolve(6,n).get('reason')}for n in range(32)if c.resolve(6,n)['status']!='structure_validated'],
                      'preservation_contract':'Copy every original bank word, including unresolved legacy pointers; do not normalize or remove them.'},
            'clone_room':{'source_map':'5:123','header':room['header'],'layout':room['layout'],'size':[room['width'],room['height']],'section_label':room['section_label']['text'],'events':event_records(rom,room),'warps':room['warps']},
            'source_warehouse_warps':warehouse['warps'],
            'director_hint':{'root':0x9046EE,'text':0x904966,'source':'extracted/scripts/orange_progression_audit.json'},
            'route59_sign':{'text':0xA9C482,'source':'extracted/scripts/orange_progression_audit.json'},
            'limits':'Map32 is a proposed new bank entry beyond the physical pointer prefix, not a certified globally unused ID. Unknown computed accesses remain outside the bounded ownership model. No route60 map or intended Office interior is recovered.'}


def main():
    out=ROOT/'extracted/runtime/office_access';out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'roms/POKEMON Liquid Crystal.gba';before={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in (source,SOURCE_SAVE)}
    data=audit(source.read_bytes());data.update(complete=False,rom_sha256=hashlib.sha256(ROM.read_bytes()).hexdigest());p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-office-audit-')as directory:
            temp=Path(directory);shutil.copyfile(ROM,temp/'copy.gba');(temp/'copy.sav').write_bytes(SOURCE_SAVE.read_bytes()[:0x20000])
            p=PatchJourney(FRONTEND,temp,out)
            try:
                p.boot()
                for state,bit,label in [(1,False,'pending'),(0x3303,True,'completed')]:
                    p.room(state,bit)
                    p.checks.append({'label':'explicit_city_object_visibility_fixture','flags_set':[0x5B6,0x270],'meaning':'Disposable late-city setup hides original doorway objects; these flags are not earned or changed by P001.'})
                    p.enter(3,109,54,17,prefix=flagwrite(0x5B6,True)+flagwrite(0x270,True));p.finish_event(label+'_office_entry')
                    record=p.map_record(label+'_city_header');p.expect(label+'_city_header_unchanged',record['live_matches_default_header'],True)
                    p.fixture(b'\x5b\xff\x00\x02');p.button(1);p.until_message(0x904535,label+'_locked_door');p.finish_event(label+'_locked_text')
                    p.button(64,16,120);p.capture(label+'_up_attempt')
                    p.checks.append({'label':label+'_physical_up_result','location':p.location(),'field_callback':p.u32(0x030030F4)})
                # Preview the proposed cloned geometry using the existing map,
                # not a new header or modification. Original NPC still present.
                p.restore();p.enter(5,123,4,7);p.finish_event('clone_asset_preview');p.capture('clone_asset_preview')
                p.expect('clone_floor_walk_is_possible',p.location()['x'],4)
                p.walk((4,6));p.expect('clone_walk_one_tile',(p.location()['x'],p.location()['y']),(4,6))
                data['complete']=True
            except Exception as error:
                data['error']=f'{type(error).__name__}: {error}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript)
        data['source_unchanged']=all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in before.items())
        (out/'office_access.json').write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items()if k not in ('checks','transcript','clone_room','source_warehouse_warps')},indent=2))


if __name__=='__main__':main()
