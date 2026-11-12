"""Execute recovered Atlas machine operations, checking its native trace first.

The instruction translator accepts only the recovered x86 subset, unsigned
64-bit arithmetic, and its one local branch shape. Unknown code fails closed.
Default execution prints reference verification; --output NEW_DIR records the
scoped Wow experiment and appends its checkpoint to the working text.
"""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import time

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'WOWSignal/sources/3i-atlas-expansion'
BASE = ROOT / 'WOWSignal/steps/03-hebrew-gematria/run-001'
REGS = 'state relations constraints observations unresolved context target events'.split()
MASK = (1 << 64) - 1
EXPECTED = 'e38685a723b769cbb1a573bf8accab0f9064b40d49773b0c5feed16016658d5e'
MARKER = 'Original Atlas circuit recovered — scoped machine-execution trial001'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def operand(value):
    if value == '%rax':
        return 'a'
    if re.fullmatch(r'\$\d+', value):
        return str(int(value[1:]))
    m = re.fullmatch(r'(\w+)\(%rip\)', value)
    if m and m[1] in REGS:
        return f'r[{REGS.index(m[1])}]'
    raise ValueError('Unsupported operand: ' + value)


def statement(line):
    op, rest = line.split(None, 1)
    if op == 'incq':
        y = operand(rest)
        return [f'{y}=({y}+1)&MASK', f'z=({y}==0)']
    if op == 'sete' and rest == '%al':
        return ['a=(a&(~255&MASK))|int(z)']
    if op == 'movzbq' and rest == '%al, %rax':
        return ['a=a&255']
    parts = rest.split(', ')
    if len(parts) != 2:
        raise ValueError('Unsupported instruction: ' + line)
    x, y = map(operand, parts)
    if y.isdecimal():
        raise ValueError('Immediate destination')
    if op == 'movq':
        return [f'{y}={x}']
    if op in ('addq', 'xorq', 'andq'):
        symbol = {'addq':'+', 'xorq':'^', 'andq':'&'}[op]
        return [f'{y}=({y}{symbol}{x})&MASK', f'z=({y}==0)']
    if op == 'cmpq':
        return [f'z=({y}=={x})']
    if op == 'testq':
        return [f'z=(({y}&{x})==0)']
    if op == 'xchgq':
        return [f'tmp={x}', f'{x}={y}', f'{y}=tmp']
    raise ValueError('Unsupported instruction: ' + line)


def compile_body(body):
    lines = ['def apply(r,a,z):']
    def emit(seq, indent):
        for line in seq:
            for st in statement(line):
                lines.append(' '*indent + st)
    if 'jz 1f' in body:
        j = body.index('jz 1f'); jump = body.index('jmp 2f')
        one = body.index('1:'); two = body.index('2:')
        assert j < jump < one < two and two == len(body)-1
        emit(body[:j],4)
        lines.append('    if z:')
        emit(body[one+1:two],8)
        lines.append('    else:')
        emit(body[j+1:jump],8)
    else:
        emit(body,4)
    lines.append('    return a,z')
    code = '\n'.join(lines)+'\n'; scope = {'MASK':MASK}
    exec(compile(code,'<whitelisted Atlas instructions>','exec'),scope)
    return scope['apply'], code


