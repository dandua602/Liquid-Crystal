# Liquid Crystal completion project

**[Make the cartridge test ROM—offline patcher v2](patches/P002/P002-easy-cartridge-test-v2.zip)** ·
**[Download P002](patches/P002/P002-prototype.zip)** ·
**[Read the walkthrough](WALKTHROUGH.md)** ·
**[Where everything is on GitHub](GITHUB.md)**

The approved **P002 prototype** includes the warehouse Iron Tail / Rock Smash
puzzle, six-member Mister R battle and a new Office Block service room reached
after victory. Its normal door returns to the warehouse. It also fixes the
cleared rock respawning after movement. Original inputs remain unchanged.
Main Office floors, later islands and the ending remain future work.

- [Real-console cartridge test instructions](HARDWARE_TEST.md) and [public patch/helper kit](patches/P002/P002-cartridge-tools.zip)
- [Player walkthrough with directions, route map and screenshots](WALKTHROUGH.md)
- [P002 implementation and exact test scope](research/P002_implementation.md)
- [P002 build manifest](extracted/builds/P002-manifest.json) and [acceptance](extracted/builds/P002-validation.json)
- [Next chapter proposal: P003 communications shutdown](research/P003_review.md) (review only)
- [Current state](PROJECT_STATE.md) and [remaining work](research/remaining_work.md)
- [Frozen P002 proposal](research/P002_review.md) and [implementation approval](research/design/p002_approval.json)
- [Earlier P001 implementation](research/P001_implementation.md), [native-stat combat](research/P001_native_combat.md) and [P001-only guide](walkthrough/P001.md)

Use `builds/P002-prototype.zip`. Its standalone patch applies to the exact original
supplied Liquid Crystal ROM and includes P001; its upgrade patch applies to exact
P001. Four patch directions support original/P001 installation and rollback.
No ROM/save is included in the ZIP. The built ROM is
`builds/dev/Liquid Crystal P002.gba`. Back up your personal save and use a copy.
Before removing P002, leave its new room and save in the original warehouse.

On GitHub, the same patch-only download and its instructions are in
[`patches/P002/`](patches/P002/). Original ROMs and saves are excluded.

From the existing `/workspace/Liquid-Crystal` checkout:

```sh
python3 tools/verify_sources.py
python3 tools/build_p001.py
python3 tools/build_p002.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/package_p002.py
```

Python 3.12 standard library suffices for build, static analysis and packaging.
For emulator development, `python3 tools/setup_runtime.py` builds/verifies pinned
mGBA 0.10.5 outside the checkout. No service needs starting. Replays use disposable
copies and recorded map/state/party fixtures; neither enemy HP nor outcomes are
injected. See [test plan](tests/test_plan.md) before rerunning unchanged cases.

```sh
python3 tools/p001_runtime.py --case puzzle
python3 tools/p001_runtime.py --case win
```

P001-only cases retain their original tools. Current P002 runtime uses
`python3 tools/p002_runtime.py --case NAME` with access, journey, matrix, puzzle,
loss, exits or rollback. Run journey before rollback when regenerating fixtures.
Retained runtime artifacts are hash-bound to the actual tested output ROM. Primary victory coverage uses a boosted native-generated Mewtwo. Additional
level95/100 native-stat probes use six members without boosts or PP refills,
with a loss and victory respectively. Human balance and an ordinary continuous
playthrough remain unverified.

Keep exact user-supplied filenames under `roms/` and `saves/source/`; never edit
those files in place or add ROM/save binaries to Git. Original uploads remain
separately retained under `/workspace/attachments/`. No worktree is needed. Publish
this substantial prototype checkpoint through environment settings; publication
is separate from Git commit/push, and fresh-task restoration remains unverified.

Earlier archaeology remains available in [text checkpoint](research/text_inventory_checkpoint.md),
[map inventory](research/orange_map_inventory.md), [connectivity](research/orange_connectivity.md),
[Mister R diagnosis](research/mister_r_diagnosis.md), [linked progression](research/linked_progression_findings.md),
[Orange entry](research/entry_progression_findings.md), [trainer assets](research/trainer_asset_findings.md)
and [space ownership](research/space_ownership.md). These preserve bounded evidence,
unresolved frontiers and historical milestone limitations. Original project sites
remain proxy-denied; the user explicitly authorized and approved the new P001 design.
