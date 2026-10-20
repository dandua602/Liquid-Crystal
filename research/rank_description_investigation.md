# Commanding Rank description: independent byte investigation

Read-only inspection of the locked Liquid Crystal source ROM, SHA-256 `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. All offsets below are ROM file offsets. No ROM, save, application tool, test, or existing research file was changed by this investigation.

## Classification

The Commanding Rank keyword is genuine item-description prose with two item-record references. It is a **text/script boundary anomaly**, not a false keyword match. There is no dedicated `FF` terminator between the description's final period and an independently referenced script entry. The first subsequent `FF` is also the low byte of the following script's object operand.

The strict English decoder correctly rejects the combined span. Accepting `4F` as an English glyph, treating it as a control, or claiming a clean terminated string ending at the period would lose the evidence. Runtime appearance and actual gameplay accessibility remain untested.

## Exact boundary evidence

Readable bytes occupy `[0xAAAF41, 0xAAAF9A)`, 89 bytes:

```text
The Commanding Rank given to you
by Mister G, an ex-commander in the
Elite group Nexus 4.
```

SHA-256 of those 89 bytes: `619998f48d750014d9033a1b9351fc572e18360f355ed63351809bfe9de5c547`.

```text
offset      bytes
0xAAAF40    FF CE DC D9 00 BD E3 E1 E1 D5 E2 D8 DD E2 DB 00
0xAAAF80    E2 00 E8 DC D9 FE BF E0 DD E8 D9 00 DB E6 E3 E9
0xAAAF90    E4 00 C8 D9 EC E9 E7 00 A5 AD 4F FF 00 F4 CE AB
0xAAAFA0    08 51 00 00 0F 00 E8 CC AB 08 09 02 5C 09 45 03
```

- `0xAAAF99 = AD`, the final period.
- `0xAAAF9A = 4F`, the independently referenced script entry. The incoming pointer at `0xC00582` is `9A AF AA 08`.
- `0xAAAF9B = FF`, the first `FF` at or after the description start.
- The seven bytes at `0xAAAF9A` are `4F FF 00 F4 CE AB 08`: the retained FireRed macro/command table identifies this shape as `applymovement 0x00FF, 0x08ABCEF4`.
- The next three bytes at `0xAAAFA1` are `51 00 00`: `waitmovement 0` in that reference format.

`gba_text_codec.parse(rom, 0xAAAF41, limit=89)` returns the exact prose, no issues, `terminated=False`, end `0xAAAF9A`. With limit 91, permissive parsing emits `<BYTE_4F>`, records the unsupported glyph at `0xAAAF9A`, and terminates on the operand byte at `0xAAAF9B`, end `0xAAAF9C`. Strict parsing with limit 91 returns `None`.

The retained character/control definitions use `FF` as EOS, `FC` to introduce extended controls, and do not assign `4F` an English glyph. The description contains no `FC` sequence that could make the trailing `4F` an operand. The reference charmap assigns `4F` to Japanese `ぽ`; that fact does not establish an intended Japanese glyph or the visible Liquid Crystal glyph under its current font mode.

## Two concrete item-record references

An all-byte-alignment search for `41 AF AA 08` finds exactly `0x3DDFAC` and `0x99C030`. These are both at offset `+0x14` in a 44-byte item record with item ID `0x0114` at offset `+0x0E`:

| Table base | Index | Record start | Name bytes decode to | Description pointer field |
|---|---|---|---|---|
| `0x3DB028` | `0x114` | `0x3DDF98` | `RED ORB` | `0x3DDFAC = 0x08AAAF41` |
| `0x9990AC` | `0x114` | `0x99C01C` | `G Rank` | `0x99C030 = 0x08AAAF41` |

Old record, 44 bytes:

```text
CC BF BE 00 C9 CC BC FF 00 00 00 00 00 00 14 01
00 00 00 00 41 AF AA 08 02 00 02 04 39 22 0A 08
00 00 00 00 00 00 00 00 00 00 00 00
```

Relocated record, 44 bytes:

```text
C1 00 CC D5 E2 DF FF FF 00 00 00 00 00 00 14 01
00 00 00 00 41 AF AA 08 02 00 02 04 39 22 0A 08
00 00 00 00 00 00 00 00 00 00 00 00
```

Neighbor records further support the table interpretation. Indices `0x112`, `0x113`, and `0x115` are `LETTER`, `DNA SAMPLE`, `BLUE ORB` in the old table; their names are `SHOVEL`, `DNA SAMPLE`, `GS BALL` in the relocated table. IDs and description-pointer positions retain the same 44-byte structure.

The original FireRed ROM's old `0x114` record has description pointer bytes `2A 8F 3D 08` instead; Liquid Crystal changed that field to the Commanding Rank prose. Its relocated table region is `FF` in FireRed.

## Native consumer evidence

This goes beyond unclassified raw pointer hits. Liquid Crystal contains a Thumb function at `0x9A96C` with bytes:

```text
10 B5 00 04 00 0C 06 4C FF F7 96 FF 00 04 00 0C
2C 21 48 43 14 34 00 19 00 68 10 BC 02 BC 08 47
28 B0 3D 08
```

This complete 36-byte span matches the supplied FireRed ROM byte-for-byte; SHA-256 `b9729f848e5c6b7b262030fea7c81b46660aa8183099f3c3638c1d8f22ba2e4f`.

Its relevant operations are:

```text
0x9A972  ldr  r4, [pc, #24]  ; literal at 0x9A98C = 0x083DB028
0x9A974  bl   0x9A8A4        ; sanitizes item ID
0x9A97C  movs r1, #44
0x9A97E  muls r0, r1
0x9A980  adds r4, #20
0x9A982  adds r0, r0, r4
0x9A984  ldr  r0, [r0]       ; return description pointer
```

Consequently input item ID `0x114` addresses the pointer at `0x3DDFAC` and returns `0x08AAAF41`; this function uses the old record table for descriptions. Its instruction structure matches `ItemId_GetDescription` in the pinned reference source. ID `0x114` is inside the sanitizer's accepted range.

The nearby name-returning function at `0x9A8BC` instead computes `base + 44 * sanitized_id` using the literal `AC 90 99 08` at `0x9A8D8`, i.e. relocated base `0x9990AC`. The same literal in FireRed is `28 B0 3D 08`. Thus the observed accessor pair supports the `G Rank` name and Commanding Rank description belonging to the same item ID, despite the old table's retained `RED ORB` label. Neither whole table should be declared unused.

An even-alignment Thumb BL-shape search finds six call sites targeting the description-returning function: `0x966BE`, `0x9B340`, `0x108842`, `0x10D9C6`, `0x131F28`, `0x13D556`. For each, the inspected 56-byte context `[site-24, site+32)` is identical between the supplied Liquid Crystal and FireRed ROMs. These are static native-call evidence; they do not identify a currently executable menu state or prove that this save can obtain/highlight the item.

The earlier script audit's award sequence independently sets variable `0x8000` to item operand `0x114` at `0xAAAFC2`, variable `0x8001` to `1`, and executes `callstd 0`. It now has a matching item-record identity. The actual award/runtime path remains unverified.

## Reference interpretation and limits

Previously retained references `asm__macros__event.inc`, `data__script_cmd_table.inc`, `include__characters.h`, `charmap.txt`, and `src__text.c` provide the script/control/EOS interpretation. `src__text.c:813` handles EOS separately; an ordinary `4F` falls through to glyph processing under that reference's standard renderer. Exact Liquid Crystal glyph appearance has not been established.

Additional official source files inspected read-only from pret/pokefirered commit `037335f4c725d7c9aecdac87066f2002b4bd7e14` were downloaded to `/tmp`, without changing the project's reference manifest:

| Source path | SHA-256 |
|---|---|
| `include/item.h` | `a2cf9f23cfcd63067550c722f4cacf72491b9a614cf1587f7898b347b6a412a4` |
| `src/item.c` | `117c3d29617bd779db7c32332ab75fe5859f02ee6165a047508558977a88d01a` |
| `src/item_menu.c` | `155bd6b0943e8df179cbc9892e573cee52fd8f67a1d0dd39b962bdbec2e3546a` |

Their URL prefix is `https://raw.githubusercontent.com/pret/pokefirered/037335f4c725d7c9aecdac87066f2002b4bd7e14/`. `include/item.h` defines the name, item ID, description-pointer and other item fields; `src/item.c:636` returns `gItems[SanitizeItemId(itemId)].description`. `src/item_menu.c:748` describes a bag UI consumer that obtains the item description and passes it to a text window. These source files provide format/semantic interpretation, not Liquid Crystal address provenance; the reported addresses come from the supplied ROM bytes.

The supported conclusion is a statically referenced item-description boundary anomaly. A standard unbounded EOS reader starting at `0xAAAF41` would consume `4F` before encountering `FF`; a physical screen artifact, crash, active menu path, intended repair, or unintended missing terminator cannot be certified by this static investigation. No patch should be made during this research step.

## Suggested regression checks

1. Preserve source-hash verification and the exact 89-byte description extent; record `terminated=False` for that bounded extent.
2. Assert `rom[0xAAAF99:0xAAAFA1] == AD 4F FF 00 F4 CE AB 08` and the incoming script pointer at `0xC00582`.
3. Assert strict parsing rejects the combined span and permissive parsing reports `4F` at the script entry. Do not add `4F` to accepted English glyphs merely to admit this candidate.
4. Recompute both records as `table_base + 44 * 0x114`, check their item IDs and `+0x14` description pointers, and distinguish the old and relocated names.
5. Retain getter bytes and derive its table/index arithmetic from those bytes; do not infer table activity solely from raw pointers or FireRed addresses.
6. Keep it in a separate anomaly inventory, retaining raw bytes and script ownership evidence, rather than promoting it to a clean terminated text record.
