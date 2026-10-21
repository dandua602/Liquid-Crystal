"""Package private cartridge ROM/save images and a separate public helper kit."""
import hashlib
import json
import zipfile
from pathlib import Path
from cartridge_image import image_with_save, P002_SHA256

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_zip(path, files):
    with zipfile.ZipFile(path, 'w') as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(files):
            raise ValueError('ZIP integrity failure')


def main():
    target = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    if sha(target) != P002_SHA256:
        raise ValueError('Changed P002')
    report = json.loads((ROOT/'extracted/runtime/cartridge/summary.json').read_text())
    if not report['complete'] or not report['sources_unchanged'] or report['hardware_verified']:
        raise ValueError('Incomplete or misleading runtime report')
    tests = json.loads((ROOT/'extracted/runtime/validation_summary.json').read_text())['project_tests']
    if tests['failed'] or tests['run'] != tests['passed'] or tests['passed'] < 155:
        raise ValueError('Project checks not complete')
    private, variants = {}, {}
    folder = ROOT/'builds/cartridge'; folder.mkdir(parents=True, exist_ok=True)
    cases = [('personal', 'P002-personal-5badge', ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'),
             ('puzzle', 'P002-warehouse-test', ROOT/'saves/test/P002-cart-puzzle.sav'),
             ('office', 'P002-office-test', ROOT/'saves/test/P002-office-fixture.sav')]
    for case, name, save in cases:
        payload = save.read_bytes()[:0x20000]; image = image_with_save(target, save.read_bytes())
        result = report['cases'][case]
        if not result['complete'] or not result['all_expectations_passed'] or result['image_sha256'] != sha(image):
            raise ValueError('Image not tested: '+case)
        evidence = json.loads((ROOT/result['artifact']).read_text())
        if not evidence['complete'] or evidence['embedded_save_sha256'] != sha(payload):
            raise ValueError('Stale embedded save evidence: '+case)
        private[name+'.gba'] = image; private[name+'.sav'] = payload
        (folder/(name+'.gba')).write_bytes(image); (folder/(name+'.sav')).write_bytes(payload)
        variants[name+'.gba'] = {'bytes': len(image), 'sha256': sha(image), 'save_sha256': sha(payload),
                                 'runtime_case': case, 'only_changed_range_from_P002': [0xC80000, 0xCA0000] if image != target else [],
                                 'artificial_test_save': case != 'personal'}
    manifest = {'id': 'P002-cartridge-test', 'game_base_sha256': P002_SHA256, 'hardware_verified': False,
                'images': variants, 'project_tests': tests, 'emulator_expectations': sum(r['expectations'] for r in report['cases'].values()),
                'save_mode': 'Existing embedded NOR save; original cartridge conversion retained',
                'original_inputs_unchanged': True, 'private_bundle_contains_rom_and_save': True,
                'public_helper_kit_contains_rom_or_save': False}
    if (ROOT/'extracted/runtime/cartridge/hardware_failure_audit.json').exists():
        manifest['hardware_status'] = 'User reported corruption/previous-save boot warning and stuck Saving; root cause unresolved'
    common = {'HARDWARE_TEST.md': (ROOT/'HARDWARE_TEST.md').read_bytes(),
              'WALKTHROUGH.md': (ROOT/'WALKTHROUGH.md').read_bytes(),
              'MANIFEST.json': (json.dumps(manifest, indent=2)+'\n').encode(),
              'VALIDATION.json': (ROOT/'extracted/runtime/cartridge/summary.json').read_bytes(),
              'extracted/runtime/cartridge/summary.json': (ROOT/'extracted/runtime/cartridge/summary.json').read_bytes(),
              'screenshots/warehouse-start.png': (ROOT/'extracted/runtime/cartridge/prepare/warehouse_start.png').read_bytes()}
    for name in ('cartridge_image.py', 'verify_cartridge.py', 'save_hardware_audit.py', 'bps_patch.py'):
        common[name] = (ROOT/'tools'/name).read_bytes()
    for image in (ROOT/'walkthrough/images').iterdir():
        if image.suffix in ('.png', '.svg'):
            common[str(image.relative_to(ROOT))] = image.read_bytes()
    # This link refers to the public download, not a recursive ZIP inside itself.
    guide = common['HARDWARE_TEST.md'].decode().replace('](patches/P002/P002-cartridge-tools.zip)',
             '](https://github.com/dandua602/Liquid-Crystal/blob/main/patches/P002/P002-cartridge-tools.zip)')
    guide = guide.replace('](patches/P002/P002-easy-cartridge-test.zip)',
             '](https://github.com/dandua602/Liquid-Crystal/blob/main/patches/P002/P002-easy-cartridge-test.zip)')
    guide = guide.replace('](patches/P002/P002-easy-cartridge-test-v2.zip)',
             '](https://github.com/dandua602/Liquid-Crystal/blob/main/patches/P002/P002-easy-cartridge-test-v2.zip)')
    guide = guide.replace('](patches/P002/P002-easy-cartridge-test-v3.zip)',
             '](https://github.com/dandua602/Liquid-Crystal/blob/main/patches/P002/P002-easy-cartridge-test-v3.zip)')
    common['HARDWARE_TEST.md'] = guide.encode()
    private.update(common)
    private['SHA256SUMS.txt'] = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(private.items())).encode()
    private_zip = ROOT/'builds/P002-cartridge-test.zip'; write_zip(private_zip, private)
    public = dict(common)
    with zipfile.ZipFile(ROOT/'patches/P002/P002-prototype.zip') as archive:
        public['P002.bps'] = archive.read('P002.bps')
    if any(name.lower().endswith(('.gba', '.sav')) for name in public):
        raise ValueError('Private content in public kit')
    public['SHA256SUMS.txt'] = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(public.items())).encode()
    public_zip = ROOT/'patches/P002/P002-cartridge-tools.zip'; write_zip(public_zip, public)
    (ROOT/'extracted/builds/P002-cartridge-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'private_zip': str(private_zip.relative_to(ROOT)), 'private_bytes': private_zip.stat().st_size,
                      'private_sha256': sha(private_zip.read_bytes()), 'public_zip': str(public_zip.relative_to(ROOT)),
                      'public_bytes': public_zip.stat().st_size, 'hardware_verified': False}, indent=2))


if __name__ == '__main__':
    main()
