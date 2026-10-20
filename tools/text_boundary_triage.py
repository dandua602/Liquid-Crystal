"""Reproducible, reviewed triage of the 53 historical keyword misses.

Classifications describe byte/format evidence, never gameplay reachability.
The frozen input predates dynamic-token support and is not another ROM version.
"""
import hashlib,json,struct
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
from gba_text_codec import ENGLISH_GLYPHS,encode,fold_case,parse
from pointer_scan import index_pointers,classify_operand
from text_extract import is_glyph_hit
ROOT=Path(__file__).resolve().parents[1]
# Reviewed contexts with clear prose followed by non-text/unsupported bytes.
# Boundaries below are probes, not proposed patch addresses or proof of use.
PARTIAL_CONTEXTS={
 0x73D9D9:0x73D98D,0x73D9DD:0x73D98D,
 0x86AB9A:0x86AA8F,0x86ABF2:0x86AA8F,0x86AC0D:0x86AA8F,0x86AC49:0x86AA8F,
 0x86CFDB:0x86CFAB,0x8ABFE8:0x8ABFCF,0x8D851B:0x8D84F4,
 0xAAAF45:0xAAAF41,0xAAAF65:0xAAAF41,0xAAAF92:0xAAAF41}
BINARY_HITS={0x4ACAF1,0x4CBF61,0x4D0874,0x4D720B,0x4FC4F2,0x51EAEF,0x61B982,0xD4F544}
DYNAMIC_HITS={0x41A304,0x41AF17,0x41AF1B,0x41B3FF}
FULL_TEXT_HITS={0x905C1F,0x9698C9,0x9698DE,0x9698E7,0x969903,0x96990A,0xAAA9F3}

