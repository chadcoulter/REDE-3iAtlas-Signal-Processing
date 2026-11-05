# Historical narrative and V8 TAO resolver sources

## Historical Wow! narrative

[WowDecodeNarrative.md](WowDecodeNarrative.md) was supplied by Chad and imported unchanged from a local file on November 4, 2026. This expanded narrative records the original sequence and identified failed readings and corrections. Its embedded implementation instructions are preserved as historical source text.

- Size: 10,703 bytes.
- SHA-256: `f9e749a06b2bfbafea5f022b5f6d9fce134756684cb5f2aeb5448fa2474a5278`.
- [Analysis and reconstruction gaps](../analysis/WowDecodeNarrative_analysis.md).

## V8 TAO resolver sources

Retrieved November 4, 2026 from `chadcoulter/RODOE-Token_POC`, branch `main`. These files are preserved as retrieved, with Git blob identifiers below to identify their exact contents.

| Local file | Original source | Git blob SHA-1 |
|---|---|---|
| [v8-resolve-through-monads.md](v8-resolve-through-monads.md) | [docs/tao/v8-resolve-through-monads.md](https://github.com/chadcoulter/RODOE-Token_POC/blob/main/docs/tao/v8-resolve-through-monads.md) | `e6820eb5f5ec2044999b560dae9d0e7aba015d9e` |
| [tao_parser/core.py](tao_parser/core.py) | [src/tao_parser/core.py](https://github.com/chadcoulter/RODOE-Token_POC/blob/main/src/tao_parser/core.py) | `ee0e03216ed5ae82174d369836c65ba272a3ffa3` |
| [tao_parser/types.py](tao_parser/types.py) | [src/tao_parser/types.py](https://github.com/chadcoulter/RODOE-Token_POC/blob/main/src/tao_parser/types.py) | `d078fe8d4580c59644bc8612b4b34043d2ff4c91` |
| [tao_parser/__init__.py](tao_parser/__init__.py) | [src/tao_parser/__init__.py](https://github.com/chadcoulter/RODOE-Token_POC/blob/main/src/tao_parser/__init__.py) | `b786c6fd18436810c723583ce9438cf864cc6930` |
| [tao_parser/serialize.py](tao_parser/serialize.py) | [src/tao_parser/serialize.py](https://github.com/chadcoulter/RODOE-Token_POC/blob/main/src/tao_parser/serialize.py) | `dd8982012a0cbbfa94896374b0f87c058a8fec8e` |

The resolver note describes Theatre, Act, Operate, preservation of information state, sufficient closure, and backward validation. The Python package includes the resolver, types, serialization, and original package exports; it requires Python 3.11 or later because it imports `enum.StrEnum`.

These are candidate sources for understanding V8 TAO. Their equivalence to the historical Wow! implementation remains unconfirmed. The original Wow! numeral/character mappings, traversal choices, and ΛΤϜ operations have not yet been recovered from these files.

No local changes have been made to the copied source files. Keep experiment adaptations elsewhere and preserve these originals for comparison. See [source recovery](../steps/00-source-recovery/README.md).

## Additional versioned operator notes

[Operator notes](operator-notes/README.md) preserve candidate transversal corrections, a current Sigma Math specification, and a working Digamma re-resolution hypothesis. These are comparison sources with differing definition histories, not automatically adopted as the historical Wow! implementation.
