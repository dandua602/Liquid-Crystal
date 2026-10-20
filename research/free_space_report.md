# Active P001 review allocation

The proposed 2 KiB interval B9EF00–B9F700 now has a bounded static certificate:
all raw ROM alias/alignment targets, 256-byte guards, positive adjacent native
table bounds and the nearby inherited-audio false pointer are reviewed in
space_ownership.md / extracted/maps/space_ownership.json. This certificate excludes
unknown computed/unindexed owners and real hardware. It supports the stated
prototype design scope; no actual allocation/write occurs before review.

Exact capacities and expected bytes are in address_ledger.md and design/p001.json.
Do not substitute the earlier save-adjacent 4 KiB candidate or expand the ROM.
The older generated inventory below is retained as historical preflight evidence.

# ROM-space preflight

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`; 16,777,216 bytes.

No free ROM/state certificate and no allocation. Candidate-root scan has frontiers; raw pointer/padding tests do not establish native/computed absence.

| Candidate FF range | Bytes | Aligned start | Incoming target addresses |
|---|---:|---|---:|
| 0xF10160–0xFF0008 | 917160 | 0xF10160 | 1935 |
| 0xCC0380–0xCFFEF0 | 260976 | 0xCC0380 | 203 |
| 0xC416F8–0xC71900 | 197128 | 0xC416F8 | 214 |
| 0xBB7908–0xBE0000 | 165624 | 0xBB7908 | 172 |
| 0xC9C000–0xCC0000 | 147456 | 0xC9C000 | 62 |
| 0xEE0230–0xF00000 | 130512 | 0xEE0230 | 176 |
| 0xEC3F4C–0xEE0000 | 114868 | 0xEC3F4C | 120 |
| 0xBE2134–0xBF86A0 | 91500 | 0xBE2134 | 49 |
| 0xFF0038–0xFFFFC3 | 65419 | 0xFF0038 | 294 |
| 0xF00E00–0xF10000 | 61952 | 0xF00E00 | 91 |
| 0xEB2830–0xEC0210 | 55776 | 0xEB2830 | 43 |
| 0xC72EA8–0xC80000 | 53592 | 0xC72EA8 | 27 |
| 0xB90923–0xB9D000 | 50909 | 0xB90924 | 11 |
| 0xB865D6–0xB90900 | 41770 | 0xB865D8 | 15 |
| 0xBB02F8–0xBB78C0 | 30152 | 0xBB02F8 | 25 |
| 0xBF8AE4–0xC00000 | 29980 | 0xBF8AE4 | 13 |
| 0x2CD1CC–0x2D235C | 20880 | 0x2CD1CC | 25 |
| 0xBAAE88–0xBB0000 | 20856 | 0xBAAE88 | 11 |
| 0xB7B873–0xB80000 | 18317 | 0xB7B874 | 5 |
| 0xC3B440–0xC3E59C | 12636 | 0xC3B440 | 5 |

There are 45 FF runs of at least 4 KiB. These are candidates, not reservations. No candidate has been overwritten.

ROM expansion is a proposal only. There are 71,496 raw 09-prefixed four-byte shapes; most can be arbitrary data. They require classification before claiming old mirror-address behavior is irrelevant.

The image-specific cartridge driver writes its bank selector at 0x09000000 and programs an embedded save at 0xC80000–0xCA0000. That save window is active storage, not asset space. Preserve it and review cartridge behavior before expanding the image. See save_hardware.json.

A final allocator must enforce input hashes, expected original bytes, bounds/alignment, nonoverlap and a changed-range allowlist. It must not automatically select the largest FF run.

The later all-mirror/unaligned guarded screen is retained separately in [allocation findings](allocation_findings.md). Its one 4,942-byte window is adjacent to active cartridge storage and remains unallocated; candidate trainer row 929 is also unreserved. Do not interpret either screen as a free-space certificate.

The subsequent concrete 2 KiB budget produces 31 guarded windows under the same all-mirror/alignment screen. Proposed 0xB9EF00–0xB9F700 avoids the entire conservatively excluded cartridge bank. See p001_budget.md; this is a more useful candidate for the small first slice, with no allocation or exhaustive ownership claim. The original 4 KiB results above remain unchanged at their stated threshold.
