"""Linked late-Orange journey and laboratory battle on disposable copies.

One forced starting map per case. Subsequent journey transitions use normal
buttons. A recorded level/stats/moves fixture makes battles and Surf testable;
no battle outcome is injected. Original source files are never written.
"""
import argparse
import code
import hashlib
import json
import shutil
import struct
import tempfile
from collections import deque
from datetime import datetime,timezone
from pathlib import Path

from map_extract import pointer,u32
from progression_runtime import Probe,ROOT,setvar,word
from warp_graph import MapCatalog


class Journey(Probe):
    def __init__(self,*args):
        super().__init__(*args)
        self.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.catalog=MapCatalog(self.rom);self.cells_cache={};self.steps=[]

    def boot(self):
        super().boot()
        # gMain callback2 identity is sampled in verified source-save field
        # control. ScriptContext alone can remain idle during wild battles.
        self.field_callback=self.u32(0x030030F4)
        if not (0x08000001<=self.field_callback<0x09000000 and self.field_callback&1):
            raise RuntimeError('Invalid field callback identity')
        self.checks.append({'label':'source_field_callback2','address':0x030030F4,'value':self.field_callback})

    def field_ready(self):
        return self.status()==2 and self.u32(0x030030F4)==self.field_callback

    def strong_party(self):
        # Retained include/pokemon.h: cached level/mail at +54/+55; eight
        # 16-bit fields from HP through special defense follow at +56.
        # setmonmove handler 0x6C07C..0x6C0A8 matches supplied FireRed.
        self.checks.append({'label':'artificial_battle_and_surf_fixture','party_slot':0,'level':100,
                            'hp_and_stats':999,'moves':{'slot0':332,'slot1':57},
                            'meaning':'Aerial Ace and Surf; not a naturally obtained team or difficulty test'})
        self.command('w 20242d8 6400'+(word(999)*7).hex())
        self.fixture(b'\x7b\x00\x00'+word(332)+b'\x7b\x00\x01'+word(57))

    def has_item(self,item):
        self.fixture(b'\x47'+word(item)+word(1))
        address=u32(self.rom,0x15FD0C+13*4)
        if address!=0x020370D0:raise RuntimeError('Special RESULT identity changed')
        return int.from_bytes(self.read(address,2),'little')

    def cells(self,group,number):
        key=group,number
        if key in self.cells_cache:return self.cells_cache[key]
        m=self.catalog.resolve(group,number);result={}
        for y in range(m['height']):
            for x in range(m['width']):
                at=m['map_blocks']+2*(y*m['width']+x)
                raw=int.from_bytes(self.rom[at:at+2],'little');tile=raw&1023;secondary=int(tile>=640)
                ts=pointer(self.rom,m['layout']+16+4*secondary)
                attr=u32(self.rom,pointer(self.rom,ts+20)+4*(tile-640*secondary))
                result[x,y]={'collision':raw>>10&3,'elevation':raw>>12,'behavior':attr&511}
        self.cells_cache[key]=m,result
        return m,result

    def objects(self):
        data=self.read(0x02036E38,16*36);result=[]
        location=self.location();player=[]
        for index in range(16):
            row=data[index*36:(index+1)*36]
            if not row[0]&1:continue
            x,y=struct.unpack_from('<hh',row,16);x-=7;y-=7
            entry={'index':index,'local_id':row[8],'x':x,'y':y,'player':bool(row[2]&1),
                   'group':row[10],'map':row[9],'invisible':bool(row[1]&32)}
            if entry['player']:player.append(entry)
            else:result.append(entry)
        if len(player)!=1 or (player[0]['x'],player[0]['y'])!=(location['x'],location['y']):
            raise RuntimeError('Runtime object layout did not match player position')
        return result

    def walk(self,target,transition=None,max_steps=700):
        location=self.location();key=location['group'],location['map'];start=(location['x'],location['y'])
        m,cells=self.cells(*key)
        blocked_edges=set()
        warps={(w['x'],w['y']) for w in m['warps']} - {target,start}
        for attempt in range(max_steps):
            location=self.location()
            if (location['group'],location['map'])!=key:
                if transition is None:raise RuntimeError('Unexpected map transition while walking')
                self.expect(f'button_transition_{key}_{target}',(location['group'],location['map']),transition)
                return
            start=(location['x'],location['y'])
            if start==target and transition is None:return
            objects={(o['x'],o['y']) for o in self.objects() if not o['invisible']}
            queue=deque([start]);parents={start:None}
            while queue and target not in parents:
                x,y=queue.popleft()
                for pos in ((x,y-1),(x-1,y),(x+1,y),(x,y+1)):
                    if pos in parents or pos not in cells or (start,pos) in blocked_edges:continue
                    door_goal=pos==target and transition is not None and cells[pos]['behavior'] in (0x60,0x69)
                    if (cells[pos]['collision'] and not door_goal) or pos in objects|warps:continue
                    if ((x,y),pos) in blocked_edges:continue
                    parents[pos]=(x,y);queue.append(pos)
            if target not in parents:raise RuntimeError(f'No candidate walking path from {start} to {target} in {key}')
            path=[];pos=target
            while pos!=start:path.append(pos);pos=parents[pos]
            if not path:
                direction={0x60:64,0x62:16,0x63:32,0x64:64,0x65:128,0x69:64,0x6C:16,0x6D:32,0x6E:16,0x6F:32}.get(cells[start]['behavior'])
                if direction is None:raise RuntimeError('Standing on an unsupported warp activation tile')
                self.frame(16,direction);self.frame(240)
                continue
            pos=path[-1];delta=pos[0]-start[0],pos[1]-start[1]
            keys={(0,-1):64,(-1,0):32,(1,0):16,(0,1):128}[delta]
            self.frame(16,keys);self.frame(24)
            after=self.location();self.steps.append({'map':list(key),'from':list(start),'requested':list(pos),'after':after})
            if not self.field_ready():
                self.capture(f'walking_event_{len(self.steps)}')
                self.finish_event('walking_battle_or_event',700)
                # Restore this fixture's move PP between encounters using
                # the ordinary encrypted-party setter, without state flags.
                self.strong_party()
            if (after['group'],after['map'])!=key:
                self.frame(180)
                continue
            if (after['x'],after['y'])==start:
                if cells[pos]['behavior'] in (0x10,0x11,0x12,0x15):
                    self.frame(1,1);self.frame(120);self.capture(f'surf_prompt_{len(self.steps)}');self.idle(100)
                    changed=self.location()
                    if (changed['x'],changed['y'])!=start:continue
                blocked_edges.add((start,pos))
        raise RuntimeError('Walking step budget exceeded')

    def button(self,keys,frames=1,settle=120):
        self.frame(frames,keys);self.frame(settle)

    def finish_event(self,label,max_presses=600):
        messages=set()
        for iteration in range(max_presses):
            if self.field_ready():
                self.checks.append({'label':label+'_observed_message_pointers','pointers':sorted(messages)})
                return
            if hasattr(self,'observe_battle'):self.observe_battle(label,iteration)
            message=self.u32(0x03000F14)
            if message not in messages:
                messages.add(message)
                if message>=0x08000000:self.capture(label+f'_text_{message:08X}')
            if iteration%16==0:
                # BattlePokemon layout is retained in include/pokemon.h.
                # Validate the full known fixture fingerprint before any
                # test-only PP refill; never edit enemy HP or an outcome.
                mon=self.read(0x02023BE4,88)
                if (mon[2:12]==word(999)*5 and mon[12:14]==word(332) and mon[0x2A]==100 and mon[0x24]<=1):
                    self.checks.append({'label':'battle_pp_refill_fixture','address':0x02023C08,'value':99,
                                        'verified_player_battlemon_prefix':mon[:20].hex()})
                    self.command('w 2023c08 63')
            self.frame(10,1);self.frame(30)
        raise RuntimeError(label+' did not finish')


