# Warp, connection and layout semantics: independent research

Source ROM: Liquid Crystal SHA-256 `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. Read-only source/ROM inspection, with this note and five pinned interpretation references retained in the project manifest. Application tools, tests, ROMs and saves were not changed by this investigation. All addresses are ROM file offsets. Counts refer to `extracted/maps/controller_map_owners.json`: 58 source warp records, 13 source connection records, ten source maps. These are static structures, not certified gameplay paths.

## Warp-event semantics

Pinned `src/field_control_avatar.c:965–984`, `SetupWarp`, directly indexes a target's `warps[warpEvent->warpId]`; the destination warp index is **zero-based**, without subtracting one. `GetWarpEventAtPosition` (`:1008–1022`) also returns the zero-based array index, matches x/y, and permits event elevation zero to match any elevation. Triggering still depends on metatile behavior and the caller; a warp record at walkable coordinates does not establish activation.

The source's dynamic test is specifically `warpEvent->mapNum == 0x7F` (`:971`). The event's map-group byte is ignored for that decision. `SetWarpDestinationToDynamicWarp` copies the saved `dynamicWarp` and ignores its warp-ID argument (`src/overworld.c:610–612`). `include/constants/maps.h:7–26` defines `MAP_DYNAMIC` as `0x7F:0x7F`, `WARP_ID_DYNAMIC` as `0x7F`, and `WARP_ID_NONE` as `-1`. Thus:

| Encoded form | Supported reference interpretation |
|---|---|
| event destination mapNum `0x7F` | Use saved dynamic warp; event group/warp ID do not select a static target |
| event warpId `0x7F`, static mapNum | Ordinary target array index 127; warp ID alone does not select dynamic behavior |
| signed `WarpData.warpId = -1` / byte `FF` | No target warp coordinate; landing may use explicit coordinates or default center |
| group/map `0:0` | Ordinary static target, not a generic sentinel |
| group/map `FF:FF` | Part of the dummy `WarpData` representation; no blanket normal-event bypass is shown |

`WarpData` has signed 8-bit group/map/warp fields (`include/global.h:392–398`), whereas `WarpEvent` has unsigned 8-bit destination fields (`include/global.fieldmap.h:136–143`). Preserve the raw bytes and distinguish the two contexts. `IsDummyWarp` (`src/overworld.c:525–539`) checks all five dummy fields, including coordinates `-1`; it does not treat any one `FF` field as a complete dummy warp.

`SetPlayerCoordsFromWarp` (`src/overworld.c:564–581`) uses the target warp's x/y only when the stored signed warp index is nonnegative and less than target warpCount, otherwise explicit nonnegative coordinates, otherwise the map center. **This is not evidence that an invalid normal warp-event index is safe**: `SetupWarp` already dereferences `target.events->warps[event.warpId]` without a preceding bound check to test for a dynamic return. Validate static target index/count before interpreting it.

When a static source event targets a target warp whose mapNum is `0x7F`, `SetupWarp` saves the current map and source event index as the dynamic return (`src/field_control_avatar.c:982–983`; `src/overworld.c:600–607`). A peculiar extra expression reads the target's warp at the *source event index* to supply the first `SetDynamicWarp` argument; that argument is unused. Do not use that ignored argument or its raw byte to infer the effective saved return. The meaningful saved return is the current group/map and originating event index.

## Native Liquid Crystal corroboration

These native intervals were found by following the independently located map-lookup code and Thumb branch-with-link targets, then compared byte-for-byte with the supplied original FireRed ROM. Their bodies match exactly:

| Interval, exclusive end | Interpreted role | SHA-256 |
|---|---|---|
| `[0x6DC54,0x6DCD0)` | SetupWarp, including literals, 124 bytes | `6d6e4aa93d3c878301864a2cba34665cce488962810c20d993ac3f903ddb2b2b` |
| `[0x552FC,0x55378)` | Landing-coordinate selection, including literals | `b4d5ebd3afb0b3ae098ae941b9d2aacb3b3809262383be260da7605de69d4e0a` |
| `[0x553C8,0x55468)` | Map-warp and saved-dynamic setters, with neighboring setter code/literals | `19e16e4449b3bb624931ed9c1b5eb81a44d468bfcb47fb143536562ccb890ae7` |
| `[0x55454,0x5546C)` | Copy saved dynamic warp to destination | `3159d3745bb661398af6cbff017614e4ed474ef907dd5a089d26465a5a1d0aee` |

Within the first function the source mapNum compare against `7F` is at `0x6DC66`; the target warp's mapNum compare against `7F` is at `0x6DCA8`. Calls select map-warp setter `0x553C8`, dynamic-return setter `0x553E8`, and saved-dynamic destination setter `0x55454`. Equality supports these local semantics; it does not validate all callees, caller activation, current saved state or gameplay reachability.

## Findings in the selected warp records

All 58 source warp destinations resolve to a map slot inside its physical bank prefix and a target warp index smaller than that target's warpCount under the inspected structures. No selected **source** event has destination mapNum, group or warpId `7F` or `FF`.

Eleven source events in map `5:86` (indices `5,6,7,10,11,13,14,19,27,29,39`) target `0:0:warp0`. That target warp record is at `0x722A84`, with destination group/map/warp bytes `7F/7F/7F`. Consequently these are static inbound lobby destinations with a dynamically encoded return event; `0:0` must not be flagged as an invalid placeholder.

A raw reverse comparison gives 26 exact source-map/source-warp backlinks, one return to the source map at another warp, 20 target events pointing elsewhere, and the 11 dynamically encoded return targets. These categories do not certify correct or incorrect behavior. Two adjacent entrance tiles can share a target that returns to one of them. A different map or warp on the return may be deliberate or reflect preserved map variants. No repair or content deletion follows from absence of an exact reverse.

## Connections and reciprocal expectations

`include/constants/global.h:119–126` defines direction `0=NONE`, `1=SOUTH`, `2=NORTH`, `3=WEST`, `4=EAST`, `5=DIVE`, `6=EMERGE`, with invalid `-1`. `MapConnection` is a 12-byte structure: direction byte at `+0`, signed 32-bit offset at `+4`, destination group/map bytes at `+8/+9` (`include/global.fieldmap.h:177–183`).

For ordinary cardinal camera transitions, source `src/fieldmap.c:631–655` subtracts the connection offset from the crossing-axis coordinate: north/south changes x by `-offset`, east/west changes y by `-offset`. Destination map dimensions determine the other coordinate. `GetIncomingConnection` (`:686–705`) selects a source connection by direction and overlap position; neither this code nor `CameraMove` (`:657–683`) requires a matching reverse connection in the destination. Overlap checks are at `:708–742`. A conservative integer tile overlap is the intersection of source-axis bounds with `[offset, offset + destination_axis_size - 1]`; matching this geometric interval does not establish passable collision or active transition behavior. The reference incoming predicate uses an inclusive upper boundary; preserve exact implementation details if simulating edge coordinates.

Opposite direction plus negated offset and a destination back to the source is useful static consistency evidence. It is not a source-enforced correctness requirement. Seven of the 13 selected source connection records have such an exact reverse; six lack one:

- `3:100` north `+8` to `3:60`.
- `3:100` east `0` to `3:104`.
- `3:101` west `+28` to itself.
- `3:107` west `+28` to `3:101`.
- `3:107` north `+2` to `3:102`.
- `3:111` east `+14` to `3:110`.

The reused connection array shared by `3:101` and `3:107` must remain visible rather than being deduplicated into a single map. Target `3:60` has a null events pointer, and a target connection record at `0x352E5C` has direction zero (`NONE`), offset 80, target `3:61`. Cardinal connection setup/detection dispatches only the corresponding cardinal directions (`src/fieldmap.c:129–170`, `:708–724`, `:761–790`); a zero direction is not automatically a traversable border. Report these literal observations as anomalies/uncertainties, without certifying a broken map.

Dive/emerge use connection direction 5/6 through `SetDiveWarp` (`src/overworld.c:706–749`); if no connection exists, the reference runs a dive-warp map script and checks a separately configured fixed warp. These paths do not appear among the 13 selected source connections.

## Default indexed layouts

`src/overworld.c:490–496` defines active layout lookup as `gMapLayouts[mapLayoutId-1]`, returning null for ID zero. `LoadCurrentMapData` (`:550–557`) copies the header layout ID to the saveblock and replaces `gMapHeader.mapLayout` with that indexed layout. `LoadSaveblockMapHeader` (`:558–562`) instead uses the stored saveblock layout ID. Comparing coordinates against only the raw header layout pointer is insufficient in general.

The native Liquid Crystal layout lookup is at `0x55170`; literal site `0x55194` points to `0xC2FC30`. Exact 40-byte span `[0x55170,0x55198)`:

```text
00 B5 03 48 00 68 41 8E 00 29 03 D1 00 20 06 E0
08 50 00 03 03 48 01 39 89 00 09 18 08 68 02 BC
08 47 00 00 30 FC C2 08
```

SHA-256 `b751dc5ad2802eccfb7356eeae957b606132e5387c2ba0f5f876d35d9dfa7b04`. The supplied FireRed function has identical preceding code and a different table literal `0x34EB8C`. Native `LoadCurrentMapData`-shaped interval `[0x55274,0x552BC)` is unchanged, including the header-ID assignment and the call back to this lookup.

The layout table is sparse, so a zero slot is not an array terminator. There are 18 zero entries among IDs `1..0x379`; the first is layout ID `0x16`, pointer slot `0xC2FC84`, with later selected IDs still valid. Validate the selected `layoutId-1` slot directly. Do not use the group/map physical-pointer-prefix method to infer this table's length.

For all **32 unique maps** in the ten selected owners plus the 58 warp destinations and 13 connection destinations, the raw header layout pointer equals `table[header.layoutId-1]`. There is no default header/indexed-layout mismatch in this scope. The checked map set is:

```text
0:0; 1:99;
3:60,98,99,100,101,102,103,104,106,107,109,110,111;
5:86,87,88,89,90,91,92,93,95,96,97,99,102,103,104,105;
6:23.
```

Selected layout IDs are `3:99=333`, `3:100=334`, `3:101=33E`, `3:102=340`, `3:104=34B`, `3:107=35C`, `3:111=379`, `5:86=332`, `5:102=348`, `6:23=36E` (all IDs hexadecimal). Target `3:60` has layout ID `FC`, pointer `0x32F3B4`, dimensions 30×56, despite its null events pointer.

Runtime scripts may change layout IDs: `SetCurrentMapLayout` updates the stored ID and active pointer (`src/overworld.c:978–982`); `ScrCmd_setmaplayoutindex` invokes it (`src/scrcmd.c:711–716`). Current save overrides, map-script execution and engine hooks remain unverified. The equality finding applies to default header IDs, not every possible runtime state.

## Reference provenance

Interpretation uses pret/pokefirered commit `037335f4c725d7c9aecdac87066f2002b4bd7e14`, with standard TLS verification. Previously retained `src__overworld.c`, `include__global.h`, `include__global.fieldmap.h` and `src__scrcmd.c` remain authoritative local references. The five additional files below are now retained under `research/references/`, using their temporary basenames, with entries appended to `manifest.json`. All 24 reference-manifest file hashes were verified after retention.

| Source path | Temporary local path | SHA-256 |
|---|---|---|
| `src/field_control_avatar.c` | `/tmp/src__field_control_avatar.c` | `305daa295f88ce682b2b1868700d2f76012c659cb0df2905e6177a51ee4e9b8d` |
| `src/fieldmap.c` | `/tmp/src__fieldmap.c` | `bbe15c7af1059a9f796dddaca28bdaaf206b715895029e189fa6ae012272ce68` |
| `include/constants/maps.h` | `/tmp/include__constants__maps.h` | `fd72a95bb4bd8c589630826d745814beaafe7a8518ffa3fb7927bf16d670a7dd` |
| `include/constants/global.h` | `/tmp/include__constants__global.h` | `7ecf4a63c7be65328135a75f8620786e40343bbe7688e7017e6d780526fd6a0c` |
| `include/constants/map_types.h` | `/tmp/include__constants__map_types.h` | `21b9dc465effd752f859c25d22fee121da8f56e245b1f65ad022af0f9a8008fa` |

URL prefix: `https://raw.githubusercontent.com/pret/pokefirered/037335f4c725d7c9aecdac87066f2002b4bd7e14/`.