def analyze(rom,frozen):
    digest=hashlib.sha256(rom).hexdigest()
    if frozen['source_sha256']!=digest:raise ValueError('Triage input is for a different source ROM')
    incoming=index_pointers(rom);rows=[];recovered={};partial={};repeat_groups=defaultdict(list)
    @lru_cache(maxsize=12000)
    def strict(start):
        p=parse(rom,start,strict_english=True)
        return p if p and p['terminated'] and not p['issues'] else None
    for hit in frozen['unresolved_hits']:
        at=int(hit['offset'],16);term=hit['term'];size=len(encode(term))
        if fold_case(rom[at:at+size])!=fold_case(encode(term)):raise ValueError('Stale keyword offset')
        context=rom[max(0,at-45):at+90]
        row={'term':term,'offset':hex(at),'context_offset':hex(max(0,at-45)),
             'context_hex':context.hex(' '),'context_sha256':hashlib.sha256(context).hexdigest(),
             'evidence':'CONFIRMED_IN_ROM','reachability':'UNKNOWN'}
        if at in DYNAMIC_HITS or at in FULL_TEXT_HITS:
            # Dynamic cases have an exact incoming target. The other reviewed
            # cases need a whole readable suffix rather than an accidental
            # interior pointer; keep the inferred boundary explicitly provisional.
            starts=sorted(p for p in incoming if at-4096<=p<=at) if at in DYNAMIC_HITS else range(max(0,at-1200),at+1)
            choices=[]
            for start in starts:
                p=strict(start)
                if p and p['end']>at+size and is_glyph_hit(p,at,size):choices.append((start,p))
            if not choices:raise ValueError(f'Reviewed recovery no longer parses: {at:#x}')
            start,p=choices[0];padding=0
            if at in FULL_TEXT_HITS:
                while start<at and rom[start]==0:start+=1;padding+=1
                p=strict(start)
            record=recovered.setdefault(start,{'offset':hex(start),'end_offset_exclusive':hex(p['end']),
                'text':p['text'],'plain_text':p['plain'],'sha256':hashlib.sha256(rom[start:p['end']]).hexdigest(),
                'tokens':p['tokens'],'keyword_hits':[],'leading_zero_bytes_excluded':padding,
                'exact_pointer_sites':[classify_operand(rom,s) for s in incoming.get(start,[])],
                'boundary_confidence':'REFERENCED_DYNAMIC_TEMPLATE' if at in DYNAMIC_HITS else 'PROVISIONAL_READABLE_SUFFIX',
                'reachability':'UNKNOWN'})
            record['keyword_hits'].append({'term':term,'offset':hex(at)})
            row.update(classification='RECOVERED_DYNAMIC_TEMPLATE' if at in DYNAMIC_HITS else 'RECOVERED_PROVISIONAL_TEXT',recovered_start=hex(start))
        elif at in PARTIAL_CONTEXTS:
            start=PARTIAL_CONTEXTS[at]
            p=parse(rom,start)
            failures=[t for t in p['tokens'] if t['kind']=='glyph' and rom[t['offset']] not in ENGLISH_GLYPHS]
            first=failures[0] if failures else None
            boundary=first['offset'] if first else p['end']-1
            entry=partial.setdefault(start,{'offset':hex(start),'permissive_end':hex(p['end']),
                'strict_parse_accepted':strict(start) is not None,'first_unvalidated_glyph':hex(boundary) if first else None,
                'prefix_text':''.join(t['text'] for t in p['tokens'] if t['end']<=boundary),
                'permissive_issues':p['issues'],'keyword_hits':[],
                'exact_pointer_sites':[classify_operand(rom,s) for s in incoming.get(start,[])],
                'interpretation':'Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.'})
            entry['keyword_hits'].append({'term':term,'offset':hex(at)})
            row.update(classification='PROSE_BOUNDARY_ANOMALY',context_start=hex(start),
                       first_unvalidated_glyph=entry['first_unvalidated_glyph'])
        elif at in BINARY_HITS:
            row.update(classification='BINARY_CONTEXT_SUBSTRING_CANDIDATE',
                interpretation='Reviewed mixed-case keyword substring amid non-prose/unsupported bytes. No claim of asset type or proof that hidden/compressed text is absent.')
        elif term=='Ivy' and any(at==0x7AA000+n*0x3000+delta for n in range(11) for delta in (0x2F,0x247)):
            row.update(classification='REPEATED_BINARY_WINDOW_CANDIDATE',
                interpretation='Exact repeated context, with Ivy inside a mixed-case glyph run; not classified as missing dialogue.')
            repeat_groups[row['context_sha256']].append(hex(at))
        else:raise ValueError(f'Unreviewed hit {term} at {at:#x}; review rather than guessing')
        rows.append(row)
    rank=partial[0xAAAF41]
    rank.update(description_prose_end_exclusive='0xaaaf9a',prose_length_bytes=89,
        description_prose_sha256=hashlib.sha256(rom[0xAAAF41:0xAAAF9A]).hexdigest(),
        eos_before_script=False,first_raw_ff='0xaaaf9b',following_script_bytes=rom[0xAAAF9A:0xAAAFA4].hex(' '),
        interpretation='89-byte readable item description has no FF before applymovement script at 0xAAAF9A; raw FF at 0xAAAF9B is the local-object operand. Native accessor evidence is in research/rank_description_investigation.md. No runtime appearance asserted.')
    rank['item_records']=[]
    for base in (0x3DB028,0x9990AC):
        record=base+44*0x114
        rank['item_records'].append({'base':hex(base),'index':'0x114','record_start':hex(record),
          'name':parse(rom,record,limit=14,strict_english=True)['plain'],
          'stored_id':struct.unpack_from('<H',rom,record+14)[0],
          'description_pointer_site':hex(record+20),'description_pointer':hex(struct.unpack_from('<I',rom,record+20)[0])})
    rank['native_description_accessor']={'offset':'0x9a96c','length_bytes':36,
      'sha256':hashlib.sha256(rom[0x9A96C:0x9A990]).hexdigest(),
      'table_literal_site':'0x9a98c','table_literal':hex(struct.unpack_from('<I',rom,0x9A98C)[0]),
      'name_table_literal_site':'0x9a8d8','name_table_literal':hex(struct.unpack_from('<I',rom,0x9A8D8)[0])}
    if b'\xff' in rom[0xAAAF41:0xAAAF9A] or rom[0xAAAF9A:0xAAAF9D]!=b'\x4f\xff\x00':raise ValueError('Rank boundary bytes changed')
    return {'source_sha256':digest,'original_corpus_sha256':frozen['original_corpus_sha256'],
      'summary':{'historical_hits':len(rows),'classifications':dict(Counter(r['classification'] for r in rows)),
                 'recovered_text_blocks':len(recovered),'partial_prose_contexts':len(partial),
                 'repeated_context_groups':len(repeat_groups),'unused_or_unreachable_certifications':0},
      'method':'Finite reviewed partition of the 53 frozen misses. Recovery requires complete strict-English tokens, EOS, and keyword bytes at glyph positions. Binary-context labels remain conservative. Pointer absence and raw byte repetition do not prove unused data. All original hits remain represented.',
      'hits':rows,'recovered_text':list(recovered.values()),'partial_contexts':list(partial.values()),
      'repeated_windows':[{'sha256':k,'hit_offsets':v} for k,v in repeat_groups.items()]}

def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    frozen=json.loads((ROOT/'extracted/text/text_triage_input.json').read_text());data=analyze(rom,frozen)
    (ROOT/'extracted/text/text_boundary_triage.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# Historical text-miss triage','',f"Source SHA-256: `{data['source_sha256']}`.",'',data['method'],'',
      '```json',json.dumps(data['summary'],indent=2),'```','', '## Recovered templates and readable suffixes','']
    for e in data['recovered_text']:
        lines += [f"### {e['offset']} — {e['boundary_confidence']}",'',
          'Exact pointer sites: '+(', '.join(p['offset'] for p in e['exact_pointer_sites']) or 'none found')+'.',
          'Gameplay reachability UNKNOWN.','', '```text',e['text'],'```','']
    lines += ['## Prose boundary anomalies','']
    for e in data['partial_contexts']:
        lines += [f"### {e['offset']}",'',e['interpretation'],'',
          f"First unvalidated glyph: {e['first_unvalidated_glyph']}. Strict full-string acceptance: {e['strict_parse_accepted']}.",'',
          '```text',e['prefix_text'],'```','']
    lines += ['## Complete hit partition','', '| Hit | Term | Classification |','|---|---|---|']
    for e in data['hits']:lines.append(f"| {e['offset']} | {e['term']} | {e['classification']} |")
    lines += ['', 'No row certifies unused, unreachable, placeholder or broken gameplay. Full strings, partial prose and binary-context matches remain distinct.']
    (ROOT/'research/text_boundary_triage.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(data['summary'],indent=2))
if __name__=='__main__':main()
