"""Exact-source P001 builder. Only writes new outputs under builds/dev.

Newly authored content follows the explicitly approved design. Native battle
mode 1 provides the continuation required by its exact-win completion contract.
"""
import hashlib
import json
import struct
from pathlib import Path
from bps_patch import create,apply
from gba_text_codec import encode
from map_extract import pointer
from p001_preflight import DIGEST,START,END
ROOT=Path(__file__).resolve().parents[1]
BASE=0x08000000


def h(x):return struct.pack('<H',x)
def w(x):return struct.pack('<I',x)


class Assembler:
    def __init__(self,base):self.base=base;self.data=bytearray();self.labels={};self.fixups=[]
    def label(self,name):
        if name in self.labels:raise ValueError('Duplicate script label')
        self.labels[name]=self.base+len(self.data)
    def emit(self,opcode,*args):
        self.data.append(opcode)
        for arg in args:
            if isinstance(arg,str):self.fixups.append((len(self.data),arg));self.data+=bytes(4)
            else:self.data+=arg
    def jump(self,label,condition=None):
        self.emit(0x05 if condition is None else 0x06,*(([bytes([condition]),label])if condition is not None else [label]))
    def cmp(self,var,value,label,condition=1):self.emit(0x21,h(var),h(value));self.jump(label,condition)
    def set(self,var,value):self.emit(0x16,h(var),h(value))
    def obj(self,opcode,index):self.emit(opcode,h(index))
    def flag(self,enabled):self.emit(0x29 if enabled else 0x2A,h(0x5C5))
    def xy(self,opcode,x,y):self.emit(opcode,h(1),h(x),h(y))
    def call(self,label):self.emit(0x04,label)
    def msg(self,address,wait=True):
        # Standard msgbox pattern also exposes the active text in context
        # data0, as the retained native/UI observers expect.
        self.emit(0x0F,b'\x00',w(BASE+address));self.emit(0x67,w(0));self.emit(0x66)
        if wait:self.emit(0x6D)
    def resolve(self):
        for site,name in self.fixups:
            if name not in self.labels:raise ValueError('Unresolved label '+name)
            self.data[site:site+4]=w(BASE+self.labels[name])
        return bytes(self.data)


def scripts(text):
    a=Assembler(START);state=0x5331;result=0x800D
    a.label('init');a.call('normalize');a.cmp(state,0,'init_original');a.flag(True);a.obj(0x53,1)
    a.cmp(state,1,'init_pending');a.obj(0x53,3);a.emit(0x02)
    a.label('init_original');a.flag(False);a.xy(0x63,12,11);a.obj(0x55,1);a.xy(0x57,12,11)
    a.label('init_pending');a.obj(0x55,3);a.emit(0x02)
    a.label('normalize')
    for value in (0,1,0x3302):a.cmp(state,value,'return')
    a.cmp(state,0x3303,'check_complete');a.set(state,1);a.emit(0x03)
    a.label('check_complete');a.emit(0x60,h(929));a.jump('return',1);a.set(state,0x3302)
    a.label('return');a.emit(0x03)
    a.label('rock');a.emit(0x69);a.call('normalize');a.cmp(state,0x3303,'done');a.cmp(state,0x3302,'challenge')
    a.cmp(state,1,'puzzle');a.jump('finish')
    a.label('puzzle');a.emit(0x7C,h(231));a.cmp(result,6,'iron_prompt',5)
    a.emit(0x7C,h(249));a.cmp(result,6,'smash_prompt',5);a.msg(text['missing_move']);a.jump('finish')
    a.label('iron_prompt');a.msg(text['iron_tail_prompt'],False);a.jump('move_choice')
    a.label('smash_prompt');a.msg(text['rock_smash_prompt'],False)
    a.label('move_choice');a.emit(0x6E,b'\x14\x08');a.cmp(result,0,'finish')
    a.set(state,0x3302);a.obj(0x53,3);a.msg(text['rock_broken']);a.jump('challenge')
    a.label('sign');a.emit(0x69);a.call('normalize');a.msg(0x9761E0)
    a.cmp(state,0x3303,'done');a.cmp(state,0x3302,'retry');a.jump('finish')
    a.label('retry');a.msg(text['retry'],False);a.emit(0x6E,b'\x14\x08');a.cmp(result,0,'finish');a.call('show_npc');a.jump('battle')
    a.label('actor');a.emit(0x69);a.call('normalize');a.cmp(state,0x3303,'done');a.cmp(state,0x3302,'challenge');a.jump('finish')
    a.label('challenge');a.call('show_npc');a.msg(text['challenge'],False);a.emit(0x6E,b'\x14\x08');a.cmp(result,0,'decline')
    a.label('battle');a.emit(0x62,h(929))
    # Mode 0 releases/ends after combat. Mode 1 is the native single-battle
    # continuation variant, necessary for approved exact-result completion.
    a.emit(0x5C,b'\x01',h(929),h(1),w(BASE+text['battle_intro']),w(BASE+text['victory']),'after_battle')
    a.label('after_battle');a.emit(0x26,h(result),h(0xB4));a.cmp(result,1,'not_won',5)
    a.set(state,0x3303);a.emit(0x61,h(929));a.jump('hide_finish')
    a.label('not_won');a.emit(0x62,h(929));a.set(state,0x3302);a.jump('hide_finish')
    a.label('decline');a.msg(text['retry_hint'])
    a.label('hide_finish');a.flag(True);a.obj(0x53,1);a.jump('finish')
    a.label('done');a.msg(text['completed'])
    a.label('finish');a.emit(0x6B);a.emit(0x02)
    a.label('show_npc');a.flag(False);a.emit(0x42,h(0x8000),h(0x8001))
    a.cmp(0x8000,20,'npc_default',5);a.cmp(0x8001,10,'npc_default',5)
    a.xy(0x63,12,11);a.obj(0x55,1);a.xy(0x57,12,11);a.emit(0x5B,h(1),b'\x04');a.emit(0x03)
    a.label('npc_default');a.xy(0x63,20,10);a.obj(0x55,1);a.xy(0x57,20,10);a.emit(0x5B,h(1),b'\x03');a.emit(0x03)
    return a.resolve(),a.labels


