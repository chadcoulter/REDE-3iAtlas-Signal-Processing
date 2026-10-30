# Feed the rotated target result back into the phase array

Initial phase array, in zero-based destination order, is `[1,14682301134823862838,2,1]`, taken from the preceding `replace_1_state` cyclic-routing test. All eight initial feedback registers for each physical channel come from that same test's native projection outputs.

For each round:

1. Put the phase array into the existing four reflection input slots: `state`, `relations`, `constraints`, `observations`. Retain the other four registers from the preceding projection of that physical channel.
2. Freshly assemble and run the unchanged captured signal/core chain forward on each channel.
3. Copy each reflection's complete ending register state to channel `(n+1)%4`. Replace only `state` with its source `target`; preserve the other seven cells and apply no endpoint reseeding at this turn.
4. Freshly assemble and run that destination chain in projection order, reversing values and glyphs.
5. Take projection targets in destination order 0,1,2,3 as the next phase array. Retain the full native ending banks for the next round.

Thus the phase array is input data, not a new channel-index permutation. The original/core chain values are not moved, appended or edited in this feedback experiment. Code is reassembled every pass because its seed data changes. The complete `.text` instruction body is checked for identity per physical channel and direction across all rounds.

`run_rotated_phase_feedback.py` defaults to 100 rounds, eight freshly assembled/executed programs per round. Native outputs supply all feedback; the interpreter only verifies the result. The output directory must be fresh. Per-round checkpoints, full register and source links, assembly/ELF archives and raw binary outputs encoded as hex are preserved. Repeated vectors, literal zeros and selected historical patterns are recorded without assigning a new failure or EOF meaning.
