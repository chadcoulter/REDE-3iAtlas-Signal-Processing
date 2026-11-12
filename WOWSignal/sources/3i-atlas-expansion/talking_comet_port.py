#!/usr/bin/env python3
"""Translate the 3I/ATLAS four-channel assembly operators to WASM-ready C.
Unsupported instructions fail instead of being silently replaced."""
import pathlib, re, sys
names=[f'{mode}_channel{i}' for mode in ('reflect','project') for i in range(1,5)]
registers='state relations constraints observations unresolved context target events'.split()
index={name:i for i,name in enumerate(registers)}
source=pathlib.Path(sys.argv[1]).read_text()
output=pathlib.Path(sys.argv[2])
def vals(name):
    m=re.search(r'^'+name+r':\s*\n\s*\.quad\s+([^\n]+)$',source,re.M)
    if not m: raise ValueError('missing '+name)
    return [int(x) for x in m[1].split(',')]
def ref(v):
    v=v.strip()
    if v=='%rax': return 'a'
    if re.fullmatch(r'\$\d+',v): return v[1:]+'ULL'
    m=re.fullmatch(r'(\w+)\(%rip\)',v)
    if m and m[1] in index:return f'r[{index[m[1]]}]'
    raise ValueError('unknown operand '+v)
def instruction(line):
    if re.fullmatch('[12]:',line):return 'L'+line[0]+': ;'
    m=re.fullmatch(r'([a-z][a-z0-9]*)\s*(.*?)',line)
    if not m:raise ValueError('unknown assembly '+line)
    op,rest=m.groups()
    if op in ('jz','jmp'):
        if rest not in ('1f','2f'):raise ValueError('unknown jump '+line)
        return ('if(z)goto ' if op=='jz' else 'goto ')+'L'+rest[0]+';'
    if op=='sete' and rest=='%al':return 'a=(a&~255ULL)|(z?1ULL:0ULL);'
    if op=='movzbq' and rest=='%al, %rax':return 'a&=255ULL;'
    if op=='incq':
        b=ref(rest);return f'{b}+=1ULL;z=({b}==0);'
    p=rest.split(', ')
    if len(p)!=2:raise ValueError('unknown instruction '+line)
    x,y=map(ref,p)
    if y.endswith('ULL'):raise ValueError('immediate destination '+line)
    if op=='movq':return f'{y}={x};'
    if op=='addq':return f'{y}+={x};z=({y}==0);'
    if op=='xorq':return f'{y}^={x};z=({y}==0);'
    if op=='andq':return f'{y}&={x};z=({y}==0);'
    if op=='cmpq':return f'z=({y}=={x});'
    if op=='testq':return f'z=(({y}&{x})==0);'
    if op=='xchgq':return f'tmp={x};{x}={y};{y}=tmp;'
    raise ValueError('unknown instruction '+line)
patterns,seen,sequences=[],{},{}
for i,name in enumerate(names):
    m=re.search(r'^'+name+r':\s*$',source,re.M)
    if not m:raise ValueError('missing '+name)
    next_match=re.search(r'^'+names[i+1]+r':\s*$',source,re.M) if i<7 else None
    body=source[m.end():next_match.start() if next_match else len(source)]
    seq,current,glyph=[],[],None
    def flush():
        global current,glyph
        if glyph is None:return
        if not current:raise ValueError('empty operator '+glyph)
        key=tuple(current)
        if key not in seen:
            seen[key]=len(patterns);patterns.append(key)
        seq.append(seen[key]);current=[];glyph=None
    for raw in body.splitlines():
        line=raw.strip()
        if not line:continue
        if line.startswith('# operator='):
            flush();glyph=line.split('=',1)[1]
        elif line.startswith('# traversal_index='):flush()
        elif line.startswith('#') or line.startswith('.'):continue
        elif line=='ret':flush()
        elif glyph is not None:current.append(line)
        else:raise ValueError(f'unaccounted instruction {name}: {line}')
    flush()
    sequences[name]=seq
