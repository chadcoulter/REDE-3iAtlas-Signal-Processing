import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';

const outputDir = path.dirname(fileURLToPath(import.meta.url));
const coreDir = path.resolve(outputDir, '../captured_aligned_core_pass100');
const registers = ['state','relations','constraints','observations','unresolved','context','target','events'];
const numeralValues = [[900,'Ϡ'],[800,'Ω'],[700,'Ψ'],[600,'Χ'],[500,'Φ'],[400,'Υ'],[300,'Τ'],[200,'Σ'],[100,'Ρ'],[90,'Ϟ'],[80,'Π'],[70,'Ο'],[60,'Ξ'],[50,'Ν'],[40,'Μ'],[30,'Λ'],[20,'Κ'],[10,'Ι'],[9,'Θ'],[8,'Η'],[7,'Ζ'],[6,'Ϛ'],[5,'Ε'],[4,'Δ'],[3,'Γ'],[2,'Β'],[1,'Α']].map(([n,g])=>[BigInt(n),g]);

function greek(value) {
  let n = BigInt(value);
  if (n === 0n) return '0';
  const chunks=[];
  while(n) {
    let group=n%1000n; n/=1000n;
    let word='';
    for(const [amount,glyph] of numeralValues) while(group>=amount) {word+=glyph;group-=amount;}
    chunks.push(word||'0');
  }
  return chunks.reverse().join(' | ');
}
const regRows=[['channel','register','decimal_string','hex_string','greek_numeric_encoding']];
const seqRows=[['channel','core_index','original_value_index','raw_integer_string','grouped_greek_numerals','operator_string']];
const byteRows=[['channel','byte_offset_hex','byte_count','machine_code_hex']];
const controls=[];
for(let channel=1;channel<=4;channel++) {
  const contextText=await fs.readFile(path.join(coreDir,`channel${channel}_core.context.json`),'utf8');
  const context=JSON.parse(contextText);
  // JSON's normal Number parsing would round uint64 values. Capture their
  // original decimal lexemes before converting to BigInt or spreadsheet text.
  const registerBlock=contextText.match(/"native_core_exit_state":\s*\{([^}]+)\}/s)[1];
  for(const register of registers) {
    const decimal=registerBlock.match(new RegExp('"'+register+'":\\s*(\\d+)'))[1];
    regRows.push([channel,register,decimal,'0x'+BigInt(decimal).toString(16).padStart(16,'0'),greek(decimal)]);
  }
  const source=await fs.readFile(path.join(coreDir,`channel${channel}_core.S`),'utf8');
  const markers=[...source.matchAll(/^ # traversal_index=(\d+) raw_integer=(\d+) numerals=([^\n]*)$/gm)];
  if(markers.length!==1934) throw new Error('Wrong retained sequence length');
  for(let i=0;i<markers.length;i++) {
    const marker=markers[i];
    const end=i+1<markers.length?markers[i+1].index:source.indexOf('transform_core_end:');
    const operators=[...source.slice(marker.index,end).matchAll(/^ # operator=(.)$/gm)].map(m=>m[1]).join('');
    const numeric=greek(marker[2]);
    if(numeric!==marker[3].trim()) throw new Error('Numeral encoding mismatch');
    seqRows.push([channel,i,Number(marker[1]),marker[2],numeric,operators]);
  }
  const bytes=await fs.readFile(path.join(coreDir,`channel${channel}_core.code.bin`));
  const hash=crypto.createHash('sha256').update(bytes).digest('hex');
  if(hash!==context.files['.code.bin'].sha256) throw new Error('Machine code hash mismatch');
  for(let offset=0;offset<bytes.length;offset+=32) {
    const chunk=bytes.subarray(offset,offset+32);
    byteRows.push([channel,'0x'+offset.toString(16).padStart(8,'0'),chunk.length,'0x'+chunk.toString('hex')]);
  }
  controls.push({channel,core_values:markers.length,machine_code_bytes:bytes.length,machine_code_sha256:hash});
}

function csvCell(value) {
  const text=String(value??'');
  return /[",\r\n]/.test(text)?'"'+text.replaceAll('"','""')+'"':text;
}
async function exportCsv(name, rows, widths) {
  const target=path.join(outputDir,name+'.csv');
  try {await fs.access(target);throw new Error('Refusing to overwrite '+target);} catch(error) {if(error.code!=='ENOENT') throw error;}
  const workbook=Workbook.create();
  const sheet=workbook.worksheets.add('Data');
  sheet.showGridLines=false;
  sheet.getRangeByIndexes(0,0,rows.length,rows[0].length).values=rows;
  const header=sheet.getRangeByIndexes(0,0,1,rows[0].length);
  header.format.fill='#24364B';
  header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
  sheet.getRangeByIndexes(1,0,rows.length-1,rows[0].length).format.font={name:'Arial',size:10};
  for(let c=0;c<widths.length;c++) sheet.getRangeByIndexes(0,c,Math.min(rows.length,8),1).format.columnWidthPx=widths[c];
  workbook.recalculate();
  const matrix=sheet.getRangeByIndexes(0,0,rows.length,rows[0].length).values;
  for(let r=0;r<rows.length;r++) for(let c=0;c<rows[0].length;c++) if(String(matrix[r][c]??'')!==String(rows[r][c]??'')) throw new Error(`Cell changed: ${name} ${r},${c}`);
  const inspected=await workbook.inspect({kind:'table',range:`Data!A1:${String.fromCharCode(64+rows[0].length)}4`,include:'values',tableMaxRows:4,tableMaxCols:rows[0].length,maxChars:1200});
  console.log(inspected.ndjson);
  // CSV export is a direct serialization of the verified Artifact Tool grid;
  // uint64 decimal and hex strings never pass through floating-point values.
  const text='\ufeff'+matrix.map(row=>row.map(csvCell).join(',')).join('\r\n')+'\r\n';
  await fs.writeFile(target,text,{encoding:'utf8',flag:'wx'});
  const preview=await workbook.render({sheetName:'Data',range:`A1:${String.fromCharCode(64+rows[0].length)}5`,scale:1,format:'png'});
  await fs.writeFile(path.join(outputDir,name+'_preview.png'),new Uint8Array(await preview.arrayBuffer()),{flag:'wx'});
  console.log(JSON.stringify({file:target,data_rows:rows.length-1}));
}
await exportCsv('core_output',regRows,[75,135,215,190,465]);
await exportCsv('core_transform_sequence',seqRows,[75,95,150,230,400,400]);
await exportCsv('core_machine_code',byteRows,[75,150,100,650]);
await fs.writeFile(path.join(outputDir,'export_controls.json'),JSON.stringify({register_rows:regRows.length-1,sequence_rows:seqRows.length-1,machine_code_rows:byteRows.length-1,channels:controls},null,2),{flag:'wx'});
