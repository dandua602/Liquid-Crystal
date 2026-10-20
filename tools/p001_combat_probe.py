"""Native-stat combat feasibility, not human balance certification.

Generated six-member research teams, native stats/PP and ordinary button input.
No stat boosts, battle HP edits, PP refills, outcome edits or combat save states.
"""
import argparse
import hashlib
import json
import shutil
import struct
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from p001_runtime import PatchJourney,ROOT,ROM,SOURCE_SAVE,FRONTEND
from progression_runtime import word
from allocation_runtime import trainer_flag
from gba_text_codec import parse

TEAM=[('Swampert',285,[57,58,89,231]),('Arcanine',59,[53,245,242,34]),
      ('Machamp',68,[280,157,89,339]),('Ampharos',181,[85,7,86,113]),
      ('Lapras',131,[58,57,85,34]),('Alakazam',65,[94,9,105,115])]
# Gen III internal species IDs differ after Celebi: Swampert is 285.
PARTY_MENU=0x0203B0A0


class CombatJourney(PatchJourney):
    def native_team(self,level):
        self.command('w 2024284 '+'00'*600);self.command('w 2024029 00')
        for slot,(name,species,moves)in enumerate(TEAM):
            self.fixture(b'\x79'+word(species)+bytes([level])+word(141)+bytes(9))
            self.fixture(b''.join(b'\x7b'+bytes([slot,i])+word(move)for i,move in enumerate(moves)))
        self.expect('six_native_generated_members',self.read(0x02024029,1)[0],6)
        rows=[]
        for slot,(name,species,moves)in enumerate(TEAM):
            mon=self.read(0x02024284+100*slot,100);stats=list(struct.unpack_from('<7H',mon,86))
            self.expect(f'native_generated_name_{slot}',parse(mon,8,limit=10)['plain'].upper(),name.upper())
            rows.append({'slot':slot,'name':name,'internal_species':species,'level':mon[84],'hp_maxhp_atk_def_speed_spatk_spdef':stats,'moves':moves,'held_item':141})
            self.expect(f'native_level_{slot}',mon[84],level)
            self.expect(f'native_unboosted_stats_{slot}',all(0<n<500 for n in stats),True)
        self.checks.append({'label':'explicit_native_stat_party_fixture','members':rows,'ev_training':False,'native_random_ivs_and_personalities':True,'normal_playthrough':False})
        # Documented native SaveBlock2 option: SET avoids optional switch prompts;
        # no combat state or statistics are changed by this user-facing option.
        save=self.u32(0x0300500C)
        if not 0x02000000<=save<0x0203FFE0:raise RuntimeError('Unexpected SaveBlock2 pointer')
        before=self.read(save+21,1)[0];self.command(f'w {save+21:x} {before|2:02x}')
        self.checks.append({'label':'explicit_battle_style_set_option','address':save+21,'before':before,'after':before|2})

    def finish_event(self,label,max_presses=600):
        for iteration in range(max_presses):
            if self.field_ready():return
            self.observe_battle(label,iteration)
            callback=self.u32(0x030030F4)
            if 0x0811E000<=callback<0x08121000:
                # Native cursor getter 11FB0C references this struct's slotId.
                cursor=self.read(PARTY_MENU+9,1)[0]
                hp=[int.from_bytes(self.read(0x02024284+100*s+86,2),'little')for s in range(6)]
                healthy=[s for s in range(6)if hp[s]>0]
                if healthy and cursor<6:
                    wanted=healthy[0]
                    self.checks.append({'label':'party_selection_input','callback':callback,'cursor':cursor,'wanted':wanted,'party_hp':hp})
                    self.button(1 if cursor==wanted else 128,1,20)
                    continue
            self.frame(10,1);self.frame(30)
        self.capture('bounded_combat_timeout')
        raise RuntimeError(f'{label} exceeded bounded input budget')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--level',type=int,choices=[95,100],default=95);args=parser.parse_args()
    out=ROOT/f'extracted/runtime/p001/combat_native_{args.level}';out.mkdir(parents=True,exist_ok=True)
    sources=[ROOT/'roms/POKEMON Liquid Crystal.gba',SOURCE_SAVE];hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sources}
    result={'complete':False,'rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'source_sha256':hashes,'started_at_utc':datetime.now(timezone.utc).isoformat(),'level':args.level,'limits':__doc__,
            'input_policy':'A-button first-move attacks; choose first healthy party member on knockout; SET battle style; no bag items, tactical move selection or voluntary switches.'};p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-native-combat-')as directory:
            temp=Path(directory);shutil.copyfile(ROM,temp/'copy.gba');(temp/'copy.sav').write_bytes(SOURCE_SAVE.read_bytes()[:0x20000])
            p=CombatJourney(FRONTEND,temp,out)
            try:
                p.boot();p.room(0x3302);p.native_team(args.level)
                if p.rom[0x11FB0C:0x11FB18]!=bytes.fromhex('0148407a70470000a0b00302'):raise RuntimeError('Native party cursor getter changed')
                p.sign_retry(True);p.finish_event('native_stat_battle',2400)
                outcome=p.read(0x02023E8A,1)[0]
                p.expect('native_combat_reached_decisive_outcome',outcome in (1,2),True)
                p.expect('completion_agrees_with_native_outcome',p.variable(0x5331),0x3303 if outcome==1 else 0x3302)
                p.expect('trainer_bit_agrees_with_native_outcome',trainer_flag(p,929),int(outcome==1))
                result.update(complete=True,outcome=outcome,opponents_observed=sorted(p.enemy_seen))
                p.capture('native_stat_result')
            except Exception as error:
                result['error']=f'{type(error).__name__}: {error}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:result.update(checks=p.checks,transcript=p.transcript)
        result['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[str(f.relative_to(ROOT))]for f in sources)
        (out/'combat.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items()if k not in ('checks','transcript')},indent=2))


if __name__=='__main__':main()
