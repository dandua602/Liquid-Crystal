# Codex Kickoff Prompt — Pokémon Liquid Crystal Completion Project

You are taking over a long-running ROM-hacking/reverse-engineering project. Treat this as a software-engineering and preservation task, not a casual one-off edit.

## Primary Goal

Finish the abandoned Orange Islands portion of **Pokémon Liquid Crystal** while preserving the existing Johto/Kanto experience and maintaining compatibility with existing Liquid Crystal save files whenever reasonably possible.

The goal is NOT to make a random sequel or rewrite the existing game. The goal is to:
1. reverse-engineer what already exists in the public Liquid Crystal build,
2. identify what Orange Islands content is complete, partial, unreachable, or missing,
3. reconstruct the original developers' intended continuation as faithfully as evidence allows,
4. implement the missing progression in small, testable increments,
5. produce a stable final patch/build that works on emulator and real GBA flash-cart hardware.

---

# Files

The user will keep uploading/replacing these SAME THREE filenames over time. Never assume the bytes are unchanged just because the filename is unchanged.

Expected local filenames:

- `POKEMON Liquid Crystal.gba`
- `POKEMON Liquid Crystal DD 5 badge.sav`
- `1636 - Pokemon Fire Red (U)(Squirrels).gba`

At the beginning of every new Codex session or after the user says the files were updated:

1. locate those exact files,
2. compute SHA-256 hashes,
3. record file sizes,
4. inspect GBA header title/game code/revision,
5. compare hashes against the last recorded baseline,
6. clearly report whether any source file changed,
7. NEVER overwrite these source files in place.

If the user replaces one of these files with a newer version, treat it as a new source snapshot and update the project baseline accordingly.

---

# Known Baseline From Prior Analysis

Previously confirmed on the supplied files:

## Liquid Crystal ROM
- 16 MiB
- FireRed-based
- Game code: `BPRE`
- Revision: 0
- Embedded build text confirms:
  - `Current Build Number: 3.3.00512`
  - text describing the game as a beta / 99% complete Crystal remake
- The build text was previously observed around ROM offset `0x1C5A87`

## Clean FireRed ROM
- 16 MiB
- `BPRE`
- Revision 0
- Squirrels FireRed v1.0 reference ROM
- This is the correct engine/reference base for Liquid Crystal

## Binary Difference
Previous comparison found Liquid Crystal differs from clean FireRed in approximately:
- 5,839,658 bytes
- ~34.81% of the ROM

Do not blindly trust those exact numbers if the uploaded files changed. Recompute them.

## Save
Previous save:
- standard 128 KiB GBA save region plus a 16-byte FlashGBX footer
- prior main-save generations were 36 / 35

Again, re-detect current values from the uploaded save.

---

# Important Findings Already Identified

Direct ROM searches previously found Orange Islands / late-game content involving or referencing:

- Orange Islands
- Orange League
- Mandarin City
- Valencia Island
- Sandway Town
- Route 59
- Route 60
- Science Complex
- Old Warehouse
- Safari Town
- Team Nexus
- Rudy
- Danny
- Zane
- Mister Z
- Nexus 4
- Orange League Champion
- a "Commanding Rank" key/progression item
- dialogue indicating later Team Nexus progression

Previously found gym-related text included:

- `Mandarin City Pokémon Gym`
- Leader: `Rudy`
- `The Mysterious Playboy`

and:

- `Sandway Town Pokémon Gym`
- Leader: `Danny`
- `The relationship guru`

Danny-related dialogue previously suggested his badge is the **second Official Orange League Gym Badge**.

There may be substantially more partially implemented or unreachable Orange Islands content already present in the ROM. Recover that BEFORE inventing new content.

---

# Project Philosophy

Follow these rules strictly.

## 1. Archaeology before authorship
Do not invent new Orange Islands story, maps, trainers, or scripts until all surviving relevant ROM content has been cataloged.

