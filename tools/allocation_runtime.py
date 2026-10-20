"""Focused state-allocation experiment; no ROM patch or allocation.

Tests candidate trainer 929's separate defeated bit and proposed room-state
value 2 through native commands, real game Save and a fresh emulator process.
All writes are on a disposable copy; neither candidate is allocated by this test.
"""
import hashlib
import json
import shutil
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from linked_progression import Journey,ROOT
from progression_runtime import setvar,word
from allocation_audit import native_evidence


def trainer_flag(p,index):
    p.fixture(b'\x60'+word(index))
    return p.read(0x03000EB2,1)[0]


def save_copy(p):
    before=hashlib.sha256((p.temp/'copy.sav').read_bytes()).hexdigest()
    p.button(8,1,120)
    for _ in range(4):p.button(128,1,8)
    p.button(1,1,120);p.capture('save_confirm')
    p.button(1,1,180);p.button(1,1,1800);p.frame(600);p.capture('save_complete')
    after=hashlib.sha256((p.temp/'copy.sav').read_bytes()).hexdigest()
    p.expect('copied_save_changed',before!=after,True)
    p.checks.append({'label':'save_mapper','state':p.command('m')})


def replay(p):
    p.boot();index=929;address=0x0203D000+index//8;mask=1<<(index&7)
    initial=trainer_flag(p,index)
    p.checks.append({'label':'candidate_initial_trainer_state','id':index,'defeated':initial,'address':address,'mask':mask,
                     'meaning':'A single supplied save is not an unused-trainer certificate'})
    ordinary_before=p.flag(index)
    p.checks.append({'label':'explicit_test_state_fixture','trainer_id':index,'room_variable':'0x5331','temporary_value':2,'allocation':None})
    p.fixture(b'\x62'+word(index))
    p.expect('clear_command_marks_unbeaten',trainer_flag(p,index),0)
    p.expect('unbeaten_bit_is_one',bool(p.read(address,1)[0]&mask),True)
    before=p.read(0x0203D000,1024)
    p.fixture(b'\x61'+word(index))
    p.expect('set_command_marks_defeated',trainer_flag(p,index),1)
    after=p.read(0x0203D000,1024)
    changes=[i for i,(a,b)in enumerate(zip(before,after))if a!=b]
    p.expect('only_one_trainer_bit_byte_changes',changes,[index//8])
    p.expect('defeated_bit_is_zero',bool(after[index//8]&mask),False)
    p.expect('ordinary_story_flag_is_independent',p.flag(index),ordinary_before)
    p.fixture(setvar(0x5331,2));p.expect('new_room_value_roundtrip',p.variable(0x5331),2)
    save_copy(p)
    history,checks,steps=p.transcript,p.checks,p.steps
    p.close();p.__init__(p.frontend,p.temp,p.output)
    p.transcript=history+[{'command':'<fresh emulator process>','response':{'fresh_process':True}}];p.checks=checks;p.steps=steps
    p.boot();p.capture('fresh_reload')
    p.expect('trainer_defeated_bit_survives_game_save',trainer_flag(p,index),1)
    p.expect('room_value_two_survives_game_save',p.variable(0x5331),2)
    p.expect('reloaded_story_flag_independent',p.flag(index),ordinary_before)
    p.fixture(b'\x62'+word(index));p.expect('clear_after_reload_remains_available',trainer_flag(p,index),0)


def main():
    out=ROOT/'extracted/runtime/allocation';out.mkdir(parents=True,exist_ok=True)
    files={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(f.read_bytes()).hexdigest()for k,f in files.items()}
    native=native_evidence(files['rom'].read_bytes())
    result={'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,'native_trainer_state_evidence':native,'limits':__doc__};p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-allocation-')as directory:
            temp=Path(directory);shutil.copyfile(files['rom'],temp/'copy.gba');(temp/'copy.sav').write_bytes(files['save'].read_bytes()[:0x20000])
            p=Journey(Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'),temp,out)
            try:replay(p);result['complete']=True
            except Exception as error:
                result['error']=f'{type(error).__name__}: {error}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:result.update(checks=p.checks,transcript=p.transcript,mapper=p.mapper)
        result['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[k]for k,f in files.items())
        (out/'allocation.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items()if k!='transcript'},indent=2))


if __name__=='__main__':main()
