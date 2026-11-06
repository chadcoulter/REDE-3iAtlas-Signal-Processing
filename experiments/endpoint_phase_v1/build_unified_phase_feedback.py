"""Build a self-contained GNU x86-64 assembly phase-feedback program."""
from pathlib import Path
import json, zipfile, hashlib
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'unified_phase_feedback'
REGS = ('state','relations','constraints','observations','unresolved','context','target','events')

def main():
    OUT.mkdir(exist_ok=False)
    report = json.loads((ROOT/'rotated_phase_feedback_100_results/phase_feedback_report.json').read_text())
    lines = ['# Four-channel reflection/projection with cyclic n+1 handoff.',
             '# GNU as, Linux x86-64. No input files or external dependencies.',
             '# stdout: 8 little-endian uint64 words per execution; 8 executions/cycle.',
             '# Reflection order 1,2,3,4; projection destination order 2,3,4,1.',
             '.equ CYCLES, 100', '.section .data', '.balign 8', 'phase:',
             '.quad '+','.join(report['initial_phase'])]
    for channel, bank in enumerate(report['initial_feedback_registers'],1):
        lines += [f'feedback{channel}:', '.quad '+','.join(bank[r] for r in REGS)]
    lines += ['.section .bss', '.balign 8']
    for r in REGS: lines += [r+': .skip 8']
    for c in range(1,5): lines += [f'reflected{c}: .skip 64']
    lines += ['.section .text','.globl _start','.type _start,@function','_start:', 'movq $CYCLES, %r12', 'cycle_loop:']
    def copy(src,dst):
        return [f'leaq {src}(%rip), %rsi', f'leaq {dst}(%rip), %rdi', 'movq $8, %rcx', 'rep movsq']
    for c in range(1,5):
        lines += [f'# Reflect channel {c}; phase overwrites the first four cells.']
        lines += copy(f'feedback{c}','state')
        for i,r in enumerate(REGS[:4]): lines += [f'movq phase+{i*8}(%rip), %rax',f'movq %rax, {r}(%rip)']
        lines += [f'call reflect_channel{c}'] + copy('state',f'reflected{c}') + ['call emit_registers']
    for c in range(1,5):
        dest = c%4+1
        lines += [f'# Turn {c} -> {dest}: preserve all cells except state <- target.']
        lines += copy(f'reflected{c}','state')
        lines += ['movq target(%rip), %rax','movq %rax, state(%rip)',f'call project_channel{dest}']
        lines += copy('state',f'feedback{dest}') + ['call emit_registers']
    for c in range(1,5): lines += [f'movq feedback{c}+48(%rip), %rax',f'movq %rax, phase+{(c-1)*8}(%rip)']
    lines += ['decq %r12','jnz cycle_loop','movq $60, %rax','xorq %rdi, %rdi','syscall',
              'emit_registers:', 'leaq state(%rip), %rsi','movq $64, %rdx','emit_more:',
              'movq $1, %rax','movq $1, %rdi','syscall','cmpq $-4, %rax','je emit_more',
              'testq %rax, %rax','jle output_failed','addq %rax, %rsi','subq %rax, %rdx',
              'jnz emit_more','ret','output_failed:','movq $60, %rax','movq $1, %rdi','syscall']
    bodies = []
    with zipfile.ZipFile(ROOT/'rotated_phase_feedback_100_results/assembled_sources.zip') as z:
        for direction, prefix in [('x_to_y','reflect'),('y_to_x','project')]:
            for c in range(1,5):
                name = f'cycle001_{direction}_channel{c}.S'
                source = z.read(name).decode()
                body = source.split('_start:\n',1)[1].split(' movq $1,%rax\n',1)[0]
                assert 'syscall' not in body
                lines += [f'.type {prefix}_channel{c},@function',f'{prefix}_channel{c}:',body,'ret']
                bodies.append({'routine':f'{prefix}_channel{c}','archive_member':name,'body_sha256':hashlib.sha256(body.encode()).hexdigest()})
    lines += ['.section .note.GNU-stack,"",@progbits','']
    (OUT/'atlas_phase_feedback.S').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    (OUT/'source_provenance.json').write_text(json.dumps(bodies,indent=2)+'\n')
    print('Created single assembly source with eight routines and runtime feedback loop.')

if __name__ == '__main__': main()