## 2. Preserve existing game behavior
Do not unnecessarily modify:
- Johto progression
- Kanto progression
- existing trainers
- existing flags
- existing save layout
- existing map IDs
- existing item IDs
- existing event logic

unless required and documented.

## 3. Save compatibility matters
Assume players may already have long-running Liquid Crystal saves.

Prefer:
- unused flags
- unused vars
- unused/free ROM space
- new scripts
- new text
- new map headers/maps in unused space

over repurposing active state.

Avoid changing the save structure unless absolutely necessary.

## 4. Source ROMs are read-only
Never modify the supplied `.gba` or `.sav` in place.

Create:
- working copies
- generated test ROMs
- generated test saves
- BPS/IPS/UPS patches
- diff reports

in separate project folders.

## 5. Small changes only
Never make giant unreviewed patches.

Use:
- one feature / one progression segment at a time
- one change ledger entry per patch
- one test checklist per build

## 6. Evidence labels
When reconstructing story/content, label findings as:

- `CONFIRMED_IN_ROM`
- `CONFIRMED_IN_ORIGINAL_PROJECT_DOCS`
- `STRONGLY_INFERRED`
- `NEWLY_AUTHORED`

Never blur original developer content with newly created material.

## 7. Hardware compatibility
Final builds should target real GBA hardware and typical flash carts, not only emulator behavior.

Avoid hacks that rely on emulator-only timing or undefined behavior.

---

# Repository / Working Directory Layout

Create or normalize the project into:

```text
liquid-crystal-completion/
├── README.md
├── PROJECT_STATE.md
├── CHANGELOG.md
├── TODO.md
├── .gitignore
│
├── baselines/
│   ├── hashes.json
│   ├── rom_headers.json
│   ├── save_metadata.json
│   └── source_snapshot.md
│
├── roms/
│   ├── README.md
│   └── [source ROMs are local only / gitignored]
│
├── saves/
│   ├── README.md
│   ├── source/
│   ├── test/
│   └── generated/
│
├── tools/
│   ├── verify_sources.py
│   ├── rom_diff.py
│   ├── gba_text_codec.py
│   ├── text_extract.py
│   ├── pointer_scan.py
│   ├── map_extract.py
│   ├── script_extract.py
│   ├── warp_graph.py
│   ├── flag_var_audit.py
│   ├── free_space_scan.py
│   ├── patch_build.py
│   └── save_probe.py
│
├── extracted/
│   ├── text/
│   ├── maps/
│   ├── scripts/
│   ├── trainers/
│   ├── wild_encounters/
│   ├── items/
│   └── pointers/
│
├── research/
│   ├── orange_text_index.md
│   ├── orange_map_inventory.md
│   ├── orange_connectivity.md
│   ├── orange_script_inventory.md
│   ├── progression_flags.md
│   ├── nexus_story_index.md
│   ├── dead_end_analysis.md
│   ├── intended_story_reconstruction.md
│   └── free_space_report.md
│
├── patches/
│   ├── dev/
│   └── release/
│
├── builds/
│   ├── dev/
│   └── release/
│
└── tests/
    ├── regression_checklist.md
    ├── save_compatibility.md
    └── hardware_test_notes.md
```

Do NOT put copyrighted source ROM binaries in Git.

Add to `.gitignore` at minimum:

```gitignore
*.gba
*.sav
roms/
saves/source/
builds/
```

Generated patch files may be committed if appropriate.

---

# Preferred Technical Strategy

Liquid Crystal is a heavily modified binary hack of FireRed v1.0.

Use the modern **pokefirered decompilation** only as:
- an engine reference,
- data-structure reference,
- scripting reference,
- map/event reference,
- routine reference.

Do NOT assume Liquid Crystal data resides at original FireRed addresses.

For every important structure:
- locate it independently in Liquid Crystal,
- validate with multiple references,
- record the discovered offsets/pointers,
- compare against clean FireRed where useful.

