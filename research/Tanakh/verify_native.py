import json
from pathlib import Path
import struct
import subprocess

root=Path(__file__).resolve().parent
linux='/mnt/' + root.drive[0].lower() + root.as_posix()[2:] + '/' 
def run(*args):
    return subprocess.run(['wsl','-d','Ubuntu','--exec',*args],check=True,capture_output=True).stdout
run('/usr/bin/as','--64','-o',linux+'native_entry.o',linux+'native_entry.S')
run('/usr/bin/ld','-o',linux+'tanakh_native',linux+'native_entry.o',linux+'tanakh_callable.o')
output=run(linux+'tanakh_native')
assert len(output)==64, len(output)
registers=['state','relations','constraints','observations','unresolved','context','target','events']
actual=dict(zip(registers,struct.unpack('<8Q',output)))
expected=json.loads((root/'assembly_report.json').read_text(encoding='utf-8'))['final_registers']
assert actual==expected,(actual,expected)
report={'status':'passed','native_output':actual,'matches_reference_evaluator':True,
        'method':'linked original assembled routine with Linux entry point; routine output emitted as eight little-endian uint64 cells'}
(root/'native_execution_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
