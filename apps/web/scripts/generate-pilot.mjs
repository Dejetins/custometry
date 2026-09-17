import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';
import crypto from 'node:crypto';
import vm from 'node:vm';
const emit=(target,value)=>{if(process.argv.includes('--check')){if(fs.readFileSync(target,'utf8')!==value)throw Error('Generated pilot drift: '+target);}else fs.writeFileSync(target,value);};
const root=path.resolve(import.meta.dirname,'../../..');
const source=fs.readFileSync(path.join(root,'docs/architecture/ui/target-pilot/ru/source.html'),'utf8');
const hash=crypto.createHash('sha256').update(source).digest('hex');
if(hash!=='b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700')throw Error('Pilot source changed');
const dir=path.join(root,'apps/web/src/features/reports/pilot');
// The entire document, including CSS and SVG, is retained. Only executable scripts
// are removed: the application supplies the source runtime through a typed port.
emit(path.join(dir,'document.html'),source.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g,''));
const script=source.match(/<script>\s*const uiText[\s\S]*?<\/script>/)[0].replace(/^<script>|<\/script>$/g,'');
const patches=JSON.parse(fs.readFileSync(path.join(dir,'seams.json'),'utf8'));
const parsed=ts.createSourceFile('pilot.js',script,ts.ScriptTarget.Latest,true,ts.ScriptKind.JS);
const edits=[];
for(const node of parsed.statements){if(ts.isFunctionDeclaration(node)&&patches[node.name?.text]!==undefined)edits.push([node.getStart(parsed),node.end,`function ${node.name.text}(${patches[node.name.text].args??''}) { ${patches[node.name.text].body} }`]);}
// Fixture values never enter the application bundle. Retain source labels and
// dimensional metadata for unavailable controls, with all business values absent.
const fixtureNames=new Set(['lifecycleSeries','lifecycleTotals','lifecycleValue','lifecycleReceipt','lifecycleFrequency','lifecycleMetricSeries','monthlyData','quarterData','migrationMatrix','segments']);
const blank=value=>Array.isArray(value)?value.map(blank):value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([k,v])=>[k,blank(v)])):typeof value==='number'?null:typeof value==='string'&&/[0-9₽]/.test(value)?'—':value;
for(const node of parsed.statements){if(!ts.isVariableStatement(node))continue;for(const declaration of node.declarationList.declarations){const name=declaration.name.getText(parsed);if(!fixtureNames.has(name)&&name!=='metrics')continue;const value=vm.runInNewContext('('+declaration.initializer.getText(parsed)+')',Object.create(null));const neutral=name==='metrics'?value.map(m=>({...m,value:{ru:'—',en:'—'},meta:{ru:'Данные недоступны',en:'Data unavailable'},deltas:{}})):blank(value);edits.push([declaration.initializer.getStart(parsed),declaration.initializer.end,JSON.stringify(neutral)]);}}
for(const name of Object.keys(patches))if(!edits.some(e=>e[2].startsWith(`function ${name}(`)))throw Error(`Missing seam ${name}`);
let adapted=script;for(const [start,end,value] of edits.sort((a,b)=>b[0]-a[0]))adapted=adapted.slice(0,start)+value+adapted.slice(end);
const prelude=fs.readFileSync(path.join(dir,'port-prelude.js'),'utf8');
const epilogue=fs.readFileSync(path.join(dir,'port-epilogue.js'),'utf8');
emit(path.join(dir,'runtime.ts'),`// @ts-nocheck\n// Generated from the preserved pilot ${hash}; run scripts/generate-pilot.mjs.\nexport function mountPilot(document, window, bridge, echarts) {\n${prelude}\n${adapted}\n${epilogue}\n}\n`);
emit(path.join(dir,'source-map.json'),JSON.stringify({source:'docs/architecture/ui/target-pilot/ru/source.html',sha256:hash,documentTransform:'remove executable script tags only',replacedFunctions:Object.keys(patches)},null,2)+'\n');
