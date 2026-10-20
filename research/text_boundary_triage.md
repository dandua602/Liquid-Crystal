# Historical text-miss triage

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

Finite reviewed partition of the 53 frozen misses. Recovery requires complete strict-English tokens, EOS, and keyword bytes at glyph positions. Binary-context labels remain conservative. Pointer absence and raw byte repetition do not prove unused data. All original hits remain represented.

```json
{
  "historical_hits": 53,
  "classifications": {
    "RECOVERED_DYNAMIC_TEMPLATE": 4,
    "BINARY_CONTEXT_SUBSTRING_CANDIDATE": 8,
    "PROSE_BOUNDARY_ANOMALY": 12,
    "REPEATED_BINARY_WINDOW_CANDIDATE": 22,
    "RECOVERED_PROVISIONAL_TEXT": 7
  },
  "recovered_text_blocks": 6,
  "partial_prose_contexts": 6,
  "repeated_context_groups": 2,
  "unused_or_unreachable_certifications": 0
}
```

## Recovered templates and readable suffixes

### 0x41a2e1 — REFERENCED_DYNAMIC_TEMPLATE

Exact pointer sites: 0x115144.
Gameplay reachability UNKNOWN.

```text
{DYNAMIC_00} had a marvelous battle
with the CHAMPION, {DYNAMIC_01}.
```

### 0x41af0c — REFERENCED_DYNAMIC_TEMPLATE

Exact pointer sites: 0x114de4.
Gameplay reachability UNKNOWN.

```text
Took on {DYNAMIC_00} GYM LEADER
{DYNAMIC_01}’s {DYNAMIC_02} with {DYNAMIC_03}
and won {DYNAMIC_04}!
```

### 0x41b3fb — REFERENCED_DYNAMIC_TEMPLATE

Exact pointer sites: 0x45aba0.
Gameplay reachability UNKNOWN.

```text
The LEADER, {DYNAMIC_00}, has
left, ending the chat.
```

### 0x905c04 — PROVISIONAL_READABLE_SUFFIX

Exact pointer sites: none found.
Gameplay reachability UNKNOWN.

```text
There used to be a POKéMON GYM here.<PARAGRAPH>

Unfortunitly it’s not used anymore.
```

### 0x969854 — PROVISIONAL_READABLE_SUFFIX

Exact pointer sites: none found.
Gameplay reachability UNKNOWN.

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

### 0xaaa9dc — PROVISIONAL_READABLE_SUFFIX

Exact pointer sites: none found.
Gameplay reachability UNKNOWN.

```text
It’s a map of Sunburst Island.<PARAGRAPH>

Serveral locations are marked down.<PARAGRAPH>

Route 53, Route 54, Route 55,
Sandway Town.<PARAGRAPH>

A large circle is placed around West
Vale Port.
```

## Prose boundary anomalies

### 0x73d98d

Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.

First unvalidated glyph: 0x73d9f9. Strict full-string acceptance: False.

```text
A POKéMON you get in a trade
grows quickly.<PARAGRAPH>

But if you don’t have the right GYM
BADGE, they may disobey you.
```

### 0x86aa8f

Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.

First unvalidated glyph: 0x86aca0. Strict full-string acceptance: False.

```text
ELM: This?<PARAGRAPH>

But... Is it a POKéMON EGG?
If it is, it is a great discovery!<PARAGRAPH>

ELM: What?!?<PARAGRAPH>

PROF.OAK gave you a POKéDEX?
{PLAYER}, is that true? <PARAGRAPH>

Th-that’s incredible!<PARAGRAPH>

He is superb at seeing the potential
of people as TRAINERS.<PARAGRAPH>

Wow, {PLAYER}. You may have what
it takes to become the CHAMPION.<PARAGRAPH>

You seem to be getting on
great with POKéMON too.<PARAGRAPH>

You should take the POKéMON GYM
challenge.<PARAGRAPH>

The closest GYM would be the one
in VIOLET CITY.<PARAGRAPH>

...{PLAYER}. The road to the championship
will be a long one.<PARAGRAPH>

Before you leave, make sure that
you talk to your mom.
```

### 0x86cfab

Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.

First unvalidated glyph: 0x86d000. Strict full-string acceptance: False.

