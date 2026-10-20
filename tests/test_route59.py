"""Route 59 returns, scripted emergence and Mister R source ownership."""
import csv
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from dialogue_cluster_audit import trace_graph
from map_extract import FormatError
from route59_audit import build, decode_route59, script_destination
from script_extract import decode_script
from warp_graph import MapCatalog


class Route59DecoderTests(unittest.TestCase):
    def test_ui_command_is_local_and_resume_is_explicit(self):
        rom = bytes([0x6F, 12, 0, 26, 0, 2])
        ins, error = decode_route59(rom, 0)
        self.assertIsNone(error)
        self.assertEqual(ins['values'], [12, 0, 26, 0])
        self.assertEqual(ins['end'], 5)
        graph = trace_graph(rom, 0, decoder=decode_route59)
        self.assertIn({'source': 0, 'target': 5, 'kind': 'assumed_resume_after_choice_ui'}, graph['edges'])
        self.assertIsNotNone(decode_script(rom, 0)[1])

    def test_money_operand_is_a_full_little_endian_word(self):
        rom = bytes([0x92]) + struct.pack('<I', 50000) + bytes([0, 2])
        ins, error = decode_route59(rom, 0)
        self.assertIsNone(error)
        self.assertEqual(ins['values'], [50000, 0])
        self.assertEqual(ins['end'], 6)
        self.assertEqual(decode_route59(rom[:5], 0)[1], 'truncated operands')


