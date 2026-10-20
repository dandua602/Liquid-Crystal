# Nexus machine / charging dialogue audit

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

CONFIRMED_IN_ROM: raw instruction and text bytes. STRONGLY_INFERRED: FireRed-format control/state interpretation. Gameplay reachability, active event ownership and native/standard effects remain UNKNOWN. No source ROM or save modified.

```json
{
  "anchors": 9,
  "unique_text_targets": 14,
  "nonempty_strings": 12,
  "empty_terminated_targets": 2,
  "nonempty_strings_absent_from_prior_keyword_corpus": 6,
  "unique_instruction_candidates": 204,
  "state_operand_instructions": 58,
  "unrooted_anchors": 0,
  "controller_scripts": 10,
  "instruction_overlaps": 0,
  "frontier_reasons": {},
  "used_opcodes_with_modified_handler_intervals": [
    182
  ]
}
```

Nine observed messages selected from case-insensitive machine/charge/shutdown text scans. Incoming-target roots sought within 512 bytes; explicit predecessor transfers expanded for two rounds. Paths retain both conditional outcomes and opaque engine-return assumptions. No map/runtime reachability proof.

Each instruction/frontier/root witness is retained in extracted/text/nexus_machine_audit.json. Repeated messages across clusters are shared evidence, not additional copies of the scene. Unresolved parser paths are not automatically game bugs.

## 0xaa3280 — already charged

Candidate entries: 0xAA0FD8, 0xAA2C5D.

17 instruction candidates; 3 referenced strings; 0 unresolved frontiers.

### 0xAADF68 — absent from prior keyword corpus

References: 0xAA0FD8 (loadword_then_callstd).

```text
It looks like a machine with a slot
of some sort.<PARAGRAPH>

You can put your G Rank inside to
power it up.<PARAGRAPH>

Do you want to power up your G Rank?
```

### 0xAA5FB1 — absent from prior keyword corpus

References: 0xAA2C69 (loadword_then_callstd).

```text
Your G Rank is now charged for one
use!
```

### 0xAA3280 — absent from prior keyword corpus

References: 0xAA2C74 (loadword_then_callstd).

```text
Your G Rank is already fully charged.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xaa5fb1 — charging success

Candidate entries: 0xAA0FD8, 0xAA2C5D.

17 instruction candidates; 3 referenced strings; 0 unresolved frontiers.

### 0xAADF68 — absent from prior keyword corpus

References: 0xAA0FD8 (loadword_then_callstd).

```text
It looks like a machine with a slot
of some sort.<PARAGRAPH>

You can put your G Rank inside to
power it up.<PARAGRAPH>

Do you want to power up your G Rank?
```

### 0xAA5FB1 — absent from prior keyword corpus

References: 0xAA2C69 (loadword_then_callstd).

```text
Your G Rank is now charged for one
use!
```

### 0xAA3280 — absent from prior keyword corpus

References: 0xAA2C74 (loadword_then_callstd).

```text
Your G Rank is already fully charged.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xad3b7e — shutdown complete

Candidate entries: 0xAD3D6E.

68 instruction candidates; 7 referenced strings; 0 unresolved frontiers.

### 0xAD3D3D

References: 0xAD348B (loadword_then_callstd).

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xAD3EB1 — absent from prior keyword corpus

References: 0xAD34AD (bufferstring).

```text
Activated
```

### 0xAD34C8 — absent from prior keyword corpus

References: 0xAD34B5 (bufferstring).

```text
Deactivated
```

### 0xAD3C54

References: 0xAD34ED (loadword_then_callstd).

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xAD3B7E — absent from prior keyword corpus

References: 0xAD3E9E (loadword_then_callstd).

```text
System shutdown complete.<PARAGRAPH>

Global power level: {STR_VAR_1}0%.
```

### 0xAD3BB4

