"""Keep unknown cart conversions inspectable without endorsing damaged reads."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from inspect_cartridge_readback import low_lane_bit6, report


class ReadbackDiagnosticsTests(unittest.TestCase):
    def test_fixed_low_bit_in_varied_data_is_flagged_but_ff_padding_is_not(self):
        reference = bytearray(bytes(range(256))*1024)
        reference[0xFFFE] = 0
        changed = bytearray(reference)
        for offset in range(0x10000, len(changed), 2):
            changed[offset] |= 0x40
        observed = low_lane_bit6(reference, changed)
        self.assertTrue(observed['suspicious_pattern'])
        self.assertEqual(observed['first_even_offset_after_last_clear'], 0x10000)
        self.assertFalse(low_lane_bit6(reference, reference)['suspicious_pattern'])
        self.assertFalse(low_lane_bit6(reference, b'\xff'*len(reference))['suspicious_pattern'])

    def test_unknown_layout_is_reported_and_separate_save_is_not_called_current_progress(self):
        reference = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
        save = reference[0xC80000:0xCA0000]
        changed = bytearray(reference)
        changed[0x3FEC94] ^= 1
        result = report(reference, changed, save)
        self.assertFalse(result['actual_readback_native_layout_audit']['native_layout_recognized'])
        self.assertTrue(result['separate_save_against_expected_layout']['all_28_sections_valid'])
        self.assertTrue(result['separate_save_matches_expected_embedded_payload'])
        self.assertFalse(result['first_16MiB_comparison']['game_and_cartridge_driver_match'])
        self.assertFalse(result['hardware_root_cause_proven'])


if __name__ == '__main__':
    unittest.main()
