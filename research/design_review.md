# P001 — decision ready

**Approve this design to build and test the first warehouse prototype.** The
new puzzle, team and added dialogue are explicitly NEWLY_AUTHORED, as requested
for this review. No ROM implementation or original-file modification has occurred.

- Break a cracked boulder beside the existing sign with **Iron Tail**, with
  **Rock Smash** as a fallback for teams without Iron Tail.
- Battle **Mister R**: Crobat 94, Houndoom 94, Umbreon 95, Scizor 95, Gengar 95,
  Tyranitar 96. No held items; two Full Restores.
- Declining or losing permits retry through the sign. Only an actual win completes
  the room. Normal trainer money; no new item, badge, rank or onward map.
- Preserve the original introduction, clue and exits. New save-state tags preserve
  original 0/1 and recover legacy 2/3 without granting completion.
- Use a bounded 2 KiB data region away from cartridge storage. Static checks cover
  inspected references/native neighbors, text/party/table budgets and walking
  access. Unknown computed owners and hardware remain outside that static scope;
  the patched prototype must pass runtime and compatibility acceptance.

Full moves, dialogue, addresses, state handling and acceptance:
[patch specification](patch_spec.md) and [machine-readable design](design/p001.json).
Native storage evidence includes actual Save and fresh-process reload. Source ROMs
and the original save remain unchanged.

Your kickoff requires **“No implementation until this is reviewed.”** This is
the completed proposal for that review; approval to prepare it has not been treated
as approval to modify a ROM. After approval, the next batch is the builder, patch
implementation and affected acceptance tests.
