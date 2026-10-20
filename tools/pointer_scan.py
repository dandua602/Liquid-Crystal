"""Raw little-endian ROM-pointer indexing and conservative operand-shape tests.
Pattern matches do not prove script entry alignment or gameplay reachability.
"""
import struct

BASE=0x08000000

def index_pointers(rom):
    incoming={}
    for offset in range(len(rom)-3):
        if rom[offset+3] not in (8,9):continue
        value=struct.unpack_from('<I',rom,offset)[0]-BASE
        if 0<=value<len(rom):incoming.setdefault(value,[]).append(offset)
    return incoming

def classify_operand(rom,offset):
    result={'offset':hex(offset),'aligned_4':offset%4==0,'kind':'RAW_POINTER',
            'context_hex':rom[max(0,offset-10):offset+12].hex(' ')}
    if offset>=2 and rom[offset-2:offset]==b'\x0f\x00':
        result.update(kind='LOADWORD_0_SHAPE',command_offset=hex(offset-2))
        if offset+6<=len(rom) and rom[offset+4]==9:
            result.update(kind='MSGBOX_SHAPE',callstd_index=rom[offset+5])
        return result
    if offset>=1 and rom[offset-1]==0x67:
        result.update(kind='MESSAGE_SHAPE',command_offset=hex(offset-1))
        return result
    # Header is 5C mode trainer:u16 local:u16; pointer count varies by mode.
    text_counts={0:2,1:2,2:2,3:1,4:3,5:2,6:3,7:3,8:3,9:2}
    for index in range(3):
        cmd=offset-6-index*4
        if cmd<0 or rom[cmd]!=0x5C:continue
        mode=rom[cmd+1]
        if index>=text_counts.get(mode,0):continue
        count=text_counts[mode]
        targets=[struct.unpack_from('<I',rom,cmd+6+i*4)[0]-BASE for i in range(count)]
        if not all(0<=x<len(rom) for x in targets):continue
        result.update(kind='TRAINER_TEXT_SHAPE',command_offset=hex(cmd),mode=mode,
                      trainer_id=struct.unpack_from('<H',rom,cmd+2)[0],
                      text_operand_index=index,partner_text_offsets=[hex(x) for x in targets])
        return result
    return result
