"""P001 acceptance on disposable ROM/save copies; explicit controlled fixtures.

Tests actual patched interactions and native battles. Forced room/state/party
fixtures are recorded; enemy HP and battle outcomes are never injected.
"""
import argparse
import code
import hashlib
import json
import shutil
import struct
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from linked_progression import Journey,ROOT,laboratory,journey
from progression_runtime import Probe,setvar,flagwrite,word,escape_controller
from allocation_runtime import save_copy,trainer_flag
from warp_graph import MapCatalog
ROM=ROOT/'builds/dev/Liquid Crystal P001.gba'
SOURCE_SAVE=ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'
FRONTEND=Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe')
FIELD_CALLBACK=0x080565B5


class PatchJourney(Journey):
    def __init__(self,*args):
        super().__init__(*args);self.rom=ROM.read_bytes();self.catalog=MapCatalog(self.rom);self.manifest=json.loads((ROOT/'builds/dev/P001-manifest.json').read_text());self.enemy_seen=set()
    def observe_battle(self,label,iteration):
        if iteration%4:return
        raw=self.read(0x02023C3C,88);species=int.from_bytes(raw[:2],'little');level=raw[0x2A];moves=list(struct.unpack_from('<4H',raw,12))
        party=json.loads((ROOT/'research/design/p001.json').read_text())['battle']['party']
        for mon in party:
            if (species,level,moves)==(mon['species_id'],mon['level'],mon['move_ids'])and species not in self.enemy_seen:
                self.enemy_seen.add(species);self.checks.append({'label':'actual_native_enemy_'+mon['name'],'species':species,'level':level,'moves':moves,'battlemon_address':0x02023C3C})
        if iteration%100==0:
            (self.output/'live.json').write_text(json.dumps({'label':label,'iteration':iteration,'script_pc':self.u32(0x03000EB8),'callback':self.u32(0x030030F4),'enemy_species':species,'enemy_hp':int.from_bytes(raw[0x28:0x2A],'little'),'seen':sorted(self.enemy_seen)},indent=2))
    def boot(self,expected=None):
        expected=expected or {'x':32,'y':29,'group':3,'map':62,'warp':4}
        for count,keys in [(300,0),(1,8),(180,0),(1,8),(180,0),(1,8),(420,0),(1,1),(300,0),(1,1),(120,0),(1,1),(240,0)]:
            self.frame(count,keys)
            if keys==0 and self.u32(0x030030F4)==FIELD_CALLBACK and self.status()==2 and self.location()==expected:break
        self.field_callback=FIELD_CALLBACK
        self.expect('boot_saved_location',self.location(),expected)
        self.expect('boot_field_callback',self.u32(0x030030F4),FIELD_CALLBACK)
        self.command(f's {self.temp/"baseline.state"}')
    def has_object(self,index):return any(o['local_id']==index and not o['invisible']for o in self.objects())
    def expect(self,label,actual,expected):
        if isinstance(actual,bytes):actual=hashlib.sha256(actual).hexdigest()
        if isinstance(expected,bytes):expected=hashlib.sha256(expected).hexdigest()
        super().expect(label,actual,expected)
    def room(self,value=1,defeated=False,x=14,y=10,restore=True):
        if restore:self.restore()
        self.checks.append({'label':'explicit_room_fixture','state':value,'trainer_defeated':defeated,'entry':[x,y],'normal_story_entry':False})
        self.fixture(bytes([0x61 if defeated else 0x62])+word(929))
        self.enter(6,31,x,y,prefix=setvar(0x5331,value)+flagwrite(0x5C5,value!=0))
        self.finish_event('room_entry');self.frame(60)
    def moves(self,move=33):
        self.checks.append({'label':'explicit_research_party_moves','all_slots':move})
        for slot in range(6):self.fixture(b''.join(b'\x7b'+bytes([slot,i])+word(move)for i in range(4)))
    def interact(self,direction):self.button(direction,1,16);self.button(1,1,120)
    def victory_party(self):
        self.checks.append({'label':'explicit_native_victory_fixture','slot':0,'species':150,'level':100,'held_item':141,
                             'creation':'native givemon after clearing the disposable research party','cached_hp_and_stats':999,'move':57,
                             'meaning':'Artificial Mewtwo/Surf/Lum Berry fixture, not balance or naturally earned progress; no enemy/outcome edits'})
        self.command('w 2024284 '+'00'*600);self.command('w 2024029 00')
        self.fixture(b'\x79'+word(150)+b'\x64'+word(141)+bytes(9))
        self.expect('native_victory_fixture_has_one_generated_member',self.read(0x02024029,1)[0],1)
        self.strong_party();self.fixture(b'\x7b\x00\x00'+word(57))
    def until(self,key):self.until_message(self.manifest['text_addresses'][key],key)
    def choose(self,yes):self.button(1 if yes else 2,1,120)
    def rock_prompt(self,move):
        self.fixture(b'\x7b\x00\x00'+word(move));self.walk((14,9));self.interact(16)
        self.until('iron_tail_prompt'if move==231 else 'rock_smash_prompt')
    def solve_decline(self,move=231):
        self.rock_prompt(move);self.choose(True);self.until('challenge');self.choose(False);self.finish_event('declined_challenge')
    def sign_retry(self,yes):
        self.walk((14,9));self.interact(32);self.until('retry');self.choose(yes)
    def restart(self,expected):
        history,checks,steps=self.transcript,self.checks,self.steps
        self.close();self.__init__(self.frontend,self.temp,self.output)
        self.transcript=history+[{'command':'<fresh emulator process>','response':{'fresh_process':True}}];self.checks=checks;self.steps=steps
        self.boot(expected)


