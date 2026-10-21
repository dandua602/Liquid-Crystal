# Hardware validation

P002 is built and emulator-tested. Physical cartridge/console validation is
FAILED as reported: boot corruption/previous-save warning, then stuck Saving.
The user flashes cartridges with FlashGBX and has backups. Root cause unknown.
Collect profile/reader/cart details, an unmodified-ROM saving baseline on the
same cart and a full readback from this failed attempt before further flashing.

Use [HARDWARE_TEST.md](../HARDWARE_TEST.md) for image selection, flashing/readback,
puzzle/battle/Office instructions and the power-off/save/reload checks. Screenshot confirms FlashGBX5.0.1, GBxCart RWv1.4a/b/c family,
AGB-E20-30/S29GL256N10TFI01 (or compatible),32 MiB and unknown save ID0x8209. Preserve the supplied
image's cartridge conversion; do not claim compatibility with another design.

The new [software report](../extracted/runtime/cartridge/summary.json) verifies
boot from actual ROM-embedded save bytes with blank emulated SRAM. It separately
checks native Save and fresh-process boot from updated modeled NOR contents.
Physical flash timing, chip-ID commands and all programmer protocols remain
unverified. Record cart model, flasher/profile, console and exact failing step
when hardware results arrive. ROM reflashing resets the included starting save.

The official profile uses128 KiB NOR sectors. Controlled64/128 KiB model tests
both save with28 valid sections; geometry alone does not reproduce the fault.
Read back the full32 MiB failed cart and confirm original-ROM saving baseline.
