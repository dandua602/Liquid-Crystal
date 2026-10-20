"""Orange entry and transport owners, conditions, messages and script limits."""
import hashlib
import json
from pathlib import Path
from dialogue_cluster_audit import trace_graph
from gba_text_codec import parse
from orange_progression_audit import decoder
from script_extract import catalogue
from warp_graph import MapCatalog
ROOT=Path(__file__).resolve().parents[1]
MAPS=[(4,88),(2,123),(1,4),(3,40),(2,121),(2,124),(2,125),(2,126),(1,53),(3,77)]


def build(rom):
    digest=hashlib.sha256(rom).hexdigest();catalog=MapCatalog(rom);maps=[catalog.resolve(*key)for key in MAPS]
    data=catalogue(rom,{'source_sha256':digest,'maps':maps},focus_maps={m['id']for m in maps},scope='Ten Orange authorization, ticket, gate, train and arrival map slots. Exact IDs retained; labels may be inherited.')
    traces=[];messages={};all_nodes=set()
    for row in data['roots']:
        graph=trace_graph(rom,row['offset'],max_instructions=1024,max_states=4096,max_depth=12,decoder=decoder);all_nodes.update(graph['nodes'])
        for n in graph['nodes'].values():
            for ref in n['texts']:
                target=ref['target'];p=parse(rom,target,limit=4096,strict_english=True)if 0<=target<len(rom)else None
                if p and p['terminated']and not p['issues']:
                    m=messages.setdefault(target,{'offset':target,'end':p['end'],'text':p['text'],'roots':[]})
                    if row['offset']not in m['roots']:m['roots'].append(row['offset'])
        traces.append({'root':row['offset'],'owners':row['associations'],'instructions':list(sorted(graph['nodes'].values(),key=lambda n:n['pc'])),'frontiers':graph['frontiers'],'overlaps':graph['overlaps']})
    return {'source_sha256':digest,'scope':data['scope'],'catalogue':data,'maps_with_links':maps,'traces':traces,'messages':list(sorted(messages.values(),key=lambda m:m['offset'])),
            'summary':{'maps':len(maps),'roots':len(traces),'unique_instruction_candidates':len(all_nodes),'messages':len(messages),'roots_with_frontiers':sum(bool(t['frontiers'])for t in traces)},
            'limits':'Static conditions unresolved, standard calls followed, special/native/UI/battle transfers remain assumptions. Candidate format paths are not normal gameplay proof; runtime observations are separate. No ROM/state changes.'}


def main():
    result=build((ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes());out=ROOT/'extracted/scripts/entry_audit.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],indent=2))


if __name__=='__main__':main()
