import fs from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import readline from 'node:readline';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {Workbook} from '@oai/artifact-tool';
const root=path.dirname(fileURLToPath(import.meta.url));
const report=JSON.parse(await fs.readFile(path.join(root,'build_report.json'),'utf8'));
const workbook=Workbook.create();
const sheet=workbook.worksheets.add('Waves');
const header=report.columns;
sheet.getRange('A1:H1').values=[header];
const target=await fs.open(path.join(root,'signal_waves.csv'),'wx');
await target.write(header.join(',')+'\r\n');
let rows=[],count=0,first=true;
async function flush(){
  if(!rows.length)return;
  const range=sheet.getRangeByIndexes(1,0,rows.length,8);
  range.values=rows;
  workbook.recalculate();
  const actual=range.values;
  for(let i=0;i<rows.length;i++)for(let j=0;j<8;j++)if((actual[i][j]??null)!==(rows[i][j]??null))throw new Error(`Cell changed ${count+i},${j}`);
  await target.write(actual.map(r=>r.map(v=>v??'').join(',')).join('\r\n')+'\r\n');
  if(first){
    sheet.getRange('A1:H6').format.columnWidthPx=145;
    sheet.getRange('A1:H1').format.font={bold:true,color:'#FFFFFF'};
    sheet.getRange('A1:H1').format.fill='#24364B';
    console.log((await workbook.inspect({kind:'table',range:'Waves!A1:H4',include:'values',tableMaxRows:4,tableMaxCols:8,maxChars:1200})).ndjson);
    const preview=await workbook.render({sheetName:'Waves',range:'A1:H6',scale:1,format:'png'});
    await fs.writeFile(path.join(root,'preview.png'),new Uint8Array(await preview.arrayBuffer()),{flag:'wx'});
    first=false;
  }
  count+=rows.length;
  range.clear({applyTo:'contents'});
  rows=[];
  console.log(JSON.stringify({rows_written:count}));
}
for await(const line of readline.createInterface({input:createReadStream(path.join(root,'wave_rows.jsonl')),crlfDelay:Infinity})){
  rows.push(JSON.parse(line));
  if(rows.length===20000)await flush();
}
await flush();
await target.close();
if(count!==report.base_points)throw new Error('Wrong row count');
console.log(JSON.stringify({complete:true,rows:count}));
