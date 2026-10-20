"""P002 interactions and affected P001 regression on disposable files.

Forced starting anchors/state and boosted combat fixture are explicit. Office
entry/return, battle outcomes and actual Save/reload are earned in native play.
"""
import argparse
import code
import hashlib
import json
import shutil
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from p001_runtime import PatchJourney,ROOT,SOURCE_SAVE,FRONTEND,matrix,puzzle as warehouse_puzzle,loss,exits
from progression_runtime import setvar
from allocation_runtime import save_copy,trainer_flag
from warp_graph import MapCatalog
ROM=ROOT/'builds/dev/Liquid Crystal P002.gba'


class OfficeJourney(PatchJourney):
    def __init__(self,*args):
        super().__init__(*args);self.rom=ROM.read_bytes();self.catalog=MapCatalog(self.rom)
        self.office=json.loads((ROOT/'builds/dev/P002-manifest.json').read_text())
    def until_office(self,key):self.until_message(self.office['text_addresses'][key],key)
    def map_record(self,label):
        pos=self.location();m=self.catalog.resolve(pos['group'],pos['map']);raw=self.read(0x02036DFC,28)
        row={'label':label,'location':pos,'live_header_hex':raw.hex(),'expected_header':m.get('header'),'live_matches_built_header':m.get('status')=='structure_validated'and raw==self.rom[m['header']:m['header']+28]}
        self.checks.append(row);return row
    def office_prompt(self):
        self.walk((14,9));self.interact(32);self.until_office('entry')
        self.expect('cleared_rock_stays_absent_after_walking_to_sign',self.has_object(3),False)
    def enter_office(self):
        self.office_prompt();self.choose(True);self.frame(240);self.finish_event('office_entry')
        self.expect('entered_new_service_room',(self.location()['group'],self.location()['map']),(6,32))
        self.expect('service_room_native_header',self.map_record('office_header')['live_matches_built_header'],True)
        self.expect('service_room_entry_position',(self.location()['x'],self.location()['y']),(4,7))
    def leave_office(self):
        self.walk((4,8),transition=(6,31));self.frame(120);self.finish_event('office_return')
        self.expect('normal_office_exit_returns_warehouse',(self.location()['group'],self.location()['map']),(6,31))
        self.expect('return_keeps_completed_tag',self.variable(0x5331),0x3303)
        self.expect('return_keeps_defeated_bit',trainer_flag(self,929),1)
        self.expect('return_keeps_rock_hidden',self.has_object(3),False)
        self.expect('return_keeps_mister_r_hidden',self.has_object(1),False)


def access(p):
    for value,bit in [(1,False),(2,False),(3,False),(0x7777,False),(0x3302,False),(0x3303,False),(1,True)]:
        p.room(value,bit);p.walk((14,9))
        p.expect(f'rock_visibility_after_walking_{value:04x}_{bit}',p.has_object(3),p.variable(0x5331)==1)
        p.interact(32)
        if p.variable(0x5331)==0x3302:p.until('retry');p.choose(False)
        p.finish_event('denied_access')
        p.expect(f'no_office_access_{value:04x}_{bit}',(p.location()['group'],p.location()['map']),(6,31))
    p.room(0x3302);p.checks.append({'label':'explicit_inconsistent_tag_fixture','state':0x3303,'trainer_bit':False});p.fixture(setvar(0x5331,0x3303))
    p.walk((14,9));p.interact(32);p.until('retry');p.choose(False);p.finish_event('inconsistent_recovery')
    p.expect('inconsistent_tag_recovers_before_access',p.variable(0x5331),0x3302)
    p.room(0x3303,True);p.office_prompt();p.choose(False);p.finish_event('declined_entry')
    p.expect('declined_entry_stays_warehouse',(p.location()['group'],p.location()['map']),(6,31))
    p.enter_office();p.capture('office_arrival')
    p.walk((4,5));p.interact(64);p.until_office('npc');p.finish_event('attendant_dialogue');p.capture('office_attendant')
    p.expect('attendant_keeps_completion',p.variable(0x5331),0x3303)
    p.leave_office();p.capture('warehouse_return')
    p.enter_office();p.leave_office();p.expect('repeat_access_keeps_completion',p.variable(0x5331),0x3303)


def puzzle(p):
    warehouse_puzzle(p)
    for move in (231,249):
        p.room();p.moves();p.solve_decline(move);p.walk((14,10));p.walk((14,9))
        p.expect(f'solved_rock_does_not_respawn_on_movement_{move}',p.has_object(3),False)
        p.enter(6,31,14,10);p.finish_event('solved_room_reentry');p.walk((14,9))
        p.expect(f'solved_rock_does_not_respawn_after_reentry_{move}',p.has_object(3),False)


