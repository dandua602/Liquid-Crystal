"""Read-only report for a 16/32 MiB cart dump after the failed hardware test."""
import argparse
import hashlib
import json
from pathlib import Path
from inspect_cartridge_save import audit
from verify_cartridge import readback_report

ROOT = Path(__file__).resolve().parents[1]


def report(reference, readback):
    if len(readback) not in (0x1000000, 0x2000000):
        raise ValueError('Expected a complete 16 or 32 MiB ROM dump')
    lower = readback[:0x1000000]
    result = {'readback_bytes': len(readback), 'full_readback_sha256': hashlib.sha256(readback).hexdigest(),
              'first_16MiB_comparison': readback_report(reference, lower, True),
              'embedded_save_audit_assuming_expected_game_layout': audit(reference, lower[0xC80000:0xCA0000]),
              'hardware_root_cause_proven': False,
              'limits': 'First 16 MiB compared explicitly with the shipped 16 MiB image. A 32 MiB dump is retained whole; upper-half hashes/shape do not certify board mapping or protocols.'}
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
    args = parser.parse_args()
    text = json.dumps(report(args.expected.read_bytes(), args.readback.read_bytes()), indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