def matrix(p):
    p.room(0,x=12,y=14);p.expect('original_intro_sets_original_one',p.variable(0x5331),1)
    p.walk((14,10));p.expect('original_intro_hides_actor',p.has_object(1),False);p.expect('original_intro_leaves_new_rock',p.has_object(3),True)
    for value,bit,expected,rock in [(1,False,1,True),(2,False,1,True),(3,False,1,True),(0x7777,False,1,True),
                                    (0x3302,False,0x3302,False),(0x3303,True,0x3303,False),(0x3303,False,0x3302,False),(1,True,1,True)]:
        p.room(value,bit);p.expect(f'migration_{value:04x}_{bit}',p.variable(0x5331),expected)
        p.expect(f'rock_visibility_{value:04x}_{bit}',p.has_object(3),rock)
        p.expect(f'actor_hidden_{value:04x}_{bit}',p.has_object(1),False)
    p.capture('matrix_final')


def puzzle(p):
    p.room();p.moves();p.walk((14,9));before=p.read(0x02024284,600);p.interact(16);p.until('missing_move');p.finish_event('missing_move')
    p.expect('missing_move_keeps_pending',p.variable(0x5331),1);p.expect('missing_move_keeps_rock',p.has_object(3),True)
    p.expect('missing_move_preserves_party_and_pp',p.read(0x02024284,600),before)
    p.fixture(b'\x7b\x00\x00'+word(231));before=p.read(0x02024284,600);p.interact(16);p.until('iron_tail_prompt');p.choose(False);p.finish_event('declined_move')
    p.expect('declined_move_keeps_pending',p.variable(0x5331),1);p.expect('declined_move_keeps_rock',p.has_object(3),True)
    p.expect('declined_move_preserves_party_and_pp',p.read(0x02024284,600),before)
    p.solve_decline(231);p.expect('iron_tail_earns_retry_state',p.variable(0x5331),0x3302)
    p.expect('solved_rock_removed',p.has_object(3),False);p.expect('decline_hides_actor',p.has_object(1),False)
    p.expect('field_move_does_not_consume_pp',p.read(0x02024284,600),before)
    p.moves();p.sign_retry(False);p.finish_event('sign_retry_declined')
    p.expect('retry_without_move_preserves_solved',p.variable(0x5331),0x3302)
    p.expect('declined_retry_does_not_defeat_trainer',trainer_flag(p,929),0)
    p.capture('iron_tail_solved')
    p.room();p.moves();p.solve_decline(249)
    p.expect('rock_smash_fallback_earns_retry',p.variable(0x5331),0x3302);p.expect('fallback_rock_removed',p.has_object(3),False)
    p.capture('rock_smash_solved')


def win(p):
    p.room();p.moves();p.victory_party();p.solve_decline(231)
    p.checks.append({'label':'post_puzzle_battle_move_fixture','slot':0,'move':57})
    p.fixture(b'\x7b\x00\x00'+word(57))
    p.sign_retry(True);p.finish_event('mister_r_real_battle',1800)
    p.frame(120)
    p.expect('actual_win_commits_completed_tag',p.variable(0x5331),0x3303)
    p.expect('actual_battle_loaded_all_six_authored_opponents',sorted(p.enemy_seen),[94,169,197,212,229,248])
    p.expect('actual_win_sets_native_defeated_bit',trainer_flag(p,929),1)
    p.expect('win_hides_actor',p.has_object(1),False);p.expect('win_keeps_rock_removed',p.has_object(3),False)
    p.capture('mister_r_defeated')
    p.interact(32);p.until('completed');p.finish_event('completed_repeat')
    p.expect('completed_repeat_keeps_tag',p.variable(0x5331),0x3303)


