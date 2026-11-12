"""Record full-grid BookII occurrence provenance and container graph for run009."""
import csv,gzip,hashlib,json,sys
from pathlib import Path
from step03_original_atlas_expansion import ROOT,REGS,load


def main():
    out=ROOT/'WOWSignal/steps/03-hebrew-gematria/run-009-live-mcp-whole-signal'
    assert not (out/'character_occurrences.jsonl.gz').exists()
    cells=json.loads((out/'container_map.json').read_text(encoding='utf-8'))
    _,_,_,compiled,operators=load()
    roles=dict(zip('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',['Origin','Branch','Boundary frame / transform operator','Change','Threshold','Link','State','Constraint','Instance','Context','Lattice resolution','Measure','Novel state','Contradiction','Observation','Projection','Relation','Aggregation','Whole-state traversal','Fork / choice','Form','Crossing / Kai carrier','Pattern','Target / terminal field']))
    roles.update({'Ϛ':'Resolve observable unresolvedness','Ϟ':'Resolve observable numeral/indexed relationships','Ϡ':'Resolve observable extended numerical order'})
    # Retain actual boundaries as structural tokens. They are not Greek ops.
    glyph_count=0;structural_count=0
    with gzip.open(out/'character_occurrences.jsonl.gz','wt',encoding='utf-8') as f,(out/'container_relationships.jsonl').open('w',encoding='utf-8') as graph:
        for r in range(1,83):
            state=[1]*8;a=0;z=False
            for c in range(1,51):
                cell=cells[(r-1)*50+c-1];neighbors={label:[x,y] for label,x,y in [('up',r-1,c),('down',r+1,c),('left',r,c-1),('right',r,c+1)] if 1<=x<=82 and 1<=y<=50}
                graph.write(json.dumps({'coordinate':[r,c],'numeric_container':cell['numeric_bin'],'hebrew_container':cell['hebrew'],'greek_container':cell['greek'],'neighbors':neighbors,'page_edge':r in [1,82] or c in [1,50],'retained_remainder':'Source interpretation, scope, and endpoint status remain open; numeric encoding alone does not resolve them.'},ensure_ascii=False)+'\n')
                for pos,g in enumerate(cell['greek'],1):
                    before=state.copy();kind='operator' if g in compiled else 'structural_numeric_zero_or_separator'
                    if kind=='operator':a,z=compiled[g](state,a,z);glyph_count+=1
                    else:structural_count+=1
                    item={'coordinate':[r,c],'container_value':cell['numeric_bin'],'hebrew_container':cell['hebrew'],'greek_container':cell['greek'],'occurrence_in_container':pos,'character':g,'kind':kind,'book_ii_role':roles.get(g),'book_ii_case_rule':'Uppercase tells how to resolve the observable' if g in roles else None,'book_ii_scope':'The role is an attributed interpretive mapping for this occurrence, not a recovered meaning or a replacement for the numeric value.','native_trace_scope':'run008 horizontal forward intact-source first pass; all-ones seed per row','native_before':before,'native_after':state.copy(),'native_assembly':operators[g]['assembly'] if kind=='operator' else [],'retained_neighbor_coordinates':neighbors,'retained_remainder':'Whole-grid source context, differing orientations, and unestablished message endpoints remain retained.'}
                    f.write(json.dumps(item,ensure_ascii=False)+'\n')
                f.write(json.dumps({'coordinate':[r,c],'kind':'container_boundary','character':'|','native_before':state.copy(),'native_after':state.copy(),'meaning':'Explicit representation delimiter; not a source-authored letter or closure marker.'},ensure_ascii=False)+'\n');structural_count+=1
    process={'skill_path':'C:/Users/ccoulter/.codex/skills/character-transform-reasoning/SKILL.md','authority':'Chad Coulter, REDΣ BookII version0.1 October13,2026; reference supplied verbatim in request001','whole_grid_supplied_to_live_reasoning':True,'whole_hebrew_grid_supplied_to_live_tokenizer':True,'coordinate_map':'container_map.json','tokenizer_adapter':'Flatten complete Hebrew numeral grid row-major with explicit pipe delimiters. Record each container character span before calling MCP; regroup returned letter values by these exact spans. Preserve source0 as a zero-valued structural placeholder and do not interpret tokenizer fallback letters as Greek values.','relationship_graph':'All4100 cells retain up/down/left/right neighbors including zeros, without pruning. Connected nonzero components are descriptive4-neighbor groups, not assumed sentences.','occurrence_ledger':'Every encoded Greek character and representation delimiter is retained. BookII roles are attributed to the skill. Actual machine actions are separately replayed from run008 horizontal-forward all-ones state. This local ledger is not claimed to be a model-generated per-cell inference.','request001':'Entire82x50 numeric grid, full authoritative BookII reference, explicit cell-container policy, descriptive spatial summary, and prior-run limitations. Ask live reasoning for actual coordinate-specific relationships, reverse traversal, scoped partial boundaries, retained remainders, and alternative endpoint hypotheses without sentence construction.','request002':'Live gematria tokenizer receives every Hebrew source-cell numeral in a single complete string.','response_capture':'Save complete MCP responses with start/end timestamps, provider, step identifiers, feedback and structural verification fields unchanged. MCP generated-feedback may write its own local adapter state.','verification_policy':'Check MCP numeric assertions against frozen source coordinates; structural_checksum is not a semantic or empirical truth certificate. Preserve corrections and disagreements rather than overwrite responses.','source_bounds':'All4100 cells of the frozen printout grid; no raw waveform or unobserved outside-page samples.','status':'IN-PROGRESS'}
    (out/'process.json').write_text(json.dumps(process,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_containers':len(cells),'greek_operator_occurrences':glyph_count,'structural_occurrences':structural_count}))


if __name__=='__main__':main()
