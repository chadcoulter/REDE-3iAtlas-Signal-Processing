"""Independently validate the six-exit graph, complete routes and source records."""
import hashlib,json
from collections import deque
from pathlib import Path
from step03_original_atlas_expansion import ROOT


def main():
    out=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-010-six-lateral-exits'
    graph=json.loads((out/'graph.json').read_text(encoding='utf-8'));routes=json.loads((out/'routes.json').read_text(encoding='utf-8'));trials=json.loads((out/'transform_trials.json').read_text(encoding='utf-8'))
    nodes={tuple(n['coordinate']):n for n in graph['nodes']};core=set(map(tuple,graph['core']));outer=set(nodes)-core
    g=json.loads((ROOT/'WOWSignal/steps/01-source-data/run-001/numeric_grid.json').read_text(encoding='utf-8'))['grid']
    adj={p:{q for q in nodes if abs(p[0]-q[0])+abs(p[1]-q[1])==1} for p in nodes}
    assert len(nodes)==28 and all(n['value']==g[p[0]-1][p[1]-1] for p,n in nodes.items())
    edges={tuple(sorted((p,q))) for p in adj for q in adj[p]};assert len(edges)==30 and len(edges)-len(nodes)+1==3
    corridor_edges=[]
    for c in graph['corridors']:
        path=list(map(tuple,c['path']));corridor_edges += [tuple(sorted((a,b))) for a,b in zip(path,path[1:])]
    assert len(corridor_edges)==30 and len(set(corridor_edges))==30 and set(corridor_edges)==edges
    for cycle in graph['fundamental_cycles']:
        p=list(map(tuple,cycle['path']));assert p[0]==p[-1] and all(b in adj[a] for a,b in zip(p,p[1:]))
    # Independent tree-path coverage: BFS all outer nodes, then connect every
    # other core port or original graph leaf. Compare exact coordinate walks.
    expected=set()
    for exit in graph['exits']:
        origin,target=tuple(exit['from']),tuple(exit['to']);parents={target:None};q=deque([target]);tree_edges=set()
        while q:
            a=q.popleft()
            for b in adj[a]&outer:
                tree_edges.add(tuple(sorted((a,b))))
                if b not in parents:parents[b]=a;q.append(b)
        assert len(tree_edges)==len(parents)-1
        for endpoint in sorted(parents):
            base=[];v=endpoint
            while v is not None:base.append(v);v=parents[v]
            base=[origin]+base[::-1]
            if len(adj[endpoint])==1:expected.add((exit['id'],'graph_leaf',tuple(base)))
            for port in adj[endpoint]&core:
                if endpoint==target and port==origin:continue
                expected.add((exit['id'],'core_return',tuple(base+[port])))
    actual={(r['exit'],r['kind'],tuple(map(tuple,r['path']))) for r in routes};assert actual==expected and len(actual)==26
    byroute={r['id']:r for r in routes};bytrial={(t['route'],t['orientation']):t for t in trials['trials']}
    for t in trials['trials']:
        path=byroute[t['route']]['path'];assert t['coordinates']==(path if t['orientation']=='outward' else path[::-1])
        previous=t['initial_state']
        for i,o in enumerate(t['operations'],1):
            assert o['occurrence']==i and o['native_before']==previous;previous=o['native_after']
            assert nodes[tuple(o['coordinate'])]['value']==o['numeric_container']
        assert previous==t['final_state']
    assert len(trials['trials'])==78 and sum(len(t['operations']) for t in trials['trials'])==735
    for edge in graph['source_perimeter']:
        r,c=edge['to']
        if edge['kind']=='observed_source_cell':assert g[r-1][c-1]==edge['value']==0
        else:assert not (1<=r<=82 and 1<=c<=50) and edge['value'] is None
    result={'source_cells_checked':28,'neighbor_edges_checked':30,'independent_cycles':3,'corridors_cover_every_edge_once':True,'outer_tree_BFS_confirms_all26_routes':True,'primary_bidirectional_trials':52,'separate_full_glyph_reverse_trials':26,'per_occurrence_records_checked':735,'source_perimeter_edges_checked':len(graph['source_perimeter']),'status':'PASS'}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':main()
