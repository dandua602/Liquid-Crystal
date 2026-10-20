"""Bounded FireRed-format linear traces for selected text operand candidates.
This validates instruction boundaries from incoming pointer targets, not map
ownership, command-handler identity, branch state, or runtime reachability.
"""
import json,struct
from pathlib import Path
from pointer_scan import index_pointers
ROOT=Path(__file__).resolve().parents[1]
# Opcode names and operand widths from pinned asm/macros/event.inc.
SPECS={0x00:('nop',()),0x01:('nop1',()),0x02:('end',()),0x03:('return',()),
 0x04:('call',(4,)),0x05:('goto',(4,)),0x06:('goto_if',(1,4)),
 0x07:('call_if',(1,4)),0x08:('gotostd',(1,)),0x09:('callstd',(1,)),
 0x0F:('loadword',(1,4)),0x10:('loadbyte',(1,1)),0x16:('setvar',(2,2)),
 0x17:('addvar',(2,2)),0x18:('subvar',(2,2)),0x19:('copyvar',(2,2)),
 0x1A:('setorcopyvar',(2,2)),0x21:('compare_var_to_value',(2,2)),
 0x22:('compare_var_to_var',(2,2)),0x25:('special',(2,)),
 0x26:('specialvar',(2,2)),0x27:('waitstate',()),0x28:('delay',(2,)),
 0x29:('setflag',(2,)),0x2A:('clearflag',(2,)),0x2B:('checkflag',(2,)),
 0x2F:('playse',(2,)),0x30:('waitse',()),0x31:('playfanfare',(2,)),
 0x32:('waitfanfare',()),0x44:('additem',(2,2)),0x45:('removeitem',(2,2)),
 0x46:('checkitemspace',(2,2)),0x47:('checkitem',(2,2)),
 0x4F:('applymovement',(2,4)),0x51:('waitmovement',(2,)),
 0x53:('removeobject',(2,)),0x55:('addobject',(2,)),0x5A:('faceplayer',()),
 0x66:('waitmessage',()),0x67:('message',(4,)),0x68:('closemessage',()),
 0x69:('lockall',()),0x6A:('lock',()),0x6B:('releaseall',()),
 0x6C:('release',()),0x6D:('waitbuttonpress',())}
TEXTS=[0x930C7D,0xB11C47,0xB1D4E0,0x9E2B2D,0xA9C482]

def decode_linear(rom,start,required,max_bytes=256):
    pos=start;trace=[];seen=False;reason='byte limit'
    while pos<min(len(rom),start+max_bytes):
        at=pos;op=rom[pos];pos+=1
        if op==0x5C:
            if pos+5>len(rom):reason='truncated trainer header';break
            mode=rom[pos];count={0:2,1:3,2:3,3:1,4:3,5:2,6:4,7:3,8:4,9:2}.get(mode)
            if count is None:reason='unsupported trainer mode';break
            pos=at+6+4*count;name='trainerbattle';values=[mode,struct.unpack_from('<H',rom,at+2)[0]]
        elif op in SPECS:
            name,widths=SPECS[op];values=[]
            for width in widths:
                values.append(int.from_bytes(rom[pos:pos+width],'little'));pos+=width
        else:reason=f'unsupported opcode {op:02X} at {at:#x}';break
        if pos>min(len(rom),start+max_bytes):reason='truncated instruction';break
        trace.append({'offset':hex(at),'opcode':hex(op),'name':name,'operands':[hex(v) for v in values],'raw_hex':rom[at:pos].hex(' ')})
        seen=seen or at==required
        if op in (2,3,5,6,7,8):reason='control-flow boundary';break
    return {'entry':hex(start),'contains_required_command_at_instruction_boundary':seen,'stop_reason':reason,'instructions':trace}

def run():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();idx=index_pointers(rom)
    audit=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text());results=[]
    for target in TEXTS:
        entry=next(e for e in audit['records'] if int(e['offset'],16)==target)
        refs=[r for r in entry['references'] if r['kind']=='MSGBOX_SHAPE']
        traces=[]
        for ref in refs:
            command=int(ref['command_offset'],16)
            for start in sorted(x for x in idx if command-64<=x<=command):
                trace=decode_linear(rom,start,command)
                if trace['contains_required_command_at_instruction_boundary']:
                    trace['incoming_pointer_sites']=[hex(p) for p in idx[start]]
                    traces.append(trace)
        results.append({'text_offset':hex(target),'command_candidates':[r['command_offset'] for r in refs],
                        'trace_status':'BOUNDED_FORMAT_PATH_FOUND' if traces else 'UNRESOLVED',
                        'reachability':'UNKNOWN','traces':traces})
    data={'source_sha256':audit['summary']['source_sha256'],
          'method':'Pinned FireRed opcode formats; only uninterrupted linear paths counted. Stops at unsupported opcodes or branch boundaries. Incoming pointers are raw references, not certified map/script roots. Callstd/native effects and trainer battle continuation are not simulated.',
          'results':results}
    (ROOT/'extracted/pointers/selected_text_traces.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps([{'text':r['text_offset'],'status':r['trace_status'],'entries':[t['entry'] for t in r['traces']]} for r in results],indent=2))
    return data
if __name__=='__main__':run()
