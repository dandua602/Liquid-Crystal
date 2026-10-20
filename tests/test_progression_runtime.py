"""Fixture isolation, native identities and retained progression observations."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from progression_runtime import context, flagwrite, map_geometry, setvar, validate_native, warp


class FixtureTests(unittest.TestCase):
    def test_stack_storage_rejects_calls_and_trailing_instructions(self):
        for script in (b'',b'\x00'*81,b'\x04'+struct.pack('<I',0x08AD344E),b'\x02\x02',b'\x16\x18'):
            with self.subTest(script=script), self.assertRaises(ValueError):context(script)

    def test_operand_bytes_are_not_mistaken_for_call_opcodes(self):
        script=setvar(0x5304,4)+flagwrite(0x504,True)+warp(6,23,16,5)+b'\x02'
        data=context(script)
        self.assertEqual(data[12:12+len(script)],script)
        self.assertEqual(struct.unpack_from('<I',data,8)[0],0x03000EBC)
        self.assertEqual(data[0],0)  # no return stack entries

    def test_goto_leaves_ram_before_any_rom_script_uses_stack(self):
        data=context(b'\x05'+struct.pack('<I',0x08AD344E))
        self.assertEqual(data[12:17],bytes.fromhex('05 4e 34 ad 08'))


class SuppliedProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.evidence=json.loads((ROOT/'extracted/runtime/progression/progression.json').read_text())
        cls.checks={row['label']:row for row in cls.evidence['checks']}

    def test_native_hook_identity_is_checked_before_reading_extended_state(self):
        validate_native(self.rom)
        changed=bytearray(self.rom);changed[0x7BADBC]^=1
        with self.assertRaises(ValueError):validate_native(changed)
        for row in self.evidence['native_variable_evidence']:
            self.assertEqual(bytes.fromhex(row['raw_hex']),self.rom[row['start']:row['end']])

    def test_ocean_layout_is_not_promoted_to_a_cave_door(self):
        rows=map_geometry(self.rom)
        self.assertEqual(rows,self.evidence['map_geometry'])
        by_map={row['map']:row for row in rows}
        self.assertEqual(by_map['3:111']['behavior_counts'],{'0x0':27,'0x15':1989})
        for name,expected in [('3:99',0x60),('3:111',0x15)]:
            tile=next(c for c in by_map[name]['key_cells'] if (c['x'],c['y'])==(33,18))
            self.assertEqual(tile['behavior'],expected)

    def test_completed_run_is_for_current_source_and_all_expectations_passed(self):
        self.assertTrue(self.evidence['complete'])
        self.assertTrue(self.evidence['source_unchanged'])
        self.assertEqual(self.evidence['source_sha256']['rom'],hashlib.sha256(self.rom).hexdigest())
        expectations=[r for r in self.evidence['checks'] if 'passed' in r]
        self.assertEqual(len(expectations),31)
        self.assertTrue(all(r['passed'] for r in expectations))
        self.assertIn('science_copied_warp_does_not_activate_on_ocean_tile',self.checks)
        for label in ['route54_101_loaded_header','route54_107_loaded_header','science_99_loaded_header','science_111_loaded_header']:
            self.assertTrue(self.checks[label]['live_matches_default_header'])
            self.assertEqual(self.checks[label]['live_layout'],self.checks[label]['default_layout']+0x08000000)

    def test_rejection_preserves_counter_and_escape_consumes_a_controller(self):
        rejected=self.checks['after_uncharged_controller']
        escaped=self.checks['after_escape_controller']
        self.assertEqual(rejected['variables']['0x5318'],11)
        self.assertEqual(rejected['flags'],{'0x544':1,'0x54B':0,'0x514':0})
        self.assertEqual(escaped['variables']['0x5318'],10)
        self.assertEqual(escaped['flags'],{'0x544':0,'0x54B':1,'0x514':0})
        self.assertEqual(self.checks['second_controller_accepts_without_recharge']['message_pointer'],0x08AD3BB4)

    def test_completion_boundary_is_observed_without_claiming_ten_wins(self):
        final=self.checks['completion_after_escape']
        self.assertEqual(final['variables']['0x5318'],1)
        self.assertEqual(final['flags']['0x514'],1)
        self.assertEqual(final['flags']['0x175A'],0)
        self.assertEqual(final['flags']['0x544'],0)


if __name__=='__main__':unittest.main()
