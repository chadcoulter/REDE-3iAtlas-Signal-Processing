"""Greek correspondence, translated word families, and Book II trial.

Print a ledger by default; --append saves one pass below existing working text.
Historical character correspondence is not semantic translation or phonetics.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'WOWSignal/steps/03-hebrew-gematria/run-001'
MARKER = 'Greek trial001 — character correspondence, lexical roots, and Book II execution'
MAPPING = dict(zip('אבגדהוטיכל', 'ΑΒΓΔΕϜΘΙΚΛ'))
ROLES = {'Α':'Origin', 'Β':'Branch', 'Γ':'Boundary frame / transform operator',
         'Δ':'Change', 'Ε':'Threshold', 'Ϝ':'Resolve observable retained constituents',
         'Θ':'Constraint', 'Ι':'Instance', 'Κ':'Context', 'Λ':'Lattice resolution'}
ACTIONS = {
    'Α':'Anchor the current relation to its source occurrences; preserve the preceding transformed state.',
    'Β':'Register this path as a branch of the source network; retain alternative branches.',
    'Γ':'Frame the current path under its stated adjacency and mapping boundary; keep excluded alternatives visible.',
    'Δ':'Record Hebrew-to-Greek representation change while retaining the original source character and occurrence.',
    'Ε':'Mark a resolution threshold for the current relation; keep unresolved language/direction choices active.',
    'Ϝ':'Retain all source occurrences and distinctions accumulated in this path across the representation change.',
    'Θ':'Constrain the current relation by its recorded source coordinates and transformation rule; do not infer extra letters.',
    'Ι':'Identify this particular occurrence as an instance; do not merge repeated letters or shared cells.',
    'Κ':'Attach the source-path context and mapping convention to the current state.',
    'Λ':'Relate the accumulated path back to the wider crossing network; preserve unresolved branches rather than declaring closure.',
}
SOURCES = {
    'historical_alphabet':'https://www-old.phil.uoa.gr/fileadmin/phil.uoa.gr/uploads/linguistics/Pdf/papers/Pantelidis_2014_The_Greek_Alphabet___Scriptura_Mundi.pdf',
    'digamma':'https://unicode.org/L2/L2005/05003-epigraphical.pdf',
    'expression':'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/search.html?lq=εκφράζω',
    'expression_components':'https://www.greek-language.gr/digitalResources/modern_greek/education/lex_first_grade/search.html?lex=2&lq=&start=80',
    'well':'https://www.greek-language.gr/greekLang/ancient_greek/tools/lexicon/lemma.html?id=128',
    'checking':'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/search.html?dq=&lq=ελέγχω+-%CE%BF%CE%BC%CE%B1%CE%B9',
    'checking_ancient':'https://www.greek-language.gr/greekLang/ancient_greek/tools/lexicon/lemma.html?id=89',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def calculate():
    authority = Path(os.environ['USERPROFILE']) / '.codex/skills/character-transform-reasoning/references/book-ii-alphabet.txt'
    authority_bytes = authority.read_bytes()
    authority_text = authority_bytes.decode('utf-8')
    for glyph, role in ROLES.items():
        assert any(line.startswith(glyph + ' |') and role in line
                   for line in authority_text.splitlines()), (glyph, role)
    previous = runpy.run_path(str(ROOT / 'WOWSignal/scripts/step03_numerology_exploration.py'))['calculate']()
    traces = []
    for row in previous['results']:
        state = {'source_id':row['id'], 'source_hebrew':row['input'],
                 'retained_glyph_occurrences':[], 'operator_prefix':'',
                 'branches':[], 'constraints':[], 'contexts':[],
                 'origin_anchors':[], 'thresholds':[], 'changes':[],
                 'lattice_links':[], 'retention_events':[], 'frames':[]}
        occurrences = []
        for i, source in enumerate(row['source_occurrences'], 1):
            he = source['glyph']; gr = MAPPING[he]
            ref = {**source, 'sequence_index':i}
            state['retained_glyph_occurrences'].append(ref)
            state['operator_prefix'] += gr
            field = {'Α':'origin_anchors', 'Β':'branches', 'Γ':'frames',
                     'Δ':'changes', 'Ε':'thresholds', 'Ϝ':'retention_events',
                     'Θ':'constraints', 'Κ':'contexts', 'Λ':'lattice_links'}.get(gr)
            if field:
                state[field].append({'at':i, 'source':ref,
                                     'scope_prefix':state['operator_prefix']})
            # Iota identifies this occurrence through the retained occurrence list.
            occurrences.append({'index':i, 'source_character':he, 'source':ref,
                                'greek_operator':gr, 'book_ii_role':ROLES[gr],
                                'mode':'UPPERCASE: how to resolve the observable; analyst-selected mode',
                                'action':ACTIONS[gr],
                                'resulting_relation':state['operator_prefix'],
                                'retained_occurrence_count':len(state['retained_glyph_occurrences']),
                                'remainder':['semantic reading of numeral encoding', 'source-selected traversal', 'case choice']})
        text = state['operator_prefix']
        inverse = {v:k for k, v in MAPPING.items()}
        assert ''.join(inverse[x] for x in text) == row['input']
        assert len(occurrences) == len(row['input'])
        traces.append({'id':row['id'], 'hebrew':row['input'], 'greek':text,
                       'full_reverse':text[::-1], 'per_occurrence':occurrences,
                       'final_state':state})
    lexical = [
        {'hebrew':'ביטא', 'greek_lemma':'εκφράζω', 'past_third_singular':'εξέφρασε',
         'meaning':'expressed / articulated', 'root_family':'ἐκ- + φράζω; φραζ-/φρασ-',
         'relation':'make a thought or feeling manifest; expression/articulation',
         'source':SOURCES['expression'], 'components_source':SOURCES['expression_components']},
        {'hebrew':'היטב', 'greek_equivalent':'καλῶς', 'root_family':'καλός; καλ-',
         'meaning':'well / properly', 'relation':'quality or manner of an act, not a new actor',
         'source':SOURCES['well']},
        {'hebrew':'וידא', 'greek_lemma':'ελέγχω', 'past_third_singular':'έλεγξε',
         'meaning':'checked / examined for correctness', 'root_family':'ἐλεγχ-',
         'relation':'test or examine an expression against evidence',
         'translation_choice':'Checking is a context-selected rendering of verified/made sure; not the only Greek translation.',
         'source':SOURCES['checking'], 'ancient_source':SOURCES['checking_ancient']},
    ]
    return {'trial_id':'greek-001', 'script_sha256':sha(Path(__file__).read_bytes()),
            'authority':{'title':'REDΣ Book II: The Logical Structure of Set',
                         'author':'Chad Coulter', 'date':'2026-10-13', 'version':'0.1',
                         'path':str(authority), 'sha256':sha(authority_bytes)},
            'source_grid_sha256':previous['source_grid_sha256'],
            'mapping':MAPPING, 'mapping_sources':SOURCES,
            'conventions':[
                'West-Semitic/Phoenician-derived correspondence used as an explicit experimental mapping, not a claim Greek descends from Hebrew.',
                'Vav maps to archaic Digamma Ϝ; Upsilon Υ remains a historical alternative not substituted mid-run.',
                'He maps to Epsilon Ε, not Eta Η. Tet maps to Theta Θ, not Tau Τ. Gimel maps to Gamma Γ.',
                'No vowels are reconstructed. Mapped strings are operator carriers, not asserted grammatical Greek words.',
                'Uppercase is chosen for the source-observation pass. Hebrew itself provides no case information. No final sigma closure is introduced.',
                'Book II supplies operator definitions; path-specific actions and compositions are analyst interpretations, not automated linguistic validation.',
                'Lexical translations use selected Greek words and their word families. They are not Hebrew etymologies or proof of Greek/Hebrew cognacy.',
                'Only original candidate strings are mapped; no combination of Atbash, milui, and Greek mapping is silently introduced.',
            ], 'traces':traces, 'lexical_translation_roots':lexical,
            'compositions':[
                {'source':'ביטא', 'mapped':'ΒΙΘΑ',
                 'reading':'A branch is identified as an instance, constrained, and anchored to its origin.'},
                {'source':'היטב', 'mapped':'ΕΙΘΒ',
                 'reading':'An instance reaches a threshold under constraint and remains available as a branch.'},
                {'source':'וידא', 'mapped':'ϜΙΔΑ',
                 'reading':'Retain the instance across a recorded change and reconnect it to the origin.'},
                {'source':'אג', 'mapped':'ΑΓ',
                 'reading':'Origin and boundary frame; this is a mapped operator fragment, not an expanded Greek verb.'},
                {'source':'גל', 'mapped':'ΓΛ',
                 'reading':'Boundary frame and lattice resolution; distinguish from the Hebrew noun wave/heap/shaft.'},
                {'source':'כו', 'mapped':'ΚϜ',
                 'reading':'Context with retained constituents; does not substitute for an equal-valued multi-cell loop.'},
            ],
            'working_synthesis':'Keep the originating instance identifiable while it changes; constrain and check its expression against the source. Analyst synthesis across both passes, not a recovered sentence.',
            'shared_cell_connection':{'source':[62, 2], 'hebrew':'יט', 'greek':'ΙΘ',
                                      'operator_relation':'Instance ↔ Constraint',
                                      'in':['ΒΙΘΑ','ΕΙΘΒ'],
                                      'full_reverse':'ΘΙ',
                                      'reverse_relation':'Constraint ↔ Instance',
                                      'independence':'same source cell, not independent evidence'},
            'unresolved':['source-selected Hebrew encoding', 'path and word boundaries',
                          'choice of translation equivalents', 'capitalization and alternate Waw mapping'],
            'enough':False, 'inserted_source_letters':0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--append', action='store_true')
    args = parser.parse_args()
    ledger = calculate()
    if not args.append:
        print(json.dumps(ledger, ensure_ascii=False, indent=2))
        return
    target = BASE / 'hebrew_streams_updated.txt'
    before = target.read_bytes()
    if MARKER in before.decode('utf-8'):
        raise SystemExit('Greek trial already appended; refusing duplicate.')
    assert before.startswith((BASE / 'hebrew_streams.txt').read_bytes())
    ledger['working_text_before_sha256'] = sha(before)
    note = '\n\n' + '='*60 + '\n' + MARKER + '\n\n'
    note += ('Two routes remain separate: (A) historical character-correspondence carriers executed under Chad Coulter\'s Book II; '
             '(B) selected semantic Greek translations and actual Greek lexical families. '
             'Both preserve the candidate status of the Hebrew path readings.\n'
             'Reproduce without writes: python -X utf8 -B WOWSignal/scripts/step03_greek_root_exploration.py\n\n')
    target.write_bytes(before + (note + json.dumps(ledger, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    assert target.read_bytes().startswith(before)
    print(json.dumps({'updated':str(target),
                      'mapping':MAPPING,
                      'mapped_candidates':[{'hebrew':x['hebrew'], 'greek':x['greek'], 'reverse':x['full_reverse']} for x in ledger['traces']],
                      'occurrences_executed':sum(len(x['per_occurrence']) for x in ledger['traces']),
                      'shared_cell':ledger['shared_cell_connection'],
                      'working_synthesis':ledger['working_synthesis'],
                      'prior_text_preserved':True}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
