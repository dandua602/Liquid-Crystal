# P001: warehouse puzzle and Mister R battle

**Ready for design review. No ROM implementation has been made.** The user
approved preparing a new design for review. The kickoff requires “No implementation
until this is reviewed.” Approval covers building/testing this bounded prototype;
player-release and hardware claims still require acceptance checks.

## Player experience and provenance

The existing introduction and damaged clue remain. A cracked boulder beside the
sign can be broken with Iron Tail. Rock Smash is an explicit fallback for teams
without the consumable-TM move. Mister R appears and offers the promised battle.
Declining or losing leaves a retry through the sign. Winning completes this room
once, with normal trainer prize money and usable existing exits.

NEWLY_AUTHORED: boulder placement/interaction, Rock Smash fallback, team, added
text and recovery logic. CONFIRMED_IN_ROM: room, character, original introduction,
promise of a puzzle/battle, damaged hint and exits. STRONGLY_INFERRED: the hint's
Iron Tail/red-rock reading. No missing team/mechanic was recovered from original
project documentation; see intended_story_reconstruction.md.

This slice adds no onward island/destination, badge, rank, item reward, Nexus
repair or G Rank text fix. It completes the missing room event.

## Exact puzzle and scene

1. Preserve introduction 0xAE8D7A and its original tag-2 condition.
2. Add rock object local ID **3**, graphics **96**, at **(15,9)** beside the sign
   at (13,9). LC already uses this rock asset. Visibility flag 0 and map-state
   initialization avoid allocating a new persistent rock flag.
3. Check native move **231**, then **249**. A non-egg party member knowing either
   qualifies; native fainted-member behavior is retained. Ask before breaking.
   Absence/decline changes no state, items or PP; field use consumes no PP.
4. On confirmation, record solved/retry state and remove the rock. Show existing
   object 1 at **(20,10)** during a locked challenge scene. If the player occupies
   that cell, use **(12,11)**. Both placements preserve exit/sign access. The rock
   lies outside every original introduction movement position.
5. Offer the battle. Declining hides Mister R and directs the player to the sign
   for retry. The sign retains the damaged clue and offers retries without another
   move check. Object 1 receives the same guarded challenge handler in its copied
   record, replacing its original ROM-start interaction field.
6. On battle return, call verified native **B4/GetBattleOutcome** and commit only
   for **1 (won)**. Other outcomes never complete the room. Whiteout/interruption
   leaves solved/retry for reentry. Hide the scene actor before releasing control.
   Completed interactions grant no repeat battle or additional reward.

## Newly authored battle

| Pokémon | Level | Moves |
|---|---:|---|
| Crobat | 94 | Aerial Ace, Sludge Bomb, Confuse Ray, Bite |
| Houndoom | 94 | Flamethrower, Crunch, Sunny Day, Solar Beam |
| Umbreon | 95 | Toxic, Confuse Ray, Moonlight, Faint Attack |
| Scizor | 95 | Swords Dance, Metal Claw, Slash, Quick Attack |
| Gengar | 95 | Thunderbolt, Psychic, Giga Drain, Hypnosis |
| Tyranitar | 96 | Rock Slide, Earthquake, Crunch, Iron Tail |

Levels follow existing late-Orange encounters around 88–93; balance needs testing.
Trainer **929**, name **Mister R**, ordinary single battle mode 0, object ID 1.
Class 56 and portrait 25 reuse existing Mister G assets; this portrait is a new
reuse choice. IV parameter 200, AI flags 7 (bad-move/viability/faint checks), two
Full Restores, no held items. Party flags 1: six native 16-byte custom-move records.

Clear only this trainer's bit before each attempt. Its callback can set a defeated
bit for non-loss outcomes, so exact outcome 1 is mandatory. Non-win return clears
a stale bit; a bare bit never grants completion. Normal trainer money is the only
payout. No generic Elite team is adopted as the missing intended team.

## State and old-save recovery

Reuse room variable **0x5331** and visibility flag **0x5C5**. No unrelated story
flag/variable is allocated. Trainer 929 uses native **0x0203D074, mask 2**, inverted.