def build(source,design):
    if hashlib.sha256(source).hexdigest()!=DIGEST or design['input_rom_sha256']!=DIGEST:raise ValueError('Wrong source ROM')
    if source[START:END]!=b'\xff'*(END-START)or source[0xAC8EAC:0xAC8ED4]!=bytes(40):raise ValueError('Expected allocation bytes changed')
    out=bytearray(source);writes=[]
    def write(at,data,expected,role):
        if source[at:at+len(data)]!=expected:raise ValueError('Expected bytes failed: '+role)
        if any(at<b and a<at+len(data)for a,b in [(r['start'],r['end_exclusive'])for r in writes]):raise ValueError('Overlapping write')
        out[at:at+len(data)]=data;writes.append({'start':at,'end_exclusive':at+len(data),'role':role,'before_sha256':hashlib.sha256(expected).hexdigest(),'after_sha256':hashlib.sha256(data).hexdigest()})
    text=bytearray();addresses={}
    for key,value in design['messages'].items():
        addresses[key]=0xB9F180+len(text)
        text+=b'\xfe'.join(encode(s.replace("'",'’'))for s in value.split('\n'))+b'\xff'
    code,labels=scripts(addresses)
    if len(code)>640 or len(text)>512:raise ValueError(f'Budget overflow: scripts {len(code)}/640, text {len(text)}/512')
    write(START,code,b'\xff'*len(code),'P001 scripts');write(0xB9F180,text,b'\xff'*len(text),'NEWLY_AUTHORED dialogue')
    events=pointer(source,0xC30A24);objects=pointer(source,events+4);bgs=pointer(source,events+16)
    copied=bytearray(source[objects:objects+48]);copied[16:20]=w(BASE+labels['actor'])
    # Existing LC rock template at map1:1 corroborates graphics96. Explicitly
    # override all event ownership/interaction fields for this room's new rock.
    rock=bytearray(24);rock[0]=3;rock[1]=96;struct.pack_into('<HH',rock,4,15,9);rock[9]=8;rock[16:20]=w(BASE+labels['rock'])
    copied+=rock
    background=bytearray(source[bgs:bgs+60]);background[20:24]=w(BASE+labels['sign'])
    header=bytearray(source[events:events+20]);header[0]=3;header[4:8]=w(0x08B9F394);header[16:20]=w(0x08B9F3DC)
    map_table=b'\x02'+w(0x08C099F2)+b'\x04'+w(0x08B9F428)+b'\x07'+w(BASE+labels['init'])+b'\x00'
    tables=header+copied+background+map_table+h(1)+h(1)+w(BASE+labels['init'])+h(0)
    if len(tables)!=178:raise ValueError('Unexpected table footprint')
    write(0xB9F380,tables,b'\xff'*len(tables),'copied room events/map scripts plus new rock')
    write(0xC30A24,w(0x08B9F380),w(0x08C30FA4),'room event pointer')
    write(0xC30A28,w(0x08B9F418),w(0x08C0AA14),'room map-script pointer')
    party=b''.join(struct.pack('<HBxH4H2x',200,p['level'],p['species_id'],*p['move_ids'])for p in design['battle']['party'])
    if len(party)!=96:raise ValueError('Invalid trainer party bytes')
    write(0xB9F480,party,b'\xff'*96,'NEWLY_AUTHORED trainer party')
    trainer=bytearray(source[0xAC804C:0xAC804C+40]);trainer[0]=1;trainer[1]=56;trainer[3]=25
    name=encode('Mister R')+b'\xff';trainer[4:16]=name.ljust(12,b'\x00')
    struct.pack_into('<4H',trainer,16,19,19,0,0);trainer[24]=0;struct.pack_into('<I',trainer,28,7);trainer[32]=6;trainer[36:40]=w(0x08B9F480)
    write(0xAC8EAC,trainer,bytes(40),'new trainer929 record')
    for i,(a,b)in enumerate(zip(source,out)):
        if a!=b and not any(r['start']<=i<r['end_exclusive']for r in writes):raise ValueError('Change outside allowlist')
    if len(out)!=len(source)or out[0xA0:0xC0]!=source[0xA0:0xC0]:raise ValueError('ROM size/header changed')
    manifest={'id':'P001','classification':'NEWLY_AUTHORED approved prototype','source_sha256':DIGEST,'output_sha256':hashlib.sha256(out).hexdigest(),
              'design_canonical_json_sha256':hashlib.sha256(json.dumps(design,sort_keys=True).encode()).hexdigest(),'writes':sorted(writes,key=lambda r:r['start']),
              'script_labels':labels,'text_addresses':addresses,'capacities_used':{'scripts':len(code),'text':len(text),'tables':len(tables),'party':len(party)},
              'implementation_adjustment':'Native mode1 continuation replaces proposed mode0 because mode0 ends the script before the required exact-win gate; ordinary single battle/team behavior preserved.',
              'hardware_tested':False,'runtime_acceptance':'See separately generated P001-validation.json; building alone does not establish runtime acceptance.'}
    return bytes(out),manifest


