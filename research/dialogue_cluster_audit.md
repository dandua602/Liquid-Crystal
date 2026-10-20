# Neighboring dialogue and entry-path audit

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

CONFIRMED_IN_ROM: byte/text presence. STRONGLY_INFERRED: interpretation using the pinned FireRed script formats. Static path does not prove gameplay reachability. No new story or ROM modifications.

32 unique messages across five anchor clusters; 11 absent from the prior keyword corpus. These additions were found through script operands, not invented or assumed from nearby ROM bytes.

## Method and limits

Reverse raw pointer hits that match explicit branch/call or trainer continuation operands; seek incoming pointer targets within 512 bytes with a gapless static path to the source command. Follow direct conditional branches and stack-aware calls/returns. Callstd, native/special calls, waits, and trainer engine transfers are opaque/assumed paths. Unsupported instructions stop a path; physical proximity alone adds no messages.

Both branch outcomes are explored without solving flag/variable conditions. Opaque standard/native routines and battle outcomes are not emulated. Root pointer sites remain unclassified until map/native ownership is checked. Byte bounds, depth limits, unsupported instructions and overlaps are recorded in JSON. An unparsed frontier is not a broken event.

## Anchor 0x930c7d

4 instruction candidates; 1 referenced messages; 0 frontiers; 0 overlaps.

Candidate entries: 0x9302EB.

### Reverse transfer evidence

No explicit reverse transfer found within the selected scope; incoming root pointer remains unclassified.

### Recovered messages

#### 0x930C7D — previously indexed

References: 0x9302EB (loadword_then_callstd).

```text
Mandarin City Pokémon Gym<PARAGRAPH>

Leader: Rudy<PARAGRAPH>

The Mysterious Playboy
```

### Stopped or opaque paths

No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.

## Anchor 0xb11c47

27 instruction candidates; 5 referenced messages; 0 frontiers; 0 overlaps.

Candidate entries: 0xB00435, 0xB0FF91, 0xB0FFE2.

### Reverse transfer evidence

- trainer_continuation_pointer: 0xB0FF91 operand 0xB0FF9F → 0xB0FFE2.
- explicit_script_transfer: 0xB00438 operand 0xB0043A → 0xB0FF91.

### Recovered messages

#### 0xB01F94 — previously indexed

References: 0xB0043E (loadword_then_callstd).

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

#### 0xB11AA6 — absent from prior keyword corpus

References: 0xB0FF91 (trainer_intro).

```text
Welcome back, {PLAYER}.<PARAGRAPH>

After our victory I got thinking
about my own bonds with my Pokémon.<PARAGRAPH>

I came to the conclusion that,
beating you will give me the<SCROLL>
information I need.<PARAGRAPH>

Prepare yourself, I won’t go easy on
you!
```

#### 0xB11B79 — absent from prior keyword corpus

References: 0xB0FF91 (trainer_defeat).

```text
Outstanding!
Simply amazing.<PARAGRAPH>

After battling you It’s become clear
to me what I’m lacking.
```

#### 0xB11BD5 — absent from prior keyword corpus

References: 0xB0FFA3 (loadword_then_callstd).

```text
Thank you for showing me what I
needed.<PARAGRAPH>

I’m going to train harder and
strengthen the bonds with my own<SCROLL>
Pokémon.
```

#### 0xB11C47 — previously indexed

References: 0xB0FFE2 (loadword_then_callstd).

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

### Stopped or opaque paths

No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.

## Anchor 0xb1d4e0

35 instruction candidates; 8 referenced messages; 0 frontiers; 0 overlaps.

Candidate entries: 0xAAAF9A, 0xAAAFBA.

### Reverse transfer evidence

No explicit reverse transfer found within the selected scope; incoming root pointer remains unclassified.

### Recovered messages

#### 0xABCCE8 — previously indexed

References: 0xAAAFA4 (loadword_then_callstd).

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

#### 0xABB872 — absent from prior keyword corpus

