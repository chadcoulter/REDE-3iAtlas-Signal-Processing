"""Trace all six lateral exits of the28-cell Wow component, retaining both directions."""
import csv,hashlib,json
from collections import Counter,deque
from pathlib import Path
from step03_original_atlas_expansion import ROOT,REGS,load
from step03_hebrew_gematria import hebrew
import sys
sys.path.insert(0,str(ROOT/'WOWSignal/sources/3i-atlas-expansion/original_process'))
from endpoint_phase import encode,numeral_table
from operator_machine import execute


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def edge(a,b):return tuple(sorted((a,b)))


def main():
    out=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-010-six-lateral-exits';assert not out.exists()
    source=ROOT/'WOWSignal/steps/01-source-data/run-001/numeric_grid.json';grid=json.loads(source.read_text(encoding='utf-8'))['grid']
    prior=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-009-live-mcp-whole-signal/candidate_frame_edges.json';frames=json.loads(prior.read_text(encoding='utf-8'))
    members={tuple(v['coordinate']):v['numeric_value'] for v in frames['containing_frames'][0]['members']}
    assert len(members)==28 and all(grid[r-1][c-1]==v for (r,c),v in members.items())
    adj={p:sorted(q for q in members if abs(p[0]-q[0])+abs(p[1]-q[1])==1) for p in members}
    edges=sorted({edge(p,q) for p in adj for q in adj[p]});assert len(edges)==30
    core={(r,2) for r in range(58,64)}
    table=numeral_table(ROOT/'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    _,_,_,compiled,operators=load()
    roles={'Α':'Origin','Β':'Branch','Γ':'Boundary frame / transform operator','Δ':'Change','Ε':'Threshold','Ζ':'Link','Η':'State','Θ':'Constraint','Ι':'Instance','Κ':'Context','Λ':'Lattice resolution','Ϛ':'Resolve observable unresolvedness'}
    def cell(p):
        v=members[p];return {'coordinate':list(p),'value':v,'hebrew':hebrew(v),'greek':encode(v,table),'neighbors':[list(q) for q in adj[p]],'degree':len(adj[p]),'core':p in core}
    exits=[{'id':f'E{i}','from':tuple(v['from']),'to':tuple(v['to'])} for i,v in enumerate(frames['containing_frames'][0]['core_lateral_exits_retained_inside_this_component'],1)]
    assert len(exits)==6 and {edge(e['from'],e['to']) for e in exits}=={edge(p,q) for p,q in edges if (p in core)!=(q in core)}
    # Every simple outer-tree continuation is retained until its next core return
    # or leaf. At a core-return branch, other outer branches are still explored.
    paths=[]
    for e in exits:
        def visit(route):
            current=route[-1];previous=route[-2];choices=[q for q in adj[current] if q!=previous]
            if not choices:
                paths.append({'exit':e['id'],'kind':'graph_leaf','path':route.copy()});return
            for q in choices:
                if q in core:paths.append({'exit':e['id'],'kind':'core_return','path':route+[q]})
                elif q in route:paths.append({'exit':e['id'],'kind':'outer_cycle_revisit','path':route+[q]})
                else:visit(route+[q])
        visit([e['from'],e['to']])
    assert len(paths)==26 and Counter(p['kind'] for p in paths)=={'graph_leaf':14,'core_return':12}
    # Decompose all edges into non-branching corridors, splitting also at every
    # source core cell and lateral crossing endpoint to preserve source roles.
    anchors={p for p in adj if len(adj[p])!=2}|core|{e['to'] for e in exits};visited=set();corridors=[]
    for a in sorted(anchors):
        for b in adj[a]:
            if edge(a,b) in visited:continue
            route=[a,b];visited.add(edge(a,b))
            while route[-1] not in anchors:
                nxt=next(q for q in adj[route[-1]] if q!=route[-2]);visited.add(edge(route[-1],nxt));route.append(nxt)
            corridors.append({'id':f'C{len(corridors)+1:02}','path':route})
    assert visited==set(edges)
    # Fundamental graph cycles: one per non-tree edge, no lost repeated cells.
    parent={min(members):None};todo=deque(parent);tree=set()
    while todo:
        p=todo.popleft()
        for q in adj[p]:
            if q not in parent:parent[q]=p;tree.add(edge(p,q));todo.append(q)
    basis=[]
    for a,b in edges:
        if edge(a,b) in tree:continue
        aa=[];v=a
        while v is not None:aa.append(v);v=parent[v]
        bb=[];v=b
        while v not in aa:bb.append(v);v=parent[v]
        route=aa[:aa.index(v)+1]+bb[::-1]+[a]
        basis.append({'id':f'L{len(basis)+1}','path':route,'values':[members[q] for q in route],'greek':[encode(members[q],table) for q in route]})
    assert len(basis)==3
    # Attach actual operator execution as independent, explicitly seeded trials.
    # BookII names and interpretation are a separate field/actual live MCP pass.
    trials=[];opchecks=0
    for index,p in enumerate(paths,1):
        p['id']=f'P{index:02}'
        for orientation in ['outward','reverse_containers','reverse_all_glyphs']:
            coords=p['path'] if orientation=='outward' else p['path'][::-1]
            blocks=[encode(members[q],table) for q in coords]
            state=[1]*8;a=0;z=False;ops=[]
            for ci,(xy,block) in enumerate(zip(coords,blocks),1):
                glyphs=list(block) if orientation!='reverse_all_glyphs' else list(block[::-1])
                for gi,g in enumerate(glyphs,1):
                    if g in ' |0':continue
                    before=state.copy();a,z=compiled[g](state,a,z)
                    expected=dict(zip(REGS,before));execute(operators[g]['assembly'],expected);assert state==[expected[r] for r in REGS]
                    ops.append({'occurrence':len(ops)+1,'container_index':ci,'glyph_index_in_executed_container':gi,'coordinate':list(xy),'numeric_container':members[xy],'hebrew_container':hebrew(members[xy]),'canonical_greek_container':block,'glyph':g,'book_ii_role':roles[g],'case_rule':'Uppercase tells how to resolve the observable.','native_before':before,'native_after':state.copy(),'native_changed_registers':[r for r,x,y in zip(REGS,before,state) if x!=y],'native_assembly':operators[g]['assembly'],'retained_remainder':{'source_coordinate':list(xy),'neighbors':[list(q) for q in adj[xy]],'other_exit_routes_remain_open':True,'source_message_delimiter_status':'unresolved'}})
            opchecks+=len(ops)
            trials.append({'route':p['id'],'exit':p['exit'],'kind':p['kind'],'orientation':orientation,'coordinates':[list(q) for q in coords],'values':[members[q] for q in coords],'hebrew':[hebrew(members[q]) for q in coords],'canonical_greek_containers':blocks,'executed_glyphs':''.join(o['glyph'] for o in ops),'initial_state':[1]*8,'final_state':state,'operations':ops,'seed_note':'Independent all-ones machine-comparison trial. It is not a recovered source state or a new message expansion.'})
    out.mkdir();dump(out/'graph.json',{'nodes':[cell(p) for p in sorted(members)],'edges':[[list(a),list(b)] for a,b in edges],'core':[list(p) for p in sorted(core)],'exits':exits,'corridors':corridors,'fundamental_cycles':basis,'source_perimeter':frames['containing_frames'][0]['external_perimeter_including_zeros_and_page_edges']})
    for p in paths:
        p['cells']=[cell(q) for q in p['path']]
        p['endpoint_available_continuations']=[list(q) for q in adj[p['path'][-1]]]
        p['endpoint_policy']='Core return retains onward neighbors; graph leaf retains surrounding zeros/page edge, not message EOF.'
    dump(out/'routes.json',paths);dump(out/'transform_trials.json',{'register_order':REGS,'trials':trials,'native_operator_comparisons':opchecks})
    with (out/'character_transforms.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['route','exit','orientation','occurrence','container_index','coordinate','numeric_container','hebrew_container','canonical_greek_container','glyph','book_ii_role','native_before','native_after','native_changed_registers'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for trial in trials:
            for op in trial['operations']:
                row={k:trial[k] for k in ['route','exit','orientation']};row.update({k:op[k] for k in fields if k in op})
                for k,v in list(row.items()):
                    if isinstance(v,(list,dict)):row[k]=json.dumps(v,ensure_ascii=False)
                w.writerow(row)
    compact=[]
    for p in paths:
        compact.append({'route':p['id'],'exit':p['exit'],'kind':p['kind'],'coordinates':p['path'],'values':[members[q] for q in p['path']],'hebrew':[hebrew(members[q]) for q in p['path']],'greek':[encode(members[q],table) for q in p['path']]})
    prompt='''Use Chad Coulter's character-transform-reasoning skill on these COMPLETE measured six-exit routes. The user asks: follow all six lateral exits through the28-cell component in both directions, show coordinates and transforms, record data/process. Do not build sentences from the codes. Preserve every cell, repeated letter, multi-letter numeric container, junction, return, source zero, page-edge distinction, and unresolved remainder. Input labels are one-based [row,channel]. Numeric6 usesϚ, notϜ. A container such as14=ΙΔ=יד remains ONE source cell. All Greek uppercase tells HOW to resolve the observable.

The actual graph has28vertices,30edges,3 independent cycles. Removing six core cells leaves an outer forest: two one-cell branches and a20-cell tree. All26 outer continuations are enumerated below:12 core returns and14 graph-leaf paths. Core returns are scope re-entries, not terminal messages. Their reverse container paths preserve internal glyph order; full glyph reversal is a distinct trial. Three independent graph cycles are supplied; core-return cycles may be composed through the retained original core spine, not by teleporting between letters.

Apply the actual BookII operators in occurrence order against evolving RELATIONAL CONTEXT, not just a glossary. Distinguish that conceptual operation from native machine implementations. Independent native all-ones route trials are recorded separately, not assumed original source states. For all6 exits, explain exactly how the relationship changes outbound and back, including where branches join, where paths return to which core cells, how the common tail is shared, and which continuations remain open. Include coordinate-complete traces for the short branches and at least one complete core-return loop, and account for ALL repeated Alpha occurrences on the long tail with coordinates rather than collapsing them. Cite actual route IDs when grouping repeated structure. Retain all other routes in your accounting. Give numeric observations separately from interpretation; do not infer message EOF from degree or collapse source boundaries. Do not claim a hidden decoded phrase, unique orientation, empirical verification from checksums, or internal tool failures without evidence. Output at most1500words.

AUTHORITATIVE BOOKII:\n'''+Path('C:/Users/ccoulter/.codex/skills/character-transform-reasoning/references/book-ii-alphabet.txt').read_text(encoding='utf-8')+'\nCOMPLETE GRAPH:\n'+json.dumps({'nodes':[cell(p) for p in sorted(members)],'exits':exits,'fundamental_cycles':basis,'perimeter':frames['containing_frames'][0]['external_perimeter_including_zeros_and_page_edges']},ensure_ascii=False)+'\nALL OUTWARD PATHS (reverse each coordinate-container list to obtain its inward counterpart):\n'+json.dumps(compact,ensure_ascii=False)
    dump(out/'request-001-live-relations.json',{'prompt':prompt,'max_retries':0,'require_verified':False})
    process={'user_authorized_scope':'All6 lateral exits through the28-cell component, both directions, coordinates/transforms, saved process/data. No sentence construction.','source_sha256':digest(source),'prior_frame_sha256':digest(prior),'register_order':REGS,'graph_rule':'Original4-neighbor nonzero component, all28 cells and30 edges; zeros and page edges retained in perimeter.','route_rule':'For each crossing edge, recursively retain every simple continuation in the non-core forest. Stop a single route at the next core return or graph leaf, but retain every sibling branch and endpoint onward references. No message closure follows.','corridor_rule':'Split at degree!=2, all core cells and exit-neighbor cells; every graph edge belongs to exactly one corridor.','cycles':'BFS spanning tree and all3 non-tree edges give a fundamental cycle basis; routes may compose with the original core spine for graph returns.','directions':'Outward and reverse-container order retain canonical internal encodings; reverse-all-glyphs also reverses each internal encoding.','native_comparison':'Explicit independent all-ones trials for every route/direction; every operation compared with original instruction interpreter; no register-feedback expansion in this run. BookII conceptual roles are separate.','live_mcp':'Complete graph, all26 routes, original BookII reference, and source perimeter supplied. Preserve exact request/response and qualification records.','status':'IN-PROGRESS'}
    dump(out/'process.json',process)
    print(json.dumps({'nodes':28,'edges':30,'independent_cycles':3,'corridors':len(corridors),'routes':len(paths),'trials':len(trials),'operator_checks':opchecks,'route_counts':dict(Counter(p['exit'] for p in paths)),'prompt_chars':len(prompt)},ensure_ascii=False))


if __name__=='__main__':main()
