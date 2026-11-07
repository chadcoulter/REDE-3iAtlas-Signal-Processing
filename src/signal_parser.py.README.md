# SignalParser

`signal_parser.py` has two explicit parser methods:

- `parse_hebrew(source)` preserves the source and emits ordinary Hebrew gematria
  values. Final forms share their ordinary-letter values: ך=20, ם=40, ן=50, ף=80,
  and ץ=90.
- `parse_greek(source)` preserves the source and interprets Greek characters using
  the REDΣ Book II transform alphabet. Uppercase resolves the observable; lowercase
  resolves the hidden.

Both methods retain whitespace, punctuation, repeated characters, vowel marks,
cantillation, and unknown glyphs as structural tokens. Neither method supplies a
text-specific channel layout, register model, file I/O, or CPU instruction lowering.
The generic `parse(source, mode=...)` accepts either `hebrew` or `greek`.

For Hebrew, `derive_checksum_triples()` produces one aligned frame for every
adjacent gematria pair using the configured formulas:

```text
SUM     = (g1 + g2) % 231
LINEAR  = (g1 * 22 + g2) % 231
PRODUCT = (g1 * g2) % 231
```

`reconstruct_from_triples()` enumerates candidate pairs and chains them through the
shared middle value, retaining every surviving path instead of guessing. By default
it returns canonical Hebrew glyphs for recovered values; final-form selection needs
an additional orthographic rule because final and ordinary forms share gematria.
