# Bounded allocation evidence

No allocation or free-space certificate. Runtime state fixture is separate from address ownership; computed pointers and asset extents remain review gates.

## Trainer state and candidate row

Native command 60/get, 61/set and 62/clear are patched to the same inverted-bit store as the battle get/set callbacks. The store base is 0x0203D000; zero means defeated. These are independent of ordinary story flags with the same numeric ID. Exact native bytes and script-command table identities are checked before reporting this result.

Candidate trainer 929 has a zero 40-byte row at 0xAC8EAC. Its zero span ends at 0xAC9D80, where real text/script data resumes; the earlier 1,024-row scan is not a table-capacity certificate. None of the 1247 bounded trainerbattle sites uses this ID. Computed/native IDs and ownership remain unproven. No trainer ID is reserved.

The disposable runtime experiment uses native clear/set/get, verifies one changed byte and independence from ordinary story flag 929, then uses actual game Save and a fresh emulator process. Candidate bit 929 and temporary room value 0x5331=2 persist. These are storage checks, not proof of unused IDs, migration compatibility, battle behavior or authored content.

## ROM screen

All byte offsets; raw 08–0D words normalized to this 16 MiB image, including Thumb low bits conservatively. Not decoded references.

This strengthens the earlier 08-only pointer screen. It excludes a 256-byte neighborhood of each raw target and the active cartridge driver/save windows. FF bytes and missing pointer shapes remain insufficient to certify space; a computed pointer or asset extent may still cross a window. No ROM expansion or allocation is performed.

| Largest screened windows (exclusive end) | Bytes | Reserved |
|---|---:|---|
| 0xCA58B4–0xCA6C02 | 4942 | no |

The only surviving 4 KiB window is 0xCA58B4–0xCA6C02. Its enclosing FF run also overlaps the active embedded-save area. Although the window itself is outside the observed save range, broader NOR reservation/erase extents remain unverified. It is not a safe default allocation. Boundary word shapes are retained, including unaligned overlaps; they are not promoted to real pointers.

Review gate: the final design must supply a concrete byte budget, classify boundary references/asset extents and cartridge reservations, then list exact expected bytes and allowed writes in the builder manifest. Neither this interior candidate nor 32 MiB expansion is certified.
