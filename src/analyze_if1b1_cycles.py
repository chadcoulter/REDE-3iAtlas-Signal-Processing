import csv,json,collections,pathlib
p=pathlib.Path('/mnt/data'); rows=list(csv.DictReader((p/'IF1_B1_operator_trace.csv').open(encoding='utf-8')))
keys=['state','relations','constraints','observations','pattern','context','target','events']
for r in rows:
 for k in keys+['pass_number','global_step','frame','op','seconds']:r[k]=int(r[k])
 r['signature']=tuple(r[k] for k in keys)
by=collections.defaultdict(list)
for r in rows:by[(r['direction'],r['pass_number'])].append(r)
cycles=[]; stationary=[]; transitions=collections.Counter()
for (direction,passnum),seq in by.items():
 visited=collections.defaultdict(list)
 for i,r in enumerate(seq):
  s=r['signature']
  for j in visited[s]:
   gap=i-j
   if gap==1:stationary.append((direction,passnum,seq[j]['global_step'],r['global_step'],r['glyph']))
   elif any(seq[k]['signature']!=s for k in range(j+1,i)):
    cycles.append({'direction':direction,'pass':passnum,'from_step':seq[j]['global_step'],'to_step':r['global_step'],'length':gap,'start_frame':seq[j]['frame'],'end_frame':r['frame'],'start_time':seq[j]['seconds'],'end_time':r['seconds'],'operators':''.join(x['glyph'] for x in seq[j+1:i+1]),'distinct_states':len(set(x['signature'] for x in seq[j:i+1]))})
  visited[s].append(i)
 for a,b in zip(seq,seq[1:]):transitions[sum(a[k]!=b[k] for k in keys)]+=1
cycles.sort(key=lambda x:(x['length'],x['direction'],x['pass'],x['from_step']))
report={'total_states':len(rows),'passes':len(by),'stationary_adjacent':len(stationary),'genuine_return_pairs':len(cycles),'genuine_returns_by_pass':dict(collections.Counter(f"{c['direction']}_{c['pass']}" for c in cycles)),'return_lengths':dict(sorted(collections.Counter(c['length'] for c in cycles).items())),'shortest_returns':cycles[:30],'longest_returns':sorted(cycles,key=lambda x:-x['length'])[:10],'transitions_changed_registers':dict(transitions)}
(p/'IF1_B1_cycle_analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (p/'IF1_B1_genuine_returns.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['direction','pass','from_step','to_step','length','start_frame','end_frame','start_time','end_time','operators','distinct_states']);w.writeheader();w.writerows(cycles)
print(json.dumps({k:v for k,v in report.items() if k not in ('shortest_returns','longest_returns')},indent=2));print('shortest:',json.dumps(cycles[:5],ensure_ascii=False))