def laboratory(p):
    p.restore();p.strong_party()
    p.enter(5,102,65535,65535,index=0)
    p.capture('laboratory_entry')
    p.finish_event('laboratory',1000)
    p.expect('laboratory_intro_state',p.variable(0x5315),1)
    p.expect('laboratory_rank_flag',p.flag(0x513),1)
    p.expect('laboratory_awarded_g_rank',p.has_item(0x114),1)
    p.map_record('laboratory_after_battle');p.capture('laboratory_complete')
    p.checks.append({'label':'laboratory_final_location','location':p.location()})


def journey(p,restore=True):
    if restore:p.restore()
    p.strong_party()
    # Start immediately below the director-floor coordinate event. The
    # rescue, key award and every following map transition use game scripts
    # and buttons, without setting their progression flags in the fixture.
    p.enter(6,27,9,11)
    p.idle();p.capture('police_before_rescue')
    p.button(64,16,120)
    p.finish_event('police_rescue',1000)
    p.expect('police_rescue_flag',p.flag(0x5BA),1)
    p.expect('police_awarded_old_key',p.has_item(0x116),1)
    p.strong_party()
    p.map_record('police_rescue_landing');p.capture('police_after_rescue')
    print('Rescue complete:',p.location(),flush=True)
    p.walk((9,13),transition=(3,109))
    p.capture('mandarin_after_police');p.map_record('mandarin_after_police')
    p.walk((11,5),transition=(6,28))
    p.capture('gatehouse_entry')
    p.walk((7,1),transition=(3,110))
    p.capture('route59_from_gatehouse');p.map_record('route59_from_gatehouse')
    p.walk((11,24))
    p.capture('warehouse_door_before_unlock')
    p.expect('old_key_unlock_not_already_set',p.flag(0x5C1),0)
    p.button(64,1,16);p.button(1,1,120)
    p.finish_event('warehouse_unlock')
    p.expect('old_key_unlock_from_interaction',p.flag(0x5C1),1)
    p.capture('warehouse_unlocked')
    p.walk((11,23),transition=(6,31))
    p.finish_event('mister_r_intro')
    p.expect('mister_r_intro_consumed',p.variable(0x5331),1)
    p.expect('mister_r_removed',p.flag(0x5C5),1)
    p.capture('linked_mister_r_end');p.map_record('linked_mister_r_end')


