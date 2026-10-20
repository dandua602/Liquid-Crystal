# Map variant selection audit

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

Selected variants 3:107 and 3:111, with 3:101 and 3:99 as comparison destinations. Physical group/bank pointer prefixes only; candidate slots and parsing failures are not a complete world-map certification. Warp and connection spans are parsed separately even when layouts/other arrays fail. Script traces cover only the prior 332 map-owned roots, plus bounded nearby raw-pointer targets for literal command shapes. All runtime reachability remains UNKNOWN.

CONFIRMED_IN_ROM: raw bytes, pointers, span/token checks and witnessed format paths. STRONGLY_INFERRED: FireRed field/command/native roles. Missing static evidence does not certify unused or unreachable maps.

```json
{
  "incoming_variant_warp_or_connection_associations": 0,
  "raw_variant_script_shapes": 14,
  "raw_shape_contexts": {
    "overlapping_ROM_pointer_word": 2,
    "pointer_backed_LZ77_stream": 8,
    "unresolved_context": 4
  },
  "shapes_on_catalogued_instruction_boundaries": 0,
  "nearby_pointer_format_witnesses_without_overlap": 0,
  "BL_shape_sites": 56,
  "sites_with_variant_constant_shapes": 0
}
```

## What the wider record scan establishes

Native table discovery yields 43 pointer-prefix groups and 1,504 candidate slots. Some slots are malformed, dummy or possible physical-prefix overrun candidates; the scan preserves their individual failures. It does not certify 1,504 real maps. Layout validation is recorded separately so a bad layout cannot suppress a readable warp/connection span.

No parsed literal warp/connection record in that scope targets `3:107` or `3:111`. Among sources with validated headers, three associations target `3:99` and six target `3:101`, including an additional `5:132` warp outside the prior 32-map cohort. Eight additional weak matches to `3:99` all reuse bytes at `0x170C7E` through the same unsuitable header `0x3525E4` in overlapping physical-prefix tails of groups 35–42; they are retained as unvalidated span evidence, not certified maps or warps. The large span-record total includes unsuitable candidates and is not a count of real game warps.

```json
{
  "groups_in_physical_prefix": 43,
  "candidate_slots": 1504,
  "banks_reaching_scan_limit": 0,
  "warp": {
    "slot_statuses": {
      "array_span_parsed": 1381,
      "null_pointer": 114,
      "unresolved": 9
    },
    "records_in_parsed_spans": 41381
  },
  "connection": {
    "slot_statuses": {
      "array_span_parsed": 139,
      "null_pointer": 1013,
      "unresolved": 352
    },
    "records_in_parsed_spans": 305
  },
  "incoming_candidate_associations_by_target": {
    "3:99": 11,
    "3:101": 6,
    "3:107": 0,
    "3:111": 0
  },
  "incoming_validated_header_associations_by_target": {
    "3:99": 3,
    "3:101": 6,
    "3:107": 0,
    "3:111": 0
  }
}
```

| Candidate source | Kind | Record | Destination | Source evidence |
|---|---|---|---|---|
| 3:98 | connection | 0x7471CC | 3:99 | validated_header_and_link_span |
| 3:100 | connection | 0x7480D4 | 3:99 | validated_header_and_link_span |
| 3:101 | connection | 0x7413BC | 3:101 | validated_header_and_link_span |
| 3:102 | connection | 0x741440 | 3:101 | validated_header_and_link_span |
| 3:107 | connection | 0x7413BC | 3:101 | validated_header_and_link_span |
| 5:93 | warp | 0x74BBE8 | 3:99 | validated_header_and_link_span |
| 5:95 | warp | 0xC00630 | 3:101 | validated_header_and_link_span |
| 5:96 | warp | 0x74F4EC | 3:101 | validated_header_and_link_span |
| 5:132 | warp | 0xC16F54 | 3:101 | validated_header_and_link_span |
| 35:55 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 36:47 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 37:42 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 38:37 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 39:36 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 40:35 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 41:34 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |
| 42:32 | warp | 0x170C7E | 3:99 | link_span_only_unvalidated_header |

## Literal script-shape triage

