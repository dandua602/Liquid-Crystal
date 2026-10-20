"""Native feasibility experiments, not a warehouse implementation.

Only disposable research party/state fixtures and existing game encounters.
No new story, encounter, ROM write, enemy HP or battle-outcome injection.
"""
import hashlib
import json
import shutil
import struct
import tempfile
from datetime import datetime,timezone
from pathlib import Path
from linked_progression import Journey,ROOT,laboratory
from progression_runtime import word,setvar,flagwrite,escape_controller

SIGNATURES={
    0x69F18:'60fd150850041608',
    0x69F3C:'30b5041cfff7dafc0004000c04f084fa051c201cfff7d2fc0004800b044941180448814208d2086879f120fe2880',
    0x6C0A8:'f0b5fdf725fc0004070c02490620088000261ce0d0700302201c2d21d3f790fd002811d1201c391cb9f0f6fc0006000e012809d1024806800248058017e00000d0700302c0700302701c0006060e052e',
    0xCA74C:'01480078704700008a3e0202',
}


def native_evidence(rom):
    identities=((0x15F9B4+4*0x26,0x08069F3D),(0x15F9B4+4*0x7C,0x0806C0A9),
                (0x15FD60+4*0xB4,0x080CA74D))
    for at,expected in identities:
        if struct.unpack_from('<I',rom,at)[0]!=expected:raise ValueError('Unexpected native primitive table identity')
    rows=[]
    for at,expected in SIGNATURES.items():
        raw=bytes.fromhex(expected)
        if rom[at:at+len(raw)]!=raw:raise ValueError(f'Unexpected native primitive bytes at {at:X}')
        rows.append({'offset':at,'raw_hex':expected})
    return rows


def result(p):
    return int.from_bytes(p.read(0x020370D0,2),'little')


def party_move(p):
    p.fixture(b'\x7c'+word(231))
    return result(p)


def outcome(p):
    p.fixture(b'\x26'+word(0x800D)+word(0xB4))
    native=result(p);memory=p.read(0x02023E8A,1)[0]
    p.expect('native_outcome_matches_native_literal_ram',native,memory)
    return native


def replay(p):
    p.boot()
    p.checks.append({'label':'explicit_party_fixture','meaning':'All 24 party move slots set to Tackle on disposable RAM; then Iron Tail added through native setters. No source save changed.'})
    for slot in range(6):
        p.fixture(b''.join(b'\x7b'+bytes([slot,move])+word(33)for move in range(4)))
    p.expect('iron_tail_absent_returns_party_size',party_move(p),6)
    p.fixture(b'\x7b\x00\x00'+word(231))
    p.expect('iron_tail_first_slot_found',party_move(p),0)
    p.expect('first_slot_species_returned',int.from_bytes(p.read(0x020370C0,2),'little'),65)
    p.checks.append({'label':'fainted_party_fixture','address':0x02024284+0x56,'value':0})
    p.command('w 20242da 0000')
    p.expect('native_move_check_accepts_fainted_knower',party_move(p),0)
    p.fixture(b'\x7b\x00\x00'+word(33)+b'\x7b\x05\x03'+word(231))
    p.expect('iron_tail_sixth_slot_found',party_move(p),5)
    p.fixture(b'\x7b\x05\x03'+word(33))
    p.expect('removing_last_iron_tail_restores_absence',party_move(p),6)
    # Existing laboratory trainer encounter; actual battle input and earned
    # G Rank. This rerun adds outcome observability missing in the older case.
    laboratory(p)
    p.expect('existing_laboratory_victory_outcome',outcome(p),1)
    p.restore()
    prefix=flagwrite(0x513,True)+flagwrite(0x514,False)+flagwrite(0x54B,False)+flagwrite(0x544,False)+setvar(0x5318,11)
    p.enter(6,23,16,5,prefix=prefix);p.idle()
    p.checks.append({'label':'escape_speed_fixture','address':0x020242E2,'value':999})
    p.command('w 20242e2 '+word(999).hex())
    escape_controller(p,0xAD344E,'existing_controller')
    p.expect('existing_controller_escape_outcome',outcome(p),4)
    p.expect('escape_does_not_equal_victory',result(p)==1,False)
    p.expect('existing_controller_still_consumes_on_escape',p.variable(0x5318),10)


def main():
    out=ROOT/'extracted/runtime/warehouse_primitives';out.mkdir(parents=True,exist_ok=True)
    files={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(f.read_bytes()).hexdigest()for k,f in files.items()}
    evidence=native_evidence(files['rom'].read_bytes())
    data={'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,'native_evidence':evidence,'limits':__doc__};p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-primitives-')as directory:
            temp=Path(directory);shutil.copyfile(files['rom'],temp/'copy.gba');(temp/'copy.sav').write_bytes(files['save'].read_bytes()[:0x20000])
            p=Journey(Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'),temp,out)
            try:replay(p);data['complete']=True
            except Exception as e:data['error']=f'{type(e).__name__}: {e}';p.capture('failure_state');raise
            finally:p.close()
    finally:
        if p:data.update(checks=p.checks,transcript=p.transcript)
        data['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[k]for k,f in files.items())
        (out/'primitives.json').write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items()if k!='transcript'},indent=2))


if __name__=='__main__':main()