def load():
    data = (SOURCE/'atlas_phase_feedback.S').read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == 'f599e1793e856c5023c42976ae3e1b0e2dbb8d90'
    source = data.decode('utf-8')
    def vals(name):
        return [int(x) for x in re.search(r'^'+name+r':\s*\n\.quad ([^\n]+)',source,re.M)[1].split(',')]
    phase = vals('phase'); feedback = [vals('feedback'+str(i)) for i in range(1,5)]
    names = [f'{m}_channel{i}' for m in ('reflect','project') for i in range(1,5)]
    bodies = {}; sequences = {}
    for i,name in enumerate(names):
        start = re.search(r'^'+name+':',source,re.M).end()
        end = re.search(r'^'+names[i+1]+':',source,re.M).start() if i < 7 else len(source)
        seq=[]; current=None; instructions=[]
        def flush():
            nonlocal current,instructions
            if current is not None:
                body=tuple(instructions)
                assert body and (current not in bodies or bodies[current] == body)
                bodies[current]=body;seq.append(current)
            current=None;instructions=[]
        for line in source[start:end].splitlines():
            st=line.strip()
            if st.startswith('# operator='):
                flush();current=st.split('=',1)[1]
            elif st.startswith('# traversal_index=') or st=='ret':
                flush()
            elif st and not st.startswith(('#','.')):
                if current is None:
                    raise ValueError('Unaccounted code: '+st)
                instructions.append(st)
        flush();sequences[name]=seq
    compiled={}; operators={}
    for glyph,body in bodies.items():
        compiled[glyph],code=compile_body(body)
        operators[glyph]={'assembly':list(body),'translated_python':code}
    assert 'Ϛ' in compiled and 'Ϝ' not in compiled
    return phase,feedback,sequences,compiled,operators


def circuit(phase,feedback,sequences,compiled):
    phase=list(phase);fb=copy.deepcopy(feedback);trace=[]
    chains={name:[compiled[g] for g in seq] for name,seq in sequences.items()}
    def run(name,r,a):
        z=False
        for op in chains[name]:
            a,z=op(r,a,z)
    for cycle in range(1,101):
        reflected=[]
        for c in range(4):
            r=fb[c].copy();r[:4]=phase
            run('reflect_channel'+str(c+1),r,phase[3]);reflected.append(r.copy())
            trace.append({'cycle':cycle,'stage':'reflect','channel':c+1,'values':r.copy()})
        for c in range(4):
            dest=(c+1)%4;r=reflected[c].copy();r[0]=r[6]
            run('project_channel'+str(dest+1),r,r[0]);fb[dest]=r.copy()
            trace.append({'cycle':cycle,'stage':'project','channel':dest+1,'values':r.copy()})
        phase=[fb[c][6] for c in range(4)]
    raw=b''.join(struct.pack('<8Q',*row['values']) for row in trace)
    return trace,raw,phase


