# P001 approved warehouse prototype

The user approved the concrete design with **“approved, next steps.”**
[approval.json](design/approval.json) records that later authorization. The
[review manifest](design/review_manifest.json) and its reviewed files remain
unchanged as a historical baseline. This prototype implements newly authored
content; it is not a recovered original warehouse puzzle or team.

## Result

P001 adds an interactable boulder at (15,9), Iron Tail with Rock Smash fallback,
Mister R's approved six-member level 94–96 party and retries from the damaged
sign. Missing moves and declined prompts preserve progress and party PP. Native
move detection accepts fainted knowers and excludes eggs. No extra quest reward
or onward area is added. Original introduction, clue and both exits remain.

The room's existing variable 5331 retains original 0/1 behavior and uses tagged
3302/3303 hex for solved/retry and completed. Legacy unowned values recover to 1;
completed without its persistent native trainer bit recovers to retry. Only a
native battle outcome equal to 1 commits completion. Whiteout preserves retry;
an actual escape outcome cannot count as victory or retain a stale defeated bit.

`builds/dev/Liquid Crystal P001.gba` has SHA256:

`b2c3d4e3fb6f196de90bd9d88cbdcd850e429dce919034c48326d924ae413e92`

The [build manifest](../extracted/builds/P001-manifest.json) names each guarded
write and its before/after hashes. Scripts use 607/640 bytes, dialogue 402/512,
tables 178/256 and party 96/96. The 544-byte reserve remains FF. ROM size/header,
cartridge driver and embedded save are preserved. Source ROM/save hashes remain
unchanged. Only the two room pointers change within the cartridge-bank region.

The exact-source builder checks approved review hashes, expected original bytes,
nonoverlap, capacities, allowed changed ranges, determinism and forward/reverse
BPS round trips. Generated outputs never replace source binaries. The separate
[validation report](../extracted/builds/P001-validation.json) binds runtime
acceptance to this actual output hash; building alone does not imply acceptance.

## Implementation adjustment

The reviewed proposal specified native trainer battle mode 0. The pinned
[trainer battle script](references/data__scripts__trainer_battle.inc) shows that
mode 0 releases and ends the script; mode 1 calls the explicit continuation.
P001 therefore uses mode 1 to implement the approved exact-win guard. The team,
ordinary single combat, AI, items and trainer assets remain as approved. Real
victory and persistence replays exercise the resulting native continuation.

Messages use the standard native loadword/message-0 sequence. This exposes the
active message to the existing observer as well as displaying it. An initial
direct-message version rendered correctly but was missed by the observer; that
version is superseded. Screenshots were inspected for the move/challenge prompts.

## Newly executed acceptance

All nine final case files below are complete, contain passing expectations and
match the exact output hash. Every case verifies its source ROM/save are unchanged.

| Case | Passing expectations | Behavior exercised |
| --- | ---: | --- |
| matrix | 29 | Original introduction, legacy/unknown state migration, tagged states, trainer-bit combinations and actor/rock visibility |
| puzzle | 16 | Missing move, decline, Iron Tail, Rock Smash fallback, PP/party preservation and sign retry without the move |
| win | 9 | Actual native victory, all six approved species/levels/moves observed, native defeated bit, completion and repeat interaction |
| loss | 7 | Actual enemy knockout/whiteout, no completion, return/retry |
| persistence | 22 | Actual Save and fresh process for solved/completed states; interruption before victory returns to saved retry |
| exits | 5 | Ordinary Route 59 exit and original stair destination 0:0 |
| edge | 14 | Fainted knower, native-generated egg exclusion, menu return, actor collision fallback and actual non-win outcome guard |
| regression | 16 | Laboratory battle/G Rank; police battle/rescue/Old Key; ordinary Mandarin/gatehouse/Route 59/warehouse transitions and original intro |
| regions | 6 | Bounded forced-entry walking/header controls in Goldenrod and Saffron |

That is **124 runtime expectations**, in addition to project tests recorded in
the validation report. Runtime transcripts, fixture details and screenshots are
under `extracted/runtime/p001/<case>/`. The win observer records every authored
opponent's native BattleMon species, level and four moves. It does not modify them.

## Fixture and coverage limits

Tests use copied files and explicit forced initial anchors/state/party fixtures.
Victory uses one native-generated level-100 Mewtwo with Surf, Lum Berry and cached
HP/stats 999. This proves native combat/continuation, not fair battle difficulty.
The optional `saves/test/P001-ready-fixture.sav` is an artificial solved-room QA
save and must never replace the player's original save automatically. Its metadata
identifies that party and the forced entry.

Loss uses a disposable weakened party and an actual enemy knockout. Enemy HP and
battle outcomes are never injected. Mister R is an ordinary trainer battle; Run
is unavailable. The escape guard test obtains outcome 4 from an actual existing
controller wild encounter, warps back without changing that outcome and invokes
the P001 continuation directly with an explicit stale trainer-bit fixture. Actor
collision uses direct invocation of its handler with the player on its default
tile. These two controlled branch checks are not ordinary story interactions.

Initial victory fixtures fainted and the button driver stalled selecting the
fainted member; native givemon also replaces an inconsistent research party count.
The explicit one-member native-generated fixture corrected both assumptions.
The first regression run completed the linked route but then failed in optional
region setup because MapCatalog stores raw event arrays, not an `objects` list.
The failure is retained in `regression/fixture_error_event_catalog.json`; corrected
regression and separate region cases pass. Earlier failure screenshots and live
progress files are historical diagnostics; the final named case JSON is the result.

Earlier original-ROM train/entry and archaeological artifacts are retained, not
represented as fresh patched-ROM replays. No ordinary continuous Johto/Kanto/
Orange playthrough, later island, battle balance, unknown computed-owner safety
or hardware compatibility is certified. The runtime uses the project's mGBA
0.10.5 adapter for the supplied cartridge-converted image; a stock FireRed flash
profile is not equivalent. See [space ownership](space_ownership.md) for the
bounded static allocation certificate.

## Reproduce and use

From `/workspace/Liquid-Crystal`, verify sources, run `tools/build_p001.py`, run
the affected `tools/p001_runtime.py --case NAME`, then the project unittest suite.
`tools/package_p001.py` requires all nine current output-bound acceptance records,
verifies BPS round trips and creates `builds/P001-prototype.zip` with no ROM/save.
Its README includes exact input/output hashes and reversible patch instructions.

Publish this tested prototype checkpoint after reviewing/saving environment
settings. No Git commit or push has been performed. Publication, GitHub backup
and independent fresh-task restoration are distinct. Next work is human playtest/
balance and design of the next continuation slice; the whole game is unfinished.
