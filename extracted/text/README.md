# Text outputs

`orange_text_audit.json` is the current corpus: source hash, keyword coverage, exact text/token ranges, raw pointer sites, operand-shape candidates, duplicates, and unresolved cases.

`keyword_candidates.json` is retained from the initial incomplete pass for comparison. It used case-sensitive matches, naive boundaries, and a partial codec. Its counts, boundaries, and missing-reference status are superseded; do not use it as the current index.

Regenerate the current corpus with `python3 tools/text_extract.py` from the checkout root. Reported references do not certify runtime reachability.

`dialogue_clusters.json` extends five selected anchors through candidate entry paths and referenced neighboring messages. Generate it after the text and selected-trace audits with `python3 tools/dialogue_cluster_audit.py`. Engine-return/battle edges are explicitly labeled assumptions, not runtime validation.

`nexus_machine_audit.json` records the nine machine/NPC anchors, ten controller entries, counter/charge operands, empty targets and the literal flag-signature audit. Run `tools/engine_reference_probe.py` before `tools/nexus_machine_audit.py`; both use only the Python standard library.

`text_triage_input.json` freezes the original53 misses/64 weak-reference candidates. Run `text_boundary_triage.py` before `text_extract.py` to validate and apply complete reviewed boundaries, then `orphan_reference_audit.py` for supplemental field/reference classifications. Prose anomalies are never promoted to clean terminated strings.
