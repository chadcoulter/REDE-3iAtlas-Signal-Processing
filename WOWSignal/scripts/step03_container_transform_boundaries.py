"""Extend all24 container-feedback branches to100 passes and audit boundaries."""
import csv
import hashlib
import json
from pathlib import Path
from step03_container_transform_feedback import calculate
from step03_original_atlas_expansion import ROOT, BASE, REGS


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=BASE.parent/'run-007-container-transform-boundaries'
    assert not out.exists()
    p5=BASE.parent/'run-005-container-transform-feedback/results.json'
    p10=BASE.parent/'run-006-container-transform-continuation/results.json'
    old5=json.loads(p5.read_text(encoding='utf-8'));old10=json.loads(p10.read_text(encoding='utf-8'))
    full=calculate(100);trials=[]
    for old,a,b in zip(old5['trials'],old10['trials'],full['trials']):
        assert b['history'][:5]==old['history'] and b['history'][5:10]==a['history']
        assert b['history'][10]['state_before']==a['final_state']
        seen={};repeats=[]
        for h in b['history']:
            key=tuple(h['emitted_numeric_units'])
            if key in seen: repeats.append({'first_pass':seen[key],'repeat_pass':h['iteration'],'period':h['iteration']-seen[key]})
            else:seen[key]=h['iteration']
        record={k:v for k,v in b.items() if k!='history'}
        record.update(starting_state=a['final_state'],history=b['history'][10:],first_repeat=repeats[0] if repeats else None,distinct_output_states=len(seen),unchanged_passes=[h['iteration'] for h in b['history'] if h['state_before']==h['state_after']],pass100_program=b['history'][-1]['executed_glyphs'])
        trials.append(record)
    count=sum(len(h['operator_trace']) for t in trials for h in t['history'])
    coverage={'original_grid_rows':82,'original_grid_channels':50,'original_grid_cells':4100,'initial_experiment_numeric_scope':[6,14,26,30],'initial_scope_source_coordinates':[{'row':r,'channel':2} for r in range(58,62)],'excluded_adjacent_core_units':[19,5],'continuation_inputs':'Three selected generated-container candidates from run004, with generating contexts retained. These are not an exhaustive traversal of all4100 source cells.','initial_start':'Candidate inputs and generating-program states explicitly selected in the prior experiment.','termination_rule':'No source-defined start marker, end marker, or halt opcode is specified in this feedback experiment. The100-pass limit is an investigator-set observation window.','repeat_meaning':'A repeated eight-register output, re-encoded with the same branch orientation, repeats the next program and input state under this deterministic rule. This is an execution cycle, not an observed source EOF.'}
    data={'trial':'container-transform-boundaries-003','parent_sha256':sha(p10),'pass5_sha256':sha(p5),'runner_sha256':sha(Path(__file__)),'base_runner_sha256':full['runner_sha256'],'register_order':REGS,'new_passes':[11,100],'rules':full['rules'],'rule_note':'Extend the observation window to100 total passes; transformation and feedback rules are unchanged.','source_coverage_and_boundaries':coverage,'trials':trials,'new_observed_letters':0,'status':'IN-PROGRESS'}
    out.mkdir();(out/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['container','seed','mode','orientation','pass','input_numeric_units','program']+REGS+['greek_units','hebrew_units','changes']
    with (out/'register_passes.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for t in trials:
            for h in t['history']:
                row={'container':t['intact_hebrew'],'seed':t['seed_program_id'],'mode':t['mode'],'orientation':t['orientation'],'pass':h['iteration'],'input_numeric_units':json.dumps(h['input_numeric_units']),'program':h['executed_glyphs'],'greek_units':json.dumps(h['emitted_greek'],ensure_ascii=False),'hebrew_units':json.dumps(h['emitted_hebrew'],ensure_ascii=False),'changes':json.dumps(h['changes'],ensure_ascii=False)}
                row.update(h['state_after']);w.writerow(row)
    text='# Container-transform boundary tracking: passes11–100\n\n'
    text+='Process: replay the unchanged feedback runner to100 passes; assert all saved pass1–10 records match exactly; retain every pass11–100 instruction, input, output, register write, and numeric Greek/Hebrew rendering. Compare complete eight-register outputs for exact repetition, retaining the first occurrence. All24 branches remain present. Arithmetic and original-operator cross-checks are unchanged. No linguistic filtering or sentence construction occurs.\n\n'
    text+='Coverage and boundary audit:\n'+json.dumps(coverage,ensure_ascii=False,indent=2)+'\n\n'
    text+=f'Data:2160 additional pass records; {count} additional instruction comparisons. Registers in fixed order: '+', '.join(REGS)+'.\n\n'
    for t in trials:
        text+=f"{t['intact_hebrew']} seed{t['seed_program_id']} {t['mode']} {t['orientation']}: first repeat={t['first_repeat']}; distinct outputs={t['distinct_output_states']}; pass100={list(t['final_state'].values())}\n"
    text+='\nAll numeric outputs and exact programs follow. Format: pass / executed program / numeric output / Hebrew numeric units. Boundaries between registers are retained; zero is retained.\n\n'
    for t in trials:
        text+=f"Container {t['intact_hebrew']}; seed{t['seed_program_id']}; {t['mode']}; {t['orientation']}\n"
        for h in t['history']:text+=f"{h['iteration']} / {h['executed_glyphs']} / {h['emitted_numeric_units']} / "+' ‖ '.join(h['emitted_hebrew'])+'\n'
        text+='\n'
    text+='Reproduce before this run exists: python -X utf8 -B WOWSignal/scripts/step03_container_transform_boundaries.py\nThe runner refuses an existing output directory.\n\nAdded runner, run007 results.json, register_passes.csv, README.md, manifest.json; appended all new outputs and process to the combined working Hebrew text; added the runner byte-preserving rule to .gitattributes. Earlier run results are unchanged. No commit or push.\n'
    (out/'README.md').write_text(text,encoding='utf-8')
    working=BASE/'hebrew_streams_updated.txt';before=working.read_bytes();assert 'Container-transform boundary tracking: passes11–100' not in before.decode('utf-8')
    working.write_bytes(before+('\n\n'+text).encode('utf-8'));assert working.read_bytes().startswith(before)
    attrs=ROOT/'WOWSignal/.gitattributes';b=attrs.read_bytes();rule=b'scripts/step03_container_transform_boundaries.py -text'
    if rule not in b:attrs.write_bytes(b.rstrip(b'\r\n')+b'\n'+rule+b'\n')
    paths=[Path(__file__),out/'results.json',out/'register_passes.csv',out/'README.md',working,attrs]
    manifest={'parent_sha256':sha(p10),'prior_working_bytes':len(before),'prior_working_sha256':hashlib.sha256(before).hexdigest(),'prefix_checks':24,'new_pass_records':2160,'new_instruction_checks':count,'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths],'commit_or_push':False}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'new_passes':2160,'instruction_checks':count,'repeating_branches':sum(t['first_repeat'] is not None for t in trials),'branches':[{'container':t['intact_hebrew'],'seed':t['seed_program_id'],'mode':t['mode'],'direction':t['orientation'],'first_repeat':t['first_repeat'],'distinct':t['distinct_output_states'],'pass100':list(t['final_state'].values())} for t in trials]},ensure_ascii=False))


if __name__=='__main__':main()
