# Warehouse engineering feasibility

No missing warehouse mechanic, dialogue or team is implemented or presented as
recovered developer intent. The new experiment exercises native functions and
existing encounters on disposable copies. Source ROM/save hashes are unchanged.

## Iron Tail detection

Standard command 7C is callable in this image and returns the first zero-based
party slot knowing move 231, or 6 if absent. Controlled native move setters verify
absent → first slot → sixth slot → absent. It returns the species in variable
8004. A fainted Alakazam still satisfies the native check; this is a demonstrated
behavior to account for in the eventual design, not an extra health requirement.
Reference code excludes eggs, but that branch was not separately runtime-tested.

This proves a future interaction can query Iron Tail without adding it to the
party field-action menu. It does not prove that this was the original mechanic,
identify the missing red rocks, or establish a correct interaction coordinate.

## Victory versus escape

Pinned FireRed `data/specials.inc` puts GetBattleOutcome at index B4. The actual
LC native command table, special-table pointer and B4 target are verified; this
does not assume every Liquid Crystal table kept its FireRed location. In this
image B4 targets 0x0CA74C, whose literal reads byte 0x02023E8A. Native bytes match
the supplied FireRed reference. Specialvar 26 writes its result to 800D.

An actual existing laboratory battle finishes with result 1 and earns G Rank.
An actual existing Nexus intruder escape finishes with result 4, while the old
controller still decrements. Neither enemy HP nor the outcome byte is injected.
This rerun adds result observability missing from the older journey artifacts;
the remaining journeys were not repeated.

The proposed P001 completion rule is now precise: after battle return, query B4
and commit completion only for result 1. A trainer-defeated bit alone is
insufficient: the inherited callback's non-loss classification also includes
escape-like outcomes. Result 2/3 or any other value must not grant completion.
P001 loss/whiteout/escape/interruption paths remain acceptance tests for a future
patched game; those cases were not all newly exercised here.

## Bounded ROM budget

See [P001 budget](p001_budget.md). A 2 KiB envelope makes candidates away from the
cartridge save area available without ROM expansion. Proposed 0xB9EF00–0xB9F700
passes the full raw alias/alignment and 256-byte guard screen. No bytes or trainer
ID are reserved; computed/native ownership, asset extents and final design remain
explicit gates. The earlier 4 KiB screen remains valid at its stated threshold.

## Reproduce

`python3 tools/p001_preflight.py` regenerates the read-only static budget screen.
`python3 tools/warehouse_primitives.py` runs the controlled native feasibility
experiment. Its JSON, native signatures, transcript and screenshots are under
`extracted/runtime/warehouse_primitives/`; all 16 expectations pass.
