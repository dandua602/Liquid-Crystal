"""Bounded static script paths and neighboring dialogue, never runtime reachability.
All semantic names use the retained FireRed reference; LC handlers are not verified.
"""
import bisect,hashlib,json,struct
from collections import Counter,deque
from pathlib import Path
from gba_text_codec import parse
from pointer_scan import BASE,index_pointers
from text_reference_trace import SPECS

ROOT=Path(__file__).resolve().parents[1]
SPECS=dict(SPECS)
SPECS.update({0x23:('callnative',(4,)),0x24:('gotonative',(4,)),
 0x33:('playbgm',(2,1)),0x34:('savebgm',(2,)),0x35:('fadedefaultbgm',()),
 0x36:('fadenewbgm',(2,)),0x37:('fadeoutbgm',(1,)),0x38:('fadeinbgm',(1,)),
 0x60:('checktrainerflag',(2,)),0x61:('settrainerflag',(2,)),0x62:('cleartrainerflag',(2,)),
 0x83:('buffernumberstring',(1,2)),0x85:('bufferstring',(1,4)),
 0x97:('fadescreen',(1,)),0x98:('fadescreenspeed',(1,1)),0xA2:('setmetatile',(2,2,2,2)),
 0xA1:('playmoncry',(2,2)),0xB6:('setwildbattle',(2,1,2)),0xB7:('dowildbattle',()),
 0xC7:('textcolor',(1,))})
TRAINER_TEXT_COUNTS={0:2,1:2,2:2,3:1,4:3,5:2,6:3,7:3,8:3,9:2}
CONTINUATION_MODES={1,2,6,8}


def instruction(rom,pc,specs=None):
    specs=SPECS if specs is None else specs
    if not 0<=pc<len(rom):return None,'out-of-ROM address'
    op=rom[pc];pos=pc+1;values=[];fields=[];texts=[];continuation=None
    if op==0x5C:
        if pos+5>len(rom):return None,'truncated trainer header'
        mode=rom[pos];count=TRAINER_TEXT_COUNTS.get(mode)
        if count is None:return None,f'unsupported trainer mode {mode}'
        if pc+6+4*(count+(mode in CONTINUATION_MODES))>len(rom):return None,'truncated trainer operands'
        values=[mode,int.from_bytes(rom[pc+2:pc+4],'little'),int.from_bytes(rom[pc+4:pc+6],'little')]
        fields=[pc+1,pc+2,pc+4];pos=pc+6
        roles=['defeat','victory'] if mode==9 else (['defeat'] if mode==3 else ['intro','defeat','cannot_battle'])
        for i in range(count):
            value=struct.unpack_from('<I',rom,pos)[0];values.append(value);fields.append(pos)
            texts.append({'pointer_offset':pos,'target':value-BASE,'role':'trainer_'+roles[i]});pos+=4
        if mode in CONTINUATION_MODES:
            continuation=struct.unpack_from('<I',rom,pos)[0]-BASE;values.append(continuation+BASE);fields.append(pos);pos+=4
        name='trainerbattle'
    elif op in specs:
        name,widths=specs[op]
        if pos+sum(widths)>len(rom):return None,'truncated operands'
        for width in widths:
            fields.append(pos);values.append(int.from_bytes(rom[pos:pos+width],'little'));pos+=width
        if op in (6,7) and values[0]>5:return None,'invalid comparison condition'
        if op==0x67 and values[0]:texts.append({'pointer_offset':fields[0],'target':values[0]-BASE,'role':'message'})
        if op==0x85 and values[1]:texts.append({'pointer_offset':fields[1],'target':values[1]-BASE,'role':'bufferstring'})
        if op==0x0F and values[0]==0 and pos+2<=len(rom) and rom[pos]==9 and 2<=rom[pos+1]<=6:
            texts.append({'pointer_offset':fields[1],'target':values[1]-BASE,'role':'loadword_then_callstd'})
    else:return None,f'unsupported opcode {op:02X}'
    return {'pc':pc,'end':pos,'opcode':op,'name':name,'values':values,'operand_offsets':fields,
            'raw_hex':rom[pc:pos].hex(' '),'texts':texts,'trainer_continuation':continuation},None


