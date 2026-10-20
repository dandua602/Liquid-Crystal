"""Package P001 only when retained acceptance matches the exact built ROM."""
import hashlib
import json
import zipfile
from pathlib import Path
from bps_patch import apply
ROOT=Path(__file__).resolve().parents[1]
CASES=('matrix','puzzle','win','loss','persistence','exits','edge','regression','regions')


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    folder=ROOT/'builds/dev';source=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();target=(folder/'Liquid Crystal P001.gba').read_bytes()
    manifest=json.loads((folder/'P001-manifest.json').read_text())
    if digest(source)!=manifest['source_sha256']or digest(target)!=manifest['output_sha256']:raise ValueError('Build/source mismatch')
    if apply(source,(folder/'P001.bps').read_bytes())!=target or apply(target,(folder/'P001-reverse.bps').read_bytes())!=source:raise ValueError('Patch roundtrip failed')
    results={}
    for case in CASES:
        path=ROOT/f'extracted/runtime/p001/{case}/{case}.json';data=json.loads(path.read_text());checks=[r for r in data['checks']if 'passed'in r]
        if not(data['complete']and data['source_unchanged']and checks and all(r['passed']for r in checks)and data['rom_sha256']==digest(target)):raise ValueError('Incomplete/stale runtime acceptance: '+case)
        results[case]={'artifact':str(path.relative_to(ROOT)),'artifact_sha256':digest(path.read_bytes()),'expectations':len(checks),'passed':True,'started_at_utc':data['started_at_utc']}
    native={}
    for level in (95,100):
        path=ROOT/f'extracted/runtime/p001/combat_native_{level}/combat.json';data=json.loads(path.read_text());checks=[r for r in data['checks']if'passed'in r]
        if not(data['complete']and data['source_unchanged']and checks and all(r['passed']for r in checks)and data['rom_sha256']==digest(target)and data['outcome']in (1,2)):raise ValueError('Incomplete/stale native-stat combat probe')
        native[str(level)]={'artifact':str(path.relative_to(ROOT)),'artifact_sha256':digest(path.read_bytes()),'expectations':len(checks),'outcome':data['outcome'],'passed':True}
    tests=json.loads((ROOT/'extracted/runtime/validation_summary.json').read_text())['project_tests']
    if not(tests['run']>0 and tests['run']==tests['passed']and tests['failed']==0):raise ValueError('Project tests have not passed')
    primary_count=sum(r['expectations']for r in results.values());native_count=sum(r['expectations']for r in native.values())
    validation={'id':'P001','output_sha256':digest(target),'runtime_acceptance':'passed','cases':results,'native_stat_probes':native,'primary_expectations':primary_count,'native_stat_expectations':native_count,'expectations':primary_count+native_count,'project_tests':tests,
                'limits':['Controlled entry/state/party fixtures on disposable copies; not an ordinary full-game playthrough.',
                          'Primary victory coverage uses boosted Mewtwo; additional native-stat level95 loss and level100 victory use six generated members without boosts/PP refills. Simple first-move button policy; human balance unverified.',
                          'Nonwin continuation checked directly using an actual existing wild-battle escape outcome; Mister R is an ordinary trainer battle.',
                          'Johto/Kanto controls cover forced-entry field walking/header checks only.',
                          'Supplied-image cartridge adapter required for tested runtime; hardware and independent fresh-task restoration unverified.',
                          'Prototype ends at this warehouse encounter; later islands/continuation remain future work.']}
    report=json.dumps(validation,indent=2)+'\n';(folder/'P001-validation.json').write_text(report)
    (ROOT/'extracted/builds/P001-validation.json').write_text(report)
    readme=f'''Liquid Crystal P001 — approved newly authored warehouse prototype

Adds the Iron Tail / Rock Smash boulder puzzle and six-member Mister R battle.
Keeps the original intro, damaged sign, exits and earlier game data. No new
onward area or quest reward is added. Full game completion remains future work.

Apply P001.bps to the exact supplied POKEMON Liquid Crystal.gba (16 MiB):
SHA256 {digest(source)}
Expected patched SHA256:
{digest(target)}
Do not apply it to vanilla FireRed. P001-reverse.bps restores the exact input ROM.

Use a standard BPS patcher, or the included Python 3 script:
python3 bps_patch.py "POKEMON Liquid Crystal.gba" P001.bps "Liquid Crystal P001.gba"
python3 bps_patch.py "Liquid Crystal P001.gba" P001-reverse.bps "Restored Liquid Crystal.gba"
The script refuses to overwrite an existing output.

Keep an untouched backup of your original save. Work with a copy. This patch
preserves the source ROM's cartridge bank driver and embedded save bytes; it
does not convert that image to a stock FireRed flash profile. Runtime acceptance
uses the project's mGBA 0.10.5 supplied-image adapter. Hardware is untested.

Warehouse: after the existing introduction, interact with the boulder using a
party member that knows Iron Tail (or Rock Smash). Declining the battle allows
retry from the damaged sign. Save normally; solved/completed states persist.
Legacy unowned state values recover without falsely recording a victory.

Validation: {primary_count} passing primary expectations across {len(results)} cases,
plus {native_count} native-stat combat checks (level95 loss, level100 victory);
{tests['passed']} project tests. Actual six-opponent victory, whiteout/retry, original
intro, move checks, exits, interrupted attempt and fresh-process save reload pass.
Native battle mode 1 supplies the post-battle continuation needed for exact-win
gating (reviewed mode 0 ends the script). Team and ordinary single combat remain
as approved. Native-stat probes use six generated members and ordinary HP/stats/PP;
the simple first-move button policy does not certify human battle balance.

This ZIP contains patches, the applier, manifests and this README. No ROM/save
is included. Read WALKTHROUGH.md for player instructions, the Route59 approach
diagram, puzzle screenshots, battle retries and the exact P001 endpoint.
walkthrough/P002-preview.md retains the historical next-chapter review proposal.
P002 is available separately; this package remains the P001-only version.
Full research and reproducible tools remain in the workspace.
'''
    (folder/'P001-README.txt').write_text(readme)
    files={'P001.bps':(folder/'P001.bps').read_bytes(),'P001-reverse.bps':(folder/'P001-reverse.bps').read_bytes(),
           'P001-manifest.json':(folder/'P001-manifest.json').read_bytes(),'P001-validation.json':report.encode(),
           'README.txt':readme.encode(),'bps_patch.py':(ROOT/'tools/bps_patch.py').read_bytes()}
    # Preserve version-correct instructions when the root guide advances.
    files['WALKTHROUGH.md']=(ROOT/'walkthrough/P001.md').read_text().replace('](images/','](walkthrough/images/').encode()
    for name in ('walkthrough/P002-preview.md','walkthrough/images/route59.svg','walkthrough/images/rock-prompt.png',
                 'walkthrough/images/mister-r-challenge.png','walkthrough/images/retry-sign.png','walkthrough/images/warehouse-complete.png'):
        files[name]=(ROOT/name).read_bytes()
    output=ROOT/'builds/P001-prototype.zip'
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED)as archive:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,data)
    with zipfile.ZipFile(output)as archive:
        if archive.testzip()is not None:raise ValueError('ZIP integrity failure')
        if set(archive.namelist())!=set(files):raise ValueError('Unexpected ZIP contents')
    print(json.dumps({'package':str(output),'package_sha256':digest(output.read_bytes()),'runtime_expectations':validation['expectations'],'project_tests':tests['passed'],'rom_sha256':digest(target)},indent=2))


if __name__=='__main__':main()
