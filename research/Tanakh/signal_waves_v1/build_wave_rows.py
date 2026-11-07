"""Build the complete supplied Tanakh base stream and aligned child-wave rows."""
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from signal_builder import BuildSignal, CSV_COLUMNS
source=ROOT/'research/Tanakh/tanakh_reconstructed.txt'
raw=source.read_bytes()
signal=BuildSignal(raw.decode('utf-8'))
out=Path(__file__).resolve().parent
with (out/'wave_rows.jsonl').open('x',encoding='utf-8') as f:
    for row in signal.rows(): f.write(json.dumps(row,separators=(',',':'))+'\n')
report={'source':'research/Tanakh/tanakh_reconstructed.txt','source_sha256':hashlib.sha256(raw).hexdigest(),'source_characters':len(raw.decode('utf-8')),'base_points':len(signal.base),'child_points_per_wave':len(signal.sum_wave),'modulus':signal.modulus,'multiplier':signal.multiplier,'columns':CSV_COLUMNS,'alignment':'Adjacent mapped base values; anchored at first sample; final child values blank. Source indices are Unicode code-point offsets.','base_mapping':'Ordinary Hebrew gematria, final forms share ordinary values.','wave_formulas':{'sum':'(a+b)%231','linear':'(22*a+b)%231','product':'(a*b)%231'}}
with (out/'build_report.json').open('x') as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
