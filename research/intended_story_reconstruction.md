# Evidence-only intended-story reconstruction

Status: bounded reconstruction for the warehouse slice; not a completed whole-game
story or approved continuation. The recovered evidence below is preserved; a separate new design is now proposed after explicit user clarification.
The kickoff document is the user's project instruction, not an original developer
story specification.

| Scene / event | Classification | Supported reconstruction |
|---|---|---|
| Orange authorization and first train trip | CONFIRMED_IN_ROM | Oak authorization, stamped ticket, interrupted train, Kyogre and electric restart lead to Valencia; controlled replay passes |
| Nexus laboratory | CONFIRMED_IN_ROM | Existing Mister G encounter and G Rank award; native game events tested |
| Mandarin antagonist and police rescue | CONFIRMED_IN_ROM | Mister R declares opposition; existing Elite encounters and Old Key rescue precede the Route 59 warehouse |
| Warehouse introduction | CONFIRMED_IN_ROM | Mister R says he blocked the way, offers a battle after solving his puzzle, then departs; original script sets 5331=1 and removes object 1 |
| Damaged clue | CONFIRMED_IN_ROM | Original damaged text survives at 9761E0; it is not a complete instruction |
| Iron Tail / red rocks reading | STRONGLY_INFERRED | Plausible reconstruction of the damaged clue; no working native field-menu action or room completion handler recovered |
| Warehouse local completion gap | STRONGLY_INFERRED | Audited default-room roots and tested interactions do not supply the promised puzzle/battle; native/computed paths remain outside this scoped negative evidence |
| Future Mister R team, reward, next destination | Unresolved | None established by the surviving scoped evidence; do not substitute generic Elite teams, invent a reward or reroute the existing stair |

CONFIRMED_IN_ORIGINAL_PROJECT_DOCS: none yet for the missing warehouse mechanic,
team or destination. After the network draft was published, direct original-site,
archive and search requests still returned proxy tunnel 403. Reachable GitHub
repository/issue searches recovered no relevant specification; the one repository
result contains an emulator page and ROM file, not developer story documentation.
No ROM was downloaded from that result. See external/source_lookup_02/.

NEWLY_AUTHORED: the user explicitly requested preparing a new design for review.
The separate P001 proposal adds a boulder/Iron Tail interaction with Rock Smash
fallback, a new six-Pokémon Mister R team, short new dialogue, retry and state
recovery behavior. None is presented as recovered original intent. The original
intro, clue and exits remain. See design_review.md, patch_spec.md and
design/p001.json. This authorization does not approve ROM implementation; the
kickoff's completed-design review remains required.
