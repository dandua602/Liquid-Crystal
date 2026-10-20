# Independent warp and connection destination review

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. Reviewed all 58 warp rows and 13 connection-owner rows exported by `controller_map_owners.json`. All group/map/warp IDs below are decimal and zero-based; hexadecimal values are ROM file offsets.

All destinations were read again from raw records and resolved through the native group table at `0x3526A8`. Physical group/bank pointer prefixes are scan limits, not certified engine bounds. Static links, reciprocal records and coordinate checks do not establish playability, gates, collision behavior or save-state access. No ROM/save/core-tool changes were made.

## Counts

```json
{
  "source_sha256": "c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf",
  "warp_rows": 58,
  "distinct_warp_destination_maps": 19,
  "first_hop_warps_resolved": 58,
  "source_and_landing_coordinates_in_layout": 58,
  "warp_return_classifications": {
    "EXACT_ENCODED_RETURN": 26,
    "DIFFERENT_STATIC_RETURN_MAP": 20,
    "SAME_SOURCE_MAP_OTHER_WARP": 1,
    "DYNAMIC_RETURN_SENTINEL": 11
  },
  "connection_owner_rows": 13,
  "distinct_physical_connection_records": 11,
  "connection_map_slots_resolved": 13,
  "connection_targets_passing_full_header_parser": 13,
  "connections_with_exact_encoded_reverse": 7,
  "connections_without_exact_encoded_reverse": 6,
  "connections_with_positive_axis_overlap": 13,
  "gameplay_reachability": "UNKNOWN"
}
```

All 58 warp targets have in-prefix map slots, full header/event/layout validation, in-range warp indices, and source/landing coordinates inside their layouts. There are no unresolved first-hop warp records in this cohort. A return classification is a comparison of encoded rows, not an execution test.

## Findings

- `5:86` warp 0 (`0xC012DC`) and warp 1 (`0xC012E4`) both land at `3:98` warp 2 (`0x849B94`), which points to `5:86` warp 0. This is a two-source-to-one-destination door pattern, not automatically a defect.
- Eleven `5:86` warps (5, 6, 7, 10, 11, 13, 14, 19, 27, 29, 39) land at `0:0` warp 0 (`0x722A84`). That landing row stores return tuple `127:127`, warp 127. Pinned `constants/maps.h` identifies map number 127 as MAP_DYNAMIC, and `field_control_avatar.c` SetupWarp consumes saved dynamic warp state. These eleven return destinations are runtime-dependent; do not count them as invalid map-127 links or certified one-way paths. LC runtime behavior remains unverified.
- Twenty other rows have a different static return map: two exits from `3:107` return to `3:101`; the `3:111` exit returns to `3:99`; six internal `5:86` links land on warps that then point to `0:0`; and eleven `5:86` links enter map `1:99`, whose landing rows return within `1:99` or toward `0:0`. These are encoded asymmetries to retain for follow-up, not proof of inaccessible, broken or obsolete content.
- Map `1:99` is a real structurally validated slot: group 1 base `0x78C2A0`, slot `0x78C42C`, header `0x34FCE8`, 155×20 layout, 40 warp rows at `0x9004D8`. Its warp array and mapblock data differ from `5:86`; it cannot be collapsed into that map merely because the dimensions/count match.
- Three pairs of warp records are byte-identical: `3:99`/`3:111` warp 0, and `3:101`/`3:107` warps 0 and 1. The first pair has different mapblock data (1,733 of 2,016 halfwords differ). The latter pair has identical 2,856-halfword mapblock data, shares map scripts at `0x721A70` and connections at `0x7413D4`, but keeps separate headers/events/layout addresses. Both owner identities remain recorded.
- Connection rows total 13 owner associations but 11 distinct physical records, because maps `3:101` and `3:107` share records `0x7413BC` and `0x7413C8`. Seven owner associations have opposite-direction, negated-displacement return records. Six have no such exact return. All thirteen have positive projected edge overlap under the decoded dimensions/displacement.
- `3:100` connection at `0x7480E0` resolves to map `3:60`: slot `0xC2AFF8` → header `0x350CA8`, layout `0x32F3B4` (30×56). The events word at `0x350CAC` is zero. The current parser explicitly preserves null events instead of claiming a populated event structure, so all 13 destination headers now pass its structural policy; 12 targets have nonnull events and this one does not. Its connection structure at `0x352E68` is readable; it provides no exact return to `3:100` and contains a direction-0 (CONNECTION_NONE) row at `0x352E5C` toward `3:61`. Null events and the source/map state need native/runtime investigation before any defect claim.
- `3:101` has a west self-connection with displacement +28 at `0x7413BC`; no east inverse exists in its connection list. That same physical record belongs to `3:107`, where it points to `3:101`. Section labels do not resolve which version is selected in play.

## Warp ledger