def run(output):
    start=time.monotonic();phase,feedback,sequences,compiled,operators=load()
    ref_trace,ref_bytes,ref_phase=circuit(phase,feedback,sequences,compiled)
    assert len(ref_bytes)==51200 and sha(ref_bytes)==EXPECTED, ('Native parity failed',sha(ref_bytes))
    print('PASS: original 6400-word trace matches pinned native SHA256.',flush=True)
    if output is None:
        return
    assert not output.exists(), 'Use a fresh output directory'
    grid=json.loads((BASE/'hebrew_grid.json').read_text(encoding='utf-8'))['grid']
    tokens=[grid[r][1] for r in range(57,61)]
    assert tokens==['ו','יד','כו','ל']
    trials={'reference':(phase,ref_trace,ref_bytes,ref_phase)}
    for name,inputs in [('wow_forward',[6,14,26,30]),('wow_reverse',[30,26,14,6]),('zero_phase',[0,0,0,0])]:
        trace,raw,final=circuit(inputs,feedback,sequences,compiled)
        trials[name]=(inputs,trace,raw,final)
        print(name,'SHA256',sha(raw),'final phase',final,flush=True)
    # Apply recovered ORIGINAL operator bodies directly to ONLY scoped codes.
    scoped='ϚΙΔΚϚΛ';short=[]
    for direction,seq in [('forward',scoped),('reverse',scoped[::-1])]:
        r=[1]*8
        for pass_number in range(1,4):
            a=0;z=False
            for i,glyph in enumerate(seq,1):
                before=r.copy();a,z=compiled[glyph](r,a,z)
                short.append({'direction':direction,'pass':pass_number,'step':i,'glyph':glyph,'before':before,'after':r.copy()})
    output.mkdir(parents=True)
    summaries={}
    for name,(inputs,trace,raw,final) in trials.items():
        (output/(name+'.u64le')).write_bytes(raw)
        other=trials['reference'][1]
        different=[i for i,(x,y) in enumerate(zip(trace,other)) if x['values']!=y['values']]
        summaries[name]={'inputs':inputs,'trace_sha256':sha(raw),'snapshots':len(trace),
                         'final_phase':final,'last_registers':dict(zip(REGS,trace[-1]['values'])),
                         'snapshots_different_from_reference':len(different),
                         'last_different_snapshot':different[-1]+1 if different else None}
    with (output/'circuit_trace.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['trial','cycle','stage','channel']+REGS)
        for name,(_,trace,_,_) in trials.items():
            for row in trace:writer.writerow([name,row['cycle'],row['stage'],row['channel']]+row['values'])
    ledger={'source_manifest':'WOWSignal/sources/3i-atlas-expansion/source_manifest.json',
            'native_reference_match':True,'expected_native_sha256':EXPECTED,
            'source_assembly_sha256':sha((SOURCE/'atlas_phase_feedback.S').read_bytes()),
            'runner_sha256':sha(Path(__file__).read_bytes()),'registers':REGS,
            'scope':{'display':'וידכ | ול','source_tokens':tokens,'source_bins':[6,14,26,30],
                     'rows':[58,61],'channel':2,'outside_unchanged':'יטה'},
            'mapping_correction':'Original compiler uses Ϛ for6. The earlier Ϝ retention trial is retained as a different method.',
            'operators':operators,'chain_operator_counts':{n:len(v) for n,v in sequences.items()},
            'trials':summaries,'scoped_original_operator_trace':short,
            'external_contributions':'Full circuit retains all original Atlas operator chains and four original feedback banks. Only its four initial phase cells change. Generated states are NOT exclusively Wow-derived payload.',
            'input_adapter':'Place four source bins into the four initial phase cells, as in the recovered Talking Comet input adapter. This is an experimental input adapter, not an original Wow decoder.',
            'scope_only_operator_run':'Apply only the six scoped codes using recovered operator bodies; seed all eight registers1, three feedback passes per direction, as in the earlier trace procedure.',
            'payload_status':'No source-selected register-to-message extraction rule has been recovered. Register values are generated computational states, not recovered letters.',
            'seconds':round(time.monotonic()-start,3)}
    (output/'results.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    target=BASE/'hebrew_streams_updated.txt';before=target.read_bytes()
    assert MARKER not in before.decode('utf-8') and before.startswith((BASE/'hebrew_streams.txt').read_bytes())
    section='\n\n'+'='*60+'\n'+MARKER+'\n\n'
    section+='Recovered exact pinned original reflection/projection circuit. The 6400-register-word reference trace matches its recorded native hash. This replaces the prior assumption that the original process was unavailable.\n'
    section+='Only scoped Wow inputs6,14,26,30 are supplied; יטה remains unchanged. The full-circuit trial also retains original Atlas chains and feedback banks, recorded as external contributions.\n'
    section+='Original compiler map: ו | יד | כו | ל = Ϛ | ΙΔ | ΚϚ | Λ. Numeric6 invokes original unresolvedness machine operation, not the previous Digamma retention operation.\n'
    section+='Recovered four-stage cycle: load phase into first4 registers; reflect each channel; set state from target; project to next channel; next phase equals four returned targets. Repeat100 cycles.\n'
    section+='The direct scoped-code run and full original-circuit trials are different experiments. No generated register or re-encoded numeral is promoted to a missing letter without a source-supported extraction rule.\n'
    section+='Original theory notes describe State, Generative and Reflective functions and projected missing information; they do not provide a complete payload decoder or precise reconstruction-validation test. Their original files and hashes are preserved.\n'
    section+='Complete ledger and trace: '+str(output.relative_to(ROOT)).replace('\\','/')+'\n\n'+json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    target.write_bytes(before+section.encode('utf-8'));assert target.read_bytes().startswith(before)
    print(json.dumps({'output':str(output),'native_parity':True,'trials':summaries,
                      'short_pass_finals':[x for x in short if x['step']==6],
                      'prior_working_text_preserved':True},ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();run(args.output.resolve() if args.output else None)
