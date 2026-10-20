# Design validation notes

The first literal-operand probe incorrectly used command 19/copyvar, which reads
through GetVarPointer. Its result did not match the expected literal. This was a
research-fixture error, not an identified ROM defect. The failed artifact remains
at extracted/runtime/design_state/fixture_error_first_attempt.json.

The corrected probe uses 1A/setorcopyvar and native VarGet, the same literal-or-
variable semantics needed by the map condition. The complete corrected run passes
10 expectations, including full-width 3302/3303 values, both literal probes, actual
game Save and fresh-process persistence of 3303 plus trainer bit 929. The original
ROM/save remain unchanged. No failed checks were suppressed or converted into
patch acceptance; no new puzzle/battle has run.