| Source | Record | Target | Landing record | Landing row returns to | Static comparison |
|---|---|---|---|---|---|
| 3:99 #0 | `0xC02934` | 5:93 #0 | `0x74BBE8` | 3:99 #0 | EXACT_ENCODED_RETURN |
| 3:100 #0 | `0xC04A14` | 5:90 #1 | `0x7BB1C8` | 3:100 #0 | EXACT_ENCODED_RETURN |
| 3:100 #1 | `0xC04A1C` | 5:91 #1 | `0xC0ABE4` | 3:100 #1 | EXACT_ENCODED_RETURN |
| 3:100 #2 | `0xC04A24` | 5:92 #2 | `0xC01AF0` | 3:100 #2 | EXACT_ENCODED_RETURN |
| 3:100 #3 | `0xC04A2C` | 5:88 #0 | `0x843230` | 3:100 #3 | EXACT_ENCODED_RETURN |
| 3:100 #4 | `0xC04A34` | 5:89 #1 | `0x882270` | 3:100 #4 | EXACT_ENCODED_RETURN |
| 3:100 #5 | `0xC04A3C` | 5:87 #0 | `0x76C0F8` | 3:100 #5 | EXACT_ENCODED_RETURN |
| 3:100 #6 | `0xC04A44` | 5:103 #0 | `0xC0051C` | 3:100 #6 | EXACT_ENCODED_RETURN |
| 3:101 #0 | `0xC02A70` | 5:95 #2 | `0xC00630` | 3:101 #0 | EXACT_ENCODED_RETURN |
| 3:101 #1 | `0xC02A78` | 5:96 #0 | `0x74F4EC` | 3:101 #1 | EXACT_ENCODED_RETURN |
| 3:102 #0 | `0xC042E0` | 5:97 #0 | `0x7D79A4` | 3:102 #0 | EXACT_ENCODED_RETURN |
| 3:104 #0 | `0xC045C4` | 5:104 #1 | `0xC00D6C` | 3:104 #0 | EXACT_ENCODED_RETURN |
| 3:104 #1 | `0xC045CC` | 5:105 #0 | `0xC04488` | 3:104 #1 | EXACT_ENCODED_RETURN |
| 3:107 #0 | `0xC260E0` | 5:95 #2 | `0xC00630` | 3:101 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 3:107 #1 | `0xC260E8` | 5:96 #0 | `0x74F4EC` | 3:101 #1 | DIFFERENT_STATIC_RETURN_MAP |
| 3:111 #0 | `0xC32520` | 5:93 #0 | `0x74BBE8` | 3:99 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #0 | `0xC012DC` | 3:98 #2 | `0x849B94` | 5:86 #0 | EXACT_ENCODED_RETURN |
| 5:86 #1 | `0xC012E4` | 3:98 #2 | `0x849B94` | 5:86 #0 | SAME_SOURCE_MAP_OTHER_WARP |
| 5:86 #2 | `0xC012EC` | 5:86 #3 | `0xC012F4` | 5:86 #2 | EXACT_ENCODED_RETURN |
| 5:86 #3 | `0xC012F4` | 5:86 #2 | `0xC012EC` | 5:86 #3 | EXACT_ENCODED_RETURN |
| 5:86 #4 | `0xC012FC` | 5:86 #15 | `0xC01354` | 5:86 #4 | EXACT_ENCODED_RETURN |
| 5:86 #5 | `0xC01304` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #6 | `0xC0130C` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #7 | `0xC01314` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #8 | `0xC0131C` | 1:99 #31 | `0x9005D0` | 1:99 #8 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #9 | `0xC01324` | 5:86 #26 | `0xC013AC` | 5:86 #9 | EXACT_ENCODED_RETURN |
| 5:86 #10 | `0xC0132C` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #11 | `0xC01334` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #12 | `0xC0133C` | 5:86 #6 | `0xC0130C` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #13 | `0xC01344` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #14 | `0xC0134C` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #15 | `0xC01354` | 5:86 #4 | `0xC012FC` | 5:86 #15 | EXACT_ENCODED_RETURN |
| 5:86 #16 | `0xC0135C` | 5:86 #23 | `0xC01394` | 5:86 #16 | EXACT_ENCODED_RETURN |
| 5:86 #17 | `0xC01364` | 1:99 #30 | `0x9005C8` | 1:99 #17 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #18 | `0xC0136C` | 1:99 #27 | `0x9005B0` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #19 | `0xC01374` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #20 | `0xC0137C` | 5:86 #5 | `0xC01304` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #21 | `0xC01384` | 5:86 #14 | `0xC0134C` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #22 | `0xC0138C` | 5:86 #19 | `0xC01374` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #23 | `0xC01394` | 5:86 #16 | `0xC0135C` | 5:86 #23 | EXACT_ENCODED_RETURN |
| 5:86 #24 | `0xC0139C` | 1:99 #36 | `0x9005F8` | 1:99 #24 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #25 | `0xC013A4` | 1:99 #29 | `0x9005C0` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #26 | `0xC013AC` | 5:86 #9 | `0xC01324` | 5:86 #26 | EXACT_ENCODED_RETURN |
| 5:86 #27 | `0xC013B4` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #28 | `0xC013BC` | 5:86 #11 | `0xC01334` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #29 | `0xC013C4` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:86 #30 | `0xC013CC` | 5:86 #32 | `0xC013DC` | 5:86 #30 | EXACT_ENCODED_RETURN |
| 5:86 #31 | `0xC013D4` | 1:99 #8 | `0x900518` | 1:99 #31 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #32 | `0xC013DC` | 5:86 #30 | `0xC013CC` | 5:86 #32 | EXACT_ENCODED_RETURN |
| 5:86 #33 | `0xC013E4` | 5:86 #13 | `0xC01344` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #34 | `0xC013EC` | 1:99 #7 | `0x900510` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #35 | `0xC013F4` | 1:99 #10 | `0x900528` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #36 | `0xC013FC` | 1:99 #24 | `0x900598` | 1:99 #36 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #37 | `0xC01404` | 1:99 #39 | `0x900610` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #38 | `0xC0140C` | 1:99 #32 | `0x9005D8` | 0:0 #0 | DIFFERENT_STATIC_RETURN_MAP |
| 5:86 #39 | `0xC01414` | 0:0 #0 | `0x722A84` | 127:127 #127 | DYNAMIC_RETURN_SENTINEL |
| 5:102 #0 | `0xC0186C` | 5:99 #2 | `0xC00880` | 5:102 #0 | EXACT_ENCODED_RETURN |
| 6:23 #0 | `0xC18DC4` | 3:109 #4 | `0xC22728` | 6:23 #0 | EXACT_ENCODED_RETURN |

