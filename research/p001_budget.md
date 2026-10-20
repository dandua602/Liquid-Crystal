Current proposal: see patch_spec.md / design/p001.json and space_ownership.md.
Text uses 402/512 bytes, event tables 178/256, party 96/96; scripts have 640 and
reserve 544. The underlying preflight remains below; allocations await review.

# P001 bounded byte budget

BOUNDED_STATIC_SCREEN_PASS; proposed budget only, no allocation or implementation

The original 4 KiB threshold was a screening choice, not a demonstrated patch requirement. A 2 KiB data-only slice offers 31 guarded windows. Select 0xB9EF00–0xB9F700 as the review candidate inside the 3,944-byte screened interval 0xB9EE78–0xB9FDE0. It has no raw 08–0D target shape at any byte alignment within the interval or 256-byte guards. All 2,048 bytes are FF.

Unlike the earlier 4 KiB candidate near 0xCA0000, this proposal is outside the entire conservatively excluded 0xC00000–0xD00000 cartridge bank. It requires no ROM expansion, driver change or field-menu extension. This improves the candidate; it does not prove every computed address or hidden asset extent absent.

| Proposed block | Start | Capacity |
|---|---|---:|
| scripts | 0xB9EF00 | 640 |
| text | 0xB9F180 | 512 |
| room_event_tables | 0xB9F380 | 256 |
| trainer_party | 0xB9F480 | 96 |
| reserve | 0xB9F4E0 | 544 |

Room tables have a 256-byte envelope; trainer party has 96 bytes for six 16-byte records if the final team requires custom moves/items. The exact mechanic and text must fit these budgets or explicitly reopen allocation review. Preserve map blocks/tilesets by default; geometry changes are not included.

Trainer row 929 at 0xAC8EAC is separately proposed (40 zero bytes), not allocated. The largest direct trainer ID in the bounded 1,247-command catalogue is 928. Computed/native ID use remains a distinct unresolved ownership gate. Neither generic Elite team is adopted as the missing Mister R team.

Before implementation: approve final story/mechanic, close ownership/extent and migration questions, then freeze exact hook replacements and expected bytes. A future builder must reject overflow, stale inputs, unexpected bytes and writes outside the manifest. This script creates no patch or output ROM.
