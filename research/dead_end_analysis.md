# Progression boundary: current diagnosis

**The whole beta's exact final stopping point is not yet certified.** The source save loads cleanly into the middle of Johto with the supplied-image cartridge adapter. Orange runtime fixtures bypass story entry and initialize state; they cannot establish a normal late-game playthrough.

The strongest local missing dependency is still the puzzle/battle promised by Mister R in Route 59 room `6:31`. Its introduction works, removes Mister R and has no trainer-battle command. Reachable machine/telephone/light interactions are ordinary flavor, and the damaged sign appears to hint at Iron Tail/red rocks. The standard field-move menu excludes Iron Tail; the only raw script check for move 231 is compressed data. No supported local completion handler or next-area destination has been recovered. See `mister_r_diagnosis.md` for exact offsets, search bounds and remaining indirect/native uncertainty.

The new progression experiments exclude two tempting but unsupported repairs:

1. The Mateo/Marrisa blocker-removal gate already works on original Route 54 `3:101`; forcing variant `3:107` runs the same scene and its ordinary cave exit returns to `3:101`. There is no demonstrated need to redirect the route into the variant.
2. Default Science Complex `3:111` is almost entirely ocean, with ocean rather than a door at the copied cave-warp coordinate. Its header really loads in the tested state. It cannot be treated as a finished laboratory simply because its section name exists.

The Nexus controller chain also has working execution through the intruder battle and shutdown boundary. Charge rejection preserves the counter. Escaping a charged battle still counts as success and leaves charge available, contrary to the apparent “one use” expectation. This is a concrete behavior discrepancy, not evidence that the counter is incapable of reaching its completion state. The final-boundary fixture reaches counter 1 and sets shutdown flag `0x514` even after escape.

The laboratory battle/G Rank reward and linked police rescue/Old Key → Mandarin → Route 59 → Mister R chain now work, including saving/reloading, from explicit late-game anchors. The first-trip entry component now also completes Oak/stamp/gate, Kyogre, electric-engine restart and Valencia arrival. Before claiming an exact whole-beta boundary, preserve the gap from these separate components to a continuous ordinary playthrough and other surviving native/travel paths. See linked_progression_findings.md. Relevant unsupported script/native frontiers must stay visible. A local missing handler is not evidence that all later Orange text/maps are unreachable.

The first-continuation architecture is drafted in `patch_spec.md`. It intentionally has no allocated bytes or state IDs and is not implementation-ready. It narrows the first candidate slice to the promised room puzzle/battle and records the evidence still required before that slice can be frozen. No story, map, trainer team or binary patch has been authored.

The latest asset review closes the four old raw state-command leads as inherited WaveData/LZ77 contexts, all byte-identical to FireRed. Native trainer-table consumers and bounded named records supply no intended future Mister R/Rudy team; the nearby encounters are Elite 899/912. This strengthens the local missing-handler diagnosis without turning scoped negative evidence into whole-ROM absence. Details: entry_progression_findings.md, trainer_asset_findings.md and mister_r_state_review.md.
