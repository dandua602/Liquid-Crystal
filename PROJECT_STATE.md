# Project state

## Current milestone

P002 is approved, implemented, tested and packaged. The user approved its concrete
proposal with **“approve, keep going.”** research/design/p002_approval.json records
the decision. No P002 implementation approval remains pending. Frozen review
files remain historical; current details are in research/P002_implementation.md.

All150 project tests and166 newly executed P002 runtime checks pass across seven
cases. P002 includes P001 plus the Office Block service room6:32, entered from the
warehouse sign after actual victory and exited normally back to the warehouse.
It does not add another fight/reward/rank, upper floors, Route60 or city-door unlock.
A P001 saved research game upgrades, actual victory earns access, new-map Save
and fresh-process load work, and a safe returned save loads in fresh P001.

Output: builds/dev/Liquid Crystal P002.gba. SHA256:
`9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70`.
Package: builds/P002-prototype.zip, with standalone/P001-relative forward/reverse
BPS, manifests, applier, current player walkthrough and screenshots; no ROM/save.
Originals, footer and exact P001 ROM remain unchanged. Hardware validation and
an ordinary full-game playthrough remain unverified.

## GitHub and next review

The project is committed and pushed to `main` at
https://github.com/dandua602/Liquid-Crystal. The first published commit is
`c503441964b80552ed1d7b269e059308642d5042`. The user has requested ongoing
GitHub synchronization; commit/push each meaningful tested checkpoint and verify
the remote. See GITHUB.md for patch/guide links and publishing instructions.
Cloud environment Publish is a separate filesystem/configuration snapshot.

P003 is now a concrete review proposal: Office attendant communications shutdown
using existing Mandarin aftermath flag5B2, with a newly authored hostile NPC
departure to avoid its original empty text branch. Read research/P003_review.md
and walkthrough/P003-preview.md. Ten new native fixture expectations pass on
unchanged P002; they are original branch/visibility evidence, not P003 runtime
acceptance. The preview fits133/192 script bytes and224/320 text bytes, with a
new512-byte bounded space screen. The current project suite passes155 tests.
No P003 ROM/patch or implementation approval exists. The kickoff requires review before that next ROM change.

Visual review caught a P001 flagless rock respawn after movement that immediate
visibility checks missed. P002 fixes it with two same-size call hooks and56 bytes
of helpers using existing room-template coordinates. No new flag/variable/save
format is introduced. Pending0/1 restores15,9; solved/completed places the removed
rock template63,63 outside the unchanged32x19 room. Actual P002 allocation is
151/160 script bytes,109/128 text,212/256 tables in the previously pristine544-byte
reserve. Seven delta spans relative to P001 are listed in the build manifest.
Old group6 pointers, including problematic legacy slots4/6, remain exact.

P001's ROM remains SHA256
`b2c3d4e3fb6f196de90bd9d88cbdcd850e429dce919034c48326d924ae413e92`.
Its old nine-case124 checks, two native-stat probes48 checks and Office evidence6
checks are retained, not freshly rerun for this P002 milestone. New P002 journey
has a boosted native-generated Mewtwo fixture and actual combat outcomes; it is
not human balance proof. Unknown computed owners/map uses remain outside the
bounded certificate; runtime still requires the supplied-image adapter.

## Cartridge test package

The user plays on real consoles by flashing carts and has original backups.
FlashGBX software is confirmed; the physical reader, cart model and profile
are still unconfirmed. The original uploaded ROM uses
banked SRAM plus embedded NOR save at C80000–CA0000, so the new private hardware
package includes the selected save inside each image, with the driver unchanged.
Read HARDWARE_TEST.md for exact image choices and the console checklist.

`builds/P002-cartridge-test.zip` contains P002-personal-5badge.gba (exact standard
P002), P002-warehouse-test.gba (new artificial pre-puzzle save, native-stat six
level100 team with Iron Tail/Surf) and P002-office-test.gba (earlier boosted
post-victory fixture), raw sidecar saves, manifest/checksums, guide/screenshots
and readback helper. All ROM/save files remain ignored/private. GitHub has only
`patches/P002/P002-cartridge-tools.zip`, scripts, docs, evidence and metadata.

