# Linked Orange progression and cartridge persistence

The laboratory introduction and the police-rescue → Mandarin → Route 59 → Mister R chain execute in the supplied image. A full unattended replay passes 21 expectations, including saving and loading the earned key, room and introduction state in a fresh emulator process. Original ROMs and save remain unchanged.

These are controlled late-game fixtures. The laboratory and police floor each receive one forced entry, and the first party member has artificial level 100, HP/stats 999, Aerial Ace and Surf. Recorded party PP refills support long battles. Battles use ordinary buttons; no enemy HP, battle outcome, quest flag, key or rank item is injected. This establishes the linked late-Orange segment from its test anchor, rather than an ordinary Johto/Kanto-to-Orange playthrough or game balance.

| Stage | Observed result |
|---|---|
| Laboratory `5:102`, natural entry warp | Trainer 837 battle and Axel dialogue finish; `0x5315=1`, flag `0x513=1`, G Rank item `0x114` present |
| Police floor `6:27`, start below director event | Coordinate script `0x9046EE` runs trainer 912 battle and rescue; flag `0x5BA=1`, Old Key `0x116` awarded |
| Rescue landing | Game script sends player to `6:24` at `(13,3)` |
| Police exit and Mandarin | Normal walking reaches Mandarin `3:109`, then gatehouse `6:28` |
| Gatehouse north exit | Normal warp reaches Route 59 `3:110` at `(54,67)` |
| Warehouse door | Coordinate event and actual north-facing door interaction use the earned Old Key; flag `0x5C1` changes 0→1 |
| Warehouse entry | Ordinary door activation reaches `6:31`; original Mister R introduction sets `0x5331=1`, flag `0x5C5=1`, removes him |
| In-game Save and fresh process | Continue time changes to 9:14; room `6:31`, `0x5331`, flags `0x5BA/0x5C1/0x5C5` and Old Key reload correctly |

The door uses collision 1 with door behavior `0x69`; it activates from the adjacent tile. Collision-zero flood fill alone would incorrectly reject this entry. Wild battles can run while the script context reports idle, so the navigator also waits for the sampled field callback `0x080565B5` at `gMain.callback2` before resuming movement. It records all walking requests and observed coordinates.

The earlier apparent laboratory stall was an incomplete battle/dialogue replay. The earlier save failure required understanding the cartridge conversion below. Neither is established as a game progression defect.

## Supplied image's save hardware

This particular ROM contains a cartridge save conversion. Its ASCII `FLASH1M_V103` signature does not describe the complete protocol. This is evidence about the uploaded bytes, not all Liquid Crystal distributions.

- Flash command stores around `0x1DE828` were replaced with NOPs; literal `0x1DE840` points to Thumb `0x08C72101`.
- The handler copies bank-select code into `0x0203FC00`, then writes 0/1 to cartridge address `0x09000000` (literal `0xC7213C`). SRAM at `0x0E000000` therefore has two 64 KiB banks.
- The boot/save hook at `0xD9748` points to `0x08C72141`. It restores an embedded cartridge save into SRAM at boot and programs that storage again after saving.
- The embedded 128 KiB at file offsets `0xC80000–0xCA0000` exactly equals the uploaded `.sav` payload, SHA-256 `ce2bace08fb36ed0e41b900f7af5e8033f1f76b4095c7f46f6754aeff65f5fb7`.

Byte signatures and the payload hash are reproducible with `python3 tools/save_hardware_audit.py`. The source `.sav` additionally contains its preserved 16-byte FlashGBX footer.

The headless frontend now models both banked SRAM and the observed AMD fallback NOR command path. Its private in-memory cartridge save window is initialized from the disposable `.sav`; game-generated NOR writes persist back to that copy. Source and copied `.gba` files are never written. The successful save performs two NOR erases and 65,536 halfword programs before restarting a new process. CPU savestates include bank, SRAM and private NOR state; persistence acceptance uses a separate process, not a savestate restore.

This adapter uses immediate functional writes. Chip-ID variants, electrical timing, power-loss recovery and real flashcart behavior are unverified. LC checksum lengths and every save section's semantics remain unaudited. The prior default-mGBA corruption/previous-save warning is superseded as a diagnosis of the supplied save: correct cartridge emulation loads Continue cleanly. No source-save repair was needed.

## Artifacts and next boundary

`extracted/runtime/linked/linked.json` retains 21 passing expectations, 158 walking requests, mapper counters, message pointers and the full command transcript. Screenshots include `laboratory_complete.png`, `police_after_rescue.png`, `warehouse_unlocked.png`, `linked_mister_r_end.png` and `reloaded_mister_r_room.png`. The generated `saves/test/linked-orange-fixture.sav` is ignored and explicitly labelled as an artificial test fixture; its JSON metadata is retained.

The broader script index covers 4,037 candidate owner roots and all 213 standard command widths. It retains 181 thematic/focus roots and 389 messages, with unsupported/native/context-dependent frontiers visible. The regional structural preflight expands 128 candidate slots and 599 links; neither dataset certifies every candidate map as Orange or normally reachable.

Mister R's promised puzzle/battle still has no recovered supported completion path. The laboratory is now resolved as working in this fixture, and the warehouse is reachable from the earned police key. Remaining boundary work concerns ordinary Orange entry and other surviving native/travel paths, followed by a concrete puzzle/battle specification and safe allocation. The four preflight ledgers exist, but no asset space, new flag or variable is certified or allocated. No continuation patch or new story has been created.
