"""Verify every CSV point against the unchanged source and wave equations."""
from pathlib import Path
import csv,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from signal_parser import SignalParser
out=Path(__file__).resolve().parent
source=(ROOT/'research/Tanakh/tanakh_reconstructed.txt').read_bytes()
text=source.decode('utf-8')
base=[(i,SignalParser.HEBREW_GEMATRIA[g]) for i,g in enumerate(text) if g in SignalParser.HEBREW_GEMATRIA]
count=0
with (out/'signal_waves.csv').open(encoding='utf-8',newline='') as f:
    for i,row in enumerate(csv.DictReader(f)):
        position,a=base[i]
        assert (int(row['sample_index']),int(row['source_index']),int(row['base_value']))==(i,position,a)
        if i+1<len(base):
            next_position,b=base[i+1]
            expected=(next_position,b,(a+b)%231,(22*a+b)%231,(a*b)%231)
            assert tuple(int(row[k]) for k in ('next_source_index','next_base_value','sum_wave','linear_wave','product_wave'))==expected,i
        else:
            assert all(row[k]=='' for k in ('next_source_index','next_base_value','sum_wave','linear_wave','product_wave'))
        count+=1
assert count==len(base)
report=json.loads((out/'build_report.json').read_text())
assert hashlib.sha256(source).hexdigest()==report['source_sha256']
result={'all_points_verified':True,'base_points':count,'child_samples_per_wave':count-1,'source_sha256':report['source_sha256'],'csv_sha256':hashlib.sha256((out/'signal_waves.csv').read_bytes()).hexdigest(),'final_child_samples_blank':True}
with (out/'verification.json').open('x') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