## Connection ledger

Directions: 1 south, 2 north, 3 west, 4 east under the pinned definitions. Reverse requires opposite direction, negated displacement and the original source map.

| Source | Record | Direction / shift | Target | Exact reverse record | Target full-header check |
|---|---|---|---|---|---|
| 3:99 | `0x72192C` | 2 / 0 | 3:98 | `0x7471CC` | validated by targeted full-header parser |
| 3:99 | `0x721938` | 4 / 18 | 3:100 | `0x7480D4` | validated by targeted full-header parser |
| 3:100 | `0x7480D4` | 3 / -18 | 3:99 | `0x721938` | validated by targeted full-header parser |
| 3:100 | `0x7480E0` | 2 / 8 | 3:60 | none | validated by targeted full-header parser |
| 3:100 | `0x7480EC` | 4 / 0 | 3:104 | none | validated by targeted full-header parser |
| 3:101 | `0x7413BC` | 3 / 28 | 3:101 | none | validated by targeted full-header parser |
| 3:101 | `0x7413C8` | 2 / 2 | 3:102 | `0x741440` | validated by targeted full-header parser |
| 3:102 | `0x741440` | 1 / -2 | 3:101 | `0x7413C8` | validated by targeted full-header parser |
| 3:102 | `0x74144C` | 3 / 0 | 3:103 | `0xC00418` | validated by targeted full-header parser |
| 3:104 | `0xC01964` | 4 / 0 | 3:106 | `0xC02AC4` | validated by targeted full-header parser |
| 3:107 | `0x7413BC` | 3 / 28 | 3:101 | none | validated by targeted full-header parser |
| 3:107 | `0x7413C8` | 2 / 2 | 3:102 | none | validated by targeted full-header parser |
| 3:111 | `0xC052F0` | 4 / 14 | 3:110 | none | validated by targeted full-header parser |

## Independent graph-output cross-check

The generated `controller_connectivity.json` has the same 32 map IDs as this independent one-hop resolution. All 58 landing-record offsets and return classifications agree. Native layout lookup at `0x55170` uses literal `0x55194` → table `0xC2FC30`; all 32 selected `layoutId - 1` slots match their header layout pointers. Eighteen zero words occur before the maximum selected layout index, so zero entries cannot be used as a table terminator. The graph expands only the ten owner maps; other maps retain records solely as landing/return evidence. Saved layout overrides and runtime transitions remain outside this check.

## Reference and reproduction notes

Raw addresses and values come from the locked ROM. Geometry/meaning uses the retained `include/global.fieldmap.h`, native lookup discovery and pinned official sources already fetched read-only to `/tmp`: `include/constants/maps.h`, `include/constants/global.h`, `src/field_control_avatar.c` and `src/fieldmap.c`. The dynamic sentinel is explicit in `constants/maps.h:9`; SetupWarp tests map number 127 at `field_control_avatar.c:971`. These source meanings alone do not establish LC handler identity or runtime state.

The independent temporary audit saved full machine-readable evidence to `/tmp/warp_destination_review.json`. Reproduce by decoding each source WarpEvent as `<hhBBBB`, resolving header via `group_table[group]` then `group_array[map]`, validating its warp-count/index and landing coordinates, and comparing the landing row’s encoded return tuple. Decode each connection as direction byte, signed displacement at +4 and group/map bytes at +8/+9; check reverse rows separately from destination/header validity. Keep shared physical records as separate source-map associations.
