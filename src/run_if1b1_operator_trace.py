import csv,re,subprocess,json,collections
from pathlib import Path
p=Path('/mnt/data')
src=(p/'3I_ATLAS_four_lane_all_register_feedback.S').read_text()
ops={}
lines=src.splitlines()
for i,line in enumerate(lines):
 m=re.match(r'\s*# ([^ ]+) ([A-Z]+)\s*$',line)
 if not m:continue
 glyph=m.group(1)
 if len(glyph)!=1 or glyph in ops:continue
 body=[]
 for x in lines[i+1:]:
  if x.strip().startswith('#') or not x.strip():break
  body.append(x)
 if body:ops[glyph]='\n'.join(body)+'\n'
rows=sorted([r for r in csv.DictReader(open(p/'streams(1).csv',encoding='utf-8-sig')) if r['stream_id']=='IF1_B1'],key=lambda r:int(r['frame']))
assert len(rows)==20
regs=['state','relations','constraints','observations','pattern','context','target','events']
header='''.section .bss\n'''+''.join(f'.lcomm {x},8\n' for x in regs)+'''.section .rodata\nfmt: .asciz "frame=%lu op=%lu state=%lu relations=%lu constraints=%lu observations=%lu pattern=%lu context=%lu target=%lu events=%lu\\n"\n.section .text\n.globl main\nmain:\n pushq %rbp\n movq %rsp,%rbp\n subq $64,%rsp\n'''
# printf 11 args incl format; six GP registers (rdi + 5), five stack args
fmtargs=''' movq state(%rip),%rcx\n movq relations(%rip),%r8\n movq constraints(%rip),%r9\n movq observations(%rip),%rax\n movq %rax,(%rsp)\n movq pattern(%rip),%rax\n movq %rax,8(%rsp)\n movq context(%rip),%rax\n movq %rax,16(%rsp)\n movq target(%rip),%rax\n movq %rax,24(%rsp)\n movq events(%rip),%rax\n movq %rax,32(%rsp)\n leaq fmt(%rip),%rdi\n xorl %eax,%eax\n call printf@PLT\n'''
output=[]
for direction in ('forward','reverse'):
 frames=rows if direction=='forward' else rows[::-1]
 prior=None
 for run in range(1,4):
  seeds={k:1 for k in regs} if prior is None else prior
  code=header+''.join(f' movabsq ${v},%rax\n movq %rax,{k}(%rip)\n' for k,v in seeds.items())
  provenance=[]
  for row in frames:
   glyphs=row['gematria'].replace('|','').replace(' ','')
   if direction=='reverse':glyphs=glyphs[::-1]
   for idx,glyph in enumerate(glyphs,1):
    if glyph not in ops:raise ValueError(f'Missing operator {glyph}')
    provenance.append((int(row['frame']),idx,glyph))
    code+=f' # FRAME {row["frame"]} OP {idx} {glyph}\n'+ops[glyph]
    code+=f' movq ${int(row["frame"])},%rsi\n movq ${idx},%rdx\n'+fmtargs
  code+=' xorl %eax,%eax\n leave\n ret\n.section .note.GNU-stack,"",@progbits\n'
  name=f'IF1_B1_operator_{direction}_pass{run}'
  asm=p/(name+'.S'); exe=p/name;asm.write_text(code)
  subprocess.run(['gcc','-O0','-no-pie',str(asm),'-o',str(exe)],check=True,capture_output=True)
  linesout=subprocess.run([str(exe)],check=True,capture_output=True,text=True).stdout.splitlines()
  trace=[]
  for line,prov in zip(linesout,provenance):
   d={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',line)}
   assert (d['frame'],d['op'])==prov[:2]
   d.update(direction=direction,pass_number=run,seconds=d['frame']*15,glyph=prov[2],global_step=len(trace)+1)
   trace.append(d)
  assert len(trace)==len(provenance)
  prior={k:trace[-1][k] for k in regs}
  output.extend(trace)
fields=['direction','pass_number','global_step','frame','seconds','op','glyph']+regs
with open(p/'IF1_B1_operator_trace.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(output)
# Analyze exact returns within and across passes/directions, partial repeated register values,
# and transitions where a single operator makes no change to the entire register state.
full=collections.defaultdict(list)
for r in output:full[tuple(r[k] for k in regs)].append((r['direction'],r['pass_number'],r['frame'],r['op'],r['glyph']))
returns=[{'state':list(key),'locations':locs} for key,locs in full.items() if len(locs)>1]
within=[x for x in returns if len({(loc[0],loc[1]) for loc in x['locations']})<len(x['locations'])]
cross=[x for x in returns if len({loc[0] for loc in x['locations']})>1]
noops=[];transitions=[]
for direction in ('forward','reverse'):
 for run in range(1,4):
  rr=[r for r in output if r['direction']==direction and r['pass_number']==run]
  for a,b in zip(rr,rr[1:]):
   changed=sum(a[k]!=b[k] for k in regs)
   if changed==0:noops.append({'direction':direction,'pass':run,'frame':b['frame'],'op':b['op'],'glyph':b['glyph']})
   transitions.append({'direction':direction,'pass':run,'from_frame':a['frame'],'to_frame':b['frame'],'op':b['op'],'glyph':b['glyph'],'changed_registers':changed})
report={'source':'streams(1).csv IF1_B1 peak amplitude gematria','method':'native operator bodies from 3I_ATLAS_four_lane_all_register_feedback.S, snapshot after every operator, 3 passes in each direction; reverse frame and glyph order; seed 1 each direction then feedback previous pass final','operator_snapshots':len(output),'per_run':[{'direction':d,'pass':n,'snapshots':sum(r['direction']==d and r['pass_number']==n for r in output)} for d in ('forward','reverse') for n in range(1,4)],'exact_repeated_full_states':len(returns),'exact_returns_within_run':len(within),'exact_cross_direction_states':len(cross),'unchanged_operator_transitions':len(noops),'unchanged_examples':noops[:25],'full_state_return_examples':returns[:15],'transition_changed_register_histogram':dict(collections.Counter(x['changed_registers'] for x in transitions))}
(p/'IF1_B1_operator_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k not in ('full_state_return_examples','unchanged_examples')},indent=2))