| Loaded state | Behavior |
|---|---|
| 0 | Ensure original actor visible at (12,11), repairing a mismatched visibility flag if needed; original intro runs once |
| 1 | Intro consumed; rock available, Mister R hidden |
| 0x3302 | Solved; retry via sign without another move requirement |
| 0x3303 and defeated bit | Complete; rock/actor hidden, no repeat battle/reward |
| 0x3303 with clear bit | Recover to solved/retry, granting no victory |
| Legacy 2/3 or any other value | Recover to 1 without replaying intro or granting completion |

Tags avoid mistaking old unowned 2/3 for this patch's state and remain below 0x4000
for literal map-table operands. Both round-trip in native RAM. **0x3303 plus its
trainer bit survives actual Save and fresh-process reload** on disposable copies.
0x3302 has no separate fresh-process save test. These are storage fixtures, not
earned puzzle/battle completion. Arbitrary external/cheated saves mimicking valid
tags/bits cannot be distinguished; standard source semantics 0/1 are preserved.

## Hooks and visibility timing

Header event pointer **0xC30A24 → 0x08B9F380**; map-script pointer
**0xC30A28 → 0x08B9F418**. Copy objects/BGs, add the rock, change only object 1's
script field and sign BG 1's script field. Preserve other events, warp array,
map blocks/tilesets, both layout pointers and original intro/condition bytes.

Retain tag 2. Add tag **4** initialization with condition **1==1** (zero terminates
the condition table), after object spawning in the reference load flow. Tag **7**
reuses cleanup on field return. These immediate routines have no waits, prompts
or battles: normalize state and remove actors/rock as appropriate. State 0 restores
the original actor for the existing frame intro. Actual patched load timing,
saved-room restoration and whiteout behavior remain acceptance tests.

## Bounded allocation and build contract

The **0xB9EF00–0xB9F700** envelope has 2,048 original FF bytes. The bounded static
certificate in space_ownership.md covers raw ROM aliases/alignments, 256-byte
guards, inspected adjacent native table bounds and the nearby audio false pointer.
Unknown unindexed/computed owners and hardware remain outside this certificate;
approval accepts this stated prototype scope. All addresses remain proposed until
review; no source bytes have changed.

| Block | Address | Capacity / reviewed use |
|---|---|---:|
| Scripts | 0xB9EF00 | 640 |
| Added text | 0xB9F180 | 512 / 402 |
| Room tables | 0xB9F380 | 256 / 178 |
| Party | 0xB9F480 | 96 / 96 |
| Reserve | 0xB9F4E0 | 544, unused unless explicitly budgeted |
| Trainer 929 row | 0xAC8EAC | 40 original zero bytes |

Table starts: header B9F380, objects B9F394, BGs B9F3DC, map scripts B9F418,
tag-4 conditions B9F428. Script/text labels resolve within approved blocks at
assembly; overflow must fail. Machine-readable detail: research/design/p001.json;
checked capacities/geometry: extracted/maps/design_review.json.

The builder must enforce exact input hash/expected bytes, nonoverlap and a changed-
range allowlist; write a new ROM under builds/dev; verify headers and deterministic
output; emit a reversible BPS patch and source/output hashes. No expansion, engine
hook, source-file or cartridge-driver edit is permitted.

## Acceptance before calling the prototype playable

- Original intro once; old 0/1, legacy 2/3, tagged/unknown values and inconsistent
  tag/bit pairs.
- Missing moves/declines; both move choices; eggs/fainted/PP behavior; repeated
  solve/challenge/completion interactions.
- Actual win/loss/escape/interruption, whiteout return and no repeat payout.
- Save/fresh-process reload, including saves inside the room; visibility before
  fade and after menus/battle; no actor spawning onto the player.
- Both existing reachable exits, original warp bytes, linked Orange regressions
  and bounded Johto/Kanto checks.
- Deterministic builds, BPS forward/reverse application, headers, changed-range
  allowlist and unchanged original/source hashes.

Hardware-ready release additionally requires real cartridge compatibility checks.
Later Orange continuation remains separate. The next authorization is review of
this concrete design, as required by the kickoff.
