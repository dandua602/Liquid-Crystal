# P003 proposal: Mandarin communications shutdown

**For review; no P003 ROM or patch exists. P002 remains the current download.**

After defeating Mister R, use P002's warehouse sign passage to reach the Office
service room. Its attendant would offer to shut down the local Nexus
communications network. Choosing Yes would activate surviving Mandarin aftermath
dialogue. Choosing No would leave the city as it is. This is a small connective
chapter, with a [draft player guide](../walkthrough/P003-preview.md).

## Recovered evidence and new design

**CONFIRMED_IN_ROM:** ordinary flag `0x5B2` is read by 22 literal checkflag
shapes. Bounded map associations and dialogue messages are retained in
[aftermath.json](../extracted/runtime/mandarin_aftermath/aftermath.json).
No direct literal setflag/clearflag shapes for it were found. This does not rule
out native or computed writers, nor prove the original intended trigger.

On the exact P002 ROM, disposable native flag fixtures confirm both original
citizen branches: before, the islands are overrun; after, the citizen should get
back to work. They also confirm that the Pokémon Center scientist (local5,
position9,6) disappears when the flag is set. Ten expectations pass. These tests
invoke original dialogue roots directly after explicit state/map setup; they do
not prove normal story completion or P003 behavior.

The Center's hostile local4 at2,8 remains visible with either flag value. His
original after-branch points to an empty string at`0x9314DA`; the runtime renders
a blank text box. Giving this existing actor visibility flag5B2 would remove that
blank interaction on reentry. This departure assignment is **NEWLY_AUTHORED**.

**NEWLY_AUTHORED:** the local communications shutdown, attendant offer, all five
new messages, completion trigger and local4 departure. The surviving game does
not establish this causal link. We are reusing its aftermath state rather than
claiming to recover the missing Office story. Some 5B2 branches are identical
placeholders; we cannot claim that the Department Store, gym or whole city is
repaired. A gym citizen changes dialogue, but no Rudy fight is added.

## Exact behavior and state contract

- Entry and room remain P002 map6:32, with the same normal warehouse return.
- Attendant requires room variable5331=`3303` **and** native trainer929 defeated.
  Missing either shows “The service controls are locked.” No state changes.
- If5B2 is already set, show the repeat message without another operation.
- Otherwise ask “Shut down the local NEXUS / communications network?”
  No or cancel leaves5B2 clear and says the controls are still running.
- Yes sets only existing ordinary flag5B2, then confirms shutdown. No additional
  variable, reward, trainer bit, item, map or save structure is allocated.
- On the next Center load, original scientist5 and newly assigned local4 are
  absent. Original 5B2 dialogue branches become active. Save/reload must retain
  this state without repeating the offer.

Exact strings and gate: [p003.json](design/p003.json). The attendant's old P002
endpoint line would be replaced by this interaction. Existing city front-door
blockers, flag5B6, police rescue flags, rank items, upper floors and Route60 remain
outside this proposal. G Rank is item114; item115 is GS Ball, not a new rank.
No Zane location or missing boss team is invented.

## Storage, hooks and preservation

The compiled preview uses133/192 script bytes and224/320 text bytes.
The [sizing preview](../extracted/maps/p003_design_preflight.json) compiles scripts
and encoded text without writing a ROM. The proposed512-byte interval is
`0xB9F800–0xB9FA00` (end exclusive):192 bytes for scripts and320 for text.
The [space screen](../extracted/maps/p003_space_preview.json) pins exact P002,
requires allFF bytes, checks raw08–0D pointer aliases at every alignment with
256-byte guards, and verifies the neighboring native tables' signatures/bounds.
The left table endsB9E138; the right indexed table beginsB9FEE0. The new guarded
region lies between them, outside the cartridge driver/save bank. This bounded
certificate does not exclude all unknown computed consumers or hidden assets.

Only two external edits are proposed:

| Site | Current bytes | Proposed bytes | Purpose |
|---|---|---|---|
| B9F6C4 | 2c f5 b9 08 | 00 f8 b9 08 | New Office attendant script pointer |
| C0B550 | 00 00 | b2 05 | Existing Center local4 visibility flag |

P001/P002 scripts, map bank, graphics/layouts, trainer table, original controls,
original embedded save and cartridge driver would stay byte exact outside these
two hooks and the new allocation. A future builder must reject unexpected
inputs, overlaps, overflow or writes outside the reviewed manifest.

## Required acceptance after approval

Test actual attendant interactions for locked/forged completion, No/cancel,
Yes, repeat and preexisting5B2 states. Verify no unintended state/item changes.
Walk from an earned P002 warehouse victory into the service room, operate the
controls, return normally and verify original citizen dialogue and both Center
departures using normal interactions. Test actual Save and fresh-process reload,
including a P002 saved game upgrade. Run existing affected access/puzzle/rollback
checks and reversible original/P002 patch roundtrips. Update the playable
walkthrough with observed screenshots before packaging P003.

Rollback reverses ROM bytes, not save history: after shutdown,5B2 remains set in
that save even on P002/original, where the hostile actor's blank branch returns.
Keep a pre-P003 save backup to restore the prior city story state. Leave new
map6:32 and save in the original warehouse before removing P002/P003 entirely.
Do not automatically clear an existing story flag on downgrade.

## Review decision

Approve this specific newly authored shutdown trigger, reuse of5B2 and departure
assignment before implementation. The project brief says, “No implementation
until this is reviewed” ([Step7](../PROJECT_BRIEF.md#step-7--patch-architecture)).
No approval is needed to retain this research or publish these review files on
GitHub; the pending decision concerns the next ROM change.
