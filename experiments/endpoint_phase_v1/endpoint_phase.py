"""Endpoint-seeded phase probe. Only creates new output directories/files.

Candidate wiring: every channel bank receives the same four opposite-end raw
integers in a fixed four-register assignment. Its own current raw integer then
selects the archived operator sequence. X->Y reads target; Y->X reads state and
relations. All other-channel views are retained, without averaging/reduction.
"""
import argparse
import ast
import csv
import hashlib
import itertools
import json
import re
import zipfile
from pathlib import Path

from operator_machine import MASK, REGS, execute, parse_source, validate

DEFAULT_MAPPING = ('state', 'relations', 'constraints', 'observations')


def numeral_table(path):
    for node in ast.parse(path.read_text(encoding='utf-8-sig')).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'VALUES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('Repo numeral table not found')


def encode(value, table):
    if not 0 <= value <= MASK:
        raise ValueError('Input is outside unsigned 64-bit range')
    if value == 0:
        return '0'
    chunks = []
    while value:
        chunk, value = value % 1000, value // 1000
        word = ''
        for amount, glyph in table:
            while chunk >= amount:
                word += glyph
                chunk -= amount
        chunks.append(word or '0')
    return ' | '.join(reversed(chunks))


def load_archive(path, table):
    bands = []
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith('.S'):
                continue
            raw = archive.read(name)
            text = raw.decode('utf-8')
            ops, glyph_frames = parse_source(text)
            matches = re.findall(r'(?m)^\s*# (?:elapsed_second|second)=(\d+) (?:frequency_MHz|freqMHz)=([^ ]+) amplitude=([^ ]+) rounded=(\d+) (?:greek|gematria)=([^\r\n]+)', text)
            if len(matches) != len(glyph_frames):
                raise ValueError('Row metadata alignment failed: ' + name)
            frames = []
            for metadata, glyphs in zip(matches, glyph_frames):
                second, frequency, amplitude, rounded, original = metadata
                integer = int(rounded)
                encoded = encode(integer, table)
                commands = ''.join(g for g in encoded if g not in ' |0')
                if commands != ''.join(glyphs):
                    raise ValueError('Numeric input does not reproduce source operators')
                frames.append({'second': int(second), 'frequency_MHz': frequency,
                               'amplitude': amplitude, 'rounded': integer,
                               'original_numerals': original.strip()})
            bands.append({'source': name, 'ops': ops, 'frames': frames,
                          'sha256': hashlib.sha256(raw).hexdigest()})
    if len(bands) != 4:
        raise ValueError('Expected four channels')
    if any([f['second'] for f in b['frames']] != [f['second'] for f in bands[0]['frames']] for b in bands):
        raise ValueError('Channels are not time-aligned')
    return bands


def seed_bank(opposite, mapping):
    if len(set(mapping)) != 4 or any(reg not in REGS for reg in mapping):
        raise ValueError('Four distinct existing registers are required')
    state = {reg: 1 for reg in REGS}
    for register, raw_value in zip(mapping, opposite):
        if not 0 <= raw_value <= MASK:
            raise ValueError('Invalid raw register seed')
        state[register] = raw_value
    return state


def phase(current, opposite, direction, bands, table, mapping=DEFAULT_MAPPING):
    """No state from a prior row enters; seed endpoints before current encoding."""
    if direction not in ('x_to_y', 'y_to_x'):
        raise ValueError(direction)
    states, traces = [], []
    for channel, (value, band) in enumerate(zip(current, bands), 1):
        before = seed_bank(opposite, mapping)
        state = before.copy()
        encoded = encode(value, table)
        glyphs = ''.join(g for g in encoded if g not in ' |0')
        if direction == 'y_to_x':
            glyphs = glyphs[::-1]
        for glyph in glyphs:
            execute(band['ops'][glyph], state)
        states.append(state)
        traces.append({'channel': channel, 'current_raw_integer': value,
                       'opposite_raw_integers': json.dumps(opposite),
                       'current_numerals': encoded, 'executed_commands': glyphs,
                       **{'before_' + reg: before[reg] for reg in REGS},
                       **{'after_' + reg: state[reg] for reg in REGS}})
    output = [s['target'] for s in states] if direction == 'x_to_y' else [[s['state'], s['relations']] for s in states]
    return output, traces


