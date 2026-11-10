# Wow! reconstruction progress — return paths and 5 × 5 / 7 × 7 expansion

Date: November 9, 2026

Branch: `codex/wow-signal`

Repository baseline: `ba3b1396a74764d6bb012b28def5419ffb8d2ed4`

## Purpose and status

This report continues the [expanded-matrix and ABRA progress report](README-2026-11-09-expanded-matrix-message-progress.md). It captures the subsequent traversal of `ΒΓΑΗΑΔΑ`, the next source and return relationship, the continuation of `ΑΡΑ` into another pass, and the requested expansion to 5 × 5 and 7 × 7.

The work uses Chad's process to develop candidate readings while keeping numerical groups, source identities, traversal choices, and operator interpretations visible. **The exploration remains in progress.** The candidate English instructions are composed readings of the selected operator sequences, not independently decoded quotations. No historical mapping has been silently replaced or declared recovered.

The preceding calculations were read-only. This report is the only file added for this documentation request. Existing sources, reports, code, and generated artifacts remain unchanged. No commit or push is included in this request.

## Sources and conventions

- [Step 1 measurement report](../01-source-data/run-001.md), [numeric grid](../01-source-data/run-001/numeric_grid.json), and [row metadata](../01-source-data/run-001/row_metadata.csv).
- [Historical narrative](../../sources/WowDecodeNarrative.md) and [V8 note](../../sources/v8-resolve-through-monads.md).
- [Earlier shared-center report](README-2026-11-09-shared-center-progress.md).
- [Character-transform skill](../../../skills/character-transform-reasoning/SKILL.md), [Book II](../../../skills/character-transform-reasoning/references/book-ii-alphabet.txt), and [Greek numeral encoder](../../../skills/character-transform-reasoning/scripts/redsigma_band_extract.py).

All reported source rows and channels are **one-based**. Code explicitly uses zero-based array indices. The native grid contains 82 time rows and 50 frequency channels. Blank printout cells remain preserved in the raw source and are represented as bin zero in the numeric grid; that is not a measurement of zero physical radio power.

The grouping rule continues to be maximal contiguous nonzero runs **along the selected path**. Sum each run, then encode its sum using the repository's Greek numeral function. Every intervening zero-bin sample remains in the source trace. Numerical glyphs are then read provisionally through the operator vocabulary. This numeral-to-operator bridge and the path selection are explicit interpretive choices.

Historical Ϝ remains reverse traversal for this reconstruction. Later Book II roles used here include Α Origin, Β Branch, Γ Boundary frame, Δ Change, Η State, Κ Context, and Ρ Relation. Shared glyph values do not make different source occurrences identical.

## 1. Starting reading: ΒΓΑΗΑΔΑ

The horizontal nonzero-run reading at row 51, going toward increasing channel numbers, was:

| Channels | Bins | Sum | Numeral |
|---|---|---:|---|
| 02–03 | 1,1 | 2 | Β |
| 07–08 | 1,2 | 3 | Γ |
| 11 | 1 | 1 | Α |
| 15–21 | 1,1,1,1,1,1,2 | 8 | Η |
| 38 | 1 | 1 | Α |
| 44–46 | 2,1,1 | 4 | Δ |
| 49 | 1 | 1 | Α |

The next source was the final Alpha's cell, **row 51, channel 49**, at printed time 22:14:11 EST.

## 2. Including the next source's vertical context

The new source is part of a vertical run at channel 49:

```text
Rows 51–53: [1,1,1]
Run sum:    3 → Γ
```

Thus a cell read as Α on the shorter horizontal path participates in Γ when the connected vertical run is included. The source occurrence is retained; the scope of its grouping changes. Joining the paths requires counting the turning cell once rather than concatenating an Alpha and a Gamma that both include it.

The earlier-time branch was inspected as well: rows 28 and 13 each contain an isolated one in channel 49. The continuation actually followed here uses later rows to include the complete run at the new source. That direction is a recorded branch choice, not a uniquely inferred command.

From row 51 onward, channel 49 contains nine complete nonzero runs:

| Rows | Bins | Sum | Numeral |
|---|---|---:|---|
| 51–53 | 1,1,1 | 3 | Γ |
| 55–56 | 1,1 | 2 | Β |
| 59 | 1 | 1 | Α |
| 62–63 | 1,1 | 2 | Β |
| 65 | 1 | 1 | Α |
| 68 | 1 | 1 | Α |
| 71–72 | 1,1 | 2 | Β |
| 75 | 1 | 1 | Α |
| 77 | 1 | 1 | Α |

The selected row-major display of these groups was:

