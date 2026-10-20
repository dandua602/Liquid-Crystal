"""Replay evidence: earned state, disposable persistence and fixture limits."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from orange_progression_audit import decoder

class LinkedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence=json.loads((ROOT/'extracted/runtime/linked/linked.json').read_text())
        cls.checks={r['label']:r for r in cls.evidence['checks']}

    def test_completed_current_source_replay_has_no_failed_expectation(self):
        self.assertTrue(self.evidence['complete']);self.assertTrue(self.evidence['source_unchanged'])
        rom=(ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes()
        self.assertEqual(self.evidence['source_sha256']['rom'],hashlib.sha256(rom).hexdigest())
        checks=[r for r in self.evidence['checks'] if 'passed'in r]
        self.assertEqual(len(checks),21);self.assertTrue(all(c['passed'] for c in checks))
        for label in ['laboratory_awarded_g_rank','police_awarded_old_key','old_key_unlock_from_interaction']:
            self.assertEqual(self.checks[label]['actual'],1)

    def test_journey_uses_two_entry_warps_and_no_injected_story_state(self):
        warps=[]
        for row in self.evidence['transcript']:
            if not row['command'].startswith('w 3000eb0 '):continue
            script=bytes.fromhex(row['command'].split()[2])[12:92];pc=0
            while pc<len(script):
                node,error=decoder(script,pc);self.assertIsNone(error)
                self.assertIn(node['opcode'],{2,0x2B,0x3D,0x47,0x7B})
                if node['opcode']==0x3D:warps.append(node['values'][:2])
                if node['opcode']==2:break
                pc=node['end']
        self.assertEqual(warps,[[5,102],[6,27]])
        self.assertGreater(len(self.evidence['steps']),100)
        self.assertTrue(any('fresh_process'in row['response'] for row in self.evidence['transcript']))

    def test_new_process_preserves_key_and_extended_intro_variable(self):
        for label in ['reloaded_intro_state','reloaded_flag_5BA','reloaded_flag_5C1','reloaded_flag_5C5','reloaded_old_key']:
            self.assertEqual(self.checks[label]['actual'],1)
        self.assertEqual(self.checks['reloaded_room']['actual'],[6,31])
        state=self.checks['save_mapper_state']['state']
        self.assertTrue(state['banked_sram']);self.assertTrue(state['embedded_nor_save'])
        self.assertEqual(state['nor_erases'],2);self.assertEqual(state['nor_programs'],65536)

    def test_generated_save_is_labelled_and_keeps_source_separate(self):
        metadata=json.loads((ROOT/'saves/test/linked-orange-fixture.json').read_text())
        self.assertEqual(metadata['source_save_sha256'],self.evidence['source_sha256']['save'])
        self.assertEqual(metadata['bytes'],131072)
        self.assertIn('not a normal player save',metadata['warning'])
        fixture=ROOT/'saves/test'/metadata['filename']
        if fixture.exists():self.assertEqual(hashlib.sha256(fixture.read_bytes()).hexdigest(),metadata['sha256'])

if __name__=='__main__':unittest.main()
