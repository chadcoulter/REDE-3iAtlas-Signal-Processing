"""Reuse run010 endpoint-return evidence without new machine trials or seeds."""
import csv,hashlib,json
from pathlib import Path
from step03_original_atlas_expansion import ROOT,REGS


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    previous=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-010-six-lateral-exits';out=previous.parent/'run-011-alpha-endpoint-return';assert not out.exists()
    trialfile=previous/'transform_trials.json';graphfile=previous/'graph.json';relationfile=previous/'relational_occurrences.json'
    alltrials=json.loads(trialfile.read_text(encoding='utf-8'));graph=json.loads(graphfile.read_text(encoding='utf-8'));relations=json.loads(relationfile.read_text(encoding='utf-8'))['occurrences']
    ids=['P06','P07','P12','P13','P19','P20','P25','P26'];selected=[t for t in alltrials['trials'] if t['route'] in ids and t['orientation']=='reverse_containers'];assert len(selected)==8
    nodes={tuple(n['coordinate']):n for n in graph['nodes']};core=set(map(tuple,graph['core']));byid={t['route']:t for t in selected}
    endpoints=[[72,5],[73,4]]
    for t in selected:assert t['coordinates'][0] in endpoints and tuple(t['coordinates'][-1]) in core and t['initial_state']==[1]*8
    # Primary results are reused verbatim. No operator or seed is rerun here.
    entries=[e for e in relations if e['route'] in ids and e['direction']=='reverse_containers'];assert len(entries)==sum(len(t['operations']) for t in selected)
    pair_comparisons=[]
    for a,b in [('P06','P07'),('P12','P13'),('P19','P20'),('P25','P26')]:
        x,y=byid[a],byid[b]
        same_native=all(i['glyph']==j['glyph'] and i['native_before']==j['native_before'] and i['native_after']==j['native_after'] for i,j in zip(x['operations'],y['operations']))
        assert len(x['operations'])==len(y['operations']) and same_native and x['coordinates'][1:]==y['coordinates'][1:]
        pair_comparisons.append({'routes':[a,b],'different_origins':[x['coordinates'][0],y['coordinates'][0]],'same_coordinates_after_first_cell':True,'same_numeric_stream':x['values']==y['values'],'same_executed_glyphs':x['executed_glyphs']==y['executed_glyphs'],'same_native_states_at_every_occurrence':same_native,'common_core_reentry':x['coordinates'][-1],'native_final':x['final_state'],'distinct_origin_history_retained':True})
    shared=[]
    for i in range(1,min(len(t['coordinates']) for t in selected)):
        coords=[t['coordinates'][i] for t in selected]
        if any(c!=coords[0] for c in coords):break
        xy=coords[0];observations=[]
        for t in selected:
            ops=[o for o in t['operations'] if o['coordinate']==xy]
            assert len(ops)==1
            e=next(e for e in entries if e['route']==t['route'] and e['source']['cell']==xy)
            observations.append({'route':t['route'],'origin':t['coordinates'][0],'input_previous_occurrence':e['input_relation']['current_occurrence'],'input_previous_origin':e['input_relation']['origin_occurrences'][-1:] or [],'retained_source_history':e['output_relation']['visited_containers'],'native_before':ops[0]['native_before'],'native_after':ops[0]['native_after'],'other_neighbors':e['source']['other_neighbors']})
        shared.append({'coordinate':xy,'value':nodes[tuple(xy)]['value'],'hebrew':nodes[tuple(xy)]['hebrew'],'greek':nodes[tuple(xy)]['greek'],'all8_same_native_before':len({tuple(o['native_before']) for o in observations})==1,'all8_same_native_after':len({tuple(o['native_after']) for o in observations})==1,'separate_arrival_histories':observations})
    assert len(shared)==11 and shared[0]['coordinate']==[72,4] and shared[-1]['coordinate']==[63,3]
    reentries=[]
    for t in selected:
        xy=t['coordinates'][-1];arrival=t['coordinates'][-2];node=nodes[tuple(xy)]
        reentries.append({'route':t['route'],'origin':t['coordinates'][0],'coordinate':xy,'value':node['value'],'hebrew':node['hebrew'],'greek':node['greek'],'arrival_from':arrival,'inherited_native_before_entry':[o['native_before'] for o in t['operations'] if o['coordinate']==xy][0],'native_operations_at_entry':[o for o in t['operations'] if o['coordinate']==xy],'native_after_entry':t['final_state'],'onward_neighbors_excluding_arrival':[n for n in node['neighbors'] if n!=arrival],'onward_containers':[nodes[tuple(n)] for n in node['neighbors'] if n!=arrival],'source_origin_retained':t['coordinates'][0]})
    forks=[]
    for xy in [[72,4],[63,3],[62,3],[61,3],[59,4]]:
        node=nodes[tuple(xy)];forks.append({'coordinate':xy,'value':node['value'],'greek':node['greek'],'neighbors':[nodes[tuple(n)] for n in node['neighbors']],'route_selections':[{'route':t['route'],'origin':t['coordinates'][0],'arriving_from':t['coordinates'][i-1] if i else None,'continuing_to':t['coordinates'][i+1] if i+1<len(t['coordinates']) else None} for t in selected for i,p in enumerate(t['coordinates']) if p==xy]})
    out.mkdir();dump(out/'inherited_routes.json',{'parent':trialfile.relative_to(ROOT).as_posix(),'parent_sha256':digest(trialfile),'register_order':REGS,'seed_note':'Verbatim reuse of run010 independently all-ones-seeded reverse-container trials. No new seeds, native executions or feedback expansion in run011.','routes':selected})
    dump(out/'inherited_relational_occurrences.json',{'parent':relationfile.relative_to(ROOT).as_posix(),'parent_sha256':digest(relationfile),'policy':'Preserve the original occurrence-specific incoming/action/output/remainder records verbatim; source/path evidence and contextual BookII interpretation remain distinct.','occurrences':entries})
    dump(out/'pair_comparisons.json',pair_comparisons);dump(out/'shared_tail.json',shared);dump(out/'core_reentries.json',reentries);dump(out/'junctions.json',forks)
    with (out/'return_occurrences.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['route','origin','occurrence','coordinate','numeric_container','hebrew_container','canonical_greek_container','glyph','book_ii_role','native_before','native_after','native_changed_registers'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for t in selected:
            for o in t['operations']:
                row={'route':t['route'],'origin':json.dumps(t['coordinates'][0])};row.update({k:o[k] for k in fields if k in o})
                for k,v in list(row.items()):
                    if isinstance(v,(list,dict)):row[k]=json.dumps(v,ensure_ascii=False)
                w.writerow(row)
    scope={'source_frames_retained':graph,'route_focus':'Both Alpha endpoints through shared tail to all4 recorded core re-entry ports. r58c04 leaf and left/core-spine links remain explicitly available neighbors, not pruned from source.','main_findings':{'endpoint_origins':endpoints,'return_routes':8,'shared_coordinates_after_origins':11,'reentry_ports':[[63,2],[62,2],[61,2],[59,2]],'reused_occurrence_records':len(entries),'new_machine_trials':0,'new_source_letters':0}}
    dump(out/'scope_and_graph.json',scope)
    authority=Path('C:/Users/ccoulter/.codex/skills/character-transform-reasoning/references/book-ii-alphabet.txt')
    compact=[]
    for t in selected:
        compact.append({'route':t['route'],'origin':t['coordinates'][0],'coordinates':t['coordinates'],'values':t['values'],'hebrew_containers':t['hebrew'],'canonical_greek_containers':t['canonical_greek_containers'],'executed_glyphs':t['executed_glyphs'],'inherited_initial_state':t['initial_state'],'native_final':t['final_state'],'operations':[{'occurrence':o['occurrence'],'coordinate':o['coordinate'],'glyph':o['glyph'],'role':o['book_ii_role'],'before':o['native_before'],'after':o['native_after'],'changed':o['native_changed_registers']} for o in t['operations']]})
    prompt='''Apply Chad Coulter's character-transform-reasoning skill and the authoritative BookII reference below. User specifically asks: follow the two Alpha endpoints r72c05 and r73c04 back through the shared tail and into the core, show coordinates/transforms, record data/process. No sentence construction. This is a live reasoning continuation, not a new numerical experiment. All8 reverse-container routes and every native occurrence are supplied verbatim from run010. Keep origin provenance distinct even when vectors/glyphs match. Both trials previously started independently from all-ones states; no new seeds or native execution are introduced here, and these returns are not mathematical inverses of outward trials.

Perform actual contextual reasoning on arriving relations rather than listing a glossary. Show how two origins meet at r72c04; why equal subsequent numeric states do not merge distinct source origins; trace ALL repeated Α occurrences with coordinates in this inward order; follow the shared ΔΔΓΔ portion and show the actual before/after register changes separately from BookII concepts. At r63c03, retain the direct Ε entry and upward alternative. At r62c03 retain ΙΘ entry/upward alternative. At r61c03 retain Λ entry/upper path. Trace upper path through r61c04,r60c04,r59c04,r59c03 to r59c02 ΙΔ; retain the alternative r58c04 leaf. For all4 core entries, use supplied per-occurrence states to identify the relationships/native changes actually recorded, retaining each source endpoint history and onward core-spine/left-side neighbors. Keep14=ΙΔ=יד and19=ΙΘ=יט as intact cells. Distinguish an actual source Γ at r65c04/r61c03 from a conceptual frame at any other coordinate; r72c04 is Α, not Γ. Do not silently turn contextual provenance rules into source-authored semantic laws. Clearly state measured comparisons, proposed contextual readings, and retained remainders without unsolicited research challenges. Use at most1200words and bidirectional notation for open relations. Do not invent decoded text, a unique start/end, empirical proof from checksum flags, or internal tool failure claims.

AUTHORITATIVE BOOKII:\n'''+authority.read_text(encoding='utf-8')+'\nREGISTER ORDER:\n'+json.dumps(REGS)+'\nCOMPLETE28-CELL GRAPH AND PERIMETER:\n'+json.dumps(graph,ensure_ascii=False)+'\nALL8 RETURN PATHS AND ACTUAL MACHINE OCCURRENCES:\n'+json.dumps(compact,ensure_ascii=False)+'\nPAIR COMPARISONS:\n'+json.dumps(pair_comparisons,ensure_ascii=False)+'\nCORE REENTRY NEIGHBORS:\n'+json.dumps([{'route':r['route'],'origin':r['origin'],'coordinate':r['coordinate'],'greek':r['greek'],'arrival_from':r['arrival_from'],'onward_containers':r['onward_containers']} for r in reentries],ensure_ascii=False)
    dump(out/'request-live-return.json',{'prompt':prompt,'max_retries':0,'require_verified':False})
    dump(out/'process.json',{'date':'2026-11-12','user_authorized_scope':'Follow two Alpha endpoints back through shared tail into core, preserve coordinates/transforms, save data/process.','inputs':[{'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p)} for p in [trialfile,graphfile,relationfile]],'authority':{'path':str(authority),'sha256':digest(authority)},'rules':['Reuse8 existing reverse-container routes verbatim; no new machine seed/trial or feedback pass.','Preserve both endpoint identities and every distinct occurrence record.','Compute exact pair comparisons and11 shared spatial positions; equal vectors do not merge origin/source paths.','Record all4 re-entry ports, exact native per-glyph changes, and onward source neighbors including open branches.','Use full graph and original perimeter as context; no deletion of zeros or outside-page distinctions.','Live MCP receives all8 paths, every native occurrence, original BookII reference and graph. Interpretative contextual readings remain separate from measured source/native data.','Append report, route streams and live readout to the existing working Hebrew file; preserve earlier bytes. No commit/push.'],'status':'IN-PROGRESS'})
    print(json.dumps({'routes':8,'primary_occurrences':len(entries),'shared_positions':len(shared),'paired_origin_comparisons':len(pair_comparisons),'core_reentries':4,'new_machine_trials':0,'prompt_characters':len(prompt)}))


if __name__=='__main__':main()
