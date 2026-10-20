Liquid Crystal P002 — Office Block service-room prototype (includes P001)

Playable additions: warehouse Iron Tail/Rock Smash puzzle, approved Mister R
battle and Office service-room access after victory. Its southern door returns
to the warehouse. The main Office remains closed; no new reward or fight is added.
Read WALKTHROUGH.md for directions, screenshots, retries, saving and the endpoint.

Choose ONE installation path. Use a compatible BPS patcher or included Python3:

A. Exact original supplied Liquid Crystal ROM:
SHA256 c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf
python3 bps_patch.py "POKEMON Liquid Crystal.gba" P002.bps "Liquid Crystal P002.gba"

B. Exact P001 ROM:
SHA256 b2c3d4e3fb6f196de90bd9d88cbdcd850e429dce919034c48326d924ae413e92
python3 bps_patch.py "Liquid Crystal P001.gba" P001-to-P002.bps "Liquid Crystal P002.gba"

Expected P002 SHA256:
9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70
Do not apply to vanilla FireRed. P002.bps already includes P001.
The applier refuses to overwrite an existing output. Preserve your original ROM
and save backups; use a working copy of your personal save with the new ROM.

ROLLBACK: first leave the service room, return to the warehouse and SAVE there.
A save left in P002-only map6:32 will not load in an original/P001-only ROM.
P002-to-P001.bps restores exact P001; P002-reverse.bps restores exact original.
For example:
python3 bps_patch.py "Liquid Crystal P002.gba" P002-to-P001.bps "Restored P001.gba"
An actual saved return to the warehouse was loaded successfully in fresh P001.

150 project tests and 166 runtime expectations pass
across 7 cases, including actual six-opponent victory, P001 save upgrade,
new-map save/fresh reload, normal return, native whiteout and safe downgrade.
Earlier P001 archaeology/balance artifacts are retained, not claimed freshly
replayed. P002 also fixes a cleared-rock respawn on movement using existing
room-template coordinates; no new save field or flag is allocated.

This ROM preserves the supplied image's cartridge bank driver/embedded save;
it is tested with the project's mGBA0.10.5 adapter. Stock-emulator conversion,
hardware compatibility, full-game progression and human balance are unverified.
This ZIP contains patches, applier, manifests, guide and screenshots. No ROM/save.
