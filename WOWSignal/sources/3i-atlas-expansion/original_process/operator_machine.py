"""Replay archived experimental operators; test an explicitly inferred 3F/6R schedule.

Reads assembly as data. Does not compile or run downloaded binaries.
Reverse means reverse frame AND glyph order, not inverse arithmetic.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import zipfile
from pathlib import Path

MASK = (1 << 64) - 1
REGS = ['state', 'relations', 'constraints', 'observations',
        'unresolved', 'context', 'target', 'events']


def parse_source(text):
    operators = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.fullmatch(r'\s*# (\S) ([A-Z]+)\s*', line)
        if not match or match[1] in operators:
            continue
        body = []
        for following in lines[i + 1:]:
            if following.strip().startswith('#') or following.startswith('FRAME_'):
                break
            if following.strip():
                body.append(following.strip())
        operators[match[1]] = body
    frames = []
    for section in re.split(r'(?m)^FRAME_\d+:\s*$', text)[1:]:
        glyphs = re.findall(r'(?m)^\s*# (\S) [A-Z]+\s*$', section)
        if not glyphs:
            raise ValueError('Frame without glyphs')
        frames.append(glyphs)
    return operators, frames


def execute(body, state):
    """Strict interpreter for the small x86-64 instruction subset in the archive."""
    cpu = {'%rax': 0}
    zero = False
    labels = {line[:-1]: i for i, line in enumerate(body) if line.endswith(':')}

    def read(operand):
        if operand.startswith('$'):
            return int(operand[1:]) & MASK
        if operand in cpu:
            return cpu[operand]
        match = re.fullmatch(r'(\w+)\(%rip\)', operand)
        if match and match[1] in state:
            return state[match[1]]
        raise ValueError(f'Unsupported operand {operand}')

    def write(operand, value):
        value &= MASK
        if operand == '%rax':
            cpu[operand] = value
        elif operand == '%al':
            cpu['%rax'] = (cpu['%rax'] & ~255) | (value & 255)
        else:
            match = re.fullmatch(r'(\w+)\(%rip\)', operand)
            if not match or match[1] not in state:
                raise ValueError(f'Unsupported destination {operand}')
            state[match[1]] = value

    pc = 0
    while pc < len(body):
        line = body[pc]
        pc += 1
        if line.endswith(':'):
            continue
        mnemonic, operands = line.split(None, 1)
        args = [part.strip() for part in operands.split(',')]
        if mnemonic in ('jz', 'jmp'):
            if mnemonic == 'jmp' or zero:
                pc = labels[args[0][:-1]] + 1
        elif mnemonic == 'incq':
            write(args[0], read(args[0]) + 1)
        elif mnemonic == 'sete':
            write(args[0], int(zero))
        elif mnemonic == 'movzbq':
            if args != ['%al', '%rax']:
                raise ValueError(line)
            write('%rax', cpu['%rax'] & 255)
        elif mnemonic in ('movq', 'addq', 'xorq', 'andq', 'cmpq', 'testq', 'xchgq'):
            a = read(args[0])
            if mnemonic == 'movq':
                write(args[1], a)
                continue
            b = read(args[1])
            if mnemonic == 'addq': write(args[1], a + b)
            elif mnemonic == 'xorq': write(args[1], a ^ b)
            elif mnemonic == 'andq': write(args[1], a & b)
            elif mnemonic == 'cmpq': zero = a == b
            elif mnemonic == 'testq': zero = not (a & b)
            elif mnemonic == 'xchgq':
                write(args[0], b)
                write(args[1], a)
        else:
            raise ValueError(f'Unsupported instruction: {line}')


def reference(glyph, s):
    """Independent direct translation used to check the assembly interpreter."""
    code = ord(glyph)
    if code == 0x3a3: s['state'] += s['relations'] + 1
    elif code == 0x39e: s['unresolved'] += s['state'] ^ s['target']
    elif code == 0x396: s['relations'] ^= s['state']
    elif code == 0x39f: s['observations'] += s['state'] ^ s['relations']
    elif code == 0x393: s['constraints'] = s['state'] & 255
    elif code == 0x3a0: s['target'] = s['state'] + s['context']
    elif code == 0x3da: s['unresolved'] += 1
    elif code == 0x3a7: s['state'], s['target'] = s['target'], s['state']
    elif code == 0x399: s['events'] += 1
    elif code == 0x395: s['observations'] += int(s['constraints'] == 0)
    elif code == 0x3a4: s['target'] = s['state'] + s['relations'] + s['constraints']
    elif code in (0x39a, 0x3e0, 0x392): s['context'] += 1
    elif code == 0x398: s['constraints'] += 1
    elif code == 0x394: s['state'] += 1
    elif code == 0x3de: s['relations'] ^= s['events']
    elif code == 0x391: s['state'] = 1
    elif code == 0x3a8: s['context'] = s['observations'] ^ s['relations']
    elif code == 0x39c: s['observations'] += s['state']
    elif code == 0x397: s['target'] = s['state']
    elif code == 0x3a9: s['state'] = s['target']
    elif code == 0x39d: s['target'] = s['state'] + 1
    elif code == 0x3a1: s['relations'] ^= s['target']
    elif code == 0x3a6: s['target'] = s['state'] ^ s['context']
    elif code == 0x3a5: s['context' if s['constraints'] & 1 else 'relations'] += 1
    elif code == 0x39b: s['state'] ^= s['relations']
    else: raise ValueError(f'No independent translation for {glyph!r}')
    for key in s: s[key] &= MASK


def validate(ops):
    rng = random.Random(20261026)
    seeds = [{k: n for k in REGS} for n in (0, 1, 2, 255, MASK)]
    seeds += [{k: rng.getrandbits(64) for k in REGS} for _ in range(100)]
    for glyph, body in ops.items():
        for seed in seeds:
            actual, expected = seed.copy(), seed.copy()
            execute(body, actual)
            reference(glyph, expected)
            if actual != expected:
                raise AssertionError((glyph, seed, actual, expected))
    return len(ops) * len(seeds)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=1)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    endpoints, selections, sources = [], [], []
    checks = 0
    with zipfile.ZipFile(args.archive) as archive:
        for member in archive.namelist():
            if not member.endswith('.S'): continue
            raw = archive.read(member)
            ops, frames = parse_source(raw.decode('utf-8'))
            checks += validate(ops)
            state = {k: args.seed & MASK for k in REGS}
            sources.append({'member': member, 'sha256': hashlib.sha256(raw).hexdigest(),
                            'frames': len(frames), 'glyphs': sum(map(len, frames)),
                            'registers': REGS, 'operator_count': len(ops)})
            # One forward block and two reverse blocks. All registers carry across.
            for block, direction in enumerate(('forward', 'reverse', 'reverse'), 1):
                ordered = frames if direction == 'forward' else [f[::-1] for f in frames[::-1]]
                for within in range(1, 4):
                    before = state.copy()
                    for frame in ordered:
                        for glyph in frame: execute(ops[glyph], state)
                    row = {'source': member, 'block': block, 'direction': direction,
                           'pass_in_block': within, 'pass_total': (block - 1) * 3 + within,
                           **state, 'changed_registers': sum(before[k] != state[k] for k in REGS)}
                    endpoints.append(row)
                    if within == 3:
                        selections.append(row.copy())
    for name, rows in [('pass_endpoints.csv', endpoints), ('three_block_outputs.csv', selections)]:
        with (args.output / name).open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    report = {
        'status': 'candidate schedule, not recovered wiring',
        'schedule': '3 forward passes -> snapshot; 3 reverse -> snapshot; 3 reverse -> snapshot',
        'feedback': 'All eight registers carried through all nine passes, including direction change.',
        'seed': args.seed,
        'reverse': 'Reverse frame and glyph order; original arithmetic, not algebraic inversion.',
        'scalar_selection': 'Undetermined. Full register snapshots retained; target is only a candidate scalar.',
        'operator_validation_cases': checks,
        'validation_scope': 'Independent direct translations agree on boundary and randomized register states; no native binary run.',
        'sources': sources,
        'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
        'important_difference': 'Archived four-stream sources use unresolved; saved IF1_B1 traces use pattern and depend on a different assembly file.',
        'interpretation': 'Outputs are computed feedback states. No additional source measurements or recovered signal information established.',
    }
    (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'validation_cases': checks, 'pass_endpoints': len(endpoints),
                      'block_outputs': len(selections), 'output': str(args.output)}))


if __name__ == '__main__': main()
