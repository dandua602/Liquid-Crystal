"""Read-only keyword/text-boundary/reference audit. No reachability claims."""
import bisect, hashlib, json, re
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
from gba_text_codec import encode,fold_case,parse,ENGLISH_GLYPHS
from pointer_scan import index_pointers,classify_operand

ROOT=Path(__file__).resolve().parents[1]
TERMS=['Orange','Mandarin','Valencia','Sandway','Safari','Route 59','Route 60',
 'Science Complex','Warehouse','Rudy','Danny','Zane','Mister Z','Nexus',
 'Commanding Rank','Champion','League','badge','island','ferry','gym','leader']
# Additional evidence-led discovery terms; these do not replace the requested seeds.
SUPPORT_TERMS=['Mister G','Ivy','GS Ball','Sea Ruby','toboggan']
SPECIFIC={'Orange','Mandarin','Valencia','Sandway','Route 59','Route 60',
 'Science Complex','Rudy','Danny','Zane','Mister Z','Nexus','Commanding Rank'}|set(SUPPORT_TERMS)
WINDOW=4096

def normalized(text):return re.sub(r'\s+',' ',text).strip()

def is_glyph_hit(parsed,offset,size):
    # Keyword bytes cannot be control-code arguments or placeholders.
    glyphs={t['offset'] for t in parsed['tokens'] if t['kind']=='glyph'}
    return all(x in glyphs for x in range(offset,offset+size))

def cluster_names(text):
    t=text.casefold();out=[]
    for name,terms in [
      ('Valencia / Oak / Ivy / GS Ball',('valencia','ivy','gs ball')),
      ('Mandarin / Rudy',('mandarin','rudy')),
      ('Science Complex / Team Nexus',('nexus','commanding rank','mister g','mister z','zane','science complex')),
      ('Sandway / Danny / Safari tests',('sandway','danny','sea ruby','toboggan'))]:
        if any(x in t for x in terms):out.append(name)
    return out or ['Other keyword context; relevance unresolved']

