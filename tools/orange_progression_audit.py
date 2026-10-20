"""Broad Orange travel/gate audit using all 213 standard command widths.

Standard-script table calls are followed explicitly. Native/special calls and
battles remain assumptions; virtual and battle-context jumps stop visibly.
"""
import hashlib
import json
import re
import struct
from collections import Counter
from pathlib import Path

from dialogue_cluster_audit import instruction, trace_graph
from gba_text_codec import parse
from map_extract import pointer,FormatError
from mister_r_audit import SPECS as PRIOR_SPECS, candidate_owners

ROOT=Path(__file__).resolve().parents[1]
TERMS=('orange','valencia','sandway','mandarin','nexus','mister g','mister r','mister z','rudy','danny',
       'science complex','route 59','route 60','old warehouse','prof. ivy','g rank','commanding rank')
FOCUS={'3:109','3:110','6:27','6:28','6:31','5:102'}
STATE_OPS=set(range(0x16,0x23))|{0x25,0x26,0x29,0x2A,0x2B,0x44,0x45,0x47,0x4F,0x50,0x53,0x54,0x55,0x56,0x5C,0x60,0x61,0x62,0x7C,0xA7,0xB6,0xB7}
WARP_OPS=set(range(0x39,0x42))|{0xC4,0xD1}


def standard_specs(source=None):
    source=source if source is not None else (ROOT/'research/references/asm__macros__event.inc').read_text()
    result={}
    for name,body in re.findall(r'\.macro\s+(\w+)[^\n]*\n(.*?)\.endm',source,re.S):
        lines=[line.split('@')[0].strip() for line in body.splitlines()]
        lines=[line for line in lines if line]
        if not lines or not re.fullmatch(r'\.byte 0x[0-9a-fA-F]+',lines[0]):continue
        opcode=int(lines[0].split()[-1],16);widths=[]
        for line in lines[1:]:
            match=re.fullmatch(r'\.(byte|2byte|4byte)\s+(.+)',line)
            if not match:break
            widths += [{'byte':1,'2byte':2,'4byte':4}[match[1]]]*len(match[2].split(','))
        else:result[opcode]=(name,tuple(widths))
    # Macro helpers emit these fields; conditional macros choose separate
    # opcodes for current-map versus specified-map forms.
    helpers={0x50:('applymovementat',(2,4,1,1)),0x52:('waitmovementat',(2,1,1)),
             0x54:('removeobjectat',(2,1,1)),0x56:('addobjectat',(2,1,1)),
             0x58:('showobjectat',(2,1,1)),0x59:('hideobjectat',(2,1,1)),
             0x7E:('bufferleadmonspeciesname',(1,)),0x81:('bufferdecorationname',(1,2)),
             0x84:('bufferstdstring',(1,2)),0xA8:('setobjectsubpriority',(2,1,1,1)),
             0xA9:('resetobjectsubpriority',(2,1,1)),0xBF:('vbufferstring',(1,4)),
             0xC6:('bufferboxname',(1,2)),0xD4:('bufferitemnameplural',(1,2,2))}
    result={**PRIOR_SPECS,**result,**helpers}
    if set(range(0xD5))-{0x5C}-result.keys():raise ValueError('Standard opcode coverage incomplete')
    return result


SPECS=standard_specs()


