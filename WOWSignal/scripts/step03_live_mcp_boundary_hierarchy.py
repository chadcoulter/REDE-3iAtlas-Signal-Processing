"""Build complete whole-grid component inclusion hierarchy at observed thresholds."""
import json
from collections import Counter,defaultdict
from step03_original_atlas_expansion import ROOT


def main():
    out=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-009-live-mcp-whole-signal'
    g=json.loads((ROOT/'WOWSignal/steps/01-source-data/run-001/numeric_grid.json').read_text(encoding='utf-8'))['grid']
    thresholds=sorted({v for row in g for v in row if v});nodes=[];edges=[];previous=[];membership=defaultdict(list)
    for t in thresholds:
        seen=set();current=[]
        for r in range(82):
            for c in range(50):
                if g[r][c]<t or (r,c) in seen:continue
                todo=[(r,c)];seen.add((r,c));cells=[]
                while todo:
                    x,y=todo.pop();cells.append((x+1,y+1))
                    for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                        if 0<=a<82 and 0<=b<50 and g[a][b]>=t and (a,b) not in seen:seen.add((a,b));todo.append((a,b))
                key=tuple(sorted(cells));node={'id':len(nodes)+1,'threshold':t,'size':len(cells),'cells':[list(x) for x in key]};nodes.append(node);current.append(node);membership[key].append(node['id'])
                if previous:
                    parent=next(p for p in previous if set(key)<=set(map(tuple,p['cells'])))
                    edges.append({'lower_threshold_node':parent['id'],'higher_threshold_node':node['id'],'lost_cells':[x for x in parent['cells'] if tuple(x) not in set(key)],'exact_same_membership':parent['cells']==node['cells']})
        previous=current
    groups=[{'node_ids':ids,'thresholds':[nodes[i-1]['threshold'] for i in ids],'size':len(key),'cells':[list(x) for x in key]} for key,ids in membership.items()]
    core=tuple((r,2) for r in range(58,64));coregroup=next(s for s in groups if tuple(map(tuple,s['cells']))==core)
    summary={'thresholds':thresholds,'nodes':len(nodes),'inclusion_edges':len(edges),'distinct_memberships':len(groups),'memberships_repeated_across_thresholds':sum(len(s['node_ids'])>1 for s in groups),'core_exact_membership':coregroup,'same_size_six_cell_memberships':[s for s in groups if s['size']==6],'memberships_unchanged_at4_and5':sum(4 in s['thresholds'] and 5 in s['thresholds'] for s in groups),'memberships_unchanged_at4_and5_size_at_least2':sum(4 in s['thresholds'] and 5 in s['thresholds'] and s['size']>=2 for s in groups),'size_histogram_for_memberships_unchanged_at4_and5':dict(Counter(s['size'] for s in groups if 4 in s['thresholds'] and 5 in s['thresholds']))}
    assert sum(n['size'] for n in nodes if n['threshold']==1)==1112
    (out/'component_hierarchy.json').write_text(json.dumps({'policy':'Complete4-neighbor upper-level components at every observed nonzero threshold. Inclusion relations are derived descriptive topology. Source zeros and all original source values remain in the primary container graph. Exact membership persistence is measured across sampled numeric thresholds, not physical time.','summary':summary,'nodes':nodes,'inclusion_edges':edges,'membership_groups':groups},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'hierarchy_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