def journey(p):
    # Boot uses the retained artificial P001 solved-room save, not a forced
    # completion value. Native victory earns entry to the new map.
    p.expect('p001_save_upgrade_keeps_solved_tag',p.variable(0x5331),0x3302)
    p.expect('p001_save_upgrade_keeps_unbeaten_bit',trainer_flag(p,929),0)
    p.expect('p001_save_upgrade_rock_hidden',p.has_object(3),False)
    location=p.location();p.sign_retry(True);p.frame(300);p.capture('battle_interruption');p.restart(location)
    p.expect('interrupted_p002_attempt_keeps_saved_retry',p.variable(0x5331),0x3302)
    p.expect('interrupted_p002_attempt_not_defeated',trainer_flag(p,929),0)
    p.victory_party();p.sign_retry(True);p.finish_event('earned_warehouse_victory',1800);p.frame(120)
    p.expect('actual_p002_victory_commits_tag',p.variable(0x5331),0x3303)
    p.expect('actual_p002_battle_loaded_six_approved_opponents',sorted(p.enemy_seen),[94,169,197,212,229,248])
    p.expect('actual_p002_victory_sets_bit',trainer_flag(p,929),1)
    save_copy(p);location=p.location();p.restart(location)
    p.expect('earned_win_survives_fresh_process',p.variable(0x5331),0x3303)
    p.enter_office();p.capture('office_after_earned_victory');save_copy(p);location=p.location()
    ready=ROOT/'saves/test/P002-office-fixture.sav';shutil.copyfile(p.temp/'copy.sav',ready)
    ready.with_suffix('.json').write_text(json.dumps({'kind':'Artificial research fixture, earned native victory after P001 save upgrade','rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'location':location,'party':'Generated boosted level100 Mewtwo/Surf/Lum Berry; not personal progress or balance proof','rollback':'Exit new room to warehouse and save before using a P001-only/original ROM'},indent=2)+'\n')
    p.restart(location)
    p.expect('new_map_save_fresh_reload_location',(p.location()['group'],p.location()['map']),(6,32))
    p.expect('new_map_save_fresh_reload_header',p.map_record('reloaded_office')['live_matches_built_header'],True)
    p.expect('new_map_save_keeps_completion',p.variable(0x5331),0x3303)
    p.expect('new_map_save_keeps_defeated_bit',trainer_flag(p,929),1)
    p.capture('office_fresh_reload');p.leave_office();save_copy(p);location=p.location();p.restart(location)
    p.expect('returned_warehouse_save_reload',(p.location()['group'],p.location()['map']),(6,31))
    p.expect('returned_save_keeps_completed_tag',p.variable(0x5331),0x3303)
    p.enter_office();p.leave_office();p.capture('journey_complete')


def rollback(p):
    p.expect('rollback_starts_from_earned_office_save',(p.location()['group'],p.location()['map']),(6,32))
    p.leave_office();save_copy(p);location=p.location()
    ready=ROOT/'saves/test/P002-safe-rollback-fixture.sav';shutil.copyfile(p.temp/'copy.sav',ready)
    ready.with_suffix('.json').write_text(json.dumps({'kind':'Artificial native-earned victory fixture saved safely outside the P002-only map','location':location,'rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'party':'Boosted generated Mewtwo; not personal progress','rollback_ready':True},indent=2)+'\n')
    history,checks,steps=p.transcript,p.checks,p.steps;p.close()
    old=ROOT/'builds/dev/Liquid Crystal P001.gba';shutil.copyfile(old,p.temp/'copy.gba')
    q=PatchJourney(p.frontend,p.temp,p.output);q.transcript=history+[{'command':'<fresh process using exact P001 ROM>','response':{'rom_sha256':hashlib.sha256(old.read_bytes()).hexdigest()}}];q.checks=checks;q.steps=steps
    try:
        q.boot(location);q.expect('p001_rollback_save_loads_existing_warehouse',(q.location()['group'],q.location()['map']),(6,31))
        q.expect('p001_rollback_keeps_completion',q.variable(0x5331),0x3303)
        q.expect('p001_rollback_keeps_native_bit',trainer_flag(q,929),1)
        q.walk((14,9));q.interact(32);q.until('completed');q.finish_event('p001_rollback_completed_sign');q.capture('p001_rollback_loaded')
        return q
    except BaseException:
        p.transcript=q.transcript;p.checks=q.checks;p.steps=q.steps;q.close();raise


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=['access','journey','matrix','puzzle','loss','exits','rollback'],required=True);parser.add_argument('--debug',action='store_true');args=parser.parse_args()
    out=ROOT/'extracted/runtime/p002'/args.case;out.mkdir(parents=True,exist_ok=True)
    sources=[ROOT/'roms/POKEMON Liquid Crystal.gba',ROOT/'builds/dev/Liquid Crystal P001.gba',SOURCE_SAVE]
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sources};p=None
    data={'case':args.case,'complete':False,'rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'source_sha256':hashes,'started_at_utc':datetime.now(timezone.utc).isoformat(),'limits':__doc__}
    try:
        with tempfile.TemporaryDirectory(prefix='lc-p002-')as directory:
            temp=Path(directory);shutil.copyfile(ROM,temp/'copy.gba')
            saved=ROOT/'saves/test/P001-ready-fixture.sav'if args.case=='journey'else(ROOT/'saves/test/P002-office-fixture.sav'if args.case=='rollback'else SOURCE_SAVE)
            (temp/'copy.sav').write_bytes(saved.read_bytes()[:0x20000]);data['boot_save']=str(saved.relative_to(ROOT));data['boot_save_sha256']=hashlib.sha256(saved.read_bytes()).hexdigest()
            p=OfficeJourney(FRONTEND,temp,out)
            try:
                expected=json.loads(saved.with_suffix('.json').read_text())['location']if args.case in ('journey','rollback')else None
                p.boot(expected);updated=globals()[args.case](p)
                if updated is not None:p=updated
                data['complete']=True
            except Exception as error:
                data['error']=f'{type(error).__name__}: {error}';p.capture('failure_state')
                if args.debug:code.interact(local={'p':p,'data':data})
                raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript,steps=p.steps)
        data['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[str(f.relative_to(ROOT))]for f in sources)
        (out/(args.case+'.json')).write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items()if k not in ('checks','transcript','steps')},indent=2))


if __name__=='__main__':main()
