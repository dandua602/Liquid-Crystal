"""Positive local ownership bounds for the proposed P001 ROM interval.

An exact-source bounded static certificate, not proof about every unknown
computed address or real cartridge. No allocation or ROM output.
"""
import hashlib
import json
import struct
from pathlib import Path
from allocation_audit import mirror_index
from p001_preflight import DIGEST,START,END,screen_interval
from pointer_scan import index_pointers

ROOT=Path(__file__).resolve().parents[1]
NATIVE={
 0xBFC50:'10b50004040c0904090c0023054a00201056a04208d101201056884204d1581c07e0000008e0b90808320133252beed9002010bc02bc084700b50004000c0904090cfff7ddff002806d0c0000149401803e0000000e0b908002002bc0847000000b5002808d0252806d8c0000149401803e0000000e0b908002002bc08470000',
 0xB9FF60:'0fb4184b16495a78d200891808791a78824202da01321a7006e000221a704a795a700868104912df',
}


def native_bounds(rom):
    for at,expected in NATIVE.items():
        if rom[at:at+len(bytes.fromhex(expected))]!=bytes.fromhex(expected):
            raise ValueError(f'Native ownership bytes changed at {at:X}')
    left=struct.unpack_from('<I',rom,0xBFC74)[0]-0x08000000
    right=struct.unpack_from('<I',rom,0xB9FFC0)[0]-0x08000000
    if left!=0xB9E008 or right!=0xB9FEE0:raise ValueError('Adjacent native table literal changed')
    # The group/number scan includes r3=37, i.e. 38 rows. Do not silently
    # replace it with the direct getter's separate maximum index of 37.
    scan_count=rom[0xBFC7C]+1
    left_end=left+scan_count*8
    if left_end>START or right<END:raise ValueError('Known adjacent owner crosses proposed interval')
    return {'left_table':{'start':left,'conservative_end_exclusive':left_end,'scan_rows':scan_count,
                         'direct_getter_maximum_id':rom[0xBFCB6],
                         'note':'Scan includes trailing FF records; this audit does not fix the existing bound discrepancy.'},
            'right_table':{'start':right,'index_source':'LDRB, then unsigned shift left by 3','stride':8,
                           'minimum_address':right,'maximum_index':255},
            'native_signatures':[{'offset':a,'raw_hex':b}for a,b in NATIVE.items()]}


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();ref=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    if hashlib.sha256(rom).hexdigest()!=DIGEST:raise ValueError('Unsupported source')
    bounds=native_bounds(rom);screen=screen_interval(rom,mirror_index(rom));incoming=index_pointers(rom)
    start=0x5E0458;site=0x5E0A11
    kind,status,freq,loop,count=struct.unpack_from('<HHIII',rom,start)
    if (kind,status,freq,loop,count)!=(1,0,10764288,0,7264):raise ValueError('Audio context changed')
    stop=start+16+((count+63)//64)*33
    if not start+16<=site<site+4<=stop or rom[start:stop]!=ref[start:stop]or len(incoming.get(start,[]))<2:
        raise ValueError('Audio-context witness failed')
    if struct.unpack_from('<I',rom,site)[0]!=0x08B9ED77:raise ValueError('Nearby raw shape changed')
    shapes=[];at=0
    while (at:=rom.find(bytes.fromhex('a103'),at))>=0:
        if (at>=1 and rom[at-1]in (0x60,0x61,0x62))or(at>=2 and rom[at-2]==0x5C):shapes.append(at)
        at+=1
    if shapes:raise ValueError('New raw direct trainer-929 script shape requires review')
    result={'source_sha256':DIGEST,'status':'BOUNDED_STATIC_CERTIFICATE_FOR_DESIGN_REVIEW',
            'rom_interval':screen,'adjacent_owners':bounds,
            'nearby_raw_shape':{'site':site,'word':0x08B9ED77,'classification':'inherited encoded audio payload',
                                'asset':[start,stop],'sample_count':count,'tone_pointer_sites':incoming[start],
                                'entire_asset_matches_reference':True},
            'trainer_929_direct_command_shapes':shapes,
            'scope':'All raw ROM-alias targets plus positive bounds of the inspected adjacent native tables and inherited-audio classification. Trainer battle catalogue and persistence are separate retained evidence.',
            'limits':'Unknown unindexed/native computed owners and real hardware remain outside this certificate. Proposed addresses are unallocated until architecture review. No story script or ROM is generated.'}
    (ROOT/'extracted/maps/space_ownership.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# P001 local ownership certificate','',result['status'],'',result['scope'],'',result['limits'],'',
           '## Positive adjacent-owner bounds','',
           'The healing-location lookup at 0xBFC50 uses table 0xB9E008 with eight-byte rows. Its inclusive comparison visits 38 rows, ending at 0xB9E138. The separate direct getter caps IDs at 37. These distinct observed bounds are retained; trailing FF rows are not silently trimmed or repaired. Both are well before proposed 0xB9EF00–0xB9F700.', '',
           'The native animation table at 0xB9FEE0 is indexed by a loaded unsigned byte shifted left by three. Its computed addresses begin at 0xB9FEE0 and move forward; this inspected owner cannot reach backward into the proposed interval. Exact native instructions/literals are checked before reporting the bound.', '',
           'The nearby apparent 0x08B9ED77 pointer at 0x5E0A11 is encoded audio, inside pointer-backed type-1 WaveData 0x5E0458–0x5E131A. The complete asset matches FireRed and has two tone references. It is not a supported pointer whose data extent reaches into the proposed window.', '',
           'All 08–0D raw target shapes at every alignment are still screened, with 256-byte guards. No direct raw trainerbattle/check/set/clear shape for ID 929 appears anywhere; the bounded existing battle catalogue tops out at 928. Native/computed IDs remain explicitly outside that negative evidence.', '',
           'This closes the identified local adjacent-extent questions for the design proposal under the stated static model. It is not a universal unused-memory theorem. Before player release, enforce the manifest/expected bytes, test the patched room and regressions, and validate cartridge behavior. No original ROM/save was modified.']
    (ROOT/'research/space_ownership.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'status':result['status'],'left_owner_end':hex(bounds['left_table']['conservative_end_exclusive']),
                      'right_owner_start':hex(bounds['right_table']['start']),'raw_trainer_929_shapes':len(shapes)}))


if __name__=='__main__':main()
