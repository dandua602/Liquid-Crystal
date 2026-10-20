"""Branch/call boundaries and supplied-ROM dialogue-cluster regressions."""
import json,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from dialogue_cluster_audit import instruction,trace_graph
from gba_text_codec import encode

class GraphFormatTests(unittest.TestCase):
    def test_both_conditional_paths_are_retained_without_claiming_execution(self):
        rom=bytearray(b'\xff'*64)
        rom[:7]=b'\x06\x01'+struct.pack('<I',0x08000020)+b'\x02'
        rom[32]=2;g=trace_graph(rom,0)
        self.assertEqual(set(g['nodes']),{0,6,32})
        self.assertEqual({e['kind'] for e in g['edges']},{'condition_false','condition_true'})

    def test_nested_calls_return_to_the_correct_continuations(self):
        rom=bytearray(b'\xff'*128)
        rom[:6]=b'\x04'+struct.pack('<I',0x08000020)+b'\x02'
        rom[32:38]=b'\x04'+struct.pack('<I',0x08000030)+b'\x03'
        rom[48]=3;g=trace_graph(rom,0)
        self.assertEqual([(e['source'],e['target']) for e in g['witness'](5)],[(0,32),(32,48),(48,37),(37,5)])
        self.assertFalse(g['frontiers'])

    def test_battle_continuation_is_an_explicit_engine_candidate(self):
        rom=bytearray(b'\xff'*128)
        rom[:18]=b'\x5c\x01\x64\x03\x00\x00'+struct.pack('<III',0x08000040,0x08000050,0x08000020)
        rom[18]=2;rom[32]=2;g=trace_graph(rom,0)
        self.assertEqual({e['kind'] for e in g['edges']},{'engine_postbattle_candidate','engine_beaten_script_candidate'})
        self.assertIn(32,g['nodes'])

    def test_type_nine_text_roles_are_defeat_and_victory(self):
        rom=b'\x5c\x09\x45\x03\x00\x00'+struct.pack('<II',0x08000020,0x08000030)
        ins,error=instruction(rom,0)
        self.assertIsNone(error)
        self.assertEqual([r['role'] for r in ins['texts']],['trainer_defeat','trainer_victory'])

    def test_invalid_target_does_not_decode_wrapped_or_negative_memory(self):
        rom=b'\x05'+struct.pack('<I',0x02000000)+b'\x02'
        g=trace_graph(rom,0)
        self.assertEqual(set(g['nodes']),{0})
        self.assertEqual(g['frontiers'][0]['reason'],'non-ROM target')

    def test_unknown_opcode_stops_instead_of_skipping_to_dialogue(self):
        g=trace_graph(b'\xff\x02',0)
        self.assertFalse(g['nodes'])
        self.assertEqual(g['frontiers'][0]['reason'],'unsupported opcode FF')

    def test_loop_terminates_without_inventing_fallthrough(self):
        g=trace_graph(b'\x05'+struct.pack('<I',0x08000000)+b'\x02',0)
        self.assertEqual(set(g['nodes']),{0})
        self.assertFalse(g['frontiers'])

    def test_state_budget_reports_a_frontier_without_crashing(self):
        rom=bytearray(b'\xff'*64)
        rom[:7]=b'\x06\x01'+struct.pack('<I',0x08000020)+b'\x02'
        rom[32]=2
        g=trace_graph(rom,0,max_states=1)
        self.assertEqual(g['state_count'],1)
        self.assertTrue(any(f['reason']=='state limit' for f in g['frontiers']))

class SuppliedRomClusterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'extracted/text/dialogue_clusters.json').read_text())
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()

    def cluster(self,anchor):return next(c for c in self.data['clusters'] if c['anchor_text']==anchor)

    def test_danny_defeat_speech_and_badge_continuation_are_linked(self):
        c=self.cluster('0xb11c47');messages={m['offset']:m for m in c['messages']}
        self.assertIn('Outstanding!',messages[0xB11B79]['plain_text'])
        self.assertFalse(messages[0xB11B79]['in_prior_keyword_corpus'])
        self.assertTrue(any(e['source']==0xB0FF91 and e['target']==0xB0FFE2 and e['kind']=='engine_beaten_script_candidate' for e in c['edges']))
        root=next(x for x in c['roots'] if x['offset']==0xB00435)
        path=root['witnesses_to_anchor_commands']['0xb0ffe2']
        self.assertIn('engine_beaten_script_candidate',[e['kind'] for e in path])

    def test_mister_g_departure_and_item_tuple_are_preserved(self):
        c=self.cluster('0xb1d4e0')
        self.assertTrue(any(m['offset']==0xAB7EEB and 'Mister Z is waiting' in m['plain_text'] for m in c['messages']))
        ins=next(n for n in c['instructions'] if n['pc']==0xAAAFC2)
        self.assertEqual(ins['values'],[0x8000,0x114])
        self.assertFalse(c['instruction_overlaps'])

    def test_selected_clusters_have_no_unsupported_or_overlapping_instruction_paths(self):
        self.assertEqual(len(self.data['clusters']),5)
        for c in self.data['clusters']:
            self.assertFalse(c['instruction_overlaps'])
            self.assertFalse(c['frontiers'])
            for root in c['roots']:
                for path in root['witnesses_to_anchor_commands'].values():
                    self.assertIsNotNone(path)
                    pc=root['offset']
                    for edge in path:
                        self.assertEqual(edge['source'],pc)
                        pc=edge['target']

    def test_cluster_instructions_and_text_pointers_match_rom_bytes(self):
        for c in self.data['clusters']:
            pcs={n['pc'] for n in c['instructions']}
            for n in c['instructions']:
                self.assertEqual(self.rom[n['pc']:n['end']].hex(' '),n['raw_hex'])
            for m in c['messages']:
                self.assertEqual(self.rom[m['end']-1],255)
                for ref in m['references']:
                    self.assertIn(ref['command'],pcs)
                    site=ref['pointer_offset']
                    self.assertEqual(int.from_bytes(self.rom[site:site+4],'little'),0x08000000+m['offset'])
                    self.assertEqual(ref['target'],m['offset'])
            for root in c['roots']:
                for site in root['incoming_pointer_sites']:
                    self.assertEqual(int.from_bytes(self.rom[site:site+4],'little'),0x08000000+root['offset'])

if __name__=='__main__':unittest.main()
