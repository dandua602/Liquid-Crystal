"""Read-only patch preflight: candidate padding, active hooks and regional links.
Nothing is allocated. Padding and absent scoped references are not free-space
or unused-state certificates; native/computed and unresolved uses remain.
"""
import bisect
import hashlib
import json
import re
from pathlib import Path

from pointer_scan import index_pointers
from warp_graph import MapCatalog,warp_destination,connection_destination

ROOT=Path(__file__).resolve().parents[1]


def padding_candidates(rom,incoming,minimum=4096):
    targets=sorted(incoming);result=[]
    for match in re.finditer(b'\xff{'+str(minimum).encode()+b',}',rom):
        start,end=match.span();aligned=(start+3)&~3
        used=targets[bisect.bisect_left(targets,start):bisect.bisect_left(targets,end)]
        result.append({'start':start,'end':end,'bytes':end-start,'aligned_start':aligned,
                       'aligned_bytes':max(0,end-aligned),'incoming_target_count':len(used),
                       'incoming':[{'target':target,'sites':incoming[target]} for target in used],
                       'status':'CANDIDATE_ONLY_NOT_ALLOCATED'})
    return sorted(result,key=lambda r:r['bytes'],reverse=True)


def regional_links(rom):
    catalog=MapCatalog(rom);queue=[(3,n,0) for n in range(77,112)];seen=set();edges=[];failures=[]
    while queue:
        group,number,depth=queue.pop(0)
        if (group,number) in seen:continue
        seen.add((group,number));m=catalog.resolve(group,number)
        if m['status']!='structure_validated':failures.append(m);continue
        for kind,records in [('warp',m['warps']),('connection',m['connections'])]:
            for record in records:
                target=catalog.resolve(record['destination_group'],record['destination_map'])
                destination=(warp_destination(record,m,target) if kind=='warp' else connection_destination(record,m,target))
                edges.append({'source':m['id'],'kind':kind,'record':record,'destination':destination})
                if depth<2 and target['group']!=0 and (target['group']!=3 or 77<=target['map']<=111):
                    queue.append((target['group'],target['map'],depth+1))
    return {'scope':'Outdoor candidate slots 3:77–111 and up to two room hops. Includes inherited/non-Orange slots and stops expansion through 0:0. Links are structure, not gameplay reachability.',
            'expanded_slots':len(seen),'context_maps':list(catalog.maps.values()),'edges':edges,'failures':failures}


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();digest=hashlib.sha256(rom).hexdigest()
    prior=json.loads((ROOT/'extracted/scripts/orange_progression_audit.json').read_text())
    if prior['source_sha256']!=digest:raise ValueError('Stale progression audit')
    incoming=index_pointers(rom);padding=padding_candidates(rom,incoming)
    hooks=[{'site':site,'bytes':rom[site:site+length].hex(' '),'role':role,'allocation':None}
           for site,length,role in [(0xC30A24,4,'6:31 map events pointer'),(0xC30A28,4,'6:31 map scripts pointer'),
                                    (0xC30A18,4,'indexed default layout pointer; preserve if geometry unchanged'),
                                    (0xC30F30,4,'object 1 ROM-start script field; original field preserved unless reviewed'),
                                    (0xC30F7C,4,'damaged-sign BG script pointer; preserve original clue')]]
    # Raw 09-prefixed words are deliberately not promoted to real pointers.
    expansion_shapes=[at for at in range(len(rom)-3) if rom[at+3]==9]
    result={'source_sha256':digest,'source_bytes':len(rom),'padding_candidates':padding,'hook_ledger':hooks,
            'expansion':{'proposed_start':len(rom),'gba_maximum_bytes':0x2000000,'allocated_bytes':0,
                         'verified_cartridge_bank_port':0x09000000,'active_embedded_save_range':[0xC80000,0xCA0000],
                         'raw_09_word_shapes':len(expansion_shapes),'first_shape_sites':expansion_shapes[:32],
                         'status':'NOT_CERTIFIED; review cross-bank and existing mirror-address uses before expansion'},
            'active_extended_operand_candidates':prior['global_extended_operand_candidates'],
            'active_flag_command_candidates':prior['global_flag_command_candidates'],
            'regional_graph':regional_links(rom),
            'certification':'No free ROM/state certificate and no allocation. Candidate-root scan has frontiers; raw pointer/padding tests do not establish native/computed absence.'}
    (ROOT/'extracted/maps/architecture_preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# ROM-space preflight','',f'Source SHA-256: `{digest}`; {len(rom):,} bytes.','',result['certification'],'',
           '| Candidate FF range | Bytes | Aligned start | Incoming target addresses |','|---|---:|---|---:|']
    for row in padding[:20]:lines.append(f"| 0x{row['start']:X}–0x{row['end']:X} | {row['bytes']} | 0x{row['aligned_start']:X} | {row['incoming_target_count']} |")
    lines += ['',f"There are {len(padding)} FF runs of at least 4 KiB. These are candidates, not reservations. No candidate has been overwritten.",'',
              f"ROM expansion is a proposal only. There are {len(expansion_shapes):,} raw 09-prefixed four-byte shapes; most can be arbitrary data. They require classification before claiming old mirror-address behavior is irrelevant.",'',
              'The image-specific cartridge driver writes its bank selector at 0x09000000 and programs an embedded save at 0xC80000–0xCA0000. That save window is active storage, not asset space. Preserve it and review cartridge behavior before expanding the image. See save_hardware.json.', '',
              'A final allocator must enforce input hashes, expected original bytes, bounds/alignment, nonoverlap and a changed-range allowlist. It must not automatically select the largest FF run.']
    (ROOT/'research/free_space_report.md').write_text('\n'.join(lines)+'\n')
    lines=['# Candidate address ledger','',result['certification'],'','| Existing field | Original bytes | Role | Allocation |','|---|---|---|---|']
    for row in hooks:lines.append(f"| 0x{row['site']:X} | `{row['bytes']}` | {row['role']} | none |")
    lines += ['','The embedded save window 0xC80000–0xCA0000 and image-specific driver around 0xC72100 are active cartridge data/code, not a new allocation pool. All original fields remain unchanged. No target addresses have been assigned. Any geometry change additionally requires reviewing both header and indexed layout pointers.']
    (ROOT/'research/address_ledger.md').write_text('\n'.join(lines)+'\n')
    lines=['# State allocation ledger','',result['certification'],'',f"The broad candidate-root scan observes {len(prior['global_extended_operand_candidates'])} distinct extended-operand candidates and {len(prior['global_flag_command_candidates'])} distinct flag-command IDs. See architecture_preflight.json for instruction sites.",'',
           'No flag or variable is allocated. Existing 0x5331 / 0x5C5 belong to Mister R; 0x5315 and 0x513 to laboratory progression; 0x5318 and the controller/charge/shutdown flags remain active. These must not become an implicit free pool.','',
           'The scoped scan follows standard scripts but retains unsupported/native/context-transfer frontiers. Unseen IDs are not certified unused. Save persistence must be verified for any selected state and old-save defaults must be specified.', '', 'The later ownership review favors a proposed extension of existing room-owned 0x5331, preserving original 0/1 and considering 2/3 for solved/completed. This is a design proposal, not an allocation. Current value 1 and temporary value 2 have verified save/reload persistence; value 3 and unusual old-save migration remain unverified. See allocation_findings.md for the separate inverted trainer-bit store; candidate ID 929 is not allocated. See mister_r_state_review.md and patch_spec.md.']
    (ROOT/'research/flag_var_ledger.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'padding_candidates':len(padding),'active_extended_candidates':len(result['active_extended_operand_candidates']),
                      'active_flag_candidates':len(result['active_flag_command_candidates']),'expanded_regional_slots':result['regional_graph']['expanded_slots'],
                      'regional_edges':len(result['regional_graph']['edges'])},indent=2))


if __name__=='__main__':main()
