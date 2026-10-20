"""Prepare a copy of exact P002 with a supplied save in its existing NOR window.

For the same cartridge conversion as the uploaded ROM; no chip compatibility
claim. Writes a new output only. Does not flash hardware or alter source files.
"""
import argparse
import hashlib
from pathlib import Path
from save_hardware_audit import SIGNATURES, WINDOW

P002_SHA256 = '9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70'
PAYLOAD_SIZE = 0x20000
FLASHGBX_FOOTER_SIZE = 16


def image_with_save(rom, save):
    if hashlib.sha256(rom).hexdigest() != P002_SHA256:
        raise ValueError('Expected exact P002 ROM; patch your original with P002.bps first')
    if len(save) not in (PAYLOAD_SIZE, PAYLOAD_SIZE+FLASHGBX_FOOTER_SIZE):
        raise ValueError('Expected a 128 KiB save payload, optionally with its 16-byte FlashGBX footer')
    for address, expected in SIGNATURES.items():
        if rom[address:address+len(expected)] != expected:
            raise ValueError('Unexpected cartridge driver signature')
    payload = save[:PAYLOAD_SIZE]
    if payload in (bytes(PAYLOAD_SIZE), b'\xff'*PAYLOAD_SIZE):
        raise ValueError('Refusing an empty save')
    start, end = WINDOW
    result = rom[:start]+payload+rom[end:]
    if len(result) != len(rom) or result[:start] != rom[:start] or result[end:] != rom[end:]:
        raise ValueError('Write escaped the existing embedded save window')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('p002_rom', type=Path)
    parser.add_argument('save', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = image_with_save(args.p002_rom.read_bytes(), args.save.read_bytes())
    with args.output.open('xb') as stream:
        stream.write(result)
    print(f'Created {args.output.name}: {len(result)} bytes, SHA256 {hashlib.sha256(result).hexdigest()}')
    print('Only the embedded save payload was selected; cartridge driver and game code are unchanged.')


if __name__ == '__main__':
    main()
