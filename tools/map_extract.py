"""Targeted LC map ownership discovery from native lookup and controller pointers.
Physical pointer prefixes are scan limits, not engine-enforced map counts.
"""
import bisect,csv,hashlib,json,struct
from pathlib import Path
from gba_text_codec import parse
from pointer_scan import BASE,index_pointers
ROOT=Path(__file__).resolve().parents[1]
LOOKUP_SIGNATURE=bytes.fromhex('00 04 09 04 03 4a 80 0b 80 18 00 68 89 0b 09 18 08 68 70 47')
NAME_LOOKUP_SIGNATURE=bytes.fromhex('70 b5 06 1c 09 04 12 04 14 0c 08 0c 05 4a 89 18 0d 0c a4 2d 16 d8 ff f7 d7 ff 01 28 06 d1 02 49 08 e0 00 00 00 00 a8 ff 2e f2 3e 08 04 48 a9 00 09 18 09 68 30 1c 43 f7 e9 ff 01 1c 0b e0 00 00 80 89 2c 08')
class FormatError(ValueError):pass

def u32(rom,offset):
    if offset<0 or offset+4>len(rom):raise FormatError('Out-of-ROM word')
    return struct.unpack_from('<I',rom,offset)[0]
def pointer(rom,offset,nullable=False):
    value=u32(rom,offset)
    if nullable and value==0:return None
    target=value-BASE
    if not 0<=target<len(rom):raise FormatError('Non-ROM pointer')
    return target

def pointer_prefix(rom,start,limit=4096):
    values=[]
    for i in range(limit):
        try:target=pointer(rom,start+i*4)
        except FormatError:return {'start':start,'end':start+i*4,'targets':values,'stop':'non-ROM-pointer word','terminator_hex':rom[start+i*4:start+i*4+8].hex(' ')}
        values.append(target)
    return {'start':start,'end':start+limit*4,'targets':values,'stop':'scan limit','terminator_hex':''}

def discover_lookup(rom):
    offsets=[];position=0
    while True:
        at=rom.find(LOOKUP_SIGNATURE,position)
        if at<0:break
        position=at+1
        try:table=pointer(rom,at+20)
        except FormatError:continue
        offsets.append({'function':at,'literal_site':at+20,'table':table,'raw_hex':rom[at:at+24].hex(' ')})
    if len(offsets)!=1:raise FormatError('Native map lookup discovery ambiguous')
    return offsets[0]

def events(rom,offset):
    if offset%4 or offset+20>len(rom):raise FormatError('Invalid event structure')
    counts=list(rom[offset:offset+4]);arrays=[]
    for i,stride in enumerate((24,8,16,12)):
        target=pointer(rom,offset+4+i*4,nullable=True)
        if counts[i] and (target is None or target+counts[i]*stride>len(rom)):raise FormatError('Invalid event array span')
        arrays.append(target)
    return {'offset':offset,'counts':counts,'arrays':arrays}

def header(rom,offset):
    if offset%4 or offset+28>len(rom):raise FormatError('Invalid map header')
    layout=pointer(rom,offset);ev=pointer(rom,offset+4,nullable=True)
    width,height=struct.unpack_from('<ii',rom,layout)
    if width<=0 or height<=0:raise FormatError('Invalid layout dimensions')
    blocks=pointer(rom,layout+12)
    if width*height*2>len(rom)-blocks:raise FormatError('Layout blocks outside ROM')
    # A null events pointer is present in retained legacy map slots. Preserve
    # that distinction: zero exported events is not a runtime safety claim.
    event_info=events(rom,ev) if ev is not None else {'offset':None,'counts':[0,0,0,0],'arrays':[None]*4}
    result={'header':offset,'layout':layout,'width':width,'height':height,'map_blocks':blocks,
      'map_scripts':pointer(rom,offset+8,nullable=True),'connection_structure':pointer(rom,offset+12,nullable=True),
      'music':struct.unpack_from('<H',rom,offset+16)[0],'layout_id':struct.unpack_from('<H',rom,offset+18)[0],
      'section_id':rom[offset+20],'map_type':rom[offset+23],'events':event_info}
    # The targeted owner layouts happen to use contiguous arrays; record and
    # validate this independent geometry without imposing it on every LC map.
    spans=[event_info['arrays'][i]+event_info['counts'][i]*stride if event_info['arrays'][i] is not None else None for i,stride in enumerate((24,8,16,12))]
    result['contiguous_event_geometry']=ev is not None and all(spans[i]==event_info['arrays'][i+1] for i in range(3)) and spans[3]==ev
    return result

