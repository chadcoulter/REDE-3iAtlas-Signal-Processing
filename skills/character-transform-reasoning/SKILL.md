
# Character Transform Reasoning — governed adaptation

## Authority and references
- Treat `references/book-ii-alphabet.txt` as the verbatim operator authority (REDΣ Set Calculus Book II, Chad Coulter, 2026-10-13, v0.1). Never revise Book II definitions as a side effect of evaluation.
- Read `references/governance-v0.4.md` for the adaptation of Governance-Driven Resolution Lattice v0.4; consult `references/governance-v0.4-source.docx` when exact source definitions are needed.
- Read `references/resolution-contract.md` for state format, typed operator/measurement namespaces, gates and validation.
- Preserve the author's ownership, exact terms and original input; distinguish source definitions from inferred readings.

## Execute
1. **Receive H.** Capture the user's original text verbatim as human request H, its interpretive purpose, scope, explicit overrides, and required output. Do not autocorrect, normalize, suppress repetition, or repair unusual glyphs.
2. **Freeze G per cycle.** Select Book II operator authority and explicit user-governed constraints; set materiality predicate, equivalence, priorities, Enough Boundary, and resource budget. Hold G fixed for the cycle. A user-authorized G revision starts a new cycle retaining prior trace.
3. **Segment.** Iterate Unicode code points in source order. Each occurrence (including spaces, punctuation, combining marks and repetitions) has a unique index. If a grapheme contains multiple code points, retain both the grouped display and component occurrences.
4. **Select mapping.** Detect Greek glyphs directly. For Latin input, show the selected Latin→Greek mapping as an explicit, fallible intermediate representation; retain other plausible mappings. Never assert an invented canonical mapping as Book II. Keep Koppa distinct from Kappa.
5. **Execute transforms.** Apply each operator sequentially against the evolving relational state, recording source occurrence, mapped operator, role, action, connected constituents, witnesses, and retained remainder. UPPERCASE tells **how to resolve the observable**; lowercase tells **how to resolve the hidden**. Apply Stigma Ϛ/ϛ (unresolvedness), Koppa Ϙ/ϙ (actor participation), and Kai ϗ (conjunction/composition) according to Book II. Use one-way arrows only for invoked closure or partial closure.
6. **Compose candidate Rn.** Generate an actual sentence-level reading based on the transform sequence. Preserve candidate states, contribution edges, alternatives, residual ambiguity, and provenance in a reversible resolution lattice. Avoid substituting ordinary prose paraphrase for a transform execution.
7. **Evaluate under G.** Apply materiality to distinctions that might affect H. Compare candidates directionally (Better/Same/Worse, or a recorded mixed/unresolved result). Treat equivalence as governance-relative, never as string equality alone. Keep nonmaterial alternatives open rather than deleting them. Keep the operator namespace separate from measurement labels (see contract).
8. **Correct or reverse.** Use feedback to revise, regenerate, recombine, or reverse a selected candidate without erasing any prior candidate or its source. Compare forward and backward with the same frozen G; persist relevant source and target references.
9. **Terminate distinctly.** Return VALID TRANSFORM only after three *consecutive eligible* materially unchanged transitions in the same cycle; SUFFICIENT RESOLUTION when an authorized Enough Boundary is met; INVALID VALIDATION for a failed applicable governance validation; BUDGET EXHAUSTED for a stop without acceptance. Preserve open relations and residuals. Do not fabricate three stability gates by restating the same result; absent real candidate transitions, use Enough or retain UNRESOLVED/IN-PROGRESS as applicable.
10. **Deliver.** Output the transformed reading and the amount of detailed trace the user asked for. Do not introduce unsolicited objections or challenge endings. Do not present a provisional interpretation as demonstrated proof of an external factual claim.

## Output defaults
- For letter-by-letter requests: one row per Unicode character occurrence in order: index, original character, explicit mapping/operator, action on state, resulting relation/remainder; then composed reading, alternative interpretations material to H, and resolution status.
- For conversational requests: preserve the exact original text in internal trace, give concise composed reading with a compact explanation and status. Expand to a full trace if asked.
- If the user supplies their own reading, treat it as a candidate or authorized interpretive constraint according to their wording; preserve prior candidates and evaluate without silently replacing source definitions.
- Distinguish **operator behavior** from **governance measurement**. Chi/Kai can appear in both namespaces but each use must be typed and identified.

## Optional deterministic trace validation
For a saved JSON resolution trace, run `scripts/validate_resolution.py trace.json` to check invariants and gate accounting. It checks record consistency; it does not determine semantic truth or independently certify a transform reading.
