"""Package tested P002 and its current player walkthrough; no ROMs/saves."""
import hashlib
import json
import zipfile
from pathlib import Path
from bps_patch import apply
ROOT=Path(__file__).resolve().parents[1]
CASES=('access','journey','matrix','puzzle','loss','exits','rollback')


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    folder=ROOT/'builds/dev';manifest=json.loads((folder/'P002-manifest.json').read_text())
    original=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();old=(folder/'Liquid Crystal P001.gba').read_bytes();target=(folder/'Liquid Crystal P002.gba').read_bytes()
    if (digest(original),digest(old),digest(target))!=(manifest['original_source_sha256'],manifest['input_p001_sha256'],manifest['output_sha256']):raise ValueError('Source/build mismatch')
    for name,a,z in [('P002.bps',original,target),('P002-reverse.bps',target,original),('P001-to-P002.bps',old,target),('P002-to-P001.bps',target,old)]:
        patch=(folder/name).read_bytes()
        if digest(patch)!=manifest['patches'][name]['sha256']or apply(a,patch)!=z:raise ValueError('Patch mismatch: '+name)
    cases={}
    for name in CASES:
        path=ROOT/f'extracted/runtime/p002/{name}/{name}.json';d=json.loads(path.read_text());checks=[c for c in d['checks']if'passed'in c]
        if not(d['complete']and d['source_unchanged']and d['rom_sha256']==digest(target)and checks and all(c['passed']for c in checks)):raise ValueError('Incomplete/stale P002 case: '+name)
        cases[name]={'artifact':str(path.relative_to(ROOT)),'sha256':digest(path.read_bytes()),'expectations':len(checks),'passed':True,'started_at_utc':d['started_at_utc']}
    tests=json.loads((ROOT/'extracted/runtime/validation_summary.json').read_text())['project_tests']
    if not(tests['run']>0 and tests['run']==tests['passed']and tests['failed']==0):raise ValueError('Project tests not passed')
    report={'id':'P002','output_sha256':digest(target),'runtime_acceptance':'passed','cases':cases,'expectations':sum(c['expectations']for c in cases.values()),'project_tests':tests,
            'walkthrough_sha256':digest((ROOT/'WALKTHROUGH.md').read_bytes()),'scope':'Approved Office service-room slice and affected warehouse behavior; includes P001.',
            'limits':['Forced research anchors/state/party; actual native victory, entry/return, game Save, fresh-process load and safe P001 downgrade tested.',
                      'Battle fixture is boosted generated Mewtwo, not human balance or ordinary continuous full-game playthrough.',
                      'No new Office quest, upper floors, city-front-door unlock, Route60, battle, badge/rank/item reward.',
                      'Unknown computed map/space users and hardware remain outside bounded certification; tested runtime uses the supplied-image mGBA adapter.',
                      'Exit map6:32 and save in original warehouse before downgrade/removal.']}
    report_text=json.dumps(report,indent=2)+'\n'
    (folder/'P002-validation.json').write_text(report_text);(ROOT/'extracted/builds/P002-validation.json').write_text(report_text)
    readme=f'''Liquid Crystal P002 — Office Block service-room prototype (includes P001)

Playable additions: warehouse Iron Tail/Rock Smash puzzle, approved Mister R
battle and Office service-room access after victory. Its southern door returns
to the warehouse. The main Office remains closed; no new reward or fight is added.
Read WALKTHROUGH.md for directions, screenshots, retries, saving and the endpoint.

Choose ONE installation path. Use a compatible BPS patcher or included Python3:

A. Exact original supplied Liquid Crystal ROM:
SHA256 {digest(original)}
python3 bps_patch.py "POKEMON Liquid Crystal.gba" P002.bps "Liquid Crystal P002.gba"

B. Exact P001 ROM:
SHA256 {digest(old)}
python3 bps_patch.py "Liquid Crystal P001.gba" P001-to-P002.bps "Liquid Crystal P002.gba"

Expected P002 SHA256:
{digest(target)}
Do not apply to vanilla FireRed. P002.bps already includes P001.
The applier refuses to overwrite an existing output. Preserve your original ROM
and save backups; use a working copy of your personal save with the new ROM.

ROLLBACK: first leave the service room, return to the warehouse and SAVE there.
A save left in P002-only map6:32 will not load in an original/P001-only ROM.
P002-to-P001.bps restores exact P001; P002-reverse.bps restores exact original.
For example:
python3 bps_patch.py "Liquid Crystal P002.gba" P002-to-P001.bps "Restored P001.gba"
An actual saved return to the warehouse was loaded successfully in fresh P001.

{tests['passed']} project tests and {report['expectations']} runtime expectations pass
across {len(cases)} cases, including actual six-opponent victory, P001 save upgrade,
new-map save/fresh reload, normal return, native whiteout and safe downgrade.
Earlier P001 archaeology/balance artifacts are retained, not claimed freshly
replayed. P002 also fixes a cleared-rock respawn on movement using existing
room-template coordinates; no new save field or flag is allocated.

This ROM preserves the supplied image's cartridge bank driver/embedded save;
it is tested with the project's mGBA0.10.5 adapter. Stock-emulator conversion,
hardware compatibility, full-game progression and human balance are unverified.
This ZIP contains patches, applier, manifests, guide and screenshots. No ROM/save.
'''
    (folder/'P002-README.txt').write_text(readme)
    files={name:(folder/name).read_bytes()for name in manifest['patches']}
    files.update({'README.txt':readme.encode(),'P002-manifest.json':(folder/'P002-manifest.json').read_bytes(),
                  'P002-validation.json':report_text.encode(),'bps_patch.py':(ROOT/'tools/bps_patch.py').read_bytes(),'WALKTHROUGH.md':(ROOT/'WALKTHROUGH.md').read_bytes()})
    for path in (ROOT/'walkthrough/images').iterdir():
        if path.suffix in ('.png','.svg'):files[str(path.relative_to(ROOT))]=path.read_bytes()
    output=ROOT/'builds/P002-prototype.zip'
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED)as archive:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,data)
    with zipfile.ZipFile(output)as archive:
        if archive.testzip()is not None or set(archive.namelist())!=set(files):raise ValueError('ZIP integrity failure')
    print(json.dumps({'package':str(output),'sha256':digest(output.read_bytes()),'rom_sha256':digest(target),'project_tests':tests['passed'],'runtime_expectations':report['expectations']},indent=2))


if __name__=='__main__':main()
