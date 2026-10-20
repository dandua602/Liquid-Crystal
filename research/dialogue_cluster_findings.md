# Step 2 milestone: neighboring messages and candidate entry paths

## Completed

Expanded the five established anchors by explicit script-transfer pointers, not physical proximity. Added stack-aware calls/returns, both conditional branches, and separately labeled trainer-engine continuation candidates. The resulting corpus contains 32 distinct referenced strings, 11 absent from the earlier keyword corpus. Six of those additions are direct story/event context; five belong to the shared Pokédex dialogue reached through Oak's common tail. Do not count the shared material as newly discovered Orange story.

The five selected clusters have no unresolved opcode frontier, instruction overlap, or configured search-limit stop. That means these bounded format paths were decoded; it does not mean native routines, standard scripts, battle outcomes or gameplay paths were simulated.

## Findings and byte evidence

All addresses are ROM offsets. Text/instruction bytes are CONFIRMED_IN_ROM; their FireRed-format meanings are STRONGLY_INFERRED. LC handlers, map roots and runtime execution remain unverified.

### Danny: an explicit battle-to-badge link

- Raw pointer `0xC0ABA4` targets candidate entry `0xB00435`.
- `0xB00435` has checkflag-shaped operand `0x571`; the conditional transfer at `0xB00438` points to `0xB0FF91` through operand `0xB0043A`.
- `0xB0FF91` is trainerbattle mode 1, trainer `0x364`, with text pointers `0xB11AA6` and `0xB11B79`. Its explicit continuation operand at `0xB0FF9F` targets `0xB0FFE2`.
- That continuation references the Sea Ruby Badge speech at `0xB11C47` and contains setflag-shaped operand `0x575`.
- The address after the trainer command, `0xB0FFA3`, instead references post-battle dialogue at `0xB11BD5`. Engine logic chooses which trainer continuation is used; the graph keeps both as outcome-dependent candidates.
- The other conditional path references Danny's challenge introduction at `0xB01F94`, then transfers to `0xB07E9A`, which has setflag-shaped operand `0x570`.

Newly recovered strings:

| Offset | Text/context |
|---|---|
| `0xB11AA6` | “Welcome back, {PLAYER}.” Danny says battling the player may reveal what his own Pokémon bonds lack. |
| `0xB11B79` | “Outstanding! Simply amazing.” He says the battle clarified what he is lacking. |
| `0xB11BD5` | He thanks the player and says he will train harder and strengthen his own Pokémon bonds. |

This links the gym battle text to the badge speech in the encoded script structure. It is not proof the battle or badge can be reached in play, and the flag operands have not been certified as safe, unused, or independently mapped to save state.

### Mister G: item tuple, departure and Axel call

Candidate entry `0xAAAF9A` has an incoming pointer at `0xC00582`. Its uninterrupted path includes the pre-battle speech `0xABCCE8`, trainer `0x345` in mode 9, revised Commanding Rank speech `0xB1D4E0`, an item-giving-shaped sequence, and departure speech `0xAB7EEB`.

At `0xAAAFC2` and `0xAAAFC7`, values `0x114` and `1` are placed in script variables `0x8000` and `0x8001`, then callstd 0 at `0xAAAFCC` matches the reference engine's obtain-item convention. The script subsequently sets operand `0x513`, performs fades/object removal, writes var `0x5315` to `1`, and transfers to `0xAAAFEB`. This is evidence for an item award; its runtime behavior and identification of the LC item record remain open.

The expanded path references Axel's call at `0xAB7CF8`, a repeated-question variant at `0xAACF4C`, and his response acknowledging that the player already removed a lab leader at `0xAAD76A`. The repeated-question branch is a finite static graph cycle; it is not classified as a bug.

Two previously unindexed trainer strings are at `0xABB872` (“You put up a mighty good fight, son.”) and `0xABB853` (“Meddlers have no place here.”). Mode 9 interprets these as defeat/victory strings, not a normal intro/defeat pair, per the pinned battle parameter definitions. Outcomes have not been tested.

### Oak: branch tree links the GS Ball handoff to later requests

An incoming pointer at `0x77785C` targets candidate entry `0x9D609D`. The format path checks operands `0x1722` and `0x1721`; the latter's conditional transfer at `0x9D60A9` targets the handoff at `0x9D60E1`. The handoff speech at `0x9E2B2D` is followed by remove-item-shaped operands `0x115`, quantity `1`, and setflag-shaped operand `0x1722`.

The other branch transfers through `0xA844E4` to `0xB123CD`. That path references the existing GS Ball return-to-player / Kurt delivery request at `0xA9B0A4`, plus later Kurt-research and Celebi-related dialogue. This is a connected static branch tree, not a new story reconstruction or proof that each condition is attainable.

The new reminder at `0x9013C2` asks whether the player has brought the Ball and then mentions checking the Pokédex. Oak's branches also join common script `0x90116D`, which reaches five additional strings at `0x98270C`, `0x982782`, `0x9827C8`, `0x9827FE`, and `0x982841`. These are shared Pokédex progress/completion context, not Orange-specific continuation.

### Sign anchors

The Rudy gym sign and Route 59 directional sign remain simple message/release/end format paths. No additional dialogue is linked from those roots within this scope. Their raw table pointer sites remain unclassified; the analysis does not silently treat neighboring table entries as connected events.

## Files and validation

- `tools/dialogue_cluster_audit.py`: repeatable branch/call/neighboring-message audit.
- `extracted/text/dialogue_clusters.json`: source hash, bounds, raw instruction bytes, pointer operands, candidate roots, witness paths, edges, messages, overlaps and unresolved frontiers.
- `research/dialogue_cluster_audit.md`: complete decoded cluster text and pointer evidence.
- `tests/test_dialogue_clusters.py`: branch alternatives, nested returns, trainer outcomes/roles, bad targets, unknown opcodes, loops, supplied-ROM paths and byte integrity.
- Pinned `src/battle_setup.c` added to `research/references/manifest.json` to distinguish trainer continuations and mode 9 text roles.

Twenty-six tests pass across both test files. No ROM/save writes, boot tests, save loading tests, emulator tests or hardware tests were performed.

## Risks / unknowns

All raw root pointers still need an owner. Opcode-handler identity, dynamic/native effects, standard scripts, trainer outcomes and flag attainability remain unverified. The selected scope is five anchors and two reverse-pointer rounds, with explicit depth/state/instruction bounds. Step 2 remains incomplete for the rest of the Orange/Nexus corpus; no unused/reachable/broken event classification is justified yet.

## Next bounded step

Expand this entry-path and neighboring-message audit to the remaining Science Complex / Nexus machine dialogue anchors, including charging and shutdown messages, before moving to maps or story authorship.
