"""Native combat evidence and preservation failures in the next design preview."""
import copy
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from p002_design import preflight


class NextSliceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes()
        cls.design=json.loads((ROOT/'research/design/p002.json').read_text())

    def test_native_stats_combat_can_win_and_lose_without_false_completion(self):
        for level,outcome in [(95,2),(100,1)]:
            data=json.loads((ROOT/f'extracted/runtime/p001/combat_native_{level}/combat.json').read_text())
            self.assertTrue(data['complete']);self.assertTrue(data['source_unchanged'])
            self.assertEqual(data['rom_sha256'],hashlib.sha256(self.rom).hexdigest());self.assertEqual(data['outcome'],outcome)
            self.assertTrue(all(c['passed']for c in data['checks']if'passed'in c))
            party=next(c['members']for c in data['checks']if c['label']=='explicit_native_stat_party_fixture')
            self.assertEqual(len(party),6)
            self.assertTrue(all(m['level']==level and max(m['hp_maxhp_atk_def_speed_spatk_spdef'])<500 for m in party))
            self.assertFalse(any(c['label']=='battle_pp_refill_fixture'for c in data['checks']))

    def test_preview_preserves_every_bank_word_and_uses_matching_shared_layout(self):
        result=preflight(self.rom,self.design);table=bytes.fromhex(result['tables_hex'])
        bank=self.design['group_bank'];self.assertEqual(table[:128],self.rom[bank['old_bank']:bank['old_bank']+128])
        self.assertEqual(struct.unpack_from('<I',table,128)[0],0x08000000+self.design['new_room']['header'])
        self.assertEqual(struct.unpack_from('<I',table,132)[0],0x08000000+result['shared_donor_layout'])
        self.assertEqual([r['map']for r in result['legacy_unresolved_headers']],[4,6])
        self.assertTrue(all(result['used'][n]<=result['capacities'][n]for n in result['used']))

    def test_preview_rejects_wrong_input_unsafe_gate_reused_map_and_overflow(self):
        with self.assertRaises(ValueError):preflight(b'wrong ROM',self.design)
        for path,value in [(('entry','gate'),{'variable':0x5331,'value':3,'trainer_id':929,'trainer_bit_required':False}),
                           (('new_room','map'),[6,31]),(('entry','prompt'),'X'*180)]:
            changed=copy.deepcopy(self.design);changed[path[0]][path[1]]=value
            with self.assertRaises(ValueError):preflight(self.rom,changed)


if __name__=='__main__':unittest.main()