```text
Γ Β Α
Β Α Α
Β Α Α
```

Its middle group is Α at **row 65, channel 49**. Selecting that group supplied the horizontal return branch. The later groups remain available; they were not discarded as meaningless or treated as an established terminal boundary.

At the earlier event midpoint, rows 60 and 61 in channel 49 are both bin zero. This new column does not reproduce the event's +4 central edge in channel 02.

## 3. Returning through row 65 and the original core

Row 65, traversed toward decreasing channel numbers, has the run sequence:

```text
Α | Δ | Γ | Α | Α | Α | Β | Α | Α | Α | Γ | Α
```

Its groups, in forward channel order, are:

| Channels | Sum | Numeral |
|---|---:|---|
| 02 | 1 | Α |
| 04 | 3 | Γ |
| 07 | 1 | Α |
| 11 | 1 | Α |
| 16 | 1 | Α |
| 24–25 | 2 | Β |
| 27 | 1 | Α |
| 36 | 1 | Α |
| 39 | 1 | Α |
| 41–42 | 3 | Γ |
| 44–46 | 4 | Δ |
| 49 | 1 | Α |

Both row 51 and row 65 have total 20, encoded Κ. Their constituent groups differ, so matching totals do not establish identical contexts.

The horizontal return reaches **row 65, channel 02**. That cell is one constituent of the `[1,1]` group at rows 65–66 that supplied Β in the earlier ABRA reading. Following channel 02 toward earlier times then encounters:

```text
Α: row 65
Ρ: rows 63 → 58, bins 5,19,30,26,14,6
Α: row 51
```

The return sequence is `Α | Ρ | Α`. Inside Ρ it traverses the retained source edge as **30 → 26**. The route returns to the exact starting coordinate:

```text
(row 51, channel 02)
  → (51,49)
  → (65,49)
  → (65,02)
  → (51,02)
```

This demonstrates a return in the selected source-grid trace, not a physical journey or preservation claim about an astronomical transmitter. The closing coordinate is an alias of the starting source occurrence, not a new independent sample.

Grouped continuously, counting shared turning cells once, that complete route reads:

```text
Outbound and first turn: Β Γ Α Η Α Δ Γ
Vertical continuation:  Β Α Β Α
Horizontal return:      Δ Γ Α Α Α Β Α Α Α Γ Α
Return through core:    Ρ Α
```

The candidate instruction composed at this stage was:

> Carry the change into its frame. Follow the branch to its source, then return through the retained relationship to the originating source.

## 4. Carrying ΑΡΑ into the next pass

At the return to row 51, channel 02, the immediate neighbors are:

```text
Earlier time: 0
Later time:   0
Left channel: 0
Source:       1
Right channel:1
```

The next horizontal reading therefore groups the returned source with its right neighbor:

```text
(51,02), (51,03): [1,1] → Β
```

The terminal Alpha of the return participates in the initial Beta of the next pass. It is not counted separately when joining the paths. Combining the incoming return with the horizontal pass, before extending its far-end turn, gives nine groups:

```text
Α | Ρ | Β | Γ | Α | Η | Α | Δ | Α
```

The row-major display used in the chat was:

```text
Α Ρ Β
Γ Α Η
Α Δ Α
```

Its middle group is **Α at row 51, channel 11**. Its main diagonal `ΑΑΑ` refers to different source positions: row 65/channel 02, row 51/channel 11, and row 51/channel 49. Its middle column `ΡΑΔ` was read provisionally as Relation–Origin–Change.

The candidate composed instruction was:

> Carry the source relationship into the branch. Establish the frame in which its state can form, and carry change into the next originating state.

Inspecting the new middle source vertically gives another `[1,1]` run at rows 51–52, channel 11, encoded Β. Horizontally, the same source cell remains an isolated one between zero-bin neighbors. This again shows a source occurrence participating in a larger group under a different path context.

Continuing straight in channel 02 was retained as an alternative. From row 51 toward later times it reads `ΑΡΒΑΓ`; toward earlier times it reads `ΑΑΓΒΑΑ`, under the same run rule. No rule has uniquely selected the horizontal continuation over these alternatives.

## 5. Expansion method: preserve the distinction between two displays

Chad requested expansion to 5 × 5 and 7 × 7. The preceding three-by-three was a **row-major summary of nine sequential groups**. It did not establish a unique outer border or two native source axes.

For the requested larger matrices, the exploration explicitly returned to the **overlapping-window construction used in the earlier size expansions**. For odd size n, select 2n−1 consecutive source-linked groups centered on the chosen group, and form n windows of n groups. Entry `(i,j)` references sequence group `i+j`. These display axes index overlapping group positions along the selected path; neither is automatically a native time or frequency axis.