def decoder(rom,pc):
    node,error=instruction(rom,pc,specs=SPECS)
    if not node:return node,error
    op=node['opcode'];values=node['values']
    if op in (8,9,10,11):
        if op in (10,11) and values[0]>5:return None,'invalid comparison condition'
        index=values[-1]
        if index>=10:return None,'standard-script index outside verified table'
        try:target=pointer(rom,0x160450+4*index)
        except FormatError:return None,'invalid standard-script table pointer'
        node['standard_target']=target
        node['flow_opcode']={8:5,9:4,10:6,11:7}[op]
        node['flow_values']=([values[0]] if op in (10,11) else [])+[target+0x08000000]
    elif op in (0x5E,0x5F,0xBA,0xBB,0xBC,0xBD):
        # Width is known; destination depends on context not tracked here.
        node['flow_opcode']=0x24
        node['dynamic_transfer_note']='Unresolved battle/virtual-address context; no fallthrough inferred'
    elif op in (0x39,0x3A,0x3B,0x3C,0x3D,0xD1):node['resume_kind']='assumed_resume_after_script_warp'
    elif op in (0x6E,0x6F,0x70,0x71):node['resume_kind']='assumed_resume_after_choice_ui'
    elif op==0x5D:node['resume_kind']='assumed_resume_after_trainer_battle'
    return node,None


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();digest=hashlib.sha256(rom).hexdigest()
    scan=json.loads((ROOT/'extracted/maps/map_selection_audit.json').read_text())
    if scan['source_sha256']!=digest:raise ValueError('Stale map scan')
    owners,conditions,flags=candidate_owners(rom,scan['map_record_scan'])
    messages={};text_cache={};rows=[];all_frontiers=Counter();all_nodes=set();state_refs={};flag_refs={}
    def text(at):
        if at not in text_cache:
            parsed=parse(rom,at,limit=4096,strict_english=True) if 0<=at<len(rom) else None
            text_cache[at]=parsed if parsed and parsed['terminated'] and not parsed['issues'] else None
        return text_cache[at]
    for root,associations in sorted(owners.items()):
        graph=trace_graph(rom,root,max_instructions=512,max_states=2048,max_depth=12,decoder=decoder)
        linked={t['target'] for node in graph['nodes'].values() for t in node['texts'] if text(t['target'])}
        relevant={at for at in linked if any(term in text(at)['plain'].lower() for term in TERMS)}
        focus=any(a['map_id'] in FOCUS for a in associations)
        all_frontiers.update(f['reason'] for f in graph['frontiers']);all_nodes.update(graph['nodes'])
        for node in graph['nodes'].values():
            for index,(site,value) in enumerate(zip(node['operand_offsets'],node['values'])):
                if 0x5000<=value<=0x5562 and node['opcode'] in STATE_OPS:
                    state_refs.setdefault(value,{})[site]={'pc':node['pc'],'name':node['name'],'operand_index':index,'site':site}
            if node['opcode'] in (0x29,0x2A,0x2B):
                flag_refs.setdefault(node['values'][0],{})[node['pc']]={'pc':node['pc'],'name':node['name']}
        if not relevant and not focus:continue
        if focus:
            graph=trace_graph(rom,root,max_instructions=2048,max_states=8192,max_depth=16,decoder=decoder)
            linked={t['target'] for node in graph['nodes'].values() for t in node['texts'] if text(t['target'])}
        for at in linked:
            parsed=text(at)
            row=messages.setdefault(at,{'offset':at,'end':parsed['end'],'text':parsed['text'],'roots':[],
                                         'terms':[term for term in TERMS if term in parsed['plain'].lower()]})
            row['roots'].append(root)
        selected=[node for node in graph['nodes'].values() if node['opcode'] in STATE_OPS|WARP_OPS or node['opcode'] in (0x23,0x24)]
        rows.append({'root':root,'owners':associations,'focus':focus,'instruction_count':len(graph['nodes']),
                     'state_count':graph['state_count'],'frontiers':graph['frontiers'],'overlaps':graph['overlaps'],
                     'messages':sorted(linked),'selected_instructions':sorted(selected,key=lambda n:n['pc'])})
    result={'source_sha256':digest,'scope':'4037 candidate owner roots from full-header-passed physical-prefix map slots; 512 instructions/2048 states/depth12 each. Selected Mandarin/Route59/laboratory roots expanded to 2048/8192/depth16. Standard scripts resolved from verified table. Candidate owners are not certified world-map membership.',
            'limits':'Native and special effects, UI and battle resumes remain assumptions. Conditions not solved; virtual/battle-context jumps stop. Standard opcode widths do not prove that modified LC handlers retain every meaning. This audit does not certify unused flags or global absence.',
            'summary':{'candidate_roots':len(owners),'thematic_or_focus_roots':len(rows),'messages':len(messages),
                       'unique_initial_instruction_candidates':len(all_nodes),'initial_frontiers':dict(sorted(all_frontiers.items())),
                       'focus_roots':sum(r['focus'] for r in rows)},
            'command_specs':{f'{op:02X}':{'name':name,'widths':list(widths)} for op,(name,widths) in sorted(SPECS.items())},
            'global_extended_operand_candidates':{f'0x{k:X}':list(v.values()) for k,v in sorted(state_refs.items())},
            'global_flag_command_candidates':{f'0x{k:X}':list(v.values()) for k,v in sorted(flag_refs.items())},
            'roots':rows,'messages':sorted(messages.values(),key=lambda m:m['offset'])}
    (ROOT/'extracted/scripts/orange_progression_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    lines=['# Broad Orange travel and progression script index','',result['scope'],'',result['limits'],'',
           '| Root | Candidate map owners | Instructions | Messages | Frontiers |','|---|---|---:|---:|---:|']
    for r in rows:
        lines.append(f"| 0x{r['root']:X} | "+', '.join(sorted({a['map_id'] for a in r['owners']}))+f" | {r['instruction_count']} | {len(r['messages'])} | {len(r['frontiers'])} |")
    for msg in result['messages']:
        if msg['terms']:lines += ['',f"## 0x{msg['offset']:X}",'',msg['text'],'','Roots: '+', '.join(f'0x{x:X}' for x in msg['roots'])]
    (ROOT/'research/orange_progression_index.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(result['summary'],indent=2))


if __name__=='__main__':main()
