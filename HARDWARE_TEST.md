# P002 cartridge test

P002 adds the warehouse rock puzzle, Mister R battle and Office service room.
The [walkthrough](WALKTHROUGH.md) covers the story steps. P003 is still a design
proposal. **Hardware saving failed in the user's reported test:** corruption/previous-save
warning on boot, followed by a saving hang. Screenshot confirms FlashGBX5.0.1,
GBxCart RWv1.4a/b/c family, AGB-E20-30/S29GL256N10TFI01 (or compatible),
32 MiB and Unknown FLASH save chip0x8209. Root cause is still unknown. Do not treat the emulator checks as hardware acceptance.

The [v3 offline tool](patches/P002/P002-easy-cartridge-test-v3.zip) can download
the exact matching raw `.sav`: select the already-generated warehouse test ROM,
click Create, then **Download matching P002-warehouse-test.sav**. That is the same
128 KiB payload already embedded in the ROM, not a confirmed fix. Confirm the
cart/save profile before a separate save restore. Preserve a full ROM readback
from the failed attempt before reflashing so the actual bytes can be checked.

## Download a working test ROM on your computer

Workspace ZIP links cannot be downloaded in this chat. Instead download the
[small offline patcher ZIP from GitHub](patches/P002/P002-easy-cartridge-test-v3.zip)
using **Download raw file**, then:

1. Extract it and open **Make-Test-ROM.html** in Chrome, Edge or Firefox.
2. Select your original **POKEMON Liquid Crystal.gba**, exact P001 or exact P002.
   For a compatible newer cart dump, also choose the original five-badge `.sav`
   backup when requested. The page verifies the unchanged game/driver bytes and
   original save before normalizing a copy in memory.
3. Click **Create and download test ROM**. Your browser saves
   **P002-warehouse-test.gba**, including the pre-puzzle test save. A persistent
   **Download P002-warehouse-test.gba** link remains available if automatic
   downloading does not start.
4. Keep the output for diagnosis. Before another write on the failing cart,
   collect the full readback described below. Writing a separate save is not
   established as a fix.

No Python or separate patcher installation is required. Your source ROM stays
on your computer and the page makes no network requests. The output is byte for
byte identical to the previously tested warehouse image described below.
If rejected, open **File details for troubleshooting** and share the file size
and SHA256 shown there. Renaming a file does not change the check. The page
will reject unsupported game/driver changes rather than force an unverified ROM.

The ZIP also contains a direct BPS patch for people who prefer a BPS patcher.
Apply it directly to the original upload, not an already patched ROM.

## Read back the failed cart before another write

In FlashGBX5.0.1 choose **Backup ROM**, retain the detected **32 MiB** size, and
save the complete dump. Upload that dump (ZIP if needed). Do not overwrite the
original backup or reflash between the failure and this readback. We need to
compare the full cartridge image, not just the raw `.sav`. The user has confirmed
that the original unmodified ROM saves successfully on this exact cart; that
baseline does not need to be repeated.

