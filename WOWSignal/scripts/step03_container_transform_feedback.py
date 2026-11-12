"""Treat intact candidate containers as machine transforms, then expand state.

New experimental feedback rule: execute a candidate; encode ALL eight output
registers in fixed order; execute that resulting program on the carried state.
This is not claimed to be a recovered decompressor or the original append/
prepend experiment. Default output is read-only; --output NEW_DIR saves once.
"""
import argparse
import json
from pathlib import Path
import sys

from step03_original_atlas_expansion import ROOT,BASE,REGS,load,sha
from step03_hebrew_gematria import TABLE

sys.path.insert(0,str(ROOT/'WOWSignal/sources/3i-atlas-expansion/original_process'))
from endpoint_phase import encode,numeral_table
from operator_machine import execute

MARKER='Container-as-transform experiment001 — intact units and encoded-state feedback'


def hebrew_state(value):
    if value==0:return '0'
    chunks=[]
    while value:
        part,value=value%1000,value//1000;word=''
        for amount,letter in reversed(TABLE):
            if part in (15,16):
                word+='טו' if part==15 else 'טז';part=0;break
            while part>=amount:word+=letter;part-=amount
        chunks.append(word or '0')
    return ' | '.join(chunks[::-1])


def calculate(rounds):
    assert rounds>0
    _,_,_,compiled,operators=load()
    table=numeral_table(ROOT/'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    old=BASE.parent/'run-004-expanded-hebrew-parser/results.json'
    data=json.loads(old.read_text(encoding='utf-8'))
    chainfile=BASE.parent/'run-003-growing-container/results.json'
    chains=json.loads(chainfile.read_text(encoding='utf-8'))['results']['wow_parts']
    candidates=[]
    for lane,word in [(4,'הגה'),(1,'וידא'),(3,'וידא')]:
        view=next(r for r in data['streams'] if r['case']=='wow_parts' and r['lane']==lane and r['direction']=='container_order_reverse')
        hit=next(h for h in view['matches'] if h['word']==word)
        seen=set();parts=[]
        for ref in hit['glyph_occurrences']:
            idx=ref['chain_index_1based']
            if idx not in seen:
                seen.add(idx);parts.append({k:ref.get(k) for k in ['value','token','kind','row','channel','step','cycle','register','projection_program','chain_index_1based']})
        seeds=sorted({r['projection_program'] for r in hit['glyph_occurrences'] if r.get('projection_program')})
        candidates.append({'id':f'lane{lane}_{word}','matched_word':word,
                           'intact_hebrew':''.join(p['token'] for p in parts),
                           'parts':parts,'values':[p['value'] for p in parts],
                           'seed_program_ids':seeds,'original_match':hit})
    assert [c['intact_hebrew'] for c in candidates]==['הגה','וידא','כוידא']
    trials=[]
    for candidate in candidates:
        for seed_id in candidate['seed_program_ids']:
            program=next(p for p in chains['programs'] if p['id']==seed_id)
            for mode in ['intact_parts','whole_container_total']:
                initial=(candidate['values'] if mode=='intact_parts' else [sum(candidate['values'])])
                for direction in ['forward','container_reverse','full_glyph_reverse']:
                    state=[program['output'][reg] for reg in REGS];values=initial.copy();history=[]
                    for iteration in range(1,rounds+1):
                        blocks=[encode(v,table) for v in values]
                        ordered=blocks if direction=='forward' else blocks[::-1]
                        glyphs=''.join(ch for block in ordered for ch in block if ch not in ' |0')
                        if direction=='full_glyph_reverse':
                            glyphs=''.join(ch for block in blocks for ch in block if ch not in ' |0')[::-1]
                        before=state.copy();a=0;z=False;trace=[]
                        for index,glyph in enumerate(glyphs,1):
                            prior=state.copy();a,z=compiled[glyph](state,a,z)
                            expected=dict(zip(REGS,prior));execute(operators[glyph]['assembly'],expected)
                            assert state==[expected[k] for k in REGS]
                            trace.append({'index':index,'glyph':glyph,'before':prior,'after':state.copy(),
                                          'changed_registers':[reg for reg,x,y in zip(REGS,prior,state) if x!=y]})
                        history.append({'iteration':iteration,'input_numeric_units':values.copy(),
                                        'greek_blocks':blocks,'executed_glyphs':glyphs,
                                        'state_before':dict(zip(REGS,before)),
                                        'state_after':dict(zip(REGS,state)),
                                        'changes':{reg:[x,y] for reg,x,y in zip(REGS,before,state) if x!=y},
                                        'emitted_numeric_units':state.copy(),
                                        'emitted_greek':[encode(v,table) for v in state],
                                        'emitted_hebrew':[hebrew_state(v) for v in state],
                                        'operator_trace':trace})
                        # This explicitly chosen projection, not a hidden default,
                        # supplies the next program and carries the same state.
                        values=state.copy()
                    trials.append({'candidate_id':candidate['id'],'intact_hebrew':candidate['intact_hebrew'],
                                   'seed_program_id':seed_id,'mode':mode,'orientation':direction,
                                   'history':history,'final_state':dict(zip(REGS,state))})
    assert len(trials)==24
    return {'trial':'container-transform-feedback-001','source_parser_sha256':sha(old.read_bytes()),
            'source_growth_sha256':sha(chainfile.read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),
            'register_order':REGS,'candidates':candidates,'trials':trials,
            'rules':[
                'Candidate lexical spans are treated as possible code, not assumed instructions selected by the signal.',
                'Restore intact numeric source tokens; lane3 retains כ in כוידא and value26 rather than extracting only its ו.',
                'Compare original numeric parts and their whole-container sum. Equal sums do not mean equal machine programs.',
                'Seed from actual generating-program output states; no arbitrary new register seed.',
                'After executing each program, encode all eight output registers in fixed REGS order as the next program; carry the output state.',
                'Compare forward, reversed numeric-container order, and full glyph reversal in each iteration.',
                'Five iterations per branch are a bounded trial, not convergence, EOF, missing-data validation or semantic closure.',
                'The output-register re-encoding rule is newly chosen for this experiment; the preceding recovered run003 append/prepend rule remains unchanged.',
                'Hebrew output is an additive base1000 display extension, with15/16 exceptions; it is not new physical source text.',
            ],'iterations':rounds,'new_observed_letters':0,'status':'IN-PROGRESS'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--rounds',type=int,default=5)
    args=p.parse_args()
    if args.output:assert not args.output.exists()
    ledger=calculate(args.rounds)
    if not args.output:
        print(json.dumps(ledger,ensure_ascii=False,indent=2));return
    working=BASE/'hebrew_streams_updated.txt';before=working.read_bytes()
    assert MARKER not in before.decode('utf-8') and before.startswith((BASE/'hebrew_streams.txt').read_bytes())
    args.output.mkdir(parents=True)
    (args.output/'results.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    selected=[t for t in ledger['trials'] if t['orientation']=='forward']
    section='\n\n'+'='*60+'\n'+MARKER+'\n\n'
    section+='User asks to treat the container as transform information and follow its expansion. This pass executes candidate code against its recorded generating context, then explicitly re-encodes all output registers for the next iteration. It does not change the earlier original append/prepend procedure or claim a recovered decompressor.\n'
    section+='Intact units: הגה = [5,3,5]; וידא in lane1 = [6,14,1]; lane3 restores כוידא = [26,14,1]. Full-container totals13,21,41 are compared separately. No leading כ is dropped.\n'
    section+='Original compiler:6 usesϚ. Initial per-unit programs ΕΓΕ, ϚΙΔΑ, ΚϚΙΔΑ; whole-container programs ΙΓ, ΚΑ, ΜΑ. Meanings inferred from dictionaries are not presumed machine behavior.\n'
    section+='All24 branches, original operator comparisons, register changes and emitted code are in '+str(args.output).replace('\\','/')+'/results.json\n\n'
    for trial in selected:
        section+=f"Candidate {trial['intact_hebrew']}; seed program {trial['seed_program_id']}; mode {trial['mode']}\n"
        for row in trial['history']:
            section+=f"Iteration {row['iteration']}: {row['executed_glyphs']}\n"
            section+='Changes: '+json.dumps(row['changes'],ensure_ascii=False)+'\n'
            section+='Emitted Hebrew register sequence (fixed register order, not a sentence): '+' ‖ '.join(row['emitted_hebrew'])+'\n'
            section+='Emitted Greek register sequence: '+' ‖ '.join(row['emitted_greek'])+'\n'
        section+='\n'
    section+='All source streams and surrounding יטה remain unchanged. These are computed transform expansions, not recovered source letters or a validated message.\n'
    working.write_bytes(before+section.encode('utf-8'));assert working.read_bytes().startswith(before)
    print(json.dumps({'output':str(args.output),'branches':len(ledger['trials']),
                      'summary':[{'container':t['intact_hebrew'],'seed':t['seed_program_id'],'mode':t['mode'],
                                  'program_lengths':[len(x['executed_glyphs']) for x in t['history']],
                                  'first_changes':t['history'][0]['changes'],'final_state':t['final_state']}
                                 for t in selected],'prior_text_preserved':True},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
