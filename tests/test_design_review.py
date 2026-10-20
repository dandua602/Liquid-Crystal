"""Review evidence must reject changed native bounds and unsafe proposals."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from design_review_audit import audit
from space_ownership import native_bounds


class DesignReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.design=json.loads((ROOT/'research/design/p001.json').read_text())
        cls.geometry=json.loads((ROOT/'extracted/maps/mister_r_diagnosis.json').read_text())['geometry']
        cls.moves=(ROOT/'research/references/include__constants__moves.h').read_text()

    def test_inclusive_native_scan_and_forward_table_do_not_cross_window(self):
        rows=native_bounds(self.rom)
        self.assertEqual(rows['left_table']['scan_rows'],38)
        self.assertEqual(rows['left_table']['conservative_end_exclusive'],0xB9E138)
        self.assertEqual(rows['right_table']['minimum_address'],0xB9FEE0)
        changed=bytearray(self.rom);changed[0xBFC7C]=255
        with self.assertRaises(ValueError):native_bounds(changed)
        changed=bytearray(self.rom);changed[0xB9FFC0]^=1
        with self.assertRaises(ValueError):native_bounds(changed)

    def test_proposal_rejects_blocked_entry_or_colliding_object_id(self):
        for field,value in [('position',[12,14]),('local_id',1)]:
            changed=copy.deepcopy(self.design);changed['rock'][field]=value
            with self.assertRaises(ValueError):audit(changed,self.rom,self.geometry,self.moves)

    def test_review_text_party_and_table_capacities_are_real(self):
        result=audit(self.design,self.rom,self.geometry,self.moves)
        self.assertEqual(result['text_bytes'],402);self.assertEqual(result['event_table_bytes'],178)
        self.assertEqual(result['party_bytes'],96)
        changed=copy.deepcopy(self.design);changed['battle']['party'][0]['move_ids'][0]=1
        with self.assertRaises(ValueError):audit(changed,self.rom,self.geometry,self.moves)
        changed=copy.deepcopy(self.design);changed['hooks']['warp_init_condition_operands']=[0,0]
        with self.assertRaises(ValueError):audit(changed,self.rom,self.geometry,self.moves)

    def test_tagged_state_survives_actual_save_on_current_source(self):
        data=json.loads((ROOT/'extracted/runtime/design_state/design_state.json').read_text())
        self.assertTrue(data['complete']);self.assertTrue(data['source_unchanged'])
        self.assertEqual(data['source_sha256']['rom'],hashlib.sha256(self.rom).hexdigest())
        checks={c['label']:c for c in data['checks']if'passed'in c}
        self.assertTrue(all(c['passed']for c in checks.values()))
        self.assertEqual(checks['tagged_completed_state_survives_actual_save_reload']['actual'],0x3303)
        self.assertEqual(checks['frame_table_operand_3302_is_literal']['actual'],0x3302)
        self.assertEqual(checks['frame_table_operand_3303_is_literal']['actual'],0x3303)


if __name__=='__main__':unittest.main()
