Current design note: the original 2/3 state proposal below is superseded by
reviewed-as-proposed tags 3302/3303 (hex). See patch_spec.md and flag_var_ledger.md.
The underlying raw-shape ownership findings remain unchanged.

# Mister R state ownership review

Prefer a reviewed extension of room-owned variable 0x5331 for P001, preserving original 0/1 semantics, rather than treating unrelated flags as free. Values 2/3 are design proposals only, not allocated.

All four unresolved raw instruction shapes are inside inherited asset-format spans. No additional supported state handler is established. Computed IDs/native paths and out-of-scope scripts remain unknown; this is not global absence or a hardware/save-ABI certificate.

| Raw instruction shape | Enclosing inherited asset | Classification | Same as FireRed |
|---|---|---|---|
| 0x52AFF4 | 0x52A3C0–0x52B159 | INHERITED_POINTER_BACKED_AUDIO_FORMAT | yes |
| 0x553EC9 | 0x553108–0x554198 | INHERITED_POINTER_BACKED_AUDIO_FORMAT | yes |
| 0x611485 | 0x60FEB0–0x6124C7 | INHERITED_POINTER_BACKED_AUDIO_FORMAT | yes |
| 0x70EFA3 | 0x703C40–0x71A034 | INHERITED_VALIDATED_LZ77 | yes |

Three shapes are within type-1 compressed WaveData spans with two independent ToneData references each. The fourth lies in a validated LZ77 stream beginning 0x703C40; its entire compressed payload matches FireRed. That stream has no discovered absolute header pointer, which is why the earlier pointer-only classification left it unresolved.

The existing room frame condition and introduction remain the supported owners of 0x5331; the introduction writes 1. The linked game-save/fresh-process replay already proves persistence of that existing value. Extending this owned variable can avoid a new save-layout field or an unrelated new flag, but new values and migration behavior still require architecture review.

Proposed state contract: 0 preserves the original intro; 1 means introduced/puzzle pending; 2 means puzzle solved/battle retry available; 3 means won/completed. Unknown values take a safe recovery path without replaying the intro, granting rewards or marking victory. No state values are changed by this audit. The missing mechanic, team and trainer/asset allocation are still unresolved.