class SuppliedRoute59Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.reference = (ROOT / 'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        cls.data = json.loads((ROOT / 'extracted/maps/route59_destination_audit.json').read_text())
        cls.traces = {t['root']: t for t in cls.data['script_traces']['traces']}

    def test_all_static_links_match_rom_without_expanding_legacy_maps(self):
        self.assertEqual(len(self.data['maps']), 13)
        self.assertEqual(len(self.data['edges']), 20)
        self.assertEqual({e['source_map'] for e in self.data['edges']}, {'3:110', '6:28', '6:29', '6:30', '6:31'})
        for edge in self.data['edges']:
            size = 8 if edge['kind'] == 'warp' else 12
            self.assertEqual(bytes.fromhex(edge['raw_hex']), self.rom[edge['offset']:edge['offset'] + size])
            self.assertIn(edge['destination']['status'], ('warp_record_validated', 'connection_record_validated'))
            if edge['kind'] == 'warp':
                self.assertTrue(edge['source_coordinates_in_default_layout'])
                self.assertTrue(edge['destination']['landing_coordinates_in_layout'])
            self.assertEqual(edge['reachability'], 'UNKNOWN')
        self.assertEqual(self.data['summary']['warp_return_relations'],
                         {'another_map': 8, 'dynamic_return': 1, 'exact_return': 9, 'source_map_different_warp': 1})

    def test_custom_four_map_catalogue_and_rom_start_candidates_are_preserved(self):
        cat = self.data['script_catalogue']
        self.assertEqual(len(cat['maps']), 4)
        self.assertEqual(cat['summary']['event_records'], 29)
        self.assertEqual(cat['summary']['script_associations'], 29)
        self.assertEqual(len(cat['roots']), 15)
        self.assertEqual(len(self.data['ROM_start_fields']), 4)
        for event in self.data['ROM_start_fields']:
            self.assertEqual(event['raw_script_word'], 0x08000000)
            self.assertEqual(event['script_target'], 0)
            self.assertEqual(event['script_status'], 'ROM_script_candidate')
        self.assertEqual(len(self.traces[0]['association_ids']), 4)
        self.assertEqual(self.traces[0]['frontiers'], [{'pc': 0, 'reason': 'unsupported opcode FE'}])
        self.assertEqual(self.data['script_traces']['summary']['instruction_overlap_records'], 0)

    def test_two_emergence_paths_have_witnesses_and_twelve_owners(self):
        transitions = self.data['scripted_transitions']
        self.assertEqual(len(transitions), 2)
        self.assertEqual({t['command'] for t in transitions}, {0xAA08C1, 0xAE8CB1})
        self.assertEqual({t['destination']['landing']['index'] for t in transitions}, {1, 4})
        for t in transitions:
            self.assertEqual(t['name'], 'warpteleport')
            self.assertEqual(t['destination']['target_map'], '3:110')
            self.assertEqual(t['destination']['status'], 'indexed_target_warp_validated')
            self.assertEqual(len(t['owner_associations']), 6)
            self.assertTrue(all(a['map_id'] == '6:30' and a['kind'] == 'background' for a in t['owner_associations']))
            self.assertEqual(t['witness'][0]['source'], t['root'])
            self.assertEqual(t['witness'][-1]['target'], t['command'])
            nodes = self.traces[t['root']]['instructions']
            self.assertTrue(any(n['name'] == 'checkflag' and n['values'] == [0x1685] for n in nodes))
            self.assertTrue(any(n['name'] == 'dofieldeffect' and n['values'] == [0x25] for n in nodes))
            self.assertFalse(self.traces[t['root']]['frontiers'])
        catalog = MapCatalog(self.rom)
        for index in (128, 255):
            self.assertEqual(script_destination(catalog, {'values': [3, 110, index, 0x8004, 0x8005]})['status'], 'unresolved')

    def test_mister_r_frame_gate_is_owned_and_has_no_battle_in_local_trace(self):
        room = next(m for m in self.data['script_catalogue']['maps'] if m['id'] == '6:31')
        entry = room['map_script_table']['entries'][0]
        condition = entry['conditional_table']['entries'][0]
        self.assertEqual((entry['tag'], condition['operand_1'], condition['operand_2'], condition['script_target']),
                         (2, 0x5331, 0, 0xAE8D7A))
        trace = self.traces[0xAE8D7A]
        self.assertEqual(trace['association_ids'], ['6:31:map_entry:0:condition:0'])
        self.assertFalse(trace['frontiers'])
        by_pc = {n['pc']: n for n in trace['instructions']}
        self.assertEqual(by_pc[0xAE8D7A]['values'], [0x5331, 1])
        self.assertEqual((by_pc[0xAE8DB5]['name'], by_pc[0xAE8DB5]['values']), ('setflag', [0x5C5]))
        self.assertEqual((by_pc[0xAE8DB8]['name'], by_pc[0xAE8DB8]['values']), ('removeobject', [1]))
        self.assertFalse(any(n['opcode'] == 0x5C for n in trace['instructions']))
        self.assertTrue(any('solve my puzzle' in m.get('plain_text', '') for m in trace['messages']))

    def test_seller_branches_preserve_amount_item_and_state(self):
        trace = self.traces[0xA9C566]
        self.assertFalse(trace['frontiers'])
        by_pc = {n['pc']: n for n in trace['instructions']}
        self.assertEqual((by_pc[0xA9C58B]['name'], by_pc[0xA9C58B]['values']), ('checkmoney', [50000, 0]))
        self.assertEqual((by_pc[0xA9C59C]['name'], by_pc[0xA9C59C]['values']), ('removemoney', [50000, 0]))
        self.assertEqual(by_pc[0xA9C5A6]['values'], [0x8000, 0x2A])
        self.assertEqual(by_pc[0xA9C5AB]['values'], [0x8001, 1])
        self.assertEqual((by_pc[0xA9C5C5]['name'], by_pc[0xA9C5C5]['values']), ('setflag', [0x5C0]))
        self.assertTrue(all(pc in by_pc for pc in (0xA9C612, 0xA9C623, 0xA9C634)))

    def test_audit_reproduces_and_native_comparisons_remain_scoped(self):
        old = json.loads((ROOT / 'extracted/maps/controller_connectivity.json').read_text())
        self.assertEqual(build(self.rom, self.reference, old), self.data)
        old['source_sha256'] = '0' * 64
        with self.assertRaises(FormatError):
            build(self.rom, self.reference, old)
        probe = self.data['command_handler_probe']['handler_comparisons']
        self.assertEqual(len(probe), 12)
        self.assertTrue(all(p['compared_bytes_equal'] for p in probe))
        for path, count in [('extracted/maps/route59_links.csv', 20), ('extracted/scripts/route59_script_associations.csv', 29)]:
            with (ROOT / path).open() as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), count)


if __name__ == '__main__':
    unittest.main()
