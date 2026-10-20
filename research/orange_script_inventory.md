# Orange candidate map script catalogue

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

All event/script pointer fields and map-script tables in the 32-slot connectivity scope. All associations preserved. Focused format traces only for Route 54/Science Complex, comparison maps and direct cave destinations; no recursive world or full progression extraction.

CONFIRMED_IN_ROM: bytes, pointer chains and associations. STRONGLY_INFERRED: field roles and execution rules from pinned FireRed. No runtime accessibility or unused-content certification.

```json
{
  "map_slots": 32,
  "event_records": 555,
  "event_kinds": {
    "background": 140,
    "coordinate": 130,
    "object": 285
  },
  "event_script_statuses": {
    "ROM_script_candidate": 534,
    "hidden_item_union_not_script": 5,
    "null": 16
  },
  "script_associations": 559,
  "unique_script_roots": 332,
  "map_entry_script_associations": 25,
  "unknown_map_script_tag_records": 14,
  "unterminated_map_tables": 0
}
```

## Per-map records

| Map | Section label | Objects / coordinates / BG | Map-script tags |
|---|---|---|---|
| 0:0 | NOT USED | 1 / 2 / 0 | 255 (unknown_tag), 255 (unknown_tag), 187 (unknown_tag), 255 (unknown_tag), 9 (unknown_tag), 72 (unknown_tag), 131 (unknown_tag), 42 (unknown_tag) |
| 1:99 | LIGHTHOUSE | 20 / 2 / 0 | 3 (on_transition) |
| 3:60 | NOT USED | 0 / 0 / 0 | none |
| 3:98 | WEST VALE PORT | 10 / 3 / 5 | 1 (on_load), 3 (on_transition) |
| 3:99 | ROUTE 53 | 14 / 0 / 6 | 1 (on_load) |
| 3:100 | SANDWAY TOWN | 17 / 10 / 8 | 1 (on_load), 3 (on_transition), 2 (on_frame_table) |
| 3:101 | ROUTE 54 | 9 / 0 / 4 | 2 (on_frame_table), 1 (on_load) |
| 3:102 | ROUTE 55 | 12 / 0 / 4 | 1 (on_load) |
| 3:103 | ROUTE 55 | 9 / 0 / 2 | 1 (on_load) |
| 3:104 | ROUTE 56 | 12 / 0 / 4 | 1 (on_load) |
| 3:106 | ROUTE 57 | 10 / 90 / 2 | 1 (on_load) |
| 3:107 | ROUTE 54 | 9 / 0 / 4 | 2 (on_frame_table), 1 (on_load) |
| 3:109 | MANDARIN CITY | 27 / 4 / 9 | 1 (on_load), 5 (on_resume) |
| 3:110 | ROUTE 59 | 22 / 3 / 18 | none |
| 3:111 | SCIENCE COMPLEX | 14 / 0 / 6 | 1 (on_load) |
| 5:86 | WEST VALE PORT | 20 / 5 / 2 | 255 (unknown_tag) |
| 5:87 | SANDWAY TOWN | 2 / 0 / 0 | 255 (unknown_tag) |
| 5:88 | SANDWAY TOWN | 2 / 0 / 0 | 255 (unknown_tag) |
| 5:89 | SANDWAY TOWN | 5 / 0 / 2 | 3 (on_transition), 5 (on_resume), 1 (on_load) |
| 5:90 | SANDWAY TOWN | 6 / 0 / 3 | none |
| 5:91 | SANDWAY TOWN | 5 / 3 / 2 | none |
| 5:92 | CRYSTAL CAVES | 15 / 6 / 3 | 1 (on_load), 3 (on_transition) |
| 5:93 | CRYSTAL CAVES | 1 / 0 / 0 | none |
| 5:95 | CRYSTAL CAVES | 5 / 0 / 0 | none |
| 5:96 | ROUTE 54 | 1 / 0 / 0 | 255 (unknown_tag) |
| 5:97 | CRYSTAL CAVES | 1 / 0 / 0 | 255 (unknown_tag) |
| 5:99 | NEXUS LABORATORY | 19 / 0 / 32 | none |
| 5:102 | NEXUS LABORATORY | 3 / 0 / 12 | 2 (on_frame_table) |
| 5:103 | CRYSTAL CAVES | 6 / 1 / 0 | none |
| 5:104 | CRYSTAL CAVES | 4 / 1 / 0 | 2 (on_frame_table) |
| 5:105 | ROUTE 56 | 1 / 0 / 0 | 255 (unknown_tag) |
| 6:23 | MANDARIN CITY | 3 / 0 / 12 | none |

## Interpretation limits

Object visibility flags, coordinate trigger operands and BG facing kinds are exported, not solved. BG kinds 5/6/7 contain hidden-item data and are not treated as script pointers. Object clones are explicitly unresolved if encountered; none are silently interpreted as normal objects.

Map-script tags use 5-byte entries ending only at tag zero. Unknown nonzero tags are retained and skipped by that format; they are not used as script roots. Only the first entry for a requested tag is selected in the reference. Types 2/4 point to 8-byte condition rows ending at a zero first operand; each compares VarGet of both operands. Coordinate events instead compare the low byte of their raw index operand. Runtime LC handlers have not all been verified.

## Focused traces

Stack-aware bounded format traces from map-owned references. Both condition outcomes retained. Standard/native/battle/warp returns are assumptions; condition values, collision and saved state are not simulated. Unsupported opcodes stop paths and remain frontiers. Shared roots and shared physical records preserve every owner association.

```json
{
  "focus_roots": 67,
  "unique_instruction_candidates": 800,
  "transition_or_destination_setter_instructions": 0,
  "layout_setter_instructions": 0,
  "unique_strict_complete_messages": 137,
  "instruction_overlap_records": 0,
  "frontier_reasons": {
    "unsupported opcode 15": 2,
    "unsupported opcode 7F": 3,
    "unsupported opcode 8F": 5,
    "unsupported opcode A4": 1
  }
}
```

Trace evidence: `extracted/scripts/route54_science_script_audit.json`. All instruction bytes, control edges, stop frontiers, owner association IDs and witness paths to selected state/transition/native candidates are retained. An unsupported opcode or assumed native return is not a game bug.

Pinned structure/execution references: `include/global.fieldmap.h`; `src/script.c:382–486`; `src/field_control_avatar.c:463–519,1025–1063`; `src/event_object_movement.c:1312–1341,2509–2516`; `asm/macros/map.inc`; `asm/macros/event.inc`. Full provenance and hashes are in `research/references/manifest.json`.
