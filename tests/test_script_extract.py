"""Event unions, map-entry bounds, script ownership and gate witnesses."""
import csv
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from dialogue_cluster_audit import SPECS, trace_graph
from map_extract import FormatError
from script_extract import (catalogue, conditional_table, decode_script, event_records,
                            focus_audit, map_script_table)


class MapScriptFormatTests(unittest.TestCase):
    def test_unknown_nonzero_tags_consume_five_bytes_and_duplicates_remain(self):
        rom = bytearray(128)
        rom[0:16] = bytes([255]) + struct.pack('<I', 0) + bytes([1]) + struct.pack('<I', 0x08000040) + bytes([1]) + struct.pack('<I', 0x08000050) + bytes([0])
        table = map_script_table(rom, 0)
        self.assertTrue(table['terminated'])
        self.assertEqual(table['terminator'], 15)
        self.assertEqual([e['offset'] for e in table['entries']], [0, 5, 10])
        self.assertEqual([e['first_entry_for_tag'] for e in table['entries']], [True, True, False])
        self.assertEqual(table['entries'][0]['script_status'], 'null')
        self.assertEqual(table['entries'][1]['script_target'], 64)
        self.assertFalse(map_script_table(rom, 0, limit=2)['terminated'])

    def test_condition_table_has_two_byte_terminator_and_explicit_limits(self):
        rom = struct.pack('<HHIH', 0x5305, 0x4001, 0x08000008, 0)
        result = conditional_table(rom, 0)
        self.assertTrue(result['terminated'])
        self.assertEqual(result['end'], len(rom))
        self.assertEqual(result['entries'][0]['operand_2'], 0x4001)
        self.assertFalse(conditional_table(rom[:-1], 0)['terminated'])
        self.assertFalse(conditional_table(rom, 0, limit=1)['terminated'])
        self.assertFalse(map_script_table(bytes([1, 2, 3]), 0)['terminated'])

    def test_hidden_item_and_clone_unions_never_become_direct_script_roots(self):
        rom = bytearray(128)
        # Pointer-looking hidden-item data is not an executable pointer field.
        rom[5] = 7
        struct.pack_into('<I', rom, 8, 0x08000060)
        # Clone metadata refers to a different object's template.
        rom[34] = 255
        struct.pack_into('<I', rom, 48, 0x08000060)
        m = {'id': '1:1', 'width': 10, 'height': 10,
             'events': {'counts': [1, 0, 0, 1], 'arrays': [32, None, None, 0]}}
        rows = event_records(rom, m)
        self.assertEqual(rows[0]['script_status'], 'clone_indirect_unresolved')
        self.assertEqual(rows[1]['script_status'], 'hidden_item_union_not_script')
        self.assertTrue(all(r['script_target'] is None for r in rows))

    def test_coordinate_gate_preserves_raw_and_low_byte_operands(self):
        rom = bytearray(64)
        struct.pack_into('<HHBBHH2xI', rom, 0, 1, 2, 0, 0, 0x5305, 0x1234, 0x08000030)
        m = {'id': '1:1', 'width': 10, 'height': 10,
             'events': {'counts': [0, 0, 1, 0], 'arrays': [None, None, 0, None]}}
        row = event_records(rom, m)[0]
        self.assertEqual(row['trigger_value_raw'], 0x1234)
        self.assertEqual(row['trigger_value_compared_low_byte'], 0x34)
        self.assertEqual(row['script_target'], 48)

    def test_local_warp_decoder_preserves_map_order_and_resume_assumption(self):
        rom = bytes([0x39, 3, 107, 255]) + struct.pack('<HH', 0x8004, 20) + bytes([2])
        ins, error = decode_script(rom, 0)
        self.assertIsNone(error)
        self.assertEqual(ins['values'], [3, 107, 255, 0x8004, 20])
        self.assertEqual(ins['end'], 8)
        graph = trace_graph(rom, 0, decoder=decode_script)
        self.assertIn({'source': 0, 'target': 8, 'kind': 'assumed_resume_after_script_warp'}, graph['edges'])
        self.assertEqual(set(graph['nodes']), {0, 8})
        self.assertNotIn(0x39, SPECS)  # Existing dialogue traces keep their prior decoder.


class SuppliedMapScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.data = json.loads((ROOT / 'extracted/scripts/map_script_catalogue.json').read_text())
        cls.focus = json.loads((ROOT / 'extracted/scripts/route54_science_script_audit.json').read_text())
        cls.maps = {m['id']: m for m in cls.data['maps']}

    def test_all_records_associations_and_aliases_are_preserved(self):
        self.assertEqual(len(self.maps), 32)
        self.assertEqual(self.data['summary']['event_kinds'], {'background': 140, 'coordinate': 130, 'object': 285})
        self.assertEqual(len(self.data['roots']), 332)
        owners = [a for r in self.data['roots'] for a in r['associations']]
        self.assertEqual(len(owners), 559)
        self.assertEqual(len({a['id'] for a in owners}), 559)
        self.assertEqual(sum(a['kind'] == 'map_entry' for a in owners), 25)
        for a in owners:
            self.assertEqual(struct.unpack_from('<I', self.rom, a['pointer_site'])[0], a['script_target'] + 0x08000000)
        for compare in self.data['alias_comparisons']:
            self.assertTrue(compare['same_map_script_pointer'])
            self.assertEqual(compare['event_record_raw_differences'], [])

    def test_every_event_matches_source_bytes_and_default_coordinates(self):
        strides = {'object': 24, 'coordinate': 16, 'background': 12}
        for m in self.maps.values():
            for e in m['events']:
                self.assertEqual(bytes.fromhex(e['raw_hex']), self.rom[e['offset']:e['offset'] + strides[e['kind']]])
                self.assertTrue(e['coordinates_in_default_layout'])
                self.assertEqual(e['reachability'], 'UNKNOWN')
        self.assertEqual(self.maps['3:60']['events'], [])
        self.assertEqual(self.data['summary']['event_script_statuses']['hidden_item_union_not_script'], 5)
        # The unknown-tag-only lobby scan must not fabricate a map entry root.
        self.assertTrue(self.maps['0:0']['map_script_table']['terminated'])
        self.assertTrue(all(e['tag_name'] == 'unknown_tag' for e in self.maps['0:0']['map_script_table']['entries']))
        self.assertFalse(any(a['map_id'] == '0:0' and a['kind'] == 'map_entry' for r in self.data['roots'] for a in r['associations']))

    def test_route54_frame_gate_matches_blocker_objects_and_trace(self):
        for key in ('3:101', '3:107'):
            entry = self.maps[key]['map_script_table']['entries'][0]
            condition = entry['conditional_table']['entries'][0]
            self.assertEqual((condition['offset'], condition['operand_1'], condition['operand_2'], condition['script_target']),
                             (0x721D62, 0x5305, 0, 0xA7094D))
            objects = [e for e in self.maps[key]['events'] if e['kind'] == 'object' and e['local_id'] in (5, 6)]
            self.assertEqual([(e['visibility_flag'], e['script_status']) for e in objects], [(0x52E, 'null')] * 2)
        trace = next(t for t in self.focus['traces'] if t['root'] == 0xA7094D)
        self.assertFalse(trace['frontiers'])
        by_pc = {n['pc']: n for n in trace['instructions']}
        self.assertEqual((by_pc[0xA7094D]['name'], by_pc[0xA7094D]['values']), ('setvar', [0x5305, 1]))
        self.assertEqual(by_pc[0xA7099A]['values'], [6])
        self.assertEqual(by_pc[0xA709BF]['values'], [5])
        self.assertEqual((by_pc[0xA709C2]['name'], by_pc[0xA709C2]['values']), ('setflag', [0x52E]))
        self.assertEqual(len(trace['messages']), 3)
        self.assertTrue(any('Crystal Onix' in m.get('plain_text', '') for m in trace['messages']))

    def test_focus_instructions_witnesses_and_limits_remain_explicit(self):
        self.assertEqual(len(self.focus['traces']), 67)
        self.assertEqual(self.focus['summary']['instruction_overlap_records'], 0)
        self.assertTrue(self.focus['summary']['frontier_reasons'])
        self.assertEqual(self.focus['summary']['transition_or_destination_setter_instructions'], 0)
        for t in self.focus['traces']:
            self.assertEqual(t['reachability'], 'UNKNOWN')
            edges = {(e['source'], e['target'], e['kind']) for e in t['edges']}
            for n in t['instructions']:
                self.assertEqual(bytes.fromhex(n['raw_hex']), self.rom[n['pc']:n['end']])
            for candidate in t['selected_gate_transition_native_candidates']:
                witness = candidate['witness']
                if witness:
                    self.assertEqual(witness[0]['source'], t['root'])
                    self.assertEqual(witness[-1]['target'], candidate['pc'])
                for edge in witness:
                    self.assertIn((edge['source'], edge['target'], edge['kind']), edges)

    def test_catalogue_and_focus_reproduce_and_stale_input_fails(self):
        connectivity = json.loads((ROOT / 'extracted/maps/controller_connectivity.json').read_text())
        result = catalogue(self.rom, connectivity)
        self.assertEqual(result, self.data)
        self.assertEqual(focus_audit(self.rom, result), self.focus)
        connectivity['source_sha256'] = '0' * 64
        with self.assertRaises(FormatError):
            catalogue(self.rom, connectivity)
        with (ROOT / 'extracted/scripts/map_script_associations.csv').open() as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 559)


if __name__ == '__main__':
    unittest.main()
