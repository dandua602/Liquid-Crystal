# Orange text index — boundary and reference audit

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`. Supersedes the initial keyword-only report; counts differ because searches now ignore case, suffix duplicates are merged, and boundaries use pointer targets/control parsing.

2372 keyword hits → 1388 accepted blocks; 318 specific research-seed blocks; 42 unresolved hits. Supporting terms are separately listed in JSON.

## Evidence rules

CONFIRMED_IN_ROM labels byte/text presence only. FireRed character/control and operand formats are pinned in references/manifest.json; their semantic interpretation in LC is STRONGLY_INFERRED until engine/runtime validation. All offsets are ROM file offsets; pointers use little-endian 0x08000000 + offset. Every byte alignment was searched. A script operand shape does not establish a map owner, valid entry path, execution, or reachability. No pointer found is not proof of unused content. No scene has been newly authored.

The decoder consumes FC control arguments, FD placeholders and F7 dynamic indices; FF is EOS only outside parameters. Dynamic expansion is not simulated. Unknown controls reject strict candidates and remain unresolved. Case-folding changes only letter bytes, and keyword bytes must map to glyph tokens. Complete text boundaries from the reviewed triage supplement take priority over accidental interior pointer starts; otherwise pointer-backed boundaries take priority. Fallback/readable suffixes without exact references remain provisional. A 4096-byte backward search and 8192-byte parse bound mean long/encoded/compressed content can be missed. Interior pointers are retained separately.

## Provisional event clusters

These are topic groups, not a proven chronological progression. A Zane, Ivy, or other proper-name hit alone does not identify an Orange Islands event; some matches belong to earlier game content. Order below follows entry/places/event subjects; scripts must determine actual ordering.

### Other keyword context; relevance unresolved — STRONGLY_INFERRED grouping

25 candidate blocks: 0x17c1d0, 0x3d648d, 0x4487c0, 0x8ed0e0, 0x914899, 0x925a5e, 0x925b23, 0x931350, 0x977d1f, 0x9c7d46, 0x9cb344, 0x9cc9b3, 0x9d614e, 0x9d6b53, 0x9d6c31, 0x9d9423, 0x9db7a0, 0xa13d94, 0xa3b0eb, 0xa9bb79, 0xa9bbce, 0xad4077, 0xb19bb1, 0xb1a2cf, 0xc05294.

### Science Complex / Team Nexus — STRONGLY_INFERRED grouping

167 candidate blocks: 0x23e830, 0x723ab0, 0x853e34, 0x85504e, 0x855222, 0x8698fd, 0x871ead, 0x8720d0, 0x883073, 0x88325c, 0x883447, 0x883634, 0x8c4ef1, 0x8c4fda, 0x8c52ae, 0x8c5397, 0x8dbc50, 0x8dbca2, 0x8e420a, 0x8e5fbc, 0x9031ae, 0x9031e7, 0x90321d, 0x903255, 0x90328f, 0x9032c7, 0x9032ff, 0x903335, 0x90336a, 0x9033a1, 0x9033d6, 0x90340b, 0x903440, 0x903475, 0x904247, 0x904598, 0x90b24c, 0x90b2da, 0x90b30e, 0x90b345, 0x90b37e, 0x90b3b9, 0x90b3f2, 0x90b42b, 0x9173bf, 0x918e17, 0x918eb9, 0x91934b, 0x919432, 0x9194ff, 0x920bc9, 0x92ed6e, 0x93030b, 0x93082c, 0x930d0c, 0x930fc0, 0x9311ba, 0x931271, 0x935c80, 0x935d4c, 0x9393ff, 0x939422, 0x9403ec, 0x952a0e, 0x95d67f, 0x96823a, 0x9682da, 0x969f0d, 0x969f5f, 0x969f80, 0x96a012, 0x96a102, 0x96a18f, 0x96a2a2, 0x973311, 0x974464, 0x97aaac, 0x982a6f, 0x982af6, 0x997b6e, 0x9ad021, 0x9b33f0, 0x9ba36f, 0x9c294b, 0x9c3e12, 0x9cb4a4, 0x9cb5e7, 0x9d5cf6, 0x9d5d40, 0x9d5f6e, 0x9d5f89, 0x9d6003, 0x9d9e54, 0x9db93d, 0x9e0105, 0x9e014a, 0x9e04f2, 0x9e0537, 0x9e1d59, 0x9e25ab, 0x9e25fa, 0x9e267c, 0x9e278a, 0x9e283e, 0x9eea72, 0x9eea81, 0x9eeae3, 0x9f15a5, 0x9f423a, 0xa0884d, 0xa088b4, 0xa08ac8, 0xa0afc6, 0xa0b112, 0xa0e791, 0xa13fb2, 0xa142bd, 0xa143b3, 0xa2560a, 0xa5fe7c, 0xa5fedc, 0xa745ed, 0xa7fd92, 0xa8ebf9, 0xa8ec41, 0xa8edf2, 0xa96d00, 0xa96e40, 0xa9802b, 0xa980c1, 0xa9822a, 0xa982c7, 0xa9b80d, 0xa9b883, 0xa9c368, 0xa9c42f, 0xa9c482, 0xa9c4d4, 0xaa0f50, 0xaa1d8c, 0xaa1ed3, 0xaa5dc4, 0xaa5f0b, 0xaaab4c, 0xaacf4c, 0xab7cf8, 0xab7eeb, 0xabb58a, 0xabcce8, 0xac3320, 0xac3370, 0xac3398, 0xac3410, 0xac53a0, 0xac5dc8, 0xac5df0, 0xac8050, 0xad339b, 0xad3bb4, 0xad3c54, 0xad3d04, 0xad3d3d, 0xafc29e, 0xb01831, 0xb1d4e0, 0xb1dea8, 0xc05304.

### Valencia / Oak / Ivy / GS Ball — STRONGLY_INFERRED grouping

82 candidate blocks: 0x3d8f7f, 0x731b10, 0x7720d9, 0x90e378, 0x90e39d, 0x914938, 0x914c24, 0x914eae, 0x91e818, 0x91ea90, 0x9265af, 0x9265f2, 0x926636, 0x92decf, 0x92df12, 0x92df56, 0x92e39c, 0x92e6cb, 0x931f83, 0x93636c, 0x9363c1, 0x9363e6, 0x9365b2, 0x9365d4, 0x936b67, 0x936c74, 0x936cc6, 0x936cfe, 0x93a50d, 0x93a558, 0x93ebed, 0x93ec43, 0x945271, 0x9452e6, 0x945654, 0x9456c9, 0x95109c, 0x951111, 0x9514a0, 0x951513, 0x951cfc, 0x951d6e, 0x952127, 0x952199, 0x95252c, 0x955858, 0x955c4a, 0x955cbc, 0x9560ae, 0x95612d, 0x968d35, 0x969854, 0x997e34, 0x99c03c, 0x9aa791, 0x9ad8f9, 0x9c7b69, 0x9ccb4f, 0x9ccb9d, 0x9cccbd, 0x9ccd5c, 0x9d0f04, 0x9d0f8a, 0x9d5a78, 0x9d69b8, 0x9d6aa1, 0x9d6ceb, 0x9d93a2, 0x9e2b2d, 0xa175e4, 0xa3543f, 0xa9b0a4, 0xb12063, 0xb121a6, 0xb1a0e7, 0xb1a1f4, 0xb1a347, 0xb1a3dd, 0xb1a6de, 0xb1d7de, 0xb2922f, 0xb2928d.

### Sandway / Danny / Safari tests — STRONGLY_INFERRED grouping

27 candidate blocks: 0x71dd90, 0xa24a9a, 0xa258f4, 0xaaa9dc, 0xac03a0, 0xac5940, 0xac8525, 0xad339b, 0xb0019c, 0xb01952, 0xb01bb0, 0xb01f94, 0xb07f2a, 0xb080d1, 0xb0add5, 0xb0fda0, 0xb0fe2c, 0xb0ff2a, 0xb0ffad, 0xb1075c, 0xb109a2, 0xb11c47, 0xb11dc4, 0xb11de8, 0xb11e5e, 0xb17310, 0xb1a512.

### Mandarin / Rudy — STRONGLY_INFERRED grouping

21 candidate blocks: 0x930255, 0x93028c, 0x930c7d, 0x930cbc, 0x930d37, 0x93111e, 0x9f0daf, 0x9f3887, 0x9f3d4b, 0x9f3d67, 0xa7149f, 0xa9b5ba, 0xa9b695, 0xa9bdc8, 0xa9be87, 0xa9c482, 0xa9c4d4, 0xa9c502, 0xb0019c, 0xb1aeb9, 0xc04ea4.

## Specific-seed text and references

### 0x17c1d0 — Orange

CONFIRMED_IN_ROM: bytes through 0x17c246 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x1645e5; command candidate 0x1645e3; target 0x17c1d0.

```text
By the way, “appeal” is a weird
word, if you think about it.<PARAGRAPH>

Like, is it like an orange peel?
Or like a ringing bell?
```

### 0x23e830 — Nexus

CONFIRMED_IN_ROM: bytes through 0x23e836 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Nexus
```

### 0x3d648d — Orange

CONFIRMED_IN_ROM: bytes through 0x3d64e2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x3dc090, 0x99a114.

```text
A peculiar stone that makes certain
species of POKéMON evolve.
It is colored orange.
```

### 0x3d8f7f — Ivy

CONFIRMED_IN_ROM: bytes through 0x3d8fd4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x3ddfd8, 0x99c05c.

```text
A mysterious POKé BALL given to
you by PROF. IVY. It’s rumored to
contain a POKéMON!
```

### 0x4487c0 — Orange

CONFIRMED_IN_ROM: bytes through 0x448830 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x44fce8.

```text
One of the legendary bird POKéMON.
Those seeing it are overwhelmed by its
orange wings that seem to be on fire.
```

### 0x71dd90 — Sandway

CONFIRMED_IN_ROM: bytes through 0x71dd9d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8bc0.

```text
SANDWAY TOWN
```

### 0x723ab0 — Nexus

CONFIRMED_IN_ROM: bytes through 0x723ac1 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8bd0.

```text
NEXUS LABORATORY
```

### 0x731b10 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x731b20 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8b24.

```text
VALENCIA ISLAND
```

### 0x7720d9 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x7721ac (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x462ef8, 0x915ea6.

```text
This game is a remake of POKéMON
Crystal which has Johto, Kanto and
Valencia Island completed. 
Report bugs at http://romhack.me/
pokemonliquidcrystal

Enjoy the game and I’ll leave the 
rest to PROF. OAK!.....
```

### 0x853e34 — Zane

CONFIRMED_IN_ROM: bytes through 0x853e9f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9732b9; command candidate 0x9732b7; target 0x853e34.
- Raw/unclassified pointer sites: 0x7184c0.

```text
ZANE: This kid won’t let anyone into
AZALEA TOWN until he gets his POKé<SCROLL>
DOLL back.<PARAGRAPH>

Please do something {PLAYER}!
```

### 0x85504e — Zane, gym

CONFIRMED_IN_ROM: bytes through 0x8550c3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x855033; command candidate 0x855031; target 0x85504e.
- Raw/unclassified pointer sites: 0x40dc55.

```text
ZANE: Thanks for finding that
kids doll.<PARAGRAPH>

I would’nt of been able to get
to the GYM otherwise!<PARAGRAPH>

I’ll see you later {PLAYER}!
```

### 0x855222 — Zane, gym

CONFIRMED_IN_ROM: bytes through 0x855297 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x855207; command candidate 0x855205; target 0x855222.

```text
ZANE: Thanks for finding that
kids doll.<PARAGRAPH>

I would’nt of been able to get
to the GYM otherwise!<PARAGRAPH>

I’ll see you later {PLAYER}!
```

### 0x8698fd — Zane, gym

CONFIRMED_IN_ROM: bytes through 0x869972 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8698e2; command candidate 0x8698e0; target 0x8698fd.

```text
ZANE: Thanks for finding that
kids DOLL.<PARAGRAPH>

I wouldn’t of been able to get
to the GYM otherwise!<PARAGRAPH>

I’ll see you later {PLAYER}!
```

### 0x871ead — Zane

CONFIRMED_IN_ROM: bytes through 0x871f1f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x871e61; command candidate 0x871e5f; target 0x871ead.
- Raw/unclassified pointer sites: 0xe4d9b0.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x8720d0 — Zane

CONFIRMED_IN_ROM: bytes through 0x872142 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x872082; command candidate 0x872080; target 0x8720d0.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x883073 — Zane

CONFIRMED_IN_ROM: bytes through 0x8830e5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x883027; command candidate 0x883025; target 0x883073.
- Raw/unclassified pointer sites: 0x85835, 0x8587d.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x88325c — Zane

