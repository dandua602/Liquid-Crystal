# New native checksum and hardware report

The user reports boot corruption/previous-save recovery and a saving hang on
hardware. The cause is unresolved. Both original and packaged test saves pass
all28 sector checksums/signatures and both complete slot-ID sets using native
LC layout3FEC94, pinned through consumer literals atDA23C and instructions at
DA1DA. Its lengths are F24, FF0x3, D98, FF0x8,450. This supersedes the older
unresolved checksum-length statement below, not the observed hardware failure.
No checksum repair/re-signing has been applied. A bad data byte in any one of
all28 sections is detected by the new audit regression. Native layout and driver
identity checks are separate; valid save data alone does not prove hardware I/O.

V3 offers an exact raw128 KiB copy of the already embedded test payload. It has
no FlashGBX footer; source metadata stays untouched. A separate save restore is
not established as a fix. Compare a fresh complete ROM readback from the failed
test with the expected game/driver and inspect its embedded payload.

Historical evidence follows.

# Save compatibility

Original source save and its 16-byte FlashGBX footer remain unchanged. The supplied ROM's embedded save at 0xC80000–0xCA0000 exactly equals the 128 KiB payload. Its cartridge conversion uses banked SRAM plus NOR programming; standard BPRE flash emulation produced misleading corruption warnings.

The corrected emulator adapter passes clean source loading and a real game save/fresh-process reload in the linked replay. Room 6:31, extended variable 0x5331, flags 0x5BA/0x5C1/0x5C5 and Old Key persist. See research/linked_progression_findings.md and extracted/runtime/linked/linked.json. The generated saves/test fixture is artificial and ignored, with retained metadata; never replace the source with it.

Full LC checksum lengths, all extended variables, power-loss recovery, patched-ROM compatibility and real hardware remain unverified. Standard FireRed checksum mismatch alone is not evidence of damage.
