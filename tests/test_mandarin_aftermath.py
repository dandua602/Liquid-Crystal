"""Review preview guards and independently observed original aftermath behavior."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from p003_design import DIGEST, preflight


class MandarinAftermathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
        cls.design = json.loads((ROOT/'research/design/p003.json').read_text())

    def test_preview_rejects_wrong_source_unsafe_gate_state_and_overflow(self):
        self.assertEqual(hashlib.sha256(self.rom).hexdigest(), DIGEST)
        result = preflight(self.rom, self.design)
        self.assertTrue(result['no_ROM_output_created'])
        self.assertTrue(all(result['used'][k] <= result['capacities'][k] for k in result['used']))
        with self.assertRaises(ValueError):
            preflight(b'wrong source', self.design)
        for key, value in [('gate', {'variable': 0x5331, 'value': 0x3303, 'trainer_id': 929, 'trainer_bit_required': False}),
                           ('aftermath_flag', 0x5B6), ('messages', dict(self.design['messages'], prompt='X'*400))]:
            changed = copy.deepcopy(self.design); changed[key] = value
            with self.assertRaises(ValueError):
                preflight(self.rom, changed)

    def test_original_branch_and_object_observations_are_hash_bound(self):
        data = json.loads((ROOT/'extracted/runtime/mandarin_aftermath/aftermath.json').read_text())
        self.assertEqual(data['rom_sha256'], DIGEST)
        self.assertTrue(data['complete']); self.assertTrue(data['source_unchanged'])
        checks = {c['label']: c for c in data['checks'] if 'passed' in c}
        self.assertEqual(len(checks), 10)
        self.assertTrue(all(c['passed'] for c in checks.values()))
        for value, address in [(False, 0x930F2A), (True, 0x930ED2)]:
            self.assertEqual(checks[f'original_city_branch_{value}']['actual'], 0x08000000+address)
            self.assertEqual(checks[f'original_scientist_visibility_{value}']['actual'], not value)
            self.assertTrue(checks[f'hostile_actor_still_present_{value}']['actual'])
        self.assertEqual(data['post_branch_empty_text']['text'], '')
        self.assertEqual(checks['original_hostile_branch_True']['actual'], 0x089314DA)
        self.assertEqual(data['center_hostile_object']['offset']+20, 0xC0B550)


if __name__ == '__main__':
    unittest.main()
