"""Read-only native state and bounded space screen; never allocates or patches.

Raw words include all GBA ROM wait-state aliases and byte alignments. Absence
of these shapes cannot exclude computed addresses, extents or native owners.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
from trainer_audit import discover

ROOT=Path(__file__).resolve().parents[1]
PROTECTED=((0xC72100,0xC72EA8),(0xC80000,0xCA0000))
NATIVE={
    0x6C30C:'10b5041cfdf7f2fa00000000000000000000000014f080f8a070002010bc02bc0847',
    0x6C330:'00b5fdf7e1fa014908470000252d2408',
    0x6C34C:'00b5fdf7d3fa0149084700003d2d2408',
    0x803E4:'00b5fff767fe0149084700000d2d2408',
    0x803FC:'00b5fff75bfe014908470000252d2408',
    0x80424:'00b50149084700000d2d2408',
    0x242CA8:'10b50004040c201c251c261c002c24d02304dc0c1b0c07200340802040049840060e002904d001290cd0022910d014e00b48001900783040002801d101200ce000200ae0064909190a7832430a7004e0034909190a78b2430a7010bc02bc084700d00302',
    0x242D0C:'0021fcb400f003f8fcbc02bc0847014d2847c046a92c2408',
    0x242D24:'0221fcb400f003f8fcbc01bc0047014d2847c046a92c2408',
    0x242D3C:'0121fcb400f003f8fcbc01bc0047014d2847c046a92c2408',
}


def native_evidence(rom):
    for opcode,target in ((0x60,0x806C30D),(0x61,0x806C331),(0x62,0x806C34D)):
        if struct.unpack_from('<I',rom,0x15F9B4+4*opcode)[0]!=target:
            raise ValueError('Unexpected trainer-state command table')
    rows=[]
    for start,expected in NATIVE.items():
        data=bytes.fromhex(expected)
        if rom[start:start+len(data)]!=data:raise ValueError(f'Native trainer-state identity mismatch at {start:X}')
        rows.append({'start':start,'end_exclusive':start+len(data),'raw_hex':expected})
    return rows


def mirrored_target(word,size):
    if size<=0 or size>0x2000000 or size&(size-1):raise ValueError('Require power-of-two GBA ROM size')
    if not 0x08000000<=word<0x0E000000:return None
    # A conservative address-shape normalization, not proof of a live read.
    # In particular this image overrides 09000000 with its SRAM bank port.
    return (word-0x08000000)&(size-1)


def mirror_index(rom):
    incoming={}
    for site in range(len(rom)-3):
        if not 8<=rom[site+3]<=13:continue
        word=struct.unpack_from('<I',rom,site)[0]
        target=mirrored_target(word,len(rom))
        incoming.setdefault(target,[]).append({'site':site,'word':word})
    return incoming


def guarded_windows(rom,incoming,minimum=4096,guard=256):
    """Screen FF spans against raw targets, guards and protected hardware data."""
    if minimum<=0 or guard<0:raise ValueError('Invalid screen budget')
    result=[];targets=sorted(incoming)
    import bisect
    for match in re.finditer(b'\xff{'+str(minimum).encode()+b',}',rom):
        start,end=match.span();cursor=start+guard
        lo=bisect.bisect_left(targets,start-guard)
        hi=bisect.bisect_left(targets,end+guard)
        blocked=[(t-guard,t+guard+1)for t in targets[lo:hi]]
        blocked += [(a-guard,b+guard)for a,b in PROTECTED if a<end+guard and b>start-guard]
        for a,b in sorted(blocked)+[(end-guard,end)]:
            aligned=(cursor+3)&~3
            if a-aligned>=minimum:
                result.append({'start':aligned,'end_exclusive':a,'bytes':a-aligned,'ff_span':[start,end],
                               'guard_bytes':guard,'allocated_bytes':0})
            cursor=max(cursor,b)
    return sorted(result,key=lambda r:r['bytes'],reverse=True)


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();digest=hashlib.sha256(rom).hexdigest()
    trainers=json.loads((ROOT/'extracted/trainers/trainer_audit.json').read_text())
    if trainers['source_sha256']!=digest:raise ValueError('Stale trainer audit')
    native=native_evidence(rom);table,_=discover(rom);index=929;row=table+40*index
    zero_end=row
    while zero_end<len(rom) and rom[zero_end]==0:zero_end+=1
    incoming=mirror_index(rom);windows=guarded_windows(rom,incoming)
    result={'source_sha256':digest,'native_trainer_state':{'evidence':native,'base':0x0203D000,
            'byte_offset':'trainer_id >> 3','mask':'1 << (trainer_id & 7)',
            'modes':{'0':'get: zero bit means defeated','1':'clear: OR mask means unbeaten','2':'set: BIC mask means defeated'},
            'battle_get_hook':0x803E4,'battle_set_hook':0x803FC,
            'limits':'Shared native hooks, not a new encounter test. No maximum safe trainer ID inferred; native clear function 80450 is not the hooked script command 62.'},
        'trainer_candidate':{'id':index,'row':row,'raw_hex':rom[row:row+40].hex(),'row_all_zero':rom[row:row+40]==bytes(40),
            'zero_span':[row,zero_end],'next_bytes_hex':rom[zero_end:zero_end+16].hex(),
            'direct_battle_command_hits':[r for r in trainers['battles'] if r['trainer_id']==index],
            'battle_catalogue_size':len(trainers['battles']),'bit_address':0x0203D000+index//8,'mask':1<<(index&7),
            'status':'CANDIDATE_ONLY: computed/native IDs and row ownership not certified; no trainer allocated'},
        'rom_screen':{'scope':'All byte offsets; raw 08–0D words normalized to this 16 MiB image, including Thumb low bits conservatively. Not decoded references.',
            'raw_word_shapes':sum(len(v)for v in incoming.values()),'distinct_target_shapes':len(incoming),
            'protected_ranges':[list(r)for r in PROTECTED],'minimum_bytes':4096,'guard_bytes':256,
            'windows':windows,'best_window_boundary_shapes':[]},
        'status':'No allocation or free-space certificate. Runtime state fixture is separate from address ownership; computed pointers and asset extents remain review gates.'}
    if windows:
        best=windows[0];near=[t for t in sorted(incoming)if best['start']-512<=t<best['end_exclusive']+512]
        result['rom_screen']['best_window_boundary_shapes']=[{'target':t,'references':incoming[t]}for t in near]
    out=ROOT/'extracted/maps/allocation_audit.json';out.write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Bounded allocation evidence','',result['status'],'',
        '## Trainer state and candidate row','',
        'Native command 60/get, 61/set and 62/clear are patched to the same inverted-bit store as the battle get/set callbacks. The store base is 0x0203D000; zero means defeated. These are independent of ordinary story flags with the same numeric ID. Exact native bytes and script-command table identities are checked before reporting this result.', '',
        f'Candidate trainer {index} has a zero 40-byte row at 0x{row:X}. Its zero span ends at 0x{zero_end:X}, where real text/script data resumes; the earlier 1,024-row scan is not a table-capacity certificate. None of the {len(trainers["battles"])} bounded trainerbattle sites uses this ID. Computed/native IDs and ownership remain unproven. No trainer ID is reserved.', '',
        'The disposable runtime experiment uses native clear/set/get, verifies one changed byte and independence from ordinary story flag 929, then uses actual game Save and a fresh emulator process. Candidate bit 929 and temporary room value 0x5331=2 persist. These are storage checks, not proof of unused IDs, migration compatibility, battle behavior or authored content.', '',
        '## ROM screen','',result['rom_screen']['scope'],'',
        'This strengthens the earlier 08-only pointer screen. It excludes a 256-byte neighborhood of each raw target and the active cartridge driver/save windows. FF bytes and missing pointer shapes remain insufficient to certify space; a computed pointer or asset extent may still cross a window. No ROM expansion or allocation is performed.', '',
        '| Largest screened windows (exclusive end) | Bytes | Reserved |','|---|---:|---|']
    for w in windows[:5]:lines.append(f'| 0x{w["start"]:X}–0x{w["end_exclusive"]:X} | {w["bytes"]} | no |')
    lines += ['', 'The only surviving 4 KiB window is 0xCA58B4–0xCA6C02. Its enclosing FF run also overlaps the active embedded-save area. Although the window itself is outside the observed save range, broader NOR reservation/erase extents remain unverified. It is not a safe default allocation. Boundary word shapes are retained, including unaligned overlaps; they are not promoted to real pointers.', '', 'Review gate: the final design must supply a concrete byte budget, classify boundary references/asset extents and cartridge reservations, then list exact expected bytes and allowed writes in the builder manifest. Neither this interior candidate nor 32 MiB expansion is certified.']
    (ROOT/'research/allocation_findings.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'trainer_candidate':index,'row':hex(row),'screened_windows':len(windows),'largest':windows[:1]},indent=2))


if __name__=='__main__':main()
