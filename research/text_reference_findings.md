# Step 2 milestone: text boundaries and references

## Completed

Reverified the three source hashes against the locked baseline. Replaced the first pass's nearest-FF text boundaries with pointer-backed, control-aware candidates and explicitly provisional suffix recovery. Searches now ignore English letter case, retaining exact original bytes/case in reports. Added bounded linear script-format traces for five messages.

The audit has 2,372 keyword hits (including separately declared supporting terms): 2,319 accepted into 1,384 text blocks, and 53 unresolved. Of those blocks, 318 match specific research seeds; this does not mean all 318 belong to Orange Islands. Proper names can refer to earlier-game events. Across the full corpus, 1,074 blocks have script-operand shapes, 183 only raw pointers, and 127 no absolute pointer found. Counts supersede the initial pass, which missed uppercase text and duplicated some suffixes.

## Concrete evidence

All offsets below are ROM file offsets, not CPU addresses. CONFIRMED_IN_ROM means the bytes exist. Reading these structures as FireRed commands is STRONGLY_INFERRED from the pinned engine reference and matching instruction layout; LC command-handler identity and runtime behavior remain unchecked.

| Text start | Present text/topic | Pointer operand site | Message command candidate | Bounded format path |
|---|---|---|---|---|
| `0x930C7D` | Mandarin gym / Rudy / The Mysterious Playboy | `0x9302ED` | `0x9302EB` | Incoming pointer at `0xC227B8` targets `0x9302EB`; uninterrupted loadword/callstd/release/end sequence |
| `0xB11C47` | Sea Ruby Badge described as second Official Orange League Gym Badge | `0xB0FFE4` | `0xB0FFE2` | Incoming pointer at `0xB0FF9F` targets `0xB0FFE2`; message-shaped sequence followed by setflag `0x575`, release, end |
| `0xB1D4E0` | Mister G explains Commanding Rank / Nexus One / charging | `0xAAAFBC` | `0xAAAFBA` | From incoming target `0xAAAF9A`, decoder traverses earlier message and trainerbattle-shaped command to this message |
| `0x9E2B2D` | Oak receives GS Ball and suggests Orange League | `0x9D60E3` | `0x9D60E1` | Incoming pointer at `0x9D60AB`; message-shaped sequence followed by item-removal/setflag-shaped commands and end |
| `0xA9C482` | Route 59 sign links Mandarin, Science Complex, Route 60, Old Warehouse | `0xA9C479` | `0xA9C477` | Incoming pointer target yields uninterrupted message/release/end format |

`setflag 0x575` above is an operand interpretation, not certification that it is a badge flag. Full save-state meaning belongs to Step 4. Incoming pointer sites have not been classified as map event roots. Calls/native effects/trainer battle continuation are not simulated. No gameplay path or event status has been certified.

## Surviving dialogue variants

CONFIRMED_IN_ROM:

- A Mister G speech candidate at `0xABB58A` ends by saying that anyone with Commanding Rank keys can disable the machines. Its start is inferred, and its only raw interior pointer hit is unclassified. There is no recognized text operand for that parsed extent in this audit.
- The version at `0xB1D4E0` instead says the keys need power and that the machine on the desk can charge them. It has a loadword/callstd-shaped reference at `0xAAAFBA`.
- Scientist dialogue candidates at `0x93030B` and `0x93082C` describe Nexus taking over Mandarin and the Science Complex north of the city. The latter has a recognizable message operand; the former has only unclassified interior pointer evidence.
- Oak calls after the second Orange badge and asks to discuss the GS Ball. Variants at `0xB12063` and `0xB121A6` are both message-referenced (operands `0x94F4A9` and `0x94F4BF`). The reference shapes alone do not identify which conditions choose them.

These differences are evidence to preserve, not grounds to delete a copy or choose an intended chronology. No variant has been certified obsolete, unused, unreachable, or broken. The broader JSON records 94 groups of exactly equal plain text after control removal/whitespace normalization; edited variants are kept separate.

## Encoding and validation

Engine reference: pret/pokefirered commit `037335f4c725d7c9aecdac87066f2002b4bd7e14`; URLs and individual SHA-256 hashes are in `references/manifest.json`. It supplies character/control definitions and command formats only. No Liquid Crystal address was inferred from FireRed's addresses.

The codec now handles Pokémon's é, arrows, %, &, FC control arities, and FD placeholders, with source offsets/raw bytes retained per token. It distinguishes FF parameters from EOS. Unknown controls, unsupported font modes, or unsuitable boundaries remain unresolved rather than being guessed. Strict English is a candidate-selection heuristic and can reject legitimate non-English/custom text. Some inferred suffixes still have questionable prefixes; those are explicitly provisional.

Fourteen tests pass, covering control parameters containing FF, truncation, unknown controls, placeholders, false keyword hits in control arguments, unaligned pointers, trainer operands, uppercase dialogue, actual ROM examples, uninterrupted trace boundaries, and correspondence of generated token/pointer offsets to source bytes. No ROM boot, save loading, or gameplay tests were run.

## Files

- `tools/gba_text_codec.py`: control-aware decoder using the retained character reference.
- `tools/pointer_scan.py`: all-alignment raw pointer index and operand-shape classification.
- `tools/text_extract.py`: repeatable corpus, boundary, reference, duplicate, and unresolved-hit audit.
- `tools/text_reference_trace.py`: five selected bounded linear format traces.
- `extracted/text/orange_text_audit.json`: full evidence and unresolved cases.
- `extracted/pointers/selected_text_traces.json`: instruction bytes and incoming pointer sites for selected messages.
- `research/orange_text_index.md`: expanded research-seed text index.
- `tests/test_text_analysis.py`: 14 passing regression/integrity tests.

## Next bounded step

Expand the specific text-reference clusters to adjacent non-keyword messages and validate their script entry paths. Step 2 remains in progress; map ownership, complete chronology, indirect references, and orphan/unused classification are still open. Do not start story authorship or ROM patching.
