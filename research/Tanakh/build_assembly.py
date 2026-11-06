"""Apply the Atlas numerical parser and archived operators to Hebrew gematria."""
import ast
import csv
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
ATLAS = Path(__file__).resolve().parents[2]
ARCHIVE = Path(r'C:\Users\ccoulter\Downloads\3I_ATLAS_six_recordings_four_stripes_asm.zip')
sys.path.insert(0, str(ATLAS / 'experiments/endpoint_phase_v1'))
from endpoint_phase import encode, numeral_table
from operator_machine import REGS, parse_source, reference, validate


def main():
    source = ROOT / 'tanakh_reconstructed.txt'
    raw = source.read_bytes()
    text = raw.decode('utf-8')
    # Explicit ordinary gematria convention. Final forms retain their source
    # identity but use their corresponding ordinary letter's numerical value.
    letters = 'אבגדהוזחטיכלמנסעפצקרשת'
    values = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]
    gematria = dict(zip(letters, values))
    for final, base in zip('ךםןףץ', 'כמנפצ'):
        gematria[final] = gematria[base]
    unknown = set(text) - set(gematria)
    if unknown:
        raise ValueError(f'Unmapped source characters: {unknown!r}')
    table_path = ATLAS / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py'
    table = numeral_table(table_path)
    with zipfile.ZipFile(ARCHIVE) as archive:
        members = sorted(n for n in archive.namelist() if n.endswith('.S'))
        ops, _ = parse_source(archive.read(members[0]).decode('utf-8'))
        for member in members[1:]:
            other, _ = parse_source(archive.read(member).decode('utf-8'))
            assert other == ops, 'Archive operator mappings disagree'
    validation_cases = validate(ops)
    mapped = {ch: encode(value, table) for ch, value in gematria.items()}
    assert all(len(glyph) == 1 and glyph in ops for glyph in mapped.values())
    state = dict.fromkeys(REGS, 1)
    rows = []
    full = ROOT / 'tanakh_atlas_gematria.S'
    preview = ROOT / 'tanakh_atlas_first100_expanded.S'
    header = ['# Generated using Hebrew gematria -> Atlas Greek numerals -> archived operators.',
              '# Every source letter is dispatched. Five-letter 2+3 roles remain an unexecuted hypothesis.',
              '.section .data', '.balign 8']
    for register in REGS:
        header.extend([f'{register}:', '    .quad 1'])
    header.extend(['.section .text', '.globl tanakh_transform', 'tanakh_transform:'])
    with full.open('w', encoding='utf-8', newline='\n') as f, preview.open('w', encoding='utf-8', newline='\n') as p:
        f.write('\n'.join(header[:header.index('.section .text')]) + '\n')
        for glyph, body in ops.items():
            f.write(f'.macro OP_{ord(glyph):04X}\n')
            f.write('\n'.join('    ' + line for line in body) + '\n.endm\n')
        f.write('.section .text\n.globl tanakh_transform\ntanakh_transform:\n')
        p.write('\n'.join(header) + '\n')
        for index, ch in enumerate(text):
            glyph = mapped[ch]
            if index % 10 == 0:
                f.write(f'FRAME_{index // 10}:\n')
            f.write(f'    OP_{ord(glyph):04X} # {index} {ch}={gematria[ch]} {glyph}\n')
            before = state.copy() if index < 100 else None
            reference(glyph, state)
            if index < 100:
                p.write(f'    # index={index} Hebrew={ch} value={gematria[ch]} Greek={glyph}\n')
                p.write('\n'.join('    ' + line for line in ops[glyph]) + '\n')
                rows.append({'index':index,'source':ch,'gematria':gematria[ch],
                             'greek':glyph,'candidate_5_symbol_role':'control' if index % 5 < 2 else 'data',
                             'before':before,'after':state.copy(),'assembly':ops[glyph]})
        f.write('    ret\n.section .note.GNU-stack,"",@progbits\n')
        p.write('    ret\n.section .note.GNU-stack,"",@progbits\n')
    with (ROOT / 'hebrew_greek_assembly_mapping.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f)
        w.writerow(['hebrew','codepoint','gematria','greek_numeral_operator','assembly'])
        for ch in sorted(gematria):
            w.writerow([ch,f'U+{ord(ch):04X}',gematria[ch],mapped[ch],'; '.join(ops[mapped[ch]])])
    (ROOT/'first100_assembly_trace.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report = {'source_sha256':hashlib.sha256(raw).hexdigest(),
              'parser_source':str(table_path),'archive':str(ARCHIVE),
              'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
              'mapping':gematria,'final_forms':'ordinary numerical values; exact source glyph preserved',
              'operators':'existing experimental Atlas machine implementations; Book II definitions not changed',
              'segmentation':'10 source letters per display frame; every letter executed; no instruction/data split imposed',
              'candidate_layout':'2 control + 3 data per five symbols annotated only in preview trace',
              'operator_validation_cases':validation_cases,'characters':len(text),
              'full_frames':len(text)//10,'trailing_letters':len(text)%10,
              'initial_registers':dict.fromkeys(REGS,1),'final_registers':state,
              'execution':'one forward pass using existing Atlas direct-reference interpreter; native assembly not run',
              'status':'experimental mapping and execution; not a recovered instruction format'}
    (ROOT/'assembly_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'characters':len(text),'operator_validation_cases':validation_cases,'first10_greek': ''.join(mapped[c] for c in text[:10]),'final_registers':state},ensure_ascii=True))


if __name__ == '__main__':
    main()
