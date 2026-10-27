# What the current four assembly programs do

Analysis covers the exact `channel1_pass100.S` through `channel4_pass100.S` sources and their tested native x86-64 executions. Original files were not changed. Machine behavior below is derived from the instructions, rather than inferred from the descriptive Greek/operator names.

## Overall computation

Each executable is a fixed, unrolled eight-word state machine. Its 2,100 numerical chain values have already been translated into 9,923–11,110 Greek-selected operator invocations. Those operators are expanded inline as x86-64 instructions. Across four channels there are 41,424 operator invocations.

Conceptually:

```text
eight memory cells = the compiled-in seeds
execute the inline arithmetic/operator sequence
write the eight final words to stdout
exit
```

The eight logical registers are memory cells in `.data`: `state`, `relations`, `constraints`, `observations`, `unresolved`, `context`, `target`, `events`. Native RAX and flags perform the temporary arithmetic. Additions and increments wrap at 64 bits. Operations consist of assignment, addition, XOR, swapping two cells, masking to the low byte, and parity/zero tests.

There are no runtime reads of input files, stdin, network, arguments, time or randomness. Seeds and the command sequence are compiled into each ELF. The four executables run separately. The Python runner supplies cross-channel values when generating the next compiled data section and combines their returned target values into the validation vector.

Runtime output is exactly 64 bytes: eight little-endian unsigned 64-bit words in the order listed above. The wrapper calls Linux `write(1, &state, 64)` and then exits zero if 64 bytes were written; its failure branch exits one. There are no function calls, recursion or backward branches. Upsilon contains forward-only local branches testing whether `constraints` is odd.

## Main register roles implemented by the instructions

| Cell | Actual behavior |
|---|---|
| `state` | Reset to one, incremented, combined with relations, XORed, copied from target or swapped with it. |
| `relations` | XOR accumulator using state, target and the event count; conditionally incremented. |
| `constraints` | Receives the low 8 bits of state; can also be incremented. Its zero/parity controls other operations. |
| `observations` | Accumulates state, state XOR relations, and zero-test results. It feeds context through the pattern operator. |
| `unresolved` | Accumulates state XOR target and increments. It does not feed the other seven cells in these operator bodies. |
| `context` | Incremented or overwritten with observations XOR relations; contributes to projection and form calculations. |
| `target` | An output selected from state, state+1, state+context, state+relations+constraints, state XOR context, or a swap. |
| `events` | Initial count plus the number of Iota operators, modulo 2^64. Indexed-relation operators read it. |

The exact 27-operator machine-effect table is saved in `assembly_analysis_pass100/operator_semantics.csv`. The names describe the experiment's operators; for example, the machine operation called observation is arithmetic over existing cells, not a runtime sensor read.

## Why the final targets are 2, 1, 5, 1

Tracing every operator identifies the final target assignment in each program:

| Channel | Final assignment | State at assignment | Final target | Chain value index |
|---|---|---:|---:|---:|
| 1 | Nu: `target = state + 1` | 1 | 2 | 2003 |
| 2 | Eta: `target = state` | 1 | 1 | 2007 |
| 3 | Nu: `target = state + 1` | 4 | 5 | 2007 |
| 4 | Eta: `target = state` | 1 | 1 | 1999 |

Indices are zero-based in the complete 2,100-value chain. Original recording values occupy indices 200 through 1999. Channels 1–3 make their last target writes in transient generated back values; channel 4 makes its last target write in the last original recorded value. Later repeated tails do not overwrite target.

The last assignment for channel 1 is in the encoding of `4339781448502755133`; for channel 2, `10104003543691758907`; for channel 3, `11983556121188428252`; for channel 4, `231168`. Full before/after states and source-block line numbers are in `assembly_analysis.json`.

The vector is a computed result under the present seeds. In a native test changing only channel 3's compiled `events` seed from 68705 to 68704, its target changed from 5 to 6. This is one tested perturbation, not a complete characterization of arbitrary inputs.

## What the repeating regions execute

The left output has two words per channel. The final repeating pairs are:

| Channel | Front pair | Machine effect of a pair | Consecutive copies at the front |
|---|---|---|---:|
| 1 | `[1,0]` | Alpha resets state to one; zero emits no instruction. | 92 |
| 2 | `[1,5]` | Alpha resets state; Epsilon adds one to observations only if constraints is zero. | 37 |
| 3 | `[1,6]` | Alpha resets state; Stigma increments unresolved. | 93 |
| 4 | `[1,48]` | Alpha resets state; Mu adds state to observations; Eta copies state to target. | 55 |

Thus the left vector `[1,1,1,1]` describes only the first word of each pair. The second words continued changing after that vector stabilized. The final complete paired pattern is common from round 64 onward, whereas the first-word vector stabilized earlier.

At the right:

| Channel | Repeated value | Machine effect per value | Tail copies |
|---|---:|---|---:|
| 1 | 2 | Beta increments context. | 96 |
| 2 | 1 | Alpha resets state to one. | 92 |
| 3 | 5 | Epsilon adds the zero-constraints test to observations. Final constraints is 1, so this adds zero. | 92 |
| 4 | 1 | Alpha resets state to one. | 100 |

The explicit exit syscall terminates execution after these operations. Numeric zero emits no halt instruction. Repetition is represented as actual repeated assignments, additions or conditional arithmetic.

## Native experiments on the repeated regions

For each channel, two additional programs collapsed its front pair run to one pair or its back run to one value. All eight programs assembled and executed. All four target outputs stayed unchanged in all eight comparisons, while other outputs changed in three comparisons:

- Channel 1 tail collapse changed context; replacing 96 Beta increments with one removes 95 increments.
- Channel 3 front collapse changed unresolved; replacing 93 Stigma increments with one removes 92 increments.
- Channel 4 front collapse changed relations, observations, unresolved and context.

The other five collapses preserved the entire eight-word output for these seeds. Consequently, target stability and full-state equivalence are different properties. Removing a boundary region should account for the state it contributes, even when its target stays unchanged.

## Information retention and seed placement

Every current program's first instruction is `state = 1`. The compiled initial state seed is overwritten before it is read. Under the current four-value mapping, this discards the first opposite-end seed at the start of each executable. Placing a value in a different named cell changes which operations can use it.

All 32 one-bit seed perturbation tests ran successfully. Most changed some output cells, while only the tested channel-3 events change altered a final target. Exact per-test changes are saved in `native_sensitivity.csv`; these results apply to those perturbations, not all possible values.

Numeric grouping also affects what reaches the machine: group separators and zero groups emit no instructions. The values 1, 1000 and 1000000 all dispatch Alpha alone after group metadata is removed. Raw integer magnitudes and group positions remain in source comments and chain records, but they are not encoded as distinct operands in those Alpha instructions. Assignment/reset and low-byte masking also lose information, so reversing operator order is not the arithmetic inverse of the computation.

## Saved evidence

`assembly_analysis_pass100/assembly_analysis.json` contains the channel statistics, exact target-writing sites, seeds and outputs, boundary counts and all 44 native comparisons. `integer_state_trace.csv` records all eight cells after every chain value. `operator_semantics.csv` lists each operator's arithmetic. `native_analysis_sources.zip` preserves the native comparison sources. All original assembly and executables remain intact.