CONFIRMED_IN_ROM: bytes through 0x8832ce (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x88320e; command candidate 0x88320c; target 0x88325c.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x883447 — Zane

CONFIRMED_IN_ROM: bytes through 0x8834b9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8833f7; command candidate 0x8833f5; target 0x883447.
- MSGBOX_SHAPE at operand 0x937dd3; command candidate 0x937dd1; target 0x883447.
- MSGBOX_SHAPE at operand 0x937e49; command candidate 0x937e47; target 0x883447.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x883634 — Zane

CONFIRMED_IN_ROM: bytes through 0x8836a6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8835e2; command candidate 0x8835e0; target 0x883634.

```text
My name is ZANE.
I’m gonna be the greatest POKéMON<SCROLL>
TRAINER in history!<PARAGRAPH>

Hey. You look weak!
Come on. Let’s battle!
```

### 0x8c4ef1 — Zane

CONFIRMED_IN_ROM: bytes through 0x8c4fcb (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
rivell: Well if you don’t mind then
Were going to have our POKéMON<SCROLL>
BATTLE.<PARAGRAPH>

......................
.....................<PARAGRAPH>

ZANE: .......................
............<PARAGRAPH>

<PARAGRAPH>

rivell: Ok. That sounds like a good
idea. Lets do it!
```

### 0x8c4fda — Zane

CONFIRMED_IN_ROM: bytes through 0x8c5063 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8c4d76; command candidate 0x8c4d74; target 0x8c4fda.
- Raw/unclassified pointer sites: 0x96baf.

```text
<COLOR 08>ZANE: I’m ZANE. A POKéMON
TRAINER like you.<PARAGRAPH>

I saw {PLAYER} come down here
and then you followed so I<SCROLL>
had to come and see what was<SCROLL>
going on.
```

### 0x8c52ae — Zane

CONFIRMED_IN_ROM: bytes through 0x8c5388 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
rivell: Well if you don’t mind then
Were going to have our POKéMON<SCROLL>
BATTLE.<PARAGRAPH>

......................
.....................<PARAGRAPH>

ZANE: .......................
............<PARAGRAPH>

<PARAGRAPH>

rivell: Ok. That sounds like a good
idea. Lets do it!
```

### 0x8c5397 — Zane

CONFIRMED_IN_ROM: bytes through 0x8c5420 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8c5134; command candidate 0x8c5132; target 0x8c5397.

```text
<COLOR 08>ZANE: I’m ZANE. A POKéMON
TRAINER like you.<PARAGRAPH>

I saw {PLAYER} come down here
and then you followed so I<SCROLL>
had to come and see what was<SCROLL>
going on.
```

### 0x8dbc50 — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x8dbc99 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8dba9d; command candidate 0x8dba9b; target 0x8dbc50.

```text
VERMILION POKéMON GYM
LEADER: LT. SURGE<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE
```

### 0x8dbca2 — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x8dbcef (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8dbaa8; command candidate 0x8dbaa6; target 0x8dbca2.

```text
VERMILION POKéMON GYM
LEADER: LT. SURGE<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x8e420a — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x8e4253 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8e3c5f; command candidate 0x8e3c5d; target 0x8e420a.

```text
SAFFRON POKéMON GYM
LEADER: SABRINA<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x8e5fbc — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x8e6007 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 CELADON POKéMON GYM
LEADER: ERIKA<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, ZANE, AXEL and {PLAYER}
```

### 0x8ed0e0 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x8ed277 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8e932c; command candidate 0x8e932a; target 0x8ed0e0.

```text
<COLOR 08>OFFICER: What do you mean your
closing the contest down?<PARAGRAPH>

???: Because I’m the new PARK
WARDEN and I said I’m closing the<SCROLL>
contest down.<PARAGRAPH>

OFFICER: But you can’t do that.
The contests have been going for<SCROLL>
years without problems.<PARAGRAPH>

WARDEN: It’s the other WARDENS
fault for moving to the ORANGE<SCROLL>
ISLANDS.<PARAGRAPH>

He should’ve known this would
happen.<PARAGRAPH>

Now if you’ll please excuse me.
I don’t have time for this<SCROLL>
nonsense...
```

### 0x9031ae — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x9031e6 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
LEADER: BUGSY<PARAGRAPH>

WINNING TRAINERS: 
rival , AXEL, ZANE, {PLAYER}
```

### 0x9031e7 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90321d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x812b3a; command candidate 0x812b38; target 0x9031e7.

```text
LEADER: WHITNEY<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER} 
```

### 0x90321d — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x903255 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: MORTY
WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
```

### 0x903255 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90328f (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: JASMINE<PARAGRAPH>

WINNING TRAINERS:
rivel , AXEL, ZANE, {PLAYER}
```

### 0x90328f — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x9032c7 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: MORTY<PARAGRAPH>

WINNING TRAINERS:
rivel , AXEL, ZANE, {PLAYER}
```

### 0x9032c7 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x9032ff (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: MORTY<PARAGRAPH>

WINNING TRAINERS:
rivel , AXEL, ZANE, {PLAYER}
```

### 0x9032ff — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x903334 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: PRYCE<PARAGRAPH>

WINNING TRAINERS:
{RIVAL} , AXEL, ZANE, {PLAYER}
```

### 0x903335 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x903369 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x82aa7b; command candidate 0x82aa79; target 0x903335.

```text
LEADER: MORTY<PARAGRAPH>

WINNING TRAINERS:
{RIVAL} , AXEL, ZANE, {PLAYER}
```

### 0x90336a — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90339f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x82c463; command candidate 0x82c461; target 0x90336a.

```text
LEADER: JASMINE<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x9033a1 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x9033d4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8247c7; command candidate 0x8247c5; target 0x9033a1.

```text
LEADER: MORTY<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x9033d6 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90340a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x80bc8d; command candidate 0x80bc8b; target 0x9033d6.

```text
LEADER: BUGSY<PARAGRAPH>

WINNING TRAINERS: 
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x90340b — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90343e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8457e2; command candidate 0x8457e0; target 0x90340b.

```text
LEADER: PRYCE<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x903440 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x903474 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x85384d; command candidate 0x85384b; target 0x903440.

```text
LEADER: CLAIR<PARAGRAPH>

WINNING TRAINERS:
{RIVAL} , AXEL, ZANE, {PLAYER}
```

### 0x903475 — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x9034bc (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16d1e2; command candidate 0x16d1e0; target 0x903475.

```text
CELADON POKéMON GYM
LEADER: ERIKA<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x904247 — Mister G

CONFIRMED_IN_ROM: bytes through 0x9043e4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90420f; command candidate 0x90420d; target 0x904247.

```text
???: So, you arrived at last.<PARAGRAPH>

Don’t bother, I already know who you
are.<PARAGRAPH>

I heard all there is to know from
Mister G and Z.<PARAGRAPH>

I’m a mastermind in the art of crime,
also known as Mister R.<PARAGRAPH>

I see you were able to obtain the
G Rank, well let me tell you<SCROLL>
straight up.<PARAGRAPH>

Mister G was a pushover compared to
me.<PARAGRAPH>

I’ll cease these silly games of yours
starting right here and now.<PARAGRAPH>

This place is officially off limits,
bye now!
```

### 0x904598 — Nexus

CONFIRMED_IN_ROM: bytes through 0x9045c5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90458f; command candidate 0x90458d; target 0x904598.

```text
Welcome to the Team Nexus Police
Department!
```

### 0x90b24c — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b281 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90b1f4; command candidate 0x90b1f2; target 0x90b24c.

```text
LEADER: FALKNER<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x90b2da — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b30e (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: BUGSY
WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER}
```

### 0x90b30e — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b345 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: WHITNEY
WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER} 
```

### 0x90b345 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b37e (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: MORTY
WINNING TRAINERS:  rivel , AXEL, ZANE, {PLAYER}
```

### 0x90b37e — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b3b9 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: JASMINE
WINNING TRAINERS:  rivel , AXEL, ZANE, {PLAYER}
```

### 0x90b3b9 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b3f2 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: MORTY
WINNING TRAINERS:  rivel , AXEL, ZANE, {PLAYER}
```

### 0x90b3f2 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b42b (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: PRYCE
WINNING TRAINERS:  rivel , AXEL, ZANE, {PLAYER}
```

### 0x90b42b — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x90b464 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 LEADER: CLAIR
WINNING TRAINERS:  rivel , AXEL, ZANE, {PLAYER}
```

### 0x90e378 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x90e392 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90e370; command candidate 0x90e36e; target 0x90e378.

```text
VALENCIA ISLAND
EAST GATE
```

### 0x90e39d — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x90e3c9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90e395; command candidate 0x90e393; target 0x90e39d.

```text
VALENCIA ISLAND - SUNBURST ISLAND<PARAGRAPH>

TOLL GATE
```

### 0x914899 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9148c2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x914733; command candidate 0x914731; target 0x914899.

```text
ORANGE ISLANDS GATE - 
UNDERSEA EXPRESS 
```

### 0x914938 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x914970 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9148ce; command candidate 0x9148cc; target 0x914938.

```text
I’m going to VALENCIA ISLAND when
the next train comes!
```

### 0x914c24 — Orange, Valencia, island

CONFIRMED_IN_ROM: bytes through 0x914c8d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x914745; command candidate 0x914743; target 0x914c24.

```text
The UNDERSEA EXPRESS is a direct
route from here to VALENCIA ISLAND<SCROLL>
which belongs to the ORANGE ISLANDS!
```

### 0x914eae — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x914f1d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x914928; command candidate 0x914926; target 0x914eae.
- Raw/unclassified pointer sites: 0x99e34a.

```text
It’s so quick to get to VALENCIA
ISLAND using the UNDERSEA EXPRESS.<PARAGRAPH>

Definatly quicker than taking the
SS.AQUA.
```

### 0x9173bf — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x91740a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16d6bd; command candidate 0x16d6bb; target 0x9173bf.

```text
FUCHSIA POKéMON GYM
LEADER: JANINE<PARAGRAPH>

WINNING TRAINERS:
AXEL, ZANE, {RIVAL} and {PLAYER}
```

### 0x918e17 — Mister G

CONFIRMED_IN_ROM: bytes through 0x918eb8 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text

MISTER G: Erm... Aha we got you...
Oh you’re er not him.<PARAGRAPH>

Pity. W-well, d-don’t interrupt
we’re dealing with an important<SCROLL>
matter, not for little kids got<SCROLL>
that?!
```

### 0x918eb9 — Mister G

CONFIRMED_IN_ROM: bytes through 0x918f35 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x914318; command candidate 0x914316; target 0x918eb9.

```text
MISTER G: What do you want?
I said leave it’s important matters<SCROLL>
not for you!<PARAGRAPH>

My two cohorts will sort you out if
you don’t!
```

### 0x91934b — Mister G

CONFIRMED_IN_ROM: bytes through 0x9193ee (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x919332; command candidate 0x919330; target 0x91934b.

```text
<COLOR 08>MISTER G: Erm...
Aha we got you...
Oh you’re er not him.<PARAGRAPH>

Pity. W-well, d-don’t interrupt we’re
dealing with an important matter,<SCROLL>
not for little kids got that?!
```

### 0x919432 — Mister G

CONFIRMED_IN_ROM: bytes through 0x9194d5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x919416; command candidate 0x919414; target 0x919432.

```text
<COLOR 08>MISTER G: Erm... Aha we got you...
Oh you’re er not him.<PARAGRAPH>

Pity. W-well, d-don’t interrupt
we’re dealing with an important<SCROLL>
matter, not for little kids got<SCROLL>
that?!
```

### 0x9194ff — Mister G

CONFIRMED_IN_ROM: bytes through 0x91959e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9194f6; command candidate 0x9194f4; target 0x9194ff.

```text
MISTER R: You know we could have
amounted to more than this me and<SCROLL>
my comrades.<PARAGRAPH>

You probably met them in the other
areas of MT. SILVER. MISTER G and<SCROLL>
MISTER H?
```

### 0x91e818 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x91e87c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x914fe4; command candidate 0x914fe2; target 0x91e818.

```text
<COLOR 08>Hello and welcome to the UNDERSEA
EXPRESS.<PARAGRAPH>

Would you like to board
the train to VALENCIA ISLAND?
```

### 0x91ea90 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x91eb7e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x91e980; command candidate 0x91e97e; target 0x91ea90.

```text
<COLOR 08>Ah I see a stamped SS.TICKET there.<PARAGRAPH>

I guess you are looking to travel to
VALENCIA ISLAND.<PARAGRAPH>

If you speak to the manager in the
SS OFFICE department they will give<SCROLL>
you SEA PASS free of charge.<PARAGRAPH>

You can use it to ride the UNDERSEA
EXPRESS!
```

### 0x920bc9 — Zane

CONFIRMED_IN_ROM: bytes through 0x920c1f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x920b4b; command candidate 0x920b49; target 0x920bc9.
- MSGBOX_SHAPE at operand 0x920d54; command candidate 0x920d52; target 0x920bc9.
- MSGBOX_SHAPE at operand 0x920de6; command candidate 0x920de4; target 0x920bc9.

```text
<COLOR 08>GRUNT: Damn.
I need some fresh air...<PARAGRAPH>

Being with that mad man, ZANE is
exhausting!
```

### 0x925a5e — Orange

CONFIRMED_IN_ROM: bytes through 0x925ad5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x925a1c; command candidate 0x925a1a; target 0x925a5e.

```text
That orange tomb stone at the end
of the room is dedicated to a<SCROLL>
POKéMON who died helping to<SCROLL>
build the new RADIO TOWER.
```

### 0x925b23 — Orange

CONFIRMED_IN_ROM: bytes through 0x925bc3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x925ae1; command candidate 0x925adf; target 0x925b23.

```text
That orange tomb stone at the end of
the room is dedicated to a POKéMON<SCROLL>
who died helping to build the new<SCROLL>
RADIO TOWER.<PARAGRAPH>

I wonder what it has to do with
MR.FUJI?
```

### 0x9265af — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9265f0 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92659e; command candidate 0x92659c; target 0x9265af.

```text
The train to VALENCIA ISLAND is
currently waiting in platform 1.
```

### 0x9265f2 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x926634 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x926578; command candidate 0x926576; target 0x9265f2.

```text
The next train to VALENCIA ISLAND
is due to arrive in {STR_VAR_1} minutes.
```

### 0x926636 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x926677 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92658b; command candidate 0x926589; target 0x926636.

```text
The next train to VALENCIA ISLAND
is due to arrive in {STR_VAR_1} minute.
```

### 0x92decf — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x92df10 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92debe; command candidate 0x92debc; target 0x92decf.

```text
The train to VALENCIA ISLAND is
currently waiting in platform 1.
```

### 0x92df12 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x92df54 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92de98; command candidate 0x92de96; target 0x92df12.

```text
The next train to VALENCIA ISLAND
is due to arrive in {STR_VAR_1} minutes.
```

### 0x92df56 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x92df97 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92deab; command candidate 0x92dea9; target 0x92df56.

```text
The next train to VALENCIA ISLAND
is due to arrive in {STR_VAR_1} minute.
```

### 0x92e39c — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x92e41b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9015d8; command candidate 0x9015d6; target 0x92e39c.
- Raw/unclassified pointer sites: 0x89113.

```text
<COLOR 08>Welcome to FAST SHIP S.S.AQUA.<PARAGRAPH>

I see that you have a stamped
TICKET.<PARAGRAPH>

I presume you would like to
travel to VALENCIA ISLAND?
```

### 0x92e6cb — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x92e6e8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92e6c3; command candidate 0x92e6c1; target 0x92e6cb.

```text
PLATFORM 1 - VALENCIA ISLAND
```

### 0x92ed6e — Mister G

CONFIRMED_IN_ROM: bytes through 0x92ee0e (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 MISTER R: You know we could have
amounted to more than this me and<SCROLL>
my comrades.<PARAGRAPH>

You probably met them in the other
areas of MT. SILVER. MISTER G and<SCROLL>
MISTER H?
```

### 0x930255 — Mandarin, Orange

CONFIRMED_IN_ROM: bytes through 0x930280 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x93024c; command candidate 0x93024a; target 0x930255.

```text
Mandarin City
Also Known As The Big Orange
```

### 0x93028c — Mandarin

CONFIRMED_IN_ROM: bytes through 0x9302ea (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x930283; command candidate 0x930281; target 0x93028c.

```text
Mandarin City Police Dep-<PARAGRAPH>

The rest has been scribbled over with
the words ”NEEXXXXUUSSSSSSS!”
```

### 0x93030b — Nexus, Science Complex

CONFIRMED_IN_ROM: bytes through 0x93055f (exclusive). Boundary: PROVISIONAL_SUFFIX. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0xe5bd5.

```text
<COLOR 08>Scientist: Hey, thanks for
getting rid of those guys.<PARAGRAPH>

I’m from the Science Complex just
north of here.<PARAGRAPH>

I don’t think I’ve seen your face
before, are you new?<SCROLL>
As a thanks I can tell you about<SCROLL>
the situation here.<PARAGRAPH>

These guys calling themself Team
Nexus just suddenly arrived here<SCROLL>
and took over the city.<PARAGRAPH>

The Police Station was completly
overun and had to be cleared out,<SCROLL>
so there’s nobody to take back<SCROLL>
control of the city.<PARAGRAPH>

I watched you battle and I can
tell, you’re good.<PARAGRAPH>

Why not drive these guys out?<PARAGRAPH>

Either way, thanks for helping us
out, we should be getting back to<SCROLL>
the Science Complex now.
```

### 0x93082c — Nexus, Science Complex

CONFIRMED_IN_ROM: bytes through 0x930a80 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9307f6; command candidate 0x9307f4; target 0x93082c.
- Raw/unclassified pointer sites: 0x382b, 0x2c8c14, 0x456c52, 0x71c1a6, 0x71c1ea, 0x71c266, 0x71c31e, 0x71cdda, 0x71f4ee, 0x7228da, 0x741386, 0x99e1c8, 0x93986b, 0x97442c, 0x1e3fe5.

```text
<COLOR 08>Scientist: Hey, thanks for
getting rid of those guys.<PARAGRAPH>

I’m from the Science Complex just
north of here.<PARAGRAPH>

I don’t think I’ve seen your face
before, are you new?<PARAGRAPH>

As a thanks I can tell you about
the situation here.<PARAGRAPH>

These guys calling themself Team
Nexus just suddenly arrived here<SCROLL>
and took over the city.<PARAGRAPH>

The Police Station was completly
overun and had to be cleared out,<SCROLL>
so there’s nobody to take back<SCROLL>
control of the city.<PARAGRAPH>

I watched you battle and I can
tell, you’re good.<PARAGRAPH>

Why not drive these guys out?<PARAGRAPH>

Either way, thanks for helping us
out, we should be getting back to<SCROLL>
the Science Complex now.
```

### 0x930c7d — Mandarin, Rudy, gym, leader

CONFIRMED_IN_ROM: bytes through 0x930cbb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9302ed; command candidate 0x9302eb; target 0x930c7d.

```text
Mandarin City Pokémon Gym<PARAGRAPH>

Leader: Rudy<PARAGRAPH>

The Mysterious Playboy
```

### 0x930cbc — Mandarin

CONFIRMED_IN_ROM: bytes through 0x930cd6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9302f7; command candidate 0x9302f5; target 0x930cbc.

```text
Mandarin City Dept. Store
```

### 0x930d0c — Route 59, Science Complex

CONFIRMED_IN_ROM: bytes through 0x930d2b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x930d03; command candidate 0x930d01; target 0x930d0c.
- Raw/unclassified pointer sites: 0x3740b.

```text
↑ Science Complex via Route 59
```

### 0x930d37 — Mandarin

CONFIRMED_IN_ROM: bytes through 0x930d53 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x930d2e; command candidate 0x930d2c; target 0x930d37.

```text
Mandarin City Office Block.
```

### 0x930fc0 — Nexus

CONFIRMED_IN_ROM: bytes through 0x931021 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x930fb7; command candidate 0x930fb5; target 0x930fc0.

```text
The Dept. Store is no longer selling
Rare Candies.<PARAGRAPH>

Turns out it was a scam by those
Nexus fools!
```

### 0x93111e — Rudy, gym, leader

CONFIRMED_IN_ROM: bytes through 0x93119a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9310a7; command candidate 0x9310a5; target 0x93111e.

```text
I’m hanging around outside the Gym
waiting for the leader, Rudy, to<SCROLL>
return.<PARAGRAPH>

He’s never around to battle anyone
when needed.
```

### 0x9311ba — Science Complex

CONFIRMED_IN_ROM: bytes through 0x931251 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9311a6; command candidate 0x9311a4; target 0x9311ba.
- MSGBOX_SHAPE at operand 0x9311b1; command candidate 0x9311af; target 0x9311ba.

```text
The famous Science Complex is just
up this way.<PARAGRAPH>

I hear they are working on a project
to revive an ancient powerful<SCROLL>
Pokémon!<PARAGRAPH>

I wonder what it could be?
```

### 0x931271 — Science Complex

CONFIRMED_IN_ROM: bytes through 0x9312de (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x93125d; command candidate 0x93125b; target 0x931271.
- MSGBOX_SHAPE at operand 0x931268; command candidate 0x931266; target 0x931271.

```text
I should be at work right now in the
Science Complex.<PARAGRAPH>

I’ve been stuck in here ever since
those guys arrived.
```

### 0x931350 — Route 59, island

CONFIRMED_IN_ROM: bytes through 0x9313df (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x931301; command candidate 0x9312ff; target 0x931350.

```text
Have you seen them?<PARAGRAPH>

Those dreadful machines on Route 58
and Route 59.<PARAGRAPH>

I heard they were placed on Sunburst
Island to damage Trainer’s Pokémon!
```

### 0x931f83 — Champion, Valencia, gym, island, leader

CONFIRMED_IN_ROM: bytes through 0x932158 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x931d91; command candidate 0x931d8f; target 0x931f83.
- Raw/unclassified pointer sites: 0x6b6180.

```text
<COLOR 08>JIN: So then...
Here we are inside the middle of the<SCROLL>
tunnel...<PARAGRAPH>

(sigh) This runs right underneath
the ocean.<PARAGRAPH>

Scary huh?<PARAGRAPH>

So what’s your name, kid?<PARAGRAPH>

{PLAYER} huh?<PARAGRAPH>

(sigh) Interesting name...
I think I might of heard it before..<PARAGRAPH>

Hey, wait!
Aren’t you the new JOHTO CHAMPION?<PARAGRAPH>

(sigh) I thought I recognised you...<PARAGRAPH>

I used to run a GYM on VALENCIA
ISLAND.<PARAGRAPH>

Me and my POKéMON would take down
any TRAINER that challenged us.<PARAGRAPH>

Eventually we got tired of it so now
I’m an ex-GYM LEADER..
```

### 0x935c80 — Zane

CONFIRMED_IN_ROM: bytes through 0x935d4a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x93579b; command candidate 0x935791; target 0x935c80.
- MSGBOX_SHAPE at operand 0x9357a1; command candidate 0x93579f; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x935825; command candidate 0x93581b; target 0x935c80.
- MSGBOX_SHAPE at operand 0x93582b; command candidate 0x935829; target 0x935c80.
- MSGBOX_SHAPE at operand 0x935a3a; command candidate 0x935a38; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x935af9; command candidate 0x935aef; target 0x935c80.
- MSGBOX_SHAPE at operand 0x935aff; command candidate 0x935afd; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x935b4b; command candidate 0x935b41; target 0x935c80.
- MSGBOX_SHAPE at operand 0x935b51; command candidate 0x935b4f; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x935b9d; command candidate 0x935b93; target 0x935c80.
- MSGBOX_SHAPE at operand 0x935ba3; command candidate 0x935ba1; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x9361d9; command candidate 0x9361cf; target 0x935c80.
- MSGBOX_SHAPE at operand 0x9361df; command candidate 0x9361dd; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x937ff3; command candidate 0x937fe9; target 0x935c80.
- MSGBOX_SHAPE at operand 0x938003; command candidate 0x938001; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x938058; command candidate 0x93804e; target 0x935c80.
- MSGBOX_SHAPE at operand 0x938068; command candidate 0x938066; target 0x935c80.
- TRAINER_TEXT_SHAPE at operand 0x93815b; command candidate 0x938151; target 0x935c80.
- MSGBOX_SHAPE at operand 0x93816b; command candidate 0x938169; target 0x935c80.

```text
<COLOR 08>ZANE: Even training my POKéMON in
KANTO doesn’t help.<PARAGRAPH>

You have humiliated me for the last
time, {PLAYER}.<PARAGRAPH>

I’m becoming more evil towards you
and the rest of the world.<PARAGRAPH>

Just wait and see what happens next!
```

### 0x935d4c — Zane

CONFIRMED_IN_ROM: bytes through 0x935e1e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x93578b; command candidate 0x935789; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x935815; command candidate 0x935813; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x935ae9; command candidate 0x935ae7; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x935b3b; command candidate 0x935b39; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x935b8d; command candidate 0x935b8b; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x9361c9; command candidate 0x9361c7; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x937fd9; command candidate 0x937fd7; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x93803e; command candidate 0x93803c; target 0x935d4c.
- MSGBOX_SHAPE at operand 0x938141; command candidate 0x93813f; target 0x935d4c.
- Raw/unclassified pointer sites: 0x935a2a, 0x935a31.

```text
<COLOR 08>ZANE: Huff, puff, I finally caught up
to you {PLAYER}.<PARAGRAPH>

I saw you get off at VERMILION CITY
so I trailed you.<PARAGRAPH>

I’ve been training my POKéMON here
in KANTO.<PARAGRAPH>

The’re far stronger than before.
Let me show you how much!
```

### 0x93636c — Ivy

CONFIRMED_IN_ROM: bytes through 0x9363b5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936363; command candidate 0x936361; target 0x93636c.

```text
This is PROF. IVY’s POKéMON RESEARCH
LAB.<PARAGRAPH>

I’m one of the gardeners here.
```

### 0x9363c1 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9363da (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9363b8; command candidate 0x9363b6; target 0x9363c1.

```text
PROF. IVY’s RESEARCH LAB
```

### 0x9363e6 — Ivy

CONFIRMED_IN_ROM: bytes through 0x936449 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Watering flowers all day is fun.
I love it!<PARAGRAPH>

Especially becuase this is PROF. IVY’s private garden!
```

### 0x9365b2 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9365d3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x93646a; command candidate 0x936468; target 0x9365b2.
- MSGBOX_SHAPE at operand 0x936482; command candidate 0x936480; target 0x9365b2.

```text
PROF. IVY is a great RESEARCHER.
```

### 0x9365d4 — Ivy

CONFIRMED_IN_ROM: bytes through 0x936637 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9363dd; command candidate 0x9363db; target 0x9365d4.

```text
Watering flowers all day is fun.
I love it!<PARAGRAPH>

Especially because this is
PROF. IVY’s private garden!
```

### 0x936b67 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x936bc6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936b5e; command candidate 0x936b5c; target 0x936b67.

```text
The POKéMON CENTERS on VALENCIA
ISLAND are less equipped than the<SCROLL>
CENTERS on the main regions.
```

### 0x936c74 — Ivy

CONFIRMED_IN_ROM: bytes through 0x936cba (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936c6b; command candidate 0x936c69; target 0x936c74.

```text
These are PROF.IVY’s books!<PARAGRAPH>

She must of left them out for a
reason...
```

### 0x936cc6 — Ivy

CONFIRMED_IN_ROM: bytes through 0x936cf2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936cbd; command candidate 0x936cbb; target 0x936cc6.

```text
PROF.IVY’s todo list!<PARAGRAPH>

Better not read it...
```

### 0x936cfe — Ivy

CONFIRMED_IN_ROM: bytes through 0x936da9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936cf5; command candidate 0x936cf3; target 0x936cfe.

```text
Hello PROF.IVY.<PARAGRAPH>

A package has arrived for you at
the MEADOW TOWN POKé MART.<PARAGRAPH>

I take it you will be picking it up
as soon as you can.<PARAGRAPH>

Thanks in advance and see you soon
:-D
```

### 0x9393ff — Zane

CONFIRMED_IN_ROM: bytes through 0x939420 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
WINNING TRAINERS:
AXEL, ZANE, {RIVAL}
```

### 0x939422 — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x93946a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16abb4; command candidate 0x16abb2; target 0x939422.

```text
CERULEAN POKéMON GYM
LEADER: MISTY<PARAGRAPH>

WINNING TRAINERS:
AXEL, ZANE, {RIVAL}, {PLAYER}
```

### 0x93a50d — Ivy

CONFIRMED_IN_ROM: bytes through 0x93a54b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9284d7; command candidate 0x9284d5; target 0x93a50d.

```text
A great professor lives near this
town.<PARAGRAPH>

Her name is PROF.IVY.
```

### 0x93a558 — Ivy, island

CONFIRMED_IN_ROM: bytes through 0x93a6be (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x93a54f; command candidate 0x93a54d; target 0x93a558.

```text
I’ve lived on this ISLAND all my
life.<PARAGRAPH>

I’ve witnessed everything that has
occoured in my lifetime.<PARAGRAPH>

Hmm...<PARAGRAPH>

You remind me of that time...<PARAGRAPH>

It was only three years ago.
Three kids came to this ISLAND.<PARAGRAPH>

They were looking for PROF.IVY.
A great POKéMON RESEARCHER.<PARAGRAPH>

What?<PARAGRAPH>

Your looking for PROF.IVY too?
Well her house is east of town.<PARAGRAPH>

I hope you’re good at climbing!
```

### 0x93ebed — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x93ec3e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9323aa; command candidate 0x9323a8; target 0x93ebed.

```text
VALENCIA ISLAND is a nice peacful
place.<PARAGRAPH>

It’s nice to lay out on the beach
here.
```

### 0x93ec43 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x93ec90 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9324c1; command candidate 0x9324bf; target 0x93ec43.

```text
There’s lot’s of powerful TRAINERS
on VALENCIA ISLAND.<PARAGRAPH>

You better watch out.
```

### 0x9403ec — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x9404e3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90f0fc; command candidate 0x90f0fa; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x90f14b; command candidate 0x90f149; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x90f19a; command candidate 0x90f198; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x913360; command candidate 0x91335e; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x9133f1; command candidate 0x9133ef; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x921a5c; command candidate 0x921a5a; target 0x9403ec.
- MSGBOX_SHAPE at operand 0x924d60; command candidate 0x924d5e; target 0x9403ec.
- Raw/unclassified pointer sites: 0x941028, 0x151bed, 0x151c3d.

```text
<COLOR 08>ZANE: You again!<PARAGRAPH>

You’re still snooping around KANTO?<PARAGRAPH>

I would’ve thought someone as strong
as yourself would have wiped out the<SCROLL>
KANTO GYM LEADERS by now...<PARAGRAPH>

Well, I too have been challenging the
KANTO GYMs.<PARAGRAPH>

I think I’m finally ready to end
this!
```

### 0x945271 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9452d4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x945230; command candidate 0x94522e; target 0x945271.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x9452e6 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9453bf (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x945214; command candidate 0x945212; target 0x9452e6.
- MSGBOX_SHAPE at operand 0x932371; command candidate 0x93236f; target 0x9452fb (interior target).
- Raw/unclassified pointer sites: 0x93236b, 0x676741.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks you you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x945654 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9456b7 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x945613; command candidate 0x945611; target 0x945654.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x9456c9 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9457a2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9455f7; command candidate 0x9455f5; target 0x9456c9.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks you you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x95109c — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9510ff (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x95105b; command candidate 0x951059; target 0x95109c.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x951111 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9511e9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x95103f; command candidate 0x95103d; target 0x951111.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x9514a0 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x951503 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x951458; command candidate 0x951456; target 0x9514a0.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x951513 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9515eb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x951435; command candidate 0x951433; target 0x951513.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x951cfc — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x951d5f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x951c94; command candidate 0x951c92; target 0x951cfc.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x951d6e — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x951e46 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x951c6e; command candidate 0x951c6c; target 0x951d6e.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x952127 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x95218a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9520b5; command candidate 0x9520b3; target 0x952127.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x952199 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x952271 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x952092; command candidate 0x952090; target 0x952199.
- Raw/unclassified pointer sites: 0xe0679b.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly
Thanks again. 
```

### 0x95252c — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x95258f (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x952a0e — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x952a54 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16a6c5; command candidate 0x16a6c3; target 0x952a0e.

```text
PEWTER POKéMON GYM
LEADER: BROCK<PARAGRAPH>

WINNING TRAINERS:
ZANE, AXEL, {RIVAL}, {PLAYER}
```

### 0x955858 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x955954 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9524bd; command candidate 0x9524bb; target 0x955858.
- Raw/unclassified pointer sites: 0x956644.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly.
JIN has already boarded the train.<PARAGRAPH>

Thanks again. 
```

### 0x955c4a — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x955cad (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x955bcc; command candidate 0x955bca; target 0x955c4a.

```text
<COLOR 08>JIN: (sigh) You did good
today, {PLAYER}.<PARAGRAPH>

Hopfully i’ll see you around
VALENCIA ISLAND at some point.
```

### 0x955cbc — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x955db8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x955ba0; command candidate 0x955b9e; target 0x955cbc.

```text
<COLOR 08>OFFICER: Oh wow! You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly.
JIN has already boarded the train.<PARAGRAPH>

Thanks again. 
```

### 0x9560ae — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x95611e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x956030; command candidate 0x95602e; target 0x9560ae.

```text
<COLOR 08>JIN: (sigh) You did good today,
{PLAYER}.<PARAGRAPH>

Maybe I’ll see you around VALENCIA
ISLAND at some point.<PARAGRAPH>

Catch ya later.
```

### 0x95612d — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x95621a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x956004; command candidate 0x956002; target 0x95612d.

```text
<COLOR 08>OFFICER: Oh wow!<PARAGRAPH>

You did it!
The engine has started again.<PARAGRAPH>

You and JIN did very well today.<PARAGRAPH>

Thanks to you both, the train can
now make it’s way to VALENCIA<SCROLL>
ISLAND.<PARAGRAPH>

We better board the train quickly.<PARAGRAPH>

Thanks again for your help today. 
```

### 0x95d67f — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x95d6c6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16a074; command candidate 0x16a072; target 0x95d67f.

```text
VIRIDIAN POKéMON GYM
LEADER: BLUE<PARAGRAPH>

WINNING TRAINERS:
AXEL, ZANE, {RIVAL}, {PLAYER}
```

### 0x96823a — Mister G

CONFIRMED_IN_ROM: bytes through 0x9682d9 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
MISTER R: You know we could have
amounted to more than this me and<SCROLL>
my comrades.<PARAGRAPH>

You probably met them in the other
areas of MT. SILVER.<SCROLL>
MISTER G and MISTER H?
```

### 0x9682da — Mister G

CONFIRMED_IN_ROM: bytes through 0x96833c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92ee8b; command candidate 0x92ee89; target 0x9682da.

```text
MISTER G: He took all three of us at
the same time and still won.<PARAGRAPH>

He’s powerful that’s for sure. 
```

### 0x968d35 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x968d81 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x92e287; command candidate 0x92e285; target 0x968d35.

```text
<COLOR 08>Welcome to FAST SHIP S.S.AQUA.<PARAGRAPH>

Would you like travel to VALENCIA
ISLAND?
```

### 0x969854 — Ivy, Orange, Valencia, island

CONFIRMED_IN_ROM: bytes through 0x969bba (exclusive). Boundary: PROVISIONAL_SUFFIX. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x442d5c.

```text
OAK: Ah! There you are {PLAYER}!
It’s good that you could make it.<PARAGRAPH>

I need you to help me out.<PARAGRAPH>

I have a friend called PROF. IVY
who lives out on VALENCIA ISLAND<SCROLL>
which is part of the ORANGE ISLANDS.<PARAGRAPH>

She recently obtained a mysterious
POKé BALL and can’t make head or<SCROLL>
tail of it.<PARAGRAPH>

I agreed to take a look at the BALL
with my scanners but it’s to<SCROLL>
valuable to ship over here and I<SCROLL>
can’t leave this LAB to get it...<PARAGRAPH>

That’s why I need your help.<PARAGRAPH>

You’ve traveled far with your
POKéMON {PLAYER}!<PARAGRAPH>

I would like you to go and fetch the
BALL for me.<PARAGRAPH>

It shouldn’t be a problem for you and
your POKéMON.<PARAGRAPH>

You will need to get your SS.TICKET
stamped to be able to travel to the<SCROLL>
ORANGE ISLANDS.<PARAGRAPH>

Here you go.<PARAGRAPH>

<COLOR 02>PROF.OAK stamps the back of
{PLAYER}’s SS.TICKET!<PARAGRAPH>

<COLOR 08>The boat leaves from VERMILION CITY
only.<PARAGRAPH>

The TRAINERS over in the ORANGE
ISLANDS are quite powerful so you<SCROLL>
better watch your step!<PARAGRAPH>

Good luck!
```

### 0x969f0d — Zane

CONFIRMED_IN_ROM: bytes through 0x969f5e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x969e59; command candidate 0x969e57; target 0x969f0d.

```text
Hmm I better start working on
’the thing’ before MASTER ZANE<SCROLL>
finds out I’m late.
```

### 0x969f5f — Zane

CONFIRMED_IN_ROM: bytes through 0x969f7e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x969ec0; command candidate 0x969eb6; target 0x969f5f.

```text
I should tell ZANE about this.
```

### 0x969f80 — Zane

CONFIRMED_IN_ROM: bytes through 0x969fbc (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x969ec6; command candidate 0x969ec4; target 0x969f80.

```text
Oh well...<PARAGRAPH>

I’m sure ZANE is already aware of
your presence.
```

### 0x96a012 — Zane

CONFIRMED_IN_ROM: bytes through 0x96a040 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x969fcd; command candidate 0x969fcb; target 0x96a012.

```text
Hey no peeking!
This is for ZANE’s eyes only.
```

### 0x96a102 — Zane

CONFIRMED_IN_ROM: bytes through 0x96a149 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x96a0d2; command candidate 0x96a0d0; target 0x96a102.

```text
It’s dangerous for kids to be down
here, especially with ZANE around..
```

### 0x96a18f — Zane

CONFIRMED_IN_ROM: bytes through 0x96a1df (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x96a15a; command candidate 0x96a158; target 0x96a18f.

```text
This place used to be a large
mansion.<PARAGRAPH>

ZANE converted the cellar to a huge
lab.
```

### 0x96a2a2 — Zane

CONFIRMED_IN_ROM: bytes through 0x96a2d4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x96a28f; command candidate 0x96a289; target 0x96a2a2.

```text
I must get this system ready for
ZANE’s big plan.
```

### 0x973311 — Zane

CONFIRMED_IN_ROM: bytes through 0x973384 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x972843; command candidate 0x972841; target 0x973311.
- MSGBOX_SHAPE at operand 0xa23e7d; command candidate 0xa23e7b; target 0x973311.
- Raw/unclassified pointer sites: 0x52dd51.

```text
ZANE: This kid won’t let anyone into
AZALEA TOWN until he gets his POKé<SCROLL>
DOLL back.<PARAGRAPH>

Here, you can make use of this!
```

### 0x974464 — Zane

CONFIRMED_IN_ROM: bytes through 0x9744a4 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
<COLOR 08>MISTER R: Alright then.<PARAGRAPH>

ZANE: Excellent you won’t regret it.
```

### 0x977d1f — Orange, island

CONFIRMED_IN_ROM: bytes through 0x977db4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x977d16; command candidate 0x977d14; target 0x977d1f.
- MSGBOX_SHAPE at operand 0x9d6a59; command candidate 0x9d6a57; target 0x977d1f.

```text
In MEADOW TOWN things are
always peaceful...<PARAGRAPH>

In fact the whole of the ORANGE
ISLANDS is usually peaceful.<PARAGRAPH>

Until these guys arrived a few
weeks ago. 
```

### 0x97aaac — Mister G

CONFIRMED_IN_ROM: bytes through 0x97abeb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x919734; command candidate 0x919732; target 0x97aaac.
- Raw/unclassified pointer sites: 0x97b738.

```text
MISTER R: You know we could have
amounted to more than this me and<SCROLL>
my comrades.<PARAGRAPH>

You probably met them in the other
areas of MT. SILVER.<PARAGRAPH>

MISTER G and MISTER H?<PARAGRAPH>

Why don’t you run along now, RED
could show up any minute, and we<SCROLL>
need to be ready.<PARAGRAPH>

Heh, since you fought the ELITE FOUR
once, why not go and fight them again?
```

### 0x982a6f — Zane

CONFIRMED_IN_ROM: bytes through 0x982adb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x982a3d; command candidate 0x982a3b; target 0x982a6f.
- MSGBOX_SHAPE at operand 0x982c07; command candidate 0x982c05; target 0x982a6f.

```text
<COLOR 08>ZANE: Great battle!<PARAGRAPH>

I’m starting not to mind losing to
you.<PARAGRAPH>

I know that next time we meet you
won’t win.
```

### 0x982af6 — Zane

CONFIRMED_IN_ROM: bytes through 0x982bae (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x982a27; command candidate 0x982a25; target 0x982af6.
- MSGBOX_SHAPE at operand 0x982bda; command candidate 0x982bd8; target 0x982af6.

```text
<COLOR 08>ZANE: Oh!
It’s you!<PARAGRAPH>

I heard there was a legendary TRAINER
somewhere around here.<PARAGRAPH>

I was gonna beat him...
I want a battle!<PARAGRAPH>

I’ve improved since we last met...<PARAGRAPH>

I, ZANE, challenge you!
```

### 0x997b6e — Zane, gym, leader

CONFIRMED_IN_ROM: bytes through 0x997bb1 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x16d1d8; command candidate 0x16d1d6; target 0x997b6e.

```text
CELADON POKéMON GYM
LEADER: ERIKA<PARAGRAPH>

WINNING TRAINERS:
{RIVAL}, AXEL, ZANE
```

### 0x997e34 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x997e83 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
   <COLOR 08>Welcome to FAST SHIP S.S.AQUA.<PARAGRAPH>

Would you like travel to VALENCIA ISLAND?
```

### 0x99c03c — GS Ball

CONFIRMED_IN_ROM: bytes through 0x99c050 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
            GS BALL
```

### 0x9aa791 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9aa7c9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9a447e; command candidate 0x9a447c; target 0x9aa791.
- MSGBOX_SHAPE at operand 0x9a4496; command candidate 0x9a4494; target 0x9aa791.

```text
You really are tough kid...<PARAGRAPH>

Welcome to VALENCIA ISLAND!
```

### 0x9ad021 — Zane

CONFIRMED_IN_ROM: bytes through 0x9ad0b5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x97e0f5; command candidate 0x97e0f3; target 0x9ad021.

```text
<COLOR 08>{RIVAL}: Oh, you brought your friends
along with you, didn’t you?<PARAGRAPH>

No problem, my master-plan will come
true regardless.<PARAGRAPH>

Come on ZANE, let’s move out.
```

### 0x9ad8f9 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9ad934 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 ROUTE 48<PARAGRAPH>

← ESSENCE TOWN
↑ ORIENTAL CITY<SCROLL>
→ PROF. IVY’S LAB
```

### 0x9b33f0 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0x9b34e4 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
<COLOR 08>OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORSOLA and are planning to experiment on them? Thats awful. The leader of this group must be found! You say his name is ZANE? Thank you for your co-operation.
```

### 0x9ba36f — Mister G

CONFIRMED_IN_ROM: bytes through 0x9ba4b0 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
  MISTER R: You know we could have
amounted to more than this me and<SCROLL>
my comrades.<PARAGRAPH>

You probably met them in the other
areas of MT. SILVER.<PARAGRAPH>

MISTER G and MISTER H?<PARAGRAPH>

Why don’t you run along now, RED
could show up any minute, and we<SCROLL>
need to be ready.<PARAGRAPH>

Heh, since you fought the ELITE FOUR
once, why not go and fight them again?
```

### 0x9c294b — Mister G

CONFIRMED_IN_ROM: bytes through 0x9c2972 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x414644.

```text


Linkandzelda
Zeikku
Mister Glitch



```

### 0x9c3e12 — Zane, gym

CONFIRMED_IN_ROM: bytes through 0x9c3e8a (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
  ZANE: Thanks for finding that
kid’s DOLL.<PARAGRAPH>

I wouldn’t of been able to get
to the GYM otherwise!<PARAGRAPH>

I’ll see you later {PLAYER}!
```

### 0x9c7b69 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9c7bb0 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x977db8; command candidate 0x977db6; target 0x9c7b69.

```text
That PROF. IVY is beautiful, I
wouldn’t mind examining her in her<SCROLL>
lab.
```

### 0x9c7d46 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9c7d72 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x984d4f; command candidate 0x984d4d; target 0x9c7d46.
- Raw/unclassified pointer sites: 0x9c7cd7, 0x9c7d33.

```text
The ORANGE ISLANDS are gorgeous
arn’t they?
```

### 0x9cb344 — Champion, League, Orange, gym

CONFIRMED_IN_ROM: bytes through 0x9cb387 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c8fac; command candidate 0x9c8faa; target 0x9cb344.

```text
The ORANGE LEAGUE consists of four
GYMS and a CHAMPION!<PARAGRAPH>

Good luck!
```

### 0x9cb4a4 — Zane

CONFIRMED_IN_ROM: bytes through 0x9cb4fb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c9875; command candidate 0x9c9873; target 0x9cb4a4.

```text
<COLOR 08>{RIVAL}: What happened ZANE?
Did you configure it correctly?<PARAGRAPH>

ZANE, this is unacceptable!
```

### 0x9cb5e7 — Zane

CONFIRMED_IN_ROM: bytes through 0x9cb65c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c98bc; command candidate 0x9c98ba; target 0x9cb5e7.

```text
<COLOR 08>{RIVAL}: Heh!
I should’ve known you would’ve shown<SCROLL>
up again, you meddler!<PARAGRAPH>

You’re too late anyway.
ZANE! We’re leaving.
```

### 0x9cc9b3 — League, Orange, badge, gym, island

CONFIRMED_IN_ROM: bytes through 0x9ccae0 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c8fc0; command candidate 0x9c8fbe; target 0x9cc9b3.
- Raw/unclassified pointer sites: 0x9c8fb5.

```text
<FONT 02>{PLAYER} received the
PLATINUMBADGE!<PAUSE_MUSIC><PLAY_BGM 04 01><PAUSE FE><PAUSE 56><RESUME_MUSIC><PARAGRAPH>

That’s an offical ORANGE ISLANDS
LEAGUE GYM BADGE!<PARAGRAPH>

There are a total of four badges
too collect throughout the ISLANDS!<PARAGRAPH>

The PLATINUMBADGE helps you gain
stronger relationships with your<SCROLL>
POKéMON!<PARAGRAPH>

I know you will go far in the ORANGE
LEAGUE...<PARAGRAPH>

Good luck!
```

### 0x9ccb4f — Ivy

CONFIRMED_IN_ROM: bytes through 0x9ccb9b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c8f58; command candidate 0x9c8f56; target 0x9ccb4f.

```text
<COLOR 04>IVY: Thank you.
This package came faster than I<SCROLL>
expected.<PARAGRAPH>

See you later.
```

### 0x9ccb9d — Ivy

CONFIRMED_IN_ROM: bytes through 0x9ccc7c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9c8f6a; command candidate 0x9c8f68; target 0x9ccb9d.

```text
<COLOR 04>IVY: Who are you?<PARAGRAPH>

{PLAYER}?<PARAGRAPH>

Oh yes!
You’re sent here by PROF. OAK right?<PARAGRAPH>

I’ve been expecting you.<PARAGRAPH>

I have the item ready for you to
take back to PROF. OAK in my LAB.<PARAGRAPH>

Come by there to pick it up.<PARAGRAPH>

It’s on ROUTE 48.<PARAGRAPH>

See you soon!
```

### 0x9cccbd — GS Ball, League, Orange

CONFIRMED_IN_ROM: bytes through 0x9ccd4f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9cccb4; command candidate 0x9cccb2; target 0x9cccbd.
- Raw/unclassified pointer sites: 0x9cb449.

```text
Hello there {PLAYER}!<PARAGRAPH>

I see that you delivered the GS BALL
safely to PROF. OAK!<PARAGRAPH>

Have you returned to compete in the
ORANGE LEAGUE?<PARAGRAPH>

Good luck with that!
```

### 0x9ccd5c — Ivy

CONFIRMED_IN_ROM: bytes through 0x9ccd9c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9ccd53; command candidate 0x9ccd51; target 0x9ccd5c.

```text
IVY: PROF. OAK is waitng.
Hurry up and deliver the BALL to<SCROLL>
him!
```

### 0x9d0f04 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9d0f76 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9ccca6; command candidate 0x9ccca4; target 0x9d0f04.

```text
IVY: PROF. OAK is waiting for that
BALL so I suggest you deliver it to<SCROLL>
him right away.<PARAGRAPH>

Give PROF. OAK my regards!
```

### 0x9d0f8a — Ivy

CONFIRMED_IN_ROM: bytes through 0x9d0fdc (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x99fec2; command candidate 0x99fec0; target 0x9d0f8a.

```text
I’m one of PROF. IVY’S helpers.
I’m doing some research for her at<SCROLL>
the momment...
```

### 0x9d5a78 — GS Ball, Ivy

CONFIRMED_IN_ROM: bytes through 0x9d5b5c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9cb44f; command candidate 0x9cb44d; target 0x9d5a78.
- MSGBOX_SHAPE at operand 0x9ccc92; command candidate 0x9ccc90; target 0x9d5a78.

```text
IVY: There you are!<PARAGRAPH>

PROF. OAK sure did pick a fine lad to
pick up his GS BALL!<PARAGRAPH>

It’s been a while since I had my
hands on one of these...<PARAGRAPH>

The secret of this BALL has yet to
be discovered...<PARAGRAPH>

Well here it is.
Take good care of it!
```

### 0x9d5cf6 — Zane

CONFIRMED_IN_ROM: bytes through 0x9d5d35 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d5cdc; command candidate 0x9d5cda; target 0x9d5cf6.
- MSGBOX_SHAPE at operand 0x9dbc14; command candidate 0x9dbc12; target 0x9d5cf6.
- MSGBOX_SHAPE at operand 0x9dbd27; command candidate 0x9dbd25; target 0x9d5cf6.

```text
<COLOR 08>Mister R: Alright then.<PARAGRAPH>

Zane: Excellent you wont regret
it.
```

### 0x9d5d40 — Zane

CONFIRMED_IN_ROM: bytes through 0x9d5f63 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d5cb3; command candidate 0x9d5cb1; target 0x9d5d40.
- MSGBOX_SHAPE at operand 0x9dbbeb; command candidate 0x9dbbe9; target 0x9d5d40.
- MSGBOX_SHAPE at operand 0x9dbcbd; command candidate 0x9dbcbb; target 0x9d5d40.

```text
<COLOR 08>MISTER R: So er, you’re ZANE are
you?<PARAGRAPH>

Heard you got locked away for
murder.<PARAGRAPH>

ZANE: You heard wrong.<PARAGRAPH>

Now, I hear you gentlemen are the
people to go to for knowing people<SCROLL>
yes?<PARAGRAPH>

MISTER R: That is correct, we’ve
built up many contacts.<PARAGRAPH>

Doesn’t come cheap though.<PARAGRAPH>

ZANE: I understand completely and
will pay you any amount you wish, if<SCROLL>
you work for me.<PARAGRAPH>

MISTER R: Doing what?
We don’t do murder or anything which<SCROLL>
can be proven to be a crime.<PARAGRAPH>

ZANE: You’d just help me get to know
people who I need and be on site to<SCROLL>
handle things.<PARAGRAPH>

So, do we have a deal?
```

### 0x9d5f6e — Mister G

CONFIRMED_IN_ROM: bytes through 0x9d5f87 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d5c9b; command candidate 0x9d5c99; target 0x9d5f6e.
- MSGBOX_SHAPE at operand 0x9dbbd3; command candidate 0x9dbbd1; target 0x9d5f6e.
- MSGBOX_SHAPE at operand 0x9dbca5; command candidate 0x9dbca3; target 0x9d5f6e.

```text
???: Me, Mister G, H, R.
```

### 0x9d5f89 — Mister G

CONFIRMED_IN_ROM: bytes through 0x9d5ffb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d5c90; command candidate 0x9d5c8e; target 0x9d5f89.
- MSGBOX_SHAPE at operand 0x9dbbc8; command candidate 0x9dbbc6; target 0x9d5f89.
- MSGBOX_SHAPE at operand 0x9dbc9a; command candidate 0x9dbc98; target 0x9d5f89.

```text
<COLOR 08>MISTER H: ...Hello friends...<PARAGRAPH>

Mister G: Still moody as always.<PARAGRAPH>

Right, do either of you know who
we’re meeting?
```

### 0x9d6003 — Mister G

CONFIRMED_IN_ROM: bytes through 0x9d6067 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d5c7e; command candidate 0x9d5c7c; target 0x9d6003.
- MSGBOX_SHAPE at operand 0x9dbbb6; command candidate 0x9dbbb4; target 0x9d6003.
- MSGBOX_SHAPE at operand 0x9dbc88; command candidate 0x9dbc86; target 0x9d6003.

```text
<COLOR 08>MISTER G: Good to see you again R.<PARAGRAPH>

MISTER R: You too.<PARAGRAPH>

Seen H?<PARAGRAPH>

MISTER G: I think he’s coming now.
```

### 0x9d614e — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9d619f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9a92e7; command candidate 0x9a92e5; target 0x9d614e.

```text
The ORANGE ISLANDS are so
peaceful...<PARAGRAPH>

That’s why I came here in the first
place!
```

### 0x9d69b8 — GS Ball, League, Orange

CONFIRMED_IN_ROM: bytes through 0x9d6a56 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d60f6; command candidate 0x9d60f4; target 0x9d69b8.
- MSGBOX_SHAPE at operand 0xb123d8; command candidate 0xb123d6; target 0x9d69b8.

```text
OAK: Hello {PLAYER}.
Good of you to stop by.<PARAGRAPH>

The research on the GS BALL is going
to take a while.<PARAGRAPH>

In the mean time why don’t you take
the ORANGE LEAGUE challenge?
```

### 0x9d6aa1 — Ivy

CONFIRMED_IN_ROM: bytes through 0x9d6b0e (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 TRAINER TIPS<PARAGRAPH>

Have you come to meet PROF. IVY?
Her lab is located down from here,<SCROLL>
and up the mountain path. 
```

### 0x9d6b53 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9d6be2 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 TRAINER TIPS<PARAGRAPH>

While in the ORANGE ISLANDS you
may experience some strong
currents.<PARAGRAPH>

Therfore you will need a strong
POKéMON to be able to SURF.
```

### 0x9d6c31 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9d6ca2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x936ace; command candidate 0x936acc; target 0x9d6c31.

```text
This is one of POKéMON CENTERS in the
ORANGE ISLANDS.<PARAGRAPH>

It’s nothing compared to the one in
LEAF BAY CITY, though.
```

### 0x9d6ceb — Ivy

CONFIRMED_IN_ROM: bytes through 0x9d6d23 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9692bd; command candidate 0x9692bb; target 0x9d6ceb.

```text
ROUTE 47<PARAGRAPH>

↑ MEADOW TOWN
← ESSENCE TOWN<SCROLL>
→ PROF. IVY’S LAB
```

### 0x9d93a2 — Valencia, island

CONFIRMED_IN_ROM: bytes through 0x9d9421 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d939a; command candidate 0x9d9398; target 0x9d93a2.

```text
It was nice seeing you again.<PARAGRAPH>

You should check out VALENCIA ISLAND
and explore everywhere.<PARAGRAPH>

You never know what you might find.
```

### 0x9d9423 — League, Orange, gym, island

CONFIRMED_IN_ROM: bytes through 0x9d95e4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d938d; command candidate 0x9d938b; target 0x9d9423.

```text
Ah!
Well if it isn’t {PLAYER}!<PARAGRAPH>

I knew we would meet again sometime.<PARAGRAPH>

Thanks again for the help back on
UNDERSEA EXPRESS.<PARAGRAPH>

I truly enjoyed watching you fight
that KYOGRE.<PARAGRAPH>

You see, the GYM next to this house
used to be my GYM.<PARAGRAPH>

But they threw me off the ORANGE
LEAGUE and brought on some newbie.<PARAGRAPH>

I would go over to SUNBURST ISLAND
and teach him a lesson.<PARAGRAPH>

Too bad I can’t be bothered...<PARAGRAPH>

It’s good to see you are doing good,
{PLAYER}.<PARAGRAPH>

Perhaps we can catchup sometime.
```

### 0x9d9e54 — Zane

CONFIRMED_IN_ROM: bytes through 0x9d9e95 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9dbce6; command candidate 0x9dbce4; target 0x9d9e54.
- Raw/unclassified pointer sites: 0x303b74.

```text
<COLOR 08>MISTER R: Alright then.<PARAGRAPH>

ZANE: Excellent! You won’t regret it.
```

### 0x9db7a0 — Orange, island

CONFIRMED_IN_ROM: bytes through 0x9db93c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8e935c; command candidate 0x8e935a; target 0x9db7a0.

```text
<COLOR 08>OFFICER: What do you mean you’re
closing the contest down?<PARAGRAPH>

???: Because I’m the new PARK WARDEN
and I said I’m closing the contest<SCROLL>
down.<PARAGRAPH>

OFFICER: But you can’t do that!<PARAGRAPH>

The contests have been going for
years without problems.<PARAGRAPH>

WARDEN: It’s the other WARDEN’S
fault for moving to the ORANGE<SCROLL>
ISLANDS.<PARAGRAPH>

He should have known this would
happen.<PARAGRAPH>

Now if you’ll please excuse me.<PARAGRAPH>

I don’t have time for this
nonsense...
```

### 0x9db93d — Nexus

CONFIRMED_IN_ROM: bytes through 0x9db992 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x9d34bc; command candidate 0x9d34b6; target 0x9db93d.

```text
Hey!
You there!<PARAGRAPH>

Which do you think is cooler?
TEAM NEXUS’s uniform or TEAM<SCROLL>
SATURN’s?
```

### 0x9e0105 — Zane

CONFIRMED_IN_ROM: bytes through 0x9e0148 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e00c9; command candidate 0x9e00c7; target 0x9e0105.

```text
<COLOR 08>ZANE: Capture every last one of
them...<PARAGRAPH>

Don’t let any get away!
```

### 0x9e014a — Zane

CONFIRMED_IN_ROM: bytes through 0x9e04aa (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e00de; command candidate 0x9e00dc; target 0x9e014a.
- Raw/unclassified pointer sites: 0x9e1d37, 0xe5a060, 0x9edf69.

```text
<COLOR 08>ZANE: Oh, it’s you!<PARAGRAPH>

I had a feeling you would reach
me here...<PARAGRAPH>

Well im not interested
in battling you here today as I<SCROLL>
have much more important plans.<PARAGRAPH>

I have changed {PLAYER}...
I have become more evil towards<SCROLL>
people and POKéMON...<PARAGRAPH>

...<PARAGRAPH>

...<PARAGRAPH>

What?...<PARAGRAPH>

I’m guessing you want to
know why im here with these men?<PARAGRAPH>

Ok i’ll tell you.<PARAGRAPH>

Im here to capture some CORSOLA
for me and my new group.<PARAGRAPH>

Thats right, I’ve
formed my own criminal<SCROLL>
organisation... TEAM TEILIGHT!<PARAGRAPH>

With the new evil scientists that
work for me, I can create a<SCROLL>
special potion for POKéMON.<PARAGRAPH>

This potion will make a
POKéMON instantly grow 5 levels.<PARAGRAPH>

The liquid that is contained
inside CORSOLA’s branches is what<SCROLL>
is needed to make it...<PARAGRAPH>

When a CORSOLA’s branch breaks, it
grows back in just one night.<PARAGRAPH>

Well im done talking to you for
now.<PARAGRAPH>

My men have grabbed enough CORSOLA
to make 9001 potions.<PARAGRAPH>

Just try to stop us!
```

### 0x9e04f2 — Zane

CONFIRMED_IN_ROM: bytes through 0x9e0535 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x950211; command candidate 0x95020f; target 0x9e04f2.
- MSGBOX_SHAPE at operand 0x9e04b6; command candidate 0x9e04b4; target 0x9e04f2.

```text
<COLOR 08>ZANE: Capture every last one of
them...<PARAGRAPH>

Don’t let any get away!
```

### 0x9e0537 — Nexus, Zane

CONFIRMED_IN_ROM: bytes through 0x9e0878 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x950226; command candidate 0x950224; target 0x9e0537.
- MSGBOX_SHAPE at operand 0x9e04cb; command candidate 0x9e04c9; target 0x9e0537.
- Raw/unclassified pointer sites: 0x89deb, 0x7efd7, 0x14d56b.

```text
<COLOR 08>ZANE: Oh, it’s you!<PARAGRAPH>

I had a feeling you would reach me..<PARAGRAPH>

Well I’m not interested in battling
you here today as I have much more<SCROLL>
important plans.<PARAGRAPH>

I have changed {PLAYER}...
I have become more evil towards<SCROLL>
people and POKéMON since I joined<SCROLL>
TEAM ROCKET.<PARAGRAPH>

{RIVAL}, that fool, inspired me to
do something..<PARAGRAPH>

TEAM NEXUS!<PARAGRAPH>

I’m here to capture some CORSOLA
for me and TEAM NEXUS.<PARAGRAPH>

That’s right, I’ve formed my own
criminal organisation.<PARAGRAPH>

TEAM NEXUS!<PARAGRAPH>

With the new evil scientists that
work for me, I can create anything<SCROLL>
for POKéMON.<PARAGRAPH>

Like a POTION that will make a
POKéMON instantly grow 5 levels.<PARAGRAPH>

The liquid that is contained inside
CORSOLA’s branches is what is needed<SCROLL>
to make it...<PARAGRAPH>

When a CORSOLA’s branch breaks, it
grows back in just one night.<PARAGRAPH>

Well I’m done with you now.<PARAGRAPH>

My men have grabbed enough CORSOLA
to make 9000 potions.<PARAGRAPH>

Just try to stop us!
```

### 0x9e1d59 — Zane

CONFIRMED_IN_ROM: bytes through 0x9e1da3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9db37f; command candidate 0x9db37d; target 0x9e1d59.

```text
I need to improve the formulea
before MASTER ZANE can make use<SCROLL>
of this...
```

### 0x9e25ab — Mister G

CONFIRMED_IN_ROM: bytes through 0x9e25de (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e24de; command candidate 0x9e24dc; target 0x9e25ab.

```text
<COLOR 08>MISTER G: ...I’m sorry It has to be
this way...
```

### 0x9e25fa — Mister G

CONFIRMED_IN_ROM: bytes through 0x9e2621 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e24b5; command candidate 0x9e24b3; target 0x9e25fa.

```text
<COLOR 08>MISTER G: Just give up...
He won’t.
```

### 0x9e267c — Mister Z

CONFIRMED_IN_ROM: bytes through 0x9e2735 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e22cb; command candidate 0x9e22c9; target 0x9e267c.
- MSGBOX_SHAPE at operand 0x9e2464; command candidate 0x9e2462; target 0x9e267c.
- MSGBOX_SHAPE at operand 0x9e227f; command candidate 0x9e227d; target 0x9e2730 (interior target).
- Raw/unclassified pointer sites: 0x9e2a7c, 0x9e228b, 0x9e2298, 0x9e229f, 0x9e234a, 0x9e22bb, 0x9e22c2, 0x9e22a6, 0x9e22ad, 0x9e22b4.

```text
<COLOR 08>MISTER Z: You are too late,
meddler.<PARAGRAPH>

This isn’t some heroes tale where
you hear all of my plan and arrive<SCROLL>
just in time to stop me.<PARAGRAPH>

It has already started, so I wash
my hands of you.
```

### 0x9e278a — Mister Z

CONFIRMED_IN_ROM: bytes through 0x9e2830 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e23df; command candidate 0x9e23dd; target 0x9e278a.

```text
<COLOR 08>MISTER Z: Yes thank you.<PARAGRAPH>

Ahem, in front of you are the
individual parts for the operation<SCROLL>
detailing what each of<SCROLL>
you will do.<PARAGRAPH>

We move out right now, so get to it.
```

### 0x9e283e — Mister Z

CONFIRMED_IN_ROM: bytes through 0x9e2886 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9e2393; command candidate 0x9e2391; target 0x9e283e.

```text
<COLOR 08>MISTER R: Alright settle down,
MISTER Z would like to say something.
```

### 0x9e2b2d — Champion, GS Ball, Ivy, League, Orange, gym

CONFIRMED_IN_ROM: bytes through 0x9e2dfe (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9d60e3; command candidate 0x9d60e1; target 0x9e2b2d.
- Raw/unclassified pointer sites: 0x2550d7.

```text
OAK: Ah you have returned!<PARAGRAPH>

I see you brought the GS BALL with
you.<PARAGRAPH>

Well done {PLAYER}!
I knew you could do it.<PARAGRAPH>

Let me take it from you...<PARAGRAPH>

<COLOR 02>{PLAYER} handed the GS BALL to
PROF. OAK.<PARAGRAPH>

<COLOR 08>This is most intresting!<PARAGRAPH>

I have seen one of these before.<PARAGRAPH>

It was about three years ago now...<PARAGRAPH>

I wasn’t able to figure anything out!<PARAGRAPH>

But as soon as I got word that
PROF. IVY had obtained yet another<SCROLL>
GS BALL I thought I would have<SCROLL>
another crack at it.<PARAGRAPH>

Thanks again for bringing me this.
I’ll need some time to work...<PARAGRAPH>

Hey! I know!<PARAGRAPH>

While I’m working on this why don’t
you enter into the ORANGE LEAGUE!<PARAGRAPH>

It’s similar to the JOHTO and KANTO
LEAGUE but consists of only four<SCROLL>
GYMS and a CHAMPION!<PARAGRAPH>

I think you would do really well in
the ORANGE LEAGUE {PLAYER}!
```

### 0x9eea72 — Zane

CONFIRMED_IN_ROM: bytes through 0x9eea7f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9ee855; command candidate 0x9ee853; target 0x9eea72.

```text
<COLOR 08>ZANE: ...
```

### 0x9eea81 — Zane

CONFIRMED_IN_ROM: bytes through 0x9eea9e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9ee867; command candidate 0x9ee865; target 0x9eea81.

```text
<COLOR 08>ZANE: No {RIVAL}, it’s a fail.
```

### 0x9eeae3 — Zane

CONFIRMED_IN_ROM: bytes through 0x9eeb42 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9f2556; command candidate 0x9f2554; target 0x9eeae3.

```text
<COLOR 08>{RIVAL}: This time, {PLAYER}, you
will not interfere.<PARAGRAPH>

ZANE, control the bird while I take
care of him!
```

### 0x9f0daf — Mandarin, island

CONFIRMED_IN_ROM: bytes through 0x9f0de7 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9f0da6; command candidate 0x9f0da4; target 0x9f0daf.

```text
Route 58<PARAGRAPH>

↑ Mandarin City
← Sunburst Island via Route 57
```

### 0x9f15a5 — Nexus

CONFIRMED_IN_ROM: bytes through 0x9f15f9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x9f156a; command candidate 0x9f1564; target 0x9f15a5.
- TRAINER_TEXT_SHAPE at operand 0x9f1592; command candidate 0x9f158c; target 0x9f15a5.

```text
You have some brass to mess with
Team Nexus!<PARAGRAPH>

Hey, wait a sec!
You have the G Rank!?
```

### 0x9f3887 — Mandarin

CONFIRMED_IN_ROM: bytes through 0x9f38b4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9f3873; command candidate 0x9f3871; target 0x9f3887.
- MSGBOX_SHAPE at operand 0x9f387e; command candidate 0x9f387c; target 0x9f3887.

```text
Hello, welcome to Mandarin City Dept.
Store.
```

### 0x9f3d4b — Mandarin, gym

CONFIRMED_IN_ROM: bytes through 0x9f3d65 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9f3d2d; command candidate 0x9f3d2b; target 0x9f3d4b.
- MSGBOX_SHAPE at operand 0x9f3d3a; command candidate 0x9f3d38; target 0x9f3d4b.

```text
Mandarin City Pokémon Gym
```

### 0x9f3d67 — Rudy, leader

CONFIRMED_IN_ROM: bytes through 0x9f3d89 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9f3d42; command candidate 0x9f3d40; target 0x9f3d67.

```text
Leader: Rudy<PARAGRAPH>

Winning Trainers:
{PLAYER}
```

### 0x9f423a — Nexus

CONFIRMED_IN_ROM: bytes through 0x9f4259 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x9f41ff; command candidate 0x9f41f9; target 0x9f423a.
- TRAINER_TEXT_SHAPE at operand 0x9f4227; command candidate 0x9f4221; target 0x9f423a.

```text
Defeat Team Nexus? Fat chance!
```

### 0xa0884d — Zane

CONFIRMED_IN_ROM: bytes through 0xa088b2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa054c0; command candidate 0xa054be; target 0xa0884d.

```text
<COLOR 08>ZANE: ... {PLAYER}... I’m sorry...
I didn’t mean to...<PARAGRAPH>

This wasn’t supposed to...
Please...<PARAGRAPH>

Use this...
```

### 0xa088b4 — Zane

CONFIRMED_IN_ROM: bytes through 0xa088e9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa0549e; command candidate 0xa0549c; target 0xa088b4.

```text
ZANE gets attacked by HYPER BEAM,
and falls near {PLAYER}.
```

### 0xa08ac8 — Zane

CONFIRMED_IN_ROM: bytes through 0xa08c5b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa0547c; command candidate 0xa0547a; target 0xa08ac8.

```text
<COLOR 08>ZANE: I started being against you
from the point you tortured the<SCROLL>
birds just to test our technology...<PARAGRAPH>

The technology was a fail, and yet
you still went on.<PARAGRAPH>

Then, you decided to take control of
the REGIS, and now GROUDON in this<SCROLL>
very dungeon...<PARAGRAPH>

You attacked your own father, even
if he came because he cared about<SCROLL>
you...<PARAGRAPH>

And now, you refuse to give up when
there is nothing left.<PARAGRAPH>

THIS IS ENOUGH, {RIVAL}!
```

### 0xa0afc6 — Zane

CONFIRMED_IN_ROM: bytes through 0xa0b102 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa05462; command candidate 0xa05460; target 0xa0afc6.

```text
<COLOR 08>ZANE: THAT’S ENOUGH!<PARAGRAPH>

{RIVAL}: What made ya so irritated
all of a sudden?<PARAGRAPH>

ZANE: You did!
I did not join TEAM ROCKET for this!<PARAGRAPH>

I joined because I wanted to be
powerful, because I wanted to beat<SCROLL>
{PLAYER}.<PARAGRAPH>

Not because I wanted to watch you
mistreat POKéMON!<PARAGRAPH>

POKéMON are my friends, but to you
they are nothing but tools of war!
```

### 0xa0b112 — Zane

CONFIRMED_IN_ROM: bytes through 0xa0b133 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa0543e; command candidate 0xa0543c; target 0xa0b112.

```text
<COLOR 08>ZANE: ... That’s... Enough...
```

### 0xa0e791 — Zane

CONFIRMED_IN_ROM: bytes through 0xa0e79e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa05400; command candidate 0xa053fe; target 0xa0e791.

```text
<COLOR 08>ZANE: ...
```

### 0xa13d94 — Orange, island

CONFIRMED_IN_ROM: bytes through 0xa13dde (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa13d41; command candidate 0xa13d3f; target 0xa13d94.
- MSGBOX_SHAPE at operand 0xa13d59; command candidate 0xa13d57; target 0xa13d94.

```text
If you come to the ORANGE ISLANDS
then you better be prepared for<SCROLL>
battle!
```

### 0xa13fb2 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa13ff3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0x9aa029; command candidate 0x9aa023; target 0xa13fb2.

```text
I haven’t seen you around here
before...<PARAGRAPH>

Are you a NEXUS MEMBER?
```

### 0xa142bd — Zane, leader

CONFIRMED_IN_ROM: bytes through 0xa143b2 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 <COLOR 08>OFFICER: Thank you for
getting rid of those gang<SCROLL>
members. What?!? They took some<SCROLL>
CORSOLA and are planning to<SCROLL>
experiment on them? Thats awful.<SCROLL>
The leader of this group must be<SCROLL>
found! You say his name is ZANE?<SCROLL>
Thank you for your co-operation.
```

### 0xa143b3 — Zane, leader

CONFIRMED_IN_ROM: bytes through 0xa144a1 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x950254; command candidate 0x950252; target 0xa143b3.

```text
<COLOR 08>OFFICER: Thank you for getting rid
of those men.<PARAGRAPH>

What?!
They took some CORSOLA and are<SCROLL>
planning to experiment on them?<PARAGRAPH>

That’s criminal!<PARAGRAPH>

The leader of this group must be
found!<PARAGRAPH>

You say his name is ZANE?
Thank you for your co-operation.
```

### 0xa175e4 — Valencia

CONFIRMED_IN_ROM: bytes through 0xa175f2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8b7c.

```text
VALENCIA PORT
```

### 0xa24a9a — Sandway

CONFIRMED_IN_ROM: bytes through 0xa24ac3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa24a86; command candidate 0xa24a84; target 0xa24a9a.
- MSGBOX_SHAPE at operand 0xa24a91; command candidate 0xa24a8f; target 0xa24a9a.

```text
Route 53<PARAGRAPH>

↑ West Vale Port
→ Sandway Town
```

### 0xa2560a — Nexus

CONFIRMED_IN_ROM: bytes through 0xa25648 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa255f6; command candidate 0xa255f4; target 0xa2560a.
- MSGBOX_SHAPE at operand 0xa25601; command candidate 0xa255ff; target 0xa2560a.

```text
Aban-<PARAGRAPH>

It’s scratched off and replaced with
”Nexus Laboratory”
```

### 0xa258f4 — Sandway

CONFIRMED_IN_ROM: bytes through 0xa25925 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa258e0; command candidate 0xa258de; target 0xa258f4.
- MSGBOX_SHAPE at operand 0xa258eb; command candidate 0xa258e9; target 0xa258f4.

```text
Sandway Town<PARAGRAPH>

Where The Future Is Not So Far Away
```

### 0xa3543f — Ivy

CONFIRMED_IN_ROM: bytes through 0xa354ac (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9a72e1; command candidate 0x9a72df; target 0xa3543f.

```text
TRAINER TIPS<PARAGRAPH>

Have you come to meet PROF. IVY?
Her lab is located South from here,<SCROLL>
and up the mountain path. 
```

### 0xa3b0eb — Orange, island

CONFIRMED_IN_ROM: bytes through 0xa3b17a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x9a892a; command candidate 0x9a8928; target 0xa3b0eb.

```text
TRAINER TIPS<PARAGRAPH>

While in the ORANGE ISLANDS you
may experience some strong<SCROLL>
currents.<PARAGRAPH>

Therefore you will need a strong
POKéMON to be able to SURF.
```

### 0xa5fe7c — Mister G

CONFIRMED_IN_ROM: bytes through 0xa5fed7 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa5fe60; command candidate 0xa5fe5e; target 0xa5fe7c.

```text
<COLOR 08>Mister G: You’ve got no chance of
winning against me, whenever that<SCROLL>
time comes, hehe...
```

### 0xa5fedc — Mister G, island

CONFIRMED_IN_ROM: bytes through 0xa5ffb8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa5fe4e; command candidate 0xa5fe4c; target 0xa5fedc.

```text
<COLOR 08>Mister G: So you’re the one who’s
been trespassing on my property.<PARAGRAPH>

I’m Mister G, the new ruler of this
Island.<PARAGRAPH>

What was that?<PARAGRAPH>

How dare you speak to me like that,
you medler!<PARAGRAPH>

Oh, whatever...
My job here is done, ciao!
```

### 0xa7149f — Mandarin, island

CONFIRMED_IN_ROM: bytes through 0xa714fc (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa71464; command candidate 0xa7145e; target 0xa7149f.
- TRAINER_TEXT_SHAPE at operand 0xa7148c; command candidate 0xa71486; target 0xa7149f.

```text
I came from Mandarin Island, just
east of here.<PARAGRAPH>

Would you like to battle before I
head back?
```

### 0xa745ed — Mister Z

CONFIRMED_IN_ROM: bytes through 0xa74669 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa74565; command candidate 0xa74563; target 0xa745ed.
- MSGBOX_SHAPE at operand 0xa7457d; command candidate 0xa7457b; target 0xa745ed.

```text
This is nonsense!<PARAGRAPH>

Why can’t we be stronger and
stronger already?!<PARAGRAPH>

Oh well, I’ll wait for Mister Z to
finish his grand plan!
```

### 0xa7fd92 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa7fde6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa77b09; command candidate 0xa77b03; target 0xa7fd92.
- TRAINER_TEXT_SHAPE at operand 0xa7b414; command candidate 0xa7b40e; target 0xa7fd92.

```text
H-hey you!<PARAGRAPH>

You don’t have a Team Nexus uniform
on you, are you supposed to be here?
```

### 0xa8ebf9 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa8ec40 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa5df2b; command candidate 0xa5df29; target 0xa8ebf9.

```text
The Nexus One is running stable.<PARAGRAPH>

There’s no way it can be stopped now!
```

### 0xa8ec41 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa8ecf8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa60172; command candidate 0xa60170; target 0xa8ec41.

```text
If you try and stop the Nexus One,
the machine upstairs, it’s built to<SCROLL>
mailfunction and destroy itself,<SCROLL>
along with you.<PARAGRAPH>

But, even if you’re able to stop
it, it won’t have any effect!
```

### 0xa8edf2 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa8ee1f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa8edb7; command candidate 0xa8edb1; target 0xa8edf2.
- TRAINER_TEXT_SHAPE at operand 0xa8eddf; command candidate 0xa8edd9; target 0xa8edf2.

```text
You were wrong to mess with Team
Nexus, kid!
```

### 0xa96d00 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa96d57 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa96c9c; command candidate 0xa96c9a; target 0xa96d00.
- MSGBOX_SHAPE at operand 0xa96cb4; command candidate 0xa96cb2; target 0xa96d00.

```text
Team Nexus isn’t about to give up
just because of you.<PARAGRAPH>

The Nexus 4 will never give up.
```

### 0xa96e40 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa96e6d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa96e05; command candidate 0xa96dff; target 0xa96e40.
- TRAINER_TEXT_SHAPE at operand 0xa96e2d; command candidate 0xa96e27; target 0xa96e40.

```text
You have some brass to mess with
Team Nexus!
```

### 0xa9802b — Mister G, Mister Z, Nexus

CONFIRMED_IN_ROM: bytes through 0xa980bf (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa97ff5; command candidate 0xa97ff3; target 0xa9802b.
- MSGBOX_SHAPE at operand 0xa96fe0; command candidate 0xa96fde; target 0xa98093 (interior target).
- Raw/unclassified pointer sites: 0xa96ffb, 0xa97002, 0xa9700c, 0xa97013.

```text
<COLOR 08>Mister G: If only Red accepted our
offer back then, this would never be<SCROLL>
a bother.<PARAGRAPH>

I must do what’s best for the Nexus 4
and Mister Z, as agreed.
```

### 0xa980c1 — Mister G

CONFIRMED_IN_ROM: bytes through 0xa98132 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa97fe0; command candidate 0xa97fde; target 0xa980c1.

```text
<COLOR 08>Mister G: It’s time, you had been
warned and did not heed my warning.<PARAGRAPH>

I’ll be waiting for, us to finish
this.
```

### 0xa9822a — Mister G

CONFIRMED_IN_ROM: bytes through 0xa9823d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa98221; command candidate 0xa9821f; target 0xa9822a.

```text
Mister G’s Office.
```

### 0xa982c7 — Mister G, Mister Z, Nexus

CONFIRMED_IN_ROM: bytes through 0xa9835b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa96ff2; command candidate 0xa96ff0; target 0xa982c7.
- MSGBOX_SHAPE at operand 0xa981d7; command candidate 0xa981d5; target 0xa982c7.

```text
<COLOR 08>Mister G: If only Red accepted our
offer back then, this would never be<SCROLL>
a bother.<PARAGRAPH>

I must do what’s best for the Nexus 4
and Mister Z, as agreed.
```

### 0xa9b0a4 — GS Ball, Ivy

CONFIRMED_IN_ROM: bytes through 0xa9b239 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb12531; command candidate 0xb1252f; target 0xa9b0a4.

```text
Ah, {PLAYER}, good of you to stop by.<PARAGRAPH>

Let’s get right to it, shall we?<PARAGRAPH>

The GS Ball you gave to me from
Prof. Ivy, I’ve been unable to<SCROLL>
uncover any new data about the ball.<PARAGRAPH>

It just seems to not want to do
anything special...<PARAGRAPH>

I’d like to return the Ball to you,
and ask that you deliver it to Kurt<SCROLL>
in Azalea Town in Johto.<PARAGRAPH>

He’s an expert on Poké Balls, so if
anyone would know about the GS Ball,<SCROLL>
it would be Kurt.
```

### 0xa9b5ba — Mandarin

CONFIRMED_IN_ROM: bytes through 0xa9b5e6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9b5b1; command candidate 0xa9b5af; target 0xa9b5ba.

```text
Welcome to Mandarin City Police
Department.
```

### 0xa9b695 — Mandarin, Warehouse, island

CONFIRMED_IN_ROM: bytes through 0xa9b6f7 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x3de004, 0x99c088.

```text
A rusty, old looking key for the
Old Warehouse on Mandarin Island.
Looks untouched for centuries.
```

### 0xa9b80d — Science Complex

CONFIRMED_IN_ROM: bytes through 0xa9b876 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9b804; command candidate 0xa9b802; target 0xa9b80d.

```text
My grandpa was going to take me to
the Science Complex, but apparently<SCROLL>
things are dangerous around here.
```

### 0xa9b883 — Route 59, Science Complex

CONFIRMED_IN_ROM: bytes through 0xa9b8b4 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9b87a; command candidate 0xa9b878; target 0xa9b883.

```text
Beyond here is Route 59 and the
Science Complex.
```

### 0xa9bb79 — Champion, Orange, island

CONFIRMED_IN_ROM: bytes through 0xa9bbcc (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9bb3e; command candidate 0xa9bb38; target 0xa9bb79.
- TRAINER_TEXT_SHAPE at operand 0xa9bb66; command candidate 0xa9bb60; target 0xa9bb79.

```text
Overcoming you will bring me one step
closer to being the Orange Islands<SCROLL>
Champion.
```

### 0xa9bbce — Champion, Orange, island

CONFIRMED_IN_ROM: bytes through 0xa9bc15 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9bb42; command candidate 0xa9bb38; target 0xa9bbce.
- TRAINER_TEXT_SHAPE at operand 0xa9bb6a; command candidate 0xa9bb60; target 0xa9bbce.

```text
It seems you are closer to being the
Orange Islands Champion than I...
```

### 0xa9bdc8 — Mandarin, island

CONFIRMED_IN_ROM: bytes through 0xa9be03 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9bd8d; command candidate 0xa9bd87; target 0xa9bdc8.
- TRAINER_TEXT_SHAPE at operand 0xa9bdb5; command candidate 0xa9bdaf; target 0xa9bdc8.

```text
I’ll show you how things are done
here in Mandarin Island!
```

### 0xa9be87 — Mandarin, island

CONFIRMED_IN_ROM: bytes through 0xa9bf02 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9be4c; command candidate 0xa9be46; target 0xa9be87.
- TRAINER_TEXT_SHAPE at operand 0xa9be74; command candidate 0xa9be6e; target 0xa9be87.

```text
I am the winner of the forty-ninth
annual beauty pageant here in<SCROLL>
Mandarin Island!<PARAGRAPH>

You think you stand a chance against
me?
```

### 0xa9c368 — Nexus

CONFIRMED_IN_ROM: bytes through 0xa9c37e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9c32d; command candidate 0xa9c327; target 0xa9c368.
- TRAINER_TEXT_SHAPE at operand 0xa9c355; command candidate 0xa9c34f; target 0xa9c368.

```text
Long live Team Nexus!
```

### 0xa9c42f — Nexus

CONFIRMED_IN_ROM: bytes through 0xa9c451 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xa9c3ce; command candidate 0xa9c3c4; target 0xa9c42f.
- TRAINER_TEXT_SHAPE at operand 0xa9c3f6; command candidate 0xa9c3ec; target 0xa9c42f.

```text
Team Nexus is blasting off again!
```

### 0xa9c482 — Mandarin, Route 59, Route 60, Science Complex, Warehouse

CONFIRMED_IN_ROM: bytes through 0xa9c4c8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9c479; command candidate 0xa9c477; target 0xa9c482.

```text
Route 59<PARAGRAPH>

↓ Mandarin City
→ Science Complex<PARAGRAPH>

↑ Route 60 & Old Warehouse
```

### 0xa9c4d4 — Mandarin, Science Complex

CONFIRMED_IN_ROM: bytes through 0xa9c4f6 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9c4cb; command candidate 0xa9c4c9; target 0xa9c4d4.

```text
← Science Complex
→ Mandarin City
```

### 0xa9c502 — Mandarin, Route 59, Warehouse

CONFIRMED_IN_ROM: bytes through 0xa9c52d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa9c4f9; command candidate 0xa9c4f7; target 0xa9c502.

```text
← Route 59 & Old Warehouse
→ Mandarin City
```

### 0xaa0f50 — Mister G

CONFIRMED_IN_ROM: bytes through 0xaa0fc1 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa981c2; command candidate 0xa981c0; target 0xaa0f50.

```text
<COLOR 08>Mister G: It’s time, you had been
warned and did not heed my warning.<PARAGRAPH>

I’ll be waiting for us, to finish
this.
```

### 0xaa1d8c — Mister G, Nexus

CONFIRMED_IN_ROM: bytes through 0xaa1ed1 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa97f91; command candidate 0xa97f8f; target 0xaa1d8c.

```text
<COLOR 08>Mister G: Well, if it isn’t that
meddler from the Lighthouse.<PARAGRAPH>

You didn’t heed my warning, eh?<PARAGRAPH>

Quite the trouble you are, you know
that?<PARAGRAPH>

Well, good news for us, my boys are
ready to go with the delivery.<PARAGRAPH>

Yes, that’s correct, you’re too
late.<PARAGRAPH>

We’re all done an dusted here.<PARAGRAPH>

Behind me is our very own invention,
the Nexus S!
```

### 0xaa1ed3 — Nexus

CONFIRMED_IN_ROM: bytes through 0xaa1f71 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa97fa3; command candidate 0xa97fa1; target 0xaa1ed3.

```text
<COLOR 08>Go!<PARAGRAPH>

Take the Nexus S to the other base.
They are waiting for the goods.<PARAGRAPH>

As a member of the Nexus 4, I must stay and take care of this little problem here.
```

### 0xaa5dc4 — Mister G, Nexus

CONFIRMED_IN_ROM: bytes through 0xaa5f09 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa98166; command candidate 0xa98164; target 0xaa5dc4.

```text
<COLOR 08>Mister G: Well, if it isn’t that
meddler from the Lighthouse.<PARAGRAPH>

You didn’t heed my warning, eh?<PARAGRAPH>

Quite the trouble you are, you know
that?<PARAGRAPH>

Well, good news for us, my boys are
ready to go with the delivery.<PARAGRAPH>

Yes, that’s correct, you’re too
late.<PARAGRAPH>

We’re all done an dusted here.<PARAGRAPH>

Behind me is our very own invention,
the Nexus S!
```

### 0xaa5f0b — Nexus

CONFIRMED_IN_ROM: bytes through 0xaa5fa9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa98178; command candidate 0xa98176; target 0xaa5f0b.

```text
<COLOR 08>Go!<PARAGRAPH>

Take the Nexus S to the other base.
They are waiting for the goods.<PARAGRAPH>

As a member of the Nexus 4, I must
stay and take care of this little<SCROLL>
problem here.
```

### 0xaaa9dc — Sandway, island

CONFIRMED_IN_ROM: bytes through 0xaaaa7b (exclusive). Boundary: PROVISIONAL_SUFFIX. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0xe1c95f.

```text
It’s a map of Sunburst Island.<PARAGRAPH>

Serveral locations are marked down.<PARAGRAPH>

Route 53, Route 54, Route 55,
Sandway Town.<PARAGRAPH>

A large circle is placed around West
Vale Port.
```

### 0xaaab4c — Nexus, Zane

CONFIRMED_IN_ROM: bytes through 0xaaabab (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa96e95; command candidate 0xa96e93; target 0xaaab4c.

```text
It looks like the full list of Team
Nexus’ plans.<PARAGRAPH>

Inside it says:
”Nice try, sucker!  - Zane.”
```

### 0xaacf4c — Nexus, Zane

CONFIRMED_IN_ROM: bytes through 0xaacfbe (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaab207; command candidate 0xaab205; target 0xaacf4c.

```text
S-sorry, the connection is going, I
didn’t hear your answer.<PARAGRAPH>

So, can you help out by beating Team
Nexus and Zane?
```

### 0xab7cf8 — League, Nexus, Orange, Zane, island

CONFIRMED_IN_ROM: bytes through 0xab7ee9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaaaff4; command candidate 0xaaaff2; target 0xab7cf8.

```text
Axel: Hello, {PLAYER}, are you there?<PARAGRAPH>

It’s Axel.<PARAGRAPH>

I heard you were visiting the Orange
Islands to challenge the Orange<SCROLL>
League.<PARAGRAPH>

Well, I was wondering if you could
help me out again with a problem.<PARAGRAPH>

I’ve got reports of Team Nexus
movements all across the Orange<SCROLL>
Islands.<PARAGRAPH>

Team Nexus is apparently led by Zane
himself!<PARAGRAPH>

This is an issue of utmost
importance, but I’m not allowed to<SCROLL>
deal with it since it’s out of my<SCROLL>
jurisdiction.<PARAGRAPH>

Since you’re there, are you able to
investigate and stop Zane once and<SCROLL>
for all?
```

### 0xab7eeb — Mister G, Mister Z

CONFIRMED_IN_ROM: bytes through 0xab7f50 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaaafd0; command candidate 0xaaafce; target 0xab7eeb.

```text
<COLOR 08>Mister G: I will now take my leave,
but before that I will tell you,<SCROLL>
Mister Z is waiting for you.
```

### 0xabb58a — Commanding Rank, Mister G, Mister Z, Nexus

CONFIRMED_IN_ROM: bytes through 0xabb851 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0xe578ed.

```text
<COLOR 08>Mister G: ...<PARAGRAPH>

You, kid, what’s your name?<PARAGRAPH>

{PLAYER}?<PARAGRAPH>

Hmm, so my suspicions are confirmed.<PARAGRAPH>

You’re the rascal that took out Team
Rocket and Team Saturn, correct?<PARAGRAPH>

I have failed here today, though I
do not regret my actions.<PARAGRAPH>

Becoming a member of Team Nexus and
the Nexus 4, I was able to fulfill<SCROLL>
my duty as originally agreed.<PARAGRAPH>

One of my other orders from Mister Z
was, upon beating me I must step<SCROLL>
down and award my Commanding Rank<SCROLL>
to you.<PARAGRAPH>

A Commanding Rank is a unique item
given to all of the Nexus 4 to show<SCROLL>
they are fit to hold the position.<PARAGRAPH>

This item was designed to work as a
key, to turn off the Nexus One.<PARAGRAPH>

Only a member of the Nexus 4 is able
to disable it.<PARAGRAPH>

With the Commanding Rank keys anyone
can disable them.
```

### 0xabcce8 — Mister G, Mister Z, Nexus, Zane, island

CONFIRMED_IN_ROM: bytes through 0xabcef2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaaafa6; command candidate 0xaaafa4; target 0xabcce8.

```text
<COLOR 08>Mister G: You came, to finish this?<PARAGRAPH>

You look shocked.<PARAGRAPH>

Did you expect to find Zane, Mister Z
here too?<PARAGRAPH>

He’s not on the island, in fact his
current whereabouts are unknown to<SCROLL>
the majority of Team Nexus and<SCROLL>
myself.<PARAGRAPH>

Zane is using facilities like this
one to conduct projects for a grand<SCROLL>
plan of his.<PARAGRAPH>

We have our orders, and we followed
them.<PARAGRAPH>

I was instructed to terminate you on
first contact.<PARAGRAPH>

Instead I decided to lead you here,
into my own Office, to do the deed.<PARAGRAPH>

Prepare yourself, child, for this
will only happen once.
```

### 0xac03a0 — Danny

CONFIRMED_IN_ROM: bytes through 0xac03a6 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Danny
```

### 0xac3320 — Zane

CONFIRMED_IN_ROM: bytes through 0xac3325 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac3370 — Zane

CONFIRMED_IN_ROM: bytes through 0xac3375 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac3398 — Zane

CONFIRMED_IN_ROM: bytes through 0xac339d (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac3410 — Zane

CONFIRMED_IN_ROM: bytes through 0xac3415 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac53a0 — Zane

CONFIRMED_IN_ROM: bytes through 0xac53a5 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac5940 — Danny

CONFIRMED_IN_ROM: bytes through 0xac5946 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Danny
```

### 0xac5dc8 — Zane

CONFIRMED_IN_ROM: bytes through 0xac5dcd (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac5df0 — Zane

CONFIRMED_IN_ROM: bytes through 0xac5df5 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Zane
```

### 0xac8050 — Mister G

CONFIRMED_IN_ROM: bytes through 0xac805b (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
4 Mister G
```

### 0xac8525 — Danny

CONFIRMED_IN_ROM: bytes through 0xac852e (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
<MN> éDanny
```

### 0xad339b — Mister G, Sandway, island

CONFIRMED_IN_ROM: bytes through 0xad344d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xa7fff6; command candidate 0xa7fff4; target 0xad339b.

```text
It’s a map of Sunburst Island.<PARAGRAPH>

Serveral locations are marked down.<PARAGRAPH>

Mister G’s Office, Route 53,
Route 54, Route 55, Sandway Town.<PARAGRAPH>

A large circle is placed around West
Vale Port.
```

### 0xad3bb4 — Nexus

CONFIRMED_IN_ROM: bytes through 0xad3c4f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaeff14; command candidate 0xaeff12; target 0xad3bb4.
- Raw/unclassified pointer sites: 0x8ad0b.

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xad3c54 — Nexus

CONFIRMED_IN_ROM: bytes through 0xad3cad (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xad34ef; command candidate 0xad34ed; target 0xad3c54.

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xad3d04 — Nexus

CONFIRMED_IN_ROM: bytes through 0xad3d3b (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.
```

### 0xad3d3d — Nexus

CONFIRMED_IN_ROM: bytes through 0xad3d6d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xad348d; command candidate 0xad348b; target 0xad3d3d.

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xad4077 — Orange, island

CONFIRMED_IN_ROM: bytes through 0xad40da (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- TRAINER_TEXT_SHAPE at operand 0xad403c; command candidate 0xad4036; target 0xad4077.
- TRAINER_TEXT_SHAPE at operand 0xad4064; command candidate 0xad405e; target 0xad4077.

```text
I came here to be the strongest in
the Orange Islands, and I’ll<SCROLL>
continue that path by beating you!
```

### 0xafc29e — Nexus

CONFIRMED_IN_ROM: bytes through 0xafc309 (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
 Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient in G Rank to activate
System Console.<PARAGRAPH>

Please charge G Rank.
```

### 0xb0019c — Mandarin, Sandway, island

CONFIRMED_IN_ROM: bytes through 0xb001e9 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xab7fd7; command candidate 0xab7fd5; target 0xb0019c.
- Raw/unclassified pointer sites: 0x1e10fb, 0xc5665, 0xc585d, 0xc5a45, 0xc5c1d, 0xc69f3, 0xc6aa3, 0xc6b53, 0x10c4d1, 0xdc60f.

```text
Route 56<PARAGRAPH>

← Sandway Town via Crystal Caves
→ Route 57 - Mandarin Island North
```

### 0xb01831 — Nexus

CONFIRMED_IN_ROM: bytes through 0xb018a2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaeffdc; command candidate 0xaeffda; target 0xb01831.

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### 0xb01952 — Danny, Safari, toboggan

CONFIRMED_IN_ROM: bytes through 0xb01b23 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb0162f; command candidate 0xb0162d; target 0xb01952.

```text
<COLOR 08>Danny: Congratulations {PLAYER},
you made it to the top of<SCROLL>
Mountain Zone.<PARAGRAPH>

Because this is the Safari Zone,
you were unable to use the force<SCROLL>
of your Pokémon in battle.<PARAGRAPH>

Well, then, I guess it’s time to
move on to the next challenge.<PARAGRAPH>

We need to somehow get down from
this mountain, so I prepared some<SCROLL>
materials for you to find to build<SCROLL>
a toboggan.<PARAGRAPH>

There’s 4 Sticks, 1 Silk Scaf and
1 Metal Coat.<PARAGRAPH>

Once you find them, return to me
and we can move on to the next<SCROLL>
challenge.
```

### 0xb01bb0 — Danny

CONFIRMED_IN_ROM: bytes through 0xb01c4f (exclusive). Boundary: PROVISIONAL_SUFFIX. References: NO_ABSOLUTE_POINTER_FOUND. Map/event owner and reachability UNKNOWN.

No absolute pointer found in the ROM for this parsed extent; orphan status unresolved.

```text
’aDanny: Hey, {PLAYER}, you’re back
for another race?<PARAGRAPH>

I hope you listened to what I said
and have improved the bond between<SCROLL>
you and your Pokémon.<PARAGRAPH>

So, are you ready?
```

### 0xb01f94 — Danny, Safari, Sandway, badge, gym, leader

CONFIRMED_IN_ROM: bytes through 0xb02260 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb00440; command candidate 0xb0043e; target 0xb01f94.
- Raw/unclassified pointer sites: 0xdac71.

```text
Hi there kid, I’m Danny, the Gym
Leader of Sandway Town.<PARAGRAPH>

What are you doing in a place like
this?<PARAGRAPH>

...<PARAGRAPH>

I see, so you think you have what
it takes to challenge me to a Gym<SCROLL>
Battle?<PARAGRAPH>

Sorry, but I don’t think you have.<PARAGRAPH>

You won’t give up until you have my
badge?<PARAGRAPH>

I like that dedication.
What’s your name?<PARAGRAPH>

{PLAYER}?<PARAGRAPH>

Ok, then.<PARAGRAPH>

You can challenge me to a Gym
Battle on one condition.<PARAGRAPH>

You have to complete a series of
tests set by me.<PARAGRAPH>

The first test, you have to qualify
to be a challenger by meeting me at<SCROLL>
the top of the Safari Town Mountain<SCROLL>
Zone.<PARAGRAPH>

If you can make it through the Zone
without battling your Pokémon,<SCROLL>
you’ll go on to the next challenge.<PARAGRAPH>

So, then, let the challenges begin.<PARAGRAPH>

I’ll see you at the Mountain Safari
Zone, {PLAYER}.
```

### 0xb07f2a — toboggan

CONFIRMED_IN_ROM: bytes through 0xb07f7d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb02348; command candidate 0xb02346; target 0xb07f2a.

```text
{STR_VAR_1} looks great.<PARAGRAPH>

Now that you have your 3 Pokémon,
we’re going to build a toboggan.
```

### 0xb080d1 — badge, gym, toboggan

CONFIRMED_IN_ROM: bytes through 0xb0820c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb01cab; command candidate 0xb01ca9; target 0xb080d1.
- MSGBOX_SHAPE at operand 0xb12332; command candidate 0xb12330; target 0xb080d1.
- MSGBOX_SHAPE at operand 0xb12491; command candidate 0xb1248f; target 0xb080d1.
- Raw/unclassified pointer sites: 0x11d65, 0x1f685, 0x124a0d, 0x125e4d, 0x159ba9.

```text
For the final challenge, we’re
going to have a race down the<SCROLL>
mountain in our toboggans.<PARAGRAPH>

If you can beat me to the bottom,
I’ll allow you to challenge me to a<SCROLL>
Gym Battle for my badge.<PARAGRAPH>

The key to winning this race is the
bond between you and your Pokémon.<PARAGRAPH>

If you have strong bonds, you will
have a chance at winning.
```

### 0xb0add5 — Sandway, gym

CONFIRMED_IN_ROM: bytes through 0xb0adee (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb02371; command candidate 0xb0236f; target 0xb0add5.
- MSGBOX_SHAPE at operand 0xb0a242; command candidate 0xb0a240; target 0xb0add5.

```text
Sandway Town Pokémon Gym
```

### 0xb0fda0 — toboggan

CONFIRMED_IN_ROM: bytes through 0xb0fe2a (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb01ca0; command candidate 0xb01c9e; target 0xb0fda0.
- MSGBOX_SHAPE at operand 0xb12327; command candidate 0xb12325; target 0xb0fda0.
- MSGBOX_SHAPE at operand 0xb12486; command candidate 0xb12484; target 0xb0fda0.

```text
There, wasn’t that a great way to
bond with your Pokémon?<PARAGRAPH>

You built yourself a toboggan!<PARAGRAPH>

Now, then, let’s move on to the
final challenge!
```

### 0xb0fe2c — Danny, toboggan

CONFIRMED_IN_ROM: bytes through 0xb0ff28 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb01c5c; command candidate 0xb01c5a; target 0xb0fe2c.

```text
Danny: Congratulations again,
{PLAYER}.<PARAGRAPH>

You were able to find all the
materials for the next challenge.<PARAGRAPH>

Now it’s time to build your toboggan.<PARAGRAPH>

For this, you need to have a strong
bond with your Pokémon.<PARAGRAPH>

Please choose 3 Pokémon to help you
build the toboggan.
```

### 0xb0ff2a — Danny

CONFIRMED_IN_ROM: bytes through 0xb0ff90 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb0164e; command candidate 0xb0164c; target 0xb0ff2a.

```text
Danny: Have you gotten all the
materials yet?<PARAGRAPH>

I’ll be waiting here until you manage
to find them all.
```

### 0xb0ffad — Danny, leader

CONFIRMED_IN_ROM: bytes through 0xb0ffd0 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb0a24a; command candidate 0xb0a248; target 0xb0ffad.

```text
Leader: Danny<PARAGRAPH>

Winning Trainers:
{PLAYER}
```

### 0xb1075c — Danny, Sandway, gym

CONFIRMED_IN_ROM: bytes through 0xb1082e (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb018fd; command candidate 0xb018fb; target 0xb1075c.

```text
<COLOR 08>Danny: ... I lost.<PARAGRAPH>

That was a fantastic race {PLAYER}.<PARAGRAPH>

You really showed me how strong
peoples bonds with thier Pokémon<SCROLL>
can become.<PARAGRAPH>

Congratulations for beating me,
I’ll be waiting for you at the<SCROLL>
Sandway Town Gym.
```

### 0xb109a2 — Sandway, gym

CONFIRMED_IN_ROM: bytes through 0xb109bb (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb10984; command candidate 0xb10982; target 0xb109a2.
- MSGBOX_SHAPE at operand 0xb10991; command candidate 0xb1098f; target 0xb109a2.

```text
Sandway Town Pokémon Gym
```

### 0xb11c47 — League, Orange, Sea Ruby, badge, gym, leader

CONFIRMED_IN_ROM: bytes through 0xb11dc3 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb0ffe4; command candidate 0xb0ffe2; target 0xb11c47.

```text
<FONT 02>{PLAYER} received the
Sea Ruby Badge!<PAUSE_MUSIC><PLAY_BGM 04 01><PAUSE FE><PAUSE 56><RESUME_MUSIC><PARAGRAPH>

This battle has shown me, instead of
worrying about other Trainer’s<SCROLL>
bonds, I need to strengthen and<SCROLL>
deepen my own bonds with my Pokémon.<PARAGRAPH>

The Sea Ruby Badge is the second of
the Official Orange League Gym<SCROLL>
Badges.<PARAGRAPH>

You did exceptionally well to earn
this.<PARAGRAPH>

I expect you’ll do fine with the
remaining Orange Gym Leaders.<PARAGRAPH>

Good luck, {PLAYER}.
```

### 0xb11dc4 — Danny, leader

CONFIRMED_IN_ROM: bytes through 0xb11de7 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb10999; command candidate 0xb10997; target 0xb11dc4.

```text
Leader: Danny<PARAGRAPH>

Winning Trainers:
{PLAYER}
```

### 0xb11de8 — Danny, Sandway, gym, leader

CONFIRMED_IN_ROM: bytes through 0xb11e25 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xacac2e; command candidate 0xacac2c; target 0xb11de8.

```text
Sandway Town Pokémon Gym<PARAGRAPH>

Leader: Danny<PARAGRAPH>

The relationship guru
```

### 0xb11e5e — Danny, Safari, toboggan

CONFIRMED_IN_ROM: bytes through 0xb1202f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb11e4f; command candidate 0xb11e4d; target 0xb11e5e.

```text
<COLOR 08>Danny: Congratulations {PLAYER},
you made it to the top of<SCROLL>
Mountain Zone.<PARAGRAPH>

Becuase this is the Safari Zone,
you were unable to use the force<SCROLL>
of your Pokémon in battle.<PARAGRAPH>

Well, then, I guess it’s time to
move on to the next challenge.<PARAGRAPH>

We need to somehow get down from
this mountain, so I prepared some<SCROLL>
materials for you to find to build<SCROLL>
a toboggan.<PARAGRAPH>

There’s 4 Sticks, 1 Silk Scaf and
1 Metal Coat.<PARAGRAPH>

Once you find them, return to me
and we can move on to the next<SCROLL>
challenge.
```

### 0xb12063 — GS Ball, League, Orange, gym, island

CONFIRMED_IN_ROM: bytes through 0xb121a5 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x94f4a9; command candidate 0x94f4a7; target 0xb12063.

```text
OAK: Hello, {PLAYER}?
It’s Prof. Oak.<PARAGRAPH>

How are you doing in the Orange
Islands?<PARAGRAPH>

I just heard you got the 2nd Orange
League Gym Bagde.<PARAGRAPH>

Sounds to me like you’re doing just
fine.<PARAGRAPH>

So, Is there any chance you can
visit me at my Lab sometime?<PARAGRAPH>

I need to speak with you about that
mysterious GS Ball.<PARAGRAPH>

See you soon, {PLAYER}.<PARAGRAPH>

Click
... ... ...
```

### 0xb121a6 — GS Ball, League, Orange, gym, island

CONFIRMED_IN_ROM: bytes through 0xb122e8 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x94f4bf; command candidate 0x94f4bd; target 0xb121a6.

```text
OAK: Hello, {PLAYER}?
It’s Prof. Oak.<PARAGRAPH>

How are you doing in the Orange
Islands?<PARAGRAPH>

I just heard you got the 2nd Orange
League Gym Bagde.<PARAGRAPH>

Sounds to me like you’re doing just
fine.<PARAGRAPH>

So, is there any chance you can
visit me at my Lab sometime?<PARAGRAPH>

I need to speak with you about that
mysterious GS Ball.<PARAGRAPH>

See you soon, {PLAYER}.<PARAGRAPH>

Click
... ... ...
```

### 0xb17310 — Danny, Sandway, gym

CONFIRMED_IN_ROM: bytes through 0xb17450 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb123a7; command candidate 0xb123a5; target 0xb17310.

```text
<COLOR 08>Danny: ... I lost.<PARAGRAPH>

That was a fantastic race {PLAYER}.<PARAGRAPH>

You really showed me how strong
peoples bonds with thier Pokémon<SCROLL>
can become.<PARAGRAPH>

Your {STR_VAR_2} was outstanding.<PARAGRAPH>

I knew there was something about it
when I first saw it.<PARAGRAPH>

It must love you very much.<PARAGRAPH>

Congratulations for beating me,
I’ll be waiting for you at the<SCROLL>
Sandway Town Gym.
```

### 0xb19bb1 — League, Orange

CONFIRMED_IN_ROM: bytes through 0xb19c36 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb12545; command candidate 0xb12543; target 0xb19bb1.

```text
Thanks {PLAYER}, I trust that you
will be able to handle this task.<PARAGRAPH>

So the Orange League is going well
I hear?<PARAGRAPH>

Do stop by some other time.
```

### 0xb1a0e7 — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb1a139 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb12401; command candidate 0xb123ff; target 0xb1a0e7.

```text
<COLOR 08>{PLAYER}, here’s your GS Ball back!<PARAGRAPH>

Could you go see why Ilex Forest is so
restless?
```

### 0xb1a1f4 — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb1a20b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a17e; command candidate 0xb1a17c; target 0xb1a1f4.

```text
{PLAYER} put in the GS Ball.
```

### 0xb1a2cf — League, Orange

CONFIRMED_IN_ROM: bytes through 0xb1a345 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a2c3; command candidate 0xb1a2c1; target 0xb1a2cf.

```text
Hello {PLAYER}, good to see you.<PARAGRAPH>

How is the Orange League going?<PARAGRAPH>

I hope you’re winning your way
through and keeping strong.
```

### 0xb1a347 — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb1a3db (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a2b5; command candidate 0xb1a2b3; target 0xb1a347.

```text
{PLAYER}! Isn’t it amazing?<PARAGRAPH>

The GS Ball turned out to be related
to Ilex Forest and the legendary<SCROLL>
Celebi.<PARAGRAPH>

I knew Kurt had it in him to solve
the mystery!
```

### 0xb1a3dd — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb1a4ac (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a29b; command candidate 0xb1a299; target 0xb1a3dd.

```text
Hi {PLAYER}.
I see you delivered the GS Ball to<SCROLL>
Kurt.<PARAGRAPH>

Does he know what it is yet?<PARAGRAPH>

I see, so he is researching it.<PARAGRAPH>

Let’s give him a day or so to see
what he can do.<PARAGRAPH>

I have faith that Kurt can unlock
it’s secrets.
```

### 0xb1a512 — Danny

CONFIRMED_IN_ROM: bytes through 0xb1a5af (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1256d; command candidate 0xb1256b; target 0xb1a512.

```text
Danny: Hey, {PLAYER}, you’re back
for another race?<PARAGRAPH>

I hope you listened to what I said
and have improved the bond between<SCROLL>
you and your Pokémon.<PARAGRAPH>

So, are you ready?
```

### 0xb1a6de — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb1a78b (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb126f2; command candidate 0xb126f0; target 0xb1a6de.

```text
ILEX FOREST SHRINE...<PARAGRAPH>

It’s in honor of the forest’s
protector...<PARAGRAPH>

Oh?
What is this?<PARAGRAPH>

It’s a hole.<PARAGRAPH>

It looks like the GS Ball would fit
inside it.<PARAGRAPH>

Want to put the GS Ball here?
```

### 0xb1aeb9 — Mandarin, island

CONFIRMED_IN_ROM: bytes through 0xb1af4f (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb08fc2; command candidate 0xb08fc0; target 0xb1aeb9.

```text
The items being sold here are very
high grade items.<PARAGRAPH>

Similar to the things you can get at
the Dept. Store across the waters in<SCROLL>
Mandarin Island North.
```

### 0xb1d4e0 — Commanding Rank, Mister G, Mister Z, Nexus

CONFIRMED_IN_ROM: bytes through 0xb1d7dd (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xaaafbc; command candidate 0xaaafba; target 0xb1d4e0.

```text
<COLOR 08>Mister G: ...<PARAGRAPH>

You, kid, what’s your name?<PARAGRAPH>

{PLAYER}?<PARAGRAPH>

Hmm, so my suspicions are confirmed.<PARAGRAPH>

You’re the rascal that took out Team
Rocket and Team Saturn, correct?<PARAGRAPH>

I have failed here today, though I
do not regret my actions.<PARAGRAPH>

Becoming a member of Team Nexus and
the Nexus 4, I was able to fulfill<SCROLL>
my duty as originally agreed.<PARAGRAPH>

One of my other orders from Mister Z
was, upon beating me I must step<SCROLL>
down and award my Commanding Rank<SCROLL>
to you.<PARAGRAPH>

A Commanding Rank is a unique item
given to all of the Nexus 4 to show<SCROLL>
they are fit to hold the position.<PARAGRAPH>

This item was designed to work as a
key, to turn off the Nexus One.<PARAGRAPH>

Only a member of the Nexus 4 is able
to disable it.<PARAGRAPH>

Just a warning, but they need to be
powered up to be used.<PARAGRAPH>

You can use the machine on the desk
to charge it.
```

### 0xb1d7de — Ivy, Orange, Valencia, island

CONFIRMED_IN_ROM: bytes through 0xb1db9c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x90114a; command candidate 0x901148; target 0xb1d7de.

```text
OAK: Ah! There you are {PLAYER}!
It’s good that you could make it.<PARAGRAPH>

I need you to help me out.<PARAGRAPH>

I have a friend called PROF. IVY
who lives out on VALENCIA ISLAND<SCROLL>
which is part of the ORANGE ISLANDS.<PARAGRAPH>

She recently obtained a mysterious
POKé BALL and can’t make head or<SCROLL>
tail of it.<PARAGRAPH>

I agreed to take a look at the BALL
with my scanners but it’s to<SCROLL>
valuable to ship over here and I<SCROLL>
can’t leave this LAB to get it...<PARAGRAPH>

That’s why I need your help.<PARAGRAPH>

You’ve traveled far with your
POKéMON {PLAYER}!<PARAGRAPH>

I would like you to go and fetch the
BALL for me.<PARAGRAPH>

It shouldn’t be a problem for you and
your POKéMON.<PARAGRAPH>

You will need to get your SS.TICKET
stamped to be able to travel to the<SCROLL>
ORANGE ISLANDS.<PARAGRAPH>

Here you go.<PARAGRAPH>

I’ve spoken to the S.S.Office in
Vermillion City, they will stamp<SCROLL>
your S.S.Ticket for you to be able<SCROLL>
to travel to the Orange Islands via<SCROLL>
the Undersea Express service on<SCROLL>
Route 100.<PARAGRAPH>

The TRAINERS over in the ORANGE
ISLANDS are quite powerful so you<SCROLL>
better watch your step!<PARAGRAPH>

Good luck!
```

### 0xb1dea8 — Zane, gym

CONFIRMED_IN_ROM: bytes through 0xb1df20 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0x8ad543; command candidate 0x8ad541; target 0xb1dea8.

```text
ZANE: Thanks for finding that
kid’s DOLL.<PARAGRAPH>

I wouldn’t have been able to get
to the GYM otherwise!<PARAGRAPH>

I’ll see you later {PLAYER}!
```

### 0xb2922f — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb2928c (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a0dc; command candidate 0xb1a0da; target 0xb2922f.

```text
Hi {PLAYER}, how’s it going?<PARAGRAPH>

Have you delivered that GS Ball yet?<PARAGRAPH>

Say hi to Kurt for me would you?
```

### 0xb2928d — GS Ball

CONFIRMED_IN_ROM: bytes through 0xb2936d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: SCRIPT_OPERAND_SHAPE. Map/event owner and reachability UNKNOWN.

- MSGBOX_SHAPE at operand 0xb1a797; command candidate 0xb1a795; target 0xb2928d.

```text
Kurt: I see, the Ilex Forest has
calmed down.<PARAGRAPH>

It must have involved the Forest’s
Protector.<PARAGRAPH>

I see the GS Ball is gone as well.<PARAGRAPH>

Thank you for calming the forests for
me, {PLAYER}.<PARAGRAPH>

I will continue to make Balls for
you like always.
```

### 0xc04ea4 — Mandarin

CONFIRMED_IN_ROM: bytes through 0xc04eb2 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8be4.

```text
MANDARIN CITY
```

### 0xc05294 — Route 59

CONFIRMED_IN_ROM: bytes through 0xc0529d (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8be8.

```text
ROUTE 59
```

### 0xc05304 — Science Complex

CONFIRMED_IN_ROM: bytes through 0xc05314 (exclusive). Boundary: REFERENCED_PARSEABLE_START. References: RAW_POINTER_ONLY. Map/event owner and reachability UNKNOWN.

- Raw/unclassified pointer sites: 0x2c8bec.

```text
SCIENCE COMPLEX
```

## No-absolute-pointer candidates (not certified orphaned)

- 0x23e830: Nexus
- 0x8c4ef1: rivell: Well if you don’t mind then Were going to have our POKéMON BATTLE. ...................... ..................... ZANE: ..............
- 0x8c52ae: rivell: Well if you don’t mind then Were going to have our POKéMON BATTLE. ...................... ..................... ZANE: ..............
- 0x8e5fbc: CELADON POKéMON GYM LEADER: ERIKA WINNING TRAINERS: {RIVAL}, ZANE, AXEL and {PLAYER}
- 0x9031ae: LEADER: BUGSY WINNING TRAINERS: rival , AXEL, ZANE, {PLAYER}
- 0x90321d: LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x903255: LEADER: JASMINE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x90328f: LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x9032c7: LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x9032ff: LEADER: PRYCE WINNING TRAINERS: {RIVAL} , AXEL, ZANE, {PLAYER}
- 0x90b2da: LEADER: BUGSY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER}
- 0x90b30e: LEADER: WHITNEY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER}
- 0x90b345: LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x90b37e: LEADER: JASMINE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x90b3b9: LEADER: MORTY WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x90b3f2: LEADER: PRYCE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x90b42b: LEADER: CLAIR WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x918e17: MISTER G: Erm... Aha we got you... Oh you’re er not him. Pity. W-well, d-don’t interrupt we’re dealing with an important matter, not for lit
- 0x92ed6e: MISTER R: You know we could have amounted to more than this me and my comrades. You probably met them in the other areas of MT. SILVER. MIST
- 0x9363e6: Watering flowers all day is fun. I love it! Especially becuase this is PROF. IVY’s private garden!
- 0x9393ff: WINNING TRAINERS: AXEL, ZANE, {RIVAL}
- 0x95252c: JIN: (sigh) You did good today, {PLAYER}. Hopfully i’ll see you around VALENCIA ISLAND at some point.
- 0x96823a: MISTER R: You know we could have amounted to more than this me and my comrades. You probably met them in the other areas of MT. SILVER. MIST
- 0x974464: MISTER R: Alright then. ZANE: Excellent you won’t regret it.
- 0x997e34: Welcome to FAST SHIP S.S.AQUA. Would you like travel to VALENCIA ISLAND?
- 0x99c03c: GS BALL
- 0x9ad8f9: ROUTE 48 ← ESSENCE TOWN ↑ ORIENTAL CITY → PROF. IVY’S LAB
- 0x9b33f0: OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORSOLA and are planning to experiment on them? Thats awful
- 0x9ba36f: MISTER R: You know we could have amounted to more than this me and my comrades. You probably met them in the other areas of MT. SILVER. MIST
- 0x9c3e12: ZANE: Thanks for finding that kid’s DOLL. I wouldn’t of been able to get to the GYM otherwise! I’ll see you later {PLAYER}!
- 0x9d6aa1: TRAINER TIPS Have you come to meet PROF. IVY? Her lab is located down from here, and up the mountain path.
- 0x9d6b53: TRAINER TIPS While in the ORANGE ISLANDS you may experience some strong currents. Therfore you will need a strong POKéMON to be able to SURF
- 0xa142bd: OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORSOLA and are planning to experiment on them? Thats awful
- 0xac03a0: Danny
- 0xac3320: Zane
- 0xac3370: Zane
- 0xac3398: Zane
- 0xac3410: Zane
- 0xac53a0: Zane
- 0xac5940: Danny
- 0xac5dc8: Zane
- 0xac5df0: Zane
- 0xac8050: 4 Mister G
- 0xac8525: <MN> éDanny
- 0xad3d04: Nexus One Status: Activated. Global power level: {STR_VAR_1}0%.
- 0xafc29e: Inserting G Rank into Nexus One. Insufficient in G Rank to activate System Console. Please charge G Rank.
- 0xb01bb0: ’aDanny: Hey, {PLAYER}, you’re back for another race? I hope you listened to what I said and have improved the bond between you and your Pok

## Duplicate text candidates

- 0x1914a4, 0x9529d2: PEWTER POKéMON GYM LEADER: BROCK WINNING TRAINERS: {RIVAL}, {PLAYER}
- 0x2791d4, 0x840894, 0x848127, 0x84aafb, 0x8c22ac, 0x8c2686, 0x8c2b32, 0x8cc30b: {PLAYER} received the GLACIERBADGE! That BADGE will raise the SPECIAL stats of POKéMON. It also lets
- 0x80445c, 0x882ec1: I found a good POKéMON in DARK CAVE. I’m going to raise it to take on FALKNER. He’s the leader of VI
- 0x804586, 0x869e2f: FALKNER, from the VIOLET POKéMON GYM, is a fine tainer! He inherited his father’s GYM and has done a
- 0x804685, 0x89f500: Hey, you’re a POKéMON TRAINER? If you beat the GYM LEADER here, you’ll be ready for prime time!
- 0x8049ae, 0x85dfb1, 0x8a4612: Hey! I’m no TRAINER but I can give some advice! Believe me! If you believe, a championship dream can
- 0x804c1a, 0x804fef, 0x8abcec: I’m FALKNER, the VIOLET POKéMON GYM leader! People say you can clip flying-type POKéMON’s wings with
- 0x804d02, 0x8050d7, 0x8abdd4: ...Darn! My dad’s cherished bird POKéMON... All right. Take this. It’s the official POKéMON LEAGUE Z
- 0x804e62, 0x805237, 0x8abf34: There are POKéMON GYMS in cities and towns ahead. You should test your skills at these GYMS. I’m goi
- 0x804efd, 0x8052d2, 0x885851: {PLAYER} received the ZEPHYRBADGE! ZEPHYRBADGE raises the attack power of POKéMON. It also enables P
- 0x805c8a, 0x92369a: FLASH illuminates even the darkest of all places. But to use it out of battle, you need the BADGE fr
- 0x806326, 0x8065a8, 0x88a008, 0x8aca75, 0x8acc78, 0x92acb7, 0x95e968: Have you gone to the POKéMON GYM? You can test your POKéMON and yourself there. It’s a rite of passa
- 0x80639f, 0x88a081, 0x8acaf2: You have some good POKéMON there. It must be from the training you gave them around VIOLET CITY. The
- 0x812a74, 0x8131ee: Yo, CHAMP in making! This GYM is home to normal-type POKéMON TRAINERS. I recommend you use fighting-
- 0x81309e, 0x813514, 0x8138c4, 0x813c77: ...Sniff... What? What do you want? A BADGE? Oh, right. I forgot. Here’s PLAINBADGE.{PLAYER} receive
- 0x814033, 0x823f60: ...Sniff... What? What do you want? A BADGE? Oh, right. I forgot. Here’s PLAINBADGE. {PLAYER} receiv
- 0x81f408, 0x81f45a: ECRUTEAK CITY POKéMON GYM LEADER: MORTY The Mystic Seer of the Future
- 0x821896, 0x821918: MORTY, the GYM LEADER, is absent. Sorry, but you’ll have to leave. HOhohoho.
- 0x821a4f, 0x824bf7, 0x84969d, 0x849740, 0x8c306f, 0x8c33c9, 0x8c439d: TIN TOWER is off limits to anyone without ECRUTEAK GYM’s BADGE. Sorry, but you’ll have to leave.
- 0x824ddd, 0x824eae, 0x856de1: TIN TOWER may be entered by those bearing ECRUTEAK’s GYM BADGE. However, now that SUICUNE, RAIKOU an
- 0x8268cc, 0x826b5a, 0x826dba, 0x826f8e, 0x827173, 0x82f700, 0x82f8e6, 0x836b2f, 0x836d12, 0x836ef4, 0x8370d6, 0x870901, 0x870ae3: ... You again? There’s no need to panic. I don’t bother with wimps like you. Speaking of weaklings, 
- 0x82adbd, 0x836887, 0x8490d6, 0x84acb2, 0x84c03b, 0x84c38b, 0x84c6dd: Wha? Huh? I lost? How about that! You’re worthy of STORMBADGE!
- 0x82af4a, 0x836a13, 0x849262, 0x84ae3e, 0x84c1c7, 0x84c519, 0x84c86b: {PLAYER} received the STORMBADGE! STORMBADGE makes all POKéMON up to L70 obey, even traded ones. It 
- 0x82ba23, 0x82bb2a: A GYM LEADER isn’t just about being strong. A LEADER also needs to be compassionate.
- 0x82bf35, 0x82c8e1, 0x83670b: JASMINE: ...Oh, I’m so relieved... This is just so wonderful... Thank you so very, very much. ...I w
- 0x82bffb, 0x939695: JASMINE, the GYM LEADER, is at the LIGHTHOUSE. She’s been tending to a sick POKéMON. A strong TRAINE
- 0x8384c2, 0x8387fd, 0x838b3b, 0x83a754, 0x83aa92, 0x83add3, 0x988340, 0x9ac6a3: That’s WHIRLPOOL. Teach it to a POKéMON to get across wild water. But keep this in mind. You can use
- 0x83db83, 0x83e99c, 0x879836, 0x8a071d, 0x8a1051, 0x8a1985: ELM: This? But... Is it a POKéMON EGG? If it is, it is a great discovery! ELM: What?!? PROF.OAK gave
- 0x8400b5, 0x845844: This GYM has a slippery floor. It’s fun, isn’t it? But hey--we’re not playing games here!
- 0x840358, 0x846d17: To get to PRYCE, our GYM LEADER, you need to think before you skate.
- 0x8403bf, 0x846d7e: If you don’t skate with precision, you won’t get far in this GYM.
- 0x84071b, 0x847fae, 0x84a982, 0x8c2126, 0x8c2500, 0x8c2a18, 0x8cc161: Ah, I am impressed by your prowess. With your strong will, I know you will overcome all life’s obsta
- 0x8419be, 0x841a9c: We stashed the real DIRECTOR in the UNDERGROUND WAREHOUSE. It’s at the far end of the UNDERGROUND. B
- 0x84edf4, 0x857ebd: CLAIR, our GYM LEADER, is waiting for you. However, it would be impossible for a run-of-the-mill TRA
- 0x8507bb, 0x87ab4f, 0x87d90d, 0x87e1d3, 0x87ea99, 0x8ef8ec: My name is GIOVANNI! Three years ago I used to command TEAM ROCKET. I disbanded TEAM ROCKET after I 
- 0x852cf9, 0x880fae: CLAIR: Thanks for getting rid of TEAM AQUA for us! So there was a POKéMON here! ................ TEA
- 0x8532ad, 0x874a7e, 0xa28101, 0xa2c06c: I am CLAIR. The world’s best dragon master. I can hold my own against even the POKéMON LEAGUE’s ELIT
- 0x8533fe, 0x874bcf, 0xa2a033, 0xa2d864: What’s the matter? Aren’t you going to the POKéMON LEAGUE? Do you know how to get there? From here, 
- 0x8540b7, 0x85450b, 0x8546d4, 0x855bbd, 0x856530, 0x8566e0, 0x886dd7, 0x886f96: It’s you again! I’m heading to AZALEA TOWN to take out the GYM LEADER! I’ve allready thrashed VIOLET
- 0x85504e, 0x855222: ZANE: Thanks for finding that kids doll. I would’nt of been able to get to the GYM otherwise! I’ll s
- 0x862561, 0x8626d2, 0x869af7, 0x8722b4, 0x88406d, 0x8a47fb: Oh sorry! I didn’t see you there. I’m FALKNER. The VIOLET GYM LEADER. I’ve just been training my POK
- 0x86c560, 0x8d7fcb, 0x8d884f: LANCE: I’ve been waiting for you. {PLAYER}! I knew that you, with your skills, would eventually reac
- 0x87027d, 0x872663, 0x879dcb: Are you off to the POKéMON LEAGUE? Here. Take this. It should help you.
- 0x871ead, 0x8720d0, 0x883073, 0x88325c, 0x883447, 0x883634: My name is ZANE. I’m gonna be the greatest POKéMON TRAINER in history! Hey. You look weak! Come on. 
- 0x87249c, 0x87255f, 0x882616, 0x88abb8, 0x88ac80, 0x88ad2f, 0x88ae0b, 0x88aebb, 0x8a23f4, 0x8a4708: I’m sorry but the GYM LEADER Is out training in DARK CAVE! He should be back soon. In the mean time,
- 0x878fd0, 0x8d3abc, 0x925e75: Only TRAINERS who have proven them- selves may pass. Oh! The eight BADGES of JOHTO! Please, go right
- 0x879291, 0x87efed: Hello and Welcome to the SS. MAGMA. We will be arriving at the POKéMON LEAGUE shortly. In the mean t
- 0x879a91, 0x8ae70d: Have you gone to the BATTLE TOWER? I think a lot of tough TRAINERS have gathered there already. But 
- 0x87ef2d, 0x8812ff, 0x8814dd: Welcome to the SS. MAGMA. Would you like to go to the POKéMON LEAGUE?
- 0x87f8de, 0x87fe4e: Hey! What are you doing in our cabin? Oh. A fight! I could do with some practice for the POKéMON LEA
- 0x87f960, 0x87fed0: Your quite a tough TRAINER. You should have no problem at the POKéMON LEAGUE.
- 0x87f9cb, 0x87ff39: Have you beaten my boyfriend yet? He’s quite weak. He thinks he can take on the POKéMON LEAGUE!
- 0x87fa34, 0x87ffa2: You beat me fare and square! I’ve got alot of training to do before the POKéMON LEAGUE!
- 0x883e3c, 0x8d7ccd, 0x8d8532, 0x97825c: PROF.OAK: Ah, {PLAYER}! It’s been a long while. You certainly look more impressive. Your conquest of
- 0x8890ce, 0x89ccad: As the captin was driving the ship to the POKéMON LEAGUE an unexpected event occurred. A giant fish 
- 0x88922e, 0x89ce0d: That KEY will unseal the POKéMON ZAPDOS! Thanks again for saving me. I’ll take the ship to the POKéM
- 0x8896a1, 0x89d257: So you are the intruder! You seem very strong and capable for the league! I’m afraid you won’t be go
- 0x8a22d4, 0x8d5567: Hold it! ...Are you going to take the POKéMON LEAGUE challenge? ...Don’t make me laugh. You’re so mu
- 0x8c36c1, 0x8c3c91, 0x8c3fe6: ELM: {PLAYER}? Is that you? It’s PROF. ELM. I just had a call from the GYM LEADER of ECRUTEAK CITY. 
- 0x8c4ef1, 0x8c52ae: rivell: Well if you don’t mind then Were going to have our POKéMON BATTLE. ...................... ..
- 0x8c4fda, 0x8c5397: ZANE: I’m ZANE. A POKéMON TRAINER like you. I saw {PLAYER} come down here and then you followed so I
- 0x8d040f, 0x8d0833: DRAY:It’s finaly happening. The legends are true. I’m DRAY. The ECRUTEAK CITY GYM LEADER! That bird 
- 0x8d7f2f, 0x8d87b2: ...It’s over. But it’s an odd feeling. I’m not angry that i lost. In fact, I feel happy. Happy that 
- 0x8e243d, 0x8e2569: DIRECTOR: Thank you guys so much for saving SILPH.CO. I never got your names...... Ah! {PLAYER} and 
- 0x901259, 0x94aaad: OAK: Ah, {PLAYER}! It’s good of you to come all this way to KANTO. What do you think of the TRAINERS
- 0x9031e7, 0x90b30e: LEADER: WHITNEY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER}
- 0x903255, 0x90b37e: LEADER: JASMINE WINNING TRAINERS: rivel , AXEL, ZANE, {PLAYER}
- 0x9033d6, 0x90b2da: LEADER: BUGSY WINNING TRAINERS: {RIVAL}, AXEL, ZANE, {PLAYER}
- 0x916d54, 0x9176d9: Fufufu! I’m JANINE, the GYM LEADER! No, I’m not! Gotcha, sucker!
- 0x918e17, 0x91934b, 0x919432: MISTER G: Erm... Aha we got you... Oh you’re er not him. Pity. W-well, d-don’t interrupt we’re deali
- 0x9194ff, 0x92ed6e, 0x96823a: MISTER R: You know we could have amounted to more than this me and my comrades. You probably met the
- 0x9265af, 0x92decf: The train to VALENCIA ISLAND is currently waiting in platform 1.
- 0x9265f2, 0x92df12: The next train to VALENCIA ISLAND is due to arrive in {STR_VAR_1} minutes.
- 0x926636, 0x92df56: The next train to VALENCIA ISLAND is due to arrive in {STR_VAR_1} minute.
- 0x93030b, 0x93082c: Scientist: Hey, thanks for getting rid of those guys. I’m from the Science Complex just north of her
- 0x931b82, 0x931e90: ???: (sigh) Then I’ll go with him. OFFICER: And who are you? ???: (sigh...) The name’s JIN. I’m an E
- 0x93341d, 0x933d8f: GIOVANNI: Well I can see your eger to know what were doing here. We made a ZAPDOS land on top of thi
- 0x93a1d8, 0x93a2e2: ...Thank you for your help at the LIGHTHOUSE... But this is different. Please allow me to introduce 
- 0x945271, 0x945654, 0x95109c, 0x9514a0, 0x951cfc, 0x952127, 0x95252c, 0x955c4a: JIN: (sigh) You did good today, {PLAYER}. Hopfully i’ll see you around VALENCIA ISLAND at some point
- 0x9452e6, 0x9456c9: OFFICER: Oh wow! You did it! The engine has started again. You and JIN did very well today. Thanks y
- 0x948d14, 0x948ef5: MISTY: Aww! Why did you have to show up and bug us now? Do you know what they call people like you? 
- 0x951111, 0x951513, 0x951d6e, 0x952199: OFFICER: Oh wow! You did it! The engine has started again. You and JIN did very well today. Thanks t
- 0x955858, 0x955cbc: OFFICER: Oh wow! You did it! The engine has started again. You and JIN did very well today. Thanks t
- 0x959296, 0x965c3e: AXEL: Where is your LEADER? GRUNT: ... ... ... AXEL: I said, where is your LEADER?
- 0x95de09, 0x98255c: OAK: Wow! That’s excellent! You collected the BADGES of GYMS in KANTO. Well done! I was right in my 
- 0x968d35, 0x997e34: Welcome to FAST SHIP S.S.AQUA. Would you like travel to VALENCIA ISLAND?
- 0x978f08, 0xa15d08: ???: I’m the LEADER of TEAM SATURN! I came over from the OUKA region in search of two sacred POKéMON
- 0x97aaac, 0x9ba36f: MISTER R: You know we could have amounted to more than this me and my comrades. You probably met the
- 0x9b33f0, 0xa142bd: OFFICER: Thank you for getting rid of those gang members. What?!? They took some CORSOLA and are pla
- 0x9c7236, 0xa2a1b1, 0xa314cf: I won’t admit this. I may have lost, but you’re still not ready for the POKéMON LEAGUE. I know. Behi
- 0x9e0105, 0x9e04f2: ZANE: Capture every last one of them... Don’t let any get away!
- 0xa9802b, 0xa982c7: Mister G: If only Red accepted our offer back then, this would never be a bother. I must do what’s b
- 0xaa1d8c, 0xaa5dc4: Mister G: Well, if it isn’t that meddler from the Lighthouse. You didn’t heed my warning, eh? Quite 
- 0xaa1ed3, 0xaa5f0b: Go! Take the Nexus S to the other base. They are waiting for the goods. As a member of the Nexus 4, 

Exact normalized equality does not establish which copy is active. Similar but edited versions are not merged.

## Scope still open

Generic gym/league/island text remains in JSON without assuming Orange relevance. Orange Mail, Ivysaur substring matches, and credits are separated. Neighboring dialogue without keywords, indirect/computed references, native text consumers, custom controls, map ownership, chronology, and orphan/unused classification still need follow-up. Step 2 is not complete.

## Next bounded step

Expand the specific text-reference clusters to adjacent non-keyword messages and validate their script entry paths; keep all reachability claims open until map/script archaeology.