References: 0xAAAFAC (trainer_defeat).

```text
You put up a mighty good fight, son.
```

#### 0xABB853 — absent from prior keyword corpus

References: 0xAAAFAC (trainer_victory).

```text
Meddlers have no place here.
```

#### 0xB1D4E0 — previously indexed

References: 0xAAAFBA (loadword_then_callstd).

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

#### 0xAB7EEB — previously indexed

References: 0xAAAFCE (loadword_then_callstd).

```text
<COLOR 08>Mister G: I will now take my leave,
but before that I will tell you,<SCROLL>
Mister Z is waiting for you.
```

#### 0xAB7CF8 — previously indexed

References: 0xAAAFF2 (loadword_then_callstd).

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

#### 0xAACF4C — previously indexed

References: 0xAAB205 (loadword_then_callstd).

```text
S-sorry, the connection is going, I
didn’t hear your answer.<PARAGRAPH>

So, can you help out by beating Team
Nexus and Zane?
```

#### 0xAAD76A — previously indexed

References: 0xAACFC0 (loadword_then_callstd).

```text
Oh?<PARAGRAPH>

You already are taking them down,
and you got rid of one of their<SCROLL>
lab leaders?<PARAGRAPH>

That’s great, just what I expected
from you, {PLAYER}!<PARAGRAPH>

Thanks again, I owe you one!<PARAGRAPH>

Talk to you later.
```

### Stopped or opaque paths

No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.

## Anchor 0x9e2b2d

129 instruction candidates; 17 referenced messages; 0 frontiers; 0 overlaps.

Candidate entries: 0x9D609D, 0x9D60E1.

### Reverse transfer evidence

- explicit_script_transfer: 0x9D60A9 operand 0x9D60AB → 0x9D60E1.

### Recovered messages

#### 0x9013C2 — absent from prior keyword corpus

References: 0x90109B (loadword_then_callstd).

```text
OAK: Hello there {PLAYER}!
Good of you to stop by.<PARAGRAPH>

Have you got that BALL for me yet?
I’m still waiting for it.<PARAGRAPH>

Let me check out your POKéDEX...
```

#### 0xB1D7DE — previously indexed

References: 0x901148 (loadword_then_callstd).

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

#### 0x98255C — previously indexed

References: 0x90115C (loadword_then_callstd).

```text
OAK: Wow!
That’s excellent!<PARAGRAPH>

You collected the BADGES of GYMS in<SCROLL>
KANTO.<PARAGRAPH>

Well done!
I was right in my assessment of you.<PARAGRAPH>

Tell you what, {PLAYER}.
I’ll make arrangements so that you<SCROLL>
can go to MT.SILVER.<PARAGRAPH>

MT.SILVER is a big mountain that is
home to many wild POKéMON.<PARAGRAPH>

It’s too dangerous for your average
TRAINER, so it’s off limits.<PARAGRAPH>

But we can make an exception in your
case, {PLAYER}.<PARAGRAPH>

Go up to INDIGO PLATEAU.
You can reach MT.SILVER from there.
```

#### 0x98270C — absent from prior keyword corpus

References: 0x901199 (loadword_then_callstd).

```text
The amount of progress you’ve made
on your POKéDEX is:<PARAGRAPH>

{STR_VAR_1} POKéMON seen and
{STR_VAR_2} POKéMON owned.<PARAGRAPH>

<FONT 02>PROF. OAK’s rating:
```

#### 0x982782 — absent from prior keyword corpus

References: 0x9011D6 (loadword_then_callstd).

```text
And your NATIONAL POKéDEX is:<PARAGRAPH>

{STR_VAR_1} POKéMON seen and
{STR_VAR_2} POKéMON owned.
```

#### 0x9827C8 — absent from prior keyword corpus

References: 0x9011F9 (loadword_then_callstd).

```text
If you’re in the area,
I hope you come visit again.
```

#### 0x9827FE — absent from prior keyword corpus

References: 0x901230 (loadword_then_callstd).