def trace_graph(rom,root,max_instructions=512,max_states=2048,max_depth=8,decoder=None):
    decoder=instruction if decoder is None else decoder
    first=(root,());queue=deque([first]);parents={first:None};seen=set();nodes={};edges=[];frontiers=[];paths={}
    def add(state,dest,stack,kind):
        source=state[0];edges.append({'source':source,'target':dest,'kind':kind})
        next_state=(dest,stack)
        if not 0<=dest<len(rom):frontiers.append({'pc':source,'target':dest,'reason':'non-ROM target','edge_kind':kind});return
        if len(stack)>max_depth:frontiers.append({'pc':source,'target':dest,'reason':'call-depth limit'});return
        if next_state not in parents:parents[next_state]=(state,kind);queue.append(next_state)
    while queue and len(seen)<max_states:
        state=queue.popleft();pc,stack=state
        if state in seen:continue
        seen.add(state)
        if pc not in nodes and len(nodes)>=max_instructions:
            frontiers.append({'pc':pc,'reason':'instruction limit'});continue
        ins,error=decoder(rom,pc)
        if error:frontiers.append({'pc':pc,'reason':error});continue
        nodes[pc]=ins;paths.setdefault(pc,state);op=ins.get('flow_opcode',ins['opcode']);v=ins.get('flow_values',ins['values']);end=ins['end']
        if op in (2,0x0C,0x0D):continue
        if op==3:
            if stack:add(state,stack[-1],stack[:-1],'return')
        elif op in (5,6):
            if op==6:add(state,end,stack,'condition_false')
            add(state,v[-1]-BASE,stack,'goto' if op==5 else 'condition_true')
        elif op in (4,7):
            if op==7:add(state,end,stack,'condition_false')
            add(state,v[-1]-BASE,stack+(end,),'call' if op==4 else 'condition_true_call')
        elif op in (8,0x24):frontiers.append({'pc':pc,'reason':'opaque terminal standard/native transfer'})
        elif op==0x5C:
            add(state,end,stack,'engine_postbattle_candidate')
            if ins['trainer_continuation'] is not None:add(state,ins['trainer_continuation'],stack,'engine_beaten_script_candidate')
        else:
            kind={9:'assumed_return_after_callstd',0x23:'assumed_return_after_native',
                  0x25:'assumed_return_after_special',0x26:'assumed_return_after_specialvar',
                  0x27:'assumed_resume_after_waitstate',0xB7:'assumed_resume_after_wildbattle'}.get(op,'next')
            add(state,end,stack,ins.get('resume_kind',kind))
    if queue:frontiers.append({'pc':queue[0][0],'reason':'state limit'})
    spans=sorted((pc,n['end']) for pc,n in nodes.items());overlaps=[]
    for i,(pc,end) in enumerate(spans):
        if i and pc<spans[i-1][1]:overlaps.append({'pc':pc,'overlaps_instruction_at':spans[i-1][0]})
    def witness(pc):
        state=paths.get(pc)
        if state is None:return None
        path=[]
        while parents[state] is not None:
            previous,kind=parents[state];path.append({'source':previous[0],'target':state[0],'kind':kind});state=previous
        return list(reversed(path))
    return {'root':root,'nodes':nodes,'edges':edges,'frontiers':frontiers,'overlaps':overlaps,'witness':witness,'state_count':len(seen)}


def incoming_control_edges(rom,sites,target):
    out=[]
    for site in sites:
        for start in (site-1,site-2,site-14,site-18):
            ins,error=instruction(rom,start)
            if error or site not in ins['operand_offsets']:continue
            op=ins['opcode'];kind=None
            if op in (4,5,6,7) and site==ins['operand_offsets'][-1]:kind='explicit_script_transfer'
            if op==0x5C and ins['trainer_continuation']==target and site==ins['operand_offsets'][-1]:kind='trainer_continuation_pointer'
            if kind:out.append({'source_command':start,'pointer_site':site,'target':target,'kind':kind})
    # A byte sequence can have more than one interpretation; do not suppress ambiguity.
    return list({(e['source_command'],e['pointer_site']):e for e in out}.values())


