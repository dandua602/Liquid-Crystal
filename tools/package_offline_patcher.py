"""Make a downloadable patch-only offline browser tool; never publish ROM/save files."""
import base64
import hashlib
import json
import zipfile
from pathlib import Path
from bps_patch import create, apply

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = (ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
    target = (ROOT/'builds/cartridge/P002-warehouse-test.gba').read_bytes()
    evidence = json.loads((ROOT/'extracted/runtime/cartridge/summary.json').read_text())
    case = evidence['cases']['puzzle']
    if sha(source) != 'c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf' or sha(target) != case['image_sha256'] or not case['complete'] or not case['all_expectations_passed']:
        raise ValueError('Wrong source or untested target')
    patch = create(source, target, b'P002 warehouse hardware test; artificial native-stat party/progress; embedded save; not personal progress')
    if apply(source, patch) != target:
        raise ValueError('Patch roundtrip failed')
    start, end = 0xC80000, 0xCA0000
    source_cases = []
    for name, data in [('original upload', source),
                       ('P001', (ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes()),
                       ('P002', (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes())]:
        delta = create(data, target, b'P002 warehouse test; artificial test progress')
        if apply(data, delta) != target:
            raise ValueError('Source-specific patch failed: '+name)
        source_cases.append({'name': name, 'sha256': sha(data),
                             'gameSha256': sha(data[:start]+data[end:]),
                             'patchSha256': sha(delta), 'patchBase64': base64.b64encode(delta).decode()})
    config = {'sourceSha256': sha(source), 'targetSha256': sha(target),
              'sourceBytes': len(source), 'targetBytes': len(target),
              'outputName': 'P002-warehouse-test.gba', 'patchSha256': sha(patch),
              'patchBase64': base64.b64encode(patch).decode(), 'sources': source_cases,
              'saveStart': start, 'saveEnd': end, 'originalSaveSha256': sha(source[start:end]),
              'version': 2}
    html = (ROOT/'tools/cartridge_patcher.html').read_text().replace('__PATCH_DATA__', json.dumps(config))
    readme = '''LIQUID CRYSTAL — MAKE THE WAREHOUSE CARTRIDGE TEST ROM

1. Extract this ZIP.
2. Open Make-Test-ROM.html in Chrome, Edge or Firefox.
3. Choose the original upload, exact P001 or exact P002 ROM.
   A later cart dump is supported only when its game/driver bytes match one of
   those and you also select your original 5-badge .sav backup. The page checks
   that backup before normalizing the embedded save in a memory-only copy.
4. Click Create and download test ROM. Find P002-warehouse-test.gba in Downloads.
5. In FlashGBX use Write ROM and your existing correct cart profile, then verify.
6. Boot the console and Continue. You start beside the warehouse rock puzzle.

If automatic downloading does not start, click the visible Download ROM link.
If rejected, open File details and copy the size/hash for troubleshooting.

No Python or separate patcher installation needed. Everything runs offline on
your computer. No ROM or save file is uploaded. Original files are unchanged.

The output includes a separate artificial pre-puzzle save with six native-stat
level100 Pokemon, Iron Tail/Surf and the retained Old Key/door unlock. It is not
your personal progress. Face right/A for the rock; decline the battle to test
Save and power-off/reload. Then face left/A at the sign to retry the battle.
The test save is embedded: do not restore a separate save for this initial test.

Use the same compatible cartridge family/profile as the uploaded conversion.
Physical-console compatibility and chip timing still need your test. Full guide:
https://github.com/dandua602/Liquid-Crystal/blob/main/HARDWARE_TEST.md

The included P002-warehouse-test.bps is an alternative for a BPS patcher. Apply
it DIRECTLY to your original Liquid Crystal upload, not P001/P002 or FireRed.
The BPS and browser tool produce the exact same previously tested 16 MiB ROM.
This ZIP contains patches, the offline tool and instructions; no ROM/save files.
'''
    manifest = {k: v for k, v in config.items() if k not in ('patchBase64', 'sources')}
    manifest['sources'] = [{k: v for k, v in row.items() if k != 'patchBase64'} for row in source_cases]
    manifest.update(contains_rom_or_save=False, hardware_verified=False)
    files = {'Make-Test-ROM.html': html.encode(), 'P002-warehouse-test.bps': patch,
             'README.txt': readme.encode(), 'MANIFEST.json': (json.dumps(manifest, indent=2)+'\n').encode()}
    files['SHA256SUMS.txt'] = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(files.items())).encode()
    folder = ROOT/'patches/P002'; path = folder/'P002-easy-cartridge-test.zip'
    with zipfile.ZipFile(path, 'w') as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 20, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16; archive.writestr(info, data)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or any(n.endswith(('.gba', '.sav')) for n in archive.namelist()):
            raise ValueError('Invalid public ZIP')
    (folder/'P002-easy-cartridge-test-v2.zip').write_bytes(path.read_bytes())
    (ROOT/'extracted/builds/P002-offline-patcher-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'zip': str(path.relative_to(ROOT)), 'bytes': path.stat().st_size,
                      'patch_bytes': len(patch), 'target_sha256': sha(target)}, indent=2))


if __name__ == '__main__':
    main()
