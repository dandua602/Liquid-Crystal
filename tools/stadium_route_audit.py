"""Reproduce inherited warehouse-to-link-room behavior and test the stair seal."""
import hashlib
import json
import shutil
import struct
import tempfile
from pathlib import Path
from p002_runtime import OfficeJourney, ROOT, FRONTEND, SOURCE_SAVE
from warp_graph import MapCatalog
from script_extract import event_records
from build_p002a import SITE, BEFORE, AFTER
from allocation_runtime import save_copy, trainer_flag


def run(name, path, sealed=False):
    output = ROOT/'extracted/runtime/stadium'/name; output.mkdir(parents=True, exist_ok=True)
    data = {'rom_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'fixture': 'Explicit warehouse room/state anchor on disposable five-badge save; normal movement triggers route/seat. No battle data/outcome writes.'}
    p = None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-stadium-') as directory:
            temp = Path(directory); shutil.copyfile(path, temp/'copy.gba'); (temp/'copy.sav').write_bytes(SOURCE_SAVE.read_bytes()[:0x20000])
            p = OfficeJourney(FRONTEND, temp, output)
            p.rom = path.read_bytes(); p.catalog = MapCatalog(p.rom)
            try:
                p.boot(); p.room(0x3303, True, x=19, y=7)
                for _ in range(3): p.button(16, 16, 240)
                p.expect('stair_result', (p.location()['group'], p.location()['map']), (6,31) if sealed else (0,0))
                p.capture('stair_result')
                if sealed:
                    p.expect('blocked_stair_keeps_position', (p.location()['x'],p.location()['y']), (19,7))
                    for value, bit in ((1,False),(0x3303,True)):
                        p.room(value,bit,x=20,y=8)
                        for _ in range(3):p.button(64,16,120)
                        p.expect(f'north_approach_blocked_{value}',p.location(),{'x':20,'y':8,'group':6,'map':31,'warp':255})
                    p.room();p.moves();p.solve_decline();p.walk((14,10));p.walk((14,9))
                    p.expect('puzzle_still_solves',p.variable(0x5331),0x3302)
                    p.expect('solved_rock_still_absent',p.has_object(3),False)
                    p.room(0x3303,True,x=19,y=7)
                    save_copy(p);saved_location=p.location();p.restart(saved_location)
                    p.rom=path.read_bytes();p.catalog=MapCatalog(p.rom)
                    p.expect('completion_survives_hotfix_save_reload',p.variable(0x5331),0x3303)
                    p.expect('trainer_bit_survives_hotfix_save_reload',trainer_flag(p,929),1)
                    p.enter_office(); p.leave_office()
                    p.expect('south_exit_still_reaches_route59', p.variable(0x5331), 0x3303)
                    p.walk((12,14), transition=(3,110))
                    p.expect('actual_south_exit_route59', (p.location()['group'],p.location()['map']), (3,110))
                else:
                    p.walk((3,6)); p.button(64,16,240)
                    for _ in range(8): p.button(1,1,120)
                    p.capture('seat_after_input')
                    data['after_seat'] = {'callback':p.u32(0x030030F4), 'script_pc':p.u32(0x03000EB8),
                                          'player_battlemon_hex':p.read(0x02023BE4,88).hex(), 'enemy_battlemon_hex':p.read(0x02023C3C,88).hex(),
                                          'battle_outcome':p.read(0x02023E8A,1)[0]}
                data['complete'] = True
            finally:
                p.close()
    finally:
        if p: data.update(checks=p.checks, transcript=p.transcript)
        (output/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
    return data


def main():
    original = ROOT/'roms/POKEMON Liquid Crystal.gba'
    p002 = ROOT/'builds/dev/Liquid Crystal P002.gba'
    o, r = original.read_bytes(), p002.read_bytes()
    m = MapCatalog(r).resolve(0,0)
    events = event_records(r,m)
    static = {'legacy_stair_warp': {'site': 0xC30F60, 'source_hex':o[0xC30F60:0xC30F68].hex(), 'p002_hex':r[0xC30F60:0xC30F68].hex()},
              'stadium_map':m, 'events':events, 'seat_scripts':[{'site':at,'hex':r[at:at+12].hex(),'same_as_original':r[at:at+12]==o[at:at+12]}for at in (0x1BB8C3,0x1BB8CF)],
              'native_seat_special':{'index':32,'function':struct.unpack_from('<I',r,0x15FD60+32*4)[0], 'reference':'EnterColosseumPlayerSpot; pinned reference special index, not a trainer-table encounter'}}
    for name,path in [('original',original),('p002',p002),('p002a',ROOT/'builds/dev/Liquid Crystal P002a.gba')]:
        result = run(name,path,name=='p002a')
        static.setdefault('cases',{})[name]={'rom_sha256':result['rom_sha256'],'complete':result['complete'],
                                             'checks_passed':sum(c.get('passed',False) for c in result['checks']), 'after_seat':result.get('after_seat')}
    static['limits'] = 'User route/last save uncertain. Native original/P002 replay reaches legacy link room and stalls after seat input; exact physical garbled battle not reproduced. P002a blocks that stair only, not saved-room recovery or global link-room repair.'
    output = ROOT/'extracted/runtime/stadium/summary.json'
    output.write_text(json.dumps(static,indent=2)+'\n')
    print(json.dumps(static['cases'],indent=2))


if __name__ == '__main__':
    main()
