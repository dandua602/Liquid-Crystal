"""Read-only report for a 16/32 MiB cart dump, including unknown conversions."""
import argparse
import hashlib
import json
from pathlib import Path
from inspect_cartridge_save import audit
from verify_cartridge import readback_report

ROOT = Path(__file__).resolve().parents[1]


def low_lane_bit6(reference, readback):
    """Flag a long varied-data suffix whose even bytes all have bit6 set.

    This is an observed pattern, not a diagnosis of a particular reader/chip.
    Uniform FF padding alone is deliberately excluded.
    """
    lane = readback[::2]
    last_clear = next((i for i in range(len(lane)-1, -1, -1) if not lane[i] & 0x40), -1)
    start = (last_clear+1)*2
    tail = readback[start:]
    varied = len(tail) >= 0x10000 and len(set(tail)) > 16
    ref_clear = sum(not value & 0x40 for value in reference[start::2])
    return {'mask': 0x0040, 'first_even_offset_after_last_clear': start,
            'suffix_bytes': len(tail), 'suffix_has_varied_data': varied,
            'reference_clear_words_in_suffix': ref_clear,
            'suspicious_pattern': varied and ref_clear >= 4096,
            'interpretation': 'A long varied-data suffix forces the low-byte bit high; not proof of stored-ROM corruption, transport error or a particular chip fault.'}


def report(reference, readback, save=None):
    if len(readback) not in (0x1000000, 0x2000000):
        raise ValueError('Expected a complete 16 or 32 MiB ROM dump')
    lower = readback[:0x1000000]
    try:
        actual_audit = audit(lower, lower[0xC80000:0xCA0000])
    except ValueError as error:
        actual_audit = {'native_layout_recognized': False, 'reason': str(error)}
    result = {'readback_bytes': len(readback), 'full_readback_sha256': hashlib.sha256(readback).hexdigest(),
              'first_16MiB_comparison': readback_report(reference, lower, True),
              'embedded_save_audit_assuming_expected_game_layout': audit(reference, lower[0xC80000:0xCA0000]),
              'actual_readback_native_layout_audit': actual_audit,
              'low_lane_bit6': low_lane_bit6(reference, lower),
              'hardware_root_cause_proven': False,
              'limits': 'First 16 MiB compared explicitly with the shipped 16 MiB image. A 32 MiB dump is retained whole; upper-half hashes/shape do not certify board mapping or protocols.'}
    if save is not None:
        result['separate_save_against_expected_layout'] = audit(reference, save)
        result['separate_save_matches_expected_embedded_payload'] = save[:0x20000] == reference[0xC80000:0xCA0000]
        result['separate_save_matches_readback_window'] = save[:0x20000] == lower[0xC80000:0xCA0000]
    if len(readback) == 0x2000000:
        upper = readback[0x1000000:]
        result['upper_16MiB'] = {'sha256': hashlib.sha256(upper).hexdigest(),
                                 'identical_to_lower_half': upper == lower,
                                 'all_ff': upper == b'\xff'*len(upper), 'all_zero': upper == bytes(len(upper))}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readback', type=Path)
    parser.add_argument('--expected', type=Path, default=ROOT/'builds/cartridge/P002-warehouse-test.gba')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--save', type=Path, help='Optional separate save; checked against expected LC layout, not proof of the unknown ROM format')
    args = parser.parse_args()
    text = json.dumps(report(args.expected.read_bytes(), args.readback.read_bytes(), args.save.read_bytes() if args.save else None), indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
