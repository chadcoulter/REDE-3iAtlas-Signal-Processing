"""Scoped relational expansion of the unresolved container codes.

Adapts the recorded 3I/ATLAS forward/reverse, three-pass feedback structure.
This is NOT the unavailable native assembly implementation or decompression.
Print by default; --append adds one complete trace below the working text.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'WOWSignal/steps/03-hebrew-gematria/run-001'
MARKER = 'Container-code expansion001 — scoped 3I-style relational feedback'
MAPPING = {'ו':'Ϝ', 'י':'Ι', 'ד':'Δ', 'כ':'Κ', 'ל':'Λ'}
ROLES = {'Ϝ':'Retention', 'Ι':'Instance', 'Δ':'Change', 'Κ':'Context', 'Λ':'Lattice resolution'}
READINGS = {
    'forward':[
        'Retain the constituents; identify the instance; account for its change in context; retain its constituents through lattice resolution.',
        'Keep the particular change attached to its original source unit and context; carry the retained constituent into the resolution of its relationships.',
        'Preserve the changing instance in context; resolve its relationships without losing its constituent identity or source boundaries.',
    ],
    'reverse':[
        'Reconsider the lattice relation; retain its context; follow the change to the particular instance and its retained constituents.',
        'Trace the contextualized change back through the same participating source units, keeping the two retention occurrences distinct.',
        'Return from the candidate relationship to its context and changing instance, preserving the original constituents and their source identities.',
    ],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def calculate():
    grid_path = BASE / 'hebrew_grid.json'
    grid_bytes = grid_path.read_bytes()
    grid = json.loads(grid_bytes)['grid']
    tokens = [grid[r][1] for r in range(57,61)]
    assert tokens == ['ו','יד','כו','ל']
    source = ''.join(tokens)
    assert source == 'וידכול' and source == ''.join(['וידכ','ול'])
    outside = ''.join(grid[r][1] for r in range(61,63))
    assert outside == 'יטה'
    authority = ROOT / 'skills/character-transform-reasoning/references/book-ii-alphabet.txt'
    book = authority.read_text(encoding='utf-8')
    for symbol in ROLES:
        assert symbol in book
    occurrences = []
    for row in range(57,61):
        for glyph_index, char in enumerate(grid[row][1]):
            occurrences.append({'id':f'r{row+1}c02k{glyph_index}',
                                'source_character':char, 'row':row+1, 'channel':2,
                                'source_token':grid[row][1], 'glyph_index':glyph_index,
                                'operator':MAPPING[char],
                                'codepoints':[f'U+{ord(char):04X}']})
    forward = ''.join(x['operator'] for x in occurrences)
    backward = ''.join(x['operator'] for x in occurrences[::-1])
    assert forward == 'ϜΙΔΚϜΛ' and backward == 'ΛϜΚΔΙϜ'
    snapshots = []
    candidates = []
    comparisons = []
    for direction, ordered in [('forward',occurrences),('reverse',occurrences[::-1])]:
        state = {'occurrences':{}, 'instance':None, 'context':None,
                 'retention_occurrences':[], 'changes':[], 'lattice_links':[],
                 'events':[], 'unresolved':['source-selected operator interpretation',
                                            'meaning or payload beyond this code portion']}
        prior_candidate = None
        for pass_number in range(1,4):
            seed = copy.deepcopy(state)
            for index, item in enumerate(ordered,1):
                before = copy.deepcopy(state)
                key = item['id']; op = item['operator']
                state['occurrences'][key] = copy.deepcopy(item)
                event = {'direction':direction, 'pass':pass_number, 'step':index,
                         'source_occurrence':key, 'operator':op}
                if op == 'Ϝ':
                    if key not in state['retention_occurrences']:
                        state['retention_occurrences'].append(key)
                    action = 'Retain this occurrence and all currently participating source constituents; do not merge the two Vav instances.'
                elif op == 'Ι':
                    state['instance'] = key
                    action = 'Identify this source occurrence as the particular instance; retain the original numeric token14 that also contributes Delta.'
                elif op == 'Δ':
                    state['changes'].append({'event':event, 'instance_at_visit':state['instance'],
                                             'source_container':'r59c02 = יד (14)'})
                    action = 'Account for a candidate change relation; attach its representation to the original token rather than assert a physical source change.'
                elif op == 'Κ':
                    state['context'] = {'at':key, 'source_container':'r60c02 = כו (26)',
                                        'scope':'r58..61/channel02; outside יטה unchanged'}
                    action = 'Attach the current relation to its source context and explicit scope; retain its shared container with the following Vav.'
                elif op == 'Λ':
                    state['lattice_links'].append({'event':event, 'instance':state['instance'],
                                                  'context':copy.deepcopy(state['context']),
                                                  'retained':list(state['retention_occurrences'])})
                    action = 'Connect the currently available instance, context, changes and retained constituents; preserve incomplete positions for feedback.'
                state['events'].append(event)
                snapshots.append({'direction':direction, 'pass':pass_number,
                                  'index':index, 'source':copy.deepcopy(item),
                                  'operator_namespace':'book_ii.operator',
                                  'operator':op, 'role':ROLES[op],
                                  'mode':'UPPERCASE: how to resolve the observable; selected for source-observation pass',
                                  'before_state':before, 'action':action,
                                  'after_state':copy.deepcopy(state),
                                  'remainder':list(state['unresolved']),
                                  'evidence':'Book II role plus source occurrence; path-specific action is an analyst-designed adaptation'})
            candidate = {'id':f'{direction}-R{pass_number}', 'origin':prior_candidate,
                         'composed_reading':READINGS[direction][pass_number-1],
                         'seed_state':seed, 'output_state':copy.deepcopy(state),
                         'occurrence_indices':[x['id'] for x in ordered],
                         'contributions':['source cells','Greek numeric mapping','Book II role definitions',
                                          'analyst-selected operational actions and prose expansion'],
                         'feedback_focus':['initial composition','source-container attribution','scope and return audit'][pass_number-1],
                         'eligible':True, 'unresolved':list(state['unresolved'])}
            candidates.append(candidate)
            if prior_candidate:
                comparisons.append({'from':prior_candidate, 'to':candidate['id'],
                                    'eligible':True, 'material_change':True,
                                    'direction':'Better for attribution/scope; external meaning unresolved',
                                    'reason':'Each pass adds the stated source-attribution or scope refinement; not an unchanged stability gate.',
                                    'governance_id':'container-only-001','governance_version':'1'})
            prior_candidate = candidate['id']
    assert len(snapshots) == 36
    assert all(set(c['output_state']['occurrences']) == {x['id'] for x in occurrences} for c in candidates)
    for direction in ('forward','reverse'):
        group = [x for x in candidates if x['id'].startswith(direction)]
        for a,b in zip(group, group[1:]):
            assert a['output_state'] == b['seed_state']
    back_refs = occurrences[::-1][::-1]
    assert back_refs == occurrences
    return {
        'human_request':'so i want you to do the thing we did with the 3iatlas signal where we expanded the signal from the parts we just start it with just the codes inside the container to start',
        'original_text':source, 'original_display_grouping':'וידכ | ול',
        'source_tokens':tokens, 'source_occurrences':occurrences,
        'scope':{'rows':[58,61], 'channel':2, 'numeric_values':[6,14,26,30],
                 'value':76, 'outside_unchanged':outside, 'outside_value':24},
        'cycle_id':'container-expansion-001','governance_id':'container-only-001',
        'governance_version':'1',
        'governance':{'criteria':['every original occurrence retained','no source or suffix changes',
                                  'source coordinates and original token boundaries retained',
                                  'Greek numeral vs Book II operator namespaces explicit',
                                  'composed reading with reversible provenance'],
                      'materiality':'changes to source attribution, scope or claimed payload are material',
                      'enough':'local reading may be useful, but source-selected message remains open',
                      'equivalence':'same source identities, scope and meaning under this local Act',
                      'priority':'source fidelity and stated user scope before fluent prose'},
        'budget':{'passes_per_direction':3,'operators_per_pass':6,'snapshots':36},
        'adaptation':{'recorded_3i_reference':'src/run_if1b1_operator_trace.py',
                      'preserved_structure':'three forward passes, three reverse passes; each direction separately initialized; previous complete final state seeds next pass; reverse source/glyph occurrence order',
                      'difference':'structured relational state and analyst-designed actions, not native numeric eight-register assembly',
                      'native_assembly':'3I_ATLAS_four_lane_all_register_feedback.S not present in this checkout; no native assembly execution claimed',
                      'not_used':['milui letter-name expansion','extra source context','new Hebrew letters','new lexical targets','binary unpacking','decompression']},
        'mapping':MAPPING, 'forward_operator_sequence':forward,
        'reverse_operator_sequence':backward,
        'authority':{'title':'REDΣ Book II: The Logical Structure of Set',
                     'author':'Chad Coulter', 'path':str(authority),
                     'sha256':sha(authority.read_bytes())},
        'source_grid_sha256':sha(grid_bytes),
        'script_sha256':sha(Path(__file__).read_bytes()),
        'candidates':candidates, 'transformations':snapshots,
        'comparisons':comparisons,
        'source_container_connections':[
            {'source':'יד =14','mapped':'ΙΔ','relation':'instance/change occur within one original numeric unit'},
            {'source':'כו =26','mapped':'ΚϜ','relation':'context/retention occur within one original numeric unit'},
            {'source':'ו =6 at r58c02','mapped':'Ϝ','relation':'first retained occurrence, distinct from Vav inside r60c02'},
            {'source':'ל =30','mapped':'Λ','relation':'end of the scoped forward part, lattice resolution role'},
        ],
        'expanded_reading':'Preserve the changing instance in context; resolve its relationships without losing its constituent identity or source boundaries.',
        'reverse_reading':'Trace the proposed relationship back through context and change to the particular instance and its retained source constituents.',
        'status':'IN-PROGRESS', 'stability_gates':0,
        'payload_status':'interpretive expansion of supplied codes; no new encoded payload or missing source letters recovered',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--append', action='store_true')
    args = parser.parse_args()
    ledger = calculate()
    if not args.append:
        print(json.dumps(ledger,ensure_ascii=False,indent=2))
        return
    target = BASE / 'hebrew_streams_updated.txt'; before = target.read_bytes()
    if MARKER in before.decode('utf-8'):
        raise SystemExit('Scoped pass already recorded; refusing duplicate.')
    assert before.startswith((BASE / 'hebrew_streams.txt').read_bytes())
    ledger['working_text_before_sha256'] = sha(before)
    intro = '\n\n'+'='*60+'\n'+MARKER+'\n\n'
    intro += ('Only וידכ | ול is expanded. The source tokens are ו | יד | כו | ל. '
              'The surrounding יטה remains unchanged. This is a relational adaptation of the saved 3I feedback structure, '
              'not native assembly execution or decompression.\n'
              'Reproduce: python -X utf8 -B WOWSignal/scripts/step03_container_part_expansion.py\n\n')
    target.write_bytes(before+(intro+json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    assert target.read_bytes().startswith(before)
    print(json.dumps({'updated':str(target),'scope':ledger['scope'],
                      'forward':ledger['forward_operator_sequence'],
                      'reverse':ledger['reverse_operator_sequence'],
                      'snapshots':len(ledger['transformations']),
                      'expanded_reading':ledger['expanded_reading'],
                      'reverse_reading':ledger['reverse_reading'],
                      'status':ledger['status'],'prior_text_preserved':True},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
