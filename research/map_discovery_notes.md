# Independent map structure discovery: Nexus controller ownership

Source: locked Liquid Crystal ROM SHA-256 `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. This investigation read ROMs and reports only and created this independent note. All offsets are ROM file offsets; stored pointers add `0x08000000`. Group/map numbers and BG-event indices are decimal and zero-based. No runtime reachability or event accessibility has been established.

## Discovery chain

Each of the ten known controller roots has incoming pointer sites in `extracted/text/nexus_machine_audit.json`. All 17 sites fit script fields at `+8` in 12-byte `BgEvent` records. Searching nearby candidate `MapEvents` records, then all-ROM incoming pointers to those records, identifies ten map headers. Incoming references to the headers locate the group-map arrays. References to the relevant group-array starts meet at `0x3526A8`, whose address is independently used by native map lookup code. No Liquid Crystal map-table address was assumed from FireRed.

Native lookup function `[0x55238, 0x55250)` including its literal:

```text
00 04 09 04 03 4A 80 0B 80 18 00 68 89 0B 09 18 08 68 70 47 A8 26 35 08
```

The instructions mask two input arguments to 16 bits, multiply each by four, load the group-array pointer from the table at `0x083526A8`, then load the map-header pointer from that array. The literal is at `0x5524C`. This exact 24-byte span also matches the supplied FireRed ROM; SHA-256 `5c54a38e516f692c233b81bfb5d16d6ae8df4a2e112e15d3c743d1c5866ca063`. Pinned `src/overworld.c:541` supplies the corresponding interpretation `gMapGroups[mapGroup][mapNum]`; addresses came from Liquid Crystal pointer chains.

Validated group entries:

| Group | Top-level pointer site | Bytes | Map-array base |
|---|---|---|---|
| 3 | `0x3526B4` | `08 AF C2 08` | `0xC2AF08` |
| 5 | `0x3526BC` | `18 28 C2 08` | `0xC22818` |
| 6 | `0x3526C0` | `B8 3E C1 08` | `0xC13EB8` |

## Controller owners and coordinates

Kind and elevation bytes are both zero in every listed BG event. The table preserves script reuse in separate maps and two events sharing the same root in map `5:86`.

| Root | Pointer site | Group:map | BG index | BG record | x,y | Header | Events |
|---|---|---|---|---|---|---|---|
| `0xAD344E` | `0xC01900` | `5:102` | 11 | `0xC018F8` | 11,1 | `0xC00A6C` | `0xC01904` |
| `0xAD344E` | `0xC18E58` | `6:23` | 11 | `0xC18E50` | 16,4 | `0xC18AE4` | `0xC18E5C` |
| `0xAD354B` | `0xC04308` | `3:102` | 2 | `0xC04300` | 5,49 | `0xB4A100` | `0xC04318` |
| `0xAD3D6E` | `0xC04314` | `3:102` | 3 | `0xC0430C` | 8,54 | `0xB4A100` | `0xC04318` |
| `0xAD3D94` | `0xC02AAC` | `3:101` | 3 | `0xC02AA4` | 55,9 | `0xB30B88` | `0xC02AB0` |
| `0xAD3D94` | `0xC04600` | `3:104` | 3 | `0xC045F8` | 13,17 | `0xC0C90C` | `0xC04604` |
| `0xAD3D94` | `0xC2611C` | `3:107` | 3 | `0xC26114` | 55,9 | `0xC24978` | `0xC26120` |
| `0xAD3DBA` | `0xC02AA0` | `3:101` | 2 | `0xC02A98` | 24,14 | `0xB30B88` | `0xC02AB0` |
| `0xAD3DBA` | `0xC26110` | `3:107` | 2 | `0xC26108` | 24,14 | `0xC24978` | `0xC26120` |
| `0xAD3DE0` | `0xC04B30` | `3:100` | 5 | `0xC04B28` | 12,6 | `0xB29130` | `0xC04B4C` |
| `0xAD3E06` | `0xC04B3C` | `3:100` | 6 | `0xC04B34` | 38,28 | `0xB29130` | `0xC04B4C` |
| `0xAD3E2C` | `0xC02974` | `3:99` | 4 | `0xC0296C` | 26,17 | `0xB1E89C` | `0xC02984` |
| `0xAD3E2C` | `0xC32560` | `3:111` | 4 | `0xC32558` | 26,17 | `0xC313D0` | `0xC32570` |
| `0xAD3E52` | `0xC02980` | `3:99` | 5 | `0xC02978` | 18,24 | `0xB1E89C` | `0xC02984` |
| `0xAD3E52` | `0xC3256C` | `3:111` | 5 | `0xC32564` | 18,24 | `0xC313D0` | `0xC32570` |
| `0xAD3E78` | `0xC01474` | `5:86` | 0 | `0xC0146C` | 116,14 | `0xB278B8` | `0xC01484` |
| `0xAD3E78` | `0xC01480` | `5:86` | 1 | `0xC01478` | 117,14 | `0xB278B8` | `0xC01484` |

## Header and event geometry

`MapHeader` uses layout/events/scripts/connections at `+0/+4/+8/+12`, map-layout ID at `+0x12`, and region/map-section ID at `+0x14`. `MapEvents` has four counts followed by four pointers (objects, warps, coordinate triggers, background events), total 20 bytes. Standard record sizes are 24, 8, 16 and 12 bytes respectively. For all ten maps, every array begins exactly where the preceding count/stride ends; the BG array ends exactly at the owning `MapEvents` record. Zero-count coordinate arrays share their base with the BG array. This independently validates the struct geometry across different counts, coordinates and layouts.

| Group:map | Layout | Width×height | Layout ID | Section | Counts object/warp/coord/BG | Object / warp / coord / BG array starts |
|---|---|---|---|---|---|---|
| `3:99` | `0xB1F880` | 42×48 | `0x333` | `0xE7` | 14/1/0/6 | `0xC027E4` / `0xC02934` / `0xC0293C` / `0xC0293C` |
| `3:100` | `0xC082F8` | 100×36 | `0x334` | `0xE8` | 17/7/10/8 | `0xC0487C` / `0xC04A14` / `0xC04A4C` / `0xC04AEC` |
| `3:101` | `0xB3464C` | 68×42 | `0x33E` | `0xEA` | 9/2/0/4 | `0xC02998` / `0xC02A70` / `0xC02A80` / `0xC02A80` |
| `3:102` | `0xB4B774` | 42×68 | `0x340` | `0xEB` | 12/1/0/4 | `0xC041C0` / `0xC042E0` / `0xC042E8` / `0xC042E8` |
| `3:104` | `0xC0DF80` | 68×42 | `0x34B` | `0xED` | 12/2/0/4 | `0xC044A4` / `0xC045C4` / `0xC045D4` / `0xC045D4` |
| `3:107` | `0xC25FEC` | 68×42 | `0x35C` | `0xEA` | 9/2/0/4 | `0xC26008` / `0xC260E0` / `0xC260F0` / `0xC260F0` |
| `3:111` | `0xC323B4` | 42×48 | `0x379` | `0xF3` | 14/1/0/6 | `0xC323D0` / `0xC32520` / `0xC32528` / `0xC32528` |
| `5:86` | `0xB29114` | 155×20 | `0x332` | `0xE6` | 20/40/5/2 | `0xC010FC` / `0xC012DC` / `0xC0141C` / `0xC0146C` |
| `5:102` | `0xC00CE8` | 20×15 | `0x348` | `0xEC` | 3/1/0/12 | `0xC01824` / `0xC0186C` / `0xC01874` / `0xC01874` |
| `6:23` | `0xC18D60` | 20×15 | `0x36E` | `0xF1` | 3/1/0/12 | `0xC18D7C` / `0xC18DC4` / `0xC18DCC` / `0xC18DCC` |

## Header section labels

Liquid Crystal has a name-pointer table at `0x2C8980`. The native name-returning function at `0xC4D78` derives index `mapsec - 0x58`: its literal `00 00 A8 FF` at `0xC4D9C` is the shifted subtraction constant, and its literal at `0xC4DB8` is `80 89 2C 08`. It loads the name at table base plus four times that index and copies the string. A department-store special case exists in the reference; these section IDs are outside that original special-case map-section ID.

Exact inspected native bytes `[0xC4D78, 0xC4DBC)`:

```text
70 B5 06 1C 09 04 12 04 14 0C 08 0C 05 4A 89 18 0D 0C A4 2D 16 D8 FF F7 D7 FF 01 28 06 D1 02 49 08 E0 00 00 00 00 A8 FF 2E F2 3E 08 04 48 A9 00 09 18 09 68 30 1C 43 F7 E9 FF 01 1C 0B E0 00 00 80 89 2C 08
```

The following labels are read from those section indices; they are section labels, not independently established individual building/floor names. In particular, multiple physical maps may share a section.

| Section | Pointer site | Text offset | Label | Maps in this investigation |
|---|---|---|---|---|
| `0xE6` | `0x2C8BB8` | `0x71B60C` | WEST VALE PORT | 5:86 |
| `0xE7` | `0x2C8BBC` | `0x71D388` | ROUTE 53 | 3:99 |
| `0xE8` | `0x2C8BC0` | `0x71DD90` | SANDWAY TOWN | 3:100 |
| `0xEA` | `0x2C8BC8` | `0x71DDB0` | ROUTE 54 | 3:101, 3:107 |
| `0xEB` | `0x2C8BCC` | `0x721D04` | ROUTE 55 | 3:102 |
| `0xEC` | `0x2C8BD0` | `0x723AB0` | NEXUS LABORATORY | 5:102 |
| `0xED` | `0x2C8BD4` | `0xC003E8` | ROUTE 56 | 3:104 |
| `0xF1` | `0x2C8BE4` | `0xC04EA4` | MANDARIN CITY | 6:23 |
| `0xF3` | `0x2C8BEC` | `0xC05304` | SCIENCE COMPLEX | 3:111 |

## Safe scope and bank extents

Targeted ownership needs no guessed bank lengths. For each header-pointer site, compute `(site - validated_group_array_base) / 4`, require an exact nonnegative integer, and verify the group entry, target header, event structure, BG index/coordinate, and root pointer. Use the native lookup table as the anchor. A header pointer elsewhere in arbitrary data (for example layout/map data can contain the same value) does not alone identify a group-map slot.

Do not use the next numeric group pointer as an end address: group arrays are scattered and nonmonotonic. Do not reject an entire bank merely because some earlier map entries have dummy, reused, or unsuitable layout data. Such headers exist in this ROM.

Physical pointer runs give bounded scan candidates only: group 3 has pointer-looking words in `[0xC2AF08,0xC2B0C8)`, group 5 in `[0xC22818,0xC22A2C)`, and group 6 in `[0xC13EB8,0xC13F38)`, followed by `F7 F7 F7 F7`. These imply candidate physical lengths 112, 133 and 32; this investigation does not certify every slot or an engine-enforced map count. In group 5, pointer-looking data immediately precedes the true start `0xC22818`, demonstrating why a maximal pointer run is insufficient to locate an array start. The top-level table has 43 pointer-looking entries through `0x352750`, followed by `FF`; no native bounds check or count was established.

Additional prefix inspection supports these physical extents: every slot in all three prefixes points to a four-byte-aligned, in-ROM 28-byte header whose layout pointer is in-ROM and halfword-aligned, and whose nonzero event/script/connection pointer fields point into ROM. Their type/biking/flag/battle bytes retain plausible small values. Every nonempty event-array count/pointer pair passes span checks in groups 3 and 6. Group 5 map 55 has unsuitable event-array bytes; group 5 maps 25, 28 and 83 and group 6 map 4 have unsuitable layout dimensions. These failures are explicitly retained as individual slot concerns, not reasons to continue past a bank sentinel or discard later validated map slots. All ten targeted owners pass the full layout/event/BG checks.

For broader extraction, retain these physical bounds as candidate limits, validate each selected header/event/layout separately, and report validation failures instead of silently trimming or assuming contiguity implies validity. Warp targets, map scripts, collision, active flag states and map-entry conditions remain a separate stage. Static ownership does not establish runtime reachability.

## Pinned official interpretation sources

URL prefix `https://raw.githubusercontent.com/pret/pokefirered/037335f4c725d7c9aecdac87066f2002b4bd7e14/`. Files were fetched with normal TLS verification to `/tmp`; root may retain them in the project reference manifest.

