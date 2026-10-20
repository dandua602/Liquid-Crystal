"""Allocation screens must reject unsafe assumptions and stale native evidence."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from allocation_audit import guarded_windows,mirror_index,mirrored_target,native_evidence


class AllocationTests(unittest.TestCase):
    def test_all_rom_aliases_and_unaligned_words_are_screened(self):
        for high in range(8,14):
            self.assertEqual(mirrored_target((high<<24)+5,0x1000000),5)
        self.assertIsNone(mirrored_target(0x0E000005,0x1000000))
        rom=bytearray(b'\xff'*32);struct.pack_into('<I',rom,1,0x0C000005)
        self.assertIn({'site':1,'word':0x0C000005},mirror_index(rom)[5])

    def test_guarded_windows_exclude_targets_and_preserve_alignment(self):
        rom=b'\xff'*0x4000;windows=guarded_windows(rom,{0x2000:[]})
        self.assertEqual(len(windows),2)
        for w in windows:
            self.assertEqual(w['start']%4,0)
            self.assertGreaterEqual(w['bytes'],4096)
            self.assertTrue(w['end_exclusive']<=0x1F00 or w['start']>=0x2101)
            self.assertEqual(w['allocated_bytes'],0)

    def test_changed_native_bit_operation_rejects_evidence(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertTrue(native_evidence(rom))
        changed=bytearray(rom);changed[0x242CFE]^=1
        with self.assertRaises(ValueError):native_evidence(changed)
        changed=bytearray(rom);changed[0x15F9B4+4*0x61]^=1
        with self.assertRaises(ValueError):native_evidence(changed)

    def test_real_save_roundtrip_and_candidate_screen_match_current_source(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();digest=hashlib.sha256(rom).hexdigest()
        run=json.loads((ROOT/'extracted/runtime/allocation/allocation.json').read_text())
        self.assertTrue(run['complete']);self.assertTrue(run['source_unchanged'])
        self.assertEqual(run['source_sha256']['rom'],digest)
        checks={c['label']:c for c in run['checks']if'passed'in c}
        self.assertTrue(all(c['passed']for c in checks.values()))
        for key in ('trainer_defeated_bit_survives_game_save','room_value_two_survives_game_save','only_one_trainer_bit_byte_changes','ordinary_story_flag_is_independent'):
            self.assertIn(key,checks)
        self.assertTrue(any(r['response'].get('fresh_process')for r in run['transcript']if isinstance(r['response'],dict)))
        audit=json.loads((ROOT/'extracted/maps/allocation_audit.json').read_text())
        self.assertEqual(audit['source_sha256'],digest)
        candidate=audit['trainer_candidate'];self.assertTrue(candidate['row_all_zero'])
        self.assertEqual(candidate['direct_battle_command_hits'],[])
        for w in audit['rom_screen']['windows']:
            self.assertEqual(rom[w['start']:w['end_exclusive']],b'\xff'*w['bytes'])
            for a,b in audit['rom_screen']['protected_ranges']:
                self.assertFalse(w['start']<b and w['end_exclusive']>a)


if __name__=='__main__':unittest.main()
