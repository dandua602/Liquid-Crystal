# P001 address ledger — proposed for review

No ROM bytes have been written. Exact input hash, native ownership scope and
acceptance risks are in patch_spec.md and space_ownership.md. All original/source
files remain unchanged. These targets are reserved only upon design approval.

| Existing write site | Expected original bytes | Proposed replacement |
|---|---|---|
| 0xC30A24 | `a4 0f c3 08` | 0x08B9F380 |
| 0xC30A28 | `14 aa c0 08` | 0x08B9F418 |

| New data block | Proposed range (exclusive end) | Expected bytes |
|---|---|---|
| Scripts | B9EF00–B9F180 | FF |
| Added text | B9F180–B9F380 | FF |
| Event/map tables | B9F380–B9F480 | FF |
| Party | B9F480–B9F4E0 | FF |
| Reserve | B9F4E0–B9F700 | FF; remains unused unless explicitly budgeted |
| Trainer row 929 | AC8EAC–AC8ED4 | 40 zero bytes |

Table starts: event header B9F380; three objects B9F394; five BGs B9F3DC;
map-script table B9F418; tag-4 condition B9F428. Original warp pointer is retained.
Copied records change only object 1's interaction and sign BG 1's interaction;
new rock object 3 is added. The builder resolves script/text labels within the
reviewed capacities and rejects overflow. Original intro/condition/warp/layout/
blocks/tileset data remain untouched. No cartridge-bank or engine write is allowed.
