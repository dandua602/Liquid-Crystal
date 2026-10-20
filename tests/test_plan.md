# Faster validation workflow

The project test suite runs in seconds; exact current totals are recorded in
extracted/runtime/validation_summary.json.
The bottleneck is recovering requirements and proving allocation, rather than
running those tests. Group work into substantial design/build/acceptance batches.

## Resume or documentation-only work

Read PROJECT_STATE.md and research/remaining_work.md, then verify original
sources with `python3 tools/verify_sources.py`. Do not regenerate every inventory
or replay unchanged journeys. Existing artifacts retain exact source hashes and
their fixture limits; reusing them is not a fresh runtime execution.

## During a code or evidence change

Run the affected unittest file, for example
`python3 -m unittest discover -s tests -p 'test_allocation.py' -v`.
Rebuild only an artifact whose inputs or generator changed. Rerun an emulator
case when its frontend, fixture, native assumptions or tested ROM behavior changes.
The allocation case is `python3 tools/allocation_runtime.py`; it uses native
commands, actual game Save and a fresh process on disposable copies.

## At a completed milestone

Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` and
`python3 tools/verify_sources.py` once; retain the result. Check pinned references
through the existing suite. State which runtime cases were newly executed and
which current-source artifacts were retained. Publish a substantial checkpoint,
not each passing check. A documentation or audit change does not require replaying
the whole train/laboratory/police journey.

## P001 prototype acceptance (implemented)

The user approved implementation. Test the new puzzle directly from recorded
pre-intro, consumed-intro, solved/retry and completed fixtures. Cover absent move,
win/loss/escape, repeat reward, save/reload and exact exits. Check deterministic
builds, expected-original bytes, allowed changed ranges, headers and reversible
patching. Then run affected linked journeys and a broader compatibility pass once.
Use real hardware for cartridge compatibility; emulator success cannot replace it.

The warehouse native-feasibility case is `python3 tools/warehouse_primitives.py`:
move-presence fixtures and existing laboratory victory/controller escape are used
to verify actual native return semantics. It was newly executed for the result
reader change, not as a redundant full journey replay. P001 static budget checks
are `python3 tools/p001_preflight.py`; neither command implements the warehouse.

P001 commands: `python3 tools/build_p001.py`, then the relevant
`python3 tools/p001_runtime.py --case NAME`. Cases are matrix, puzzle, win, loss,
persistence, exits, edge, regression and regions. All nine retained results must
match the output hash before packaging. `python3 tools/package_p001.py` enforces
that requirement and verifies exact forward/reverse patching. Unit tests check
CRC corruption, known BPS vectors, changed-range ownership and compiled bytecode.

Regression replays cover laboratory, police/Old Key through the warehouse and
bounded Johto/Kanto field controls. Entry/train evidence on the original source
is retained, not freshly replayed on every patch. Preserve frozen reviewed ledgers;
do not regenerate architecture_audit.py reports during routine resume.

## Player walkthrough requirement

For every new playable story slice, update WALKTHROUGH.md with prerequisites,
route directions, exact interactions, puzzle solution, battle/retry/save behavior,
rewards and the actual endpoint. Add observed screenshots or route diagrams.
Keep unreleased previews separate and labeled. Package the guide/images with
the patch and verify relative links. This is an explicit continuing user requirement.

Native-stat combat probes are tools/p001_combat_probe.py --level 95 or --level 100. They use fixed first-move input and normal
calculated stats/PP, not difficulty certification. P002 sizing is tools/p002_design.py;
it produces only a data preview, never a ROM. Office asset/doorway evidence uses
explicit disposable visibility flags and is not normal earlier-story progression.

## P002 approved implementation

Build tools/build_p002.py after exact P001. Current P002 acceptance is
`python3 tools/p002_runtime.py --case NAME`: access, journey, matrix, puzzle, loss,
exits and rollback. Run journey before rollback when regenerating saves. All
seven results must match the exact P002 output for tools/package_p002.py.

New movement checks cover the flagless-rock respawn missed by immediate removal
checks. The current fix preserves P001 entry addresses with two same-size calls
and uses existing template coords outside the room; no new flag/variable. Test
both field moves, movement/reentry, original introduction and completed reload.
Rollback acceptance really saves outside the new map and boots exact P001 in a
fresh process; BPS CRC roundtrip alone cannot establish save compatibility.

WALKTHROUGH.md is the latest playable guide; archive older version-specific guides
and keep frozen review previews unchanged. Package the current guide with the
matching patch, check its relative image links and inspect actual screenshots.
