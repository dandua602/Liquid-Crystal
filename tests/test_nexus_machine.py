"""Nexus state-operand, controller-family and engine-reference regressions."""
import hashlib,json,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from engine_reference_probe import make_probe

class DiscoveryTests(unittest.TestCase):
    def test_handler_table_is_found_independently_after_relocation(self):
        def fixture(table):
            rom=bytearray(b'\xff'*0x3000)
            rom[0x100:0x108]=b'\x00\x20\x70\x47'*2
            words=[0x08000101,0x08000105]+[0x08000109]*211
            rom[table:table+852]=struct.pack('<'+'I'*213,*words)
            return rom
        result=make_probe(fixture(0x500),fixture(0x1000),{0,1})
        self.assertEqual(result['selected_tables'],{'firered':'0x500','liquid_crystal':'0x1000'})
        self.assertTrue(all(r['compared_bytes_equal'] for r in result['handler_comparisons']))

class NexusRomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'extracted/text/nexus_machine_audit.json').read_text())
        cls.probe=json.loads((ROOT/'extracted/pointers/engine_handler_probe.json').read_text())
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.nodes={n['pc']:n for c in cls.data['clusters'] for n in c['instructions']}
        cls.messages={m['offset']:m for c in cls.data['clusters'] for m in c['messages']}

    def test_ten_distinct_controllers_preserve_their_own_flags(self):
        controllers=self.data['controller_scripts']
        self.assertEqual(len(controllers),10)
        self.assertEqual({c['state_flag'] for c in controllers},set(range(0x54B,0x555)))
        for c in controllers:
            self.assertIsNotNone(c['flag_write_offset'])
            self.assertEqual(self.rom[c['entry']+1:c['entry']+4],b'\x2b'+struct.pack('<H',c['state_flag']))
            self.assertEqual(self.rom[c['flag_write_offset']:c['flag_write_offset']+3],b'\x29'+struct.pack('<H',c['state_flag']))
            self.assertIsNone(c['map_owner'])

    def test_charging_and_insufficient_charge_check_the_same_flag(self):
        self.assertEqual(self.nodes[0xAA2C5D]['values'],[0x544])
        self.assertEqual(self.nodes[0xAA2C66]['name'],'clearflag')
        self.assertEqual(self.nodes[0xAA2C66]['values'],[0x544])
        self.assertEqual(self.nodes[0xAEFF09]['values'],[0x544])
        self.assertIn('one\nuse',self.messages[0xAA5FB1]['plain_text'])
        self.assertIn('Insufficient charge',self.messages[0xB01831]['plain_text'])

    def test_counter_initialization_display_and_completion_operands(self):
        self.assertEqual(self.nodes[0xAD34D6]['values'],[0x5318,11])
        self.assertEqual(self.nodes[0xAD3496]['values'],[0x8005,0x5318])
        self.assertEqual(self.nodes[0xAD349B]['values'],[0x8005,1])
        self.assertEqual(self.nodes[0xAEFF2C]['values'],[0x5318,1])
        self.assertEqual(self.nodes[0xAD353A]['values'],[0x5318,1])
        self.assertEqual(self.nodes[0xAD3EAD]['values'],[0x514])
        self.assertIn('{STR_VAR_1}0%',self.messages[0xAD3B7E]['plain_text'])

    def test_battle_tuple_is_encoded_and_runtime_resume_remains_an_assumption(self):
        self.assertEqual(self.nodes[0xAEFF22]['values'],[0x7D,100,0])
        edges=[e for c in self.data['clusters'] for e in c['edges'] if e['source']==0xAEFF28]
        self.assertTrue(edges)
        self.assertEqual({e['kind'] for e in edges},{'assumed_resume_after_wildbattle'})
        self.assertIn(0xB6,self.data['summary']['used_opcodes_with_modified_handler_intervals'])

    def test_status_substitutions_and_empty_targets_are_kept_distinct(self):
        self.assertEqual(self.messages[0xAD3EB1]['plain_text'],'Activated')
        self.assertEqual(self.messages[0xAD34C8]['plain_text'],'Deactivated')
        targets=list(self.messages.values());summary=self.data['summary']
        self.assertEqual(sum(not m['empty_string'] for m in targets),summary['nonempty_strings'])
        self.assertEqual(sum(m['empty_string'] for m in targets),2)
        self.assertTrue(all(self.rom[m['offset']]==255 for m in targets if m['empty_string']))

    def test_no_literal_setflag_signature_is_misreported_as_no_native_write(self):
        signatures=self.data['flag_0544_literal_signatures']
        self.assertEqual(signatures['hits']['setflag'],[])
        self.assertEqual(signatures['hits']['clearflag'],[0xAA2C66])
        self.assertIn('native',signatures['method'])

    def test_sampled_control_handlers_match_but_battle_handler_differs(self):
        rows={r['opcode']:r for r in self.probe['handler_comparisons']}
        for op in (4,5,6,7,0x2B,0x29,0x2A,0x85):self.assertTrue(rows[op]['compared_bytes_equal'])
        self.assertFalse(rows[0xB6]['compared_bytes_equal'])
        for row in rows.values():
            chunk=row['liquid_crystal'];lo=int(chunk['file_offset'],16);hi=int(chunk['end_exclusive'],16)
            self.assertEqual(hashlib.sha256(self.rom[lo:hi]).hexdigest(),chunk['sha256'])

    def test_source_pointers_and_candidate_paths_are_complete_within_bounds(self):
        self.assertEqual(self.data['summary']['unrooted_anchors'],0)
        self.assertEqual(self.data['summary']['instruction_overlaps'],0)
        self.assertFalse(self.data['summary']['frontier_reasons'])
        for m in self.messages.values():
            self.assertEqual(hashlib.sha256(self.rom[m['offset']:m['end']]).hexdigest(),m['sha256'])
            for ref in m['references']:
                site=ref['pointer_offset']
                self.assertEqual(int.from_bytes(self.rom[site:site+4],'little'),0x08000000+m['offset'])
        for n in self.nodes.values():self.assertEqual(self.rom[n['pc']:n['end']].hex(' '),n['raw_hex'])

if __name__=='__main__':unittest.main()
