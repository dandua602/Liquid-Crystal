"""Guarded P002 builder with standalone and P001-relative reversible BPS."""
import hashlib
import json
from pathlib import Path
from bps_patch import create,apply
from build_p001 import w,h,BASE,Assembler
from p002_design import preflight
ROOT=Path(__file__).resolve().parents[1]
ORIGINAL_SHA='c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf'


def digest(data):return hashlib.sha256(data).hexdigest()


def build(source,design):
    plan=preflight(source,design);out=bytearray(source);writes=[];b=design['budget']
    # Flagless object templates respawn on movement even after removeobject.
    # Keep existing script addresses and use two same-size call hooks to move
    # the cleared rock's template outside this room; restore it for states0/1.
    prior=json.loads((ROOT/'builds/dev/P001-manifest.json').read_text())
    helper=Assembler(b['scripts_start']+plan['used']['scripts'])
    helper.label('visibility_init');helper.emit(0x04,w(BASE+prior['script_labels']['normalize']))
    helper.cmp(0x5331,0,'visibility_pending');helper.cmp(0x5331,1,'visibility_pending')
    helper.emit(0x63,h(3),h(63),h(63));helper.emit(0x03)
    helper.label('visibility_pending');helper.emit(0x63,h(3),h(15),h(9));helper.emit(0x03)
    helper.label('visibility_solved');helper.set(0x5331,0x3302);helper.emit(0x63,h(3),h(63),h(63));helper.emit(0x03)
    plan['scripts_hex']+=helper.resolve().hex();plan['used']['scripts']+=len(helper.data);plan['script_labels'].update(helper.labels)
    if plan['used']['scripts']>b['scripts_capacity']:raise ValueError('Visibility fix exceeds approved script budget')
    solve_site=prior['script_labels']['move_choice']+14
    allowed=[(b[n+'_start'],b[n+'_start']+b[n+'_capacity'])for n in ('scripts','text','tables')]+[(0x3526C0,0x3526C4),(0xB9F3F0,0xB9F3F4),(0xB9EF00,0xB9EF05),(solve_site,solve_site+5)]
    def write(at,data,expected,role):
        end=at+len(data)
        if not any(a<=at and end<=z for a,z in allowed):raise ValueError('Write outside approved allocation')
        if source[at:end]!=expected:raise ValueError('Expected original bytes failed: '+role)
        if any(at<r['end_exclusive']and r['start']<end for r in writes):raise ValueError('Overlapping writes')
        out[at:end]=data;writes.append({'start':at,'end_exclusive':end,'role':role,'before_sha256':digest(expected),'after_sha256':digest(data)})
    for name in ('scripts','text','tables'):
        data=bytes.fromhex(plan[name+'_hex']);write(b[name+'_start'],data,b'\xff'*len(data),'P002 '+name)
    write(0x3526C0,w(BASE+design['group_bank']['new_bank']),w(BASE+design['group_bank']['old_bank']),'relocated group6 bank; original32 words preserved')
    write(0xB9F3F0,w(BASE+plan['script_labels']['sign']),w(BASE+design['entry']['preserve_pending_dispatcher']),'completed warehouse sign dispatcher')
    write(0xB9EF00,b'\x04'+w(BASE+helper.labels['visibility_init']),b'\x04'+w(BASE+prior['script_labels']['normalize']),'keep rock template hidden after reload/movement')
    write(solve_site,b'\x04'+w(BASE+helper.labels['visibility_solved']),b'\x16'+h(0x5331)+h(0x3302),'preserve solved-state write and prevent immediate rock respawn')
    if len(out)!=len(source)or out[0xA0:0xC0]!=source[0xA0:0xC0]:raise ValueError('ROM size/header changed')
    if out[0xC00000:0xD00000]!=source[0xC00000:0xD00000]:raise ValueError('Cartridge bank changed relative to P001')
    for at,(before,after)in enumerate(zip(source,out)):
        if before!=after and not any(r['start']<=at<r['end_exclusive']for r in writes):raise ValueError('Unowned changed byte')
    manifest={'id':'P002','classification':'NEWLY_AUTHORED approved Office Block service room; includes approved P001',
              'input_p001_sha256':digest(source),'original_source_sha256':ORIGINAL_SHA,'output_sha256':digest(out),
              'design_file_sha256':digest((ROOT/'research/design/p002.json').read_bytes()),'writes_relative_to_p001':sorted(writes,key=lambda x:x['start']),
              'prior_manifest':'extracted/builds/P001-manifest.json','capacities_used':plan['used'],'script_labels':plan['script_labels'],
              'text_addresses':plan['text_addresses'],'new_map':[6,32],'map_bank_words_preserved':32,
              'runtime_acceptance':'See separately generated P002-validation.json; building alone does not establish acceptance.',
              'implementation_adjustment':f'Two same-size P001 call hooks plus{len(helper.data)}-byte helper prevent native movement from respawning the flagless cleared rock. Existing0/1 restores its template15,9; solved/completed moves template63,63 outside room before removal. No new flag/variable or engine/save-format change.',
              'hardware_tested':False,'rollback':'Exit new map6:32 back to original warehouse6:31 and save before removing P002.'}
    return bytes(out),manifest


def main():
    path=ROOT/'research/design/p002.json';design=json.loads(path.read_text());approval=json.loads((ROOT/'research/design/p002_approval.json').read_text())
    review=ROOT/'research/design/p002_review_manifest.json'
    if approval['decision']!='approved for implementation'or digest(path.read_bytes())!=approval['design_sha256']or digest(review.read_bytes())!=approval['review_manifest_sha256']:raise ValueError('P002 reviewed approval mismatch')
    for name,expected in json.loads(review.read_text())['artifacts'].items():
        if digest((ROOT/name).read_bytes())!=expected:raise ValueError('Reviewed file changed: '+name)
    source=(ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes();target,manifest=build(source,design);again,second=build(source,design)
    if target!=again or manifest!=second:raise ValueError('Nondeterministic P002')
    original=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    if digest(original)!=ORIGINAL_SHA:raise ValueError('Original source changed')
    folder=ROOT/'builds/dev';folder.mkdir(parents=True,exist_ok=True);patches={}
    for name,a,z in [('P002.bps',original,target),('P002-reverse.bps',target,original),('P001-to-P002.bps',source,target),('P002-to-P001.bps',target,source)]:
        patch=create(a,z,('Liquid Crystal '+name).encode())
        if apply(a,patch)!=z:raise ValueError('BPS roundtrip failed: '+name)
        (folder/name).write_bytes(patch);patches[name]={'sha256':digest(patch),'bytes':len(patch),'input_sha256':digest(a),'output_sha256':digest(z)}
    manifest.update(patches=patches,deterministic_build_verified=True,bps_roundtrips_verified=True)
    (folder/'Liquid Crystal P002.gba').write_bytes(target)
    for path in (folder/'P002-manifest.json',ROOT/'extracted/builds/P002-manifest.json'):path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'rom_sha256':digest(target),'used':manifest['capacities_used'],'patches':patches},indent=2))


if __name__=='__main__':main()
