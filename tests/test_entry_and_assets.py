"""Native trainer ABI, earned transport state and inherited false script hits."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from map_extract import FormatError
from orange_progression_audit import decoder
from trainer_audit import discover,party,record
from progression_runtime import context,word

class TrainerFormatTests(unittest.TestCase):
    def test_no_item_party_uses_native_abi_padding_between_members(self):
        rom=struct.pack('<HBxH2x',100,90,25)+struct.pack('<HBxH2x',200,91,181)
        parsed=party(rom,0,2,0)
        self.assertEqual([r['species_id']for r in parsed],[25,181])
        self.assertEqual([r['offset']for r in parsed],[0,8])
        self.assertEqual([r['level']for r in parsed],[90,91])

    def test_custom_no_item_party_keeps_moves_and_trailing_padding(self):
        member=struct.pack('<HBxH4H2x',200,90,181,1,2,3,4)
        parsed=party(member*2,0,2,1)
        self.assertEqual([r['offset']for r in parsed],[0,16])
        self.assertEqual(parsed[1]['move_ids'],[1,2,3,4])
        with self.assertRaises(FormatError):party(member,0,2,1)
        with self.assertRaises(FormatError):party(member,0,7,1)

    def test_native_consumers_agree_and_wrong_party_pointer_is_rejected(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        table,consumers=discover(rom)
        self.assertEqual(table,0xABFD84);self.assertEqual(len(consumers),2)
        self.assertEqual(record(rom,table,837)['name'],'4 Mister G')
        self.assertEqual(record(rom,table,899)['name'],'Elite')
        changed=bytearray(rom);at=consumers[0]['literal_site'];changed[at:at+4]=struct.pack('<I',0x08000020)
        with self.assertRaises(FormatError):discover(changed)
        changed=bytearray(rom);at=table+837*40+36;changed[at:at+4]=b'\x00'*4
        with self.assertRaises(FormatError):record(changed,table,837)

    def test_no_named_future_team_is_invented_from_elite_or_failed_rows(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        data=json.loads((ROOT/'extracted/trainers/trainer_audit.json').read_text())
        self.assertEqual(data['source_sha256'],hashlib.sha256(rom).hexdigest())
        self.assertEqual(len(data['records'])+len(data['failed_candidate_rows']),1024)
        self.assertFalse(any('mister r'in n['name'].lower()or'rudy'in n['name'].lower()for n in data['bounded_name_candidates']))
        native=data['native_party_strides']
        self.assertEqual(bytes.fromhex(native['raw_hex']),rom[native['offset']:native['end_exclusive']])
        self.assertTrue(native['matches_reference']);self.assertEqual(native['stride_by_flags'],[8,16,8,16])

class EntryEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'extracted/runtime/entry/entry.json').read_text())
        cls.checks={c['label']:c for c in cls.data['checks']}

    def test_fresh_entry_replay_reaches_valencia_with_no_failed_expectation(self):
        self.assertTrue(self.data['complete']);self.assertTrue(self.data['source_unchanged'])
        digest=hashlib.sha256((ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()).hexdigest()
        self.assertEqual(self.data['source_sha256']['rom'],digest)
        checks=[c for c in self.data['checks']if'passed'in c]
        self.assertEqual(len(checks),18);self.assertTrue(all(c['passed']for c in checks))
        self.assertEqual(self.checks['valencia_port_reached']['actual'],[3,77])
        self.assertEqual(self.checks['non_electric_does_not_complete_trip']['actual'],0)
        self.assertEqual(self.checks['engine_restart_completes_trip']['actual'],1)

    def test_all_transitions_after_the_gate_are_earned_without_state_injection(self):
        warps=[];after_gate=False
        for row in self.data['transcript']:
            if not row['command'].startswith('w 3000eb0 '):continue
            script=bytes.fromhex(row['command'].split()[2])[12:92];pc=0
            while pc<len(script):
                node,error=decoder(script,pc);self.assertIsNone(error)
                if after_gate:self.assertIn(node['opcode'],{2,0x2B,0x7B})
                if node['opcode']==0x3D:
                    key=node['values'][:2];warps.append(key)
                    if key==[2,121]:after_gate=True
                if node['opcode']==2:break
                pc=node['end']
        self.assertEqual(warps,[[2,123],[4,88],[2,123],[2,121]])
        self.assertGreater(len(self.data['steps']),100)
        for label in ['oak_awards_orange_authorization','office_awards_stamp','kyogre_encounter_flag']:
            self.assertEqual(self.checks[label]['actual'],1)

    def test_party_creation_fixture_is_bounded_and_no_script_call_is_allowed(self):
        script=b'\x79'+word(181)+bytes([70])+word(0)+bytes(9)+b'\x02'
        self.assertEqual(context(script)[12:12+len(script)],script)
        for script in [script[:-3],b'\x04'+struct.pack('<I',0x08931413)]:
            with self.assertRaises(ValueError):context(script)
        fixture=self.checks['electric_party_fixture']
        self.assertEqual((fixture['species_id'],fixture['replaced_party_slot']),(181,5))
        self.assertIn('Artificial',fixture['warning'])

class MisterStateReviewTests(unittest.TestCase):
    def test_four_unresolved_raw_shapes_are_inherited_asset_bytes(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        reference=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        data=json.loads((ROOT/'extracted/scripts/mister_r_state_review.json').read_text())
        self.assertEqual(data['source_sha256'],hashlib.sha256(rom).hexdigest());self.assertEqual(data['allocations'],[])
        self.assertEqual({r['instruction']['pc']for r in data['reclassified_shapes']},{0x52AFF4,0x553EC9,0x611485,0x70EFA3})
        for row in data['reclassified_shapes']:
            asset=row['asset'];a=asset['start'];b=asset.get('end_exclusive',asset.get('end'))
            self.assertEqual(rom[a:b],reference[a:b]);self.assertTrue(row['matches_reference'])
            self.assertLessEqual(a,row['instruction']['pc']);self.assertGreaterEqual(b,row['instruction']['end'])

if __name__=='__main__':unittest.main()
