# Hardware validation

P002 is built and emulator-tested. Physical cartridge/console validation is
pending the user's test. The user flashes cartridges and has backups.

Use [HARDWARE_TEST.md](../HARDWARE_TEST.md) for image selection, flashing/readback,
puzzle/battle/Office instructions and the power-off/save/reload checks. FlashGBX
software is confirmed; physical reader, cart model and profile are unconfirmed. Preserve the supplied
image's cartridge conversion; do not claim compatibility with another design.

The new [software report](../extracted/runtime/cartridge/summary.json) verifies
boot from actual ROM-embedded save bytes with blank emulated SRAM. It separately
checks native Save and fresh-process boot from updated modeled NOR contents.
Physical flash timing, chip-ID commands and all programmer protocols remain
unverified. Record cart model, flasher/profile, console and exact failing step
when hardware results arrive. ROM reflashing resets the included starting save.
