# Remaining milestones

**P002 is approved, built, tested and packaged.** Its [walkthrough](../WALKTHROUGH.md)
includes both the warehouse chapter and the new Office service room. See
[implementation](P002_implementation.md) for exact behavior and limitations.

1. **GitHub checkpoint published.** Main now contains the tested P002 patch-only
   download, walkthrough, project tools and research. See [GitHub instructions](../GITHUB.md).
   The user requested ongoing GitHub synchronization. Commit/push tested milestones
   and verify the remote. Cloud environment Publish is separate; use it when setup
   or the prepared filesystem needs a new snapshot, not for each chat turn.
2. **Review concrete P003, then implement the approved chapter.**
   [P003 proposal](P003_review.md) and [draft guide](../walkthrough/P003-preview.md)
   define the attendant shutdown, reuse of existing flag5B2 and a newly authored
   NPC departure. Ten native checks verify original aftermath branches/visibility
   on unchanged P002. A new512-byte bounded screen and compiler preview fit133/192
   script bytes and224/320 text bytes. No P003 implementation approval, output ROM
   or runtime acceptance exists yet. Apply the kickoff review requirement to this
   concrete proposal, then test actual interactions, earned access, city aftermath,
   Save/reload, upgrades and rollback before packaging. Do not restart broad scans.
3. **Use P002a for the newly reported stadium issue.**
   [Fix/evidence](P002a_safety_fix.md) seals the original unsafe stair into0:0.
   [Offline download](../patches/P002a/P002a-safety-fix.zip) uses current ROM/save
   backups without resetting earned progress; saved-inside-stadium or invalid
   data stops for recovery. User is unsure of exact route/last save. Native
   affected checks26, project tests159 and browser checks9 pass. Hardware hotfix
   validation and any actual saved-room recovery remain outstanding.
4. **Earlier console saving issue.** User now says the cart works and they beat
   Mister R; the exact save fix method/power-cycle verification was not provided.
   Historical evidence follows. **If saving fails again, investigate the failed console save test.** User reported corruption/previous
   save recovery and stuck Saving. Screenshot gives FlashGBX5.0.1, GBxCart RWv1.4a/b/c and AGB-E20-30/S29GL256N;
   unknown save ID0x8209 remains. The user confirmed the original saves
   successfully on this exact cart. If that failure recurs, preserve a failed-attempt
   readback before diagnostic writes; do not ask for the baseline again. Both prepared save slots pass native LC checksums; v3 exports the same
   raw test save for diagnosis, without claiming a fix.

   **Prepared console files:** [Hardware guide](../HARDWARE_TEST.md) and
   private `builds/P002-cartridge-test.zip` provide embedded personal, pre-puzzle
   and Office saves. The public helper kit is on GitHub. Three blank-SRAM
   embedded-ROM boots and native NOR Save/fresh boot pass in software; current
   suite155 passes. FlashGBX software confirmed; await reader/cart/profile/console and real power-off/save/
   reload results. Reflashing resets the selected starting save.
5. **Human playtest and broad progression.** P002 passes actual victory,
   loss, old-save upgrade, movement persistence, entry/return, new-map save/reload
   and safe P001 downgrade. These controlled fixtures do not certify difficulty,
   stock-emulator conversion, real hardware or ordinary full-game progression.

Keep walkthrough directions, puzzles, battles, retries, saving, rewards, endpoint
and screenshots synchronized with every newly released story slice. Before
removing P002, leave its new map and save in the original warehouse. Never replace
personal saves with the artificial QA fixtures. Do not rerun unchanged research
or whole journeys merely because another chat turn starts.