The official FlashGBX5.0.1 [profile](https://github.com/lesserkuma/FlashGBX/blob/5.0.1/FlashGBX/config/fc_AGB_S29GL256.txt)
uses32 MiB capacity and128 KiB erase sectors. The old software adapter used64 KiB
sectors. A focused comparison now tests both geometries: both return to field
and retain28 valid save sections. Thus erase size alone did not reproduce the
reported hang; chip IDs/timing/bank circuitry remain outside the model. The ROM
profile does not identify the unknown save chip0x8209 or prove a save restore
method. No new ROM/driver patch has been made on that speculation.

`tools/inspect_cartridge_readback.py` accepts16 or32 MiB dumps read-only, explicitly
compares the first16 MiB to the expected image, audits the embedded save using
native LC lengths, and records the upper half separately. It never truncates or
rewrites the user's dump. See [geometry evidence](extracted/runtime/cartridge/geometry/summary.json).

## Choose your image

The private cloud package `builds/P002-cartridge-test.zip` contains these 16 MiB
ROMs, separate 128 KiB raw saves, checksums, screenshots and this guide:

| ROM | Starting point | Save/party |
|---|---|---|
| P002-personal-5badge.gba | Your uploaded five-badge location | Your original progress; exact standard P002 |
| P002-warehouse-test.gba | Between the warehouse sign and rock | New artificial test save, puzzle pending, Mister R unbeaten |
| P002-office-test.gba | Inside the Office service room | Existing artificial post-victory test save |

**Use P002-warehouse-test.gba to test the new content immediately.** Its test
party is level 100 Swampert, Arcanine, Machamp, Ampharos, Lapras and Alakazam, with
native-generated stats/PP and Lum Berries. Swampert has Surf and Iron Tail.
The late-game map anchors are artificial; the retained controlled replay earned
the Old Key and warehouse unlock. This is a test shortcut, not your personal
progress. The Office-only save uses the earlier boosted Mewtwo fixture.

Each image already contains its selected save at `0xC80000–0xCA0000`, matching the
conversion found in your uploaded cartridge ROM. The FlashGBX 16-byte footer is
metadata and is **not** copied into the ROM. The sidecar raw saves are optional
copies for tools that explicitly support this cart's save method. A separate
save restore is not required to select the included starting point on a cart
that supports the uploaded conversion.

## Flash and verify

The user confirmed **FlashGBX** as the flashing software. Use the same compatible
cartridge and FlashGBX cart-type/profile that worked with the original dump. The
screenshot identifies the GBxCart RWv1.4a/b/c reader family and
AGB-E20-30/S29GL256N10TFI01 (or compatible) profile; save ID0x8209 is unrecognized. This package
preserves that dump's bank selector,
NOR save driver, game size and header; it is not an EverDrive/EZ-Flash conversion.

1. Keep your existing backup. If you have played since making it, make a fresh
   full-ROM/save backup too: this cart stores progress inside the ROM area.
2. Extract the ZIP and choose **one** ROM from the table. Do not flash the ZIP,
   a `.bps` patch or the raw `.sav` as a ROM.
3. In FlashGBX, connect your reader and insert the GBA cart. Keep the known
   working cart-type/profile. Use **Write ROM** and select
   **P002-warehouse-test.gba** (or your other chosen image). Write the complete
   16 MiB image and enable verification if your version offers it. Otherwise
   use a full-ROM readback for the comparison below. Wait for completion.
   The test progress is already inside the ROM: do not separately restore a
   `.sav` for this first test. A later save restore could replace that starting
   point. Do not select a different chip profile by guesswork.
4. For a manual check, dump a full 16 MiB ROM immediately after flashing and run:

   ```sh
   python3 verify_cartridge.py P002-warehouse-test.gba readback.gba
   ```

   The result must say `passed: true` and `exact_match: true`. You can also compare
   the image's SHA256 with `MANIFEST.json` or `SHA256SUMS.txt`.
5. Insert the cart in the console, power on and select **Continue**. The warehouse
   test should put you between the damaged sign on the left and rock on the right.
   See `screenshots/warehouse-start.png`. If it boots elsewhere, record the
   flashed filename and readback result before making further save changes.

Do not assume these images work on a different save-chip/bank arrangement. Real
hardware timing, flash-chip IDs and all programmer protocols remain untested.

## Quick console test

1. With the warehouse image, face **right**, press **A**, accept Iron Tail, then
   decline the battle. The rock should disappear. Walk a few tiles and return;
   it should stay gone.
2. Use **START → SAVE**, wait for completion and return to the field. Power off,
   wait a few seconds, then power on and Continue. The rock should still be gone.
3. Face **left** toward the sign, press **A**, advance the clue and accept the
   Mister R rematch. Defeat all six opponents. Your test team is provided for
   convenience; use any tactics or healing items available. A loss should allow
   another attempt instead of granting completion.
4. Interact with the damaged sign again and accept the Office passage. In the
   service room, walk two tiles north and speak to the attendant. The current
   endpoint says the main office is closed.
5. Save inside the service room. Power off/on and Continue. You should remain
   in that room. Walk south through its normal door to return to the warehouse.
6. Save outside the new room. Power off/on once more and confirm repeat Office
   access. Leave the new room and save before downgrading to an older ROM.

If saving hangs, returns to old progress or gives an error, report which image,
cart, flasher/profile and console you used, and which step failed. A photo of
the screen or exact message is useful. Do not reflash between save/reload steps:
reflashing restores the image's bundled starting save.

After playing, a ROM dump may legitimately differ in the embedded save window.
To check that game code/driver bytes still match, use:

```sh
python3 verify_cartridge.py P002-warehouse-test.gba after-playing.gba --after-play
```

This checks bytes outside the save window; it does not certify valid save data
or prove the console test succeeded.

## Rebuild with your own save

GitHub contains the public [patch/helper kit](patches/P002/P002-cartridge-tools.zip),
without ROMs or saves. Extract it beside your original uploaded ROM and save,
then run with Python 3:

```sh
python3 bps_patch.py "POKEMON Liquid Crystal.gba" P002.bps P002-base.gba
python3 cartridge_image.py P002-base.gba "POKEMON Liquid Crystal DD 5 badge.sav" P002-my-cart.gba
```

The input ROM must be your exact original upload, not vanilla FireRed or a
later cartridge dump whose embedded save has changed. The second command embeds
the supplied 128 KiB payload and accepts its original 16-byte FlashGBX trailer.
It refuses to overwrite an existing output. Original inputs remain untouched.

The private ROM/save ZIP stays outside GitHub. The public helper kit, walkthrough
and hardware report contain no ROM or save files. Keep private artifacts when
you download them; a repository clone cannot restore them without your inputs.

## Current hardware result and software evidence

The user reported a corruption/previous-save warning and stuck Saving. A fresh
readback is needed to distinguish a flash/readback/driver problem from save-data
behavior. Reader/profile details are recorded above; the user confirmed that
the original unmodified ROM saves on this same cart. Do not repeat a write as a substitute for
collecting that evidence. The original and test payloads both pass all28 section
checksums using the native LC layout at3FEC94; this does not prove what hardware
read. See [failure audit](extracted/runtime/cartridge/hardware_failure_audit.json).

Software checks booted all three selected images with blank emulated SRAM,
using the ROM's actual embedded save rather than injecting a sidecar. The
warehouse image also passed an in-game Save and a fresh-process boot from the
updated modeled NOR contents. Existing P002 checks cover the full battle and
Office path. These results support a hardware test; they are not physical
cartridge validation. See `VALIDATION.json` in the private ZIP and
[software evidence](extracted/runtime/cartridge/summary.json).
