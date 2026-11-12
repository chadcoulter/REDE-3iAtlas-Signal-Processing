"""Apply the RECOVERED append/prepend extension rule to scoped Wow parts.

Four original temporal parts become four trial lanes, each initially one value.
This is an explicit input adapter, not four recorded Wow frequency channels.
Machine operations are taken from the recovered pinned Atlas assembly.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys

from step03_original_atlas_expansion import ROOT, BASE, SOURCE, REGS, load, sha

MARKER='Recovered growing-chain expansion001 — append target, prepend state and relations'


def run(output,passes):
    assert not output.exists() and passes>0
    _,_,_,compiled,operators=load()
    original=SOURCE/'original_process'
    sys.path.insert(0,str(original))
    from operator_machine import validate
    validation=validate({g:v['assembly'] for g,v in operators.items()})
    # Original numerical encoder, unchanged; no arbitrary dictionary matching.
    from endpoint_phase import encode,numeral_table
    table=numeral_table(ROOT/'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    data=json.loads((BASE/'hebrew_grid.json').read_text(encoding='utf-8'))['grid']
    assert [data[r][1] for r in range(57,61)]==['ו','יד','כו','ל']
    def execute_chain(chain,prior,opposite,direction):
        r=prior.copy();r[:4]=opposite;a=0;z=False;count=0
        values=chain if direction=='x_to_y' else chain[::-1]
        commands=[]
        for value in values:
            glyphs=''.join(ch for ch in encode(value,table) if ch not in ' |0')
            if direction=='y_to_x':glyphs=glyphs[::-1]
            commands.append(glyphs)
            for glyph in glyphs:a,z=compiled[glyph](r,a,z);count+=1
        return r,count,commands
    def trial(initial):
        chains=[[v] for v in initial];orig=copy.deepcopy(chains);programs=[];history=[]
        def execute_all(direction,feedback,step):
            opposite=[c[-1] if direction=='x_to_y' else c[0] for c in chains]
            states=[]
            for i,(chain,prior) in enumerate(zip(chains,feedback)):
                state,count,commands=execute_chain(chain,prior,opposite,direction)
                programs.append({'id':len(programs)+1,'validates_step':step,'direction':direction,
                                 'lane':i+1,'chain_length':len(chain),
                                 'chain_sha256':sha(b''.join(struct.pack('<Q',v) for v in chain)),
                                 'opposite_seed':opposite,'retained_feedback':prior,
                                 'operator_count':count,'output':dict(zip(REGS,state))})
                states.append(state)
            return states
        direction='x_to_y';pending=execute_all(direction,[[1]*8 for _ in range(4)],0)
        for step in range(1,passes*2+1):
            if direction=='x_to_y':
                projected=[state[6] for state in pending]
                for chain,value in zip(chains,projected):chain.append(value)
            else:
                projected=[[state[0],state[1]] for state in pending]
                for chain,pair in zip(chains,projected):chain[:0]=pair
            next_direction='y_to_x' if direction=='x_to_y' else 'x_to_y'
            newstates=execute_all(next_direction,pending,step)
            history.append({'step':step,'cycle':(step+1)//2,'direction':direction,
                            'projected_values':projected,'front':[c[0] for c in chains],
                            'back':[c[-1] for c in chains],'lengths':list(map(len,chains)),
                            'next_direction':next_direction,
                            'next_targets':[s[6] for s in newstates],
                            'output_states':[dict(zip(REGS,s)) for s in newstates]})
            pending=newstates;direction=next_direction
        assert len(programs)==4+8*passes
        for first,chain in zip(orig,chains):
            assert chain[2*passes:2*passes+1]==first and len(chain)==1+3*passes
        return {'initial_values':initial,'history':history,'programs':programs,
                'final_chains':chains,'final_front':[c[0] for c in chains],
                'final_back':[c[-1] for c in chains],
                'chain_lengths':list(map(len,chains)),
                'generated_value_vocabulary':sorted(set(v for c in chains for v in c)),
                'greek_final_chains':[[encode(v,table) for v in c] for c in chains]}
    results={name:trial(values) for name,values in [('wow_parts',[6,14,26,30]),
                                                   ('reversed_parts',[30,26,14,6]),
                                                   ('zero_parts',[0,0,0,0])]}
    output.mkdir(parents=True)
    ledger={'original_implementation':'experiments/endpoint_phase_v1/native_reassemble_every_pass.py',
            'pinned_commit':'c0ad2a1d40db7cc3e3b29b833cdb1dcd0622a86c',
            'runner_sha256':sha(Path(__file__).read_bytes()),
            'original_rule':'execute full chain; X->Y append target; Y->X prepend [state,relations]; execute extended chain immediately in opposite direction; retain eight-register feedback; endpoint vector overwrites first four registers',
            'scope':'Only numeric parts6,14,26,30 from וידכ | ול. Original יטה stays outside this trial.',
            'input_adapter':'Four consecutive temporal numeric parts become four trial lanes; each starts as a one-value chain. They are not four recorded channels.',
            'external_Atlas_payload':'None of the original Atlas measurement chains or feedback bank values seed this growing-chain trial. Original operator bodies and extension wiring are reused.',
            'execution':'Portable execution of original machine bodies. Pinned fixed-circuit native trace matched in preceding trial; randomized original operator validation passes here. No new native ELF binaries compiled because WSL access is unavailable.',
            'operator_validation_cases':validation,'passes_each_direction':passes,
            'normalization':'Original Greek encoder uses Ϛ for6, not Ϝ. All uint64 arithmetic wraps at2^64.',
            'generated_value_status':'Projected computational values, not recovered measurements or independently established message letters.',
            'results':results}
    (output/'results.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    target=BASE/'hebrew_streams_updated.txt';before=target.read_bytes()
    assert MARKER not in before.decode('utf-8')
    intro='\n\n'+'='*60+'\n'+MARKER+'\n\n'
    intro+='The actual original growing-chain rule has now been recovered. It adds computed values to the chain itself and executes the longer chain before the next projection. This differs from the earlier fixed-sequence feedback/paraphrase trial.\n'
    intro+='Only four scoped parts are used as initial data; their assignment to four one-value lanes is an explicit Wow adapter. No Atlas measurement chains or fixed Atlas feedback banks enter this trial.\n'
    intro+='Projection is not proof of recovery: all generated states are labelled computational values. No register-to-natural-language payload rule is supplied by the recovered implementation.\n'
    intro+='All steps, states, original-middle preservation checks and Greek encodings: '+str(output.relative_to(ROOT)).replace('\\','/')+'/results.json\n\n'
    concise={k:v for k,v in ledger.items() if k!='results'}
    concise['results']={k:{kk:vv for kk,vv in v.items() if kk not in ['programs','greek_final_chains']} for k,v in results.items()}
    target.write_bytes(before+(intro+json.dumps(concise,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    assert target.read_bytes().startswith(before) and target.read_bytes().startswith((BASE/'hebrew_streams.txt').read_bytes())
    print(json.dumps({'output':str(output),'validation_cases':validation,
                      'results':{k:{'lengths':v['chain_lengths'],'front':v['final_front'],
                                    'back':v['final_back'],'vocabulary':v['generated_value_vocabulary'],
                                    'first_six_steps':v['history'][:6]}
                                 for k,v in results.items()},'prior_text_preserved':True},ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--passes',type=int,default=100)
    a=p.parse_args();run(a.output.resolve(),a.passes)
