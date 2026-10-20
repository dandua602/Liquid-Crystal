"""Historical keyword-miss recovery, malformed boundaries, and weak-reference checks."""
import json,hashlib,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from gba_text_codec import parse,encode,fold_case

class DynamicTokenTests(unittest.TestCase):
    def test_dynamic_index_is_preserved_and_not_rendered_as_glyph(self):
        p=parse(b'\xf7\x01'+encode(' is CHAMPION')+b'\xff',strict_english=True)
        self.assertTrue(p['terminated']);self.assertFalse(p['issues'])
        self.assertEqual(p['plain'],'{DYNAMIC_01} is CHAMPION')
        self.assertEqual(p['tokens'][0]['raw'],'f701')

    def test_ff_dynamic_index_is_data_not_terminator(self):
        b=b'\xf7\xff'+encode('Hello')+b'\xff';p=parse(b,strict_english=True)
        self.assertEqual(p['plain'],'{DYNAMIC_FF}Hello');self.assertEqual(p['end'],len(b))

    def test_truncated_dynamic_token_is_not_certified_complete(self):
        p=parse(b'\xf7',strict_english=True)
        self.assertFalse(p['terminated']);self.assertTrue(p['issues'])

class SuppliedTextTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        cls.frozen=json.loads((ROOT/'extracted/text/text_triage_input.json').read_text())
        cls.triage=json.loads((ROOT/'extracted/text/text_boundary_triage.json').read_text())
        cls.weak=json.loads((ROOT/'extracted/text/orphan_reference_audit.json').read_text())

    def test_every_historical_hit_is_preserved_with_exact_glyph_bytes(self):
        original={(x['term'],x['offset']) for x in self.frozen['unresolved_hits']}
        current={(x['term'],x['offset']) for x in self.triage['hits']}
        self.assertEqual(len(original),53);self.assertEqual(original,current)
        for term,offset in current:
            at=int(offset,16);needle=encode(term)
            self.assertEqual(fold_case(self.rom[at:at+len(needle)]),fold_case(needle))

    def test_full_oak_and_sunburst_text_precede_accidental_interior_hits(self):
        records={r['offset']:r for r in self.triage['recovered_text']}
        self.assertIn('OAK: Ah!',records['0x969854']['plain_text'])
        self.assertIn('Sunburst Island',records['0xaaa9dc']['plain_text'])
        main=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text())
        offsets={r['offset'] for r in main['records']}
        self.assertIn('0x969854',offsets);self.assertIn('0xaaa9dc',offsets)
        self.assertNotIn('0x96999a',offsets);self.assertNotIn('0xaaaa35',offsets)

    def test_rank_prose_has_no_eos_and_script_operand_is_not_a_valid_text_boundary(self):
        bounded=parse(self.rom,0xAAAF41,limit=89,strict_english=True)
        self.assertFalse(bounded['terminated']);self.assertFalse(bounded['issues'])
        self.assertEqual(bounded['end'],0xAAAF9A)
        self.assertEqual(self.rom[0xAAAF99:0xAAAFA1],bytes.fromhex('ad 4f ff 00 f4 ce ab 08'))
        self.assertIsNone(parse(self.rom,0xAAAF41,limit=91,strict_english=True))
        permissive=parse(self.rom,0xAAAF41,limit=91)
        self.assertTrue(permissive['terminated']);self.assertTrue(permissive['issues'])

    def test_same_item_id_uses_rank_name_and_description_across_two_tables(self):
        for base in (0x3DB028,0x9990AC):
            row=base+44*0x114
            self.assertEqual(struct.unpack_from('<H',self.rom,row+14)[0],0x114)
            self.assertEqual(struct.unpack_from('<I',self.rom,row+20)[0],0x08AAAF41)
        self.assertEqual(parse(self.rom,0x9990AC+44*0x114,limit=14)['plain'],'G Rank')
        self.assertEqual(struct.unpack_from('<I',self.rom,0x9A98C)[0],0x083DB028)
        self.assertEqual(struct.unpack_from('<I',self.rom,0x9A8D8)[0],0x089990AC)
        fr=(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba').read_bytes()
        self.assertEqual(self.rom[0x9A96C:0x9A990],fr[0x9A96C:0x9A990])

    def test_binary_repetition_is_verified_without_unused_claim(self):
        groups=self.triage['repeated_windows']
        self.assertEqual(len(groups),2)
        for group in groups:
            self.assertEqual(len(group['hit_offsets']),11)
            for offset in group['hit_offsets']:
                at=int(offset,16)
                self.assertEqual(hashlib.sha256(self.rom[at-45:at+90]).hexdigest(),group['sha256'])
        self.assertEqual(self.triage['summary']['unused_or_unreachable_certifications'],0)

    def test_weak_reference_partition_and_no_unused_certification(self):
        rows=self.weak['records']
        self.assertEqual(len(rows),64)
        self.assertTrue(all(r['unused_status']=='UNKNOWN' and r['reachability']=='UNKNOWN' for r in rows))
        by_offset={r['offset']:r for r in rows}
        self.assertEqual(by_offset['0x918e17']['facts']['data_kind'],'applymovement_shape')
        self.assertEqual(by_offset['0x997e34']['facts']['data_kind'],'pokemart_shape')
        self.assertEqual(by_offset['0x23e830']['classification'],'INLINE_NAME_FIELD')
        self.assertEqual(by_offset['0xac8525']['facts']['name_start'],'0xac8528')
        self.assertEqual(by_offset['0xac8525']['facts']['record_index'],'0x364')

if __name__=='__main__':unittest.main()
