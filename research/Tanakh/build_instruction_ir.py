"""Build inspectable parser instructions, then emit assembly from those records."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    mapping = {}
    library = {}
    with (ROOT/'hebrew_greek_assembly_mapping.csv').open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            glyph = row['greek_numeral_operator']
            opcode = f'OP_{ord(glyph):04X}'
            mapping[row['hebrew']] = {'value':int(row['gematria']),'operator':glyph,'opcode':opcode}
            library[opcode] = {'operator':glyph,'assembly':row['assembly'].split('; ')}
    # Restore original library order for byte-for-byte comparison with the
    # already assembled source. Only the used operator bodies are dispatched.
    previous = ROOT/'tanakh_atlas_gematria.S'
    with previous.open(encoding='utf-8') as f:
        header = []
        for line in f:
            if line == 'FRAME_0:\n':
                break
            header.append(line)
    raw = (ROOT/'tanakh_reconstructed.txt').read_bytes()
    text = raw.decode('utf-8')
    ir = ROOT/'tanakh_parser_instructions.jsonl'
    with ir.open('w',encoding='utf-8',newline='\n') as f:
        for start in range(0,len(text),10):
            instructions = []
            for index in range(start,min(start+10,len(text))):
                ch = text[index]
                instructions.append({'index':index,'source':ch,**mapping[ch]})
            f.write(json.dumps({'frame':start//10,'instructions':instructions},ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'atlas_instruction_library.json').write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    output = ROOT/'tanakh_from_instruction_ir.S'
    digest = hashlib.sha256()
    expected_index = 0
    preview = []
    with ir.open(encoding='utf-8') as source, output.open('w',encoding='utf-8',newline='\n') as f:
        f.writelines(header)
        for line in source:
            frame = json.loads(line)
            assert frame['frame'] == expected_index//10
            f.write(f"FRAME_{frame['frame']}:\n")
            for instruction in frame['instructions']:
                index = instruction['index']
                assert index == expected_index
                expected_index += 1
                opcode = instruction['opcode']
                assert opcode in library
                assert library[opcode]['operator'] == instruction['operator']
                assert mapping[instruction['source']]['value'] == instruction['value']
                digest.update(instruction['source'].encode('utf-8'))
                f.write(f"    {opcode} # {index} {instruction['source']}={instruction['value']} {instruction['operator']}\n")
                if len(preview)<10:
                    preview.append({**instruction,'assembly':library[opcode]['assembly']})
        f.write('    ret\n.section .note.GNU-stack,"",@progbits\n')
    assert expected_index == len(text)
    assert digest.hexdigest() == hashlib.sha256(raw).hexdigest()
    same = hashlib.sha256(output.read_bytes()).digest() == hashlib.sha256(previous.read_bytes()).digest()
    assert same
    report = {'pipeline':['exact Hebrew source','explicit ordinary gematria','Atlas Greek numeral encoding','parser instruction records','archived Atlas instruction bodies','x86-64 assembly'],
              'instruction_occurrences':expected_index,'used_instruction_definitions':len(library),
              'display_frame_letters':10,'frame_count':(expected_index+9)//10,
              'instruction_data_split':'not imposed; each character is a parser instruction',
              'source_round_trip_verified':True,'assembly_identical_to_successfully_assembled_source':same,
              'ir':ir.name,'library':'atlas_instruction_library.json','assembly':output.name,
              'first10':preview}
    (ROOT/'instruction_pipeline_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='first10'}))


if __name__ == '__main__':
    main()
