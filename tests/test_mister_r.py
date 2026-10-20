"""Independent invariants for room geometry, native dispatch and state evidence."""
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from mister_r_audit import component, decoder, native_flavor, room_geometry
from map_extract import FormatError
from runtime_smoke import warp_context


class GeometryModelTests(unittest.TestCase):
    def test_component_respects_collision_elevation_and_disconnection(self):
        cells = [{'x':x,'y':y,'collision':int((x,y)==(1,1)),
                  'elevation':4 if x==2 else 3} for y in range(2) for x in range(3)]
        self.assertEqual(component(cells,3,2,(0,0)),{(0,0),(1,0),(0,1)})
        self.assertEqual(component(cells,3,2,(1,1)),set())
        self.assertEqual(component(cells,3,2,(4,4)),set())

    def test_scoped_door_widths_preserve_following_instruction(self):
        data=bytes([0xAC])+struct.pack('<HH',14,9)+bytes([0xAE,2])
        ins,error=decoder(data,0)
        self.assertIsNone(error)
        self.assertEqual(ins['values'],[14,9])
        self.assertEqual(decoder(data,ins['end'])[0]['name'],'waitdooranim')
        self.assertEqual(decoder(data[:4],0)[1],'truncated operands')

    def test_forced_context_has_only_warp_and_end_without_script_calls(self):
        data=warp_context(6,31)
        self.assertEqual(len(data),0x74)
        self.assertEqual(struct.unpack_from('<I',data,8)[0],0x03000EBC)
        self.assertEqual(data[12:21],bytes.fromhex('3d061f00ffffffff02'))
        self.assertEqual(data[0],0)  # no script return stack entries


class SuppliedMisterRTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.reference=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        cls.data=json.loads((ROOT/'extracted/maps/mister_r_diagnosis.json').read_text())

    def test_geometry_export_is_reproducible_and_all_attribute_words_match(self):
        geometry=room_geometry(self.rom)
        self.assertEqual(geometry,self.data['geometry'])
        self.assertEqual(geometry['summary']['floor_component'],74)
        for cell in geometry['cells']:
            self.assertEqual(cell['word'],struct.unpack_from('<H',self.rom,cell['offset'])[0])
            self.assertEqual(cell['attribute_word'],struct.unpack_from('<I',self.rom,cell['attribute_offset'])[0])
        by_pos={(c['x'],c['y']):c for c in geometry['cells']}
        self.assertEqual(by_pos[12,14]['behavior'],0x65)
        self.assertEqual(by_pos[20,7]['behavior'],0x6E)
        self.assertFalse(by_pos[26,2]['in_floor_component'])

    def test_only_sign_background_is_adjacent_to_floor(self):
        events=self.data['geometry']['events']
        self.assertEqual([e['index'] for e in events if e['kind']=='background' and e['adjacent_to_floor']],[1])
        object_two=next(e for e in events if e.get('local_id')==2)
        self.assertFalse(object_two['adjacent_to_floor'])
        self.assertEqual(next(e for e in events if e.get('local_id')==1)['raw_script_word'],0x08000000)

    def test_intro_movement_ends_on_floor_and_no_battle_is_encoded(self):
        intro=self.data['intro']
        self.assertEqual(intro['frontiers'],[])
        self.assertFalse(any(n['opcode']==0x5C for n in intro['instructions']))
        self.assertEqual(intro['movements'][-1]['end'],[20,10])
        for movement in intro['movements']:
            self.assertTrue(movement['terminated'])
            for step in movement['steps']:
                self.assertTrue(step['on_default_floor'])
                self.assertEqual(self.rom[step['offset']],step['opcode'])

    def test_native_dispatch_is_verified_and_rejects_changed_literal(self):
        native=native_flavor(self.rom,self.reference)
        self.assertEqual(native,self.data['native_flavor'])
        self.assertTrue(all(row['matches_reference'] for row in native['native_intervals']))
        changed=bytearray(self.rom);changed[0x6D3AC]^=1
        with self.assertRaises(FormatError):native_flavor(changed,self.reference)
        for row in native['dispatch']:
            self.assertTrue(row['script_matches_reference'])
            self.assertEqual(row['frontiers'],[])

    def test_raw_state_hits_are_retained_without_promoting_shape_to_owner(self):
        search=self.data['wider_search']
        self.assertEqual(len(search['state_raw_hits']['operand_5331']),69)
        self.assertEqual(len(search['state_raw_hits']['flag_5C5']),46)
        supported=[r for r in search['state_command_shapes'] if r['owner_witnesses']]
        self.assertEqual({r['instruction']['pc'] for r in supported},{0xAE8D7A,0xAE8DB5})
        unresolved=[r for r in search['state_command_shapes'] if r['classification']=='unresolved_raw_shape']
        self.assertEqual(len(unresolved),4)
        self.assertTrue(all(not r['owner_witnesses'] for r in unresolved))
        self.assertEqual([r['map_id'] for r in search['state_condition_owners']],['6:31'])


if __name__=='__main__':unittest.main()
