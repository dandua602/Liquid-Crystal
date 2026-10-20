"""Concrete 2 KiB design budget and fail-closed static screen; no ROM writes.

This is a bounded allocation proposal, not global/native ownership proof or
permission to implement before architecture review.
"""
import hashlib
import json
from pathlib import Path
from allocation_audit import mirror_index,guarded_windows
from trainer_audit import discover

ROOT=Path(__file__).resolve().parents[1]
DIGEST='c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf'
START,END=0xB9EF00,0xB9F700
BUDGET=[('scripts',0x280),('text',0x200),('room_event_tables',0x100),('trainer_party',0x60),('reserve',0x220)]


def screen_interval(rom,incoming,start=START,end=END,guard=256):
    if not 0<=start<end<=len(rom)or start%4:raise ValueError('Invalid proposed ROM interval')
    if rom[start:end]!=b'\xff'*(end-start):raise ValueError('Candidate is not unchanged FF padding')
    if start<0xD00000 and end>0xC00000:raise ValueError('Cartridge driver/save bank excluded conservatively')
    hits=[{'target':t,'references':v}for t,v in incoming.items()if start-guard<=t<end+guard]
    if hits:raise ValueError('Raw ROM alias/reference shape crosses guarded candidate')
    return {'start':start,'end_exclusive':end,'bytes':end-start,'guard':guard,'incoming_shape_hits':hits,
            'expected_bytes':'FF repeated 2048 times','expected_sha256':hashlib.sha256(rom[start:end]).hexdigest()}


def budget_rows():
    at=START;rows=[]
    for purpose,size in BUDGET:
        rows.append({'purpose':purpose,'start':at,'end_exclusive':at+size,'capacity_bytes':size});at+=size
    if at!=END:raise ValueError('Budget does not fit proposed interval')
    return rows


def main():
    rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    if hashlib.sha256(rom).hexdigest()!=DIGEST:raise ValueError('Unsupported source ROM')
    incoming=mirror_index(rom);screen=screen_interval(rom,incoming)
    windows=guarded_windows(rom,incoming,minimum=2048)
    enclosing=next(w for w in windows if w['start']<=START and END<=w['end_exclusive'])
    table,_=discover(rom);row=table+929*40
    if rom[row:row+40]!=bytes(40):raise ValueError('Candidate trainer row changed')
    trainers=json.loads((ROOT/'extracted/trainers/trainer_audit.json').read_text())
    if trainers['source_sha256']!=DIGEST:raise ValueError('Stale trainer-use catalogue')
    ids=sorted({r['trainer_id']for r in trainers['battles']})
    hooks=[{'site':at,'expected_hex':rom[at:at+4].hex(),'purpose':purpose,'replacement':None}for at,purpose in
           [(0xC30A24,'room event-table pointer'),(0xC30A28,'room map-script-table pointer')]]
    data={'source_sha256':DIGEST,'status':'BOUNDED_STATIC_SCREEN_PASS; proposed budget only, no allocation or implementation',
          'rom_proposal':screen,'enclosing_screened_window':enclosing,'budget':budget_rows(),
          'trainer_row_proposal':{'id':929,'start':row,'bytes':40,'expected_hex':rom[row:row+40].hex(),
                                  'largest_bounded_script_id':max(ids),'direct_hits':[r for r in trainers['battles']if r['trainer_id']==929],
                                  'ownership':'No native/computed-ID absence certificate; not reserved'},
          'existing_hook_fields':hooks,'excluded_bank':[0xC00000,0xD00000],
          'limits':['All ROM wait-state aliases and byte alignments screened, with 256-byte guards.',
                    'No native/computed-address or enclosing-asset-extent absence certificate.',
                    'No hardware or broader cartridge reservation certificate.',
                    'No trainer team, puzzle interaction or NPC migration policy is frozen.',
                    'No expected pointer replacement or output ROM exists before design review.']}
    out=ROOT/'extracted/maps/p001_preflight.json';out.write_text(json.dumps(data,indent=2)+'\n')
    lines=['# P001 bounded byte budget','',data['status'],'',
           'The original 4 KiB threshold was a screening choice, not a demonstrated patch requirement. A 2 KiB data-only slice offers 31 guarded windows. Select 0xB9EF00–0xB9F700 as the review candidate inside the 3,944-byte screened interval 0xB9EE78–0xB9FDE0. It has no raw 08–0D target shape at any byte alignment within the interval or 256-byte guards. All 2,048 bytes are FF.', '',
           'Unlike the earlier 4 KiB candidate near 0xCA0000, this proposal is outside the entire conservatively excluded 0xC00000–0xD00000 cartridge bank. It requires no ROM expansion, driver change or field-menu extension. This improves the candidate; it does not prove every computed address or hidden asset extent absent.', '',
           '| Proposed block | Start | Capacity |','|---|---|---:|']
    for row in data['budget']:lines.append(f'| {row["purpose"]} | 0x{row["start"]:X} | {row["capacity_bytes"]} |')
    lines += ['', 'Room tables have a 256-byte envelope; trainer party has 96 bytes for six 16-byte records if the final team requires custom moves/items. The exact mechanic and text must fit these budgets or explicitly reopen allocation review. Preserve map blocks/tilesets by default; geometry changes are not included.', '',
              'Trainer row 929 at 0xAC8EAC is separately proposed (40 zero bytes), not allocated. The largest direct trainer ID in the bounded 1,247-command catalogue is 928. Computed/native ID use remains a distinct unresolved ownership gate. Neither generic Elite team is adopted as the missing Mister R team.', '',
              'Before implementation: approve final story/mechanic, close ownership/extent and migration questions, then freeze exact hook replacements and expected bytes. A future builder must reject overflow, stale inputs, unexpected bytes and writes outside the manifest. This script creates no patch or output ROM.']
    (ROOT/'research/p001_budget.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'status':data['status'],'window':[hex(START),hex(END)],'bytes':END-START,'screened_2k_windows':len(windows)},indent=2))


if __name__=='__main__':main()
