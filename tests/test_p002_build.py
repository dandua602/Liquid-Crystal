"""P002 bank preservation, changed-range ownership and native acceptance."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_p002 import build
from bps_patch import apply
from orange_progression_audit import decoder
from warp_graph import MapCatalog


class P002Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();cls.p001=(ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes()
        cls.target=(ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes();cls.design=json.loads((ROOT/'research/design/p002.json').read_text())
        cls.manifest=json.loads((ROOT/'builds/dev/P002-manifest.json').read_text())

    def test_wrong_input_rejected_and_every_delta_byte_owned(self):
        with self.assertRaises(ValueError):build(self.original,self.design)
        self.assertEqual(hashlib.sha256(self.target).hexdigest(),self.manifest['output_sha256'])
        writes=self.manifest['writes_relative_to_p001'];changed=[i for i,(a,b)in enumerate(zip(self.p001,self.target))if a!=b]
        self.assertGreater(len(changed),300)
        self.assertTrue(all(any(w['start']<=i<w['end_exclusive']for w in writes)for i in changed))
        self.assertEqual(self.p001[0xC00000:0xD00000],self.target[0xC00000:0xD00000])
        self.assertEqual(self.p001[0xA0:0xC0],self.target[0xA0:0xC0])

    def test_all_existing_bank_words_preserved_and_new_map_layout_resolves(self):
        self.assertEqual(self.target[0xB9F600:0xB9F680],self.p001[0xC13EB8:0xC13F38])
        self.assertEqual(self.target[0xC13EB8:0xC13F38],self.p001[0xC13EB8:0xC13F38])
        catalog=MapCatalog(self.target);room=catalog.resolve(6,32);donor=catalog.resolve(5,123)
        self.assertEqual(room['status'],'structure_validated');self.assertEqual(room['layout'],donor['layout'])
        self.assertTrue(room['layout_pointer_matches_indexed']);self.assertEqual(room['events']['counts'],[1,1,0,0])
        self.assertEqual((room['warps'][0]['destination_group'],room['warps'][0]['destination_map'],room['warps'][0]['destination_warp']),(6,31,0))
        # Original city blockers, scripts, warp records and layout data stay exact.
        city=MapCatalog(self.p001).resolve(3,109);newcity=catalog.resolve(3,109)
        self.assertEqual(city,newcity)

    def test_all_four_patch_directions_restore_exact_input(self):
        for name,source,target in [('P002.bps',self.original,self.target),('P002-reverse.bps',self.target,self.original),
                                   ('P001-to-P002.bps',self.p001,self.target),('P002-to-P001.bps',self.target,self.p001)]:
            with self.subTest(patch=name):self.assertEqual(apply(source,(ROOT/'builds/dev'/name).read_bytes()),target)

    def test_p002_scripts_preserve_only_owned_solved_write_and_acceptance_matches_output(self):
        at=0xB9F4E0;end=at+self.manifest['capacities_used']['scripts'];nodes=[]
        while at<end:
            node,error=decoder(self.target,at);self.assertIsNone(error);nodes.append(node);at=node['end']
        self.assertEqual(at,end)
        self.assertFalse(any(n['opcode']in(0x17,0x18,0x29,0x2A,0x44,0x45,0x5C,0x61,0x62,0x79,0x90)for n in nodes))
        self.assertEqual([n['values']for n in nodes if n['opcode']==0x16],[[0x5331,0x3302]])
        self.assertTrue(any(n['opcode']==0x60 and n['values']==[929]for n in nodes))
        for case in ('access','journey','matrix','puzzle','loss','exits','rollback'):
            data=json.loads((ROOT/f'extracted/runtime/p002/{case}/{case}.json').read_text())
            with self.subTest(case=case):
                self.assertTrue(data['complete']);self.assertTrue(data['source_unchanged'])
                self.assertEqual(data['rom_sha256'],self.manifest['output_sha256'])
                self.assertTrue(all(c['passed']for c in data['checks']if'passed'in c))


if __name__=='__main__':unittest.main()