def main():
    design_path=ROOT/'research/design/p001.json';design=json.loads(design_path.read_text());approval=json.loads((ROOT/'research/design/approval.json').read_text())
    if approval['decision']!='approved for implementation'or approval['design_sha256']!=hashlib.sha256(design_path.read_bytes()).hexdigest():raise ValueError('Reviewed design approval mismatch')
    review_path=ROOT/'research/design/review_manifest.json'
    if hashlib.sha256(review_path.read_bytes()).hexdigest()!=approval['review_manifest_sha256']:raise ValueError('Reviewed manifest changed')
    for name,digest in json.loads(review_path.read_text())['artifacts'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Reviewed artifact changed: '+name)
    source=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();target,manifest=build(source,design)
    again,second=build(source,design)
    if target!=again or manifest!=second:raise ValueError('Nondeterministic build')
    patch=create(source,target,b'Liquid Crystal P001: newly authored warehouse prototype')
    reverse=create(target,source,b'Liquid Crystal P001: restore exact input image')
    if apply(source,patch)!=target or apply(target,reverse)!=source:raise ValueError('BPS roundtrip failed')
    out=ROOT/'builds/dev';out.mkdir(parents=True,exist_ok=True)
    (out/'Liquid Crystal P001.gba').write_bytes(target);(out/'P001.bps').write_bytes(patch);(out/'P001-reverse.bps').write_bytes(reverse)
    manifest['patch_sha256']=hashlib.sha256(patch).hexdigest();manifest['reverse_patch_sha256']=hashlib.sha256(reverse).hexdigest();manifest['deterministic_build_verified']=True;manifest['bps_roundtrip_verified']=True
    manifest['design_file_sha256']=hashlib.sha256(design_path.read_bytes()).hexdigest()
    (out/'P001-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    retained=ROOT/'extracted/builds';retained.mkdir(parents=True,exist_ok=True);(retained/'P001-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'output':str(out/'Liquid Crystal P001.gba'),'sha256':manifest['output_sha256'],'capacities_used':manifest['capacities_used'],'patch_bytes':len(patch),'reverse_bytes':len(reverse)},indent=2))


if __name__=='__main__':main()