def views(output):
    return [{'active_channel': active + 1,
             'donor_channels': [donor + 1 for donor in range(4) if donor != active],
             'values': [output[donor] for donor in range(4) if donor != active]}
            for active in range(4)]


def checks(bands, table):
    opposite = [11, 22, 33, 44]
    seeded = seed_bank(opposite, DEFAULT_MAPPING)
    assert [seeded[k] for k in DEFAULT_MAPPING] == opposite
    assert all(seeded[k] == 1 for k in REGS if k not in DEFAULT_MAPPING)
    for view in views([10, 20, 30, 40]):
        assert len(view['values']) == 3 and view['active_channel'] not in view['donor_channels']
    x = [b['frames'][0]['rounded'] for b in bands]
    y = [b['frames'][-1]['rounded'] for b in bands]
    forward, traces = phase(x, y, 'x_to_y', bands, table)
    repeated, _ = phase(x, y, 'x_to_y', bands, table)
    assert forward == repeated
    assert all(t['before_' + k] == v for t in traces for k, v in zip(DEFAULT_MAPPING, y))
    reverse, _ = phase(forward, x, 'y_to_x', bands, table)
    assert len(forward) == len(reverse) == 4 and all(len(pair) == 2 for pair in reverse)
    return sum(validate(b['ops']) for b in bands)


