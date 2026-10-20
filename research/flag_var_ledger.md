# P001 state ledger — proposed for review

Use only existing room-owned 5331 and 5C5, plus proposed trainer 929's separate
native completion bit. No new unrelated story flag/variable is needed. No ROM or
source save has been changed; temporary storage experiments are labelled fixtures.

| Field/value | Proposed ownership/behavior |
|---|---|
| 5331 = 0 | Original intro; restore original actor visibility if mismatched |
| 5331 = 1 | Introduced, puzzle pending |
| 5331 = 3302 hex | New solved/retry tag |
| 5331 = 3303 hex + trainer defeated | New completed tag |
| 3303 hex + bit clear | Recover to solved/retry without granting victory |
| Legacy 2/3 or unknown | Recover to 1 without replaying intro/completing |
| Flag 5C5 | Existing Mister R visibility; hide outside locked scene/initial intro |
| Trainer 929 | Native inverted bit at 0203D074 mask 2, separate from story flag 929 |
| Object 3 flag 0 | Always eligible template; map initialization removes solved rock |
| 800D | Existing transient native result field; special B4 must equal 1 to complete |

Native ownership/persistence evidence is retained in allocation_findings.md,
space_ownership.md and extracted/runtime/design_state/design_state.json. Both
new tags and literal operands round-trip. Actual Save/fresh-process reload preserves
3303 plus trainer bit; 3302 has no independent fresh-save run. The first literal
probe used the wrong command and failed; corrected 1A/VarGet run passes, with the
failed artifact retained (design/validation_notes.md).

The supported source room writes original 1; raw alternate state shapes were
classified as inherited assets. Arbitrary external/cheated saves that mimic the
new tag/bit combination cannot be distinguished. Prototype acceptance must cover
old 0/1, legacy 2/3, inconsistent visibility and new completed/retry saves.