def loss(p):
    p.room(0x3302);p.checks.append({'label':'explicit_loss_party_fixture','hp':[1,0,0,0,0,0],'first_cached_stats':1,'move':150,'enemy_or_outcome_writes':False})
    for slot in range(6):p.command(f'w {0x02024284+100*slot+0x56:x} '+word(1 if slot==0 else 0).hex())
    p.command('w 20242d8 0100'+(word(1)*7).hex());p.fixture(b'\x7b\x00\x00'+word(150))
    p.sign_retry(True);p.finish_event('mister_r_real_loss',1500)
    p.expect('loss_preserves_retry_tag',p.variable(0x5331),0x3302)
    p.expect('loss_does_not_set_defeated_bit',trainer_flag(p,929),0)
    p.expect('whiteout_leaves_warehouse',(p.location()['group'],p.location()['map'])!=(6,31),True)
    p.capture('whiteout_location');p.room(0x3302,restore=False)
    p.expect('return_after_loss_has_retry',p.variable(0x5331),0x3302);p.expect('return_after_loss_rock_stays_removed',p.has_object(3),False)


def persistence(p):
    p.room();p.moves();p.victory_party();p.solve_decline(231)
    p.checks.append({'label':'post_puzzle_battle_move_fixture','slot':0,'move':57});p.fixture(b'\x7b\x00\x00'+word(57))
    location=p.location();save_copy(p)
    ready=ROOT/'saves/test/P001-ready-fixture.sav';ready.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p.temp/'copy.sav',ready)
    (ready.with_suffix('.json')).write_text(json.dumps({'kind':'Artificial P001 research fixture','rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'location':location,'state':'0x3302','party':'One native-generated level-100 Mewtwo, Surf, Lum Berry, cached HP/stats 999; forced Orange room; not a normal playthrough or balanced team','source_save_unchanged':True},indent=2)+'\n')
    p.restart(location);p.expect('solved_save_fresh_reload',p.variable(0x5331),0x3302)
    p.expect('solved_reload_removes_rock',p.has_object(3),False);p.expect('solved_reload_hides_actor',p.has_object(1),False)
    # Start actual battle and interrupt before winning; saved retry state must survive.
    p.sign_retry(True);p.frame(300);p.capture('battle_interruption');p.restart(location)
    p.expect('interrupted_attempt_reload_stays_retry',p.variable(0x5331),0x3302)
    p.expect('interrupted_attempt_not_defeated',trainer_flag(p,929),0)
    p.victory_party();p.sign_retry(True);p.finish_event('persisted_real_victory',1800);p.frame(120)
    p.expect('persisted_fixture_earns_win',p.variable(0x5331),0x3303);location=p.location();save_copy(p)
    p.restart(location);p.expect('won_save_fresh_reload',p.variable(0x5331),0x3303)
    p.expect('won_reload_defeated_bit',trainer_flag(p,929),1);p.expect('won_reload_keeps_rock_removed',p.has_object(3),False)
    p.expect('won_reload_hides_actor',p.has_object(1),False);p.capture('completed_fresh_reload')


def exits(p):
    p.room(0x3302);p.walk((12,14),transition=(3,110));p.expect('normal_exit_reaches_route59',(p.location()['group'],p.location()['map']),(3,110))
    p.room(0x3302,x=19,y=7);p.button(16,16,240)
    if (p.location()['group'],p.location()['map'])==(6,31):p.button(16,16,240)
    p.expect('unchanged_stair_destination',(p.location()['group'],p.location()['map']),(0,0));p.capture('stair_destination')


def edge(p):
    p.room();p.moves();p.fixture(b'\x7b\x00\x00'+word(231))
    p.checks.append({'label':'explicit_fainted_knower_fixture','slot':0,'hp':0})
    p.command('w 20242da 0000');p.solve_decline()
    p.expect('fainted_knower_solves_puzzle',p.variable(0x5331),0x3302)
    p.button(8);p.button(2);p.button(2)
    p.expect('menu_return_keeps_rock_hidden',p.has_object(3),False)
    p.expect('menu_return_keeps_actor_hidden',p.has_object(1),False)
    p.room();p.command('w 2024284 '+'00'*600);p.command('w 2024029 00')
    p.checks.append({'label':'explicit_native_egg_fixture','species':25,'move':231,'creation':'native giveegg and setmonmove after clearing disposable party'})
    p.fixture(b'\x7a'+word(25));p.fixture(b'\x7b\x00\x00'+word(231))
    p.expect('native_egg_fixture_count',p.read(0x02024029,1)[0],1)
    p.expect('native_egg_fixture_header_flag',bool(p.read(0x02024284+19,1)[0]&4),True)
    p.walk((14,9));p.interact(16);p.until('missing_move');p.finish_event('egg_rejected')
    p.expect('egg_knower_cannot_solve',p.variable(0x5331),1)
    p.expect('egg_knower_keeps_rock',p.has_object(3),True)
    p.room(0x3302,x=20,y=10)
    p.checks.append({'label':'direct_actor_handler_collision_fixture','entry':[20,10],'root':p.manifest['script_labels']['actor']})
    p.run_root(p.manifest['script_labels']['actor']);p.until('challenge')
    actor=next(o for o in p.objects()if o['local_id']==1 and not o['invisible'])
    p.expect('actor_uses_unoccupied_fallback',(actor['x'],actor['y']),(12,11))
    p.choose(False);p.finish_event('collision_decline')
    # Ordinary trainer battles reject Run. Obtain outcome 4 from a real
    # existing wild encounter, then test the patched continuation directly.
    p.restore();prefix=flagwrite(0x513,True)+flagwrite(0x514,False)+flagwrite(0x54B,False)+flagwrite(0x544,False)+setvar(0x5318,11)
    p.enter(6,23,16,5,prefix=prefix);p.idle()
    p.checks.append({'label':'explicit_escape_speed_fixture','speed':999})
    p.command('w 20242e2 '+word(999).hex());escape_controller(p,0xAD344E,'nonwin_outcome_source')
    p.expect('actual_existing_encounter_escaped',p.read(0x02023E8A,1)[0],4)
    p.room(0x3302,defeated=True,restore=False)
    p.expect('warp_preserves_actual_escape_outcome',p.read(0x02023E8A,1)[0],4)
    p.checks.append({'label':'direct_nonwin_continuation_fixture','root':p.manifest['script_labels']['after_battle'],'outcome_injected':False,'stale_trainer_bit_fixture':True})
    p.run_root(p.manifest['script_labels']['after_battle']);p.finish_event('nonwin_continuation')
    p.expect('escape_result_cannot_complete',p.variable(0x5331),0x3302)
    p.expect('escape_result_clears_stale_trainer_bit',trainer_flag(p,929),0)
    p.capture('edge_complete')


def regression(p):
    laboratory(p);journey(p)
    p.expect('linked_entry_new_rock_present',p.has_object(3),True)


def regions(p):
    for number,label in [(15,'johto_goldenrod'),(10,'kanto_saffron')]:
        p.restore();m,cells=p.cells(3,number)
        occupied=set()
        for kind,stride,xy_offset in [(0,24,4),(1,8,0),(2,16,0)]:
            base=m['events']['arrays'][kind]
            for index in range(m['events']['counts'][kind]):occupied.add(struct.unpack_from('<HH',p.rom,base+index*stride+xy_offset))
        floor={xy for xy,c in cells.items()if c=={'collision':0,'elevation':3,'behavior':0}}
        choices=[(xy,(xy[0]+1,xy[1]))for xy in floor if (xy[0]+1,xy[1])in floor and all(abs(xy[0]-ox)+abs(xy[1]-oy)>2 for ox,oy in occupied)]
        start,target=min(choices,key=lambda pair:abs(pair[0][0]-m['width']//2)+abs(pair[0][1]-m['height']//2))
        p.checks.append({'label':'bounded_region_control_fixture','region':label,'entry':start,'normal_travel':False})
        p.enter(3,number,*start);p.finish_event(label+'_entry')
        p.walk(target);p.expect(label+'_button_movement',(p.location()['x'],p.location()['y']),target)
        p.expect(label+'_unchanged_header',p.map_record(label)['live_matches_default_header'],True)
        p.capture(label)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=['matrix','puzzle','win','loss','persistence','exits','edge','regression','regions'],required=True);parser.add_argument('--debug',action='store_true');args=parser.parse_args()
    out=ROOT/'extracted/runtime/p001'/args.case;out.mkdir(parents=True,exist_ok=True)
    originals=[ROOT/'roms/POKEMON Liquid Crystal.gba',SOURCE_SAVE];hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in originals}
    data={'case':args.case,'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'source_sha256':hashes,'limits':__doc__};p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-p001-')as directory:
            temp=Path(directory);shutil.copyfile(ROM,temp/'copy.gba');(temp/'copy.sav').write_bytes(SOURCE_SAVE.read_bytes()[:0x20000])
            p=PatchJourney(FRONTEND,temp,out)
            try:p.boot();globals()[args.case](p);data['complete']=True
            except Exception as e:
                data['error']=f'{type(e).__name__}: {e}';p.capture('failure_state')
                if args.debug:code.interact(local={'p':p,'data':data})
                raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript,steps=p.steps)
        data['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[str(f.relative_to(ROOT))]for f in originals)
        (out/(args.case+'.json')).write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items()if k not in ('transcript','steps')},indent=2))


if __name__=='__main__':main()