Three ROM-embedded-save boots passed with blank emulated SRAM and no sidecar
injection. Nineteen expectations cover those cases, native NOR Save and a fresh
process using updated NOR bytes. Native team preparation is separately recorded.
The optional LC_PROBE_ROM_SAVE_BOOT frontend mode supports these checks; default
P001/P002 behavior stays unchanged. Full current suite155 passes. Package CLI
patch/embed/readback, overwrite refusal, ZIP integrity and member hashes pass.
No physical flash timing, chip/profile compatibility or hardware success is
claimed. Await user console power-off/save/reload and gameplay results. Reflashing
an image resets its embedded starting save; a post-play dump may differ only in
that window, checked with tools/verify_cartridge.py --after-play.

## Walkthrough requirement

The user explicitly requires clear instructions as each story slice is created.
WALKTHROUGH.md now covers P002 including the prior warehouse chapter, verified
nearby approach, Old Key, route diagram, puzzle/battle/retry/save steps, Office
entry/decline/attendant/return, screenshots and the exact current endpoint.
Update and package this guide/images with each future story release.
walkthrough/P001.md is version-specific; P002-preview.md is frozen historical
review material, not current runtime status.

Before removing P002, exit new map6:32 to original warehouse6:31 and save. A
save left inside the new map cannot load in P001-only/original ROMs. Artificial
Office/safe-rollback fixtures under saves/test are QA only, never replacements
for the user's personal save. Fresh P001 load after the safe exit was tested.

## Earlier source-ROM research evidence

The following records pre-prototype archaeology milestones. Statements about
pending review/allocation refer to those historical milestones; current P001
implementation and acceptance are recorded above and in the implementation report.