def write_json(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Never overwrite any file from a previous experiment.
    if args.output.exists():
        raise FileExistsError('Choose a fresh output directory: ' + str(args.output))
    extractor = args.repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py'
    table = numeral_table(extractor)
    bands = load_archive(args.archive, table)
    validation_cases = checks(bands, table)
    n = len(bands[0]['frames'])
    args.output.mkdir(parents=True)
    totals = {'channel_roundtrips': n * 4, 'state_matches_original_x': 0,
              'relations_matches_original_x': 0, 'either_matches_original_x': 0,
              'both_match_original_x': 0, 'forward_target_matches_recorded_y': 0,
              'state_reforward_matches_projected_target': 0,
              'relations_reforward_matches_projected_target': 0}
    trace_fields = ['row', 'opposite_row', 'direction', 'channel', 'current_raw_integer',
                    'opposite_raw_integers', 'current_numerals', 'executed_commands']
    trace_fields += ['before_' + k for k in REGS] + ['after_' + k for k in REGS]
    summary_fields = ['row', 'second', 'opposite_row', 'opposite_second', 'x_raw_amplitudes',
                      'y_raw_amplitudes', 'x_rounded', 'y_rounded', 'forward_target',
                      'reverse_state_relations', 'state_matches', 'relations_matches',
                      'forward_other_channel_views', 'reverse_other_channel_views']
    example = None
    with (args.output / 'register_trace.csv').open('x', newline='', encoding='utf-8') as trace_file, (args.output / 'phases.csv').open('x', newline='', encoding='utf-8') as phase_file:
        tw = csv.DictWriter(trace_file, fieldnames=trace_fields)
        sw = csv.DictWriter(phase_file, fieldnames=summary_fields)
        tw.writeheader()
        sw.writeheader()
        for row in range(n):
            other = n - 1 - row
            x = [b['frames'][row]['rounded'] for b in bands]
            y = [b['frames'][other]['rounded'] for b in bands]
            projected, forward_trace = phase(x, y, 'x_to_y', bands, table)
            restored, reverse_trace = phase(projected, x, 'y_to_x', bands, table)
            state_back = [pair[0] for pair in restored]
            relations_back = [pair[1] for pair in restored]
            reforward_state, _ = phase(state_back, x, 'x_to_y', bands, table)
            reforward_relations, _ = phase(relations_back, x, 'x_to_y', bands, table)
            sm = [a == b for a, b in zip(state_back, x)]
            rm = [a == b for a, b in zip(relations_back, x)]
            totals['state_matches_original_x'] += sum(sm)
            totals['relations_matches_original_x'] += sum(rm)
            totals['either_matches_original_x'] += sum(a or b for a, b in zip(sm, rm))
            totals['both_match_original_x'] += sum(a and b for a, b in zip(sm, rm))
            totals['forward_target_matches_recorded_y'] += sum(a == b for a, b in zip(projected, y))
            totals['state_reforward_matches_projected_target'] += sum(a == b for a, b in zip(reforward_state, projected))
            totals['relations_reforward_matches_projected_target'] += sum(a == b for a, b in zip(reforward_relations, projected))
            for direction, traces in [('x_to_y', forward_trace), ('y_to_x', reverse_trace)]:
                for trace in traces:
                    tw.writerow({'row': row, 'opposite_row': other, 'direction': direction, **trace})
            result = {'row': row, 'second': bands[0]['frames'][row]['second'],
                      'opposite_row': other, 'opposite_second': bands[0]['frames'][other]['second'],
                      'x_raw_amplitudes': [b['frames'][row]['amplitude'] for b in bands],
                      'y_raw_amplitudes': [b['frames'][other]['amplitude'] for b in bands],
                      'x_rounded': x, 'y_rounded': y, 'forward_target': projected,
                      'reverse_state_relations': restored, 'state_matches': sm,
                      'relations_matches': rm, 'forward_other_channel_views': views(projected),
                      'reverse_other_channel_views': views(restored)}
            sw.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in result.items()})
            if row == 0:
                example = result
    # Test the consistency-only hypothesis on all 24 assignments for the first endpoint pair.
    mappings = []
    for mapping in itertools.permutations(DEFAULT_MAPPING):
        output, _ = phase(example['x_rounded'], example['y_rounded'], 'x_to_y', bands, table, mapping)
        back, _ = phase(output, example['x_rounded'], 'y_to_x', bands, table, mapping)
        mappings.append({'mapping_y1_y2_y3_y4': list(mapping), 'forward_target': output,
                         'reverse_state_relations': back,
                         'matches_default_forward': output == example['forward_target'],
                         'either_reverse_matches': sum(x in pair for x, pair in zip(example['x_rounded'], back))})
    write_json(args.output / 'mapping_comparison.json', mappings)
    write_json(args.output / 'first_row.json', example)
    report = {'branch': 'codex/atlas-endpoint-phase-test',
              'status': 'Executed candidate endpoint-seeded wiring; no assumed scalar reduction of reverse pairs.',
              'archive': str(args.archive), 'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'sources': [{k: b[k] for k in ('source', 'sha256')} for b in bands],
              'rows_per_channel': n, 'mapping_y1_y2_y3_y4': DEFAULT_MAPPING,
              'other_register_seed': 1, 'operator_validation_cases': validation_cases,
              'operator_encoding_rows_verified': n * 4,
              'execution': 'Archived x86-64 operator bodies interpreted, unsigned 64-bit arithmetic; no native binary run.',
              'rules': ['Opposite row is N-1-row, within each saved ranked stripe.',
                        'Use saved rounded integers before numeral decoding; retain float amplitudes in output.',
                        'All four channel banks receive the four opposite raw seeds in the same fixed assignment.',
                        'Each bank processes its own current input; banks are snapshotted before other-channel extraction.',
                        'X->Y uses original glyph order and reads one target per donor channel.',
                        'Y->X uses reverse glyph order and reads state and relations per donor channel.',
                        'Reverse current input is the four projected targets; reverse opposite seeds are original x values.',
                        'Each active channel excludes itself from three-donor output views.',
                        'Remaining register seeds are 1; rows are independent endpoint-pair tests, not a continuous sweep.',
                        'Channel-bank wiring and scalar-to-command encoding are explicit test choices, not a recovered four-lane implementation.'],
              'totals': totals, 'mapping_trials_first_row': len(mappings),
              'distinct_forward_outputs_across_mappings': len({tuple(m['forward_target']) for m in mappings}),
              'limitations': ['Ranked stripes may change frequency identity between ends.',
                              'Four raw seeds to eight registers is a provisional mapping; only permutations of these four slots were tested.',
                              'Reversed glyph order is the repository reversal convention, not an algebraic inverse.',
                              'Independent channel banks do not allow an active channel input to change another bank; other-channel views expose this assumption.',
                              'The original four-lane all-register-feedback assembly dependency is absent.']}
    write_json(args.output / 'report.json', report)
    print(json.dumps({'totals': totals, 'mapping_trials': len(mappings),
                      'distinct_forward_outputs': report['distinct_forward_outputs_across_mappings'],
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
