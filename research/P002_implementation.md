# Approved P002: Office Block service room

The user approved the concrete P002 design with **“approve, keep going.”**
[p002_approval.json](design/p002_approval.json) records that authorization and the
reviewed design hashes. Frozen proposal/spec/preview files remain unchanged as
historical review evidence. Current player instructions are in
[WALKTHROUGH.md](../WALKTHROUGH.md); the old P001 guide is archived separately.

## Delivered behavior

After the existing warehouse puzzle and an actual Mister R victory, the damaged
sign displays its original clue and offers entry into the new **Office Block
service room**, map6:32. Declining stays in the warehouse. The new room has the
approved attendant dialogue and a normal southern exit back to the warehouse's
existing warp0. Entry remains repeatable. Saving inside the new map, fresh-process
reloading and returning all work. No new battle/reward/rank, main-office floors,
Route60 or city-door unlock is added.

This is **NEWLY_AUTHORED** content. The original police director's clue supports
an outside-city secret Office entrance, but does not establish this exact room,
dialogue, art choice or route. Existing city blockers/flags and door/warp remain
byte-identical. Source ROMs/save, P001 ROM and the FlashGBX footer remain unchanged.

Final ROM SHA256:

`9224cec2f142c5bb514fb24e6883ae4cc11df1e452778937fa3a21fe78513a70`

The [manifest](../extracted/builds/P002-manifest.json) records all seven delta
writes relative to exact P001. Its source chain plus P001's manifest describes
the cumulative change from the original input. Four BPS files cover original→P002,
P002→original, P001→P002 and P002→P001. Every direction restores exact bytes.

| P002 allocation | Used / capacity |
| --- | ---: |
| Scripts B9F4E0–B9F580 | 151 / 160 B |
| Text B9F580–B9F600 | 109 / 128 B |
| Tables B9F600–B9F700 | 212 / 256 B |

The group6 bank pointer at3526C0 points to a copy of all32 original words plus
the new header entry. Legacy problematic slots4/6 are preserved, not repaired or
normalized. The new header shares the approved original interior's layout,
tilesets and indexed layout ID without altering donor map5:123. The warehouse
sign pointer atB9F3F0 dispatches to the completed-entry handler. Native live
header checks confirm actual engine lookup of map6:32.

## Rock persistence fix found during visual review

The first P002 build passed immediate object-removal checks, but screenshots
showed the cleared rock again after walking toward the sign. A focused probe
confirmed an active local3 object and blocked movement: this was a real respawn,
not merely a stale image. The existing flagless template was being spawned again
by native movement. This issue also existed in P001's original removal strategy.

The fix stays inside the reviewed160-byte script capacity and uses no new flag,
variable, engine code or save-format field. Two same-size call hooks atB9EF00
andB9F003 route through a56-byte helper. It preserves the original normalizer and
the original solved-state write; for state0/1 it restores the rock template to
(15,9), and for solved/completed states it moves that template to(63,63), outside
the unchanged32×19 room, before removal. Original script entry addresses remain
unchanged. Newly added walking/reentry checks and inspected screenshots confirm
the rock stays absent after movement, map returns and save reloads.

This is a necessary implementation correction to the approved persistence
behavior. The frozen design sizing preview remains95 bytes because it predates
that discovered defect; the actual151-byte use is recorded in the build manifest.
First-build runtime results are retained under `extracted/runtime/p002/first_build/`
and are superseded by the final hash-bound cases.

## Newly executed runtime acceptance

The final [validation report](../extracted/builds/P002-validation.json) records
exact case hashes, test totals and limitations. Seven final cases exercise:

- **Access:** legacy/pending/inconsistent-state denial, bit/tag requirements,
  decline, native header/landing, attendant, normal return and repeated entry.
- **Journey:** upgrade of an actual saved P001 research fixture, interruption
  before victory, real six-opponent victory, actual Save and fresh-process load
  both in the warehouse and inside the new room, then repeat entry/return.
- **Matrix:** original introduction and old/tagged state/visibility combinations.
- **Puzzle:** missing moves, declines, Iron Tail, Rock Smash, unchanged PP/party,
  sign retry and new post-movement/reentry rock-persistence checks.
- **Loss:** actual enemy knockout/whiteout and retained retry without completion.
- **Exits:** both existing reachable warehouse exits retain their destinations.
- **Rollback:** leave the earned Office save, save back in the warehouse, replace
  the disposable ROM with exact P001 and load it in a fresh process. Completed
  state/native bit and original P001 sign behavior remain functional.

All runtime files verify originals and exact P001 remain unchanged. Forced
initial anchors/state and boosted party fixtures are explicit. Journey victory
uses a generated, boosted Mewtwo, without enemy HP or outcome writes; it proves
native behavior rather than human balance. Older P001 native-stat battle and
full linked-route artifacts are retained, not claimed as fresh P002 executions.

The project suite also rejects wrong ROMs, validates every changed byte's owner,
checks all original bank words/new native layout, forbids new reward/flag writes
and verifies all four BPS directions plus current runtime evidence.

## Usage and limits

Use `builds/P002-prototype.zip`. Its standalone patch applies to the exact
original supplied Liquid Crystal ROM; its upgrade patch applies to exact P001.
The package contains the walkthrough, screenshots, manifests and applier without
ROM/save files. It includes all P001 content. No source binary was edited in place.

Before removing P002, **leave map6:32, return to the warehouse and save**. A save
left in the new room is not compatible with P001-only/original ROMs. Keep an
untouched personal save backup. Artificial Office/rollback fixtures under
saves/test are QA aids, not replacement player saves.

The runtime still uses the supplied-image mGBA0.10.5 cartridge adapter. Hardware,
stock-emulator conversion, unknown computed space/map uses, human difficulty and
ordinary continuous full-game progression remain unverified. No whole-game
completion percentage or restored original-intent claim follows from this slice.
