"""Audit whole-grid live MCP tokenization and source-boundary calculations."""
import csv,gzip,hashlib,json
from pathlib import Path
from step03_original_atlas_expansion import ROOT


def main():
    out=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-009-live-mcp-whole-signal'
    cells=json.loads((out/'container_map.json').read_text(encoding='utf-8'))
    result=json.loads((out/'response-tokenize.json').read_text(encoding='utf-8'))['response']['structuredContent']['result']
    source=ROOT/'WOWSignal/steps/01-source-data/run-001/numeric_grid.json';grid=json.loads(source.read_text(encoding='utf-8'))['grid']
    assert len(cells)==4100 and len(result['values'])==len(result['text'])==8202
    checks=[]
    for cell in cells:
        a,b=cell['text_start_0based'],cell['text_end_exclusive'];values=result['values'][a:b]
        expected=grid[cell['row']-1][cell['channel']-1]
        assert sum(values)==expected==cell['numeric_bin']
        assert result['text'][a:b]==cell['hebrew']
        checks.append({'row':cell['row'],'channel':cell['channel'],'numeric_bin':expected,'hebrew':cell['hebrew'],'live_letter_values':values,'regrouped_sum':sum(values),'matches':True})
    assert result['sum']==sum(c['numeric_bin'] for c in cells)==1487
    (out/'tokenizer_container_verification.json').write_text(json.dumps({'passed':4100,'failed':0,'source_sum':1487,'live_sum':result['sum'],'containers':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    readout='Live MCP Hebrew source containers, verified against all4100 numeric bins. Zeros retained. Separators mark representation/container boundaries, not source punctuation or end markers.\n\n'
    for c in range(50):readout+=f'Channel{c+1:02}: '+' | '.join(cells[r*50+c]['hebrew'] for r in range(82))+'\n'
    readout+='\nHorizontal views of the same cells (not additional observations):\n'
    for r in range(82):readout+=f'Row{r+1:02}: '+' | '.join(cells[r*50+c]['hebrew'] for c in range(50))+'\n'
    (out/'mcp_preserved_hebrew_streams.txt').write_text(readout,encoding='utf-8')
    runs=json.loads((out/'run_relationships.json').read_text(encoding='utf-8'));core=runs['summary']['core_run']
    assert core['values']==[6,14,26,30,19,5] and core['sum']==100
    assert len(runs['runs'])==1416
    claims=[]
    def check(label,actual,stated):
        claims.append({'claim':label,'computed':actual,'mcp_stated':stated,'matches':actual==stated});assert actual==stated
    check('first nonzero row-major',[c['row'] for c in cells if c['numeric_bin']][0],1)
    nz=[c for c in cells if c['numeric_bin']];check('first nonzero coordinate',[nz[0]['row'],nz[0]['channel']],[1,4]);check('last nonzero coordinate',[nz[-1]['row'],nz[-1]['channel']],[82,44])
    for r,c,value in [(57,2,0),(58,2,6),(59,2,14),(60,2,26),(61,2,30),(62,2,19),(63,2,5),(64,2,0),(59,1,1),(59,3,2),(59,4,4),(59,5,0),(63,3,1),(64,3,1),(64,4,4),(65,4,3),(1,3,0),(1,4,2),(1,5,0),(2,4,1),(82,43,0),(82,44,1),(82,45,0),(81,44,0)]:check(f'r{r}c{c}',grid[r-1][c-1],value)
    check('source nonzero count',len(nz),1112);check('source zero count',4100-len(nz),2988);check('source sum',sum(c['numeric_bin'] for c in cells),1487)
    check('core sum',sum(grid[r-1][1] for r in range(58,64)),100)
    check('forward first three original core containers',sum(grid[r-1][1] for r in range(58,61)),46)
    counts={'operator':0,'structural':0,'container_boundary':0}
    with gzip.open(out/'character_occurrences.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f:
            rec=json.loads(line)
            if rec['kind']=='operator':counts['operator']+=1
            elif rec['kind']=='container_boundary':counts['container_boundary']+=1
            else:counts['structural']+=1
    check('Greek encoded operator occurrences',counts['operator'],1115)
    (out/'reasoning_claim_checks.json').write_text(json.dumps({'numeric_and_coordinate_claim_checks':claims,'interpretation_note':'Coordinate/arithmetic checks do not certify inferred source semantics. The earlier[6,14,1] candidate is a generated-chain candidate, not a substitution into the original[6,14,26] triple.','occurrence_counts':counts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    hierarchy=json.loads((out/'component_hierarchy.json').read_text(encoding='utf-8'))
    nodes=hierarchy['nodes'];byid={n['id']:n for n in nodes}
    for threshold in hierarchy['summary']['thresholds']:
        selected=[n for n in nodes if n['threshold']==threshold]
        flattened=[tuple(x) for n in selected for x in n['cells']]
        expected={(r+1,c+1) for r in range(82) for c in range(50) if grid[r][c]>=threshold}
        assert len(flattened)==len(set(flattened)) and set(flattened)==expected
        for n in selected:
            cells_set=set(map(tuple,n['cells']));reached={next(iter(cells_set))};pending=list(reached)
            while pending:
                r,c=pending.pop()
                for xy in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    if xy in cells_set and xy not in reached:reached.add(xy);pending.append(xy)
                    if 1<=xy[0]<=82 and 1<=xy[1]<=50 and grid[xy[0]-1][xy[1]-1]>=threshold:assert xy in cells_set
            assert reached==cells_set
    for edge in hierarchy['inclusion_edges']:
        parent=byid[edge['lower_threshold_node']];child=byid[edge['higher_threshold_node']]
        assert set(map(tuple,child['cells']))<=set(map(tuple,parent['cells']))
    assert len(nodes)==620 and len(hierarchy['inclusion_edges'])==225
    for axis in ['vertical','horizontal']:
        seen=[]
        for run in runs['runs']:
            if run['axis']!=axis:continue
            r,c=run['start'];dr,dc=(1,0) if axis=='vertical' else (0,1)
            coords=[(r+i*dr,c+i*dc) for i in range(run['length'])]
            assert [grid[a-1][b-1] for a,b in coords]==run['values']
            seen+=coords
        assert len(seen)==len(set(seen))==1112
    (out/'hierarchy_verification.json').write_text(json.dumps({'thresholds_checked':11,'nodes_checked':620,'inclusion_edges_checked':225,'all_threshold_memberships_complete_disjoint_connected_and_maximal':True,'all_nonzero_source_cells_covered_once_per_axis_in_run_comparison':True},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_containers_verified':len(checks),'source_sum':1487,'reasoning_claim_checks':len(claims),'occurrences':counts,'hierarchy_nodes_checked':620,'inclusion_links_checked':225}))


if __name__=='__main__':main()
