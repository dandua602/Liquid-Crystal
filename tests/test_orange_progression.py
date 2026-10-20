"""Standard-table control flow and conservative allocation boundaries."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from architecture_audit import padding_candidates
from dialogue_cluster_audit import trace_graph
from orange_progression_audit import SPECS,decoder
from save_hardware_audit import audit

class ExtendedFlowTests(unittest.TestCase):
    def image(self):
        rom=bytearray(0x160480)
        struct.pack_into('<I',rom,0x160450,0x08000020)
        rom[32]=3
        return rom

    def test_standard_call_returns_to_its_own_continuation(self):
        rom=self.image();rom[:3]=b'\x09\x00\x02'
        graph=trace_graph(rom,0,decoder=decoder)
        self.assertEqual(set(graph['nodes']),{0,2,32})
        self.assertEqual([(e['source'],e['target']) for e in graph['witness'](2)],[(0,32),(32,2)])
        self.assertFalse(graph['frontiers'])

    def test_conditional_standard_jump_keeps_both_paths_without_return(self):
        rom=self.image();rom[:4]=b'\x0a\x01\x00\x02'
        graph=trace_graph(rom,0,decoder=decoder)
        self.assertEqual(set(graph['nodes']),{0,3,32})
        self.assertEqual({e['kind'] for e in graph['edges']},{'condition_false','condition_true'})

    def test_invalid_table_index_and_comparison_stop(self):
        for script in (b'\x09\x0a',b'\x0b\x06\x00'):
            graph=trace_graph(script,0,decoder=decoder)
            self.assertFalse(graph['nodes']);self.assertTrue(graph['frontiers'])

    def test_bad_standard_pointer_is_a_frontier_instead_of_a_crash(self):
        rom=self.image();rom[:3]=b'\x09\x00\x02';rom[0x160450:0x160454]=b'\x00'*4
        graph=trace_graph(rom,0,decoder=decoder)
        self.assertFalse(graph['nodes'])
        self.assertEqual(graph['frontiers'][0]['reason'],'invalid standard-script table pointer')

    def test_context_dependent_jump_never_invents_fallthrough(self):
        for opcode in (0x5E,0x5F,0xBA,0xBB,0xBC,0xBD):
            script=bytes([opcode])+b'\x00'*sum(SPECS[opcode][1])+b'\x02'
            graph=trace_graph(script,0,decoder=decoder)
            self.assertEqual(set(graph['nodes']),{0});self.assertTrue(graph['frontiers'])

    def test_helper_widths_keep_following_commands_aligned(self):
        for opcode,length in [(0x50,9),(0x52,5),(0x54,5),(0xA8,6),(0xD4,6)]:
            script=bytes([opcode])+b'\x00'*(length-1)+b'\x02'
            graph=trace_graph(script,0,decoder=decoder)
            self.assertEqual(set(graph['nodes']),{0,length})
        self.assertEqual(set(SPECS)|{0x5C},set(range(0xD5)))

    def test_pointer_at_padding_end_belongs_to_next_region(self):
        rows=padding_candidates(b'\x00'+b'\xff'*16+b'\x00',{0:[40],1:[41],16:[42],17:[43]},minimum=8)
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['start'],rows[0]['end'],rows[0]['aligned_start']),(1,17,4))
        self.assertEqual([r['target'] for r in rows[0]['incoming']],[1,16])
        self.assertEqual(rows[0]['status'],'CANDIDATE_ONLY_NOT_ALLOCATED')

class SuppliedCartridgeTests(unittest.TestCase):
    def test_embedded_save_is_exactly_the_uploaded_payload(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        save=(ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav').read_bytes()
        result=audit(rom,save)
        self.assertTrue(result['embedded_window']['equals_source_save_payload'])
        changed=bytearray(rom);changed[0xC7213C]^=1
        with self.assertRaises(ValueError):audit(changed,save)

    def test_preflight_preserves_hook_bytes_and_allocates_nothing(self):
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        result=json.loads((ROOT/'extracted/maps/architecture_preflight.json').read_text())
        self.assertEqual(result['source_sha256'],hashlib.sha256(rom).hexdigest())
        self.assertEqual(result['expansion']['allocated_bytes'],0)
        for hook in result['hook_ledger']:
            data=bytes.fromhex(hook['bytes'])
            self.assertEqual(data,rom[hook['site']:hook['site']+len(data)])
            self.assertIsNone(hook['allocation'])
        self.assertTrue(all(r['status']=='CANDIDATE_ONLY_NOT_ALLOCATED' for r in result['padding_candidates']))

if __name__=='__main__':unittest.main()
