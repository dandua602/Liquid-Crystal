"""Preserve weak candidate tiers and bound negative map-selection evidence."""
import csv
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from map_extract import FormatError, LOOKUP_SIGNATURE
from map_selection_audit import build, lz77_extent, scan_map_links, thumb_bl


class SelectionProbeFormatTests(unittest.TestCase):
    def test_thumb_bl_forward_backward_and_alignment(self):
        rom = bytearray(128)
        for at, target in [(8, 100), (100, 8)]:
            relative = target - at - 4
            struct.pack_into('<HH', rom, at, 0xF000 | ((relative >> 12) & 0x7FF),
                             0xF800 | ((relative >> 1) & 0x7FF))
            self.assertEqual(thumb_bl(rom, at), target)
        self.assertIsNone(thumb_bl(rom, 9))
        self.assertIsNone(thumb_bl(rom, 126))
        self.assertIsNone(thumb_bl(bytes(8), 0))

    def test_lz77_extent_validates_distances_bounds_and_partial_final_run(self):
        rom = bytes.fromhex('10 06 00 00 10 41 42 43 00 02 ff ff')
        valid = lz77_extent(rom, 0)
        self.assertEqual((valid['start'], valid['end'], valid['declared_output_size']), (0, 10, 6))
        self.assertIsNone(lz77_extent(rom[:-5], 0))
        self.assertIsNone(lz77_extent(rom, 0, max_output=5))
        self.assertIsNone(lz77_extent(rom, 0, max_input=8))
        self.assertIsNone(lz77_extent(bytes.fromhex('10 03 00 00 80 00 00'), 0))
        self.assertEqual(lz77_extent(bytes.fromhex('10 04 00 00 40 41 00 00'), 0)['end'], 8)

    def test_bad_layout_does_not_hide_readable_variant_warp(self):
        rom = bytearray(b'\xff' * 0x1000)
        rom[0:24] = LOOKUP_SIGNATURE + struct.pack('<I', 0x08000100)
        struct.pack_into('<I', rom, 0x100, 0x08000200)
        struct.pack_into('<I', rom, 0x200, 0x08000300)
        # Header layout is deliberately invalid; events and warp are readable.
        struct.pack_into('<IIII', rom, 0x300, 0xFFFFFFFF, 0x08000400, 0, 0)
        rom[0x400:0x404] = bytes([0, 1, 0, 0])
        struct.pack_into('<IIII', rom, 0x404, 0, 0x08000500, 0, 0)
        struct.pack_into('<hhBBBB', rom, 0x500, 1, 2, 0, 0, 107, 3)
        result = scan_map_links(rom)
        self.assertEqual(len(result['slots']), 1)
        self.assertEqual(len(result['incoming_records']), 1)
        record = result['incoming_records'][0]
        self.assertEqual(record['destination_map'], 107)
        self.assertEqual(record['source_evidence'], 'link_span_only_unvalidated_header')
        self.assertEqual(result['slots'][0]['connection']['status'], 'null_pointer')


class SuppliedMapSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.reference = (ROOT / 'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        cls.data = json.loads((ROOT / 'extracted/maps/map_selection_audit.json').read_text())

    def test_scan_retains_failures_and_distinguishes_weak_inbound_rows(self):
        scan = self.data['map_record_scan']
        self.assertEqual(scan['summary']['candidate_slots'], 1504)
        self.assertEqual(scan['summary']['groups_in_physical_prefix'], 43)
        self.assertEqual(scan['summary']['banks_reaching_scan_limit'], 0)
        self.assertEqual(scan['summary']['incoming_candidate_associations_by_target'], {'3:99': 11, '3:101': 6, '3:107': 0, '3:111': 0})
        self.assertEqual(scan['summary']['incoming_validated_header_associations_by_target'], {'3:99': 3, '3:101': 6, '3:107': 0, '3:111': 0})
        for kind in ('warp', 'connection'):
            self.assertEqual(sum(scan['summary'][kind]['slot_statuses'].values()), 1504)
            self.assertGreater(scan['summary'][kind]['slot_statuses']['unresolved'], 0)
        weak = [r for r in scan['incoming_records'] if r['source_evidence'] != 'validated_header_and_link_span']
        self.assertEqual(len(weak), 8)
        self.assertEqual({r['header'] for r in weak}, {0x3525E4})
        self.assertEqual({r['offset'] for r in weak}, {0x170C7E})
        for row in scan['incoming_records']:
            size = 8 if row['kind'] == 'warp' else 12
            self.assertEqual(bytes.fromhex(row['raw_hex']), self.rom[row['offset']:row['offset'] + size])
            self.assertEqual(row['reachability'], 'UNKNOWN')

    def test_raw_shapes_keep_unresolved_context_and_path_frontiers(self):
        shapes = self.data['raw_script_shapes']
        self.assertEqual(len(shapes), 14)
        self.assertEqual(self.data['summary']['raw_shape_contexts'],
                         {'overlapping_ROM_pointer_word': 2, 'pointer_backed_LZ77_stream': 8, 'unresolved_context': 4})
        for row in shapes:
            self.assertFalse(row['catalogue_instruction_boundary_match'])
            self.assertFalse(row['pointer_target_scan_truncated'])
            self.assertEqual(row['status'], 'unvalidated_command_shape')
            for attempt in row['pointer_target_path_attempts']:
                self.assertFalse(attempt['witness'] is not None and not attempt['overlaps'])
            if row['compressed_stream']:
                stream = row['compressed_stream']
                self.assertLessEqual(stream['start'], row['offset'])
                self.assertLessEqual(row['instruction_shape']['end'], stream['end'])
                self.assertEqual(lz77_extent(self.rom, stream['start'])['end'], stream['end'])
                self.assertTrue(stream['incoming_pointer_sites'])
        unresolved = {row['offset'] for row in shapes if row['context_class'] == 'unresolved_context'}
        self.assertEqual(unresolved, {0x424326, 0x430E4E, 0x603F66, 0xE63774})
        self.assertTrue(self.data['catalogue_paths']['summary']['frontier_reasons'])
        self.assertEqual(self.data['catalogue_paths']['summary']['roots'], 332)
        self.assertEqual(self.data['catalogue_paths']['summary']['unique_instructions'], 3717)

    def test_header_pointer_fragment_is_not_promoted_to_native_use(self):
        first, second = self.data['header_pointer_evidence']
        self.assertEqual([r['pointer_site'] for r in first['references']], [0xC2B0B4])
        self.assertEqual([r['pointer_site'] for r in second['references']], [0xC2B0C4, 0xC32A2C])
        fragment = second['references'][1]['layout_shaped_context']
        self.assertEqual((fragment['start'], fragment['width'], fragment['height']), (0xC32A20, 68, 42))
        self.assertEqual(fragment['incoming_absolute_pointer_sites'], [])
        self.assertEqual(second['references'][1]['role'], 'unclassified_data_pointer')

    def test_native_target_discovery_and_probe_contexts_match_rom(self):
        native = self.data['native_probe']
        destination = next(r for r in native['target_discovery'] if r['opcode'] == 0x3E)
        self.assertEqual(destination['selected_last_call']['target'], 0x5538C)
        self.assertEqual(len(native['call_sites']), 56)
        self.assertEqual(native['summary']['sites_with_variant_constant_shapes'], 0)
        for call in native['call_sites']:
            self.assertEqual(thumb_bl(self.rom, call['offset']), call['target'])
            self.assertEqual(bytes.fromhex(call['context_hex']), self.rom[call['context_start']:call['offset'] + 8])
        self.assertTrue(all(row['compared_bytes_equal'] for row in native['handler_comparison']['handler_comparisons']))

    def test_complete_audit_reproduces_and_stale_catalogue_is_rejected(self):
        catalogue = json.loads((ROOT / 'extracted/scripts/map_script_catalogue.json').read_text())
        self.assertEqual(build(self.rom, self.reference, catalogue), self.data)
        catalogue['source_sha256'] = '0' * 64
        with self.assertRaises(FormatError):
            build(self.rom, self.reference, catalogue)
        with (ROOT / 'extracted/maps/map_selection_incoming.csv').open() as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 17)


if __name__ == '__main__':
    unittest.main()
