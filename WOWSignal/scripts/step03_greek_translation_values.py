"""Translate the current candidate phrase first; compare word totals second.

Print a ledger by default. --append adds it once to the existing text file.
The small, manually selected Greek comparison bank is not exhaustive.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'WOWSignal/steps/03-hebrew-gematria/run-001'
MARKER = 'Translation first, Greek numerical equality second — trial001'
GREEK_VALUES = dict(zip('αβγδεϝζηθικλμνξοπϟρστυφχψωϡ',
                        list(range(1,10)) + list(range(10,100,10)) + list(range(100,1000,100))))


def greek(text):
    decomposed = unicodedata.normalize('NFD', text.lower())
    # Retain a subscript iota as an iota, while removing accents/breathings.
    decomposed = decomposed.replace('\u0345', 'ι')
    plain = ''.join(ch for ch in decomposed if not unicodedata.combining(ch))
    plain = plain.replace('ς','σ').replace('ϛ','ϝ').replace('ϙ','ϟ')
    letters = [ch for ch in plain if ch.isalpha()]
    if any(ch not in GREEK_VALUES for ch in letters):
        raise ValueError('Unsupported Greek letters: ' + plain)
    parts = [{'letter':ch, 'value':GREEK_VALUES[ch]} for ch in letters]
    return {'written':text, 'normalized':''.join(letters), 'parts':parts,
            'total':sum(x['value'] for x in parts)}


def calculate():
    earlier = runpy.run_path(str(ROOT / 'WOWSignal/scripts/step03_numerology_exploration.py'))['calculate']()
    inputs = {r['id']:r for r in earlier['results']}
    # Preserve the previously assembled phrase; do not present it as a native
    # contiguous source sentence. These equivalent choices are made for meaning,
    # before the numerical comparison; the values do not determine translation.
    translations = [
        ('expression', 'εξέφρασε', 'he/it expressed', 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/search.html?lq=εκφράζω'),
        ('well', 'καλώς', 'well / properly', 'https://www.greek-language.gr/greekLang/ancient_greek/tools/lexicon/lemma.html?id=128'),
        ('verified', 'έλεγξε', 'he/it checked; context-selected equivalent of verified', 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/search.html?dq=&lq=ελέγχω+-%CE%BF%CE%BC%CE%B1%CE%B9'),
    ]
    translated = []
    for key, word, gloss, source in translations:
        inp = inputs[key]
        translated.append({'hebrew':inp['input'], 'hebrew_value':inp['standard'],
                           'greek_translation':greek(word), 'gloss':gloss,
                           'source':source, 'source_occurrences':inp['source_occurrences'],
                           'translation_preserves_numeric_value':inp['standard'] == greek(word)['total']})
    bank = [
        ('ἀγαθή', 'good, feminine singular adjective; not the verb expressed', 'https://www.greek-language.gr/greekLang/ancient_greek/tools/lexicon/lemma.html?id=58'),
        ('ἀΐδια', 'everlasting things, neuter plural adjective used substantively; not the adverb well', 'https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionaries.v1%3Alsj-n2248/'),
        ('βέβαια', 'certainly / of course, modern Greek adverb; not the past-tense verb verified', 'https://christikolexiko.academyofathens.gr/index.php?catid=2&id=2&option=com_content&pageS=1228&view=article'),
        ('ἰδέα', 'form / idea, feminine singular noun', 'https://www.greek-language.gr/digitalResources/ancient_greek/tools/liddell-scott/search.html?lq=ἰδέα'),
        ('γαῖα', 'earth, poetic noun', 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/search.html?lq=Γαία'),
        ('ἀγαθά', 'good things, neuter plural; not the same inflection as ἀγαθή', 'https://www.greek-language.gr/greekLang/ancient_greek/tools/lexicon/lemma.html?id=58'),
    ]
    bank_results = [{**greek(word), 'gloss':meaning, 'source':source,
                     'selection':'manually selected illustrative vocabulary; not exhaustive or random'}
                    for word, meaning, source in bank]
    bank_results += [{**greek(word), 'gloss':gloss, 'source':source,
                      'selection':'meaning-based translation candidate above'}
                     for _, word, gloss, source in translations]
    numeric_matches = []
    for key, inp in inputs.items():
        hits = [x for x in bank_results if x['total'] == inp['standard']]
        numeric_matches.append({'id':key, 'hebrew':inp['input'], 'hebrew_total':inp['standard'],
                                'source_occurrences':inp['source_occurrences'],
                                'equal_total_greek_candidates':hits,
                                'scope':'whole-word total only; not equal per-character values or translation',
                                'no_hit_means':'no hit in the selected bank only, not impossibility'})
    greek_to_greek = []
    for row in translated:
        v = row['greek_translation']
        hits = [x for x in bank_results if x['total'] == v['total'] and x['normalized'] != v['normalized']]
        greek_to_greek.append({'translated_word':v['written'], 'translated_total':v['total'],
                               'other_equal_total_bank_words':hits})
    phrase = 'εξέφρασε καλώς· έλεγξε'
    assert greek('ἀγαθή')['total'] == 22
    assert greek('ἀΐδια')['total'] == 26
    assert greek('βέβαια')['total'] == 21
    assert [r['greek_translation']['total'] for r in translated] == [876,1051,108]
    assert sum(r['hebrew_value'] for r in translated) == 69
    assert greek(phrase)['total'] == 2035
    return {
        'trial_id':'translation-equality-001',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_grid_sha256':earlier['source_grid_sha256'],
        'step1_translation':{'hebrew_candidate_assembly':'ביטא היטב; וידא',
                             'greek_translation':phrase,
                             'english':'He expressed well; he checked.',
                             'status':'translation of prior editorial candidate assembly, not an established contiguous source sentence',
                             'words':translated},
        'step2_numeric_comparison':{'greek_letter_values':GREEK_VALUES,
                                    'normalization':'lowercase, strip accents/breathings/diaeresis; retain subscript iota; normalize final sigma; do not change inflected spelling',
                                    'comparison_bank':bank_results,
                                    'hebrew_total_to_greek_word_matches':numeric_matches,
                                    'translated_greek_total_to_other_greek_words':greek_to_greek},
        'phrase_comparison':{'hebrew_assembly_total':69, 'greek_translation_total':2035,
                             'equal':False,
                             'equal_value_alternative_words_in_three_main_slots':'ἀγαθή | ἀΐδια | βέβαια',
                             'alternative_total':69,
                             'alternative_status':'three numerical substitutions; different meanings and morphology; NOT a grammatical translation or recovered message'},
        'bounds':['No Book II operator reading, historical letter substitution, or recursive cipher used in this pass.',
                  'Greek vocabulary includes labelled modern and ancient forms; it is not silently treated as one historically uniform sentence.',
                  'No match is promoted to semantic equivalence; unknown strings stay in place.',
                  'No source letters or zeros changed.'],
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
    before = target.read_bytes()
    if MARKER in before.decode('utf-8'):
        raise SystemExit('Trial already appended; refusing duplicate.')
    assert before.startswith((BASE / 'hebrew_streams.txt').read_bytes())
    ledger['working_text_before_sha256'] = hashlib.sha256(before).hexdigest()
    note = '\n\n' + '='*60 + '\n' + MARKER + '\n\n'
    note += 'Requested sequence: meaning translation FIRST; numerical equality SECOND. Both shown below, never substituted for each other.\n'
    note += 'Reproduce without writes: python -X utf8 -B WOWSignal/scripts/step03_greek_translation_values.py\n\n'
    target.write_bytes(before + (note + json.dumps(ledger, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    assert target.read_bytes().startswith(before)
    print(json.dumps({'translation':ledger['step1_translation']['greek_translation'],
                      'translation_rows':ledger['step1_translation']['words'],
                      'numeric_matches':[{'hebrew':r['hebrew'], 'value':r['hebrew_total'],
                                          'greek':[x['written'] for x in r['equal_total_greek_candidates']]}
                                         for r in ledger['step2_numeric_comparison']['hebrew_total_to_greek_word_matches']],
                      'phrase_comparison':ledger['phrase_comparison'],
                      'updated':str(target), 'prior_text_preserved':True}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