Prefer automated parsing tools over manual hex inspection once a structure is understood.

Build reusable tooling rather than one-off scripts.

---

# Work Queue

## STEP 1 — Baseline Lock and Verification

This must run first.

Tasks:
1. Hash all three source files.
2. Read ROM headers.
3. Confirm Liquid Crystal build string.
4. Confirm FireRed base revision.
5. Binary diff LC vs FireRed.
6. Inspect save generations and footer.
7. Create:
   - `baselines/hashes.json`
   - `baselines/rom_headers.json`
   - `baselines/save_metadata.json`
   - `baselines/source_snapshot.md`
8. Create/update `PROJECT_STATE.md`.

Exit condition:
- exact source snapshot is reproducibly identified.

---

## STEP 2 — Orange Text Archaeology

This is the FIRST active research phase after baseline verification.

Goal:
Extract and classify every relevant Orange Islands / Team Nexus / Orange League text block from Liquid Crystal.

Search for and expand around:
- Orange
- Mandarin
- Valencia
- Sandway
- Safari
- Route 59
- Route 60
- Science Complex
- Warehouse
- Rudy
- Danny
- Zane
- Mister Z
- Nexus
- Commanding Rank
- Champion
- League
- badge
- island
- ferry
- gym
- leader

Tasks:
1. Determine the game's text encoding/pointer format.
2. Build a text decoder if needed.
3. Extract surrounding dialogue, not just keyword matches.
4. Record:
   - ROM offset
   - decoded text
   - possible pointer(s)
   - likely map/event cluster
   - confidence
   - whether text appears referenced or orphaned
5. Group dialogue into story/event clusters.
6. Detect likely unused/unreachable text.
7. Create `research/orange_text_index.md`.

Deliverable should include:
- a chronological-looking story cluster index,
- a list of orphaned/unused dialogue,
- offsets and references,
- hypotheses clearly separated from confirmed facts.

Do NOT start authoring missing story yet.

---

## STEP 3 — Map Archaeology

Goal:
Identify every Orange Islands map and how they connect.

Tasks:
1. Discover map bank/map-header structures used by Liquid Crystal.
2. Enumerate likely Orange maps.
3. Decode:
   - map IDs
   - map names
   - map headers
   - layout pointers
   - object/NPC events
   - script pointers
   - warp events
   - connections
   - signposts
   - trainer objects
4. Build a warp/connectivity graph.
5. Identify maps that exist but are unreachable.
6. Identify placeholder or duplicate maps.
7. Create:
   - `research/orange_map_inventory.md`
   - `research/orange_connectivity.md`
   - machine-readable JSON/CSV exports

Do not edit maps yet.

---

## STEP 4 — Script Archaeology

Goal:
Decode actual Orange Islands progression.

Tasks:
1. Identify script commands and script pointer structures.
2. Decode scripts attached to Orange maps.
3. Track:
   - flags
   - vars
   - trainer battles
   - badge awards
   - give-item events
   - Team Nexus state
   - ferry state
   - gate/blocker logic
   - map transitions
   - cutscenes
   - NPC conditional dialogue
4. Create `research/orange_script_inventory.md`.
5. Create `research/progression_flags.md`.
6. Mark each event:
   - WORKING
   - PARTIAL
   - UNREACHABLE
   - BROKEN
   - PLACEHOLDER
   - UNUSED

Do not fix anything yet.

---

## STEP 5 — Exact Dead-End Diagnosis

Goal:
Find the exact technical point where the public beta stops progressing.

Tasks:
1. Trace playable Orange progression from entry.
2. Identify last fully functioning event.
3. Identify first missing/broken dependency.
4. Determine whether the dead end is caused by:
   - missing map
   - missing warp
   - missing script
   - unset/unreachable flag
   - placeholder NPC
   - unimplemented gym
   - missing item
   - disabled ferry
   - incomplete Team Nexus event
   - missing text pointer
   - missing trainer/battle
   - deliberate beta stop