def build(rom,audit,selected,incoming):
    targets=sorted(incoming);all_results=[];graphs={}
    def graph(root):
        if root not in graphs:graphs[root]=trace_graph(rom,root)
        return graphs[root]
    for anchor in selected['results']:
        roots={int(t['entry'],16):{'method':'prior_incoming_target_trace','entry_path':[]} for t in anchor['traces']}
        reverse=[];frontier=list(roots)
        for depth in range(2):
            following=[]
            for target in frontier:
                for edge in incoming_control_edges(rom,incoming.get(target,[]),target):
                    reverse.append(edge);command=edge['source_command']
                    candidates=targets[bisect.bisect_left(targets,max(0,command-512)):bisect.bisect_right(targets,command)]
                    for start in candidates:
                        g=graph(start);w=g['witness'](command)
                        if w is not None and not g['overlaps']:
                            if start not in roots:
                                roots[start]={'method':'incoming_target_with_format_path_to_transfer','entry_path':w,'links_to':target,'source_command':command}
                                following.append(start)
                            # Keep the earliest supported candidate for each transfer source.
                            break
            frontier=following
        instructions={};root_info=[];edges=[];frontiers=[];overlaps=[]
        for root,why in sorted(roots.items()):
            g=graph(root);instructions.update(g['nodes']);edges.extend(g['edges']);frontiers.extend(g['frontiers']);overlaps.extend(g['overlaps'])
            root_info.append({'offset':root,'method':why,'incoming_pointer_sites':incoming.get(root,[]),
              'witnesses_to_anchor_commands':{h:g['witness'](int(h,16)) for h in anchor['command_candidates']},
              'state_count':g['state_count']})
        messages={};rejected=[]
        for pc,ins in sorted(instructions.items()):
            for ref in ins['texts']:
                target=ref['target']
                if not 0<=target<len(rom):rejected.append({'command':pc,'target':target,'reason':'non-ROM text pointer'});continue
                text=parse(rom,target,strict_english=True)
                if not text or not text['terminated'] or text['issues']:
                    rejected.append({'command':pc,'target':target,'reason':'unsupported/incomplete English text'});continue
                entry=messages.setdefault(target,{'offset':target,'end':text['end'],'text':text['text'],'plain_text':text['plain'],
                   'empty_string':not bool(text['plain'].strip()),
                   'sha256':hashlib.sha256(rom[target:text['end']]).hexdigest(),'references':[],
                   'in_prior_keyword_corpus':any(int(e['offset'],16)<=target<int(e['end_offset_exclusive'],16) for e in audit['records'])})
                entry['references'].append({'command':pc,**ref})
        all_results.append({'anchor_text':anchor['text_offset'],'roots':root_info,
           'reverse_transfer_candidates':reverse,'instructions':list(instructions.values()),
           'edges':list({(e['source'],e['target'],e['kind']):e for e in edges}.values()),
           'frontiers':list({json.dumps(f,sort_keys=True):f for f in frontiers}.values()),
           'instruction_overlaps':overlaps,'messages':list(messages.values()),'rejected_text_targets':rejected,
           'reachability':'UNKNOWN; all paths are static format candidates, not execution proofs'})
    return all_results


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();incoming=index_pointers(rom)
    audit=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text())
    selected=json.loads((ROOT/'extracted/pointers/selected_text_traces.json').read_text())
    digest=hashlib.sha256(rom).hexdigest()
    if audit['summary']['source_sha256']!=digest or selected['source_sha256']!=digest:raise SystemExit('Stale source audit')
    results=build(rom,audit,selected,incoming)
    unique={m['offset']:m for cluster in results for m in cluster['messages']}
    summary={'clusters':len(results),'unique_messages':len(unique),
      'messages_absent_from_prior_keyword_corpus':sum(not m['in_prior_keyword_corpus'] for m in unique.values()),
      'instruction_overlap_count':sum(len(c['instruction_overlaps']) for c in results),
      'frontier_reasons':dict(Counter(f['reason'] for c in results for f in c['frontiers']))}
    data={'source_sha256':digest,'summary':summary,
      'limits':{'max_instructions_per_root':512,'max_states_per_root':2048,'max_call_depth':8,'reverse_rounds':2,'entry_lookback':512},
      'evidence':'CONFIRMED_IN_ROM byte ranges; FireRed-format interpretations STRONGLY_INFERRED; gameplay reachability UNKNOWN',
      'method':'Reverse raw pointer hits that match explicit branch/call or trainer continuation operands; seek incoming pointer targets within 512 bytes with a gapless static path to the source command. Follow direct conditional branches and stack-aware calls/returns. Callstd, native/special calls, waits, and trainer engine transfers are opaque/assumed paths. Unsupported instructions stop a path; physical proximity alone adds no messages.',
      'clusters':results}
    (ROOT/'extracted/text/dialogue_clusters.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    write_report(data)
    print(json.dumps(summary,indent=2))


def hx(value):return f'0x{value:X}'
def write_report(data):
    lines=['# Neighboring dialogue and entry-path audit','',
      f"Source SHA-256: `{data['source_sha256']}`.",'',
      'CONFIRMED_IN_ROM: byte/text presence. STRONGLY_INFERRED: interpretation using the pinned FireRed script formats. Static path does not prove gameplay reachability. No new story or ROM modifications.','',
      f"{data['summary']['unique_messages']} unique messages across five anchor clusters; {data['summary']['messages_absent_from_prior_keyword_corpus']} absent from the prior keyword corpus. These additions were found through script operands, not invented or assumed from nearby ROM bytes.",'',
      '## Method and limits','',data['method'],'',
      'Both branch outcomes are explored without solving flag/variable conditions. Opaque standard/native routines and battle outcomes are not emulated. Root pointer sites remain unclassified until map/native ownership is checked. Byte bounds, depth limits, unsupported instructions and overlaps are recorded in JSON. An unparsed frontier is not a broken event.','']
    for c in data['clusters']:
        lines += [f"## Anchor {c['anchor_text']}",'',f"{len(c['instructions'])} instruction candidates; {len(c['messages'])} referenced messages; {len(c['frontiers'])} frontiers; {len(c['instruction_overlaps'])} overlaps.",'', 'Candidate entries: '+', '.join(hx(x['offset']) for x in c['roots'])+'.','', '### Reverse transfer evidence','']
        for e in c['reverse_transfer_candidates']:lines.append(f"- {e['kind']}: {hx(e['source_command'])} operand {hx(e['pointer_site'])} → {hx(e['target'])}.")
        if not c['reverse_transfer_candidates']:lines.append('No explicit reverse transfer found within the selected scope; incoming root pointer remains unclassified.')
        lines += ['', '### Recovered messages','']
        for m in c['messages']:
            lines += [f"#### {hx(m['offset'])}"+(' — absent from prior keyword corpus' if not m['in_prior_keyword_corpus'] else ' — previously indexed'),'',
              'References: '+', '.join(f"{hx(ref['command'])} ({ref['role']})" for ref in m['references'])+'.','', '```text',m['text'],'```','']
        lines += ['### Stopped or opaque paths','']
        for f in c['frontiers']:lines.append(f"- {hx(f['pc'])}: {f['reason']}"+(f"; target {hx(f['target'])}" if 'target' in f else '')+'.')
        if not c['frontiers']:lines.append('No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.')
        lines.append('')
    lines += ['## Next bounded step','', 'Expand this entry-path and neighboring-message audit to the remaining Science Complex / Nexus machine dialogue anchors, including charging and shutdown messages. Map ownership and runtime reachability remain for subsequent archaeology.']
    (ROOT/'research/dialogue_cluster_audit.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
