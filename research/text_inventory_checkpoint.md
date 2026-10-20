# Text inventory checkpoint and handoff to maps

## What closed

All 53 historical keyword misses are now explicitly partitioned without changing ROM bytes:

| Evidence class | Keyword hits | Meaning |
|---|---:|---|
| Recovered dynamic templates | 4 | F7 plus its index is a two-byte token, supported by retained text.c. Expansion remains unexecuted. |
| Recovered complete readable suffixes | 7 | Full Oak/Sunburst text and a gym-remnant message; absent exact-start pointers do not make them unused. |
| Prose-boundary anomalies | 12 | Six contexts contain real prose but strict parsing fails on adjacent non-text/unsupported bytes. |
| Repeated binary-window candidates | 22 | Two identical context families, each repeated 11 times; keyword substrings are not promoted to dialogue. |
| Other binary-context candidates | 8 | Mixed-case substring matches amid non-prose/unsupported bytes; asset type remains unspecified. |

The 11 recovered hits occupy six candidate blocks: three dynamic templates, one net-new gym-remnant block, and two fuller versions of previously truncated records. The corpus grew by four blocks, from 1,384 to 1,388. It now accounts for 2,330 accepted hits and retains 42 outside complete strict-English strings (the 12 anomaly hits plus 30 binary-context candidates). All 2,372 original keyword hits remain represented.

The weak-reference review separately accounts for all 64 frozen Orange-specific candidates: 13 inline name fields, 11 table-backed texts, two other raw-pointer texts, two preceding message targets with anomalous prefixes, two adjacent binary-prefix cases, two accidental interior-pointer truncations, two unclassified interior-pointer texts and 30 candidates without absolute pointers. Nine have normalized-equal copies with recognized text operand shapes. None is certified unused or unreachable.

## Important concrete finding

Item operand `0x114`, used in Mister G's award-shaped sequence, is named `G Rank` through the relocated item-name table. Its native description accessor still uses the original item-record table, whose description field points to `0xAAAF41`. Both table records refer to the same description.

The 89-byte readable description ends with a period at `0xAAAF99`. The next byte, `0xAAAF9A`, starts an independently referenced event script. There is no dedicated FF terminator in between. The first FF at `0xAAAF9B` is also the low byte of that script's local-object operand. Strict rejection is correct; accepting this whole span as clean text would hide the anomaly. Actual menu rendering and any gameplay consequence remain untested. No repair was made.

## Evidence files

- `extracted/text/text_triage_input.json`: small frozen input from the earlier corpus; not a different ROM snapshot.
- `extracted/text/text_boundary_triage.json` and `research/text_boundary_triage.md`: all 53 hits, six recovered blocks, six partial contexts and repeated-window evidence.
- `extracted/text/orphan_reference_audit.json` and `research/orphan_candidate_review.md`: all 64 weak-reference candidates.
- `research/rank_description_investigation.md`: item tables, native accessors, exact bytes and uncertainty.
- `extracted/text/orange_text_audit.json` and `research/orange_text_index.md`: regenerated main corpus; reviewed complete boundaries take precedence over accidental interior raw pointer starts.

## Phase boundary

This is a completed static text-inventory checkpoint, not a claim that every possible encoded/compressed LC string has been recovered. Non-keyword coverage, indirect/native consumers, custom font/control behavior and all runtime reachability remain open. Those questions now require map/script ownership evidence; do not spend more text-only passes pretending absent pointers establish unused data.

At the user's request to proceed, Step 3 has begun: `tools/map_extract.py` independently discovers the native group-table lookup, validates 17 BG-event ownership chains to ten map records, and exports their raw warps/connections. The accompanying `research/orange_map_inventory.md` and `research/map_discovery_notes.md` preserve aliases, pointer-prefix bounds, dummy-slot warnings, native lookup bytes, map dimensions and coordinates.

The next bounded task is to validate the exported warp destinations and connections and expand the Orange map inventory. No story reconstruction, ROM modification or save edit is authorized by this checkpoint.