def save_reload(p):
    p.command(f's {p.temp/"pre_save.state"}')
    before=hashlib.sha256((p.temp/'copy.sav').read_bytes()).hexdigest()
    p.button(8,1,120);p.capture('save_start_menu')
    for _ in range(4):p.button(128,1,8)
    p.button(1,1,120);p.capture('save_confirmation')
    p.button(1,1,180);p.capture('save_overwrite_confirmation')
    p.button(1,1,1800)
    for _ in range(12):
        after=hashlib.sha256((p.temp/'copy.sav').read_bytes()).hexdigest()
        if after!=before:break
        p.frame(300)
    p.frame(600)
    after=hashlib.sha256((p.temp/'copy.sav').read_bytes()).hexdigest()
    p.capture('save_result')
    p.expect('game_save_changes_copied_flash',after!=before,True)
    p.checks.append({'label':'save_mapper_state','state':p.command('m')})
    p.button(1,1,120);p.close()
    history,checks,steps=p.transcript,p.checks,p.steps
    p.__init__(p.frontend,p.temp,p.output)
    q=p
    q.transcript=history+[{'command':'<restart frontend from copied SRAM>','response':{'fresh_process':True}}]
    q.checks=checks;q.steps=steps
    q.checks.append({'label':'reload_mapper_state','state':q.mapper})
    for count,keys in [(300,0),(1,8),(180,0),(1,8),(180,0),(1,8),(420,0)]:q.frame(count,keys)
    q.capture('reloaded_continue_menu')
    for _ in range(3):q.button(1,1,240)
    q.capture('reloaded_mister_r_room')
    q.expect('reloaded_room',(q.location()['group'],q.location()['map']),(6,31))
    q.expect('reloaded_intro_state',q.variable(0x5331),1)
    for flag in (0x5BA,0x5C1,0x5C5):q.expect(f'reloaded_flag_{flag:X}',q.flag(flag),1)
    q.expect('reloaded_old_key',q.has_item(0x116),1)
    target=ROOT/'saves/test/linked-orange-fixture.sav';target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(q.temp/'copy.sav',target)
    metadata={'filename':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,
              'kind':'Generated emulator fixture, 128 KiB cartridge save payload only; original FlashGBX footer remains in source save',
              'warning':'Forced Orange starting positions and boosted first-party level/stats/moves; not a normal player save',
              'source_save_sha256':hashlib.sha256((ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav').read_bytes()).hexdigest()}
    (ROOT/'saves/test/linked-orange-fixture.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return q


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=['lab','journey','all'],default='all')
    parser.add_argument('--debug',action='store_true',help='Open a research console at failure before cleanup')
    parser.add_argument('--output',type=Path,default=ROOT/'extracted/runtime/linked')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    files={'rom':ROOT/'roms/POKEMON Liquid Crystal.gba','save':ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()}
    result={'complete':False,'case':args.case,'started_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashes,
            'limits':'One forced starting map per case, artificial first-party battle/Surf setup and recorded PP refills. All later journey transitions use buttons. No ordinary Johto/Kanto-to-Orange playthrough, balance or hardware proof.'}
    p=None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-linked-') as directory:
            temp=Path(directory);shutil.copyfile(files['rom'],temp/'copy.gba');(temp/'copy.sav').write_bytes(files['save'].read_bytes()[:0x20000])
            p=Journey(Path('/workspace/.cache/liquid-crystal-runtime/mgba-probe'),temp,args.output)
            try:
                p.boot()
                if args.case in ('lab','all'):laboratory(p)
                if args.case in ('journey','all'):
                    journey(p,restore=args.case!='all')
                    p=save_reload(p)
                result['complete']=True
            except Exception as error:
                result['error']=f'{type(error).__name__}: {error}';p.capture('failure_state');result['failure_location']=p.location()
                result['failure_context']=p.read(0x03000EA8,124).hex()
                if args.debug:code.interact(local={'p':p,'result':result})
                raise
            finally:p.close()
    finally:
        if p:result.update(checks=p.checks,steps=p.steps,transcript=p.transcript)
        if p:result['mapper']=p.mapper
        result['source_unchanged']=all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[k] for k,f in files.items())
        (args.output/'linked.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('transcript','steps')},indent=2))


if __name__=='__main__':main()