5. Document exact addresses and involved state.
6. Create `research/dead_end_analysis.md`.

---

## STEP 6 — Intended Story Reconstruction

Only after Steps 2–5 are complete.

Use:
- surviving ROM text/scripts/maps,
- original Liquid Crystal project posts/documentation,
- archived community posts where available,
- developer statements,
- map naming,
- unused events,
- internal progression clues.

Produce:
`research/intended_story_reconstruction.md`

Every scene/event must be labeled:
- CONFIRMED_IN_ROM
- CONFIRMED_IN_ORIGINAL_PROJECT_DOCS
- STRONGLY_INFERRED
- NEWLY_AUTHORED

Goal:
preserve original Liquid Crystal intent wherever possible.

---

## STEP 7 — Patch Architecture

Before editing the ROM:

1. Certify free ROM space.
2. Scan candidate free-space ranges for pointers/references.
3. Build a free-space allocation ledger.
4. Allocate:
   - new text
   - new scripts
   - new map data
   - new trainer data
   - new event flags
   - new vars
5. Avoid active FireRed/Liquid Crystal data.
6. Preserve save compatibility.
7. Create:
   - `research/free_space_report.md`
   - `research/address_ledger.md`
   - `research/flag_var_ledger.md`
   - `research/patch_spec.md`

No implementation until this is reviewed.

---

## STEP 8 — First Playable Continuation Patch

Implement ONLY the smallest missing segment immediately after the known beta dead end.

Deliverables:
- test ROM build
- patch file
- change log
- exact modified address list
- test save positioned just before new content
- regression checklist

Tests:
- boots
- old save loads
- Johto unaffected
- Kanto unaffected
- Orange progression before patch point unaffected
- new segment completes
- save/reload works
- no obvious map warp corruption
- no item/flag regression

---

## STEP 9+ — Incremental Orange Islands Completion

Repeat in small slices:
1. one route/town/island/gym/story segment,
2. patch,
3. test,
4. lock,
5. proceed.

Never implement multiple islands at once unless the dependency graph absolutely requires it.

---

## FINAL PHASE — Orange League Finale + QA

Finish:
- remaining Orange badges
- Team Nexus climax
- Orange League / Champion
- postgame resolution
- credits/end-state
- optional rematches if appropriate

Then:
- full save compatibility regression
- emulator test
- real GBA/flash-cart test
- final BPS/UPS/IPS release patch
- documentation
- changelog
- known-issues list

---

# Testing Requirements

For every generated ROM build:

1. Record source ROM hash.
2. Record output ROM hash.
3. Record all changed byte ranges.
4. Confirm GBA header integrity.
5. Produce a patch rather than relying only on a full ROM.
6. Keep a reversible change ledger.

For every save-based test:
- preserve original save untouched,
- work on a copy,
- preserve FlashGBX footer when appropriate,
- verify save checksums,
- verify load/save/reload behavior.

---

# Output Style

Codex should work in small milestones.

At the end of each step, provide:

## Completed
What was actually done.

## Findings
Concrete technical findings with offsets/pointers where relevant.

## Files Created
List exact files.

## Risks / Unknowns
What is still uncertain.

## Next Step
Exactly one bounded next step.

Do not jump ahead unless the user explicitly says to.

The user plans to simply reply with:
`ok next step`

So maintain `PROJECT_STATE.md` carefully so the project can resume cleanly.

---

# FIRST ACTION TO TAKE NOW

Start with:

## STEP 1 — Baseline Lock and Verification

Do not modify the ROM.

Create the project structure, hash/inspect all three files, verify whether they match the previously known baseline, and create/update `PROJECT_STATE.md`.

After Step 1, immediately proceed to **STEP 2 — Orange Text Archaeology** only if the source files are confirmed and no unexpected mismatch requires user review.

Do not begin writing new story or editing the ROM yet.
