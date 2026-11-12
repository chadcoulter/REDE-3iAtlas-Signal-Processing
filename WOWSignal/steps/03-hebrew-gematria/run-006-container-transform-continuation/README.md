# Container-transform continuation: passes6–10

All24 run005 branches continue under the same output-register feedback rule. No branches are selected or removed for linguistic coherence. Register order: state, relations, constraints, observations, unresolved, context, target, events.

Process: deterministically replay passes1–10 using the unchanged original runner; require exact equality of every pass1–5 record with run005; require each pass6 starting state and numeric inputs to match its saved pass5 output; retain passes6–10 as the continuation. Each operation is checked against the preserved original instruction interpreter. At each pass, encode all eight carried registers; apply the branch's unchanged orientation; execute; record every intermediate vector; emit all eight numeric values and their Greek/Hebrew numeric encodings.

The source numeric units, operator definitions, seeds, three orientations, two input modes, and feedback rule are unchanged. The original candidate subset came from earlier lexical exploration; this continuation performs no word search or sentence construction. Zero values remain in numeric/register data and encode as zero/no operation under the existing rule. All register arithmetic follows the recovered machine's uint64 behavior.

Data: 120 new pass records, 1165 new instruction records, 24 exact prefix comparisons. Full before/after states and per-instruction writes are in results.json; all pass outputs are also in register_passes.csv.

Container הגה; seed 32; intact_parts; forward
Pass5: [1, 3, 1, 4, 3, 7, 1, 17]
Pass6: ΑΓΑΔΓΖΑΙΖ
Output: [1, 0, 2, 4, 3, 7, 1, 18]
Changes: {"relations": [3, 0], "constraints": [1, 2], "events": [17, 18]}
Greek units: Α ‖ 0 ‖ Β ‖ Δ ‖ Γ ‖ Ζ ‖ Α ‖ ΙΗ
Hebrew units: א ‖ 0 ‖ ב ‖ ד ‖ ג ‖ ז ‖ א ‖ יח
Pass7: ΑΒΔΓΖΑΙΗ
Output: [1, 2, 2, 4, 3, 8, 1, 19]
Changes: {"relations": [0, 2], "context": [7, 8], "events": [18, 19]}
Greek units: Α ‖ Β ‖ Β ‖ Δ ‖ Γ ‖ Η ‖ Α ‖ ΙΘ
Hebrew units: א ‖ ב ‖ ב ‖ ד ‖ ג ‖ ח ‖ א ‖ יט
Pass8: ΑΒΒΔΓΗΑΙΘ
Output: [1, 2, 3, 4, 3, 10, 2, 20]
Changes: {"constraints": [2, 3], "context": [8, 10], "target": [1, 2], "events": [19, 20]}
Greek units: Α ‖ Β ‖ Γ ‖ Δ ‖ Γ ‖ Ι ‖ Β ‖ Κ
Hebrew units: א ‖ ב ‖ ג ‖ ד ‖ ג ‖ י ‖ ב ‖ כ
Pass9: ΑΒΓΔΓΙΒΚ
Output: [2, 2, 2, 4, 3, 13, 2, 21]
Changes: {"state": [1, 2], "constraints": [3, 2], "context": [10, 13], "events": [20, 21]}
Greek units: Β ‖ Β ‖ Β ‖ Δ ‖ Γ ‖ ΙΓ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ ב ‖ ב ‖ ד ‖ ג ‖ יג ‖ ב ‖ כא
Pass10: ΒΒΒΔΓΙΓΒΚΑ
Output: [1, 2, 3, 4, 3, 18, 2, 22]
Changes: {"state": [2, 1], "constraints": [2, 3], "context": [13, 18], "events": [21, 22]}
Greek units: Α ‖ Β ‖ Γ ‖ Δ ‖ Γ ‖ ΙΗ ‖ Β ‖ ΚΒ
Hebrew units: א ‖ ב ‖ ג ‖ ד ‖ ג ‖ יח ‖ ב ‖ כב
Repeated complete output states: []

