"""Create a native-stat warehouse test save and check actual embedded-save boot.

Disposable emulator checks for the uploaded cartridge conversion. No physical
cart access, flash-chip timing/ID certification or normal-playthrough claim.
"""
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from allocation_runtime import save_copy, trainer_flag
from cartridge_image import image_with_save, P002_SHA256
from p001_combat_probe import CombatJourney, TEAM
from p002_runtime import OfficeJourney, ROOT, ROM, FRONTEND, SOURCE_SAVE

OUT = ROOT/'extracted/runtime/cartridge'
FIXTURE = ROOT/'saves/test/P002-cart-puzzle.sav'


class HardwareJourney(OfficeJourney, CombatJourney):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare_fixture():
    output = OUT/'prepare'; output.mkdir(parents=True, exist_ok=True)
    seed = ROOT/'saves/test/linked-orange-fixture.sav'
    metadata = json.loads(seed.with_suffix('.json').read_text())
    if sha(seed.read_bytes()) != metadata['sha256']:
        raise ValueError('Changed linked progression fixture')
    p = None
    report = {'complete': False, 'seed_fixture_sha256': metadata['sha256'],
              'limits': 'Explicit native-generated level100 team replaces research party; original forced late-game anchors are inherited, not personal progress.'}
    try:
        with tempfile.TemporaryDirectory(prefix='lc-cart-prepare-') as directory:
            temp = Path(directory); shutil.copyfile(ROM, temp/'copy.gba'); shutil.copyfile(seed, temp/'copy.sav')
            p = HardwareJourney(FRONTEND, temp, output)
            try:
                p.boot({'x': 12, 'y': 14, 'group': 6, 'map': 31, 'warp': 0})
                p.expect('inherited_puzzle_pending', p.variable(0x5331), 1)
                p.expect('mister_r_not_defeated', trainer_flag(p, 929), 0)
                p.expect('inherited_old_key', p.has_item(0x116), 1)
                p.expect('inherited_door_unlocked', p.flag(0x5C1), 1)
                p.native_team(100); p.walk((14, 9))
                p.expect('rock_present_before_test', p.has_object(3), True)
                p.capture('warehouse_start'); save_copy(p)
                location = p.location(); shutil.copyfile(temp/'copy.sav', FIXTURE)
                report.update(complete=True, location=location, save_sha256=sha(FIXTURE.read_bytes()),
                              party=[{'name': name, 'species': species, 'moves': moves, 'level': 100} for name, species, moves in TEAM])
                FIXTURE.with_suffix('.json').write_text(json.dumps({
                    'kind': 'Artificial P002 cartridge test fixture, not personal progress',
                    'rom_sha256': P002_SHA256, 'sha256': report['save_sha256'],
                    'location': location, 'state': 'puzzle pending, Mister R unbeaten',
                    'party': report['party'], 'stats': 'Native-generated stats/PP, no cached 999 boosts; Lum Berries',
                    'prerequisites': 'Old Key and door unlock earned in the retained controlled linked replay; earlier starting map anchors were forced',
                    'source_save_unchanged': True}, indent=2)+'\n')
            finally:
                p.close()
    finally:
        if p:
            report.update(checks=p.checks, transcript=p.transcript)
        (output/'prepare.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def embedded_case(name, save, expected, state=None, save_reload=False):
    output = OUT/name; output.mkdir(parents=True, exist_ok=True)
    image = image_with_save(ROM.read_bytes(), save)
    report = {'complete': False, 'image_sha256': sha(image), 'embedded_save_sha256': sha(save[:0x20000]),
              'incoming_sram': '131072 FF bytes', 'boot_seed': 'Actual embedded ROM bytes, no adapter sidecar injection',
              'hardware_verified': False, 'save_reload_requested': save_reload}
    p = None
    try:
        with tempfile.TemporaryDirectory(prefix='lc-cart-boot-') as directory:
            temp = Path(directory); (temp/'copy.gba').write_bytes(image); (temp/'copy.sav').write_bytes(b'\xff'*0x20000)
            p = HardwareJourney(FRONTEND, temp, output)
            try:
                p.boot(expected); p.capture('embedded_boot')
                p.expect('boot_used_native_cartridge_bank_copy', p.command('m')['bank_selects'] > 0, True)
                if state is not None:
                    p.expect('embedded_room_state', p.variable(0x5331), state)
                if save_reload:
                    party = p.read(0x02024284, 600)
                    p.walk((14, 10)); location = p.location(); save_copy(p)
                    counters = p.command('m')
                    p.expect('native_save_programmed_embedded_nor', counters['nor_programs'] >= 65536, True)
                    p.expect('native_save_erased_embedded_nor', counters['nor_erases'] >= 2, True)
                    saved = (temp/'copy.sav').read_bytes(); history, checks, steps = p.transcript, p.checks, p.steps
                    p.close()
                    # Simulate a cart readback after its native NOR save; start
                    # a new process with that NOR and blank SRAM again.
                    (temp/'copy.gba').write_bytes(image_with_save(ROM.read_bytes(), saved))
                    (temp/'copy.sav').write_bytes(b'\xff'*0x20000)
                    p = HardwareJourney(FRONTEND, temp, output)
                    p.transcript, p.checks, p.steps = history, checks, steps
                    p.boot(location)
                    p.expect('saved_state_loaded_from_nor_in_new_process', p.variable(0x5331), state)
                    p.expect('native_party_survives_nor_reload', p.read(0x02024284, 600), party)
                    p.expect('saved_rock_remains_present', p.has_object(3), True)
                    p.capture('embedded_saved_reload')
                    report['save_reload_verified'] = True
                report['complete'] = True
            finally:
                p.close()
    finally:
        if p:
            report.update(checks=p.checks, transcript=p.transcript)
        (output/(name+'.json')).write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    originals = [ROOT/'roms/POKEMON Liquid Crystal.gba', SOURCE_SAVE, ROM]
    before = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in originals}
    if before[str(ROM.relative_to(ROOT))] != P002_SHA256:
        raise ValueError('Wrong P002')
    if 'LC_PROBE_ROM_SAVE_BOOT' in os.environ:
        raise RuntimeError('Run without a preexisting LC_PROBE_ROM_SAVE_BOOT variable')
    prepare = prepare_fixture()
    os.environ['LC_PROBE_ROM_SAVE_BOOT'] = '1'
    try:
        cases = {
            'personal': embedded_case('personal', SOURCE_SAVE.read_bytes(), {'x': 32, 'y': 29, 'group': 3, 'map': 62, 'warp': 4}),
            'puzzle': embedded_case('puzzle', FIXTURE.read_bytes(), prepare['location'], 1, True),
            'office': embedded_case('office', (ROOT/'saves/test/P002-office-fixture.sav').read_bytes(),
                                    {'x': 4, 'y': 7, 'group': 6, 'map': 32, 'warp': 255}, 0x3303)}
    finally:
        del os.environ['LC_PROBE_ROM_SAVE_BOOT']
    unchanged = all(sha((ROOT/path).read_bytes()) == digest for path, digest in before.items())
    if not unchanged:
        raise ValueError('Source changed')
    summary = {'complete': True, 'sources_unchanged': unchanged, 'source_sha256': before,
               'hardware_verified': False, 'prepare_artifact': 'extracted/runtime/cartridge/prepare/prepare.json',
               'cases': {name: {'image_sha256': r['image_sha256'], 'complete': r['complete'],
                                 'expectations': sum('passed' in c for c in r['checks']),
                                 'all_expectations_passed': all(c['passed'] for c in r['checks'] if 'passed' in c),
                                 'save_reload_verified': r.get('save_reload_verified', False),
                                 'artifact': f'extracted/runtime/cartridge/{name}/{name}.json'} for name, r in cases.items()},
               'limits': 'Software adapter checks native ROM-embedded boot with blank SRAM; observed AMD fallback only, no physical timing/flash-chip/controller certification.'}
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