```text
This port offers TRAINERS a
lift to the POKéMON LEAGUE.<PARAGRAPH>

It also offers trips to OUKA<PK>
```

### 0x8abfcf

Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.

First unvalidated glyph: 0x8ac009. Strict full-string acceptance: False.

```text
<FONT 02>{PLAYER} received the ZEPHYRBADGE!<PAUSE_MUSIC><PLAY_BGM 04 01><PAUSE FE><PAUSE 56><RESUME_MUSIC><PARAGRAPH>

ZEP         
```

### 0x8d84f4

Readable bytes coexist with unsupported/non-text tail; do not promote permissive EOS to a validated string or gameplay bug.

First unvalidated glyph: 0x8d8524. Strict full-string acceptance: False.

```text
<COLOR 04>MARY: Let’s interview the brand new
CHAMPION!
```

### 0xaaaf41

89-byte readable item description has no FF before applymovement script at 0xAAAF9A; raw FF at 0xAAAF9B is the local-object operand. Native accessor evidence is in research/rank_description_investigation.md. No runtime appearance asserted.

First unvalidated glyph: 0xaaaf9a. Strict full-string acceptance: False.

```text
The Commanding Rank given to you
by Mister G, an ex-commander in the
Elite group Nexus 4.
```

## Complete hit partition

| Hit | Term | Classification |
|---|---|---|
| 0x41a304 | Champion | RECOVERED_DYNAMIC_TEMPLATE |
| 0x41af17 | gym | RECOVERED_DYNAMIC_TEMPLATE |
| 0x41af1b | leader | RECOVERED_DYNAMIC_TEMPLATE |
| 0x41b3ff | leader | RECOVERED_DYNAMIC_TEMPLATE |
| 0x4acaf1 | Ivy | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x4cbf61 | gym | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x4d0874 | gym | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x4d720b | Zane | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x4fc4f2 | gym | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x51eaef | Ivy | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x61b982 | gym | BINARY_CONTEXT_SUBSTRING_CANDIDATE |
| 0x73d9d9 | gym | PROSE_BOUNDARY_ANOMALY |
| 0x73d9dd | badge | PROSE_BOUNDARY_ANOMALY |
| 0x7aa02f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7aa247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7ad02f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7ad247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b002f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b0247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b302f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b3247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b602f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b6247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b902f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7b9247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7bc02f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7bc247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7bf02f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7bf247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c202f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c2247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c502f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c5247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c802f | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x7c8247 | Ivy | REPEATED_BINARY_WINDOW_CANDIDATE |
| 0x86ab9a | Champion | PROSE_BOUNDARY_ANOMALY |
| 0x86abf2 | gym | PROSE_BOUNDARY_ANOMALY |
| 0x86ac0d | gym | PROSE_BOUNDARY_ANOMALY |
| 0x86ac49 | Champion | PROSE_BOUNDARY_ANOMALY |
| 0x86cfdb | League | PROSE_BOUNDARY_ANOMALY |
| 0x8abfe8 | badge | PROSE_BOUNDARY_ANOMALY |
| 0x8d851b | Champion | PROSE_BOUNDARY_ANOMALY |
| 0x905c1f | gym | RECOVERED_PROVISIONAL_TEXT |
| 0x9698c9 | Ivy | RECOVERED_PROVISIONAL_TEXT |
| 0x9698de | Valencia | RECOVERED_PROVISIONAL_TEXT |
| 0x9698e7 | island | RECOVERED_PROVISIONAL_TEXT |
| 0x969903 | Orange | RECOVERED_PROVISIONAL_TEXT |
| 0x96990a | island | RECOVERED_PROVISIONAL_TEXT |
| 0xaaa9f3 | island | RECOVERED_PROVISIONAL_TEXT |
| 0xaaaf45 | Commanding Rank | PROSE_BOUNDARY_ANOMALY |
| 0xaaaf65 | Mister G | PROSE_BOUNDARY_ANOMALY |
| 0xaaaf92 | Nexus | PROSE_BOUNDARY_ANOMALY |
| 0xd4f544 | Ivy | BINARY_CONTEXT_SUBSTRING_CANDIDATE |

No row certifies unused, unreachable, placeholder or broken gameplay. Full strings, partial prose and binary-context matches remain distinct.
