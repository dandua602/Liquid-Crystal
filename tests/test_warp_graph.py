"""Static destination, sparse-layout, alias and dynamic-return regressions."""
import copy
import csv
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from map_extract import FormatError
from warp_graph import (LAYOUT_LOOKUP_SIGNATURE, MapCatalog, build,
                        connection_destination, discover_layout_lookup, warp_destination)


class LookupAndSemanticsTests(unittest.TestCase):
    def test_layout_lookup_can_relocate(self):
        rom = bytearray(b'\xff' * 0x1000)
        rom[0x100:0x128] = LAYOUT_LOOKUP_SIGNATURE + struct.pack('<I', 0x08000800)
        found = discover_layout_lookup(rom)
        self.assertEqual((found['function'], found['literal_site'], found['table']), (0x100, 0x124, 0x800))
        rom[0x200:0x228] = rom[0x100:0x128]
        with self.assertRaises(FormatError):
            discover_layout_lookup(rom)

    def test_dynamic_destination_depends_on_map_number_only(self):
        # A dynamic source does not need a resolvable target map or warp index.
        result = warp_destination({'destination_map': 127, 'destination_group': 0, 'destination_warp': 255}, {}, None)
        self.assertEqual(result['status'], 'dynamic_destination')
        self.assertIsNone(result['target_map'])

    def test_out_of_range_warp_is_not_read_as_adjacent_data(self):
        target = {'id': '1:1', 'status': 'structure_validated', 'warps': []}
        for index in (0, 127, 255):
            result = warp_destination({'destination_map': 1, 'destination_warp': index}, {}, target)
            self.assertEqual(result['status'], 'nonindexed_or_out_of_range_warp')
            self.assertNotIn('landing', result)

    def test_connection_geometry_does_not_require_reciprocity(self):
        source = {'group': 3, 'map': 1, 'width': 10, 'height': 10}
        target = {'id': '3:2', 'status': 'structure_validated', 'width': 5, 'height': 8, 'connections': []}
        connection = {'direction': 2, 'displacement': 8}
        result = connection_destination(connection, source, target)
        self.assertEqual(result['geometric_overlap']['tiles'], 2)
        self.assertFalse(result['inverse_displacement_returns'])
        target['connections'] = [{'direction': 1, 'displacement': -8, 'destination_group': 3, 'destination_map': 1}]
        self.assertEqual(len(connection_destination(connection, source, target)['inverse_displacement_returns']), 1)
        self.assertEqual(connection_destination({'direction': 0}, source, target)['status'], 'no_direction')
        self.assertEqual(connection_destination({'direction': 99}, source, target)['status'], 'unknown_direction')


class SuppliedConnectivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.inventory = json.loads((ROOT / 'extracted/maps/controller_map_owners.json').read_text())
        cls.data = json.loads((ROOT / 'extracted/maps/controller_connectivity.json').read_text())
        cls.maps = {m['id']: m for m in cls.data['maps']}

    def test_all_individual_links_and_aliases_survive(self):
        edges = self.data['edges']
        self.assertEqual(len(self.maps), 32)
        self.assertEqual(sum(m['seed'] for m in self.maps.values()), 10)
        self.assertEqual(len(edges), 71)
        self.assertEqual(len({e['id'] for e in edges}), 71)
        for kind, count, physical in [('warp', 58, 58), ('connection', 13, 11)]:
            selected = [e for e in edges if e['kind'] == kind]
            self.assertEqual(len(selected), count)
            self.assertEqual(len({e['offset'] for e in selected}), physical)
        self.assertTrue(all(e['reachability'] == 'UNKNOWN' for e in edges))
        self.assertEqual({e['source_map'] for e in edges}, {m['id'] for m in self.maps.values() if m['seed']})
        first, alias = self.maps['3:101'], self.maps['3:107']
        self.assertNotEqual(first['events']['arrays'][1], alias['events']['arrays'][1])
        self.assertEqual([w['raw_hex'] for w in first['warps']], [w['raw_hex'] for w in alias['warps']])
        self.assertEqual(first['connection_structure'], alias['connection_structure'])

    def test_targets_and_landings_match_rom(self):
        for e in self.data['edges']:
            length = 8 if e['kind'] == 'warp' else 12
            self.assertEqual(bytes.fromhex(e['raw_hex']), self.rom[e['offset']:e['offset'] + length])
            target = self.maps[e['destination']['target_map']]
            self.assertEqual(target['status'], 'structure_validated')
            if e['kind'] == 'warp':
                self.assertTrue(e['source_coordinates_in_layout'])
                self.assertTrue(e['destination']['landing_coordinates_in_layout'])
                landing = e['destination']['landing']
                self.assertEqual(landing['offset'], target['events']['arrays'][1] + e['destination_warp'] * 8)
                self.assertEqual(bytes.fromhex(landing['raw_hex']), self.rom[landing['offset']:landing['offset'] + 8])

    def test_native_warp_interpretation_evidence_matches_firered(self):
        reference = (ROOT / 'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        spans = [(0x6DC54, 0x6DCD0, '6d6e4aa93d3c878301864a2cba34665cce488962810c20d993ac3f903ddb2b2b'),
                 (0x552FC, 0x55378, 'b4d5ebd3afb0b3ae098ae941b9d2aacb3b3809262383be260da7605de69d4e0a'),
                 (0x553C8, 0x55468, '19e16e4449b3bb624931ed9c1b5eb81a44d468bfcb47fb143536562ccb890ae7'),
                 (0x55454, 0x5546C, '3159d3745bb661398af6cbff017614e4ed474ef907dd5a089d26465a5a1d0aee')]
        for start, end, digest in spans:
            self.assertEqual(self.rom[start:end], reference[start:end])
            self.assertEqual(hashlib.sha256(self.rom[start:end]).hexdigest(), digest)
        # The native layout-index code matches; its relocated table literal differs.
        self.assertEqual(self.rom[0x55170:0x55194], reference[0x55170:0x55194])
        self.assertNotEqual(self.rom[0x55194:0x55198], reference[0x55194:0x55198])

    def test_sparse_layout_table_and_default_geometry(self):
        table = self.data['layout_lookup']['table']
        # A null hole precedes the selected custom layout IDs. It is not an end marker.
        self.assertEqual(struct.unpack_from('<I', self.rom, table + 21 * 4)[0], 0)
        for m in self.maps.values():
            site = table + (m['layout_id'] - 1) * 4
            self.assertEqual(m['indexed_layout_pointer_site'], site)
            self.assertEqual(struct.unpack_from('<I', self.rom, site)[0], 0x08000000 + m['layout'])
            self.assertTrue(m['layout_pointer_matches_indexed'])
        catalog = MapCatalog(self.rom)
        # A selected slot pointing to another real layout must not certify the old geometry.
        altered = bytearray(self.rom)
        m = self.maps['3:99']
        struct.pack_into('<I', altered, m['indexed_layout_pointer_site'], 0x08000000 + self.maps['3:100']['layout'])
        catalog.rom = altered
        self.assertEqual(catalog.resolve(3, 99)['status'], 'unresolved')

    def test_zero_tuple_is_static_and_target_return_is_dynamic(self):
        edges = [e for e in self.data['edges'] if e['kind'] == 'warp']
        returns = self.data['summary']['warp_return_relations']
        self.assertEqual(returns, {'another_map': 20, 'dynamic_return': 11, 'exact_return': 26, 'source_map_different_warp': 1})
        dynamic = [e for e in edges if e['destination']['return_relation'] == 'dynamic_return']
        self.assertEqual(len(dynamic), 11)
        self.assertEqual({e['source_map'] for e in dynamic}, {'5:86'})
        for e in dynamic:
            self.assertEqual(e['destination']['target_map'], '0:0')
            self.assertEqual(e['destination']['status'], 'warp_record_validated')
            self.assertEqual(e['destination']['landing']['destination_map'], 127)
        science = next(e for e in edges if e['source_map'] == '3:111')
        landing = science['destination']['landing']
        self.assertEqual((landing['destination_group'], landing['destination_map']), (3, 99))

    def test_null_events_and_connection_none_are_preserved(self):
        legacy = self.maps['3:60']
        self.assertIsNone(legacy['events']['offset'])
        self.assertEqual(legacy['warps'], [])
        self.assertFalse(legacy['contiguous_event_geometry'])
        self.assertEqual((legacy['width'], legacy['height']), (30, 56))
        inactive = next(c for c in legacy['connections'] if c['direction'] == 0)
        self.assertEqual((inactive['offset'], inactive['direction_name']), (0x352E5C, 'none'))
        connections = [e for e in self.data['edges'] if e['kind'] == 'connection']
        self.assertEqual(sum(bool(e['destination']['inverse_displacement_returns']) for e in connections), 7)
        self.assertTrue(all(e['destination']['geometric_overlap']['tiles'] > 0 for e in connections))

    def test_stale_or_altered_inventory_fails_and_output_reproduces(self):
        inventory = copy.deepcopy(self.inventory)
        inventory['source_sha256'] = '0' * 64
        with self.assertRaises(FormatError):
            build(self.rom, inventory)
        inventory = copy.deepcopy(self.inventory)
        inventory['maps'][0]['warps'][0]['destination_warp'] += 1
        with self.assertRaises(FormatError):
            build(self.rom, inventory)
        self.assertEqual(build(self.rom, self.inventory), self.data)
        with (ROOT / 'extracted/maps/controller_connectivity.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 71)


if __name__ == '__main__':
    unittest.main()
