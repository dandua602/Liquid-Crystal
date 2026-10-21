"""Native LC sector lengths distinguish valid data from actual corruption."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from inspect_cartridge_save import audit


class NativeSaveAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
        cls.save = (ROOT/'saves/test/P002-cart-puzzle.sav').read_bytes()

    def test_both_native_slots_validate_and_each_single_sector_corruption_is_detected(self):
        self.assertTrue(audit(self.rom, self.save)['all_28_sections_valid'])
        for sector in range(28):
            changed = bytearray(self.save); changed[sector*4096] ^= 1
            report = audit(self.rom, changed)
            self.assertFalse(report['all_28_sections_valid'])
            bad = [row['physical_sector'] for slot in report['slots'] for row in slot['sections'] if not row['valid']]
            self.assertEqual(bad, [sector])

    def test_rejects_unknown_layout_and_reports_driver_difference(self):
        wrong = bytearray(self.rom); wrong[0x3FEC94] ^= 1
        with self.assertRaises(ValueError):
            audit(wrong, self.save)
        wrong = bytearray(self.rom); wrong[0xC7213C] ^= 1
        report = audit(wrong, self.save)
        self.assertTrue(report['all_28_sections_valid'])
        self.assertFalse(report['driver_signatures_match'])


if __name__ == '__main__':
    unittest.main()
