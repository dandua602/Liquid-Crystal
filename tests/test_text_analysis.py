"""Boundary regressions for read-only archaeology; ROM fixtures stay local/ignored."""
import json,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from gba_text_codec import encode,decode,parse,fold_case
from pointer_scan import classify_operand,index_pointers
from text_extract import is_glyph_hit
from text_reference_trace import decode_linear

class TextFormatTests(unittest.TestCase):
    def test_eos_inside_sound_parameters_does_not_truncate(self):
        b=b'\xfc\x0b\xff\x01'+encode('Orange Islands')+b'\xff'
        p=parse(b,strict_english=True)
        self.assertTrue(p['terminated']);self.assertEqual(p['end'],len(b))
        self.assertEqual(p['plain'],'Orange Islands')
        self.assertEqual(p['tokens'][0]['raw'],'fc0bff01')

    def test_combined_color_and_player_placeholder(self):
        b=b'\xfc\x04\x01\x02\x03'+encode('Hello ')+b'\xfd\x01\xff'
        p=parse(b,strict_english=True)
        self.assertEqual(p['plain'],'Hello {PLAYER}')
        self.assertEqual(p['tokens'][1]['offset'],5)

    def test_unknown_control_cannot_certify_a_boundary(self):
        self.assertIsNone(parse(b'\xfc\x99'+encode('Orange')+b'\xff',strict_english=True))

    def test_truncated_control_is_not_a_complete_string(self):
        p=parse(encode('Orange')+b'\xfc\x04\x01',strict_english=True)
        self.assertFalse(p['terminated']);self.assertTrue(p['issues'])

    def test_keyword_in_control_payload_is_not_dialogue(self):
        b=b'\xfc\x04'+encode('Ora')+b'\xff'
        p=parse(b,strict_english=True)
        self.assertFalse(is_glyph_hit(p,2,3))

    def test_case_search_and_accents(self):
        self.assertEqual(fold_case(encode('ORANGE')),fold_case(encode('Orange')))
        self.assertEqual(decode(encode('Pokémon & 99%')),'Pokémon & 99%')

    def test_msgbox_pointer_need_not_be_aligned(self):
        b=bytearray(64);b[1:9]=b'\x0f\x00'+struct.pack('<I',0x08000030)+b'\x09\x02'
        self.assertIn(3,index_pointers(b)[48])
        ref=classify_operand(b,3)
        self.assertEqual(ref['kind'],'MSGBOX_SHAPE');self.assertFalse(ref['aligned_4'])

    def test_trainer_intro_and_defeat_are_separate_operands(self):
        b=bytearray(96);b[0:14]=b'\x5c\x00\x95\x03\x00\x00'+struct.pack('<II',0x08000040,0x08000050)
        ref=classify_operand(b,10)
        self.assertEqual(ref['kind'],'TRAINER_TEXT_SHAPE')
        self.assertEqual(ref['trainer_id'],0x395);self.assertEqual(ref['text_operand_index'],1)

class LocalRomRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()

    def test_mandarin_sign_starts_after_padding(self):
        p=parse(self.rom,0x930C7D,strict_english=True)
        self.assertTrue(p['terminated'])
        self.assertEqual(p['plain'],'Mandarin City Pokémon Gym\nLeader: Rudy\nThe Mysterious Playboy')
        self.assertEqual(classify_operand(self.rom,0x9302ED)['kind'],'MSGBOX_SHAPE')

    def test_danny_badge_control_sequence_is_consumed(self):
        p=parse(self.rom,0xB11C47,strict_english=True)
        self.assertTrue(p['terminated']);self.assertFalse(p['issues'])
        self.assertIn('Sea Ruby Badge is the second',p['plain'])
        self.assertIn('<PLAY_BGM 04 01>',p['text'])
        self.assertNotIn('ÇÀ',p['plain'])

    def test_uppercase_valencia_and_ivy_dialogue_is_recovered(self):
        audit=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text())
        record=next(e for e in audit['records'] if e['offset']=='0x9d5a78')
        self.assertIn('IVY: There you are!',record['plain_text'])
        self.assertIn('GS BALL',record['plain_text'])
        self.assertTrue(any(r['kind']=='MSGBOX_SHAPE' for r in record['references']))

    def test_mister_g_linear_trace_reaches_revised_speech(self):
        trace=decode_linear(self.rom,0xAAAF9A,0xAAAFBA)
        self.assertTrue(trace['contains_required_command_at_instruction_boundary'])
        instruction=next(x for x in trace['instructions'] if x['offset']=='0xaaafba')
        self.assertEqual(instruction['name'],'loadword')
        self.assertEqual(instruction['operands'],['0x0','0x8b1d4e0'])

    def test_trace_never_skips_an_unsupported_byte(self):
        trace=decode_linear(b'\xff\x0f\x00\x20\x00\x00\x08\x02',0,1)
        self.assertFalse(trace['contains_required_command_at_instruction_boundary'])
        self.assertIn('unsupported opcode',trace['stop_reason'])

    def test_generated_offsets_match_source_bytes(self):
        audit=json.loads((ROOT/'extracted/text/orange_text_audit.json').read_text())
        total=0
        for record in audit['records']:
            start=int(record['offset'],16);end=int(record['end_offset_exclusive'],16)
            self.assertEqual(self.rom[end-1],255)
            self.assertEqual(record['length_bytes'],end-start)
            for token in record['tokens']:
                self.assertEqual(self.rom[token['offset']:token['end']].hex(),token['raw'])
            for ref in record['references']+record['interior_references']:
                site=int(ref['offset'],16)
                self.assertEqual(int.from_bytes(self.rom[site:site+4],'little'),0x08000000+int(ref['target'],16))
            total+=len(record['keyword_hits'])
        self.assertEqual(total,audit['summary']['accepted_keyword_hits'])
        self.assertEqual(total+len(audit['unresolved_hits']),audit['summary']['raw_keyword_hits'])

if __name__=='__main__':unittest.main()
