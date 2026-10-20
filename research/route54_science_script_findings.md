# Route 54 and Science Complex: script ownership findings

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

CONFIRMED_IN_ROM: records, bytes, exact reuse and pointer ownership. STRONGLY_INFERRED: opcode/event semantics from pinned FireRed references. No emulator/playthrough, active save state or map-selection proof.

## Shared Route 54 gate

Both `3:101` and `3:107` have the same map-script table at `0x721A70`. Tag 2 points to conditional table `0x721D62`; its first row is operands `0x5305`, `0x0000` and script `0xA7094D`. The reference compares VarGet of both operands, then selects the first matching row.

The bounded path at `0xA7094D` sets operand `0x5305` to 1; moves object 6; removes object 6 at `0xA7099A`; moves object 5; removes object 5 at `0xA709BF`; sets flag `0x52E` at `0xA709C2`; then releases/ends. Both maps have local IDs 5/6 with visibility flag `0x52E`, at `(7,21)` and `(8,21)`. Their own script fields are null, while the map frame-script supplies this candidate blocker-removal event.

This gate is shared by both map IDs. It does not by itself explain which Route 54 variant is entered in gameplay. No warp or layout setter occurs in this complete local format path; movement, standard message routines and engine execution remain untested.

Dialogue referenced by that path:

`0xA7438C`

```text
<COLOR 08>Mateo: I don’t understand...<PARAGRAPH>

I went and looked all through the
Crystal Caves, yet there was no sign<SCROLL>
of the Crystal Onix...<PARAGRAPH>

Is it because those guys are here,
maybe it’s scared to come out...
```

`0xA71C43`

```text
<COLOR 08>Oh, it’s you.<PARAGRAPH>

So you made it through the Crystal
Caves then.<PARAGRAPH>

You probably heard, but the Crystal
Onix is nowhere to be found!<PARAGRAPH>

I don’t get it, was my Grandfather
lying?<PARAGRAPH>

Was the Crystal Onix just a hoax to
get publicity to the shop?<PARAGRAPH>

I don’t know what to believe
anymore...<PARAGRAPH>

I’m going to try and look one more
time, who knows, might just get<SCROLL>
lucky.<PARAGRAPH>

Oh, I never caught your name.<PARAGRAPH>

{PLAYER}, huh?<PARAGRAPH>

I thought I heard that somewhere
before...<PARAGRAPH>

Oh well, take care, {PLAYER}.
```

`0xA709C8`

```text
<COLOR 04>Marrisa: I’m sorry about all this.
```

## Reused Science Complex event data

Slots `3:99` (ROUTE 53 section) and `3:111` (SCIENCE COMPLEX section) have distinct map identities and layouts but the same map-script pointer `0x720AB4`. Their 14 object records and six BG records are byte-identical. This reuse is preserved as separate owner associations, not evidence that either slot is unused.

Object local IDs 1–8 and 10 carry visibility flag `0x513`; ID 9 carries `0x51C`; IDs 11–14 carry `0x542`. The ordinary script at `0xA60DC3` is owned by both maps and by cave `5:93` object 1; it branches on flag `0x513` to two message paths. This adds map ownership to previously observed Mister G/Nexus state, without establishing the active state of an uploaded save.

The six BG records comprise two null script fields, two Route 53 signposts pointing to `0xA24A7B`, and controllers `0xAD3E2C` / `0xAD3E52`. The signposts still name Route 53 in both map slots. Controller shutdown/status paths use the previously catalogued Nexus state (including flags `0x514` and `0x544`), with no new flag allocation or behavior change.

## Limits of the transition search

The focused search traces 67 unique roots owned by eight focus maps, from 332 roots catalogued across 32 map slots. It decodes 800 unique instruction candidates. No explicit script-warp/destination setter or layout setter was decoded in that bounded subset.

This does not prove those transitions absent: the shared load script at `0x8C457D` enters global helpers and stops at unsupported commands; native/standard calls and battle/wait resumes are assumptions. Other catalogued roots and native/map-selection paths have not been traced. Each frontier remains in the JSON. The earlier asymmetric warp/connection records still require caller and entry-route investigation.

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

## Alias checks

```json
[
  {
    "maps": [
      "3:101",
      "3:107"
    ],
    "same_map_script_pointer": true,
    "event_record_counts": [
      13,
      13
    ],
    "event_record_raw_differences": [],
    "interpretation": "Byte/association comparison only; map IDs remain distinct and runtime selection is UNKNOWN"
  },
  {
    "maps": [
      "3:99",
      "3:111"
    ],
    "same_map_script_pointer": true,
    "event_record_counts": [
      20,
      20
    ],
    "event_record_raw_differences": [],
    "interpretation": "Byte/association comparison only; map IDs remain distinct and runtime selection is UNKNOWN"
  }
]
```

All 555 exported event coordinates fit the inspected default layouts; saved/script layout overrides and actual accessibility remain unknown. Five hidden-item unions are retained without fabricating script pointers. Fourteen unknown map-script tags are exported, including eight encountered by the bounded scan from `0:0`; none become script roots.

Next bounded step: trace script and native references that select Route 54 `3:107` and Science Complex `3:111`, preserving the distinction between raw pointer occurrences, executable transition operands and actual playable entry.

Full evidence: `extracted/scripts/map_script_catalogue.json`, `map_script_associations.csv` and `route54_science_script_audit.json`. No ROM/save bytes changed; no content certified unused, broken or runtime-unreachable.
