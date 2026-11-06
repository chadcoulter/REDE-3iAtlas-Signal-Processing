"""Inspect the Tanakh parser stream without changing its operator semantics."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
ATLAS = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ATLAS/'experiments/endpoint_phase_v1'))
from operator_machine import REGS, reference


def main():
    mapping = {}
    with (ROOT/'hebrew_greek_assembly_mapping.csv').open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            mapping[row['hebrew']] = row['greek_numeral_operator']
    text = (ROOT/'tanakh_reconstructed.txt').read_bytes().decode('utf-8')
    stream = ''.join(mapping[ch] for ch in text)
    # Confirm the inspectable IR is exactly the sequence being analyzed.
    position = 0
    with (ROOT/'tanakh_parser_instructions.jsonl').open(encoding='utf-8') as f:
        for line in f:
            for instruction in json.loads(line)['instructions']:
                assert instruction['index'] == position
                assert instruction['source'] == text[position]
                assert instruction['operator'] == stream[position]
                position += 1
    assert position == len(text)
    counts = collections.Counter(stream)
    state = dict.fromkeys(REGS,1)
    branches = collections.Counter()
    resets = []
    for index,glyph in enumerate(stream):
        if glyph == 'Υ':
            branches['odd_increment_context' if state['constraints']&1 else 'even_increment_relations'] += 1
        if glyph == 'Α':
            resets.append(index)
        reference(glyph,state)
    old_report = json.loads((ROOT/'assembly_report.json').read_text(encoding='utf-8'))
    assert state == old_report['final_registers']
    reset_gaps = [b-a for a,b in zip(resets,resets[1:])]
    experiments = [{'case':'source_order_seed_1','final_registers':state}]
    for seed in (0,2):
        result = dict.fromkeys(REGS,seed)
        for glyph in stream:
            reference(glyph,result)
        experiments.append({'case':f'source_order_seed_{seed}','final_registers':result})
    for name,sequence in [('reverse_order',reversed(stream)),('shuffled_seed_231',None)]:
        if sequence is None:
            sequence = list(stream)
            random.Random(231).shuffle(sequence)
        result = dict.fromkeys(REGS,1)
        for glyph in sequence:
            reference(glyph,result)
        experiments.append({'case':name,'final_registers':result})
    frequencies = []
    for glyph,count in counts.most_common():
        frequencies.append({'operator':glyph,'count':count,'percent':round(100*count/len(stream),4),
                            'source_glyphs':[ch for ch,g in mapping.items() if g==glyph]})
    offsets = []
    for offset in range(10):
        frame_counts = collections.Counter(stream[i:i+10] for i in range(offset,len(stream)-9,10))
        offsets.append({'offset':offset,'complete_frames':sum(frame_counts.values()),
                        'distinct_frames':len(frame_counts),'repeated_frame_types':sum(v>1 for v in frame_counts.values()),
                        'top_frames':[{'operators':s,'count':n} for s,n in frame_counts.most_common(5)]})
    role_counts = collections.Counter('control' if i%5<2 else 'data' for i in range(len(stream)))
    report = {'source_characters':len(text),'distinct_source_glyphs':len(set(text)),
              'distinct_operators':len(counts),'instruction_frequencies':frequencies,
              'state_reset':{'count':len(resets),'first_index':resets[0],'last_index':resets[-1],
                             'maximum_distance_between_resets':max(reset_gaps),
                             'mean_distance_between_resets':sum(reset_gaps)/len(reset_gaps),
                             'scope':'Only state is overwritten; other cells retain their histories.'},
              'conditional_branches':dict(branches),
              'control_flow':'Sequential dispatch; only forward local branches inside Υ; no backward program branches, calls, or data-dependent source-position selection.',
              'register_feedback':'Cells carry across every character and ten-letter display boundary.',
              'numeric_encoding':'Gematria values are represented as Greek numerals, not alphabet-position transliteration.',
              'numerical_aliases':{'ב/כ/ך':'Β and Κ have identical archived bodies: increment context',
                                   'final_forms':'Final and ordinary forms with equal gematria dispatch to the same operator; original glyphs are retained in IR.'},
              'display_frame_alignment_comparison':offsets,'experiments':experiments,
              'two_control_three_data':{'candidate_roles':dict(role_counts),
                                         'status':'No existing operand rule connects the three proposed data symbols to the first two operators. Current Atlas bodies use fixed register operands.'},
              'interpretation':'These are behaviors of the selected Atlas mapping on this supplied reconstructed file. Repetition and execution alone do not establish recovered instruction boundaries or a purpose.'}
    (ROOT/'instruction_findings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('display_frame_alignment_comparison','instruction_frequencies')},ensure_ascii=True))
    print(json.dumps({'top_operators':frequencies[:6],'alignment_zero':offsets[0]},ensure_ascii=True))


if __name__ == '__main__':
    main()
