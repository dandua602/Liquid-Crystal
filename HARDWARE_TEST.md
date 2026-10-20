# P002 cartridge test

P002 adds the warehouse rock puzzle, Mister R battle and Office service room.
The [walkthrough](WALKTHROUGH.md) covers the story steps. P003 is still a design
proposal. **No physical-console results have been reported yet.**

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

Use the same compatible cartridge family and flashing profile that worked with
your original dump. The precise cart/flasher model is still needed to give
button-by-button instructions. This package preserves that dump's bank selector,
NOR save driver, game size and header; it is not an EverDrive/EZ-Flash conversion.

1. Keep your existing backup. If you have played since making it, make a fresh
   full-ROM/save backup too: this cart stores progress inside the ROM area.
2. Extract the ZIP and choose **one** ROM from the table. Do not flash the ZIP,
   a `.bps` patch or the raw `.sav` as a ROM.
3. Flash the complete 16 MiB `.gba` using your flasher's existing correct profile
   for that cart. Use its verification/readback option before putting the cart
   in the console. Do not select a different chip profile by guesswork.
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

## What has passed here

Software checks booted all three selected images with blank emulated SRAM,
using the ROM's actual embedded save rather than injecting a sidecar. The
warehouse image also passed an in-game Save and a fresh-process boot from the
updated modeled NOR contents. Existing P002 checks cover the full battle and
Office path. These results support a hardware test; they are not physical
cartridge validation. See `VALIDATION.json` in the private ZIP and
[software evidence](extracted/runtime/cartridge/summary.json).
