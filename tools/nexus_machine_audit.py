"""Read-only Nexus machine and charging cluster audit; no execution claims."""
import bisect,hashlib,json
from pathlib import Path
from collections import Counter
from gba_text_codec import parse
from pointer_scan import index_pointers,classify_operand
from dialogue_cluster_audit import trace_graph,build,incoming_control_edges

ROOT=Path(__file__).resolve().parents[1]
ANCHORS={0xAA3280:'already charged',0xAA5FB1:'charging success',
 0xAD3B7E:'shutdown complete',0xAD3BB4:'shutdown override / intruder protection',
 0xAD3C54:'insert G Rank prompt',0xAD3D3D:'status display',
 0xB01831:'insufficient charge',0xA8EBF9:'Nexus One stable NPC',
 0xA8EC41:'machine self-destruction warning NPC'}

def select_entries(rom,incoming):
    targets=sorted(incoming);selected=[];probes=[];cache={}
    for text,label in ANCHORS.items():
        parsed=parse(rom,text,strict_english=True)
        if not parsed or not parsed['terminated']:raise ValueError(f'Anchor is not complete English text: {text:#x}')
        refs=[classify_operand(rom,site) for site in incoming.get(text,[])]
        commands=sorted({int(r['command_offset'],16) for r in refs if r['kind']=='MSGBOX_SHAPE'})
        if not commands:raise ValueError(f'No message-shaped reference for {text:#x}')
        roots={}
        for command in commands:
            candidates=targets[bisect.bisect_left(targets,max(0,command-512)):bisect.bisect_right(targets,command)]
            accepted=[];attempts=[]
            for start in candidates:
                if start not in cache:cache[start]=trace_graph(rom,start)
                g=cache[start];path=g['witness'](command)
                attempts.append({'entry':start,'command_found':path is not None,'overlaps':g['overlaps'],
                  'frontiers':g['frontiers']})
                if path is not None and not g['overlaps']:
                    accepted.append(start);roots[start]={'entry':hex(start)}
                    # Earliest supported incoming target in the bounded window.
                    break
            if not accepted:
                roots[command]={'entry':hex(command)}
            probes.append({'text':hex(text),'label':label,'command':hex(command),
                           'accepted_incoming_targets':accepted,'attempts':attempts,
                           'status':'INCOMING_TARGET_FORMAT_PATH' if accepted else 'UNROOTED_MESSAGE_COMMAND'})
        # Include all explicit callers of the shared insertion-prompt routine,
        # rather than only the earliest caller found by the local root search.
        if text==0xAD3C54:
            for edge in incoming_control_edges(rom,incoming.get(0xAD34DD,[]),0xAD34DD):
                source=edge['source_command']
                candidates=targets[bisect.bisect_left(targets,max(0,source-512)):bisect.bisect_right(targets,source)]
                for start in candidates:
                    if start not in cache:cache[start]=trace_graph(rom,start)
                    g=cache[start]
                    if g['witness'](source) is not None and g['witness'](commands[0]) is not None and not g['overlaps']:
                        roots[start]={'entry':hex(start)}
                        probes.append({'text':hex(text),'label':'shared prompt caller',
                          'command':hex(source),'accepted_incoming_targets':[start],
                          'pointer_site':edge['pointer_site'],'shared_routine':0xAD34DD,
                          'status':'INCOMING_TARGET_FORMAT_PATH'})
                        break
        selected.append({'text_offset':hex(text),'label':label,'command_candidates':[hex(c) for c in commands],
                         'traces':list(roots.values())})
    return {'results':selected},probes