The all-byte scan covers the retained ordinary script warp/destination-setter opcodes, including the shorter warphole form. Fourteen raw `opcode, group=3, map=107/111` shapes occur. Eight lie wholly in pointer-backed well-formed LZ77 token streams; two overlap ROM pointer words at `0x6F036C` and `0x6F0388` (each points to `0x6F033F`); four contexts remain unclassified. Stream/pointer evidence is recorded without assuming that data can never be aliased deliberately.

None is an instruction boundary reached in the bounded 332-root catalogue search, or by the bounded nearby incoming-pointer-target searches. The catalogue paths decode 3,717 unique instruction candidates, with explicit unsupported/non-ROM frontiers. The four unclassified contexts are not silently rejected or promoted to scripts.

| Raw offset | Opcode | Destination | Context |
|---|---|---|---|
| 0x29188B | 0x40 | 3:111 | pointer_backed_LZ77_stream |
| 0x3D0595 | 0x40 | 3:111 | pointer_backed_LZ77_stream |
| 0x40EE47 | 0xD1 | 3:111 | pointer_backed_LZ77_stream |
| 0x424326 | 0x40 | 3:111 | unresolved_context |
| 0x430E4E | 0x40 | 3:111 | unresolved_context |
| 0x603F66 | 0xD1 | 3:111 | unresolved_context |
| 0x6F036C | 0x3F | 3:111 | overlapping_ROM_pointer_word |
| 0x6F0388 | 0x3F | 3:111 | overlapping_ROM_pointer_word |
| 0xD06A44 | 0x40 | 3:107 | pointer_backed_LZ77_stream |
| 0xD13B7C | 0x40 | 3:111 | pointer_backed_LZ77_stream |
| 0xDD9346 | 0x40 | 3:111 | pointer_backed_LZ77_stream |
| 0xE63774 | 0x40 | 3:111 | unresolved_context |
| 0xE8D8B7 | 0x40 | 3:107 | pointer_backed_LZ77_stream |
| 0xEB0A67 | 0x40 | 3:111 | pointer_backed_LZ77_stream |

## Header pointers and native evidence

Route 54 variant header `0xC24978` has one all-alignment absolute ROM pointer, its native bank slot `0xC2B0B4`. Science Complex header `0xC313D0` has bank slot `0xC2B0C4` plus a data pointer at `0xC32A2C`. The latter is +12 inside a layout-shaped fragment beginning `0xC32A20` (68×42); no absolute ROM pointer to that fragment was found. This supplies data-geometry evidence, without a validated native code-literal use or indexed alternate-layout identity.

Thumb-1 BL shapes at every halfword alignment to the independently discovered map lookup, last BL targets in five setter-handler intervals, and checksum-verified prior native wrappers. Previous 32 bytes inspected only for MOVS and PC-relative LDR constant shapes; no register/control-flow analysis. Raw BL shapes can occur in data; indirect calls, computed IDs and RAM writes are outside this probe.

The setter target `0x5538C` comes from the last BL in the independently found setwarp handler; it is not guessed from the original FireRed address. Five setter-handler intervals compare equal to supplied FireRed. This supports local decoding, not every caller/callee behavior. There are 56 BL-shape sites to the selected lookup/setter/wrapper targets. Their prior 32 bytes contain no immediate/literal value 107 or 111 in the limited MOVS/LDR probe. Computed map IDs, nonlocal register assignments, alternative/native hooks and RAM data remain unresolved.

## Conclusion and next step

The inspected static topology selects the original Route 54/Route 53 IDs, while the two variants have no supported literal entry in this bounded audit. This supports treating them as candidate disconnected copies for further research; neither is certified unused, broken or runtime-unreachable. No map ID is removed or repurposed.

Next bounded step: expand the Orange map inventory from Route 59’s outgoing links and catalogue the destination entry scripts, to follow surviving progression toward the beta dead end.

Full evidence: `extracted/maps/map_selection_audit.json` and `map_selection_incoming.csv`; retained semantics in `research/warp_semantics_notes.md`, `src/scrcmd.c:719–865` and `asm/macros/event.inc`. All original source bytes remain untouched.