def run():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    folded=fold_case(rom);incoming=index_pointers(rom);targets=sorted(incoming)
    @lru_cache(maxsize=12000)
    def candidate(start):
        p=parse(rom,start,limit=8192,strict_english=True)
        return p if p and p['terminated'] and not p['issues'] else None
    reviewed=[]
    supplement=ROOT/'extracted/text/text_boundary_triage.json'
    if supplement.exists():
        triage=json.loads(supplement.read_text())
        if triage['source_sha256']!=hashlib.sha256(rom).hexdigest():raise ValueError('Stale reviewed text boundaries')
        for entry in triage['recovered_text']:
            start=int(entry['offset'],16);end=int(entry['end_offset_exclusive'],16)
            parsed=candidate(start)
            if not parsed or parsed['end']!=end or hashlib.sha256(rom[start:end]).hexdigest()!=entry['sha256']:
                raise ValueError('Reviewed complete text no longer matches source/decoder')
            reviewed.append(parsed)
    seeds=[];counts={}
    for term in TERMS+SUPPORT_TERMS:
        needle=fold_case(encode(term));offset=0;hits=0
        while True:
            hit=folded.find(needle,offset)
            if hit<0:break
            offset=hit+1;hits+=1;seeds.append((hit,len(needle),term))
        counts[term]=hits
    records={};unresolved=[];seed_boundaries=[]
    for hit,size,term in sorted(seeds):
        lo=max(0,hit-WINDOW)
        left=bisect.bisect_left(targets,lo);right=bisect.bisect_right(targets,hit)
        # Validated supplemental full-text candidates may precede accidental
        # interior raw pointer hits. They do not confer reference/reachability.
        options=[(p['start'],p,'REVIEWED_COMPLETE_TEXT') for p in reviewed
                 if p['start']<=hit and p['end']>hit+size and is_glyph_hit(p,hit,size)]
        if not options:
            for start in targets[left:right]:
                p=candidate(start)
                if p and p['end']>hit+size and is_glyph_hit(p,hit,size):options.append((start,p,'POINTER_TARGET'))
        if not options:
            previous=rom.rfind(b'\xff',lo,hit);start=previous+1 if previous>=lo else lo
            # Token-aware suffix heuristic: discard invalid prefix tokens, not a
            # fixed number of bytes before the keyword. Still explicitly provisional.
            raw=parse(rom,start,limit=hit-start+size)
            for t in raw['tokens']:
                if t['offset']>=hit:break
                if (t['kind']=='glyph' and rom[t['offset']] not in ENGLISH_GLYPHS):start=t['end']
            starts={start,previous+1} if previous>=lo else {start}
            # A COLOR-prefixed dialogue may follow data with a misleading FF.
            color=rom.rfind(b'\xfc\x01',lo,hit)
            if color>=lo:starts.add(color)
            for start in sorted(starts):
                p=candidate(start)
                if p and p['end']>hit+size and is_glyph_hit(p,hit,size):options.append((start,p,'INFERRED_SUFFIX'))
        if not options:
            unresolved.append({'term':term,'offset':hex(hit),'reason':'No complete strict-English candidate containing keyword as glyphs; may be binary, unsupported encoding/control, or outside window.'});continue
        start,p,method=min(options,key=lambda x:x[0])
        # Merge overlapping suffix candidates with the same EOS; retain earliest
        # independently acceptable start and record all seed-level choices.
        end=p['end'];entry=records.get(end)
        if entry is None or start<entry['start']:
            entry={'start':start,'parsed':p,'method':method,'hits':entry['hits'] if entry else []}
            records[end]=entry
        entry['hits'].append({'term':term,'offset':hex(hit),'search':'case-insensitive Gen III letter bytes'})
        seed_boundaries.append({'term':term,'hit_offset':hex(hit),'selected_start':hex(start),'method':method})
    output=[]
    for end,entry in sorted(records.items(),key=lambda pair:pair[1]['start']):
        p=entry['parsed'];start=p['start'];refs=[];inside=[]
        for target in targets[bisect.bisect_left(targets,start):bisect.bisect_left(targets,end-1)]:
            token=next((t for t in p['tokens'] if t['offset']<=target<t['end']),None)
            for site in incoming[target]:
                ref=classify_operand(rom,site);ref.update(target=hex(target),interior=target!=start,
                    target_at_token_start=bool(token and token['offset']==target))
                if target==start:refs.append(ref)
                else:inside.append(ref)
        typed=[r for r in refs+inside if r['kind']!='RAW_POINTER' and r['target_at_token_start']]
        terms={x['term'] for x in entry['hits']};plain=normalized(p['plain']);specific=bool(terms&SPECIFIC)
        if 'orange mail' in plain.casefold() and not ((terms&SPECIFIC)-{'Orange'}):relevance='NON_STORY_ORANGE_MAIL'
        elif 'Orange Islands Trainer Battle' in plain:relevance='CREDITS'
        elif 'ivysaur' in plain.casefold() and not ((terms&SPECIFIC)-{'Ivy'}):relevance='NON_STORY_SPECIES_NAME'
        elif specific:relevance='ORANGE_SPECIFIC_SEED'
        else:relevance='BROAD_CONTEXT_NOT_ASSUMED_ORANGE'
        output.append({'offset':hex(start),'end_offset_exclusive':hex(end),'length_bytes':end-start,
          'sha256':hashlib.sha256(rom[start:end]).hexdigest(),'boundary_method':entry['method'],
          'boundary_confidence':'REFERENCED_PARSEABLE_START' if refs else 'PROVISIONAL_SUFFIX',
          'evidence':'CONFIRMED_IN_ROM','interpretation':'Control and operand semantics use pinned FireRed reference; LC runtime not tested.',
          'text':p['text'],'plain_text':p['plain'],'keyword_hits':entry['hits'],'tokens':p['tokens'],
          'references':refs,'interior_references':inside,'typed_reference_count':len(typed),
          'reference_status':'SCRIPT_OPERAND_SHAPE' if typed else ('RAW_POINTER_ONLY' if refs or inside else 'NO_ABSOLUTE_POINTER_FOUND'),
          'reachability':'UNKNOWN','likely_clusters':cluster_names(plain),'relevance':relevance})
    groups=defaultdict(list)
    for e in output:groups[normalized(e['plain_text'])].append(e['offset'])
    duplicates=[{'offsets':v,'normalized_plain_text':k,'comparison':'exact after removing controls and collapsing whitespace; raw bytes can differ'} for k,v in groups.items() if len(v)>1 and len(k)>60]
    summary={'source_sha256':hashlib.sha256(rom).hexdigest(),'search_window_bytes':WINDOW,
      'requested_terms':TERMS,'support_terms':SUPPORT_TERMS,'raw_seed_counts':counts,
      'raw_keyword_hits':len(seeds),'accepted_keyword_hits':sum(len(e['keyword_hits']) for e in output),
      'unresolved_keyword_hits':len(unresolved),'text_blocks':len(output),
      'specific_blocks':sum(e['relevance']=='ORANGE_SPECIFIC_SEED' for e in output),
      'reference_status_counts':dict(Counter(e['reference_status'] for e in output)),
      'normalized_duplicate_groups':len(duplicates),
      'scope':'Uncompressed Gen III English byte strings; not all possible LC dialogue or scripts.'}
    audit={'summary':summary,'records':output,'duplicate_groups':duplicates,'unresolved_hits':unresolved,'seed_boundary_choices':seed_boundaries}
    (ROOT/'extracted/text/orange_text_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    write_report(audit)
    print(json.dumps(summary,indent=2))
    return audit

def write_report(audit):
    summary=audit['summary'];entries=audit['records'];selected=[e for e in entries if e['relevance']=='ORANGE_SPECIFIC_SEED']
    lines=['# Orange text index — boundary and reference audit','',
      f"Source SHA-256: `{summary['source_sha256']}`. Supersedes the initial keyword-only report; counts differ because searches now ignore case, suffix duplicates are merged, and boundaries use pointer targets/control parsing.",'',
      f"{summary['raw_keyword_hits']} keyword hits → {summary['text_blocks']} accepted blocks; {len(selected)} specific research-seed blocks; {summary['unresolved_keyword_hits']} unresolved hits. Supporting terms are separately listed in JSON.",'',
      '## Evidence rules','',
      'CONFIRMED_IN_ROM labels byte/text presence only. FireRed character/control and operand formats are pinned in references/manifest.json; their semantic interpretation in LC is STRONGLY_INFERRED until engine/runtime validation. All offsets are ROM file offsets; pointers use little-endian 0x08000000 + offset. Every byte alignment was searched. A script operand shape does not establish a map owner, valid entry path, execution, or reachability. No pointer found is not proof of unused content. No scene has been newly authored.','',
      'The decoder consumes FC control arguments, FD placeholders and F7 dynamic indices; FF is EOS only outside parameters. Dynamic expansion is not simulated. Unknown controls reject strict candidates and remain unresolved. Case-folding changes only letter bytes, and keyword bytes must map to glyph tokens. Complete text boundaries from the reviewed triage supplement take priority over accidental interior pointer starts; otherwise pointer-backed boundaries take priority. Fallback/readable suffixes without exact references remain provisional. A 4096-byte backward search and 8192-byte parse bound mean long/encoded/compressed content can be missed. Interior pointers are retained separately.','',
      '## Provisional event clusters','',
      'These are topic groups, not a proven chronological progression. A Zane, Ivy, or other proper-name hit alone does not identify an Orange Islands event; some matches belong to earlier game content. Order below follows entry/places/event subjects; scripts must determine actual ordering.']
    clusters=defaultdict(list)
    for e in selected:
        for cluster in e['likely_clusters']:clusters[cluster].append(e)
    for name,items in clusters.items():
        lines += ['',f'### {name} — STRONGLY_INFERRED grouping','',f"{len(items)} candidate blocks: "+', '.join(e['offset'] for e in items)+'.']
    lines += ['', '## Specific-seed text and references','']
    for e in selected:
        lines += [f"### {e['offset']} — {', '.join(sorted({h['term'] for h in e['keyword_hits']}))}",'',
          f"CONFIRMED_IN_ROM: bytes through {e['end_offset_exclusive']} (exclusive). Boundary: {e['boundary_confidence']}. References: {e['reference_status']}. Map/event owner and reachability UNKNOWN.",'']
        for ref in e['references']+e['interior_references']:
            if ref['kind']=='RAW_POINTER':continue
            lines += [f"- {ref['kind']} at operand {ref['offset']}; command candidate {ref.get('command_offset')}; target {ref['target']}"+(' (interior target).' if ref['interior'] else '.')]
        raw=[r['offset'] for r in e['references']+e['interior_references'] if r['kind']=='RAW_POINTER']
        if raw:lines += ['- Raw/unclassified pointer sites: '+', '.join(raw)+'.']
        if not e['references'] and not e['interior_references']:lines += ['No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.']
        lines += ['', '```text',e['text'],'```','']
    lines += ['## No-absolute-pointer candidates (not certified orphaned)','']
    for e in selected:
        if e['reference_status']=='NO_ABSOLUTE_POINTER_FOUND':lines += [f"- {e['offset']}: {normalized(e['plain_text'])[:140]}"]
    lines += ['', '## Duplicate text candidates','']
    for g in audit['duplicate_groups']:lines += ['- '+', '.join(g['offsets'])+': '+g['normalized_plain_text'][:100]]
    lines += ['', 'Exact normalized equality does not establish which copy is active. Similar but edited versions are not merged.','',
      '## Scope still open','',
      'Generic gym/league/island text remains in JSON without assuming Orange relevance. Orange Mail, Ivysaur substring matches, and credits are separated. Neighboring dialogue without keywords, indirect/computed references, native text consumers, custom controls, map ownership, chronology, and orphan/unused classification still need follow-up. Step 2 is not complete.','',
      '## Next bounded step','',
      'Expand the specific text-reference clusters to adjacent non-keyword messages and validate their script entry paths; keep all reachability claims open until map/script archaeology.']
    (ROOT/'research/orange_text_index.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':run()
