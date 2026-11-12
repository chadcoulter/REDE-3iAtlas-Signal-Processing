"""Parse generated Hebrew candidates with exact occurrence/boundary traces.

Finite dictionary matching is explicit; this is not a full Hebrew grammar or
an automatic decoder. The TAO scaffold records the calculated relationships
and supplied semantic alternatives, without validating message intent.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'WOWSignal/steps/03-hebrew-gematria'
sys.path.insert(0,str(ROOT/'WOWSignal/scripts'))
sys.path.insert(0,str(ROOT/'WOWSignal/sources'))
from step03_hebrew_gematria import hebrew
from tao_parser import InformationItem,InformationState as S,Theatre,Act,Operation,TAOResolver

MARKER='Expanded Hebrew relational parse001 — container boundaries and הגה alternatives'
LEXICON={
    'כדיו':{'readings':['his/its jars or vessels; containers as a broader rendering'], 'source':'https://www.pealim.com/dict/7880-kad/'},
    'הטי':{'readings':['tilt! feminine singular imperative'], 'source':'https://www.pealim.com/dict/1193-lehatot/'},
    'יטה':{'readings':['he/it will tilt or incline'], 'source':'https://www.pealim.com/dict/1193-lehatot/'},
    'ביטא':{'readings':['he/it expressed or pronounced'], 'source':'https://www.pealim.com/dict/209-levate/'},
    'היטב':{'readings':['well; properly'], 'source':'https://www.pealim.com/dict/7798-hetev/'},
    'וידא':{'readings':['he/it verified or made sure'], 'source':'https://www.pealim.com/he/dict/479-levade/'},
    'גל':{'readings':['wave; heap; shaft'], 'source':'https://www.pealim.com/dict/2653-gal/'},
    'יד':{'readings':['hand'], 'source':'https://www.sefaria.org/Klein_Dictionary%2C_%D7%99%D6%B8%D7%93'},
    'ידו':{'readings':['his/its hand'], 'source':'https://freely-given.org/OBD/ref/HebWrd/EXOc4v6w14.htm'},
    'אב':{'readings':['father'], 'source':'https://www.pealim.com/dict/4845-aba/'},
    'אבא':{'readings':['father; dad'], 'source':'https://www.pealim.com/dict/4845-aba/'},
    'גג':{'readings':['roof; top; maximum'], 'source':'https://www.pealim.com/dict/7066-gag/'},
    'הגה':{'readings':['steering wheel; rudder; control (noun)',
                       'speech sound; utterance (noun)',
                       'he uttered/pondered (alternative verbal vocalization)'],
           'source':'https://www.pealim.com/dict/7234-hege/',
           'other_source':'https://milononline.net/מקרא/הגה'},
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rebuild(case,result,lane):
    value=result['initial_values'][lane]
    source_row={6:58,14:59,26:60,30:61}.get(value) if case!='zero_parts' else None
    entries=[{'value':value,'kind':'original_part' if source_row else 'control_input',
              'row':source_row,'channel':2 if source_row else None,
              'step':None,'cycle':None,'register':None}]
    for event in result['history']:
        step=event['step'];projection=event['projected_values'][lane]
        def item(v,register):
            program=result['programs'][(step-1)*4+lane]
            assert program['output'][register]==v
            return {'value':v,'kind':'generated','row':None,'channel':None,
                    'step':step,'cycle':event['cycle'],'register':register,
                    'projection_program':program['id']}
        if event['direction']=='x_to_y':
            entries.append(item(projection,'target'))
        else:
            entries[:0]=[item(projection[0],'state'),item(projection[1],'relations')]
    assert [x['value'] for x in entries]==result['final_chains'][lane]
    for i,x in enumerate(entries,1):
        x.update(case=case,lane=lane+1,chain_index_1based=i,token=hebrew(x['value']))
    return entries


def scan(case,lane,entries,direction):
    glyphs=[]
    for entry in entries:
        glyphs += [{**entry,'glyph_index_in_token':i,'character':ch}
                   for i,ch in enumerate(entry['token'])]
    if direction=='full_glyph_reverse':
        glyphs=glyphs[::-1]
    elif direction=='container_order_reverse':
        glyphs=[{**entry,'glyph_index_in_token':i,'character':ch}
                for entry in entries[::-1] for i,ch in enumerate(entry['token'])]
    text=''.join(x['character'] for x in glyphs);matches=[];covered=set()
    for word,definition in LEXICON.items():
        for i in range(len(text)-len(word)+1):
            if not text.startswith(word,i):
                continue
            refs=glyphs[i:i+len(word)];indices={x['chain_index_1based'] for x in refs}
            steps={x['step'] for x in refs}
            within_pair=(all(x['kind']=='generated' and x['register'] in ['state','relations'] for x in refs)
                         and len(steps)==1 and len(indices)==2)
            same_token=len(indices)==1
            matches.append({'word':word,'readings':definition['readings'],
                            'display_start_1based':i+1,'display_end_1based':i+len(word),
                            'chain_indices_1based':sorted(indices),
                            'inside_one_numeric_token':same_token,
                            'inside_one_generated_state_relations_pair':within_pair,
                            'crosses_pair_or_token_boundary':not(same_token or within_pair),
                            'origin_kinds':sorted({x['kind'] for x in refs}),
                            'palindrome':word==word[::-1],
                            'glyph_occurrences':refs})
            covered.update(range(i,i+len(word)))
    gaps=[];i=0
    while i<len(text):
        if i in covered:
            i+=1;continue
        start=i
        while i<len(text) and i not in covered:i+=1
        gaps.append({'start_1based':start+1,'end_1based':i,'text':text[start:i]})
    return {'case':case,'lane':lane+1,'direction':direction,'exact_text':text,
            'numeric_token_count':len(entries),'glyph_count':len(glyphs),
            'matches':matches,'unmatched_ranges':gaps,
            'scope':'All overlapping exact matches within this finite13-entry candidate lexicon; no insertions, spelling normalization, lane joining, or grammar acceptance.'}


def run(output):
    assert not output.exists()
    input_path=BASE/'run-003-growing-container/results.json'
    input_bytes=input_path.read_bytes();data=json.loads(input_bytes)
    records=[];obs=[]
    for case,result in data['results'].items():
        for lane in range(4):
            entries=rebuild(case,result,lane)
            obs.extend(InformationItem(f'{case}:lane{lane+1}:token{i+1}',x,
                                      S.OBSERVATION,'Recorded computational projection in run003, not a new physical measurement')
                       for i,x in enumerate(entries))
            for direction in ['source_order','full_glyph_reverse','container_order_reverse']:
                records.append(scan(case,lane,entries,direction))
    primary=[x for x in records if x['case']=='wow_parts']
    counts=[]
    for x in records:
        summary={}
        for word in LEXICON:
            hits=[h for h in x['matches'] if h['word']==word]
            if hits:summary[word]={'count':len(hits),'inside_pair':sum(h['inside_one_generated_state_relations_pair'] for h in hits),
                                  'inside_token':sum(h['inside_one_numeric_token'] for h in hits),
                                  'cross_boundary':sum(h['crosses_pair_or_token_boundary'] for h in hits)}
        counts.append({'case':x['case'],'lane':x['lane'],'direction':x['direction'],'counts':summary})
    relationships=[
        {'relation':'container/orientation/control','participants':['earlier כדיו container candidate','earlier הטי tilt candidate','generated הגה steering/control candidate'],
         'candidate_reading':'Orient the containers using a steering/control mechanism.',
         'status':'analyst relational synthesis, not a contiguous source sentence; using and mechanism are supplied relations'},
        {'relation':'expression/speech/checking','participants':['earlier ביטא expression candidate','generated הגה speech/utterance candidate','earlier וידא verification candidate'],
         'candidate_reading':'An expression or utterance is made and checked.',
         'status':'alternative analyst synthesis; source does not select speech rather than steering'},
        {'relation':'boundary/roof','participants':['generated גג roof/top candidate','container boundary hypothesis'],
         'candidate_reading':'A top or roof can act as a boundary of a containing structure.',
         'status':'functional hypothesis; no lid or roof term recovered from observed signal'},
        {'relation':'actor/hand/control','participants':['generated אבא father candidate','mixed generated/original ידו his hand candidate','generated הגה steering candidate'],
         'candidate_reading':'A hand could operate a control.',
         'status':'inferred functional edge; father identity and cross-lane composition are not established'},
    ]
    facts=InformationItem('exact_candidate_matches',counts,S.INFERENCE,'Exact finite-lexicon scan with original numeric token and generated pair attribution')
    hyp=InformationItem('container_orientation_and_expression_alternatives',relationships,S.HYPOTHESIS,'Supplied lexical interpretations; bridge terms and cross-lane relationships explicitly marked')
    question=InformationItem('unresolved_message','No complete grammatical sentence, source-selected sense, lane-composition rule, or independent payload extraction rule is established.',S.QUESTION,'Unmatched ranges and repeated projected pairs remain active')
    res=TAOResolver().resolve(Theatre('Recorded expanded chains for scoped וידכ | ול; outside יטה unchanged',tuple(obs),
                                     ('Preserve generated/original distinction','No letter edits or unmarked cross-lane joining')),
                              Act('Follow candidate Hebrew relationships','Rebuild provenance, parse exact candidates, compare orientation and retained boundaries'),
                              (Operation('rebuild_and_trace_generated_tokens',tuple(obs),(facts,),'All3612 numeric trial tokens retain provenance'),
                               Operation('compose_and_compare_relationships',(facts,),(hyp,question),'Semantic alternatives supplied and left open')))
    assert len(records)==36 and len(obs)==3612 and not res.enough
    ledger={'source':str(input_path.relative_to(ROOT)),'source_sha256':sha(input_bytes),
            'runner_sha256':sha(Path(__file__).read_bytes()),'lexicon':LEXICON,
            'method':'Reconstruct original/generation provenance; exact finite-lexicon matches; three orientation choices; respect and report token/pair boundaries; retain all gaps.',
            'case_counts':counts,'candidate_relationships':relationships,'streams':records,
            'parser':{'name':'V8 TAO record scaffold plus explicit finite lexical scanner',
                      'trace':list(res.trace),'record_backward_status':res.backward_validation.status.value,
                      'enough':res.enough,'unresolved':[x.label for x in res.unresolved_remainder],
                      'validation_limit':'The scaffold does not perform Hebrew semantics or certify that a generated word is an intended signal message.'},
            'new_source_letters':0,'status':'IN-PROGRESS'}
    output.mkdir(parents=True)
    (output/'results.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    target=BASE/'run-001/hebrew_streams_updated.txt';before=target.read_bytes()
    assert MARKER not in before.decode('utf-8') and before.startswith((BASE/'run-001/hebrew_streams.txt').read_bytes())
    section='\n\n'+'='*60+'\n'+MARKER+'\n\n'
    section+='Parser input is the actual run003 expanded Hebrew chains, with every value traced to its original source cell or generating program/extension step. No new upstream data or letter-name expansion is introduced.\n'
    section+='New candidate הגה appears96 times in primary lane4 in each reading orientation. It crosses adjacent generated state/relations pair boundaries; these repeated overlapping hits are not independent messages. Steering/control and speech/utterance remain distinct sense alternatives.\n'
    section+='גג is a roof/top candidate in lane2, with196 overlapping matches per direction, of which98 align with a generated [state,relations] pair. It is not a source-observed roof instruction.\n'
    section+='אבא appears once in primary lanes1 and3 in each direction; ידו occurs once in primary lane1 in source order, mixing generated יד with the retained original ו. This does not establish a father, speaker, or actor identity.\n'
    section+='הגה, גג and אבא are palindromes, so full reversal cannot select their meaning or establish the source direction. Original token boundaries and known source time order remain separate evidence.\n'
    section+='Container/orientation working synthesis: Orient the containers using a steering/control mechanism. This is a proposed semantic connection among earlier and generated candidates, not a recovered sentence or a ship/spacecraft interpretation of כד.\n'
    section+='Competing synthesis: expression/utterance and verification. הגה can support speech, so the steering interpretation is not uniquely forced. All unmatched surrounding letters and directions are retained below and in the full ledger.\n'
    section+='No complete grammatical message recovered. Parser record validation is provenance bookkeeping, not linguistic truth.\n'
    section+='Complete occurrence and gap ledger: '+str(output.relative_to(ROOT)).replace('\\','/')+'/results.json\n\n'
    section+=json.dumps({'counts':counts,'relationships':relationships,'parser':ledger['parser']},ensure_ascii=False,indent=2)+'\n'
    section+='Representative primary occurrences (all other occurrences remain in the ledger):\n'
    for word in ['הגה','גג','אבא','ידו']:
        for row in primary:
            if row['direction']!='source_order':continue
            hits=[x for x in row['matches'] if x['word']==word]
            if hits:
                section+=json.dumps({'lane':row['lane'],'word':word,'count':len(hits),'first':hits[0],'last':hits[-1]},ensure_ascii=False)+'\n'
    target.write_bytes(before+section.encode('utf-8'));assert target.read_bytes().startswith(before)
    print(json.dumps({'output':str(output),'numeric_tokens_traced':len(obs),'orientation_streams':len(records),
                      'primary_counts':[x for x in counts if x['case']=='wow_parts'],
                      'parser':ledger['parser'],'prior_text_preserved':True},ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();run(a.output.resolve())
