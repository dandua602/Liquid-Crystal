"""Controlled Orange progression experiments on disposable files and emulator RAM.

Forced map entry, fixture flag writes and party-stat changes are recorded. These
tests establish behavior in those states, not normal story reachability.
"""
import argparse
import hashlib
import json
import selectors
import shutil
import struct
import subprocess
import tempfile
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

from runtime_smoke import ppm_to_png

ROOT = Path(__file__).resolve().parents[1]


def word(value):
    return struct.pack('<H', value)


def setvar(var, value):
    return b'\x16' + word(var) + word(value)


def flagwrite(flag, enabled):
    return bytes([0x29 if enabled else 0x2A]) + word(flag)


def warp(group, number, x, y, index=255):
    return bytes([0x3D, group, number, index]) + word(x) + word(y)


def context(script):
    # Script return stack has 80 bytes at +12. Injected setup code must make
    # no script calls while running there. A terminal goto to a ROM root is
    # safe: later calls may reuse storage after execution has left this RAM.
    if not 0 < len(script) <= 80:
        raise ValueError('Fixture bytecode must fit context stack storage')
    from orange_progression_audit import decoder
    offset=0
    while offset<len(script):
        node,error=decoder(script,offset)
        if error or node['opcode'] not in {0x02,0x05,0x16,0x19,0x1A,0x26,0x29,0x2A,0x2B,0x3D,0x47,0x5B,0x60,0x61,0x62,0x79,0x7A,0x7B,0x7C}:
            raise ValueError('Fixture contains an unsupported or stack-using instruction')
        if node['opcode'] in (0x02,0x05) and node['end']!=len(script):
            raise ValueError('Fixture contains unreachable trailing bytecode')
        offset=node['end']
    result = bytearray(0x74)
    result[1] = 1
    struct.pack_into('<I', result, 8, 0x03000EBC)
    result[12:12+len(script)] = script
    struct.pack_into('<II', result, 0x5C, 0x0815F9B4, 0x0815FD08)
    return result