- All three original uploads and local source copies still match baselines/hashes.json. Both ROM header checksums pass. Build phrase is at 0x1C5AE5, build number at 0x1C5AFB.
- Save slots contain IDs 0–13 and generations 36/35. Vanilla FireRed checksum lengths do not validate all sections, but this is not proof of corruption. The supplied image has an embedded 128 KiB cartridge save at 0xC80000–0xCA0000, exactly matching the uploaded save payload, plus a custom SRAM bank port at 0x09000000 and NOR programmer. Correct emulation loads Continue cleanly. Earlier corruption/previous-save warnings under default BPRE flash emulation are superseded as save diagnoses. A new game save and fresh-process reload preserve Mister R room, state 0x5331, rescue/unlock/visibility flags and Old Key. Original source and FlashGBX footer remain unchanged; checksum lengths and hardware behavior remain unaudited.
- Text corpus: 2,372 raw keyword hits, 2,330 accepted hits, 1,388 candidate blocks, 318 specific research-seed blocks. All 53 historical misses are classified: 11 recovered hits, 12 prose-boundary anomaly hits, 30 binary-context candidates. The 42 not accepted as full strings remain visible with classifications. Six recovery candidates add four net blocks and expand two truncated records.
- All 64 historical weak-reference candidates were reviewed; 30 still lack absolute pointers. Nine have referenced normalized copies. No unused/unreachable certification has been made. See research/text_inventory_checkpoint.md, research/text_boundary_triage.md and research/orphan_candidate_review.md.
- Item 0x114 is G Rank. Its description at 0xAAAF41 has 89 prose bytes and no dedicated FF before the following script at 0xAAAF9A. Native item accessors and both old/relocated table records support this identity. Runtime rendering/consequence untested; no fix applied. See research/rank_description_investigation.md.
- Earlier event clusters link 32 messages across five anchors. The Nexus machine audit links nine anchors, 12 nonempty strings plus two empty targets, and ten controller scripts. Counter 0x5318 and flags 0x54B–0x554 encode 100% → 0%. New controlled tests verify charging/rejection and actual hooked battle execution through escape; a full normal controller playthrough and intended one-use semantics remain unresolved.
- Initial map extraction independently finds the native group-table lookup and maps all ten controller roots through 17 BG events to ten map records. Section labels include West Vale Port, Routes 53–56, Sandway Town, Nexus Laboratory, Mandarin City and Science Complex. Script/coordinate reuse remains visible.
- Bounded connectivity graph retains all 58 warp and 13 connection associations from those ten owners, resolving 32 distinct map slots including legacy/dynamic-return targets. All warp indices and source/landing coordinates validate against default layouts. All 32 header layout pointers match independently discovered native layoutId-1 slots; sparse zero holes are not table terminators. Saved/script layout overrides remain unknown.
- Target-warp return comparisons: 26 exact, one same-map/different-warp, 11 dynamic returns through map 0:0, and 20 different static return maps. Zero group/map is an ordinary destination, not a sentinel. Seven connections have inverse records; six do not. Route 54 variants and Science Complex return asymmetries are retained without defect/unreachable claims. Sandway's 3:60 target has a null events pointer and a CONNECTION_NONE entry. See research/orange_connectivity.md, research/warp_semantics_notes.md and research/warp_destination_review.md.
- Physical bank pointer prefixes are candidate scan bounds, not engine-enforced counts. Some intermediate slots have dummy/bad layouts; do not trim a bank at those slots or delete candidate duplicates. All ten targeted owner layouts and event arrays validate. See research/orange_map_inventory.md and research/map_discovery_notes.md.
- The 32-map event/script catalogue retains 555 event records (285 objects, 130 coordinate events, 140 BG events), 559 script associations and 332 unique roots. Five hidden-item unions are not treated as script pointers; 14 unknown map-script tag records remain visible. All exported event coordinates fit default layouts. See research/orange_script_inventory.md and extracted/scripts/.
- Focused traces cover 67 roots and 800 unique instruction candidates, linking 137 complete messages. Both Route 54 variants share frame table 0x721D62: operands 0x5305/0 select script 0xA7094D, which sets 0x5305 to 1, removes local objects 6/5 and sets visibility flag 0x52E. Dialogue references Mateo, Marrisa and the Crystal Onix. Both blocker objects have null interaction scripts; their event is map-owned.
- Science Complex 3:111 and Route 53 3:99 have byte-identical object/BG records and the same load-script pointer; Route 53 signpost text persists in both slots. No explicit warp/destination/layout setter was decoded in the focused subset, but unresolved global helpers, other roots and native effects prevent an absence or reachability conclusion. See research/route54_science_script_findings.md.
- Variant selection audit scans 43 native-table physical-prefix groups and 1,504 candidate slots, preserving malformed records and parsing warp/connection spans independently from layouts. These are candidate slots, not 1,504 certified maps. No parsed incoming literal record targets 3:107/3:111. Validated-header comparison associations total three to 3:99 and six to 3:101; eight weaker matches to 3:99 reuse one unsuitable header in overlapping group-prefix tails. No unused/unreachable certification follows.
- All 332 catalogued script roots were traced within 256 instructions/1,024 states/depth 8, yielding 3,717 unique instruction candidates and explicit frontiers. Fourteen raw variant warp/setter shapes classify as eight pointer-backed LZ77 streams, two pointer-word overlaps and four unresolved contexts; none has a map-root or nearby pointer-target format witness. Native probe records 56 BL-shape sites and a limited 32-byte constant window, not complete native dataflow. See research/map_variant_selection.md and extracted/maps/map_selection_audit.json.
- Route 59 destinations 6:28–6:31 add four catalogued maps: gatehouse to Mandarin, Black Flute seller, underwater passages and Mister R introduction room. The audit retains 29 event records/associations, 15 unique roots, 267 instruction candidates and 28 complete messages. Nineteen warp and one connection records validate across 13 context map slots. These are separate bounded exports, not a recursively expanded world graph.
- Two underwater emergence scripts, 0xAA087D / 0xAE8C6D, are each owned by six BG records. Their warpteleport commands target Route 59 warps 1/4 after move/flag/prompt/field-effect paths. This differs from some raw warp returns; keep metatile/native activation unresolved. Four event script fields contain ROM-start pointer 0x08000000 (not null), and older Johto destination/NPC data persists in the new maps. See research/route59_progression.md.
- Mister R room 6:31 has frame condition VarGet(0x5331)==VarGet(0) → 0xAE8D7A. The intro sets 0x5331 to 1, promises a puzzle/battle, sets visibility flag 0x5C5 and removes object 1. Its complete local format path has no trainer-battle command; a completion path is not yet established. This is a progression lead, not a certified beta dead end.
- Room 6:31 has 74 connected collision-zero/elevation-3 tiles; 534 blocked cells. Only its damaged sign is a BG interaction adjacent to this floor component. Mister R's three movements end at (20,10), then hide/remove him. Reachable machine/telephone/light native dispatch leads to unchanged FireRed flavor scripts, reproduced with normal buttons in the emulator.
- The damaged sign plausibly hints at Iron Tail/red rocks. The standard field-move selector/list matches FireRed and excludes Iron Tail; the sole raw checkpartymove 231 shape is in compressed data. The wider bounded search traces 4,037 candidate owner roots (53,114 instruction candidates), retains all 69/46 raw state/flag hits and all 21 Mister R/seven puzzle hits. Only the introduction's state write, visibility flag and room frame condition have supported owners; the four previously unresolved state shapes are now classified as three inherited pointer-backed audio-format spans and one validated LZ77 stream identical to FireRed. See research/mister_r_state_review.md; computed/native paths remain outside this negative evidence. No whole-ROM absence claim. See research/mister_r_diagnosis.md.
- mGBA 0.10.5 with the supplied-image cartridge adapter boots the ROM and loads the five-badge save into a playable field. A RAM-only forced warp reproduces the introduction and removal, damaged sign and three flavor interactions; live coordinates validate each walking step. The stair activates on a second east input and reaches map 0:0 at (6,8). These are forced-state behavior tests, not normal Orange progression tests. Screenshots/transcript: extracted/runtime/. Fresh game save/reload now passes in the separate linked replay; hardware remains untested.
- Route 54 cutscenes complete on both 3:101/3:107, setting 0x5305=1 and flag 0x52E. Both keep their IDs and exact default headers in the tested state. Walking from forced 3:107 into cave 5:95 and back returns to original 3:101. Do not reroute into the variant as an assumed repair.
- Science Complex 3:111 really loads its default header/layout in the fixture, but 1,989/2,016 cells have ocean behavior and 27 behavior zero. Copied cave coordinate (33,18) is ocean (0x15), whereas Route 53 has a door (0x60). North movement there does not enter the cave. Independently forcing cave 5:93 and walking out returns to 3:99. These are scoped state tests, not universal absence/unused certification.
- Charger branch clears unavailable flag 0x544; uncharged actual BG interaction preserves counter 11 and unused-controller flag. Escaping the real level-100 Electabuzz battle decrements 11→10 and sets 0x54B, while 0x544 remains clear. Repeating that controller does not decrement twice, and a second root accepts without recharge. A separate final fixture counter 2→1 sets 0x514 and clears 0x175A after escape. Test party cached speed is 999; no battle outcome is injected. Victory/loss and ten natural interactions remain untested.
- New native evidence verifies the LC extended-variable hook (5000–5562 at fixed RAM 0203D400), live map-header address and party base; it does not certify new state allocation. The linked replay separately verifies persistence of existing 0x5331 and selected flags. Full results: research/progression_runtime_findings.md, research/progression_flags.md, extracted/runtime/progression/progression.json. Provisional architecture and boundary status: research/patch_spec.md, research/dead_end_analysis.md.
- The new broad script audit follows 4,037 candidate owner roots using all 213 standard command widths; 181 thematic/focus roots and 389 messages remain indexed with unresolved frontiers. Structural preflight expands 128 candidate slots/599 links. Candidate owners/links do not certify normal world reachability.
- Laboratory 5:102 now completes its real trainer battle and dialogue, sets 0x5315=1 / flag 0x513, and awards G Rank 0x114. Police 6:27 completes its battle/rescue, sets 0x5BA and awards Old Key 0x116, then game-warps to 6:24. Ordinary walking proceeds through Mandarin 3:109, gatehouse 6:28 and Route 59 3:110. Actual door interaction sets 0x5C1 and enters Mister R 6:31; his introduction sets 0x5331 and 0x5C5. The fixture uses two forced initial anchors and boosted party; later map transitions and progression state are earned by game scripts/buttons. This is not a complete Johto/Kanto-to-Orange playthrough. See research/linked_progression_findings.md.
- Free-space/address/state ledgers exist. Forty-five FF runs of at least 4 KiB remain candidates with raw incoming targets; none is certified or allocated. The embedded cartridge save window and its driver are active storage/code and must be preserved. ROM expansion needs a review of the existing 0x09000000 bank port. No new flag or variable is reserved.
- The controlled entry replay passes Oak authorization (0x1702), office stamping (0x1778), the first station gate (0x1873), train interruption, officer/Jin access, actual Kyogre encounter (0x9B), non-electric engine rejection, Ampharos engine restart (0x1779), Valencia station arrival (0x5301) and ordinary exit to port 3:77. Eligibility flags and initial map anchors are explicit; later transitions/state are earned. The source party is boosted and an artificial Ampharos replaces slot 6 on the disposable copy. See research/entry_progression_findings.md.
- The entry static audit covers ten maps, 93 roots, 2,111 unique instruction candidates and 166 messages, preserving seven roots with frontiers. Ordinary Johto/Kanto prerequisites, every return/timetable branch and every intervening Orange route/gym remain unverified.
- Two independently discovered native trainer consumers agree on table 0xABFD84 (FireRed reference 0x23EAC8), stride 40. Native party loops use 8/16/8/16-byte rows for flags 0/1/2/3, including ABI padding. Of 1,024 physical candidate rows, 891 have complete names and bounded party arrays; 133 failures and numeric field anomalies remain explicit. This is not a certified trainer count/free-ID pool. Named candidates provide Mister G/Danny/Zane assets, but no recovered future Mister R/Rudy team. Mandarin's encounter uses Elite 899; the police rescue uses Elite 912. See research/trainer_asset_findings.md.
- The state review resolves all four old raw-shape leads: audio at 0x52A3C0, 0x553108 and 0x60FEB0, plus a validated LZ77 payload at 0x703C40–0x71A034. All enclosing bytes match FireRed. No additional supported room state handler follows. A reviewed extension of owned 0x5331 is preferred over consuming unrelated flags, but values 2/3 remain proposals and migration/allocation gates remain open.
- The previous milestone passed 125 regression/integrity tests and 70 runtime expectations across three progression replays. The later allocation milestone added four tests and 14 focused storage expectations; the native-feasibility milestone adds four tests and 16 expectations; final results are in extracted/runtime/validation_summary.json. Complete native callees remain unaudited. Original/source hashes remain unchanged. Optional runtime setup is reproducible with tools/setup_runtime.py; static analysis still needs only Python's standard library.