| Source | Local temporary path | SHA-256 |
|---|---|---|
| `include/global.fieldmap.h` | `/tmp/include__global.fieldmap.h` | `34a8c91e10803ba48b97a2df8a721ca37fad7572b2ff951a4ab7ec15a5f050eb` |
| `include/global.h` | `/tmp/include__global.h` | `044325b90e7c79146cc0cf73d31b6be3e4840059e2e778b63d9b5448fe538429` |
| `include/fieldmap.h` | `/tmp/include__fieldmap.h` | `e7d93120d2695043c7d75067f3c768344622c198503b0671d47292d6aa708a43` |
| `src/overworld.c` | `/tmp/src__overworld.c` | `df352e738b56856765aec65adc6fdea0a4b25fe567bc760d4ce2d34afc6ff7e2` |
| `src/region_map.c` | `/tmp/src__region_map.c` | `b761f02803a1c5aada4465b9a93bf2b02c5ef1118432e677a30a5a4a4b78e0cb` |

`include/global.fieldmap.h` defines the relevant event/layout/header geometry; `src/overworld.c:541` defines indexed group/map lookup; `src/region_map.c:3801` defines indexed section-name lookup. These references support field meanings and instruction interpretation, not address reuse.

## Suggested targeted checks

1. Reverify source hashes and decode the native table lookup bytes/literal.
2. Assert the three group-table pointers and each map-array/header/event pointer chain.
3. Assert all four event-array span equations for each owner and every controller pointer equals its known script root.
4. Check BG coordinates lie within the referenced layout width/height and retain zero-based event indices.
5. Preserve all 17 references and ten map owners; do not deduplicate maps merely because scripts or event coordinates match.
6. Keep map section labels separate from individual floor/building identities and from runtime reachability.