```text
I’ll be looking forward to seeing
you fill the NATIONAL POKéDEX!
```

#### 0x982841 — absent from prior keyword corpus

References: 0x901241 (loadword_then_callstd).

```text
Finally…<PARAGRAPH>

You’ve finally completed the
POKéDEX!<PARAGRAPH>

It’s magnificent!
Truly, this is a fantastic feat!
```

#### 0x901259 — previously indexed

References: 0x9D60D3 (loadword_then_callstd).

```text
OAK: Ah, {PLAYER}!<PARAGRAPH>

It’s good of you to come all this way
to KANTO.<PARAGRAPH>

What do you think of the TRAINERS
out here?<PARAGRAPH>

Pretty tough, huh?<PARAGRAPH>

OAK: Ah, you’re collecting KANTO GYM
BADGES.<PARAGRAPH>

I imagine that it’s hard, but the
experience is sure to help you.<PARAGRAPH>

Come see me when you get them all.
I’ll have a gift for you.<PARAGRAPH>

Keep trying hard, {PLAYER}!
How is your POKéDEX coming?<PARAGRAPH>

Let’s see...
```

#### 0x9E2B2D — previously indexed

References: 0x9D60E1 (loadword_then_callstd).

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

#### 0x9D69B8 — previously indexed

References: 0xB123D6 (loadword_then_callstd).

```text
OAK: Hello {PLAYER}.
Good of you to stop by.<PARAGRAPH>

The research on the GS BALL is going
to take a while.<PARAGRAPH>

In the mean time why don’t you take
the ORANGE LEAGUE challenge?
```

#### 0xA9B0A4 — previously indexed

References: 0xB1252F (loadword_then_callstd).

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

#### 0xB19BB1 — previously indexed

References: 0xB12543 (loadword_then_callstd).

```text
Thanks {PLAYER}, I trust that you
will be able to handle this task.<PARAGRAPH>

So the Orange League is going well
I hear?<PARAGRAPH>

Do stop by some other time.
```

#### 0xB2922F — previously indexed

References: 0xB1A0DA (loadword_then_callstd).

```text
Hi {PLAYER}, how’s it going?<PARAGRAPH>

Have you delivered that GS Ball yet?<PARAGRAPH>

Say hi to Kurt for me would you?
```

#### 0xB1A3DD — previously indexed

References: 0xB1A299 (loadword_then_callstd).

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

#### 0xB1A347 — previously indexed

References: 0xB1A2B3 (loadword_then_callstd).

```text
{PLAYER}! Isn’t it amazing?<PARAGRAPH>

The GS Ball turned out to be related
to Ilex Forest and the legendary<SCROLL>
Celebi.<PARAGRAPH>

I knew Kurt had it in him to solve
the mystery!
```

#### 0xB1A2CF — previously indexed

References: 0xB1A2C1 (loadword_then_callstd).

```text
Hello {PLAYER}, good to see you.<PARAGRAPH>

How is the Orange League going?<PARAGRAPH>

I hope you’re winning your way
through and keeping strong.
```

### Stopped or opaque paths

No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.

## Anchor 0xa9c482

4 instruction candidates; 1 referenced messages; 0 frontiers; 0 overlaps.

Candidate entries: 0xA9C477.

### Reverse transfer evidence

No explicit reverse transfer found within the selected scope; incoming root pointer remains unclassified.

### Recovered messages

#### 0xA9C482 — previously indexed

References: 0xA9C477 (loadword_then_callstd).

```text
Route 59<PARAGRAPH>

↓ Mandarin City
→ Science Complex<PARAGRAPH>

↑ Route 60 & Old Warehouse
```

### Stopped or opaque paths

No unresolved terminal within these candidate paths; native/standard call returns remain assumptions.

## Next bounded step

Expand this entry-path and neighboring-message audit to the remaining Science Complex / Nexus machine dialogue anchors, including charging and shutdown messages. Map ownership and runtime reachability remain for subsequent archaeology.
