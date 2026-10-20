"""Meaningful BPS vectors and exact-source/changed-range build checks."""
import hashlib
import json
import struct
import sys
import unittest
import zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from bps_patch import apply,create
from build_p001 import build
from orange_progression_audit import decoder


class BPSTests(unittest.TestCase):
    def test_known_literal_and_source_read_vector(self):
        source=b'abc';target=b'aZc'
        patch=b'BPS1\x83\x83\x80\x80\x81Z\x80'+struct.pack('<II',zlib.crc32(source),zlib.crc32(target))
        patch+=struct.pack('<I',zlib.crc32(patch))
        self.assertEqual(apply(source,patch),target)
        self.assertEqual(create(source,target),patch)

    def test_varint_boundaries_and_rejection_of_wrong_or_corrupted_inputs(self):
        source=bytes(range(256))*130;target=source[:127]+b'x'*130+source[257:]
        patch=create(source,target)
        self.assertEqual(apply(source,patch),target)
        self.assertEqual(apply(target,create(target,source)),source)
        with self.assertRaises(ValueError):apply(b'bad',patch)
        with self.assertRaises(ValueError):apply(source,patch[:-1]+bytes([patch[-1]^1]))


class BuiltP001Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes();cls.target=(ROOT/'builds/dev/Liquid Crystal P001.gba').read_bytes()
        cls.manifest=json.loads((ROOT/'builds/dev/P001-manifest.json').read_text());cls.design=json.loads((ROOT/'research/design/p001.json').read_text())

    def test_wrong_source_is_rejected_and_every_changed_byte_has_a_manifest_owner(self):
        with self.assertRaises(ValueError):build(b'wrong source',self.design)
        self.assertEqual(hashlib.sha256(self.target).hexdigest(),self.manifest['output_sha256'])
        allowed=self.manifest['writes'];changed=[i for i,(a,b)in enumerate(zip(self.source,self.target))if a!=b]
        self.assertGreater(len(changed),500)
        self.assertTrue(all(any(r['start']<=i<r['end_exclusive']for r in allowed)for i in changed))
        self.assertEqual(self.source[0xC00000:0xD00000],self.target[0xC00000:0xC30A24]+self.source[0xC30A24:0xC30A2C]+self.target[0xC30A2C:0xD00000])
        self.assertEqual(self.source[0xA0:0xC0],self.target[0xA0:0xC0])

    def test_produced_forward_and_reverse_bps_restore_exact_bytes(self):
        self.assertEqual(apply(self.source,(ROOT/'builds/dev/P001.bps').read_bytes()),self.target)
        self.assertEqual(apply(self.target,(ROOT/'builds/dev/P001-reverse.bps').read_bytes()),self.source)

    def test_compiled_script_stream_is_decodable_and_uses_native_continuation(self):
        at=0xB9EF00;end=at+self.manifest['capacities_used']['scripts'];battles=[]
        while at<end:
            node,error=decoder(self.target,at);self.assertIsNone(error)
            if node['opcode']==0x5C:battles.append(node)
            at=node['end']
        self.assertEqual(at,end);self.assertEqual(len(battles),1)
        self.assertEqual(battles[0]['values'][:3],[1,929,1])
        self.assertLessEqual(self.manifest['capacities_used']['scripts'],640)
        self.assertEqual(self.target[0xB9F4E0:0xB9F700],b'\xff'*544)

    def test_retained_acceptance_is_complete_and_bound_to_this_output(self):
        for name in ('matrix','puzzle','win','loss','persistence','exits','edge','regression','regions'):
            with self.subTest(case=name):
                result=json.loads((ROOT/f'extracted/runtime/p001/{name}/{name}.json').read_text())
                self.assertTrue(result['complete']);self.assertTrue(result['source_unchanged'])
                self.assertEqual(result['rom_sha256'],self.manifest['output_sha256'])
                checks=[row for row in result['checks']if 'passed'in row]
                self.assertGreater(len(checks),0);self.assertTrue(all(row['passed']for row in checks))


if __name__=='__main__':unittest.main()
