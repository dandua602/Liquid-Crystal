# Save compatibility

Original source save and its 16-byte FlashGBX footer remain unchanged. The supplied ROM's embedded save at 0xC80000–0xCA0000 exactly equals the 128 KiB payload. Its cartridge conversion uses banked SRAM plus NOR programming; standard BPRE flash emulation produced misleading corruption warnings.

The corrected emulator adapter passes clean source loading and a real game save/fresh-process reload in the linked replay. Room 6:31, extended variable 0x5331, flags 0x5BA/0x5C1/0x5C5 and Old Key persist. See research/linked_progression_findings.md and extracted/runtime/linked/linked.json. The generated saves/test fixture is artificial and ignored, with retained metadata; never replace the source with it.

Full LC checksum lengths, all extended variables, power-loss recovery, patched-ROM compatibility and real hardware remain unverified. Standard FireRed checksum mismatch alone is not evidence of damage.
