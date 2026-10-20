# P001 combat with native party stats

Two additional native-stat battle probes completed on the unchanged P001 ROM.
They provide **48 additional passing checks**. The existing nine-case acceptance
matrix remains valid for the exact same output bytes and was retained, not rerun.

| Team level | Native result | Recorded P001 state |
| --- | --- | --- |
| 95 | Loss/whiteout | 3302 retry, defeated bit clear |
| 100 | Victory | 3303 completed, defeated bit set |

The generated team contains Swampert, Arcanine, Machamp, Ampharos, Lapras and
Alakazam, each holding a Lum Berry. Native givemon creates the team, and native
setmonmove installs the recorded moves. Stats, HP and PP are not boosted or
refilled. No bag items, enemy HP writes, outcome edits or combat save states are
used. The level100 run observed all six authored opponents in native BattleMon
data. The level95 run lost before observing Scizor.

The button driver repeatedly selects its first move and selects a healthy party
member after a knockout. It uses SET battle style and makes no tactical move
choices or voluntary switches. It is therefore **not a human balance assessment**,
win-rate estimate or level recommendation. One sampled run at each level proves
that victory is possible with ordinary calculated stats and that a realistic
loss still preserves retry. No approved team/level/balance change was applied.

The first diagnostic used the wrong post-Celebi species number and missed the
party-menu callback range, then stalled selecting a fainted member. Those runs
were interrupted and retained as fixture_error_first_attempt.json. Swampert's
internal GenIII ID is285; the corrected fixture validates every native-generated
nickname, level and stat range. Native cursor getter11FB0C references party-menu
struct0203B0A0, and party HP controls healthy-member selection. Corrected probes
completed normally. These errors were test-fixture assumptions, not ROM defects.

Reproduce with `python3 tools/p001_combat_probe.py --level 95` or `--level 100`.
Artifacts are `extracted/runtime/p001/combat_native_95/combat.json` and the
corresponding level100 directory. Original source ROM/save hashes are verified
unchanged. Generated teams are explicit research fixtures, not naturally earned
player progress; human playtest and hardware validation remain outstanding.