def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();digest=hashlib.sha256(rom).hexdigest()
    prior=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text())
    if prior['summary']['source_sha256']!=digest:raise SystemExit('Stale keyword audit')
    incoming=index_pointers(rom);selected,probes=select_entries(rom,incoming)
    clusters=build(rom,prior,selected,incoming)
    unique={m['offset']:m for c in clusters for m in c['messages']}
    instructions={n['pc']:n for c in clusters for n in c['instructions']}
    state_ops=[n for n in instructions.values() if n['opcode'] in (0x16,0x17,0x18,0x19,0x1A,0x21,0x22,0x29,0x2A,0x2B,0x44,0x45,0x47,0xB6)]
    controllers=[]
    prompt_cluster=next(c for c in clusters if c['anchor_text']=='0xad3c54')
    for root in prompt_cluster['roots']:
        check=instructions.get(root['offset']+1)
        if check and check['opcode']==0x2B and 0x54B<=check['values'][0]<=0x554:
            flag=check['values'][0]
            write=instructions.get(root['offset']+0x21)
            controllers.append({'entry':root['offset'],'state_flag':flag,
              'flag_write_offset':write['pc'] if write and write['opcode']==0x29 and write['values']==[flag] else None,
              'incoming_pointer_sites':root['incoming_pointer_sites'],'map_owner':None,'reachability':'UNKNOWN'})
    summary={'anchors':len(ANCHORS),'unique_text_targets':len(unique),
      'nonempty_strings':sum(not m['empty_string'] for m in unique.values()),
      'empty_terminated_targets':sum(m['empty_string'] for m in unique.values()),
      'nonempty_strings_absent_from_prior_keyword_corpus':sum(not m['in_prior_keyword_corpus'] and not m['empty_string'] for m in unique.values()),
      'unique_instruction_candidates':len(instructions),'state_operand_instructions':len(state_ops),
      'unrooted_anchors':sum(p['status']=='UNROOTED_MESSAGE_COMMAND' for p in probes),
      'controller_scripts':len(controllers),
      'instruction_overlaps':sum(len(c['instruction_overlaps']) for c in clusters),
      'frontier_reasons':dict(Counter(f['reason'] for c in clusters for f in c['frontiers']))}
    signature_hits={}
    for op,name in [(0x29,'setflag'),(0x2A,'clearflag'),(0x2B,'checkflag')]:
        pattern=bytes([op,0x44,0x05]);offset=0;hits=[]
        while True:
            hit=rom.find(pattern,offset)
            if hit<0:break
            hits.append(hit);offset=hit+1
        signature_hits[name]=hits
    probe_path=ROOT/'extracted/pointers/engine_handler_probe.json'
    engine_probe=json.loads(probe_path.read_text())
    if engine_probe['source_sha256']['liquid_crystal']!=digest:raise SystemExit('Stale engine probe')
    used_opcodes={n['opcode'] for n in instructions.values()}
    modified=[c['opcode'] for c in engine_probe['handler_comparisons'] if c['opcode'] in used_opcodes and not c['compared_bytes_equal']]
    summary['used_opcodes_with_modified_handler_intervals']=modified
    data={'source_sha256':digest,'summary':summary,
      'method':'Nine observed messages selected from case-insensitive machine/charge/shutdown text scans. Incoming-target roots sought within 512 bytes; explicit predecessor transfers expanded for two rounds. Paths retain both conditional outcomes and opaque engine-return assumptions. No map/runtime reachability proof.',
      'entry_probes':probes,'state_operands':sorted(state_ops,key=lambda n:n['pc']),'clusters':clusters}
    data['flag_0544_literal_signatures']={'method':'All-ROM byte signatures only. A signature can occur in data; absence does not exclude native code, indirect flag IDs, or RAM scripts.',
                                        'hits':signature_hits}
    data['engine_probe']='extracted/pointers/engine_handler_probe.json; candidate table/code-byte comparison only; modified handler intervals are not treated as verified reference semantics'
    data['controller_scripts']=controllers
    (ROOT/'extracted/text/nexus_machine_audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    write_report(data)
    print(json.dumps(summary,indent=2))

def hx(x):return f'0x{x:X}'
def write_report(data):
    lines=['# Nexus machine / charging dialogue audit','',f"Source SHA-256: `{data['source_sha256']}`.",'',
      'CONFIRMED_IN_ROM: raw instruction and text bytes. STRONGLY_INFERRED: FireRed-format control/state interpretation. Gameplay reachability, active event ownership and native/standard effects remain UNKNOWN. No source ROM or save modified.','',
      '```json',json.dumps(data['summary'],indent=2),'```','',data['method'],'',
      'Each instruction/frontier/root witness is retained in extracted/text/nexus_machine_audit.json. Repeated messages across clusters are shared evidence, not additional copies of the scene. Unresolved parser paths are not automatically game bugs.','']
    for c in data['clusters']:
        lines += [f"## {c['anchor_text']} — {ANCHORS[int(c['anchor_text'],16)]}",'',
          'Candidate entries: '+', '.join(hx(r['offset']) for r in c['roots'])+'.','',
          f"{len(c['instructions'])} instruction candidates; {len(c['messages'])} referenced strings; {len(c['frontiers'])} unresolved frontiers.",'']
        for m in c['messages']:
            lines += [f"### {hx(m['offset'])}"+(' — absent from prior keyword corpus' if not m['in_prior_keyword_corpus'] else ''),'',
             'References: '+', '.join(hx(ref['command'])+' ('+ref['role']+')' for ref in m['references'])+'.','',
             '```text',m['text'],'```','']
        lines += ['### Frontiers','']
        for f in c['frontiers']:lines.append(hx(f['pc'])+': '+f['reason'])
        if not c['frontiers']:lines.append('No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.')
        lines.append('')
    lines += ['## Controller entries','', 'Map owners and gameplay reachability remain UNKNOWN.','',
      '| Entry | Per-controller flag | Write offset | Incoming pointer sites |','|---|---|---|---|']
    for c in data['controller_scripts']:lines.append('| '+hx(c['entry'])+' | '+hx(c['state_flag'])+' | '+(hx(c['flag_write_offset']) if c['flag_write_offset'] is not None else 'unresolved')+' | '+', '.join(hx(p) for p in c['incoming_pointer_sites'])+' |')
    lines += ['', '## State operand index','', 'Operands are not an allocation ledger and are not certified unused or mapped to save fields.','',
     '| Offset | Format interpretation | Operands |','|---|---|---|']
    for n in data['state_operands']:lines.append('| '+hx(n['pc'])+' | '+n['name']+' | '+', '.join(hx(v) for v in n['values'])+' |')
    lines += ['', '## Charge flag signature audit','', data['flag_0544_literal_signatures']['method'],'']
    for name,hits in data['flag_0544_literal_signatures']['hits'].items():lines.append(name+' 0x0544: '+(', '.join(hx(h) for h in hits) or 'no literal signature found')+'.')
    lines += ['', '## Engine comparison limitation','',data['engine_probe'],'',
      'Used opcode handler intervals differing from the reference: '+', '.join(hx(op) for op in data['summary']['used_opcodes_with_modified_handler_intervals'])+'. The wild-battle tuple remains an encoded-format observation; hooked native behavior is unresolved.']
    (ROOT/'research/nexus_machine_audit.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