## Next bounded step

Publish the tested P002 milestone, then prepare the next Office story slice from
surviving rank/antagonist/progression evidence. No concrete P003 design is yet
reviewed or approved. Scope one meaningful segment and preserve existing city
blockers and source behavior. A larger slice will require a new storage plan;
only72 bytes remain in P002's reserve plus fragmented earlier spare capacities.
Do not restart unrelated global inventories or unchanged old journeys.

## Publish checkpoint

Prior P001/guide-review startup settings were observed published. The tested P002
ROM, fixes, guide and upgrade/rollback package are newer local work. Updated setup
and startup instructions must be saved in the draft, then reviewed/saved and
published to snapshot this milestone. Draft saving is not publication. No Git
commit/push or independent fresh-task restoration has been performed.

## Resume and reproduce

Use the existing /workspace/Liquid-Crystal checkout; no worktree is needed. Python 3.12 standard library is sufficient. Inspect exact source filenames and compare hashes each session. Updated uploads require a preserved, reviewed new snapshot; never overwrite source files or baselines blindly.

Fast resume: read this file and research/remaining_work.md, then run `python3 tools/verify_sources.py`. At a substantial milestone, run the unittest suite once. Use tests/test_plan.md for focused changes. No service needs starting.

The following is the **full artifact regeneration sequence**, not a per-turn startup checklist. Use it only for changed/stale inputs or intentional reproduction:

```sh
python3 tools/verify_sources.py
python3 tools/text_boundary_triage.py
python3 tools/text_extract.py
python3 tools/orphan_reference_audit.py
python3 tools/text_reference_trace.py
python3 tools/dialogue_cluster_audit.py
python3 tools/engine_reference_probe.py
python3 tools/nexus_machine_audit.py
python3 tools/map_extract.py
python3 tools/warp_graph.py
python3 tools/script_extract.py
python3 tools/map_selection_audit.py
python3 tools/route59_audit.py
python3 tools/mister_r_audit.py
python3 tools/orange_progression_audit.py
python3 tools/architecture_audit.py
python3 tools/save_hardware_audit.py
python3 tools/entry_audit.py
python3 tools/trainer_audit.py
python3 tools/mister_r_state_review.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Optional runtime workflow (tested): `python3 tools/setup_runtime.py`, then `python3 tools/runtime_smoke.py --frontend /workspace/.cache/liquid-crystal-runtime/mgba-probe --room-interactions`. This uses disposable copies and explicitly forced room entry; it changes emulator RAM but not the source ROM/save. No persistent process needs starting after restoration.

Progression replay (tested): `python3 tools/progression_runtime.py`. This writes its own JSON/screenshots under extracted/runtime/progression/, checks 31 expectations and records all forced flags/vars/map entries/party-speed writes. It preserves the earlier Mister R smoke artifacts. Both replays depend on the same verified frontend cache.

`text_triage_input.json` preserves the historical miss/candidate cohort; the triage supplement is checked against current source hashes before influencing main text boundaries. Retained references under research/references/ require no network at runtime. Local generated outputs and saved cloud startup instructions do not establish publication or GitHub backup.

Linked replay (tested): `python3 tools/linked_progression.py` completes laboratory plus the late Orange journey, then uses in-game Save and a new emulator process. It retains 21 expectations, 158 walking requests and the cartridge mapper transcript. The ignored save fixture under saves/test/ is artificial and labelled; never substitute it for the source save. Read research/linked_progression_findings.md and extracted/runtime/save_hardware.json before interpreting older save warnings. The frontend modifies only the private cartridge save window in emulator memory and disposable save file; no source or copied ROM file is written.

Entry replay (tested): `python3 tools/entry_runtime.py` performs the complete controlled first-trip quest, including native train transfers, Kyogre and the actual electric-party selector. Static companions: `python3 tools/entry_audit.py`, `python3 tools/trainer_audit.py`, `python3 tools/mister_r_state_review.py`. They use the standard library; Capstone was used only for exploratory interpretation and is not a project/startup dependency. Forty-five pinned reference files verify.

Focused allocation evidence: `python3 tools/allocation_audit.py` checks exact native trainer hooks, candidate row 929 and all-mirror/unaligned pointer shapes. `python3 tools/allocation_runtime.py` checks native bit behavior and genuine Save/fresh-process reload with 14 expectations. Only disposable copies receive trainer state and temporary 0x5331=2; no allocation or battle acceptance is implied. See research/allocation_findings.md.

New focused feasibility replay (tested): `python3 tools/warehouse_primitives.py` records move detection and existing real win/escape outcomes with 16 expectations. `python3 tools/p001_preflight.py` checks the concrete 2 KiB design budget. Both are read-only with respect to the source files; neither tool emits a warehouse implementation or trainer team. A later separately authorized review proposal now defines the new team.

Current design evidence: `python3 tools/space_ownership.py`, `python3 tools/design_review_audit.py`, and the already executed `python3 tools/design_state_runtime.py`. The last is storage-only on disposable copies, not a new puzzle/battle. The corrected run passes 10 checks; the first copyvar fixture error is retained and explained in research/design/validation_notes.md. Current counts/source-preservation results are in extracted/runtime/validation_summary.json.