The middle source remains Α at **row 51, channel 11**. The original row-major display is retained as a previous representation rather than silently equated with this construction.

Extending the complete far-end turn also changes its shorter terminal Α at row 51/channel 49 into Γ, because the run includes rows 52 and 53 in that channel. The expanded sequence records this contextual update rather than appending a duplicate Γ after Α.

## 6. Source-linked groups used for the expansion

The extended continuous path starts on row 65 at channel 07, follows that row toward channel 02, returns through channel 02 to row 51, crosses row 51 to channel 49, and follows channel 49 through row 60. The final zero-bin reading completes the run at row 59.

| Group ID | Source cells, row/channel | Sum | Numeral |
|---:|---|---:|---|
| 0 | (65,07) | 1 | Α |
| 1 | (65,04) | 3 | Γ |
| 2 | (65,02) | 1 | Α |
| 3 | (63,02) through (58,02), in reverse time order | 100 | Ρ |
| 4 | (51,02), (51,03) | 2 | Β |
| 5 | (51,07), (51,08) | 3 | Γ |
| 6 | (51,11) | 1 | Α |
| 7 | (51,15) through (51,21) | 8 | Η |
| 8 | (51,38) | 1 | Α |
| 9 | (51,44), (51,45), (51,46) | 4 | Δ |
| 10 | (51,49), (52,49), (53,49) | 3 | Γ |
| 11 | (55,49), (56,49) | 2 | Β |
| 12 | (59,49) | 1 | Α |

All zero-bin positions between these groups remain in the trace. Groups 0 and 1 extend before the nine-group interval; groups 11 and 12 extend after it. Group 10 includes the completed turn.

```text
Thirteen-group sequence:
Α Γ | Α Ρ Β Γ Α Η Α Δ Γ | Β Α
                  ^
Center is group ID 6: Α at (51,11).
```

The caret is explanatory only; the group ID and source coordinates define the center.

## 7. The nested matrices

The overlapping-window three-by-three uses group IDs 4–8:

```text
Β Γ Α
Γ Α Η
Α Η Α
```

This differs from the previous row-major summary. It is the actual inner matrix retained by the expansions below.

The **5 × 5** uses group IDs 2–10, nine distinct groups:

```text
Α Ρ Β Γ Α
Ρ Β Γ Α Η
Β Γ Α Η Α
Γ Α Η Α Δ
Α Η Α Δ Γ
```

The **7 × 7** uses group IDs 0–12, thirteen distinct groups:

```text
Α Γ Α Ρ Β Γ Α
Γ Α Ρ Β Γ Α Η
Α Ρ Β Γ Α Η Α
Ρ Β Γ Α Η Α Δ
Β Γ Α Η Α Δ Γ
Γ Α Η Α Δ Γ Β
Α Η Α Δ Γ Β Α
```

Removing one border from the 7 × 7 reproduces the 5 × 5 exactly, including group identities. Removing another reproduces the overlapping-window 3 × 3. There are 25 and 49 display positions, but only nine and thirteen distinct groups, respectively.

At every size the other diagonal repeats **group ID 6**, not merely numerically equal Alpha occurrences. Its repeated display appearances are aliases of one source-linked group. This shared-center property follows from the window construction. The main diagonals are `ΒΑΑ`, `ΑΒΑΑΓ`, and `ΑΑΒΑΑΓΑ` at sizes 3, 5, and 7.

The central horizontal readings expand as:

```text
3 × 3: Γ Α Η
5 × 5: Β Γ Α Η Α
7 × 7: Ρ Β Γ Α Η Α Δ
```

Relation and Change enter the wider central traversal around Branch–Frame–Origin–State. The candidate composed reading was:

> Relate the branch to its frame and originating state; carry that originating relationship through change.

This remains a reading produced by the process and selected context. The repeated center and nesting establish representation identities; they do not independently establish an intentional message or select a physical location.

## 8. Current state and next relationships

The work now has a reproducible source-linked expansion, a specific middle occurrence, a completed return route, and recorded context-dependent grouping changes. It also has two distinct three-by-three representations whose difference is preserved.

Continue by following source-linked contributions, retaining the completed-turn Γ, the source identity of group 6, alternate chronological branches, and the larger context. Any next pass should identify which representation and path it consumes. A repeated cycle can preserve information without producing new measured content; changed groupings must retain their prior shorter readings and contribution links.

No new physical age, reflection target, terrestrial origin, or historical decode mapping was established in these passes. Those branches remain in the preceding report. Chad's source–branch–return interpretation remains available there as the proposed relational reading guiding this exploration.

