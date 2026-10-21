"""P002a safety fix: seal the inherited staircase into the invalid link room.

Only the collision bits of warehouse cell20,7 change. Original source files,
P002 build and every save remain untouched; no story content/state is added.
"""
import hashlib
import json
from pathlib import Path
from bps_patch import create, apply

ROOT = Path(__file__).resolve().parents[1]
P002_SHA = '9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70'
SITE = 0xC30C2C
BEFORE, AFTER = bytes.fromhex('5d32'), bytes.fromhex('5d3e')


def build(source):
    if hashlib.sha256(source).hexdigest() != P002_SHA or source[SITE:SITE+2] != BEFORE:
        raise ValueError('Expected exact P002')
    out = source[:SITE]+AFTER+source[SITE+2:]
    if out[:SITE] != source[:SITE] or out[SITE+2:] != source[SITE+2:]:
        raise ValueError('Unowned change')
    return out


def main():
    source = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    target = build(source)
    patch = create(source, target, b'P002a safety fix; seal inherited link-Colosseum stair; no new story')
    reverse = create(target, source, b'P002a reverse')
    if apply(source, patch) != target or apply(target, reverse) != source:
        raise ValueError('Patch roundtrip failed')
    manifest = {'id': 'P002a', 'kind': 'Safety bugfix for reported invalid stadium encounter, not a new story chapter',
                'input_sha256': P002_SHA, 'output_sha256': hashlib.sha256(target).hexdigest(),
                'writes': [{'site': SITE, 'before': BEFORE.hex(), 'after': AFTER.hex(), 'cell': [20, 7],
                            'map': [6, 31], 'role': 'collision0 to3; preserve tile art and elevation'}],
                'new_state_allocated': False, 'save_data_changed': False, 'hardware_tested': False,
                'block_ownership_evidence': {'block_pointer_site': 0xC30F10, 'map_block_array': 0xC30A44,
                                             'retained_validated_map_associations': [[6,31]],
                                             'scope': 'Raw08/0A/0C pointer shapes and retained valid-header inventory; unknown computed users excluded'},
                'limits': 'Prevents normal walking into the legacy stair; does not repair a saved game already in map0:0 or damaged battle data.'}
    (ROOT/'builds/dev/Liquid Crystal P002a.gba').write_bytes(target)
    (ROOT/'builds/dev/P002-to-P002a.bps').write_bytes(patch)
    (ROOT/'builds/dev/P002a-to-P002.bps').write_bytes(reverse)
    (ROOT/'extracted/builds/P002a-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
