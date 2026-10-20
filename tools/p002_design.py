"""Compile a P002 design sizing preview. Never modifies or creates a ROM."""
import hashlib
import json
import struct
from pathlib import Path
from build_p001 import Assembler,BASE,h,w
from gba_text_codec import encode
from warp_graph import MapCatalog
from script_extract import event_records
ROOT=Path(__file__).resolve().parents[1]


def preflight(rom,design):
    if hashlib.sha256(rom).hexdigest()!=design['input_rom_sha256']:raise ValueError('Wrong P001 input')
    b=design['budget'];start,end=b['start'],b['end_exclusive']
    if (start,end)!=(0xB9F4E0,0xB9F700)or rom[start:end]!=b'\xff'*544:raise ValueError('Reserve is not pristine')
    gate=design['entry']['gate']
    if gate!={'variable':0x5331,'value':0x3303,'trainer_id':929,'trainer_bit_required':True}:raise ValueError('Unsafe completion gate')
    texts=bytearray();addresses={}
    for key,text in [('entry',design['entry']['prompt']),('npc',design['new_room']['npc']['message'])]:
        addresses[key]=b['text_start']+len(texts);texts+=b'\xfe'.join(encode(s)for s in text.split('\n'))+b'\xff'
    a=Assembler(b['scripts_start'])
    a.label('sign');a.emit(0x69);a.cmp(0x5331,0x3303,'original',5)
    a.emit(0x60,h(929));a.jump('original',0)
    a.msg(design['entry']['original_clue']);a.msg(addresses['entry'],False)
    a.emit(0x6E,b'\x14\x08');a.cmp(0x800D,0,'finish')
    a.emit(0x3D,b'\x06\x20\xff',h(4),h(7));a.emit(0x27)
    a.label('finish');a.emit(0x6B);a.emit(0x02)
    a.label('original');a.emit(0x05,w(BASE+design['entry']['preserve_pending_dispatcher']))
    a.label('npc');a.emit(0x69);a.msg(addresses['npc']);a.jump('finish')
    code=a.resolve()
    c=MapCatalog(rom);donor=c.resolve(*design['new_room']['layout_asset_map']);c.resolve(6,31)
    bank=design['group_bank'];old=c.banks[6]
    if len(old['targets'])!=32 or old['start']!=bank['old_bank']or bank['pointer_site']!=c.groups['start']+24:raise ValueError('Original bank changed')
    if design['new_room']['map']!=[6,32]or bank['preserve_original_words']!=32 or bank['new_header_slot']!=32:raise ValueError('Existing map slot would be overwritten')
    if bank['new_bank']!=b['tables_start']:raise ValueError('Bank allocation changed')
    room=design['new_room'];tables=bytearray(rom[old['start']:old['start']+128])+w(BASE+room['header'])
    header=bytearray(rom[donor['header']:donor['header']+28]);header[4:8]=w(BASE+room['events']);header[8:16]=bytes(8)
    if bank['new_bank']+len(tables)!=room['header']:raise ValueError('Header placement mismatch')
    tables+=header
    if bank['new_bank']+len(tables)!=room['events']:raise ValueError('Events placement mismatch')
    tables+=b'\x01\x01\x00\x00'+w(BASE+room['objects'])+w(BASE+room['warps'])+bytes(8)
    npc=next(e for e in event_records(rom,donor)if e['kind']=='object'and e['local_id']==1)
    obj=bytearray(rom[npc['offset']:npc['offset']+24]);obj[9]=room['npc']['movement_type'];obj[10]=0;obj[16:20]=w(BASE+a.labels['npc']);obj[20:22]=bytes(2)
    if bank['new_bank']+len(tables)!=room['objects']:raise ValueError('Object placement mismatch')
    tables+=obj
    if bank['new_bank']+len(tables)!=room['warps']:raise ValueError('Warp placement mismatch')
    tables+=struct.pack('<hhBBBB',4,8,3,0,31,6)
    for name,data in [('scripts',code),('text',texts),('tables',tables)]:
        if len(data)>b[name+'_capacity']:raise ValueError(name+' budget overflow')
    return {'id':'P002','status':'DESIGN_PREVIEW_ONLY_NOT_IMPLEMENTED','input_rom_sha256':hashlib.sha256(rom).hexdigest(),
            'used':{'scripts':len(code),'text':len(texts),'tables':len(tables)},'capacities':{n:b[n+'_capacity']for n in ('scripts','text','tables')},
            'script_labels':a.labels,'scripts_hex':code.hex(),'text_addresses':addresses,'text_hex':texts.hex(),'tables_hex':tables.hex(),
            'external_pointer_sites':{'group6_bank':bank['pointer_site'],'warehouse_sign':design['entry']['source_sign_pointer_site']},
            'preserved_bank_words':old['targets'],'legacy_unresolved_headers':[{'map':n,'reason':c.resolve(6,n).get('reason')}for n in range(32)if c.resolve(6,n)['status']!='structure_validated'],
            'new_header':room['header'],'shared_donor_layout':donor['layout'],'new_room':[6,32],'no_ROM_output_created':True,
            'limits':'Sizing/data preview, not runtime acceptance or proof of unknown computed owners. New map save rollback requires leaving map6:32 first.'}


def main():
    d=json.loads((ROOT/'research/design/p002.json').read_text());r=preflight((ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes(),d)
    out=ROOT/'extracted/maps/p002_design_preflight.json';out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k]for k in ('status','used','capacities','new_room','legacy_unresolved_headers','no_ROM_output_created')},indent=2))


if __name__=='__main__':main()
