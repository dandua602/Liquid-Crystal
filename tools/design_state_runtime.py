"""Storage-only fixture for proposed version-tagged room states; not a patch.

Explicit native RAM state/trainer fixtures are not earned puzzle or battle wins.
Only disposable files are saved; original ROM/save bytes stay unchanged.
"""
import hashlib
import json
import shutil
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from allocation_runtime import save_copy,trainer_flag
from allocation_audit import native_evidence
from linked_progression import Journey,ROOT
from progression_runtime import setvar,word


def replay(p):
    p.boot()
    p.checks.append({'label':'explicit_versioned_state_storage_fixture','variable':'0x5331','values':[0x3302,0x3303],
                     'trainer_bit':929,'warning':'Native RAM fixtures only; not earned progression or an allocation'})
    for value in (0x3302,0x3303):
        p.fixture(setvar(0x5331,value))
        p.expect(f'full_width_state_{value:04x}',p.variable(0x5331),value)
        # 1A uses VarGet (literal-or-variable). 19 dereferences a variable
        # pointer directly and is deliberately not used for a literal probe.
        p.fixture(b'\x1a'+word(0x800D)+word(value))
        p.expect(f'frame_table_operand_{value:04x}_is_literal',int.from_bytes(p.read(0x020370D0,2),'little'),value)
    p.fixture(b'\x61'+word(929));p.expect('explicit_completed_bit_fixture',trainer_flag(p,929),1)
    save_copy(p)
    history,checks,steps=p.transcript,p.checks,p.steps
    p.close();p.__init__(p.frontend,p.temp,p.output)
    p.transcript=history+[{'command':'<fresh emulator process>','response':{'fresh_process':True}}];p.checks=checks;p.steps=steps
    p.boot()
    p.expect('tagged_completed_state_survives_actual_save_reload',p.variable(0x5331),0x3303)
    p.expect('completed_bit_survives_with_tagged_state',trainer_flag(p,929),1)
    p.capture('tagged_state_fresh_reload')


def main():
    out=ROOT/'extracted/runtime/design_state';out.mkdir(parents=True,exist_ok=True)
    files={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(f.read_bytes()).hexdigest()for k,f in files.items()}
    native=native_evidence(files['rom'].read_bytes())
    data={'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,'native_evidence':native,'limits':__doc__};p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-design-state-')as directory:
            temp=Path(directory);shutil.copyfile(files['rom'],temp/'copy.gba');(temp/'copy.sav').write_bytes(files['save'].read_bytes()[:0x20000])
            p=Journey(Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'),temp,out)
            try:replay(p);data['complete']=True
            except Exception as e:data['error']=f'{type(e).__name__}: {e}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript)
        data['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[k]for k,f in files.items())
        (out/'design_state.json').write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items()if k!='transcript'},indent=2))


if __name__=='__main__':main()
