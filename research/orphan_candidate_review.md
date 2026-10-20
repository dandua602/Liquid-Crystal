# Weak-reference text candidate review

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. Input is the frozen 64-row cohort in `extracted/text/text_triage_input.json` (47 without absolute pointers; 17 raw-pointer-only). This supplements the original corpus; it does not silently relabel it.

Bytes, pointer values, field alignment and equality are CONFIRMED_IN_ROM. FireRed-format interpretations and data-field roles are STRONGLY_INFERRED. Every map owner, native consumer, execution path and unused/reachable status remains UNKNOWN. No ROM/save changes were made.

## Partition of all 64 candidates

| Classification | Count |
|---|---:|
| `INLINE_NAME_FIELD` | 13 |
| `TABLE_POINTER_TEXT` | 11 |
| `OTHER_RAW_POINTER_TEXT` | 2 |
| `PRECEDING_MSGBOX_TARGET_WITH_PREFIX_ANOMALY` | 2 |
| `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | 30 |
| `ADJACENT_BINARY_PREFIX_CANDIDATE` | 2 |
| `UNCLASSIFIED_INTERIOR_POINTER_TEXT` | 2 |
| `INTERIOR_POINTER_SELECTED_TRUNCATED_TEXT` | 2 |

## Findings that change the interpretation

- Thirteen candidates are inline name fields: Nexus class name, eleven trainer names and the GS BALL item name. Trainer names align to table `0xABFD84`, stride 40, field +4; the class table uses base `0x23E558`, stride 13. The bases have raw references. No direct pointer to each inline string is expected from this storage pattern. This does not establish runtime lookup or trainer reachability.
- The old `0xAC8525` suffix begins inside trainer header bytes; Danny’s actual +4 name field starts at `0xAC8528`, trainer index `0x364`. The old `0x99C03C` GS BALL suffix includes 12 bytes before the name at `0x99C048`, item index `0x115` in table `0x9990AC`, stride 44.
- Two message-shaped operands target before the strict-English suffix: operand `0x8C4D7E` → `0x8C4EED`, and operand `0x8C513C` → `0x8C52AA`. Each target begins `FC 01 08 08`: COLOR 08 followed by an English-unvalidated glyph byte 08. These explain the missed reference, while rendering/execution remain unverified.
- Two nearby pointers are to adjacent binary data, not recovered text references. `0x918D74` targets movement `12 12 12 FE` at `0x918E14`; speech plausibly starts `0x918E18`. `0x997DE9` targets a one-item u16 inventory (`0x62`, zero terminator) at `0x997E33`; dialogue starts `0x997E37`. The original suffixes included movement/inventory bytes as formatting/spaces.
- Pointer priority truncated two complete strings: the old `0x96999A` candidate is inside Oak’s full dialogue at `0x969854` through `0x969BBA` exclusive; old `0xAAAA35` is inside the Sunburst Island map text at `0xAAA9DC` through `0xAAAA7B` exclusive. Both fuller candidates parse strictly to EOS and have no exact start pointer. The raw interior pointer hits remain unclassified.
- Eleven raw-pointer texts fit table/data roles: seven place labels, three item descriptions and a legendary-bird description. The orange-colored evolution stone and bird wings do not establish Orange story relevance. Credits mentioning Mister Glitch are another lexical false relevance match.
- Nine of the 64 candidates have normalized-equal copies with message-shaped references. Equality removes controls and collapses whitespace; it does not identify which copy is active or prove another copy unused.
- Thirty remaining candidates have no absolute pointer over their existing parsed extent. This is a bounded static observation; indirect/native use and ownership remain open. One Danny candidate at `0xB01BB0` has a cleaner possible start at `0xB01BB2` after an uncertain two-byte prefix.

## Candidate ledger

| Original start | Classification | Text preview |
|---|---|---|
| `0x23e830` | `INLINE_NAME_FIELD` | Nexus |
| `0x3d648d` | `TABLE_POINTER_TEXT` | A peculiar stone that makes certain species of POKéMON evolve. It is colored orange. |
| `0x3d8f7f` | `TABLE_POINTER_TEXT` | A mysterious POKé BALL given to you by PROF. IVY. It’s rumored to contain a POKéMON! |
| `0x4487c0` | `TABLE_POINTER_TEXT` | One of the legendary bird POKéMON. Those seeing it are overwhelmed by its orange wing |
| `0x71dd90` | `TABLE_POINTER_TEXT` | SANDWAY TOWN |
| `0x723ab0` | `TABLE_POINTER_TEXT` | NEXUS LABORATORY |
| `0x731b10` | `TABLE_POINTER_TEXT` | VALENCIA ISLAND |
| `0x7720d9` | `OTHER_RAW_POINTER_TEXT` | This game is a remake of POKéMON Crystal which has Johto, Kanto and Valencia Island c |
| `0x8c4ef1` | `PRECEDING_MSGBOX_TARGET_WITH_PREFIX_ANOMALY` | rivell: Well if you don’t mind then Were going to have our POKéMON BATTLE. .......... |
| `0x8c52ae` | `PRECEDING_MSGBOX_TARGET_WITH_PREFIX_ANOMALY` | rivell: Well if you don’t mind then Were going to have our POKéMON BATTLE. .......... |
| `0x8e5fbc` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | CELADON POKéMON GYM LEADER: ERIKA WINNING TRAINERS: {RIVAL}, ZANE, AXEL and {PLAYER} |
| `0x9031ae` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: BUGSY WINNING TRAINERS: rival , AXEL, ZANE, {PLAYER} |
| `0x90321d` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x903255` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: JASMINE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x90328f` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x9032c7` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x9032ff` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: PRYCE WINNING TRAINERS: {RIVAL} , AXEL, ZANE, {PLAYER} |
| `0x90b2da` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: BUGSY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER} |
| `0x90b30e` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: WHITNEY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER} |
| `0x90b345` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x90b37e` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: JASMINE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x90b3b9` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x90b3f2` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: PRYCE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x90b42b` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | LEADER: CLAIR WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER} |
| `0x918e17` | `ADJACENT_BINARY_PREFIX_CANDIDATE` | MISTER G: Erm... Aha we got you... Oh you’re er not him. Pity. W-well, d-don’t interr |
| `0x92ed6e` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | MISTER R: You know we could have amounted to more than this me and my comrades. You p |
| `0x93030b` | `UNCLASSIFIED_INTERIOR_POINTER_TEXT` | Scientist: Hey, thanks for getting rid of those guys. I’m from the Science Complex ju |
| `0x9363e6` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | Watering flowers all day is fun. I love it! Especially becuase this is PROF. IVY’s pr |
| `0x9393ff` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | WINNING TRAINERS: AXEL, ZANE, {RIVAL} |
| `0x95252c` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | JIN: (sigh) You did good today, {PLAYER}. Hopfully i’ll see you around VALENCIA ISLAN |
| `0x96823a` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | MISTER R: You know we could have amounted to more than this me and my comrades. You p |
| `0x96999a` | `INTERIOR_POINTER_SELECTED_TRUNCATED_TEXT` | t it’s to valuable to ship over here and I can’t leave this LAB to get it... That’s w |
| `0x974464` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | MISTER R: Alright then. ZANE: Excellent you won’t regret it. |
| `0x997e34` | `ADJACENT_BINARY_PREFIX_CANDIDATE` | Welcome to FAST SHIP S.S.AQUA. Would you like travel to VALENCIA ISLAND? |
| `0x99c03c` | `INLINE_NAME_FIELD` | GS BALL |
| `0x9ad8f9` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | ROUTE 48 ← ESSENCE TOWN ↑ ORIENTAL CITY → PROF. IVY’S LAB |
| `0x9b33f0` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORS |
| `0x9ba36f` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | MISTER R: You know we could have amounted to more than this me and my comrades. You p |
| `0x9c294b` | `OTHER_RAW_POINTER_TEXT` | Linkandzelda Zeikku Mister Glitch |
| `0x9c3e12` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | ZANE: Thanks for finding that kid’s DOLL. I wouldn’t of been able to get to the GYM o |
| `0x9d6aa1` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | TRAINER TIPS Have you come to meet PROF. IVY? Her lab is located down from here, and  |
| `0x9d6b53` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | TRAINER TIPS While in the ORANGE ISLANDS you may experience some strong currents. The |
| `0xa142bd` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORS |
| `0xa175e4` | `TABLE_POINTER_TEXT` | VALENCIA PORT |
| `0xa9b695` | `TABLE_POINTER_TEXT` | A rusty, old looking key for the Old Warehouse on Mandarin Island. Looks untouched fo |
| `0xaaaa35` | `INTERIOR_POINTER_SELECTED_TRUNCATED_TEXT` | ute 55, Sandway Town. A large circle is placed around West Vale Port. |
| `0xabb58a` | `UNCLASSIFIED_INTERIOR_POINTER_TEXT` | Mister G: ... You, kid, what’s your name? {PLAYER}? Hmm, so my suspicions are confirm |
| `0xac03a0` | `INLINE_NAME_FIELD` | Danny |
| `0xac3320` | `INLINE_NAME_FIELD` | Zane |
| `0xac3370` | `INLINE_NAME_FIELD` | Zane |
| `0xac3398` | `INLINE_NAME_FIELD` | Zane |
| `0xac3410` | `INLINE_NAME_FIELD` | Zane |
| `0xac53a0` | `INLINE_NAME_FIELD` | Zane |
| `0xac5940` | `INLINE_NAME_FIELD` | Danny |
| `0xac5dc8` | `INLINE_NAME_FIELD` | Zane |
| `0xac5df0` | `INLINE_NAME_FIELD` | Zane |
| `0xac8050` | `INLINE_NAME_FIELD` | 4 Mister G |
| `0xac8525` | `INLINE_NAME_FIELD` | <MN> éDanny |
| `0xad3d04` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | Nexus One Status: Activated. Global power level: {STR_VAR_1}0%. |
| `0xafc29e` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | Inserting G Rank into Nexus One. Insufficient in G Rank to activate System Console. P |
| `0xb01bb0` | `NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE` | ’aDanny: Hey, {PLAYER}, you’re back for another race? I hope you listened to what I s |
| `0xc04ea4` | `TABLE_POINTER_TEXT` | MANDARIN CITY |
| `0xc05294` | `TABLE_POINTER_TEXT` | ROUTE 59 |
| `0xc05304` | `TABLE_POINTER_TEXT` | SCIENCE COMPLEX |

## Reproduce and next work

`python tools/orphan_reference_audit.py` validates source hash, exact text extents, pointer values, table geometry, representative normalized duplicates, binary/message-prefix distinctions and the 64-row partition before regenerating this report and `extracted/text/orphan_reference_audit.json`.

Keep the original reference status separate from this supplemental classification. Candidate discovery should retain complete strict-English starts even when an interior raw pointer exists; nearby pointer targets should be typed by their consumer before becoming text references. Fixed-width field consumers need table-base plus index analysis. Review surviving dialogue variants and their map/script owners next; no absent-pointer candidate is certified orphaned, broken or deletable.