if len(patterns)>255:raise ValueError('too many unique operators')
cycles=re.search(r'^\.equ CYCLES,\s*(\d+)',source,re.M)
if not cycles:raise ValueError('missing CYCLES')
initial=vals('phase');feedback=[vals('feedback'+str(i)) for i in range(1,5)]
if len(initial)!=4 or any(len(v)!=8 for v in feedback):raise ValueError('incorrect source seed dimensions')
u64=lambda n:str(n)+'ULL'
text='''/* Machine-translated directly from atlas_phase_feedback.S, not simulated. */
#include <stdint.h>
#include <stddef.h>
'''+f'#define CYCLES {cycles[1]}\n'+'''
static uint64_t phase[4],fb[4][8],reflected[4][8],answer[8],trace[CYCLES*64];
static uint32_t ntrace;
void *memcpy(void *d,const void *s,size_t n) { unsigned char *a=d;const unsigned char*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d; }
static void copy(uint64_t *d,const uint64_t*s,int n) { for(int i=0;i<n;++i)d[i]=s[i]; }
'''
text+='static const uint64_t init_phase[4]={'+','.join(map(u64,initial))+'};\n'
text+='static const uint64_t init_feedback[4][8]={'+','.join('{'+','.join(map(u64,v))+'}' for v in feedback)+'};\n'
text+='static void op(uint8_t id,uint64_t r[8],uint64_t *pa,uint8_t *pz) {uint64_t a=*pa,tmp;uint8_t z=*pz;switch(id){\n'
for i,body in enumerate(patterns):
    text+=f'case {i}:{{'+'\n'.join(map(instruction,body))+'break;}\n'
text+='default:__builtin_trap();}*pa=a;*pz=z;}\n'
for name,sequence in sequences.items():
    text+='static const uint8_t '+name+'['+str(len(sequence))+']={'+','.join(map(str,sequence))+'};\n'
text+='''static void execute(const uint8_t *seq,size_t len,uint64_t r[8],uint64_t a) {
 uint8_t z=0;for(size_t i=0;i<len;++i)op(seq[i],r,&a,&z);
}
#define EXEC(name,r,rax) execute(name,sizeof(name),r,rax)
static void snap(uint64_t *r) {copy(trace+ntrace,r,8);ntrace+=8;}
static void run(const uint64_t initial[4]) {
 copy(phase,initial,4);for(int c=0;c<4;++c)copy(fb[c],init_feedback[c],8);ntrace=0;
 uint64_t r[8];
 for(int cycle=0;cycle<CYCLES;++cycle){
  for(int c=0;c<4;++c){
   copy(r,fb[c],8);copy(r,phase,4);
   switch(c){case 0:EXEC(reflect_channel1,r,phase[3]);break;
    case 1:EXEC(reflect_channel2,r,phase[3]);break;
    case 2:EXEC(reflect_channel3,r,phase[3]);break;
    case 3:EXEC(reflect_channel4,r,phase[3]);break;}
   copy(reflected[c],r,8);snap(r);
  }
  for(int c=0;c<4;++c){
   int dest=(c+1)%4;copy(r,reflected[c],8);r[0]=r[6];
   switch(dest){case 0:EXEC(project_channel1,r,r[0]);break;
    case 1:EXEC(project_channel2,r,r[0]);break;
    case 2:EXEC(project_channel3,r,r[0]);break;
    case 3:EXEC(project_channel4,r,r[0]);break;}
   copy(fb[dest],r,8);snap(r);
  }
  for(int c=0;c<4;++c)phase[c]=fb[c][6];
 }
 copy(answer,fb[0],8);
}
__attribute__((export_name("run_reference"))) void run_reference(void) {run(init_phase);}
__attribute__((export_name("resolve"))) uint32_t resolve(uint32_t a,uint32_t b,uint32_t c,uint32_t d) {
 if((a|b|c|d)&~31u)return 1;
 uint64_t supplied[4]={a,b,c,d};run(supplied);return 0;
}
__attribute__((export_name("registers_ptr"))) uint32_t registers_ptr(void){return (uint32_t)(uintptr_t)answer;}
__attribute__((export_name("trace_ptr"))) uint32_t trace_ptr(void){return (uint32_t)(uintptr_t)trace;}
__attribute__((export_name("trace_words_count"))) uint32_t trace_words_count(void){return ntrace;}
'''
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(text)
print(f'{len(patterns)} unique operator bodies, '+','.join(f'{n}={len(s)}' for n,s in sequences.items())+'; '+str(len(text))+' generated bytes')
