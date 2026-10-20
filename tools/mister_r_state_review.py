"""Classify remaining raw Mister R state shapes as inherited asset contexts.

No global/native absence certificate. Proposes extending the room-owned state
instead of consuming an unrelated flag; does not allocate or patch anything.
"""
import hashlib
import json
import struct
from pathlib import Path
from map_selection_audit import lz77_extent
from pointer_scan import index_pointers
ROOT=Path(__file__).resolve().parents[1]
AUDIO={0x52AFF4:0x52A3C0,0x553EC9:0x553108,0x611485:0x60FEB0}


def review(rom,reference,prior,progression):
    digest=hashlib.sha256(rom).hexdigest()
    if prior['source_sha256']!=digest or progression['source_sha256']!=digest:raise ValueError('Stale state evidence')
    incoming=index_pointers(rom);rows=[]
    for row in prior['wider_search']['state_command_shapes']:
        if row['classification']!='unresolved_raw_shape':continue
        pc=row['instruction']['pc'];end=row['instruction']['end'];entry={'instruction':row['instruction'],'prior_classification':row['classification']}
        if pc in AUDIO:
            at=AUDIO[pc];kind,status,freq,loop,size=struct.unpack_from('<HHIII',rom,at)
            if kind!=1 or status!=0 or loop!=0 or freq!=10764288 or not size:raise ValueError('Audio header identity changed')
            # Type-1 BDPCM encodes a block of 64 samples in 33 bytes. Retain
            # complete frames; final sample count can be a partial frame.
            stop=at+16+((size+63)//64)*33
            if not at+16<=pc<end<=stop or stop>len(rom):raise ValueError('Shape outside audio-format span')
            sites=incoming.get(at,[])
            if len(sites)<2:raise ValueError('Missing independent tone references')
            entry.update(classification='INHERITED_POINTER_BACKED_AUDIO_FORMAT',asset={'start':at,'end_exclusive':stop,'type':kind,'sample_count':size,'frequency_word':freq,'header_hex':rom[at:at+16].hex(),
                         'tone_references':[{'pointer_site':p,'tone_start':p-4,'tone_hex':rom[p-4:p+8].hex()}for p in sites]},matches_reference=rom[at:stop]==reference[at:stop])
        elif pc==0x70EFA3:
            extent=lz77_extent(rom,0x703C40)
            if not extent or not extent['start']<=pc<end<=extent['end']:raise ValueError('Compressed reference asset changed')
            entry.update(classification='INHERITED_VALIDATED_LZ77',asset=extent,matches_reference=rom[extent['start']:extent['end']]==reference[extent['start']:extent['end']],
                         note='No absolute pointer to the header was found; discovered by aligned LZ77 validation. Byte-identical reference context corroborates non-story payload. Do not invent a map/script owner.')
        else:raise ValueError('New unclassified state shape')
        if not entry['matches_reference']:raise ValueError('Inherited asset bytes changed')
        rows.append(entry)
    return {'source_sha256':digest,'reclassified_shapes':rows,'supported_extended_operand_sites':progression['global_extended_operand_candidates'].get('0x5331',[]),
            'existing_condition_owners':prior['wider_search']['state_condition_owners'],'existing_visibility_owners':prior['wider_search']['visibility_flag_owners'],
            'decision':'Prefer a reviewed extension of room-owned variable 0x5331 for P001, preserving original 0/1 semantics, rather than treating unrelated flags as free. Values 2/3 are design proposals only, not allocated.',
            'allocations':[],'limits':'All four unresolved raw instruction shapes are inside inherited asset-format spans. No additional supported state handler is established. Computed IDs/native paths and out-of-scope scripts remain unknown; this is not global absence or a hardware/save-ABI certificate.'}


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();reference=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
    result=review(rom,reference,json.loads((ROOT/'extracted/maps/mister_r_diagnosis.json').read_text()),json.loads((ROOT/'extracted/scripts/orange_progression_audit.json').read_text()))
    (ROOT/'extracted/scripts/mister_r_state_review.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Mister R state ownership review','',result['decision'],'',result['limits'],'','| Raw instruction shape | Enclosing inherited asset | Classification | Same as FireRed |','|---|---|---|---|']
    for row in result['reclassified_shapes']:
        asset=row['asset'];stop=asset.get('end_exclusive',asset.get('end'))
        lines.append(f"| 0x{row['instruction']['pc']:X} | 0x{asset['start']:X}–0x{stop:X} | {row['classification']} | yes |")
    lines += ['', 'Three shapes are within type-1 compressed WaveData spans with two independent ToneData references each. The fourth lies in a validated LZ77 stream beginning 0x703C40; its entire compressed payload matches FireRed. That stream has no discovered absolute header pointer, which is why the earlier pointer-only classification left it unresolved.', '', 'The existing room frame condition and introduction remain the supported owners of 0x5331; the introduction writes 1. The linked game-save/fresh-process replay already proves persistence of that existing value. Extending this owned variable can avoid a new save-layout field or an unrelated new flag, but new values and migration behavior still require architecture review.', '', 'Proposed state contract: 0 preserves the original intro; 1 means introduced/puzzle pending; 2 means puzzle solved/battle retry available; 3 means won/completed. Unknown values take a safe recovery path without replaying the intro, granting rewards or marking victory. No state values are changed by this audit. The missing mechanic, team and trainer/asset allocation are still unresolved.']
    (ROOT/'research/mister_r_state_review.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'reclassified_shapes':len(result['reclassified_shapes']),'allocations':result['allocations']},indent=2))


if __name__=='__main__':main()
