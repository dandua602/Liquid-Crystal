"""Compile a review-only P003 sizing preview; never writes a ROM or patch."""
import hashlib
import json
from pathlib import Path
from build_p001 import Assembler, BASE, h, w
from gba_text_codec import encode
from allocation_audit import mirror_index
from p001_preflight import screen_interval
from space_ownership import native_bounds

ROOT = Path(__file__).resolve().parents[1]
DIGEST = '9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70'
START, TEXT, END = 0xB9F800, 0xB9F8C0, 0xB9FA00
HOOK, VISIBILITY = 0xB9F6C4, 0xC0B550


def preflight(rom, design):
    if hashlib.sha256(rom).hexdigest() != DIGEST or design['input_rom_sha256'] != DIGEST:
        raise ValueError('Wrong P002 input')
    if design['gate'] != {'variable': 0x5331, 'value': 0x3303, 'trainer_id': 929, 'trainer_bit_required': True}:
        raise ValueError('Unsafe completion gate')
    if design['aftermath_flag'] != 0x5B2:
        raise ValueError('Unreviewed state change')
    if rom[START:END] != b'\xff' * (END-START):
        raise ValueError('Candidate is not pristine')
    if rom[HOOK:HOOK+4] != w(BASE+0xB9F52C) or rom[VISIBILITY:VISIBILITY+2] != bytes(2):
        raise ValueError('Unexpected hook bytes')
    addresses, texts = {}, bytearray()
    for key in ('locked', 'prompt', 'shutdown', 'repeat', 'decline'):
        addresses[key] = TEXT + len(texts)
        texts += b'\xfe'.join(encode(s) for s in design['messages'][key].split('\n')) + b'\xff'
    a = Assembler(START)
    a.label('attendant'); a.emit(0x69)
    a.cmp(0x5331, 0x3303, 'locked', 5)
    a.emit(0x60, h(929)); a.jump('locked', 0)
    a.emit(0x2B, h(0x5B2)); a.jump('repeat', 1)
    a.msg(addresses['prompt'], False); a.emit(0x6E, b'\x14\x08')
    a.cmp(0x800D, 0, 'decline')
    a.emit(0x29, h(0x5B2)); a.msg(addresses['shutdown']); a.jump('finish')
    for key in ('locked', 'repeat', 'decline'):
        a.label(key); a.msg(addresses[key]); a.jump('finish')
    a.label('finish'); a.emit(0x6B); a.emit(0x02)
    code = a.resolve()
    if len(code) > TEXT-START or len(texts) > END-TEXT:
        raise ValueError('P003 capacity overflow')
    return {'id': 'P003', 'status': 'DESIGN_FOR_REVIEW_NOT_IMPLEMENTED',
            'input_rom_sha256': DIGEST, 'no_ROM_output_created': True,
            'used': {'scripts': len(code), 'text': len(texts)},
            'capacities': {'scripts': TEXT-START, 'text': END-TEXT},
            'scripts_hex': code.hex(), 'text_hex': texts.hex(),
            'script_labels': a.labels, 'text_addresses': addresses,
            'external_writes_proposed': [
                {'site': HOOK, 'before_hex': rom[HOOK:HOOK+4].hex(), 'after_hex': w(BASE+START).hex(), 'role': 'Office attendant script pointer'},
                {'site': VISIBILITY, 'before_hex': '0000', 'after_hex': h(0x5B2).hex(), 'role': 'Center local4 disappears on aftermath flag'}],
            'state_write': {'ordinary_flag': 0x5B2, 'newly_authored_trigger': True},
            'limits': 'Sizing preview only. No P003 runtime acceptance or approval; existing flag readers have wider effects, with computed/native consumers unresolved.'}


def main():
    rom = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    design = json.loads((ROOT/'research/design/p003.json').read_text())
    preview = preflight(rom, design)
    screen = screen_interval(rom, mirror_index(rom), START, END, 256)
    screen['expected_bytes'] = 'FF repeated 512 times'
    screen['input_rom_sha256'] = DIGEST
    screen['native_bounds'] = native_bounds(rom)
    bounds = screen['native_bounds']
    if not bounds['left_table']['conservative_end_exclusive'] < START-256 < END+256 < bounds['right_table']['minimum_address']:
        raise ValueError('Native table bounds cross guarded proposal')
    screen['limits'] = 'Bounded signatures and alias shapes; unknown computed references, hidden extents and hardware remain unverified. No allocation implemented.'
    (ROOT/'extracted/maps/p003_space_preview.json').write_text(json.dumps(screen, indent=2)+'\n')
    (ROOT/'extracted/maps/p003_design_preflight.json').write_text(json.dumps(preview, indent=2)+'\n')
    print(json.dumps({k: preview[k] for k in ('status', 'used', 'capacities', 'no_ROM_output_created')}, indent=2))


if __name__ == '__main__':
    main()
