"""Compare a cart ROM readback with its flashed image; no hardware writes."""
import argparse
import hashlib
import json
from pathlib import Path
from save_hardware_audit import WINDOW


def readback_report(reference, readback, after_play=False):
    if len(reference) != 0x1000000 or len(readback) != len(reference):
        raise ValueError('Expected two full 16 MiB ROM images')
    start, end = WINDOW
    exact = reference == readback
    outside = reference[:start] == readback[:start] and reference[end:] == readback[end:]
    return {'passed': outside if after_play else exact,
            'mode': 'after_play_allow_embedded_save_changes' if after_play else 'initial_flash_exact',
            'exact_match': exact, 'game_and_cartridge_driver_match': outside,
            'embedded_save_changed': reference[start:end] != readback[start:end],
            'reference_sha256': hashlib.sha256(reference).hexdigest(),
            'readback_sha256': hashlib.sha256(readback).hexdigest(),
            'allowed_save_window': {'start': start, 'end_exclusive': end}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path)
    parser.add_argument('readback', type=Path)
    parser.add_argument('--after-play', action='store_true')
    args = parser.parse_args()
    report = readback_report(args.reference.read_bytes(), args.readback.read_bytes(), args.after_play)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
