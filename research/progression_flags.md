# Observed Orange progression state

These IDs are active state, not an allocation pool. Meanings describe the inspected paths; normal story eligibility and persistence are separate questions. `CONFIRMED_IN_ROM` covers the literal operands and scripts; the runtime column covers explicitly initialized emulator states.

| ID | Evidence / role | Runtime status |
|---|---|---|
| var `0x5305` | Route 54 frame condition zero → `0xA7094D`; set to 1 | Both `3:101` / `3:107` scenes complete |
| flag `0x52E` | Hides Route 54 local objects 5/6 | Set by both tested scenes |
| flag `0x513` | Mister G progression; controller rank-access branch | Forced in controller fixtures; separately earned by laboratory battle/dialogue in linked replay |
| flag `0x514` | Shared Nexus deactivated/status gate | Set when final fixture counter reaches 1 |
| flag `0x544` | Charge unavailable when set; charger clears it | Rejection and charging tested; remains clear after battle escape |
| var `0x5318` | Shared controller counter; display is `(value−1)×10%` | 11→10 and 2→1 tested through real battle escapes |
| flags `0x54B–0x554` | Ten controller identities | First controller set after escape and guarded on repeat; second accepts without recharge; all ten placements not played |
| flag `0x175A` | Cleared by shutdown completion path `0xAD3EAA` | Cleared in final-controller fixture; broader story purpose unknown |
| var `0x5315` | Nexus Laboratory `5:102` frame intro condition | Linked replay completes battle/dialogue and sets it to 1; G Rank awarded |
| var `0x5331` | Mister R room introduction, zero → 1 | Linked journey and fresh-process reload preserve intro value 1; completion handler unresolved |
| flag `0x5C5` | Mister R object 1 visibility | Introduction sets it and removes the object; returning battle path unresolved |

Controller script identities remain `0xAD344E`, `0xAD354B`, `0xAD3D6E`, `0xAD3D94`, `0xAD3DBA`, `0xAD3DE0`, `0xAD3E06`, `0xAD3E2C`, `0xAD3E52`, `0xAD3E78`, corresponding in order to flags `0x54B–0x554`. Their 17 BG owners are preserved in `research/orange_map_inventory.md`.

LC extended-variable native evidence establishes IDs `0x5000–0x5562` at RAM `0x0203D400 + 2×(id−0x5000)` in this snapshot. These addresses are not source-save offsets, and the range is not free state. A future ledger must audit literal and native/computed uses and load/save behavior before allocating any ID.

Linked replay additionally earns police rescue flag `0x5BA`, Old Key item `0x116`, warehouse unlock flag `0x5C1`, and Mister R visibility flag `0x5C5`. These flags, the key and existing extended variable `0x5331` survive a genuine game save/fresh-process reload. This does not certify every extended variable or any proposed new state.

Entry replay: `0x1701` is explicitly initialized Oak eligibility; Oak naturally sets authorization `0x1702`, the office sets stamp `0x1778`, the first gate sets `0x1873`, the actual Kyogre encounter sets `0x9B`, the electric restart sets `0x1779`, and arrival sets `0x5301=1`. Initial flags/party/map anchors are documented in entry_progression_findings.md; later completion flags are not injected. Timetables, return journeys and a complete normal pre-entry playthrough remain untested.

State design: prefer extending owned `0x5331` (original 0/1; proposed 2 solved/3 completed) after migration/architecture review. This is a proposal and no allocation. See mister_r_state_review.md for why the four former raw-shape leads do not establish other state handlers.
