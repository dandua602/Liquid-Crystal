"""Safety collision ownership and actual affected-route acceptance."""
import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_p002a import build,SITE,BEFORE,AFTER


class SafetyFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
        cls.target=build(cls.source)

    def test_only_collision_changes_and_sources_header_driver_save_stay_exact(self):
        self.assertEqual(self.source[SITE:SITE+2],BEFORE);self.assertEqual(self.target[SITE:SITE+2],AFTER)
        self.assertEqual(self.source[:SITE],self.target[:SITE]);self.assertEqual(self.source[SITE+2:],self.target[SITE+2:])
        a=int.from_bytes(BEFORE,'little');b=int.from_bytes(AFTER,'little')
        self.assertEqual(a&~0xC00,b&~0xC00);self.assertEqual((b>>10)&3,3)
        with self.assertRaises(ValueError):build(b'wrong ROM')

    def test_hash_bound_route_safety_puzzle_office_and_reload_checks_pass(self):
        report=json.loads((ROOT/'extracted/runtime/stadium/p002a/p002a.json').read_text())
        self.assertTrue(report['complete']);self.assertEqual(report['rom_sha256'],hashlib.sha256(self.target).hexdigest())
        checks={c['label']:c for c in report['checks']if'passed'in c}
        self.assertTrue(all(c['passed']for c in checks.values()))
        for label in ['blocked_stair_keeps_position','north_approach_blocked_1','north_approach_blocked_13059','puzzle_still_solves','solved_rock_still_absent','completion_survives_hotfix_save_reload','trainer_bit_survives_hotfix_save_reload','actual_south_exit_route59']:
            self.assertIn(label,checks)


if __name__=='__main__':unittest.main()
