"""Full82x50 source traversal; record feedback transforms and boundary data."""
import csv,gzip,hashlib,json,time
from collections import Counter
from pathlib import Path
from step03_original_atlas_expansion import ROOT,BASE,REGS,load
from step03_container_transform_feedback import hebrew_state
from step03_hebrew_gematria import hebrew
from endpoint_phase import encode,numeral_table
from operator_machine import execute


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    out=BASE.parent/'run-008-whole-signal-container-transforms';assert not out.exists()
    src=ROOT/'WOWSignal/steps/01-source-data/run-001'
    grid=json.loads((src/'numeric_grid.json').read_text(encoding='utf-8'))['grid']
    raw=json.loads((src/'raw_grid.json').read_text(encoding='utf-8'))['grid']
    assert len(grid)==82 and all(len(r)==50 for r in grid)
    source_manifest=json.loads((src/'manifest.json').read_text(encoding='utf-8'))
    expected={r['filename']:r['sha256'] for r in source_manifest['artifacts']}
    for name in ['numeric_grid.json','raw_grid.json','cells.csv','row_metadata.csv']:assert sha(src/name)==expected[name]
    _,_,_,compiled,operators=load()
    table=numeral_table(ROOT/'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    paths=[]
    for c in range(50):paths.append({'id':f'channel_{c+1:02}','axis':'vertical','coordinates':[(r,c) for r in range(82)]})
    for r in range(82):paths.append({'id':f'row_{r+1:02}','axis':'horizontal','coordinates':[(r,c) for c in range(50)]})
    for axis in ['vertical','horizontal']:
        cells=[xy for p in paths if p['axis']==axis for xy in p['coordinates']]
        assert len(cells)==len(set(cells))==4100
    out.mkdir();boundaries=[]
    with (out/'source_cells.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['row','channel','raw_character','numeric_bin','hebrew_unit','greek_unit'])
        for r in range(82):
            for c in range(50):w.writerow([r+1,c+1,raw[r][c],grid[r][c],hebrew(grid[r][c]),encode(grid[r][c],table)])
    for p in paths:
        values=[grid[r][c] for r,c in p['coordinates']];p['values']=values
        blocks=[];start=None
        for i,v in enumerate(values+[0]):
            if v and start is None:start=i
            if not v and start is not None:
                blocks.append({'start_position':start+1,'end_position':i,'start_coordinate':[v+1 for v in p['coordinates'][start]],'end_coordinate':[v+1 for v in p['coordinates'][i-1]],'values':values[start:i]});start=None
        boundaries.append({'path':p['id'],'axis':p['axis'],'source_units':len(values),'zero_units':values.count(0),'first_coordinate':[v+1 for v in p['coordinates'][0]],'last_coordinate':[v+1 for v in p['coordinates'][-1]],'first_nonzero':next((i+1 for i,v in enumerate(values) if v),None),'last_nonzero':next((len(values)-i for i,v in enumerate(values[::-1]) if v),None),'nonzero_runs':blocks,'meaning':'Nonzero runs in the preserved printout intensity bins; zero/blank is not a recovered EOF marker.'})
    dump(out/'source_boundaries.json',boundaries)
    dump(out/'process.json',{'source_files':[{'path':(src/n).relative_to(ROOT).as_posix(),'sha256':sha(src/n)} for n in ['numeric_grid.json','raw_grid.json','cells.csv','row_metadata.csv']],'register_order':REGS,'seed':[1]*8,'seed_policy':'New full-source adapter: original all-ones bootstrap; no external Atlas measurements or selected-container generating states.','path_policy':'50 complete vertical channels and82 complete horizontal rows. Each cell is covered once per axis in the intact-parts branch input.','modes':['intact_parts','whole_container_total'],'orientations':['forward','container_reverse','full_glyph_reverse'],'passes':100,'feedback':'Pass1 encodes the complete source path (or its sum). Every following pass encodes all8 previous output registers in fixed REGS order and carries that same state. This is the same experimental register-feedback rule as runs005–007, not a claimed source-authored decompressor.','orientation':'Forward executes encoded units as listed. Container reverse reverses unit order and preserves each encoded unit. Full glyph reverse reverses all executable Greek glyphs. Numeric zeros and positional provenance remain recorded;0 and numeric grouping separators emit no operations.','operation_checks':'Every executed recovered operator is checked against the preserved original interpreter from its preceding register vector.','repeat_policy':'Detect repeated complete output state; future state/program repeat under this deterministic rule. Run every branch to100 without pruning; repetition is not halt or source EOF.','boundary_policy':'Record source page/path endpoints, all nonzero run transitions, and execution repeats separately. No linguistic or target-value heuristic declares a message start/end.','source_limit':'This is the entire preserved82x50 printout grid, not a raw voltage waveform or observations outside that page.','ledger_schema':'JSONL.gz contains branch, pass, input units, encoded blocks, exact program, initial/final states, Greek/Hebrew output, and instruction triples[index,glyph,before8,after8]. Source pass input unit i references the coordinate mapping in path_definitions.json.','status':'IN-PROGRESS'})
    dump(out/'path_definitions.json',[{'id':p['id'],'axis':p['axis'],'coordinates_1based':[[r+1,c+1] for r,c in p['coordinates']],'values':p['values']} for p in paths])
    summaries=[];total_ops=0;starttime=time.monotonic()
    fields=['branch','path','axis','mode','orientation','pass','program']+REGS+['greek_units','hebrew_units','changed_registers']
    textpath=out/'hebrew_register_streams.txt'
    with gzip.open(out/'instruction_trace.jsonl.gz','wt',encoding='utf-8',compresslevel=5) as ledger,(out/'register_passes.csv').open('w',encoding='utf-8',newline='') as csvfile,textpath.open('w',encoding='utf-8') as text:
        writer=csv.DictWriter(csvfile,fieldnames=fields);writer.writeheader()
        text.write('Whole preserved source grid: computed Hebrew numeric register outputs;8 register units per line, not sentences. Order: '+', '.join(REGS)+'\n')
        for path_index,p in enumerate(paths):
            for mode in ['intact_parts','whole_container_total']:
                for direction in ['forward','container_reverse','full_glyph_reverse']:
                    branch=p['id']+'__'+mode+'__'+direction
                    state=[1]*8;values=p['values'].copy() if mode=='intact_parts' else [sum(p['values'])]
                    seen={};repeat=None;nonchanging=[];ops_count=0;first_state=None
                    text.write('\n'+branch+'\n')
                    for iteration in range(1,101):
                        blocks=[encode(v,table) for v in values]
                        seq=''.join(g for b in (blocks if direction=='forward' else blocks[::-1]) for g in b if g not in ' |0')
                        if direction=='full_glyph_reverse':seq=''.join(g for b in blocks for g in b if g not in ' |0')[::-1]
                        before=state.copy();a=0;z=False;trace=[]
                        for index,g in enumerate(seq,1):
                            prior=state.copy();a,z=compiled[g](state,a,z)
                            expected=dict(zip(REGS,prior));execute(operators[g]['assembly'],expected)
                            assert state==[expected[r] for r in REGS]
                            trace.append([index,g,prior,state.copy()])
                        ops_count+=len(trace)
                        greek=[encode(v,table) for v in state];hebr=[hebrew_state(v) for v in state]
                        record={'branch':branch,'pass':iteration,'input_numeric_units':values.copy(),'greek_blocks':blocks,'program':seq,'before':before,'after':state.copy(),'emitted_greek':greek,'emitted_hebrew':hebr,'instructions':trace}
                        ledger.write(json.dumps(record,ensure_ascii=False,separators=(',',':'))+'\n')
                        changes=[r for r,x,y in zip(REGS,before,state) if x!=y]
                        row={'branch':branch,'path':p['id'],'axis':p['axis'],'mode':mode,'orientation':direction,'pass':iteration,'program':seq,'greek_units':json.dumps(greek,ensure_ascii=False),'hebrew_units':json.dumps(hebr,ensure_ascii=False),'changed_registers':','.join(changes)}
                        row.update(dict(zip(REGS,state)));writer.writerow(row)
                        text.write(str(iteration)+' / '+' ‖ '.join(hebr)+'\n')
                        key=tuple(state)
                        if key in seen and repeat is None:repeat={'first_pass':seen[key],'repeat_pass':iteration,'period':iteration-seen[key]}
                        seen.setdefault(key,iteration)
                        if state==before:nonchanging.append(iteration)
                        if iteration==1:first_state=state.copy()
                        values=state.copy()
                    total_ops+=ops_count
                    summaries.append({'branch':branch,'path':p['id'],'axis':p['axis'],'mode':mode,'orientation':direction,'source_units':len(p['values']),'source_sum':sum(p['values']),'pass1_state':first_state,'pass100_state':state.copy(),'first_repeat':repeat,'unchanged_passes':nonchanging,'distinct_outputs':len(seen),'instruction_checks':ops_count})
            if (path_index+1)%20==0:print(f'Paths complete: {path_index+1}/132',flush=True)
    assert len(summaries)==792
    dump(out/'branch_summary.json',summaries)
    aggregates={'paths':132,'vertical_paths':50,'horizontal_paths':82,'branches':792,'passes':79200,'instruction_checks':total_ops,'source_cells':4100,'source_zero_bins':sum(v==0 for row in grid for v in row),'source_nonzero_bins':sum(v!=0 for row in grid for v in row),'branches_with_repeats':sum(t['first_repeat'] is not None for t in summaries),'repeat_period_counts':dict(Counter(t['first_repeat']['period'] for t in summaries if t['first_repeat'])),'first_repeat_pass_counts':dict(Counter(t['first_repeat']['repeat_pass'] for t in summaries if t['first_repeat'])),'source_start_marker_identified':False,'source_end_marker_identified':False,'elapsed_seconds':round(time.monotonic()-starttime,3)}
    dump(out/'summary.json',aggregates)
    report='# Whole-signal container transforms: complete preserved82x50 grid\n\n'+json.dumps(aggregates,ensure_ascii=False,indent=2)+'\n\n'
    report+='All4100 source cells are present in source_cells.csv. path_definitions.json maps every pass1 unit to its original coordinate. Fifty vertical and82 horizontal paths cover the grid in both axes. Intact input parts and whole-path sums are recorded as separate experiments; sums discard cell distinctions and are not the primary source representation. All-ones register initialization is an explicit new input adapter. The prior all-register-output feedback rule is unchanged. Every branch runs100 passes without output selection. Complete provenance, definitions, zero handling, and traversal details are in process.json.\n\n'
    report+='source_boundaries.json records source edges and every contiguous nonzero run. The compressed instruction ledger stores all79200 pass records and every instruction before/after vector. register_passes.csv retains every program and eight-value result. hebrew_register_streams.txt retains all generated Hebrew numeric streams in one file. branch_summary.json records every first repeated full state and the period. A computational repeat is not a recovered source start/end marker. Source page bounds are not automatically message bounds. No word search or sentence coherence filter was used.\n\n'
    report+='Reproduce before the run exists: python -X utf8 -B WOWSignal/scripts/step03_whole_signal_container_transforms.py\nThis command refuses an existing run directory and appends a checkpoint and the combined Hebrew outputs to the working Hebrew text.\n\n'
    report+='Added the runner and run008 source_cells.csv, source_boundaries.json, path_definitions.json, process.json, instruction_trace.jsonl.gz, register_passes.csv, hebrew_register_streams.txt, branch_summary.json, summary.json, README.md, manifest.json. Appended data and process to the existing combined working Hebrew text. Added the runner byte-preserving .gitattributes rule. Earlier run records remain unchanged. No commit or push.\n'
    (out/'README.md').write_text(report,encoding='utf-8')
    working=BASE/'hebrew_streams_updated.txt';before=working.read_bytes();assert '# Whole-signal container transforms: complete preserved82x50 grid' not in before.decode('utf-8')
    with working.open('ab') as f:f.write(('\n\n'+report+'\n').encode('utf-8'));f.write(textpath.read_bytes())
    attrs=ROOT/'WOWSignal/.gitattributes';b=attrs.read_bytes();rule=b'scripts/step03_whole_signal_container_transforms.py -text'
    if rule not in b:attrs.write_bytes(b.rstrip(b'\r\n')+b'\n'+rule+b'\n')
    paths_files=[Path(__file__),working,attrs]+sorted(out.iterdir())
    dump(out/'manifest.json',{'runner_sha256':sha(Path(__file__)),'prior_working_bytes':len(before),'prior_working_sha256':hashlib.sha256(before).hexdigest(),'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths_files],'source_hashes_verified':True,'per_axis_coverage_verified':True,'commit_or_push':False})
    print(json.dumps(aggregates,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
