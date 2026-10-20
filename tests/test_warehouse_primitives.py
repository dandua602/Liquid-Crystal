"""Native feasibility and allocation checks must reject false success."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from p001_preflight import START,END,budget_rows,screen_interval
from warehouse_primitives import native_evidence


class WarehousePrimitiveTests(unittest.TestCase):
    def test_native_outcome_reader_rejects_changed_ram_literal(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertTrue(native_evidence(rom))
        changed=bytearray(rom);changed[0xCA754]^=1
        with self.assertRaises(ValueError):native_evidence(changed)

    def test_guard_rejects_even_an_unaligned_mirror_shape(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertEqual(screen_interval(rom,{})['bytes'],2048)
        with self.assertRaises(ValueError):screen_interval(rom,{START-1:[{'site':3,'word':0x0AB9EEFF}]})
        changed=bytearray(rom);changed[START]=0
        with self.assertRaises(ValueError):screen_interval(changed,{})

    def test_budget_is_exact_and_actual_preflight_has_no_guard_hits(self):
        rows=budget_rows();self.assertEqual(rows[0]['start'],START);self.assertEqual(rows[-1]['end_exclusive'],END)
        self.assertEqual(sum(r['capacity_bytes']for r in rows),2048)
        data=json.loads((ROOT/'extracted/maps/p001_preflight.json').read_text())
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertEqual(data['source_sha256'],hashlib.sha256(rom).hexdigest())
        self.assertEqual(data['rom_proposal']['incoming_shape_hits'],[])
        self.assertEqual(data['trainer_row_proposal']['largest_bounded_script_id'],928)
        self.assertEqual(data['trainer_row_proposal']['direct_hits'],[])

    def test_existing_real_win_and_escape_are_distinguished(self):
        data=json.loads((ROOT/'extracted/runtime/warehouse_primitives/primitives.json').read_text())
        self.assertTrue(data['complete']);self.assertTrue(data['source_unchanged'])
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertEqual(data['source_sha256']['rom'],hashlib.sha256(rom).hexdigest())
        checks={c['label']:c for c in data['checks']if'passed'in c}
        self.assertTrue(all(c['passed']for c in checks.values()))
        for label,value in [('existing_laboratory_victory_outcome',1),('existing_controller_escape_outcome',4),
                            ('iron_tail_absent_returns_party_size',6),('iron_tail_first_slot_found',0),
                            ('iron_tail_sixth_slot_found',5),('native_move_check_accepts_fainted_knower',0)]:
            self.assertEqual(checks[label]['actual'],value)


if __name__=='__main__':unittest.main()
