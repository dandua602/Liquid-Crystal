# Step 2 milestone: Nexus One charging and shutdown archaeology

## Completed

Nine dialogue anchors now have candidate entry paths. The connected audit contains 204 distinct instruction candidates and 14 referenced text targets: 12 nonempty strings and two empty FF-terminated targets. Six nonempty strings were absent from the keyword corpus: the charging prompt, charge-success and already-charged messages, Activated/Deactivated buffer strings, and shutdown-complete message. Empty strings are recorded separately and are not counted as recovered dialogue.

Ten controller scripts call the shared insertion-prompt routine. Their per-controller state operands cover `0x54B` through `0x554`; the shared counter is operand `0x5318`. Their map owners and gameplay reachability remain UNKNOWN. These are ten encoded controllers, not ten certified reachable map objects.

No story, ROM patch, or save modification was produced.

## Evidence labels and engine comparison

CONFIRMED_IN_ROM means the bytes, pointers and text are present. Their command/state meanings are STRONGLY_INFERRED using retained FireRed definitions, matching handler code where available, and internally consistent script paths. Runtime behavior is untested.

A reusable probe independently searched both ROMs for adjacent Thumb NOP handlers and references to their pointer prefix. The outer table candidate is at `0x15F9B4` in each ROM; interior candidates are retained as discovery evidence rather than mistaken for additional tables. Of 68 bounded handler-code intervals compared, 64 are byte-identical. The intervals for `0x60`, `0x61`, `0x62` and `0xB6` differ. Equality of these intervals does not establish dispatcher use, helper/native equivalence or complete function boundaries.

`0xB6`, used by the machine sequence, has native hooks. At ROM `0x6C370`, bytes `00 4D 28 47` load and branch through the literal Thumb target `0x087ABFE1`. The later epilogue redirects through literal `0x08F10014`. Those hooks are not executed or fully certified here. The graph labels battle resume as an assumption, and the encoded battle tuple is not a successful battle test. The other modified intervals concern trainer-flag commands outside this selected machine path.

## Charging station

Candidate entry `0xAA0FD8` references prompt `0xAADF68` asking to power up the G Rank. Its yes/no result branch leads to `0xAA2C5D`.

- `0xAA2C5D`: checkflag-shaped operand `0x0544`.
- Conditional branch `0xAA2C60` points to already-charged message `0xAA3280`.
- Other path clears operand `0x0544` at `0xAA2C66`, then references `0xAA5FB1`: “Your G Rank is now charged for one use!”

The shutdown gate also checks `0x0544`, at `0xAEFF09`, and routes its set/condition-1 path to `0xAEFFDA`, which references insufficient-charge text `0xB01831`. These complementary branches support interpreting `0x0544` as an unavailable/uncharged state.

A complete raw byte-signature search found one `clearflag 0x0544` signature, the two check signatures above, and no literal `setflag 0x0544` signature anywhere in the ROM. This does NOT prove the flag is never set: native code, computed IDs and RAM scripts can write it. The one-use consumption mechanism remains unresolved; no gameplay bug is certified from the text/signature discrepancy.

## Shared controller structure

The controller entries are `0xAD344E`, `0xAD354B`, `0xAD3D6E`, `0xAD3D94`, `0xAD3DBA`, `0xAD3DE0`, `0xAD3E06`, `0xAD3E2C`, `0xAD3E52`, and `0xAD3E78`. Each has a distinct check/write pair within `0x54B`–`0x554`, while sharing:

- Operand `0x0513`, also set by the earlier Mister G event: controls whether the insertion-prompt path is offered.
- Operand `0x0514`: selects the deactivated/status-only path.
- Initialization at `0xAD34D6`: `setvar 0x5318, 11` when the counter is zero.
- Display helper `0xAD3496`: copies `0x5318` to `0x8005`, subtracts one, and buffers its decimal digits. The message appends `0%`, so 11 is displayed as 100%, 10 as 90%, and 1 as 0%.

The prompt at `0xAD34ED` references `0xAD3C54`; its accepted path calls `0xAD3507`, which explicitly transfers to `0xAEFF09`. Returning to a used controller instead follows the shared status display. These are static branch interpretations, not proof that all guards can be satisfied in play.

## Intruder protection and shutdown completion

The non-rejection path references `0xAD3BB4`: inserting the rank opens the control panel, the shutdown is overridden, and intruder protection begins.

- `0xAEFF1A`: cry-shaped species operand `0x007D`.
- `0xAEFF22`: wild-battle setup tuple `(0x007D, 100, 0)`, interpreted as species operand, level byte and item operand by the reference format. LC species mapping and hooked native behavior are unverified.
- `0xAEFF28`: wild-battle start opcode; continuation is outcome/runtime dependent.
- `0xAEFF2C`: subtracts one from `0x5318` on the encoded resume path.
- `0xAD353A`: checks whether the counter is 1; the corresponding branch reaches `0xAD3EAA`/`0xAD3EAD`, clearing operand `0x175A` and setting operand `0x0514`.
- Shared completion message `0xAD3B7E` is referenced from `0xAD3E9E`.

STRONGLY_INFERRED: ten successful one-time controller interactions are intended to reduce the display from 100% to 0%, then mark the system deactivated. The ten state flags and counter arithmetic support this interpretation. Map placement, all successful outcomes, repeat interactions and save/reload behavior still need validation before this can be labeled WORKING.

## NPC text and empty targets

Messages `0xA8EBF9` and `0xA8EC41` describe Nexus One being stable and threatening destruction if stopped. Their candidate roots check operand `0x0513`. The alternate text pointers `0xA5FE20` and `0xA61454` point directly to FF, producing empty text. Their purpose is unresolved; empty text alone does not certify a broken or placeholder event.

## Validation and files

All 35 tests pass, including relocated table discovery, ten distinct controller flags, charge/rejection consistency, counter operands, empty-vs-nonempty text accounting, hooked handler detection and exact ROM-byte/pointer checks. The nine selected graphs have no unsupported opcode, limit or overlap frontier. Standard/native effects and battle outcomes remain opaque despite that syntactic completeness.

- `tools/nexus_machine_audit.py`
- `tools/engine_reference_probe.py`
- `extracted/text/nexus_machine_audit.json`
- `extracted/pointers/engine_handler_probe.json`
- `research/nexus_machine_audit.md`
- `tests/test_nexus_machine.py`

The shared graph parser now records buffer-string text and distinguishes empty targets and assumed wild-battle resume. Source hashes and retained reference hashes are unchanged.

## Next bounded step

Triage the 53 unresolved keyword hits and the remaining text-boundary/orphan candidates, especially the Commanding Rank description near `0xAAAF41`, to close the outstanding static text inventory before map archaeology. Keep native charge consumption and controller map ownership as explicit follow-up questions.
