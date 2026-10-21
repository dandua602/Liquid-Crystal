"""Compare two NOR erase geometries on disposable emulator copies.

This isolates an emulator assumption; it does not emulate chip IDs/timing or
prove the user's physical failure has the same cause. No replacement ROM.
"""
import json
import os
import tempfile
from pathlib import Path
from allocation_runtime import save_copy
from cartridge_runtime import HardwareJourney
from inspect_cartridge_save import audit
from p002_runtime import ROOT, FRONTEND


def main():
    for key in ('LC_PROBE_ROM_SAVE_BOOT', 'LC_PROBE_NOR_ERASE_BYTES'):
        if key in os.environ:
            raise RuntimeError('Unset '+key+' before this controlled comparison')
    results = {}
    output = ROOT/'extracted/runtime/cartridge/geometry'; output.mkdir(parents=True, exist_ok=True)
    image = (ROOT/'builds/cartridge/P002-warehouse-test.gba').read_bytes()
    for size in (65536, 131072):
        folder = output/str(size); folder.mkdir(exist_ok=True)
        result = {'erase_sector_bytes': size, 'physical_hardware_test': False}
        os.environ['LC_PROBE_ROM_SAVE_BOOT'] = '1'; os.environ['LC_PROBE_NOR_ERASE_BYTES'] = str(size)
        p = None
        try:
            with tempfile.TemporaryDirectory(prefix='lc-nor-geometry-') as directory:
                temp = Path(directory); (temp/'copy.gba').write_bytes(image); (temp/'copy.sav').write_bytes(b'\xff'*0x20000)
                p = HardwareJourney(FRONTEND, temp, folder)
                try:
                    p.boot({'x': 14, 'y': 9, 'group': 6, 'map': 31, 'warp': 0})
                    p.walk((14, 10)); save_copy(p)
                    result['save_returned_to_field'] = p.field_ready()
                except Exception as error:
                    result['error'] = f'{type(error).__name__}: {error}'
                finally:
                    result['mapper'] = p.command('m')
                    result['save_audit'] = audit(image, (temp/'copy.sav').read_bytes())
                    p.capture('after_save'); p.close()
        finally:
            if p:
                result.update(checks=p.checks, transcript=p.transcript)
            del os.environ['LC_PROBE_ROM_SAVE_BOOT']; del os.environ['LC_PROBE_NOR_ERASE_BYTES']
        (folder/'geometry.json').write_text(json.dumps(result, indent=2)+'\n')
        results[str(size)] = {k: result.get(k) for k in ('error', 'save_returned_to_field', 'mapper')}
        results[str(size)]['all_28_save_sections_valid'] = result['save_audit']['all_28_sections_valid']
    report = {'complete': True, 'cases': results,
              'limits': 'Only erase alignment/size varies. Same simplified AMD command handling and SRAM bank model; no actual chip-ID/timing/board certification. A model failure is not proof of the physical root cause.'}
    (output/'summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
