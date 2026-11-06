"""Compare every native register from the unified program with the saved run."""
from pathlib import Path
import json, struct, hashlib
ROOT = Path(__file__).resolve().parent
OUT = ROOT/'unified_phase_feedback'
REGS = ('state','relations','constraints','observations','unresolved','context','target','events')
records = json.loads((ROOT/'rotated_phase_feedback_100_results/execution_trace.json').read_text())
data = (OUT/'execution_registers.bin').read_bytes()
assert len(records) == 800 and len(data) == 800*64
for index, record in enumerate(records):
    block = data[index*64:(index+1)*64]
    assert block.hex() == record['output_hex'], record['id']
    actual = dict(zip(REGS,map(str,struct.unpack('<8Q',block))))
    assert actual == record['native_ending_registers'], record['id']
last_cycle = records[-8:]
phase = [next(r['native_ending_registers']['target'] for r in last_cycle if r['direction']=='y_to_x' and r['channel_one_based']==c) for c in range(1,5)]
result = {'cycles':100,'executions_compared':800,'register_words_compared':6400,'all_registers_match':True,'native_output_bytes':len(data),'output_sha256':hashlib.sha256(data).hexdigest(),'final_phase':phase}
with (OUT/'verification.json').open('x') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