def label(rom,section):
    # Retained independently discovered native-name lookup literals.
    if rom[0xC4D78:0xC4DBC]!=NAME_LOOKUP_SIGNATURE:raise FormatError('Native name lookup signature changed')
    index=section-0x58
    if not 0<=index<=0xA4:return {'text':None,'status':'outside inspected name-index range'}
    site=0x2C8980+index*4;start=pointer(rom,site);p=parse(rom,start,strict_english=True)
    if not p or not p['terminated'] or p['issues']:return {'text':None,'pointer_site':site,'target':start,'status':'unparsed'}
    return {'text':p['plain'],'pointer_site':site,'target':start,'status':'section label; individual room/floor identity unverified'}

def extract(rom,roots):
    incoming=index_pointers(rom);targets=sorted(incoming);lookup=discover_lookup(rom)
    groups=pointer_prefix(rom,lookup['table'],256)
    banks={i:pointer_prefix(rom,base) for i,base in enumerate(groups['targets'])}
    header_slots={}
    for group,bank in banks.items():
        for number,h in enumerate(bank['targets']):header_slots.setdefault(h,[]).append({'group':group,'map':number,'pointer_site':bank['start']+number*4})
    owners=[];unresolved=[];maps={}
    for root in roots:
        for site in incoming.get(root,[]):
            matches=[];event_record=site-8
            # A BG array can contain at most 255 records under the u8 count.
            starts=targets[bisect.bisect_left(targets,max(0,event_record-12*254)):bisect.bisect_right(targets,event_record)]
            for array in starts:
                if (event_record-array)%12 or array%4:continue
                index=(event_record-array)//12
                for event_pointer in incoming.get(array,[]):
                    event_struct=event_pointer-16
                    try:ev=events(rom,event_struct)
                    except (FormatError,struct.error):continue
                    if ev['arrays'][3]!=array or ev['counts'][3]<=index:continue
                    x,y=struct.unpack_from('<HH',rom,event_record);elevation,kind=rom[event_record+4:event_record+6]
                    if kind>4:continue  # other union variants are not script references here
                    for header_pointer in incoming.get(event_struct,[]):
                        candidate=header_pointer-4
                        if candidate not in header_slots:continue
                        try:h=header(rom,candidate)
                        except (FormatError,struct.error):continue
                        if h['events']['offset']!=event_struct or not (x<h['width'] and y<h['height']):continue
                        for slot in header_slots[candidate]:
                            bank=banks[slot['group']]
                            if bank['stop']=='scan limit':raise FormatError('Owner bank extent exceeded scan limit')
                            key=(slot['group'],slot['map'])
                            if key not in maps:
                                hrow={**h,**slot,'section_label':label(rom,h['section_id']),'warps':[],'connections':[]}
                                warp_base=ev['arrays'][1]
                                for j in range(ev['counts'][1]):
                                    p=warp_base+j*8;wx,wy,el,wid,num,grp=struct.unpack_from('<hhBBBB',rom,p)
                                    hrow['warps'].append({'offset':p,'index':j,'x':wx,'y':wy,'elevation':el,'destination_warp':wid,'destination_map':num,'destination_group':grp,'destination_status':'raw encoded destination; see separate connectivity audit for validation'})
                                conn=hrow['connection_structure']
                                if conn is not None:
                                    count=struct.unpack_from('<i',rom,conn)[0];base=pointer(rom,conn+4,nullable=count==0)
                                    if count<0 or count>32 or (count and base+count*12>len(rom)):raise FormatError('Invalid selected-map connection array')
                                    for j in range(count):
                                        p=base+j*12
                                        hrow['connections'].append({'offset':p,'direction':rom[p],'displacement':struct.unpack_from('<i',rom,p+4)[0],'destination_group':rom[p+8],'destination_map':rom[p+9]})
                                maps[key]=hrow
                            matches.append({'script_root':root,'pointer_site':site,'group':slot['group'],'map':slot['map'],
                              'header':candidate,'events':event_struct,'bg_array':array,'bg_record':event_record,'bg_index':index,
                              'x':x,'y':y,'elevation':elevation,'kind':kind,'section_label':maps[key]['section_label']['text'],
                              'reachability':'UNKNOWN'})
            unique={(m['group'],m['map'],m['bg_record']):m for m in matches}
            if unique:owners.extend(unique.values())
            else:unresolved.append({'script_root':root,'pointer_site':site,'reason':'No validated BG-array/events/header/native-bank chain'})
    return {'source_sha256':hashlib.sha256(rom).hexdigest(),'lookup':lookup,
      'group_table_physical_prefix':{k:v for k,v in groups.items() if k!='targets'},
      'owner_bank_physical_prefixes':{str(g):{k:v for k,v in banks[g].items() if k!='targets'} for g in sorted({m['group'] for m in owners})},
      'summary':{'controller_roots':len(roots),'owned_roots':len({o['script_root'] for o in owners}),
        'bg_event_ownerships':len(owners),'map_records':len(maps),'unresolved_root_pointer_sites':len(unresolved),
        'raw_warps':sum(len(m['warps']) for m in maps.values()),'raw_connections':sum(len(m['connections']) for m in maps.values())},
      'scope':'Ten Nexus controller roots only. Pointer prefixes are physical scan candidates, not native bounds. Layout/event validation applies to selected owners; dummy/bad slots elsewhere are not discarded from the banks. No gameplay reachability or full connectivity claim.',
      'owners':sorted(owners,key=lambda m:(m['script_root'],m['group'],m['map'],m['bg_index'])),
      'maps':[maps[k] for k in sorted(maps)],'unresolved_pointer_sites':unresolved}

