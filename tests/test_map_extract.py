"""Native lookup discovery and targeted ownership/array-span regressions."""
import csv,json,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from map_extract import LOOKUP_SIGNATURE,discover_lookup,pointer_prefix,header,FormatError

class MapDiscoveryTests(unittest.TestCase):
    def test_native_signature_and_literal_can_be_relocated(self):
        rom=bytearray(b'\xff'*0x4000)
        rom[0x100:0x118]=LOOKUP_SIGNATURE+struct.pack('<I',0x08003000)
        result=discover_lookup(rom)
        self.assertEqual(result['function'],0x100);self.assertEqual(result['table'],0x3000)

    def test_pointer_prefix_never_resumes_after_sentinel(self):
        rom=bytearray(b'\xff'*0x200)
        rom[0x10:0x20]=struct.pack('<IIII',0x08000100,0x08000110,0xF7F7F7F7,0x08000120)
        p=pointer_prefix(rom,0x10)
        self.assertEqual(p['targets'],[0x100,0x110]);self.assertEqual(p['end'],0x18)

class SuppliedMapOwnersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.data=json.loads((ROOT/'extracted/maps/controller_map_owners.json').read_text())

    def test_all_ten_roots_and_seventeen_event_sites_are_preserved(self):
        self.assertEqual(self.data['summary']['owned_roots'],10)
        self.assertEqual(len(self.data['owners']),17)
        self.assertEqual(len(self.data['maps']),10)
        self.assertFalse(self.data['unresolved_pointer_sites'])
        for row in self.data['owners']:
            self.assertEqual(struct.unpack_from('<I',self.rom,row['pointer_site'])[0],0x08000000+row['script_root'])
            self.assertEqual(row['pointer_site'],row['bg_record']+8)
            self.assertEqual(row['bg_record'],row['bg_array']+row['bg_index']*12)
            self.assertEqual(struct.unpack_from('<HH',self.rom,row['bg_record']),(row['x'],row['y']))
            self.assertEqual(row['reachability'],'UNKNOWN')

    def test_event_arrays_and_layout_coordinates_are_independently_consistent(self):
        maps={(m['group'],m['map']):m for m in self.data['maps']}
        for m in maps.values():
            self.assertTrue(m['contiguous_event_geometry'])
            ev=m['events']
            for i,stride in enumerate((24,8,16,12)):
                end=ev['arrays'][i]+ev['counts'][i]*stride
                self.assertEqual(end,ev['arrays'][i+1] if i<3 else ev['offset'])
        for row in self.data['owners']:
            m=maps[row['group'],row['map']]
            self.assertLess(row['x'],m['width']);self.assertLess(row['y'],m['height'])

    def test_reused_scripts_and_map_slots_are_not_deduplicated(self):
        rows=[o for o in self.data['owners'] if (o['group'],o['map'])==(5,86)]
        self.assertEqual([(o['x'],o['y']) for o in rows],[(116,14),(117,14)])
        self.assertEqual({o['script_root'] for o in rows},{0xAD3E78})
        keys={(m['group'],m['map']) for m in self.data['maps']}
        self.assertIn((3,101),keys);self.assertIn((3,107),keys)

    def test_bank_prefix_survives_invalid_legacy_map_layout(self):
        bank=self.data['owner_bank_physical_prefixes']['6']
        self.assertEqual((bank['end']-bank['start'])//4,32)
        invalid=struct.unpack_from('<I',self.rom,bank['start']+4*4)[0]-0x08000000
        with self.assertRaises(FormatError):header(self.rom,invalid)
        self.assertTrue(any(m['group']==6 and m['map']==23 for m in self.data['maps']))

    def test_section_name_lookup_and_warp_export_match_rom(self):
        maps={(m['group'],m['map']):m for m in self.data['maps']}
        self.assertEqual(maps[3,111]['section_label']['text'],'SCIENCE COMPLEX')
        self.assertEqual(maps[5,102]['section_label']['text'],'NEXUS LABORATORY')
        self.assertEqual(maps[6,23]['section_label']['text'],'MANDARIN CITY')
        warps=[w for m in maps.values() for w in m['warps']]
        self.assertEqual(len(warps),58)
        for w in warps:
            x,y,el,wid,num,grp=struct.unpack_from('<hhBBBB',self.rom,w['offset'])
            self.assertEqual((x,y,el,wid,num,grp),(w['x'],w['y'],w['elevation'],w['destination_warp'],w['destination_map'],w['destination_group']))
        with (ROOT/'extracted/maps/controller_map_warps.csv').open() as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),58)

if __name__=='__main__':unittest.main()