Container הגה; seed 32; intact_parts; container_reverse
Pass5: [2, 2, 3, 4, 2, 12, 1, 17]
Pass6: ΙΖΑΙΒΒΔΓΒΒ
Output: [2, 0, 2, 4, 2, 16, 1, 19]
Changes: {"relations": [2, 0], "constraints": [3, 2], "context": [12, 16], "events": [17, 19]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΙϚ ‖ Α ‖ ΙΘ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ טז ‖ א ‖ יט
Pass7: ΙΘΑΙϚΒΔΒΒ
Output: [2, 0, 3, 4, 3, 19, 1, 21]
Changes: {"constraints": [2, 3], "unresolved": [2, 3], "context": [16, 19], "events": [19, 21]}
Greek units: Β ‖ 0 ‖ Γ ‖ Δ ‖ Γ ‖ ΙΘ ‖ Α ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ג ‖ ד ‖ ג ‖ יט ‖ א ‖ כא
Pass8: ΚΑΑΙΘΓΔΓΒ
Output: [2, 0, 2, 4, 3, 21, 1, 22]
Changes: {"constraints": [3, 2], "context": [19, 21], "events": [21, 22]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Γ ‖ ΚΑ ‖ Α ‖ ΚΒ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ג ‖ כא ‖ א ‖ כב
Pass9: ΚΒΑΚΑΓΔΒΒ
Output: [2, 0, 1, 4, 3, 26, 1, 22]
Changes: {"constraints": [2, 1], "context": [21, 26]}
Greek units: Β ‖ 0 ‖ Α ‖ Δ ‖ Γ ‖ ΚϚ ‖ Α ‖ ΚΒ
Hebrew units: ב ‖ 0 ‖ א ‖ ד ‖ ג ‖ כו ‖ א ‖ כב
Pass10: ΚΒΑΚϚΓΔΑΒ
Output: [1, 0, 1, 4, 4, 30, 1, 22]
Changes: {"state": [2, 1], "unresolved": [3, 4], "context": [26, 30]}
Greek units: Α ‖ 0 ‖ Α ‖ Δ ‖ Δ ‖ Λ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ 0 ‖ א ‖ ד ‖ ד ‖ ל ‖ א ‖ כב
Repeated complete output states: []

Container הגה; seed 32; intact_parts; full_glyph_reverse
Pass5: [2, 2, 3, 4, 2, 12, 1, 17]
Pass6: ΖΙΑΒΙΒΔΓΒΒ
Output: [2, 0, 2, 4, 2, 16, 1, 19]
Changes: {"relations": [2, 0], "constraints": [3, 2], "context": [12, 16], "events": [17, 19]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΙϚ ‖ Α ‖ ΙΘ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ טז ‖ א ‖ יט
Pass7: ΘΙΑϚΙΒΔΒΒ
Output: [2, 0, 3, 4, 3, 19, 1, 21]
Changes: {"constraints": [2, 3], "unresolved": [2, 3], "context": [16, 19], "events": [19, 21]}
Greek units: Β ‖ 0 ‖ Γ ‖ Δ ‖ Γ ‖ ΙΘ ‖ Α ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ג ‖ ד ‖ ג ‖ יט ‖ א ‖ כא
Pass8: ΑΚΑΘΙΓΔΓΒ
Output: [2, 0, 2, 4, 3, 21, 1, 22]
Changes: {"constraints": [3, 2], "context": [19, 21], "events": [21, 22]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Γ ‖ ΚΑ ‖ Α ‖ ΚΒ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ג ‖ כא ‖ א ‖ כב
Pass9: ΒΚΑΑΚΓΔΒΒ
Output: [2, 0, 1, 4, 3, 26, 1, 22]
Changes: {"constraints": [2, 1], "context": [21, 26]}
Greek units: Β ‖ 0 ‖ Α ‖ Δ ‖ Γ ‖ ΚϚ ‖ Α ‖ ΚΒ
Hebrew units: ב ‖ 0 ‖ א ‖ ד ‖ ג ‖ כו ‖ א ‖ כב
Pass10: ΒΚΑϚΚΓΔΑΒ
Output: [1, 0, 1, 4, 4, 30, 1, 22]
Changes: {"state": [2, 1], "unresolved": [3, 4], "context": [26, 30]}
Greek units: Α ‖ 0 ‖ Α ‖ Δ ‖ Δ ‖ Λ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ 0 ‖ א ‖ ד ‖ ד ‖ ל ‖ א ‖ כב
Repeated complete output states: []

Container הגה; seed 32; whole_container_total; forward
Pass5: [1, 0, 2, 4, 3, 7, 1, 18]
Pass6: ΑΒΔΓΖΑΙΗ
Output: [1, 2, 2, 4, 3, 8, 1, 19]
Changes: {"relations": [0, 2], "context": [7, 8], "events": [18, 19]}
Greek units: Α ‖ Β ‖ Β ‖ Δ ‖ Γ ‖ Η ‖ Α ‖ ΙΘ
Hebrew units: א ‖ ב ‖ ב ‖ ד ‖ ג ‖ ח ‖ א ‖ יט
Pass7: ΑΒΒΔΓΗΑΙΘ
Output: [1, 2, 3, 4, 3, 10, 2, 20]
Changes: {"constraints": [2, 3], "context": [8, 10], "target": [1, 2], "events": [19, 20]}
Greek units: Α ‖ Β ‖ Γ ‖ Δ ‖ Γ ‖ Ι ‖ Β ‖ Κ
Hebrew units: א ‖ ב ‖ ג ‖ ד ‖ ג ‖ י ‖ ב ‖ כ
Pass8: ΑΒΓΔΓΙΒΚ
Output: [2, 2, 2, 4, 3, 13, 2, 21]
Changes: {"state": [1, 2], "constraints": [3, 2], "context": [10, 13], "events": [20, 21]}
Greek units: Β ‖ Β ‖ Β ‖ Δ ‖ Γ ‖ ΙΓ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ ב ‖ ב ‖ ד ‖ ג ‖ יג ‖ ב ‖ כא
Pass9: ΒΒΒΔΓΙΓΒΚΑ
Output: [1, 2, 3, 4, 3, 18, 2, 22]
Changes: {"state": [2, 1], "constraints": [2, 3], "context": [13, 18], "events": [21, 22]}
Greek units: Α ‖ Β ‖ Γ ‖ Δ ‖ Γ ‖ ΙΗ ‖ Β ‖ ΚΒ
Hebrew units: א ‖ ב ‖ ג ‖ ד ‖ ג ‖ יח ‖ ב ‖ כב
Pass10: ΑΒΓΔΓΙΗΒΚΒ
Output: [2, 2, 2, 4, 3, 22, 2, 23]
Changes: {"state": [1, 2], "constraints": [3, 2], "context": [18, 22], "events": [22, 23]}
Greek units: Β ‖ Β ‖ Β ‖ Δ ‖ Γ ‖ ΚΒ ‖ Β ‖ ΚΓ
Hebrew units: ב ‖ ב ‖ ב ‖ ד ‖ ג ‖ כב ‖ ב ‖ כג
Repeated complete output states: []

Container הגה; seed 32; whole_container_total; container_reverse
Pass5: [2, 0, 3, 4, 2, 13, 1, 18]
Pass6: ΙΗΑΙΓΒΔΓΒ
Output: [2, 0, 2, 4, 2, 15, 2, 20]
Changes: {"constraints": [3, 2], "context": [13, 15], "target": [1, 2], "events": [18, 20]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΙΕ ‖ Β ‖ Κ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ טו ‖ ב ‖ כ
Pass7: ΚΒΙΕΒΔΒΒ
Output: [3, 0, 2, 4, 2, 20, 2, 21]
Changes: {"state": [2, 3], "context": [15, 20], "events": [20, 21]}
Greek units: Γ ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ Κ ‖ Β ‖ ΚΑ
Hebrew units: ג ‖ 0 ‖ ב ‖ ד ‖ ב ‖ כ ‖ ב ‖ כא
Pass8: ΚΑΒΚΒΔΒΓ
Output: [2, 0, 2, 4, 2, 25, 2, 21]
Changes: {"state": [3, 2], "context": [20, 25]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΚΕ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ כה ‖ ב ‖ כא
Pass9: ΚΑΒΚΕΒΔΒΒ
Output: [2, 0, 2, 4, 2, 31, 2, 21]
Changes: {"context": [25, 31]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΛΑ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ לא ‖ ב ‖ כא
Pass10: ΚΑΒΛΑΒΔΒΒ
Output: [2, 0, 2, 4, 2, 36, 2, 21]
Changes: {"context": [31, 36]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΛϚ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ לו ‖ ב ‖ כא
Repeated complete output states: []

Container הגה; seed 32; whole_container_total; full_glyph_reverse
Pass5: [2, 0, 3, 4, 2, 13, 1, 18]
Pass6: ΗΙΑΓΙΒΔΓΒ
Output: [2, 0, 2, 4, 2, 15, 2, 20]
Changes: {"constraints": [3, 2], "context": [13, 15], "target": [1, 2], "events": [18, 20]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΙΕ ‖ Β ‖ Κ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ טו ‖ ב ‖ כ
Pass7: ΚΒΕΙΒΔΒΒ
Output: [3, 0, 2, 4, 2, 20, 2, 21]
Changes: {"state": [2, 3], "context": [15, 20], "events": [20, 21]}
Greek units: Γ ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ Κ ‖ Β ‖ ΚΑ
Hebrew units: ג ‖ 0 ‖ ב ‖ ד ‖ ב ‖ כ ‖ ב ‖ כא
Pass8: ΑΚΒΚΒΔΒΓ
Output: [2, 0, 2, 4, 2, 25, 2, 21]
Changes: {"state": [3, 2], "context": [20, 25]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΚΕ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ כה ‖ ב ‖ כא
Pass9: ΑΚΒΕΚΒΔΒΒ
Output: [2, 0, 2, 4, 2, 31, 2, 21]
Changes: {"context": [25, 31]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΛΑ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ לא ‖ ב ‖ כא
Pass10: ΑΚΒΑΛΒΔΒΒ
Output: [2, 0, 2, 4, 2, 36, 2, 21]
Changes: {"context": [31, 36]}
Greek units: Β ‖ 0 ‖ Β ‖ Δ ‖ Β ‖ ΛϚ ‖ Β ‖ ΚΑ
Hebrew units: ב ‖ 0 ‖ ב ‖ ד ‖ ב ‖ לו ‖ ב ‖ כא
Repeated complete output states: []

Container הגה; seed 40; intact_parts; forward
Pass5: [1, 3, 1, 5, 1, 10, 1, 20]
Pass6: ΑΓΑΕΑΙΑΚ
Output: [1, 3, 1, 5, 1, 11, 1, 21]
Changes: {"context": [10, 11], "events": [20, 21]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΑ ‖ Α ‖ ΚΑ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ יא ‖ א ‖ כא
Pass7: ΑΓΑΕΑΙΑΑΚΑ
Output: [1, 3, 1, 5, 1, 12, 1, 22]
Changes: {"context": [11, 12], "events": [21, 22]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΒ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ יב ‖ א ‖ כב
Pass8: ΑΓΑΕΑΙΒΑΚΒ
Output: [1, 3, 1, 5, 1, 15, 1, 23]
Changes: {"context": [12, 15], "events": [22, 23]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΕ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טו ‖ א ‖ כג
Pass9: ΑΓΑΕΑΙΕΑΚΓ
Output: [1, 3, 1, 5, 1, 16, 1, 24]
Changes: {"context": [15, 16], "events": [23, 24]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙϚ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טז ‖ א ‖ כד
Pass10: ΑΓΑΕΑΙϚΑΚΔ
Output: [2, 3, 1, 5, 2, 17, 1, 25]
Changes: {"state": [1, 2], "unresolved": [1, 2], "context": [16, 17], "events": [24, 25]}
Greek units: Β ‖ Γ ‖ Α ‖ Ε ‖ Β ‖ ΙΖ ‖ Α ‖ ΚΕ
Hebrew units: ב ‖ ג ‖ א ‖ ה ‖ ב ‖ יז ‖ א ‖ כה
Repeated complete output states: []

Container הגה; seed 40; intact_parts; container_reverse
Pass5: [1, 7, 2, 5, 1, 9, 1, 20]
Pass6: ΚΑΘΑΕΒΖΑ
Output: [1, 6, 3, 5, 1, 11, 1, 20]
Changes: {"relations": [7, 6], "constraints": [2, 3], "context": [9, 11]}
Greek units: Α ‖ Ϛ ‖ Γ ‖ Ε ‖ Α ‖ ΙΑ ‖ Α ‖ Κ
Hebrew units: א ‖ ו ‖ ג ‖ ה ‖ א ‖ יא ‖ א ‖ כ
Pass7: ΚΑΙΑΑΕΓϚΑ
Output: [1, 6, 1, 5, 2, 12, 1, 21]
Changes: {"constraints": [3, 1], "unresolved": [1, 2], "context": [11, 12], "events": [20, 21]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Β ‖ ΙΒ ‖ Α ‖ ΚΑ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ב ‖ יב ‖ א ‖ כא
Pass8: ΚΑΑΙΒΒΕΑϚΑ
Output: [1, 6, 1, 5, 3, 15, 1, 22]
Changes: {"unresolved": [2, 3], "context": [12, 15], "events": [21, 22]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Γ ‖ ΙΕ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ג ‖ טו ‖ א ‖ כב
Pass9: ΚΒΑΙΕΓΕΑϚΑ
Output: [1, 6, 1, 5, 4, 17, 1, 23]
Changes: {"unresolved": [3, 4], "context": [15, 17], "events": [22, 23]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Δ ‖ ΙΖ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ד ‖ יז ‖ א ‖ כג
Pass10: ΚΓΑΙΖΔΕΑϚΑ
Output: [1, 7, 1, 5, 5, 18, 1, 24]
Changes: {"relations": [6, 7], "unresolved": [4, 5], "context": [17, 18], "events": [23, 24]}
Greek units: Α ‖ Ζ ‖ Α ‖ Ε ‖ Ε ‖ ΙΗ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ז ‖ א ‖ ה ‖ ה ‖ יח ‖ א ‖ כד
Repeated complete output states: []

Container הגה; seed 40; intact_parts; full_glyph_reverse
Pass5: [1, 7, 2, 5, 1, 9, 1, 20]
Pass6: ΚΑΘΑΕΒΖΑ
Output: [1, 6, 3, 5, 1, 11, 1, 20]
Changes: {"relations": [7, 6], "constraints": [2, 3], "context": [9, 11]}
Greek units: Α ‖ Ϛ ‖ Γ ‖ Ε ‖ Α ‖ ΙΑ ‖ Α ‖ Κ
Hebrew units: א ‖ ו ‖ ג ‖ ה ‖ א ‖ יא ‖ א ‖ כ
Pass7: ΚΑΑΙΑΕΓϚΑ
Output: [1, 6, 1, 5, 2, 12, 1, 21]
Changes: {"constraints": [3, 1], "unresolved": [1, 2], "context": [11, 12], "events": [20, 21]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Β ‖ ΙΒ ‖ Α ‖ ΚΑ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ב ‖ יב ‖ א ‖ כא
Pass8: ΑΚΑΒΙΒΕΑϚΑ
Output: [1, 6, 1, 5, 3, 15, 1, 22]
Changes: {"unresolved": [2, 3], "context": [12, 15], "events": [21, 22]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Γ ‖ ΙΕ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ג ‖ טו ‖ א ‖ כב
Pass9: ΒΚΑΕΙΓΕΑϚΑ
Output: [1, 6, 1, 5, 4, 17, 1, 23]
Changes: {"unresolved": [3, 4], "context": [15, 17], "events": [22, 23]}
Greek units: Α ‖ Ϛ ‖ Α ‖ Ε ‖ Δ ‖ ΙΖ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ו ‖ א ‖ ה ‖ ד ‖ יז ‖ א ‖ כג
Pass10: ΓΚΑΖΙΔΕΑϚΑ
Output: [1, 7, 1, 5, 5, 18, 1, 24]
Changes: {"relations": [6, 7], "unresolved": [4, 5], "context": [17, 18], "events": [23, 24]}
Greek units: Α ‖ Ζ ‖ Α ‖ Ε ‖ Ε ‖ ΙΗ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ז ‖ א ‖ ה ‖ ה ‖ יח ‖ א ‖ כד
Repeated complete output states: []

Container הגה; seed 40; whole_container_total; forward
Pass5: [1, 3, 2, 5, 2, 11, 1, 20]
Pass6: ΑΓΒΕΒΙΑΑΚ
Output: [1, 3, 1, 5, 2, 14, 1, 21]
Changes: {"constraints": [2, 1], "context": [11, 14], "events": [20, 21]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Β ‖ ΙΔ ‖ Α ‖ ΚΑ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ב ‖ יד ‖ א ‖ כא
Pass7: ΑΓΑΕΒΙΔΑΚΑ
Output: [1, 3, 1, 5, 2, 16, 1, 22]
Changes: {"context": [14, 16], "events": [21, 22]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Β ‖ ΙϚ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ב ‖ טז ‖ א ‖ כב
Pass8: ΑΓΑΕΒΙϚΑΚΒ
Output: [1, 3, 1, 5, 3, 19, 1, 23]
Changes: {"unresolved": [2, 3], "context": [16, 19], "events": [22, 23]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Γ ‖ ΙΘ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ג ‖ יט ‖ א ‖ כג
Pass9: ΑΓΑΕΓΙΘΑΚΓ
Output: [1, 3, 1, 5, 3, 20, 1, 24]
Changes: {"context": [19, 20], "events": [23, 24]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Γ ‖ Κ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ג ‖ כ ‖ א ‖ כד
Pass10: ΑΓΑΕΓΚΑΚΔ
Output: [2, 3, 1, 5, 3, 22, 1, 24]
Changes: {"state": [1, 2], "context": [20, 22]}
Greek units: Β ‖ Γ ‖ Α ‖ Ε ‖ Γ ‖ ΚΒ ‖ Α ‖ ΚΔ
Hebrew units: ב ‖ ג ‖ א ‖ ה ‖ ג ‖ כב ‖ א ‖ כד
Repeated complete output states: []

Container הגה; seed 40; whole_container_total; container_reverse
Pass5: [1, 3, 1, 5, 1, 11, 1, 21]
Pass6: ΚΑΑΙΑΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 12, 1, 22]
Changes: {"context": [11, 12], "events": [21, 22]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΒ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ יב ‖ א ‖ כב
Pass7: ΚΒΑΙΒΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 15, 1, 23]
Changes: {"context": [12, 15], "events": [22, 23]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΕ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טו ‖ א ‖ כג
Pass8: ΚΓΑΙΕΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 16, 1, 24]
Changes: {"context": [15, 16], "events": [23, 24]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙϚ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טז ‖ א ‖ כד
Pass9: ΚΔΑΙϚΑΕΑΓΑ
Output: [1, 3, 1, 5, 2, 17, 1, 25]
Changes: {"unresolved": [1, 2], "context": [16, 17], "events": [24, 25]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Β ‖ ΙΖ ‖ Α ‖ ΚΕ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ב ‖ יז ‖ א ‖ כה
Pass10: ΚΕΑΙΖΒΕΑΓΑ
Output: [1, 2, 1, 5, 2, 19, 1, 26]
Changes: {"relations": [3, 2], "context": [17, 19], "events": [25, 26]}
Greek units: Α ‖ Β ‖ Α ‖ Ε ‖ Β ‖ ΙΘ ‖ Α ‖ ΚϚ
Hebrew units: א ‖ ב ‖ א ‖ ה ‖ ב ‖ יט ‖ א ‖ כו
Repeated complete output states: []

Container הגה; seed 40; whole_container_total; full_glyph_reverse
Pass5: [1, 3, 1, 5, 1, 11, 1, 21]
Pass6: ΑΚΑΑΙΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 12, 1, 22]
Changes: {"context": [11, 12], "events": [21, 22]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΒ ‖ Α ‖ ΚΒ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ יב ‖ א ‖ כב
Pass7: ΒΚΑΒΙΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 15, 1, 23]
Changes: {"context": [12, 15], "events": [22, 23]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙΕ ‖ Α ‖ ΚΓ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טו ‖ א ‖ כג
Pass8: ΓΚΑΕΙΑΕΑΓΑ
Output: [1, 3, 1, 5, 1, 16, 1, 24]
Changes: {"context": [15, 16], "events": [23, 24]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Α ‖ ΙϚ ‖ Α ‖ ΚΔ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ א ‖ טז ‖ א ‖ כד
Pass9: ΔΚΑϚΙΑΕΑΓΑ
Output: [1, 3, 1, 5, 2, 17, 1, 25]
Changes: {"unresolved": [1, 2], "context": [16, 17], "events": [24, 25]}
Greek units: Α ‖ Γ ‖ Α ‖ Ε ‖ Β ‖ ΙΖ ‖ Α ‖ ΚΕ
Hebrew units: א ‖ ג ‖ א ‖ ה ‖ ב ‖ יז ‖ א ‖ כה
Pass10: ΕΚΑΖΙΒΕΑΓΑ
Output: [1, 2, 1, 5, 2, 19, 1, 26]
Changes: {"relations": [3, 2], "context": [17, 19], "events": [25, 26]}
Greek units: Α ‖ Β ‖ Α ‖ Ε ‖ Β ‖ ΙΘ ‖ Α ‖ ΚϚ
Hebrew units: א ‖ ב ‖ א ‖ ה ‖ ב ‖ יט ‖ א ‖ כו
Repeated complete output states: []

Container וידא; seed 5; intact_parts; forward
Pass5: [1, 1, 1, 30, 7, 5, 1, 6]
Pass6: ΑΑΑΛΖΕΑϚ
Output: [1, 1, 1, 30, 8, 5, 1, 6]
Changes: {"unresolved": [7, 8]}
Greek units: Α ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Ε ‖ Α ‖ Ϛ
Hebrew units: א ‖ א ‖ א ‖ ל ‖ ח ‖ ה ‖ א ‖ ו
Pass7: ΑΑΑΛΗΕΑϚ
Output: [1, 1, 1, 30, 9, 5, 0, 6]
Changes: {"unresolved": [8, 9], "target": [1, 0]}
Greek units: Α ‖ Α ‖ Α ‖ Λ ‖ Θ ‖ Ε ‖ 0 ‖ Ϛ
Hebrew units: א ‖ א ‖ א ‖ ל ‖ ט ‖ ה ‖ 0 ‖ ו
Pass8: ΑΑΑΛΘΕϚ
Output: [0, 1, 2, 30, 10, 5, 0, 6]
Changes: {"state": [1, 0], "constraints": [1, 2], "unresolved": [9, 10]}
Greek units: 0 ‖ Α ‖ Β ‖ Λ ‖ Ι ‖ Ε ‖ 0 ‖ Ϛ
Hebrew units: 0 ‖ א ‖ ב ‖ ל ‖ י ‖ ה ‖ 0 ‖ ו
Pass9: ΑΒΛΙΕϚ
Output: [0, 1, 2, 30, 11, 6, 0, 7]
Changes: {"unresolved": [10, 11], "context": [5, 6], "events": [6, 7]}
Greek units: 0 ‖ Α ‖ Β ‖ Λ ‖ ΙΑ ‖ Ϛ ‖ 0 ‖ Ζ
Hebrew units: 0 ‖ א ‖ ב ‖ ל ‖ יא ‖ ו ‖ 0 ‖ ז
Pass10: ΑΒΛΙΑϚΖ
Output: [1, 0, 2, 30, 12, 7, 0, 8]
Changes: {"state": [0, 1], "relations": [1, 0], "unresolved": [11, 12], "context": [6, 7], "events": [7, 8]}
Greek units: Α ‖ 0 ‖ Β ‖ Λ ‖ ΙΒ ‖ Ζ ‖ 0 ‖ Η
Hebrew units: א ‖ 0 ‖ ב ‖ ל ‖ יב ‖ ז ‖ 0 ‖ ח
Repeated complete output states: []

Container וידא; seed 5; intact_parts; container_reverse
Pass5: [15, 15, 16, 30, 9, 5, 16, 11]
Pass6: ΙΑΙϚΕΘΛΙϚΙΕΙΕ
Output: [14, 15, 17, 30, 11, 5, 16, 16]
Changes: {"state": [15, 14], "constraints": [16, 17], "unresolved": [9, 11], "events": [11, 16]}
Greek units: ΙΔ ‖ ΙΕ ‖ ΙΖ ‖ Λ ‖ ΙΑ ‖ Ε ‖ ΙϚ ‖ ΙϚ
Hebrew units: יד ‖ טו ‖ יז ‖ ל ‖ יא ‖ ה ‖ טז ‖ טז
Pass7: ΙϚΙϚΕΙΑΛΙΖΙΕΙΔ
Output: [15, 1, 17, 30, 13, 5, 16, 22]
Changes: {"state": [14, 15], "relations": [15, 1], "unresolved": [11, 13], "events": [16, 22]}
Greek units: ΙΕ ‖ Α ‖ ΙΖ ‖ Λ ‖ ΙΓ ‖ Ε ‖ ΙϚ ‖ ΚΒ
Hebrew units: טו ‖ א ‖ יז ‖ ל ‖ יג ‖ ה ‖ טז ‖ כב
Pass8: ΚΒΙϚΕΙΓΛΙΖΑΙΕ
Output: [1, 15, 15, 30, 14, 7, 16, 26]
Changes: {"state": [15, 1], "relations": [1, 15], "constraints": [17, 15], "unresolved": [13, 14], "context": [5, 7], "events": [22, 26]}
Greek units: Α ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ ΙΔ ‖ Ζ ‖ ΙϚ ‖ ΚϚ
Hebrew units: א ‖ טו ‖ טו ‖ ל ‖ יד ‖ ז ‖ טז ‖ כו
Pass9: ΚϚΙϚΖΙΔΛΙΕΙΕΑ
Output: [1, 14, 15, 30, 16, 8, 16, 30]
Changes: {"relations": [15, 14], "unresolved": [14, 16], "context": [7, 8], "events": [26, 30]}
Greek units: Α ‖ ΙΔ ‖ ΙΕ ‖ Λ ‖ ΙϚ ‖ Η ‖ ΙϚ ‖ Λ
Hebrew units: א ‖ יד ‖ טו ‖ ל ‖ טז ‖ ח ‖ טז ‖ ל
Pass10: ΛΙϚΗΙϚΛΙΕΙΔΑ
Output: [1, 14, 15, 30, 18, 8, 15, 34]
Changes: {"unresolved": [16, 18], "target": [16, 15], "events": [30, 34]}
Greek units: Α ‖ ΙΔ ‖ ΙΕ ‖ Λ ‖ ΙΗ ‖ Η ‖ ΙΕ ‖ ΛΔ
Hebrew units: א ‖ יד ‖ טו ‖ ל ‖ יח ‖ ח ‖ טו ‖ לד
Repeated complete output states: []

Container וידא; seed 5; intact_parts; full_glyph_reverse
Pass5: [15, 15, 16, 30, 9, 5, 16, 11]
Pass6: ΑΙϚΙΕΘΛϚΙΕΙΕΙ
Output: [14, 15, 17, 30, 11, 5, 16, 16]
Changes: {"state": [15, 14], "constraints": [16, 17], "unresolved": [9, 11], "events": [11, 16]}
Greek units: ΙΔ ‖ ΙΕ ‖ ΙΖ ‖ Λ ‖ ΙΑ ‖ Ε ‖ ΙϚ ‖ ΙϚ
Hebrew units: יד ‖ טו ‖ יז ‖ ל ‖ יא ‖ ה ‖ טז ‖ טז
Pass7: ϚΙϚΙΕΑΙΛΖΙΕΙΔΙ
Output: [15, 1, 17, 30, 13, 5, 16, 22]
Changes: {"state": [14, 15], "relations": [15, 1], "unresolved": [11, 13], "events": [16, 22]}
Greek units: ΙΕ ‖ Α ‖ ΙΖ ‖ Λ ‖ ΙΓ ‖ Ε ‖ ΙϚ ‖ ΚΒ
Hebrew units: טו ‖ א ‖ יז ‖ ל ‖ יג ‖ ה ‖ טז ‖ כב
Pass8: ΒΚϚΙΕΓΙΛΖΙΑΕΙ
Output: [1, 15, 15, 30, 14, 7, 16, 26]
Changes: {"state": [15, 1], "relations": [1, 15], "constraints": [17, 15], "unresolved": [13, 14], "context": [5, 7], "events": [22, 26]}
Greek units: Α ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ ΙΔ ‖ Ζ ‖ ΙϚ ‖ ΚϚ
Hebrew units: א ‖ טו ‖ טו ‖ ל ‖ יד ‖ ז ‖ טז ‖ כו
Pass9: ϚΚϚΙΖΔΙΛΕΙΕΙΑ
Output: [1, 14, 15, 30, 16, 8, 16, 30]
Changes: {"relations": [15, 14], "unresolved": [14, 16], "context": [7, 8], "events": [26, 30]}
Greek units: Α ‖ ΙΔ ‖ ΙΕ ‖ Λ ‖ ΙϚ ‖ Η ‖ ΙϚ ‖ Λ
Hebrew units: א ‖ יד ‖ טו ‖ ל ‖ טז ‖ ח ‖ טז ‖ ל
Pass10: ΛϚΙΗϚΙΛΕΙΔΙΑ
Output: [1, 14, 15, 30, 18, 8, 15, 34]
Changes: {"unresolved": [16, 18], "target": [16, 15], "events": [30, 34]}
Greek units: Α ‖ ΙΔ ‖ ΙΕ ‖ Λ ‖ ΙΗ ‖ Η ‖ ΙΕ ‖ ΛΔ
Hebrew units: א ‖ יד ‖ טו ‖ ל ‖ יח ‖ ח ‖ טו ‖ לד
Repeated complete output states: []

Container וידא; seed 5; whole_container_total; forward
Pass5: [1, 3, 12, 30, 6, 9, 1, 8]
Pass6: ΑΓΙΒΛϚΘΑΗ
Output: [1, 3, 2, 30, 7, 10, 1, 9]
Changes: {"constraints": [12, 2], "unresolved": [6, 7], "context": [9, 10], "events": [8, 9]}
Greek units: Α ‖ Γ ‖ Β ‖ Λ ‖ Ζ ‖ Ι ‖ Α ‖ Θ
Hebrew units: א ‖ ג ‖ ב ‖ ל ‖ ז ‖ י ‖ א ‖ ט
Pass7: ΑΓΒΛΖΙΑΘ
Output: [1, 1, 2, 30, 7, 11, 1, 10]
Changes: {"relations": [3, 1], "context": [10, 11], "events": [9, 10]}
Greek units: Α ‖ Α ‖ Β ‖ Λ ‖ Ζ ‖ ΙΑ ‖ Α ‖ Ι
Hebrew units: א ‖ א ‖ ב ‖ ל ‖ ז ‖ יא ‖ א ‖ י
Pass8: ΑΑΒΛΖΙΑΑΙ
Output: [1, 1, 2, 30, 7, 12, 1, 12]
Changes: {"context": [11, 12], "events": [10, 12]}
Greek units: Α ‖ Α ‖ Β ‖ Λ ‖ Ζ ‖ ΙΒ ‖ Α ‖ ΙΒ
Hebrew units: א ‖ א ‖ ב ‖ ל ‖ ז ‖ יב ‖ א ‖ יב
Pass9: ΑΑΒΛΖΙΒΑΙΒ
Output: [1, 1, 2, 30, 7, 15, 1, 14]
Changes: {"context": [12, 15], "events": [12, 14]}
Greek units: Α ‖ Α ‖ Β ‖ Λ ‖ Ζ ‖ ΙΕ ‖ Α ‖ ΙΔ
Hebrew units: א ‖ א ‖ ב ‖ ל ‖ ז ‖ טו ‖ א ‖ יד
Pass10: ΑΑΒΛΖΙΕΑΙΔ
Output: [2, 1, 2, 30, 7, 16, 1, 16]
Changes: {"state": [1, 2], "context": [15, 16], "events": [14, 16]}
Greek units: Β ‖ Α ‖ Β ‖ Λ ‖ Ζ ‖ ΙϚ ‖ Α ‖ ΙϚ
Hebrew units: ב ‖ א ‖ ב ‖ ל ‖ ז ‖ טז ‖ א ‖ טז
Repeated complete output states: []

Container וידא; seed 5; whole_container_total; container_reverse
Pass5: [1, 14, 1, 30, 4, 5, 1, 5]
Pass6: ΕΑΕΔΛΑΙΔΑ
Output: [1, 14, 1, 30, 4, 5, 1, 6]
Changes: {"events": [5, 6]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ Λ ‖ Δ ‖ Ε ‖ Α ‖ Ϛ
Hebrew units: א ‖ יד ‖ א ‖ ל ‖ ד ‖ ה ‖ א ‖ ו
Pass7: ϚΑΕΔΛΑΙΔΑ
Output: [1, 14, 1, 30, 5, 5, 1, 7]
Changes: {"unresolved": [4, 5], "events": [6, 7]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Ζ
Hebrew units: א ‖ יד ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ז
Pass8: ΖΑΕΕΛΑΙΔΑ
Output: [1, 15, 1, 30, 5, 5, 1, 8]
Changes: {"relations": [14, 15], "events": [7, 8]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Η
Hebrew units: א ‖ טו ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ח
Pass9: ΗΑΕΕΛΑΙΕΑ
Output: [1, 15, 1, 30, 5, 5, 1, 9]
Changes: {"events": [8, 9]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Θ
Hebrew units: א ‖ טו ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ט
Pass10: ΘΑΕΕΛΑΙΕΑ
Output: [1, 15, 2, 30, 5, 5, 1, 10]
Changes: {"constraints": [1, 2], "events": [9, 10]}
Greek units: Α ‖ ΙΕ ‖ Β ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Ι
Hebrew units: א ‖ טו ‖ ב ‖ ל ‖ ה ‖ ה ‖ א ‖ י
Repeated complete output states: []

Container וידא; seed 5; whole_container_total; full_glyph_reverse
Pass5: [1, 14, 1, 30, 4, 5, 1, 5]
Pass6: ΕΑΕΔΛΑΔΙΑ
Output: [1, 14, 1, 30, 4, 5, 1, 6]
Changes: {"events": [5, 6]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ Λ ‖ Δ ‖ Ε ‖ Α ‖ Ϛ
Hebrew units: א ‖ יד ‖ א ‖ ל ‖ ד ‖ ה ‖ א ‖ ו
Pass7: ϚΑΕΔΛΑΔΙΑ
Output: [1, 14, 1, 30, 5, 5, 1, 7]
Changes: {"unresolved": [4, 5], "events": [6, 7]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Ζ
Hebrew units: א ‖ יד ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ז
Pass8: ΖΑΕΕΛΑΔΙΑ
Output: [1, 15, 1, 30, 5, 5, 1, 8]
Changes: {"relations": [14, 15], "events": [7, 8]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Η
Hebrew units: א ‖ טו ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ח
Pass9: ΗΑΕΕΛΑΕΙΑ
Output: [1, 15, 1, 30, 5, 5, 1, 9]
Changes: {"events": [8, 9]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Θ
Hebrew units: א ‖ טו ‖ א ‖ ל ‖ ה ‖ ה ‖ א ‖ ט
Pass10: ΘΑΕΕΛΑΕΙΑ
Output: [1, 15, 2, 30, 5, 5, 1, 10]
Changes: {"constraints": [1, 2], "events": [9, 10]}
Greek units: Α ‖ ΙΕ ‖ Β ‖ Λ ‖ Ε ‖ Ε ‖ Α ‖ Ι
Hebrew units: א ‖ טו ‖ ב ‖ ל ‖ ה ‖ ה ‖ א ‖ י
Repeated complete output states: []

Container כוידא; seed 7; intact_parts; forward
Pass5: [1, 14, 1, 30, 7, 8, 1, 6]
Pass6: ΑΙΔΑΛΖΗΑϚ
Output: [1, 1, 1, 30, 8, 8, 15, 7]
Changes: {"relations": [14, 1], "unresolved": [7, 8], "target": [1, 15], "events": [6, 7]}
Greek units: Α ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Η ‖ ΙΕ ‖ Ζ
Hebrew units: א ‖ א ‖ א ‖ ל ‖ ח ‖ ח ‖ טו ‖ ז
Pass7: ΑΑΑΛΗΗΙΕΖ
Output: [0, 1, 1, 30, 8, 8, 0, 8]
Changes: {"state": [1, 0], "target": [15, 0], "events": [7, 8]}
Greek units: 0 ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Η ‖ 0 ‖ Η
Hebrew units: 0 ‖ א ‖ א ‖ ל ‖ ח ‖ ח ‖ 0 ‖ ח
Pass8: ΑΑΛΗΗΗ
Output: [0, 1, 1, 30, 8, 8, 0, 8]
Changes: {}
Greek units: 0 ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Η ‖ 0 ‖ Η
Hebrew units: 0 ‖ א ‖ א ‖ ל ‖ ח ‖ ח ‖ 0 ‖ ח
Pass9: ΑΑΛΗΗΗ
Output: [0, 1, 1, 30, 8, 8, 0, 8]
Changes: {}
Greek units: 0 ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Η ‖ 0 ‖ Η
Hebrew units: 0 ‖ א ‖ א ‖ ל ‖ ח ‖ ח ‖ 0 ‖ ח
Pass10: ΑΑΛΗΗΗ
Output: [0, 1, 1, 30, 8, 8, 0, 8]
Changes: {}
Greek units: 0 ‖ Α ‖ Α ‖ Λ ‖ Η ‖ Η ‖ 0 ‖ Η
Hebrew units: 0 ‖ א ‖ א ‖ ל ‖ ח ‖ ח ‖ 0 ‖ ח
Repeated complete output states: [{"earlier_pass": 7, "later_pass": 8}, {"earlier_pass": 7, "later_pass": 9}, {"earlier_pass": 8, "later_pass": 9}, {"earlier_pass": 7, "later_pass": 10}, {"earlier_pass": 8, "later_pass": 10}, {"earlier_pass": 9, "later_pass": 10}]

Container כוידא; seed 7; intact_parts; container_reverse
Pass5: [15, 15, 14, 30, 8, 8, 1, 11]
Pass6: ΙΑΑΗΗΛΙΔΙΕΙΕ
Output: [15, 15, 14, 30, 8, 8, 1, 15]
Changes: {"events": [11, 15]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΔ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΙΕ
Hebrew units: טו ‖ טו ‖ יד ‖ ל ‖ ח ‖ ח ‖ א ‖ טו
Pass7: ΙΕΑΗΗΛΙΔΙΕΙΕ
Output: [15, 15, 14, 30, 8, 8, 1, 19]
Changes: {"events": [15, 19]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΔ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΙΘ
Hebrew units: טו ‖ טו ‖ יד ‖ ל ‖ ח ‖ ח ‖ א ‖ יט
Pass8: ΙΘΑΗΗΛΙΔΙΕΙΕ
Output: [15, 15, 15, 30, 8, 8, 1, 23]
Changes: {"constraints": [14, 15], "events": [19, 23]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΚΓ
Hebrew units: טו ‖ טו ‖ טו ‖ ל ‖ ח ‖ ח ‖ א ‖ כג
Pass9: ΚΓΑΗΗΛΙΕΙΕΙΕ
Output: [14, 15, 15, 30, 8, 9, 1, 26]
Changes: {"state": [15, 14], "context": [8, 9], "events": [23, 26]}
Greek units: ΙΔ ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ Η ‖ Θ ‖ Α ‖ ΚϚ
Hebrew units: יד ‖ טו ‖ טו ‖ ל ‖ ח ‖ ט ‖ א ‖ כו
Pass10: ΚϚΑΘΗΛΙΕΙΕΙΔ
Output: [15, 15, 16, 30, 9, 10, 1, 29]
Changes: {"state": [14, 15], "constraints": [15, 16], "unresolved": [8, 9], "context": [9, 10], "events": [26, 29]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙϚ ‖ Λ ‖ Θ ‖ Ι ‖ Α ‖ ΚΘ
Hebrew units: טו ‖ טו ‖ טז ‖ ל ‖ ט ‖ י ‖ א ‖ כט
Repeated complete output states: []

Container כוידא; seed 7; intact_parts; full_glyph_reverse
Pass5: [15, 15, 14, 30, 8, 8, 1, 11]
Pass6: ΑΙΑΗΗΛΔΙΕΙΕΙ
Output: [15, 15, 14, 30, 8, 8, 1, 15]
Changes: {"events": [11, 15]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΔ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΙΕ
Hebrew units: טו ‖ טו ‖ יד ‖ ל ‖ ח ‖ ח ‖ א ‖ טו
Pass7: ΕΙΑΗΗΛΔΙΕΙΕΙ
Output: [15, 15, 14, 30, 8, 8, 1, 19]
Changes: {"events": [15, 19]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΔ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΙΘ
Hebrew units: טו ‖ טו ‖ יד ‖ ל ‖ ח ‖ ח ‖ א ‖ יט
Pass8: ΘΙΑΗΗΛΔΙΕΙΕΙ
Output: [15, 15, 15, 30, 8, 8, 1, 23]
Changes: {"constraints": [14, 15], "events": [19, 23]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ Η ‖ Η ‖ Α ‖ ΚΓ
Hebrew units: טו ‖ טו ‖ טו ‖ ל ‖ ח ‖ ח ‖ א ‖ כג
Pass9: ΓΚΑΗΗΛΕΙΕΙΕΙ
Output: [14, 15, 15, 30, 8, 9, 1, 26]
Changes: {"state": [15, 14], "context": [8, 9], "events": [23, 26]}
Greek units: ΙΔ ‖ ΙΕ ‖ ΙΕ ‖ Λ ‖ Η ‖ Θ ‖ Α ‖ ΚϚ
Hebrew units: יד ‖ טו ‖ טו ‖ ל ‖ ח ‖ ט ‖ א ‖ כו
Pass10: ϚΚΑΘΗΛΕΙΕΙΔΙ
Output: [15, 15, 16, 30, 9, 10, 1, 29]
Changes: {"state": [14, 15], "constraints": [15, 16], "unresolved": [8, 9], "context": [9, 10], "events": [26, 29]}
Greek units: ΙΕ ‖ ΙΕ ‖ ΙϚ ‖ Λ ‖ Θ ‖ Ι ‖ Α ‖ ΚΘ
Hebrew units: טו ‖ טו ‖ טז ‖ ל ‖ ט ‖ י ‖ א ‖ כט
Repeated complete output states: []

Container כוידא; seed 7; whole_container_total; forward
Pass5: [2, 14, 1, 31, 4, 5, 1, 5]
Pass6: ΒΙΔΑΛΑΔΕΑΕ
Output: [1, 14, 1, 31, 4, 6, 1, 6]
Changes: {"state": [2, 1], "context": [5, 6], "events": [5, 6]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Δ ‖ Ϛ ‖ Α ‖ Ϛ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ד ‖ ו ‖ א ‖ ו
Pass7: ΑΙΔΑΛΑΔϚΑϚ
Output: [1, 14, 1, 31, 6, 6, 1, 7]
Changes: {"unresolved": [4, 6], "events": [6, 7]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Ϛ ‖ Ϛ ‖ Α ‖ Ζ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ו ‖ ו ‖ א ‖ ז
Pass8: ΑΙΔΑΛΑϚϚΑΖ
Output: [1, 15, 1, 31, 8, 6, 1, 8]
Changes: {"relations": [14, 15], "unresolved": [6, 8], "events": [7, 8]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Η ‖ Ϛ ‖ Α ‖ Η
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ח ‖ ו ‖ א ‖ ח
Pass9: ΑΙΕΑΛΑΗϚΑΗ
Output: [1, 15, 1, 31, 9, 6, 1, 9]
Changes: {"unresolved": [8, 9], "events": [8, 9]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Θ ‖ Ϛ ‖ Α ‖ Θ
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ט ‖ ו ‖ א ‖ ט
Pass10: ΑΙΕΑΛΑΘϚΑΘ
Output: [1, 15, 3, 31, 10, 6, 1, 10]
Changes: {"constraints": [1, 3], "unresolved": [9, 10], "events": [9, 10]}
Greek units: Α ‖ ΙΕ ‖ Γ ‖ ΛΑ ‖ Ι ‖ Ϛ ‖ Α ‖ Ι
Hebrew units: א ‖ טו ‖ ג ‖ לא ‖ י ‖ ו ‖ א ‖ י
Repeated complete output states: []

Container כוידא; seed 7; whole_container_total; container_reverse
Pass5: [1, 14, 1, 31, 4, 5, 1, 5]
Pass6: ΕΑΕΔΛΑΑΙΔΑ
Output: [1, 14, 1, 31, 4, 5, 1, 6]
Changes: {"events": [5, 6]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Δ ‖ Ε ‖ Α ‖ Ϛ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ד ‖ ה ‖ א ‖ ו
Pass7: ϚΑΕΔΛΑΑΙΔΑ
Output: [1, 14, 1, 31, 5, 5, 1, 7]
Changes: {"unresolved": [4, 5], "events": [6, 7]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Ζ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ז
Pass8: ΖΑΕΕΛΑΑΙΔΑ
Output: [1, 15, 1, 31, 5, 5, 1, 8]
Changes: {"relations": [14, 15], "events": [7, 8]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Η
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ח
Pass9: ΗΑΕΕΛΑΑΙΕΑ
Output: [1, 15, 1, 31, 5, 5, 1, 9]
Changes: {"events": [8, 9]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Θ
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ט
Pass10: ΘΑΕΕΛΑΑΙΕΑ
Output: [1, 15, 2, 31, 5, 5, 1, 10]
Changes: {"constraints": [1, 2], "events": [9, 10]}
Greek units: Α ‖ ΙΕ ‖ Β ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Ι
Hebrew units: א ‖ טו ‖ ב ‖ לא ‖ ה ‖ ה ‖ א ‖ י
Repeated complete output states: []

Container כוידא; seed 7; whole_container_total; full_glyph_reverse
Pass5: [1, 14, 1, 31, 4, 5, 1, 5]
Pass6: ΕΑΕΔΑΛΑΔΙΑ
Output: [1, 14, 1, 31, 4, 5, 1, 6]
Changes: {"events": [5, 6]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Δ ‖ Ε ‖ Α ‖ Ϛ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ד ‖ ה ‖ א ‖ ו
Pass7: ϚΑΕΔΑΛΑΔΙΑ
Output: [1, 14, 1, 31, 5, 5, 1, 7]
Changes: {"unresolved": [4, 5], "events": [6, 7]}
Greek units: Α ‖ ΙΔ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Ζ
Hebrew units: א ‖ יד ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ז
Pass8: ΖΑΕΕΑΛΑΔΙΑ
Output: [1, 15, 1, 31, 5, 5, 1, 8]
Changes: {"relations": [14, 15], "events": [7, 8]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Η
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ח
Pass9: ΗΑΕΕΑΛΑΕΙΑ
Output: [1, 15, 1, 31, 5, 5, 1, 9]
Changes: {"events": [8, 9]}
Greek units: Α ‖ ΙΕ ‖ Α ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Θ
Hebrew units: א ‖ טו ‖ א ‖ לא ‖ ה ‖ ה ‖ א ‖ ט
Pass10: ΘΑΕΕΑΛΑΕΙΑ
Output: [1, 15, 2, 31, 5, 5, 1, 10]
Changes: {"constraints": [1, 2], "events": [9, 10]}
Greek units: Α ‖ ΙΕ ‖ Β ‖ ΛΑ ‖ Ε ‖ Ε ‖ Α ‖ Ι
Hebrew units: א ‖ טו ‖ ב ‖ לא ‖ ה ‖ ה ‖ א ‖ י
Repeated complete output states: []

Five additional passes do not establish convergence. These are computed register outputs; no new observation samples or source letters were inserted. Status: IN-PROGRESS.

## Reproduction and file changes

Run `python -X utf8 -B WOWSignal/scripts/step03_container_transform_continuation.py` from the repository root before this run exists. The command refuses to overwrite this directory or duplicate its working-text section.

Added this runner and run006 results.json, register_passes.csv, README.md, manifest.json. Appended all24 branches to the combined working Hebrew text. Added a byte-preserving .gitattributes rule for the runner. Earlier run005 files are unchanged. No commit or push.


## Pass6–10 computed observations

For intact כוידא, forward traversal, pass6 output is [1,1,1,30,8,8,15,7]; pass7 output is [0,1,1,30,8,8,0,8]. Passes8,9,10 repeat the latter eight-value output exactly. Their program is ΑΑΛΗΗΗ. Α sets state to1; the second Α leaves it1; Λ XORs state1 with relations1 to produce0; all three Η instructions copy0 into target. No event or context increment instruction occurs. Internal state changes0->1->0 remain visible even though the complete output repeats. This repeat belongs to this branch and feedback rule; other branches remain separate.

For intact וידא, forward traversal, pass6 unresolved increases7->8. Its numeric8 becomes Η in pass7. At that point ΑΑΑΛ sets state0 before Η writes target0. Pass7 output is [1,1,1,30,9,5,0,6]. The earlier כוידא/וידא prefix difference has propagated into the timing and contents of target writes.

For intact וידא under numeric-container reversal, pass6–10 events are16,22,26,30,34; target remains16 through pass9 and changes16->15 in pass10. For intact כוידא under numeric-container reversal, events are15,19,23,26,29; target remains1 through all five passes. These are machine register values, with no inferred physical units.

No full eight-register output repetition across passes1–10 was found in the other23 branches. Numeric-container reversal and full-glyph reversal yield identical complete pass6–10 output vectors for all8 candidate/seed/mode combinations tested, although their instruction orders are retained separately. This is a measured equality for these passes, not a general equivalence of the two reversal operations.

Verification: independently recomputed all10 passes and compared all120 new pass records exactly; each of the1165 new instruction operations also passed the preserved original interpreter comparison. The pass1–5 prefixes matched their saved run005 records in all24 branches.