## Reproduction

Run from the repository root with Python. This standard-library-only block reads the preserved numeric grid and extracts the existing numeral encoder without importing its signal-processing dependencies. It writes no files. Its assertions verify source, path, grouping, and matrix identities, not semantic interpretation.

```python
import ast
import json
from pathlib import Path

base = Path('WOWSignal/steps/01-source-data/run-001')
grid = json.loads((base / 'numeric_grid.json').read_text(encoding='utf-8'))['grid']
encoder = Path('skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
tree = ast.parse(encoder.read_text(encoding='utf-8'))
nodes = [n for n in tree.body if (
    isinstance(n, ast.Assign)
    and any(isinstance(v, ast.Name) and v.id == 'VALUES' for v in n.targets)
) or (isinstance(n, ast.FunctionDef) and n.name == 'greek')]
namespace = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(encoder), 'exec'), namespace)
greek = namespace['greek']

def groups(coords):
    assert all(abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1
               for a, b in zip(coords, coords[1:]))
    result = []
    i = 0
    while i < len(coords):
        r, c = coords[i]
        if grid[r][c] == 0:
            i += 1
            continue
        j = i
        while j < len(coords) and grid[coords[j][0]][coords[j][1]] != 0:
            j += 1
        cells = coords[i:j]
        total = sum(grid[r][c] for r, c in cells)
        result.append({'cells': cells, 'sum': total, 'glyph': greek(total)})
        i = j
    return result

# Full retained source-grid return, including the closing occurrence as an alias.
loop = [(50,c) for c in range(1,49)]
loop += [(r,48) for r in range(51,65)]
loop += [(64,c) for c in range(47,0,-1)]
loop += [(r,1) for r in range(63,49,-1)]
assert loop[0] == loop[-1] == (50,1)
assert len(set(loop[:-1])) == len(loop)-1
loop_groups = groups(loop)
assert [g['glyph'] for g in loop_groups] == list('ΒΓΑΗΑΔΓΒΑΒΑΔΓΑΑΑΒΑΑΑΓΑΡΑ')
assert any(a == (60,1) and b == (59,1) for a, b in zip(loop, loop[1:]))

# Incoming return joined to the shorter next horizontal pass.
joined = [(r,1) for r in range(64,49,-1)]
joined += [(50,c) for c in range(2,50)]
joined_groups = groups(joined)
assert [g['glyph'] for g in joined_groups] == list('ΑΡΒΓΑΗΑΔΑ')
assert joined_groups[4]['cells'] == [(50,10)]
assert grid[50][10] == grid[51][10] == 1
assert grid[49][10] == grid[52][10] == 0

# Longer trace supporting the nested 3, 5, and 7 overlapping-window views.
trace = [(64,c) for c in range(6,0,-1)]
trace += [(r,1) for r in range(63,49,-1)]
trace += [(50,c) for c in range(2,49)]
trace += [(r,48) for r in range(51,60)]
records = groups(trace)
assert len(records) == 13
assert [g['glyph'] for g in records] == list('ΑΓΑΡΒΓΑΗΑΔΓΒΑ')
assert records[6]['cells'] == [(50,10)]
assert records[10]['cells'] == [(50,48), (51,48), (52,48)]

expected = {
    3: ['ΒΓΑ', 'ΓΑΗ', 'ΑΗΑ'],
    5: ['ΑΡΒΓΑ', 'ΡΒΓΑΗ', 'ΒΓΑΗΑ', 'ΓΑΗΑΔ', 'ΑΗΑΔΓ'],
    7: ['ΑΓΑΡΒΓΑ', 'ΓΑΡΒΓΑΗ', 'ΑΡΒΓΑΗΑ', 'ΡΒΓΑΗΑΔ',
        'ΒΓΑΗΑΔΓ', 'ΓΑΗΑΔΓΒ', 'ΑΗΑΔΓΒΑ'],
}
previous = None
for n in (3,5,7):
    start = 6-(n-1)
    ids = [[start+i+j for j in range(n)] for i in range(n)]
    display = [''.join(records[k]['glyph'] for k in row) for row in ids]
    assert display == expected[n]
    assert ids[n//2][n//2] == 6
    assert all(ids[i][n-1-i] == 6 for i in range(n))
    assert len({k for row in ids for k in row}) == 2*n-1
    if previous is not None:
        assert [row[1:-1] for row in ids[1:-1]] == previous
    previous = ids
    print(f'{n} x {n}')
    for row in display:
        print(' '.join(row))

print('Return, joined path, group identities, and nested expansions reproduced.')
print('Candidate instructions remain interpretive readings of these representations.')
```
