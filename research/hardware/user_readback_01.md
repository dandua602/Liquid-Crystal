# Uploaded cart backup: preserve differences, hold patching

The user supplied a32 MiB ROM and128 KiB save as backups from the working cart,
explicitly asking us to allow for cartridge-specific configuration. The files
are retained unchanged outside the repository. Neither upload is published.

## Findings

- ROM SHA256: `5ea09f6bb4c7362ff32c3adc6edb0f4ab5948e4cbe290e6018b89ecc5ab9d817`.
- Save SHA256: `e5f8ea3973dfbc23fe7a63830d8f142554975d8b39b1b215e7777fbe56c6c8d8`.
  It is byte-identical to the previously generated pre-puzzle warehouse fixture,
  not a saved Mister R victory. Both slots pass all native LC checksums, with
  generations38/37. The newest location is warehouse6:31, position14,9.
  Whether this file was freshly dumped or selected from earlier downloads has
  been asked; no answer has yet been supplied.
- Before offset`0x7B400`, the ROM matches the expected warehouse test image
  except its startup instruction and two header bytes at`0xBE–0xBF`.
  Observed startup branches directly to`0x08000204`, whereas the original
  supplied conversion branches to its startup hook at`0x08C72000`.
  This is a relevant observed difference; its provenance is not established.
- From`0x7B400` through the end of the first16 MiB, every even-addressed byte
  has bit6 set, including varied code/data. The same reference region contains
  4,019,838 words with that bit clear. This broad forced-bit pattern makes the
  read unsuitable as a verified patch base. It does not distinguish a read/
  transport problem from damaged stored data, or identify a chip fault.
- The actual read's native save-layout table fails identity validation. The
  known conversion-driver area and its expected embedded-save window read FF.
  The separate save does not match that window. These bytes cannot establish
  the current cart's actual saving method while the read is suspect.
- The upper16 MiB is entirely FF. Padding alone is not a corruption diagnosis.
  P002/P002a hashes reject this ROM; that safeguard remains in place.

The exact garbled battle still has not been reproduced. Neither this read nor
the old fixture proves that the user's live save is corrupt. No ROM repair,
save edit, new output ROM or cart write was performed.

## Next capture

Preserve these files. Reconnect the reader with the cart reseated. The pinned
[FlashGBX5.0.1 troubleshooting guidance](https://github.com/lesserkuma/FlashGBX/blob/5.0.1/README.md#troubleshooting)
recommends clean contacts/stable USB and **Analyze Flash Cart** before Backup ROM
or Save Data on reproduction carts. Use the current compatible profile; do not
guess another chip or restore an old save.

Make two separate full32 MiB **Backup ROM** captures without writes or intervening
gameplay, plus a separately named **Backup Save Data** capture. Compare the two
ROM hashes and the bit-pattern diagnostics. Two identical reads alone do not
certify valid data. Obtain the actual FlashGBX save result/log if save export
fails; do not substitute the old downloaded fixture. A clean recognized image
can use P002a; a clean unknown conversion must be investigated and preserved
before adapting the one-word safety change. Do not normalize it to the old
driver by assumption.

## Reproducible read-only inspection

`tools/inspect_cartridge_readback.py READBACK.gba --save CURRENT.sav --output NEW.json`
accepts unknown conversions, records layout rejection without aborting, reports
the varied-data fixed-bit suffix and checks the separate save against the stated
reference layout. Output uses exclusive creation. The report is
[user_readback_01.json](../../extracted/runtime/cartridge/user_readback_01.json).
Two focused diagnostic tests cover the fixed-bit pattern, FF-padding exclusion
and handling an unknown native-layout table; all161 project tests pass. No full story replay is needed for
this read-only diagnostic change.