class Probe:
    def __init__(self, frontend, temp, output):
        self.frontend, self.temp, self.output = frontend, temp, output
        self.transcript, self.checks = [], []
        self.process = subprocess.Popen([str(frontend), str(temp/'copy.gba'), str(temp/'copy.sav')],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        if self.response() != {'ready': True}:
            raise RuntimeError('Frontend did not initialize')
        self.mapper=self.command('m')

    def response(self):
        if not self.selector.select(timeout=30):
            raise TimeoutError('Emulator response timed out')
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError(f'Frontend stopped, exit={self.process.poll()}')
        return json.loads(line)

    def command(self, line):
        self.process.stdin.write(line+'\n'); self.process.stdin.flush()
        response = self.response()
        stable = line.replace(str(self.temp), '<temporary>')
        self.transcript.append({'command': stable, 'response': response})
        return response

    def read(self, address, length):
        return bytes.fromhex(self.command(f'r {address:x} {length}')['hex'])

    def u32(self, address):
        return int.from_bytes(self.read(address,4),'little')

    def frame(self, count, keys=0):
        return self.command(f'f {count} {keys}')

    def capture(self, name):
        path=self.temp/(name+'.ppm')
        self.command(f'p {path}')
        ppm_to_png(path,self.output/(name+'.png'))

    def status(self):
        return self.read(0x03000EA8,1)[0]

    def location(self):
        data=self.read(self.u32(0x03005008),12)
        x,y=struct.unpack_from('<hh',data)
        return {'x':x,'y':y,'group':data[4],'map':data[5],'warp':data[6]}

    def map_record(self, label):
        from warp_graph import MapCatalog
        location=self.location()
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        expected=MapCatalog(rom).resolve(location['group'],location['map'])
        live=self.read(0x02036DFC,28)
        row={'label':label,'location':location,'live_header_hex':live.hex(),
             'default_header':expected['header'],'default_layout':expected['layout'],
             'live_layout':int.from_bytes(live[:4],'little'),
             'live_matches_default_header':live==rom[expected['header']:expected['header']+28]}
        self.checks.append(row)
        return row

    def inject(self, script):
        if self.status()!=2:
            raise RuntimeError('Refusing to replace a running script context')
        self.command(f'w 3000eb0 {context(script).hex()}')
        self.command('w 3000ea8 00'); self.command('w 3000eac 01')

    def idle(self, max_presses=100):
        for _ in range(max_presses):
            if self.status()==2:return
            self.frame(10,1);self.frame(30)
        raise RuntimeError('Script did not return field control within bound')

    def fixture(self, script):
        self.inject(script+b'\x02');self.frame(4);self.idle()

    def enter(self, group, number, x, y, prefix=b'', index=255):
        self.inject(prefix+warp(group,number,x,y,index)+b'\x02');self.frame(240)

    def run_root(self, root):
        self.inject(b'\x05'+struct.pack('<I',root+0x08000000))
        self.frame(120)

    def until_message(self, target, name):
        for _ in range(100):
            if self.u32(0x03000F14)==target+0x08000000:
                self.frame(120);self.capture(name);return
            if self.status()==2:break
            self.frame(10,1);self.frame(30)
        raise RuntimeError(f'Message {target:X} was not reached')

    def variable(self, var):
        if not 0x5000<=var<=0x5562:raise ValueError('Outside verified extended-var range')
        return int.from_bytes(self.read(0x0203D400+2*(var-0x5000),2),'little')

    def flag(self, flag):
        self.fixture(b'\x2B'+word(flag))
        return self.read(0x03000EB2,1)[0]

    def snapshot(self, label, variables=(), flags=()):
        row={'label':label,'location':self.location(),'variables':{f'0x{v:X}':self.variable(v) for v in variables},
             'flags':{f'0x{f:X}':self.flag(f) for f in flags},'status':self.status()}
        self.checks.append(row);return row

    def boot(self):
        for count,keys in [(300,0),(1,8),(180,0),(1,8),(180,0),(1,8),(420,0),
                           (1,1),(300,0),(1,1),(120,0),(1,1),(240,0)]:self.frame(count,keys)
        self.expect('source_save_location',self.location(),{'x':32,'y':29,'group':3,'map':62,'warp':4})
        self.command(f's {self.temp/"baseline.state"}')

    def restore(self):
        self.command(f'l {self.temp/"baseline.state"}')
        self.frame(1)

    def expect(self,label,actual,expected):
        self.checks.append({'label':label,'actual':actual,'expected':expected,'passed':actual==expected})
        if actual!=expected:raise AssertionError(f'{label}: expected {expected}, got {actual}')

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.write('q\n');self.process.stdin.flush()
            try:self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
        self.selector.close()


def validate_native(rom):
    # GetVarPointer hook, range and fixed extended-variable RAM base. Native
    # instruction geometry was disassembled separately and is retained here.
    if struct.unpack_from('<I',rom,0x6E468)[0]!=0x087BAD79:
        raise ValueError('Unexpected variable hook')
    if struct.unpack_from('<II',rom,0x7BADB8)!=(0x5562,0x0203D400):
        raise ValueError('Unexpected extended-variable range/base')
    if struct.unpack_from('<I',rom,0x552B4)[0]!=0x02036DFC or struct.unpack_from('<I',rom,0x40C7C)[0]!=0x02024284:
        raise ValueError('Unexpected current map header/player party literal')
    return [{'start':start,'end':end,'raw_hex':rom[start:end].hex(' ')}
            for start,end in [(0x6E454,0x6E46C),(0x7BAD78,0x7BADC8),(0x55274,0x552C0),(0x40C3C,0x40C80)]]


def map_geometry(rom):
    from warp_graph import MapCatalog
    from map_extract import pointer, u32
    catalog=MapCatalog(rom);rows=[]
    for number in (99,101,107,111):
        m=catalog.resolve(3,number);counts=Counter();cells=[]
        interesting={(w['x'],w['y']) for w in m['warps']} | {(26,17),(18,24)}
        for y in range(m['height']):
            for x in range(m['width']):
                at=m['map_blocks']+2*(y*m['width']+x)
                block=struct.unpack_from('<H',rom,at)[0];tile=block&1023
                secondary=int(tile>=640)
                tileset=pointer(rom,m['layout']+16+4*secondary)
                attr_at=pointer(rom,tileset+20)+4*(tile-640*secondary)
                behavior=u32(rom,attr_at)&511;counts[behavior]+=1
                if (x,y) in interesting:
                    cells.append({'x':x,'y':y,'offset':at,'word':block,'collision':block>>10&3,
                                  'elevation':block>>12,'behavior':behavior,'attribute_offset':attr_at})
        rows.append({'map':m['id'],'layout':m['layout'],'size':[m['width'],m['height']],
                     'behavior_counts':{f'0x{k:X}':v for k,v in sorted(counts.items())},'key_cells':cells})
    return rows


def escape_controller(probe, root, label):
    probe.run_root(root)
    probe.until_message(0xAD3BB4,label+'_warning')
    for _ in range(30):
        probe.frame(10,1);probe.frame(30)
        if probe.read(0x03000EB8,4)==struct.pack('<I',0x08AEFF29):break
    else:raise RuntimeError('Controller did not reach battle continuation')
    probe.frame(420);probe.frame(1,1);probe.frame(240);probe.capture(label+'_battle')
    probe.frame(16,128);probe.frame(16);probe.frame(16,16);probe.frame(16)
    probe.frame(1,1);probe.frame(180);probe.capture(label+'_escape')
    probe.idle(150)


def map_experiments(probe):
    for number in (101,107):
        probe.restore()
        probe.enter(3,number,65535,65535,index=0,prefix=setvar(0x5305,0)+flagwrite(0x52E,False))
        probe.capture(f'route54_{number}_intro')
        probe.idle(200)
        probe.capture(f'route54_{number}_after')
        probe.expect(f'route54_{number}_intro_state',probe.variable(0x5305),1)
        probe.expect(f'route54_{number}_blockers_hidden',probe.flag(0x52E),1)
        record=probe.map_record(f'route54_{number}_loaded_header')
        probe.expect(f'route54_{number}_keeps_map_id',record['location']['map'],number)
        probe.expect(f'route54_{number}_uses_default_header',record['live_matches_default_header'],True)
    for number in (99,111):
        probe.restore()
        probe.enter(3,number,33,19,prefix=flagwrite(0x513,True))
        probe.idle();probe.capture(f'science_{number}_loaded')
        record=probe.map_record(f'science_{number}_loaded_header')
        probe.expect(f'science_{number}_keeps_map_id',record['location']['map'],number)
        probe.expect(f'science_{number}_uses_default_header',record['live_matches_default_header'],True)
    # Physical cave entry/return from each forced variant. Return selection
    # is observed with normal buttons, not another injected warp.
    for number,comparison,x,y,cave in [(107,101,9,19,95),(111,99,33,19,93)]:
        probe.restore()
        prefix=setvar(0x5305,1)+flagwrite(0x52E,True)+flagwrite(0x513,True)
        probe.enter(3,number,x,y,prefix=prefix);probe.idle()
        probe.frame(16,64);probe.frame(240)
        probe.capture(f'variant_{number}_cave_entry')
        if number==111:
            probe.expect('science_copied_warp_does_not_activate_on_ocean_tile',
                         (probe.location()['group'],probe.location()['map']),(3,111))
            # Independently exercise the target cave's ordinary return;
            # this entry is forced and is not credited as an exit from 111.
            probe.enter(5,cave,65535,65535,index=0,prefix=prefix);probe.idle()
        else:
            probe.expect(f'variant_{number}_enters_cave',(probe.location()['group'],probe.location()['map']),(5,cave))
        for _ in range(2):probe.frame(16,128);probe.frame(24)
        probe.frame(240);probe.idle()
        probe.capture(f'variant_{number}_cave_return')
        probe.expect(f'variant_{number}_returns_to_comparison',(probe.location()['group'],probe.location()['map']),(3,comparison))
        probe.map_record(f'variant_{number}_return_header')


def experiments(probe):
    probe.boot()
    # Validate accessor semantics with an artificial, fully reversible state.
    probe.fixture(setvar(0x5318,11)+flagwrite(0x544,True))
    probe.expect('extended_var_roundtrip',probe.variable(0x5318),11)
    probe.expect('flag_set_roundtrip',probe.flag(0x544),1)
    probe.fixture(flagwrite(0x544,False))
    probe.expect('flag_clear_roundtrip',probe.flag(0x544),0)
    map_experiments(probe)
    probe.restore()
    probe.enter(6,23,10,10)
    probe.idle();probe.capture('charging_room')
    for unavailable in (True,False):
        probe.fixture(flagwrite(0x544,unavailable))
        probe.run_root(0xAA2C5D)
        probe.capture('charge_unavailable' if unavailable else 'charge_already_available')
        probe.idle()
        probe.expect('charge_clears_unavailable_'+str(unavailable),probe.flag(0x544),0)
    probe.restore()
    # Exercise the public controller entry with a rejecting charge gate.
    probe.enter(6,23,16,5,prefix=flagwrite(0x513,True)+flagwrite(0x514,False)+flagwrite(0x54B,False)+flagwrite(0x544,True)+setvar(0x5318,11))
    probe.idle()
    probe.frame(1,64);probe.frame(16);probe.frame(1,1);probe.frame(120)
    probe.until_message(0xB01831,'controller_uncharged')
    probe.idle()
    probe.snapshot('after_uncharged_controller',(0x5318,),(0x544,0x54B,0x514))
    probe.expect('rejected_controller_does_not_decrement',probe.variable(0x5318),11)
    probe.expect('rejected_controller_stays_unused',probe.flag(0x54B),0)
    # Start the same controller with available charge and observe a real
    # wild battle. Only the test party's cached speed is increased to allow
    # testing the escape continuation without replacing a battle outcome.
    probe.fixture(flagwrite(0x544,False))
    probe.checks.append({'label':'test_party_speed_fixture','address':0x02024284+0x5E,'value':999})
    probe.command('w 20242e2 '+word(999).hex())
    escape_controller(probe,0xAD344E,'intruder')
    probe.snapshot('after_escape_controller',(0x5318,),(0x544,0x54B,0x514))
    probe.expect('escape_decrements_counter',probe.variable(0x5318),10)
    probe.expect('escape_marks_controller_used',probe.flag(0x54B),1)
    probe.expect('escape_does_not_consume_charge',probe.flag(0x544),0)
    probe.run_root(0xAD344E);probe.idle()
    probe.expect('used_controller_does_not_decrement_twice',probe.variable(0x5318),10)
    probe.fixture(flagwrite(0x54C,False))
    probe.run_root(0xAD354B)
    probe.until_message(0xAD3BB4,'second_controller_accepts_without_recharge')
    probe.checks.append({'label':'second_controller_accepts_without_recharge','message_pointer':probe.u32(0x03000F14),'counter':probe.variable(0x5318)})
    probe.restore()
    prefix=flagwrite(0x513,True)+flagwrite(0x514,False)+flagwrite(0x54B,False)+flagwrite(0x544,False)+flagwrite(0x175A,True)+setvar(0x5318,2)
    probe.enter(6,23,16,5,prefix=prefix);probe.idle()
    probe.command('w 20242e2 '+word(999).hex())
    escape_controller(probe,0xAD344E,'final_controller')
    probe.snapshot('completion_after_escape',(0x5318,),(0x544,0x54B,0x514,0x175A))
    probe.expect('final_counter_reaches_one',probe.variable(0x5318),1)
    probe.expect('final_controller_deactivates_system',probe.flag(0x514),1)
    probe.expect('final_controller_clears_175A',probe.flag(0x175A),0)
    probe.capture('shutdown_complete')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend',type=Path,default=Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'))
    parser.add_argument('--output',type=Path,default=ROOT/'extracted/runtime/progression')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    paths={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
    result={'complete':False,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,
            'frontend_sha256':hashlib.sha256(args.frontend.read_bytes()).hexdigest(),
            'native_variable_evidence':validate_native(paths['rom'].read_bytes()),
            'map_geometry':map_geometry(paths['rom'].read_bytes()),
            'limits':'Forced map entry and fixture state writes in emulator RAM only; no normal progression or save/reload proof.'}
    probe=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-progression-') as directory:
            temp=Path(directory);shutil.copyfile(paths['rom'],temp/'copy.gba')
            (temp/'copy.sav').write_bytes(paths['save'].read_bytes()[:0x20000])
            try:
                probe=Probe(args.frontend,temp,args.output);experiments(probe)
                result['complete']=True
            except Exception:
                if probe:
                    probe.capture('failure_state')
                    result['failure_location']=probe.location()
                    result['failure_context_hex']=probe.read(0x03000EA8,124).hex()
                raise
            finally:
                if probe:probe.close()
    except Exception as error:
        result['error']=f'{type(error).__name__}: {error}'
        raise
    finally:
        if probe:result.update(checks=probe.checks,transcript=probe.transcript,mapper=probe.mapper)
        result['source_unchanged']=all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k] for k,p in paths.items())
        (args.output/'progression.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('transcript','native_variable_evidence')},indent=2))


if __name__=='__main__':main()