References: 0xAEFF12 (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xB01831

References: 0xAEFFDA (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xad3bb4 — shutdown override / intruder protection

Candidate entries: 0xAD344E, 0xAEFF09.

68 instruction candidates; 7 referenced strings; 0 unresolved frontiers.

### 0xAD3D3D

References: 0xAD348B (loadword_then_callstd).

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xAD3EB1 — absent from prior keyword corpus

References: 0xAD34AD (bufferstring).

```text
Activated
```

### 0xAD34C8 — absent from prior keyword corpus

References: 0xAD34B5 (bufferstring).

```text
Deactivated
```

### 0xAD3C54

References: 0xAD34ED (loadword_then_callstd).

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xAD3B7E — absent from prior keyword corpus

References: 0xAD3E9E (loadword_then_callstd).

```text
System shutdown complete.<PARAGRAPH>

Global power level: {STR_VAR_1}0%.
```

### 0xAD3BB4

References: 0xAEFF12 (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xB01831

References: 0xAEFFDA (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xad3c54 — insert G Rank prompt

Candidate entries: 0xAD344E, 0xAD354B, 0xAD3D6E, 0xAD3D94, 0xAD3DBA, 0xAD3DE0, 0xAD3E06, 0xAD3E2C, 0xAD3E52, 0xAD3E78.

167 instruction candidates; 7 referenced strings; 0 unresolved frontiers.

### 0xAD3D3D

References: 0xAD348B (loadword_then_callstd).

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xAD3EB1 — absent from prior keyword corpus

References: 0xAD34AD (bufferstring).

```text
Activated
```

### 0xAD34C8 — absent from prior keyword corpus

References: 0xAD34B5 (bufferstring).

```text
Deactivated
```

### 0xAD3C54

References: 0xAD34ED (loadword_then_callstd).

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xAD3B7E — absent from prior keyword corpus

References: 0xAD3E9E (loadword_then_callstd).

```text
System shutdown complete.<PARAGRAPH>

Global power level: {STR_VAR_1}0%.
```

### 0xAD3BB4

References: 0xAEFF12 (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xB01831

References: 0xAEFFDA (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xad3d3d — status display

Candidate entries: 0xAD344E.

68 instruction candidates; 7 referenced strings; 0 unresolved frontiers.

### 0xAD3D3D

References: 0xAD348B (loadword_then_callstd).

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xAD3EB1 — absent from prior keyword corpus

References: 0xAD34AD (bufferstring).

```text
Activated
```

### 0xAD34C8 — absent from prior keyword corpus

References: 0xAD34B5 (bufferstring).

```text
Deactivated
```

### 0xAD3C54

References: 0xAD34ED (loadword_then_callstd).

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xAD3B7E — absent from prior keyword corpus

References: 0xAD3E9E (loadword_then_callstd).

```text
System shutdown complete.<PARAGRAPH>

Global power level: {STR_VAR_1}0%.
```

### 0xAD3BB4

References: 0xAEFF12 (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xB01831

References: 0xAEFFDA (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xb01831 — insufficient charge

Candidate entries: 0xAD344E, 0xAEFF09.

68 instruction candidates; 7 referenced strings; 0 unresolved frontiers.

### 0xAD3D3D

References: 0xAD348B (loadword_then_callstd).

```text
Nexus One Status: {STR_VAR_2}.
Global power level: {STR_VAR_1}0%.
```

### 0xAD3EB1 — absent from prior keyword corpus

References: 0xAD34AD (bufferstring).

```text
Activated
```

### 0xAD34C8 — absent from prior keyword corpus

References: 0xAD34B5 (bufferstring).

```text
Deactivated
```

### 0xAD3C54

References: 0xAD34ED (loadword_then_callstd).

```text
Nexus One Status: Activated.
Global power level: {STR_VAR_1}0%.<PARAGRAPH>

Do you want to insert the G Rank?
```

### 0xAD3B7E — absent from prior keyword corpus

References: 0xAD3E9E (loadword_then_callstd).

```text
System shutdown complete.<PARAGRAPH>

Global power level: {STR_VAR_1}0%.
```

### 0xAD3BB4

References: 0xAEFF12 (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

System Control Panel opened.
Starting Shutdown sequence.<PARAGRAPH>

System Error, override detected.
Initiating Intruder Protection.
```

### 0xB01831

References: 0xAEFFDA (loadword_then_callstd).

```text
Inserting G Rank into Nexus One.<PARAGRAPH>

Insufficient charge in G Rank to
activate System Console.<PARAGRAPH>

Please charge G Rank.
```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xa8ebf9 — Nexus One stable NPC

Candidate entries: 0xA5DF20.

10 instruction candidates; 2 referenced strings; 0 unresolved frontiers.

### 0xA8EBF9

References: 0xA5DF29 (loadword_then_callstd).

```text
The Nexus One is running stable.<PARAGRAPH>

There’s no way it can be stopped now!
```

### 0xA5FE20 — absent from prior keyword corpus

References: 0xA5DF34 (loadword_then_callstd).

```text

```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## 0xa8ec41 — machine self-destruction warning NPC

Candidate entries: 0xA60167.

10 instruction candidates; 2 referenced strings; 0 unresolved frontiers.

### 0xA8EC41

References: 0xA60170 (loadword_then_callstd).

```text
If you try and stop the Nexus One,
the machine upstairs, it’s built to<SCROLL>
mailfunction and destroy itself,<SCROLL>
along with you.<PARAGRAPH>

But, even if you’re able to stop
it, it won’t have any effect!
```

### 0xA61454 — absent from prior keyword corpus

References: 0xA6017B (loadword_then_callstd).

```text

```

### Frontiers

No unsupported opcode/limit frontier in this bounded graph. Standard/native/battle effects are still assumptions.

## Controller entries

Map owners and gameplay reachability remain UNKNOWN.

| Entry | Per-controller flag | Write offset | Incoming pointer sites |
|---|---|---|---|
| 0xAD344E | 0x54B | 0xAD346F | 0xC01900, 0xC18E58 |
| 0xAD354B | 0x54C | 0xAD356C | 0xC04308 |
| 0xAD3D6E | 0x54D | 0xAD3D8F | 0xC04314 |
| 0xAD3D94 | 0x54E | 0xAD3DB5 | 0xC02AAC, 0xC04600, 0xC2611C |
| 0xAD3DBA | 0x54F | 0xAD3DDB | 0xC02AA0, 0xC26110 |
| 0xAD3DE0 | 0x550 | 0xAD3E01 | 0xC04B30 |
| 0xAD3E06 | 0x551 | 0xAD3E27 | 0xC04B3C |
| 0xAD3E2C | 0x552 | 0xAD3E4D | 0xC02974, 0xC32560 |
| 0xAD3E52 | 0x553 | 0xAD3E73 | 0xC02980, 0xC3256C |
| 0xAD3E78 | 0x554 | 0xAD3E99 | 0xC01474, 0xC01480 |

## State operand index

Operands are not an allocation ledger and are not certified unused or mapped to save fields.

| Offset | Format interpretation | Operands |
|---|---|---|
| 0xA5DF20 | checkflag | 0x513 |
| 0xA60167 | checkflag | 0x513 |
| 0xAA0FE0 | compare_var_to_value | 0x800D, 0x1 |
| 0xAA2C5D | checkflag | 0x544 |
| 0xAA2C66 | clearflag | 0x544 |
| 0xAD344F | checkflag | 0x54B |
| 0xAD3458 | checkflag | 0x514 |
| 0xAD3461 | checkflag | 0x513 |
| 0xAD346F | setflag | 0x54B |
| 0xAD3475 | compare_var_to_value | 0x5318, 0x0 |
| 0xAD3496 | copyvar | 0x8005, 0x5318 |
| 0xAD349B | subvar | 0x8005, 0x1 |
| 0xAD34A4 | checkflag | 0x514 |
| 0xAD34D6 | setvar | 0x5318, 0xB |
| 0xAD34DD | compare_var_to_value | 0x5318, 0x0 |
| 0xAD34F5 | compare_var_to_value | 0x800D, 0x1 |
| 0xAD353A | compare_var_to_value | 0x5318, 0x1 |
| 0xAD354C | checkflag | 0x54C |
| 0xAD3555 | checkflag | 0x514 |
| 0xAD355E | checkflag | 0x513 |
| 0xAD356C | setflag | 0x54C |
| 0xAD3D6F | checkflag | 0x54D |
| 0xAD3D78 | checkflag | 0x514 |
| 0xAD3D81 | checkflag | 0x513 |
| 0xAD3D8F | setflag | 0x54D |
| 0xAD3D95 | checkflag | 0x54E |
| 0xAD3D9E | checkflag | 0x514 |
| 0xAD3DA7 | checkflag | 0x513 |
| 0xAD3DB5 | setflag | 0x54E |
| 0xAD3DBB | checkflag | 0x54F |
| 0xAD3DC4 | checkflag | 0x514 |
| 0xAD3DCD | checkflag | 0x513 |
| 0xAD3DDB | setflag | 0x54F |
| 0xAD3DE1 | checkflag | 0x550 |
| 0xAD3DEA | checkflag | 0x514 |
| 0xAD3DF3 | checkflag | 0x513 |
| 0xAD3E01 | setflag | 0x550 |
| 0xAD3E07 | checkflag | 0x551 |
| 0xAD3E10 | checkflag | 0x514 |
| 0xAD3E19 | checkflag | 0x513 |
| 0xAD3E27 | setflag | 0x551 |
| 0xAD3E2D | checkflag | 0x552 |
| 0xAD3E36 | checkflag | 0x514 |
| 0xAD3E3F | checkflag | 0x513 |
| 0xAD3E4D | setflag | 0x552 |
| 0xAD3E53 | checkflag | 0x553 |
| 0xAD3E5C | checkflag | 0x514 |
| 0xAD3E65 | checkflag | 0x513 |
| 0xAD3E73 | setflag | 0x553 |
| 0xAD3E79 | checkflag | 0x554 |
| 0xAD3E82 | checkflag | 0x514 |
| 0xAD3E8B | checkflag | 0x513 |
| 0xAD3E99 | setflag | 0x554 |
| 0xAD3EAA | clearflag | 0x175A |
| 0xAD3EAD | setflag | 0x514 |
| 0xAEFF09 | checkflag | 0x544 |
| 0xAEFF22 | setwildbattle | 0x7D, 0x64, 0x0 |
| 0xAEFF2C | subvar | 0x5318, 0x1 |

## Charge flag signature audit

All-ROM byte signatures only. A signature can occur in data; absence does not exclude native code, indirect flag IDs, or RAM scripts.

setflag 0x0544: no literal signature found.
clearflag 0x0544: 0xAA2C66.
checkflag 0x0544: 0xAA2C5D, 0xAEFF09.

## Engine comparison limitation

extracted/pointers/engine_handler_probe.json; candidate table/code-byte comparison only; modified handler intervals are not treated as verified reference semantics

Used opcode handler intervals differing from the reference: 0xB6. The wild-battle tuple remains an encoded-format observation; hooked native behavior is unresolved.
