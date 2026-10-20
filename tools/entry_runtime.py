"""Orange authorization, stamped-ticket gate and actual Undersea Express trip.

Uses disposable copies and explicitly recorded story eligibility/entry anchors.
All authorization/stamp acquisition and transport thereafter use NPCs/buttons.
"""
import argparse
import code
import hashlib
import json
import shutil
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from linked_progression import Journey,ROOT
from progression_runtime import flagwrite,word


def state(p,label,flags):
    p.checks.append({'label':label,'flags':{hex(f):p.flag(f) for f in flags},'location':p.location()})


def fixtures(p,values):
    p.checks.append({'label':'explicit_story_eligibility_fixture','flags':{hex(f):v for f,v in values.items()}})
    p.fixture(b''.join(flagwrite(f,v) for f,v in values.items()))


def interact(p,label,direction=64):
    p.button(direction,1,16);p.button(1,1,120)
    p.finish_event(label,1000);p.frame(240);p.capture(label)


def electric_party_fixture(p):
    # Independently checked native party-count literal and retained 100-byte
    # Pokemon layout. Replace only slot 6 in this disposable research party.
    if int.from_bytes(p.rom[0x40C48:0x40C4C],'little')!=0x02024029:
        raise RuntimeError('Party-count native identity changed')
    p.checks.append({'label':'electric_party_fixture','replaced_party_slot':5,
                     'species_id':181,'level':70,'creation':'ordinary givemon script command',
                     'warning':'Artificial Ampharos fixture, not a naturally acquired team'})
    p.command('w 2024478 '+'00'*100);p.command('w 2024029 05')
    p.fixture(b'\x79'+word(181)+bytes([70])+word(0)+bytes(9))
    p.expect('electric_fixture_party_count',p.read(0x02024029,1)[0],6)


def replay(p):
    p.boot();p.strong_party()
    fixtures(p,{0x1702:False,0x1778:False})
    p.enter(2,123,10,14);p.finish_event('office_entry')
    interact(p,'office_without_oak')
    p.expect('office_requires_oak_authorization',p.flag(0x1778),0)
    p.restore();p.strong_party()
    fixtures(p,{0x1701:True,0x1702:False,0x1721:False,0x1722:False,0x1778:False,0x1873:False,0x177F:False,0x1779:False,0x9B:False})
    electric_party_fixture(p)
    p.enter(4,88,13,12);p.finish_event('oak_lab_entry')
    interact(p,'oak_orange_authorization')
    p.expect('oak_awards_orange_authorization',p.flag(0x1702),1)
    p.enter(2,123,10,14);p.finish_event('office_authorized_entry')
    interact(p,'office_ticket_stamp')
    p.expect('office_awards_stamp',p.flag(0x1778),1)
    interact(p,'office_repeat_stamp')
    p.expect('office_repeat_preserves_stamp',p.flag(0x1778),1)
    p.enter(2,121,4,11);p.finish_event('gate_entry')
    state(p,'gate_before_boarding',[0x1778,0x1873,0x177F])
    p.checks.append({'label':'rtc_bytes_before_gate','address':0x0300553C,'hex':p.read(0x0300553C,8).hex()})
    p.button(128,16,120);p.finish_event('station_gate',1000);p.frame(240);p.capture('station_gate_result')
    p.expect('first_trip_passes_gate',(p.location()['group'],p.location()['map']),(3,40))
    p.expect('first_gate_trip_recorded',p.flag(0x1873),1)
    p.walk((64,48),transition=(2,124));p.finish_event('platform_entry')
    p.capture('undersea_platform')
    p.walk((12,9));interact(p,'train_boarding')
    p.expect('train_reaches_interruption_car',(p.location()['group'],p.location()['map']),(2,125))
    p.walk((23,11));interact(p,'officer_accepts_help',direction=16)
    p.expect('officer_opens_engine_access',(p.location()['group'],p.location()['map']),(2,126))
    p.walk((29,8));p.button(64,16,240);p.finish_event('kyogre_encounter',1500);p.frame(240)
    p.capture('kyogre_encounter_complete')
    p.expect('kyogre_encounter_flag',p.flag(0x9B),1)
    p.walk((17,7));interact(p,'non_electric_engine_rejection')
    p.expect('non_electric_does_not_complete_trip',p.flag(0x1779),0)
    p.button(64,1,16);p.button(1,1,120)
    p.until_message(0x95624F,'choose_electric_party_member');p.button(1,1,300)
    p.capture('electric_party_selection')
    for _ in range(5):p.button(128,1,12)
    p.button(1,1,240);p.finish_event('electric_engine_restart',1500);p.frame(240)
    p.capture('valencia_station_arrival')
    p.expect('engine_restart_completes_trip',p.flag(0x1779),1)
    p.expect('train_reaches_valencia_station',(p.location()['group'],p.location()['map']),(1,53))
    p.expect('valencia_arrival_script_consumed',p.variable(0x5301),1)
    p.walk((20,9),transition=(3,77));p.finish_event('valencia_port_entry')
    p.capture('valencia_port_from_train');p.map_record('valencia_port_from_train')
    p.expect('valencia_port_reached',(p.location()['group'],p.location()['map']),(3,77))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--debug',action='store_true')
    args=parser.parse_args();out=ROOT/'extracted/runtime/entry';out.mkdir(parents=True,exist_ok=True)
    files={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(f.read_bytes()).hexdigest()for k,f in files.items()}
    result={'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,
            'limits':'Explicit Oak eligibility flags, initial map anchors and boosted first party member and artificial Ampharos bypass prior Johto/Kanto quests, team acquisition and battle difficulty. Stamp, gate and actual train trip use game events/buttons. Not an entire ordinary playthrough, schedule certification or hardware test.'}
    p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-entry-')as directory:
            temp=Path(directory);shutil.copyfile(files['rom'],temp/'copy.gba');(temp/'copy.sav').write_bytes(files['save'].read_bytes()[:0x20000])
            p=Journey(Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'),temp,out)
            try:replay(p);result['complete']=True
            except Exception as error:
                result['error']=f'{type(error).__name__}: {error}';result['failure_location']=p.location();p.capture('failure_state')
                if args.debug:code.interact(local={'p':p,'result':result})
                raise
            finally:p.close()
    finally:
        if p:result.update(checks=p.checks,steps=p.steps,transcript=p.transcript,mapper=p.mapper)
        result['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[k]for k,f in files.items())
        (out/'entry.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items()if k not in ('transcript','steps')},indent=2))


if __name__=='__main__':main()
