"""Read-only baseline inspection; Python standard library only."""
import argparse, hashlib, json, struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILES = {'liquid_crystal': ROOT/'roms/POKEMON Liquid Crystal.gba', 'firered': ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba', 'save': ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'}
# FireRed section checksum lengths, indexed by section ID.
LENGTHS = [0xF24] + [0xF80]*3 + [0xEE8] + [0xF80]*8 + [0x7D0]
def checksum(data):
    total = sum(struct.unpack('<'+'I'*(len(data)//4), data)) & 0xffffffff
    return ((total >> 16) + (total & 0xffff)) & 0xffff

def inspect():
    blobs = {k:p.read_bytes() for k,p in FILES.items()}
    hashes = {k:{'filename':FILES[k].name,'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for k,b in blobs.items()}
    headers = {}
    for k in ('liquid_crystal','firered'):
        b=blobs[k]
        headers[k]={'title':b[0xA0:0xAC].decode('ascii','replace').rstrip('\0'),'game_code':b[0xAC:0xB0].decode('ascii','replace'),'maker_code':b[0xB0:0xB2].decode('ascii','replace'),'revision':b[0xBC], 'fixed_value':b[0xB2], 'header_checksum':b[0xBD], 'computed_header_checksum':(-sum(b[0xA0:0xBD])-0x19)&255}
        headers[k]['header_checksum_valid']=headers[k]['header_checksum']==headers[k]['computed_header_checksum']
    lc,fr=blobs['liquid_crystal'],blobs['firered']
    differing=sum(a!=b for a,b in zip(lc,fr))+abs(len(lc)-len(fr))
    diff={'different_bytes':differing,'percent_of_larger_rom':100*differing/max(len(lc),len(fr))}
    s=blobs['save']; slots=[]
    for slot in range(2):
        sections=[]
        for n in range(14):
            off=(slot*14+n)*0x1000
            sid,stored,signature,generation=struct.unpack_from('<HHII',s,off+0xFF4)
            calc=checksum(s[off:off+LENGTHS[sid]]) if sid<len(LENGTHS) else None
            matches=[length for length in range(4,0xFF5,4) if checksum(s[off:off+length])==stored]
            sections.append({'matching_checksum_lengths':[hex(x) for x in matches], 'offset':hex(off),'section_id':sid,'checksum':stored,'computed_checksum':calc,'standard_firered_checksum_valid':stored==calc,'signature':hex(signature),'generation':generation})
        slots.append({'slot':slot,'sections':sections,'complete_ids':sorted(x['section_id'] for x in sections)==list(range(14)), 'standard_firered_checksums_valid':all(x['standard_firered_checksum_valid'] for x in sections), 'all_sections_have_candidate_checksum_length':all(x['matching_checksum_lengths'] for x in sections), 'generations':sorted(set(x['generation'] for x in sections))})
    save={'size_bytes':len(s),'flash_region_bytes':min(len(s),0x20000),'footer_hex':s[0x20000:].hex(),'footer_length':len(s[0x20000:]),'footer_interpretation':'16-byte trailer consistent with supplied FlashGBX provenance; signature not independently authenticated','slots':slots}
    return hashes,headers,save,diff

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-baseline',action='store_true');args=ap.parse_args()
    hashes,headers,save,diff=inspect()
    from gba_text_codec import encode, decode
    rom=FILES['liquid_crystal'].read_bytes()
    needle=encode('Current Build Number: 3.3.00512')
    offset=rom.find(needle)
    if offset < 0: raise SystemExit('Expected LC build text not found')
    if not all(h['header_checksum_valid'] for h in headers.values()): raise SystemExit('Invalid GBA header checksum')
    print('LC build text verified at', hex(offset))
    target=ROOT/'baselines/hashes.json'
    if target.exists():
        previous=json.loads(target.read_text())
        changed=[k for k in hashes if previous.get(k)!=hashes[k]]
        print('Baseline comparison:', 'CHANGED '+','.join(changed) if changed else 'unchanged')
        if changed: raise SystemExit('Source hashes changed; preserve and review new snapshot before proceeding.')
    else: print('First snapshot: no previous hashes available for comparison.')
    if args.write_baseline:
        for name,obj in [('hashes',hashes),('rom_headers',headers),('save_metadata',save),('rom_diff',diff)]:
            (ROOT/'baselines'/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'hashes':hashes,'headers':headers,'diff':diff,'slots':[{k:v for k,v in slot.items() if k!='sections'} for slot in save['slots']],'footer_hex':save['footer_hex']},indent=2))
if __name__=='__main__':main()
