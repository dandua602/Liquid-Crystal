"""Discover NOP-prefix handler-table candidates independently in both ROMs.
Byte equality supports opcode formats, not equivalence of callees/runtime state.
"""
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=0x08000000;COUNT=0xD5

def discover(rom):
    candidates=[];start=0
    while True:
        at=rom.find(b'\x00\x20\x70\x47\x00\x20\x70\x47',start)
        if at<0:break
        # Two adjacent Thumb functions: movs r0,#0; bx lr (NOP handlers).
        needle=struct.pack('<II',BASE+at+1,BASE+at+5);pos=0
        while True:
            table=rom.find(needle,pos)
            if table<0:break
            pos=table+1
            if table+COUNT*4>len(rom):continue
            entries=struct.unpack_from('<'+'I'*COUNT,rom,table)
            if sum(bool(v&1) and BASE<v<BASE+len(rom) for v in entries[:104])<100:continue
            candidates.append({'table':table,'nop_code':at,'entries':entries})
        start=at+2
    for candidate in candidates:
        candidate['contained_in_other_candidate']=any(other['table']<candidate['table']<other['table']+COUNT*4 for other in candidates)
    return candidates

def make_probe(fr,lc,opcodes):
    discovery={};chosen={}
    for key,rom in [('firered',fr),('liquid_crystal',lc)]:
        candidates=discover(rom)
        discovery[key]=[{k:v for k,v in c.items() if k!='entries'} for c in candidates]
        outer=[c for c in candidates if not c['contained_in_other_candidate']]
        if len(outer)!=1:raise ValueError(f'{key}: ambiguous handler-table candidates')
        chosen[key]=outer[0]
    results=[]
    for op in sorted(opcodes):
        row={'opcode':op};chunks=[]
        for key,rom in [('firered',fr),('liquid_crystal',lc)]:
            c=chosen[key];pointer=c['entries'][op];offset=(pointer&~1)-BASE
            if not 0<=offset<len(rom):raise ValueError('Invalid code pointer')
            next_code=min(((p&~1)-BASE for p in c['entries'] if (p&~1)-BASE>offset),default=min(len(rom),offset+128))
            end=min(next_code,offset+256,len(rom));data=rom[offset:end];chunks.append(data)
            row[key]={'pointer':hex(pointer),'file_offset':hex(offset),'end_exclusive':hex(end),
                      'sha256':hashlib.sha256(data).hexdigest(),'length_bytes':len(data)}
        row['compared_bytes_equal']=chunks[0]==chunks[1];results.append(row)
    return {'method':'Independent adjacent-NOP code search and little-endian handler-prefix references. Contained candidates are treated as interior positions, not separate tables. Compared code intervals stop at next known handler or 256 bytes. This does not verify dispatcher use, complete function boundaries, helper/native callees, or runtime state.',
      'discovery':discovery,'selected_tables':{k:hex(v['table']) for k,v in chosen.items()},
      'source_sha256':{'firered':hashlib.sha256(fr).hexdigest(),'liquid_crystal':hashlib.sha256(lc).hexdigest()},'handler_comparisons':results}

if __name__=='__main__':
    from dialogue_cluster_audit import SPECS
    fr=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    lc=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    data=make_probe(fr,lc,set(SPECS)|{0x5C})
    (ROOT/'extracted/pointers/engine_handler_probe.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'selected_tables':data['selected_tables'],'compared_handlers':len(data['handler_comparisons']),
      'equal_intervals':sum(x['compared_bytes_equal'] for x in data['handler_comparisons'])},indent=2))
