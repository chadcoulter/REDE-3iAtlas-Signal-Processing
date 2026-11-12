"""Resume every run005 branch for passes6-10; preserve pass5 inputs and rule."""
import csv
import hashlib
import json
from pathlib import Path
from step03_container_transform_feedback import calculate
from step03_original_atlas_expansion import ROOT, BASE, REGS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    previous=BASE.parent/'run-005-container-transform-feedback/results.json'
    out=BASE.parent/'run-006-container-transform-continuation'
    assert not out.exists(), 'Refusing to overwrite an existing run'
    old=json.loads(previous.read_text(encoding='utf-8'))
    full=calculate(10)
    trials=[]
    key=lambda t: tuple(t[k] for k in ['candidate_id','seed_program_id','mode','orientation'])
    assert len(old['trials'])==len(full['trials'])==24
    for prior,current in zip(old['trials'],full['trials']):
        assert key(prior)==key(current)
        assert current['history'][:5]==prior['history']
        assert current['history'][5]['state_before']==prior['final_state']
        assert current['history'][5]['input_numeric_units']==[prior['final_state'][r] for r in REGS]
        trial={k:v for k,v in current.items() if k!='history'}
        trial['starting_state']=prior['final_state']
        trial['history']=current['history'][5:]
        trial['net_changes']={r:[prior['final_state'][r],current['final_state'][r]] for r in REGS if prior['final_state'][r]!=current['final_state'][r]}
        # Mark exact repetitions only, without inferring a stable boundary.
        states=[tuple(h['state_after'][r] for r in REGS) for h in current['history']]
        trial['repeated_output_states']=[{'earlier_pass':i+1,'later_pass':j+1} for j in range(5,10) for i in range(j) if states[i]==states[j]]
        trials.append(trial)
    result={'trial':'container-transform-feedback-continuation-002','parent_results':previous.relative_to(ROOT).as_posix(),'parent_sha256':digest(previous),'runner_sha256':digest(Path(__file__)),'base_runner_sha256':full['runner_sha256'],'register_order':REGS,'passes':[6,7,8,9,10],'rules':full['rules'],'rule_note':'The earlier five-pass bound is extended to ten total passes without changing the transformation rule. Each continuation begins at the saved pass5 output.','trials':trials,'new_observed_letters':0,'status':'IN-PROGRESS'}
    out.mkdir()
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['container','seed','mode','orientation','pass','input_numeric_units','executed_glyphs']+['before_'+r for r in REGS]+['after_'+r for r in REGS]+['emitted_greek','emitted_hebrew']
    with (out/'register_passes.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for t in trials:
            for h in t['history']:
                row={'container':t['intact_hebrew'],'seed':t['seed_program_id'],'mode':t['mode'],'orientation':t['orientation'],'pass':h['iteration'],'input_numeric_units':json.dumps(h['input_numeric_units']),'executed_glyphs':h['executed_glyphs'],'emitted_greek':json.dumps(h['emitted_greek'],ensure_ascii=False),'emitted_hebrew':json.dumps(h['emitted_hebrew'],ensure_ascii=False)}
                row.update({'before_'+r:h['state_before'][r] for r in REGS});row.update({'after_'+r:h['state_after'][r] for r in REGS});writer.writerow(row)
    count=sum(len(h['operator_trace']) for t in trials for h in t['history'])
    text='''# Container-transform continuation: passes6–10

All24 run005 branches continue under the same output-register feedback rule. No branches are selected or removed for linguistic coherence. Register order: state, relations, constraints, observations, unresolved, context, target, events.

Process: deterministically replay passes1–10 using the unchanged original runner; require exact equality of every pass1–5 record with run005; require each pass6 starting state and numeric inputs to match its saved pass5 output; retain passes6–10 as the continuation. Each operation is checked against the preserved original instruction interpreter. At each pass, encode all eight carried registers; apply the branch's unchanged orientation; execute; record every intermediate vector; emit all eight numeric values and their Greek/Hebrew numeric encodings.

The source numeric units, operator definitions, seeds, three orientations, two input modes, and feedback rule are unchanged. The original candidate subset came from earlier lexical exploration; this continuation performs no word search or sentence construction. Zero values remain in numeric/register data and encode as zero/no operation under the existing rule. All register arithmetic follows the recovered machine's uint64 behavior.

'''
    text+=f'Data: 120 new pass records, {count} new instruction records, 24 exact prefix comparisons. Full before/after states and per-instruction writes are in results.json; all pass outputs are also in register_passes.csv.\n\n'
    for t in trials:
        text+=f"Container {t['intact_hebrew']}; seed {t['seed_program_id']}; {t['mode']}; {t['orientation']}\n"
        text+='Pass5: '+json.dumps([t['starting_state'][r] for r in REGS])+'\n'
        for h in t['history']:
            text+=f"Pass{h['iteration']}: {h['executed_glyphs']}\n"
            text+='Output: '+json.dumps(h['emitted_numeric_units'])+'\n'
            text+='Changes: '+json.dumps(h['changes'],ensure_ascii=False)+'\n'
            text+='Greek units: '+' ‖ '.join(h['emitted_greek'])+'\n'
            text+='Hebrew units: '+' ‖ '.join(h['emitted_hebrew'])+'\n'
        text+='Repeated complete output states: '+json.dumps(t['repeated_output_states'])+'\n\n'
    text+='Five additional passes do not establish convergence. These are computed register outputs; no new observation samples or source letters were inserted. Status: IN-PROGRESS.\n'
    working=BASE/'hebrew_streams_updated.txt';before=working.read_bytes()
    marker='Container-transform continuation: passes6–10'
    assert marker not in before.decode('utf-8')
    working.write_bytes(before+('\n\n'+text).encode('utf-8'));assert working.read_bytes().startswith(before)
    assert working.read_bytes().startswith((BASE/'hebrew_streams.txt').read_bytes())
    text+='\n## Reproduction and file changes\n\nRun `python -X utf8 -B WOWSignal/scripts/step03_container_transform_continuation.py` from the repository root before this run exists. The command refuses to overwrite this directory or duplicate its working-text section.\n\nAdded this runner and run006 results.json, register_passes.csv, README.md, manifest.json. Appended all24 branches to the combined working Hebrew text. Added a byte-preserving .gitattributes rule for the runner. Earlier run005 files are unchanged. No commit or push.\n'
    (out/'README.md').write_text(text,encoding='utf-8')
    attrs=ROOT/'WOWSignal/.gitattributes';b=attrs.read_bytes();rule=b'scripts/step03_container_transform_continuation.py -text'
    if rule not in b:attrs.write_bytes(b.rstrip(b'\r\n')+b'\n'+rule+b'\n')
    paths=[Path(__file__),out/'results.json',out/'register_passes.csv',out/'README.md',working,attrs]
    manifest={'parent_sha256':digest(previous),'prior_working_text_sha256':hashlib.sha256(before).hexdigest(),'prior_working_text_bytes':len(before),'prior_working_text_preserved':True,'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in paths],'prefix_checks':24,'new_passes':120,'new_instruction_checks':count,'commit_or_push':False}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(out),'new_instruction_checks':count,'prefix_checks':24,'trials':[{'container':t['intact_hebrew'],'seed':t['seed_program_id'],'mode':t['mode'],'direction':t['orientation'],'net_changes':t['net_changes'],'repetitions':t['repeated_output_states']} for t in trials]},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