def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    nexus=json.loads((ROOT/'extracted/text/nexus_machine_audit.json').read_text())
    if nexus['source_sha256']!=hashlib.sha256(rom).hexdigest():raise FormatError('Stale controller audit')
    result=extract(rom,[c['entry'] for c in nexus['controller_scripts']])
    (ROOT/'extracted/maps/controller_map_owners.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'extracted/maps/controller_map_owners.csv').open('w',newline='') as f:
        fields=['group','map','section_label','script_root','bg_index','x','y','pointer_site','header']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for owner in result['owners']:writer.writerow({k:(f'0x{owner[k]:X}' if k in ('script_root','pointer_site','header') else owner[k]) for k in fields})
    with (ROOT/'extracted/maps/controller_map_warps.csv').open('w',newline='') as f:
        fields=['source_group','source_map','index','x','y','destination_group','destination_map','destination_warp']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for m in result['maps']:
            for warp in m['warps']:writer.writerow({**{k:warp[k] for k in fields if k in warp},'source_group':m['group'],'source_map':m['map']})
    lines=['# First map ownership inventory — Nexus controllers','',f"Source SHA-256: `{result['source_sha256']}`.",'',result['scope'],'',
      'CONFIRMED_IN_ROM: byte/pointer/coordinate values. Structural roles use pinned FireRed field definitions and native lookup evidence. Section labels are not unique room names.','',
      f"Native lookup signature at 0x{result['lookup']['function']:X}; group-table literal at 0x{result['lookup']['literal_site']:X} → table 0x{result['lookup']['table']:X}.",'',
      '| Group:map (decimal) | Section label | Header | Layout size | Objects/warps/coords/BG |','|---|---|---|---|---|']
    for m in result['maps']:lines.append(f"| {m['group']}:{m['map']} | {m['section_label']['text']} | 0x{m['header']:X} | {m['width']}×{m['height']} | "+'/'.join(str(c) for c in m['events']['counts'])+' |')
    lines += ['', '## Background-event owners','', '| Script | Group:map | BG index | Coordinates | Pointer site |','|---|---|---|---|---|']
    for m in result['owners']:lines.append(f"| 0x{m['script_root']:X} | {m['group']}:{m['map']} | {m['bg_index']} | {m['x']},{m['y']} | 0x{m['pointer_site']:X} |")
    lines += ['', '## Bounds and remaining work','',
      'Group-table and bank starts come from native lookup pointers, not the beginning of a maximal pointer-looking run. Selected bank prefixes stop at non-ROM words. Do not trim banks at a bad intermediate layout or infer counts from numerically adjacent bank pointers. The native lookup itself has no certified bounds check.','',
      'All 17 owner records retain script reuse; identical scripts or coordinates do not certify duplicate maps. This first pass exports raw warp and connection records. Run tools/warp_graph.py for separate destination, return-record and default indexed-layout checks; see research/orange_connectivity.md. Gates and runtime reachability remain untested.','',
      'The bounded connectivity audit expands the scope to 32 distinct map slots. Continue by cataloging their event and map-entry scripts, retaining candidate aliases and legacy content.']
    (ROOT/'research/orange_map_inventory.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(result['summary'],indent=2))
if __name__=='__main__':main()
