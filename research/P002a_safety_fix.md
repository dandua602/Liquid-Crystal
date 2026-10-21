# P002a: seal the inherited Colosseum staircase

The user beat Mister R on hardware, left the warehouse, sat in a stadium and
reported a girl opponent, question-mark Pokémon, missing PP and garbled text.
They are uncertain which exit they used and where their last save is. They also
report that the cart is now working sufficiently to play through Mister R; the
exact resolution of the earlier hardware-saving issue was not supplied.

## Findings

Warehouse6:31 has an old east-facing stair at20,7 whose unchanged warp targets
map0:0. That map has a battle-room layout, label NOT USED, a female-looking NPC
and two seating coordinate events. Both seat roots (`1BB8C3`, `1BB8CF`) invoke
special32, matching the native EnterColosseumPlayerSpot entry. This is inherited
link-room code, not the newly authored Mister R fight. Its header, warps and
seat scripts are byte-identical between the original upload and P002.

Controlled native walking reaches0:0 through that stair in both ROMs. Seat input
then enters a stalled/black-screen link callback, with no initialized opposing
BattleMon. **The exact physical garbled battle was not reproduced.** This is a
strong matching unsafe route, not proof of the user's exact sequence. The other
old top warp leads to Goldenrod Dept.2:40, rather than the new Office route.

Earlier exit QA verified the unchanged stair destination but did not validate
the seating interaction. That left this unsafe route open in the prototype.
Static evidence and controlled transcripts are in
[stadium summary](../extracted/runtime/stadium/summary.json).

## Minimal fix and scope

P002a changes warehouse block word at`C30C2C` from`325D` to`3E5D`: collision0→3
at20,7, with graphic, elevation, map dimensions and every other byte retained.
This seals the legacy stair for normal walking without changing shared link-room
functions. It adds no scripts, text allocation, flags, variables, items, trainers,
map headers, save format or story. It is a safety fix for the reported bug;
P003's new story proposal remains unapproved and unimplemented.

Standard output hash:
`9b0304e19a33df9a229eaad9cee975b9c01bcac8ba217142e8a36e6b240c1d31`.
Exact input/word and write ownership are checked by the builder. Forward/reverse
BPS roundtrip to the unchanged exact P002. Original inputs/P001/P002 stay intact.
The map block is a known indexed warehouse array; no free-space allocation is
needed. The builder's only changed word lies away from the actual cartridge
driver C72100…C72EA8 and embedded save C80000…CA0000.

The stair is blocked before and after victory, including the north and east
approaches tested. Puzzle solving/cleared-rock behavior, completed tag/trainer
bit Save/fresh reload, Office sign entry/return and the south Route59 exit pass.
Twenty-six hotfix runtime expectations pass. Original/P002 route probes add
three expectations each. Forced room/state anchors are explicit; this is not a
continuous normal-playthrough or a new hardware test.

## Keep the player's current progress

[Offline hotfix ZIP](../patches/P002a/P002a-safety-fix.zip) takes a current P002
ROM/cart dump and a **fresh current save backup**. It validates known game/driver
hashes and both native LC save slots, seals the stair, and embeds that supplied
save in a new output. It preserves16/32 MiB ROM size and the upper bank verbatim.
The matching exported raw save is unchanged. No source file is overwritten or
uploaded. Nine real-browser checks cover exact output bytes,32 MiB preservation,
winning-save preservation, invalid save/driver rejection and stadium-save hold.
The managed browser blocks file URLs, so the same shipped HTML was served by an
intercepted secure route; local file use remains the user's workflow.

If the newest save is in0:0, the tool stops and requests a copy for recovery;
sealing an entrance cannot evacuate an existing saved game. If a battle was not
saved, loading the earlier good save is appropriate. Do not replace earned
Mister R progress with the pre-puzzle test `.sav`; back up current data first.
Unsaved wins cannot be recovered from a previous save. Recovery requires the
actual user save, which has not been supplied yet.

The playable continuation remains **damaged sign → Office service room**, then
the normal south door back to the warehouse. It ends at the attendant. Neither
old staircase is newly completed story content.
