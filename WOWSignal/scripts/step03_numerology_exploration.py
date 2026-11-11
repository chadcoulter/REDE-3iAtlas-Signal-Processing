"""Reproduce a bounded, explicitly conventional gematria exploration.

Default: print JSON without writing. --append: append one ledger to the working
text. Never modify source observations or label generated letters as recovered.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'WOWSignal/steps/03-hebrew-gematria/run-001'
ALPHABET = 'אבגדהוזחטיכלמנסעפצקרשת'
VALUES = dict(zip(ALPHABET, list(range(1, 11)) +
                  [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400]))
FINALS = str.maketrans('ךםןףץ', 'כמנפצ')
NAMES = dict(zip(ALPHABET, [
    'אלף', 'בית', 'גימל', 'דלת', 'הא', 'ואו', 'זין', 'חית', 'טית',
    'יוד', 'כף', 'למד', 'מם', 'נון', 'סמך', 'עין', 'פא', 'צדי',
    'קוף', 'ריש', 'שין', 'תו']))
ATBASH = dict(zip(ALPHABET, ALPHABET[::-1]))
ALBAM = {ch: ALPHABET[(i + 11) % 22] for i, ch in enumerate(ALPHABET)}
MARKER = 'Numerology trial 001 — fixed rules, milui variants, and full ledger'
SOURCES = [
    'https://www.chabad.org/library/article_cdo/aid/6664656/jewish/Gematria-FAQ.htm',
    'https://targum.shaulmolcho.com/gematria',
    'https://targum.shaulmolcho.com/letters',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def total(text):
    return sum(VALUES[ch] for ch in text.translate(FINALS))


def root(value):
    return 0 if value == 0 else 1 + (value - 1) % 9


def change(text, table):
    return ''.join(table[ch] for ch in text)


def calculate():
    grid_path = BASE / 'hebrew_grid.json'
    grid_bytes = grid_path.read_bytes()
    grid = json.loads(grid_bytes)['grid']

    def refs(cells):
        return [{'row':r + 1, 'channel':c + 1, 'glyph_index':i, 'glyph':ch}
                for r, c in cells for i, ch in enumerate(grid[r][c])]

    event = refs([(r, 1) for r in range(57, 63)])
    expression = refs([(61, 0), (61, 1), (61, 2)])
    selected = {
        'event_forward': event,
        'event_full_reverse': event[::-1],
        'expression': expression,
        'expression_full_reverse': expression[::-1],
        'well': refs([(62, 1), (61, 1), (61, 0)]),
        'verified': refs([(57, 1), (58, 1), (58, 0)]),
        'his_hand': refs([(58, 1), (57, 1)]),
        'aramaic_hand': refs([(58, 1), (58, 0)]),
        'upper_gal_path': refs([(61, 0), (61, 1), (61, 2), (60, 2), (60, 1)]),
        'single_26_cell': refs([(59, 1)]),
        'lower_26_loop': refs([(61, 1), (61, 2), (62, 2), (62, 1)]),
    }
    results = []
    for name, occurrences in selected.items():
        text = ''.join(x['glyph'] for x in occurrences)
        expansions = []
        # Nine consistent per-letter spelling conventions, not arbitrary changes
        # to individual occurrences and not all possible historical spellings.
        for he, vav in itertools.product(('הא', 'הי', 'הה'), ('ואו', 'ויו', 'וו')):
            table = dict(NAMES, ה=he, ו=vav)
            parts = [table[ch] for ch in text]
            expansions.append({'he_spelling':he, 'vav_spelling':vav,
                               'parts':parts, 'expanded_text':' '.join(parts),
                               'value':total(''.join(parts))})
        at = change(text, ATBASH)
        al = change(text, ALBAM)
        assert change(at, ATBASH) == text
        assert change(al, ALBAM) == text
        katan_parts = [root(VALUES[ch]) for ch in text]
        results.append({
            'id':name, 'input':text, 'source_occurrences':occurrences,
            'standard':total(text),
            'ordinal':sum(ALPHABET.index(ch) + 1 for ch in text),
            'katan_parts':katan_parts, 'katan_sum':sum(katan_parts),
            'digital_root_of_standard':root(total(text)),
            'atbash':at, 'atbash_standard':total(at),
            'albam':al, 'albam_standard':total(al),
            'full_glyph_reverse':text[::-1], 'milui':expansions,
            'interpretation':'generated alternatives; no lexical validation assigned',
        })
    word_ids = ('expression', 'well', 'verified')
    lookup = {x['id']:x for x in results}
    initials = []
    for order in itertools.permutations(word_ids):
        words = [lookup[key]['input'] for key in order]
        initials.append({'word_ids':order, 'editorial_words':words,
                         'initials':''.join(word[0] for word in words),
                         'endings':''.join(word[-1] for word in words),
                         'status':'initial/end-letter extraction from editorial grouping; no acronym expansion supplied'})
    for ch in ALPHABET:
        assert ATBASH[ATBASH[ch]] == ch and ALBAM[ALBAM[ch]] == ch
    a = lookup['single_26_cell']; b = lookup['lower_26_loop']
    comparisons = {method:{'single_cell':a[method], 'loop':b[method],
                            'equal':a[method] == b[method]}
                   for method in ('standard', 'ordinal', 'katan_sum',
                                  'digital_root_of_standard', 'atbash_standard',
                                  'albam_standard')}
    return {
        'trial_id':'numerology-001',
        'source_grid_sha256':digest(grid_bytes),
        'script_sha256':digest(Path(__file__).read_bytes()),
        'method_sources':SOURCES,
        'rules':{
            'alphabet':ALPHABET, 'standard_values':VALUES,
            'atbash':ATBASH, 'albam':ALBAM,
            'ordinal':'1-based position in the 22-letter alphabet',
            'katan':'digital root of EACH standard letter value, then sum; do not collapse total silently',
            'digital_root':'1+(n-1)%9 for n>0, 0 for n=0; numeric-only result',
            'milui':'One expansion per original letter, not recursive; fixed spelling table plus nine He/Vav conventions; finals normalized only for counting',
            'default_letter_names':NAMES,
            'milui_scope':'He/Vav variants are explicitly chosen trial conventions, not a claim of exhaustive received systems',
            'notarikon_style_extraction':'Initials and endings of the three previously assembled words in all six orders; word boundaries are editorial',
            'original_zeros':'Never transformed, expanded, replaced, or treated as unknown letters',
            'completion':'No external independently observed constraint specifies a missing source letter; these methods generate candidates, not recovered measurements',
            'composition':'One method per input, plus original full-reverse inputs; no recursive transform search or word-target substitution',
        },
        'counts':{'inputs':len(results), 'atbash_results':len(results),
                  'albam_results':len(results), 'milui_records':9*len(results),
                  'initial_ending_records':len(initials)},
        'results':results, 'initials_and_endings':initials,
        'single_cell_vs_loop':comparisons,
        'conclusion':'New transformed candidates recorded. No new source letters or confirmed message recovered. Equalities and failed equalities remain visible.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--append', action='store_true')
    args = parser.parse_args()
    ledger = calculate()
    if not args.append:
        print(json.dumps(ledger, ensure_ascii=False, indent=2))
        return
    target = BASE / 'hebrew_streams_updated.txt'
    previous = target.read_bytes()
    if MARKER in previous.decode('utf-8'):
        raise SystemExit('Trial already appended; refusing duplicate.')
    original = (BASE / 'hebrew_streams.txt').read_bytes()
    assert previous.startswith(original)
    ledger['working_text_before_sha256'] = digest(previous)
    preface = '\n\n' + '='*60 + '\n' + MARKER + '\n\n'
    preface += ('Methods are traditional interpretive or substitution conventions, not established signal decoding. '
                'Milui fills LETTER NAMES; generated letters do not replace original observations. '
                'Every input, convention and output below is retained, including unparsed results.\n'
                'Reproduce without writes: python -X utf8 -B WOWSignal/scripts/step03_numerology_exploration.py\n'
                'Append once: add --append. Original working text remains an exact byte prefix.\n\n')
    target.write_bytes(previous + (preface + json.dumps(ledger, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    assert target.read_bytes().startswith(previous)
    print(json.dumps({'updated':str(target), 'counts':ledger['counts'],
                      'single_cell_vs_loop':ledger['single_cell_vs_loop'],
                      'selected':[{'input':x['input'], 'atbash':x['atbash'], 'albam':x['albam'],
                                   'standard':x['standard'], 'ordinal':x['ordinal'],
                                   'katan':x['katan_sum']}
                                  for x in ledger['results']],
                      'prior_text_preserved':True}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
