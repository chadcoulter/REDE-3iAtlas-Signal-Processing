# Talking Comet — four-channel Atlas WebAssembly

Source of truth: [atlas_phase_feedback.S](https://github.com/chadcoulter/REDE-3iAtlas-Signal-Processing/blob/codex/atlas-endpoint-phase-test/experiments/endpoint_phase_v1/unified_phase_feedback/atlas_phase_feedback.S), pinned at commit `c0ad2a1d40db7cc3e3b29b833cdb1dcd0622a86c`, blob `f599e1793e856c5023c42976ae3e1b0e2dbb8d90`.

This source contains **four reflection channels**, four projection routines, eight 64-bit registers, and the 100-cycle n+1 phase handoff. It is a fixed-chain executable. The eight source registers are **state, relations, constraints, observations, unresolved, context, target, events**. In particular, the fifth is `unresolved` (not `pattern`).

## Build

From the repository root: `sh talking-comet/build.sh`.

The build downloads the pinned assembly, translates all 8 native operator routines into WASM-compatible C, compiles `atlas_phase_feedback.wasm`, and verifies its full 100-cycle trace (6,400 register words) against the source's independently verified native execution SHA-256. A source blob check prevents silently switching implementations.

Build requires Python 3, curl, clang with wasm32 target, and Node 22. The resulting WASM module is generated locally and deliberately not checked in. Deploy with `cd talking-comet && npx wrangler deploy` after a successful build.

## API

`POST /resolve` with `{"inputs":[4,8,17,28]}` (four unsigned five-bit integers) runs the original fixed reflection/projection operator chains for 100 cycles, using the supplied values as the **initial four phase cells**. The original source's feedback banks remain unchanged. The response contains all eight registers as decimal strings.

**Integration interpretation:** Supplying four five-bit values as initial phase cells is a Talking Comet adaptation; the original standalone assembly has fixed initial phase values and no input API. The `run_reference` WASM export uses the original fixed initial phase and is checked against the native trace. The custom-input path needs independent parity tests against a native assembly build with the same injected phase inputs before it is claimed equivalent.

The Worker instantiates a fresh WASM instance per request, so mutable phase/feedback data do not leak between requests. Application-side name, timestamp, gematria, and 20-bit construction remain outside this API.

The build and verification workflow is configured in `.github/workflows/talking-comet-four-channel.yml`. No production deployment is performed automatically.
