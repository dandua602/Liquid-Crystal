"""Save-window isolation and honest initial/after-play readback checks."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from cartridge_image import image_with_save
from verify_cartridge import readback_report


class CartridgeImageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
        cls.save = (ROOT/'saves/test/P002-cart-puzzle.sav').read_bytes()

    def test_only_embedded_payload_changes_footer_excluded(self):
        result = image_with_save(self.rom, self.save)
        self.assertEqual(result[:0xC80000], self.rom[:0xC80000])
        self.assertEqual(result[0xCA0000:], self.rom[0xCA0000:])
        self.assertEqual(result[0xC80000:0xCA0000], self.save)
        self.assertEqual(image_with_save(self.rom, self.save+b'footer-metadata!'), result)
        self.assertEqual(len(result), 0x1000000)

    def test_wrong_rom_bad_length_and_blank_saves_are_rejected(self):
        with self.assertRaises(ValueError):
            image_with_save(b'wrong ROM', self.save)
        for save in (self.save[:-1], self.save+bytes(17), bytes(0x20000), b'\xff'*0x20000):
            with self.assertRaises(ValueError):
                image_with_save(self.rom, save)

    def test_after_play_accepts_save_change_but_rejects_code_driver_and_size_changes(self):
        changed = image_with_save(self.rom, self.save)
        self.assertTrue(readback_report(changed, changed)['passed'])
        self.assertFalse(readback_report(self.rom, changed)['passed'])
        self.assertTrue(readback_report(self.rom, changed, True)['passed'])
        for at in (0xB9EF00, 0xC7213C):
            bad = bytearray(changed); bad[at] ^= 1
            self.assertFalse(readback_report(self.rom, bad, True)['passed'])
        with self.assertRaises(ValueError):
            readback_report(self.rom, changed[:-1], True)


if __name__ == '__main__':
    unittest.main()
