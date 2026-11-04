import type {composerReports as C} from '@custometry/contracts';
import {queryKey,type Definition} from './composer-state';
import {pruneScopes,copyScopes} from './composer-scope-state';

type Mutable<T>=T extends readonly (infer U)[]?Mutable<U>[]:T extends object?{-readonly [K in keyof T]:Mutable<T[K]>}:T;
type Draft=Mutable<Definition>;
const clone=<T,>(value:T):Mutable<T>=>structuredClone(value) as Mutable<T>;
export type Kind='chapter'|'page'|'section'|'block';
export type Node=C.ComposerChapter|C.ComposerPage|C.ComposerSection|C.ComposerBlock;
export type Target={kind:Kind;id:string};
export type Command=
 |{type:'add';kind:Exclude<Kind,'block'>;title:string;parent?:Target}
 |{type:'rename';target:Target;title:string}
 |{type:'delete'|'duplicate';target:Target;snapshot?:string}
 |{type:'reorder';target:Target;direction:-1|1}
 |{type:'move';target:Target;parent:Target|null;before?:string}
 |{type:'flag';target:Target;flag:'hidden'|'locked';value:boolean}
 |{type:'layout';page:string;layout:C.ComposerPage['layout']}
 |{type:'placement';block:string;placement:C.GridPlacement}
 |{type:'density';block:string;density:C.BlockPresentation['density']}
 |{type:'profile';profile:Definition['profile']};
export const identity=(n:Node):string=>'block_id'in n?n.block_id:'section_id'in n?n.section_id:'page_id'in n?n.page_id:n.chapter_id;
export function nodes(d:Draft,kind:Kind):Mutable<Node>[];
export function nodes(d:Definition,kind:Kind):readonly Node[];
export function nodes(d:Definition,kind:Kind):readonly Node[]{return kind==='chapter'?d.chapters??[]:kind==='page'?d.pages:kind==='section'?d.sections:d.blocks;}
export function node(d:Draft,t:Target):Mutable<Node>;
export function node(d:Definition,t:Target):Node;
export function node(d:Definition,t:Target):Node{const value=nodes(d,t.kind).find(n=>identity(n)===t.id);if(!value)throw Error('Unknown node');return value;}
export function parent(d:Definition,t:Target):Target|null {
 const n=node(d,t);
 if('block_id'in n)return {kind:'section',id:n.section_id};
 if('section_id'in n)return n.parent_section_id?{kind:'section',id:n.parent_section_id}:{kind:'page',id:n.page_id};
 if('page_id'in n)return n.chapter_id?{kind:'chapter',id:n.chapter_id}:null;
 return null;
}
export function ancestors(d:Definition,t:Target):Target[]{
 const result:Target[]=[];let current=parent(d,t);const seen=new Set([t.id]);
 while(current){if(seen.has(current.id))throw Error('Invalid hierarchy');seen.add(current.id);result.push(current);current=parent(d,current);}return result;
}
export const isLocked=(d:Definition,t:Target,includeSelf=true)=>[...(includeSelf?[t]:[]),...ancestors(d,t)].some(a=>node(d,a).locked);
export const isHidden=(d:Definition,t:Target)=>[t,...ancestors(d,t)].some(a=>node(d,a).hidden);
const sameParent=(a:Target|null,b:Target|null)=>a?.kind===b?.kind&&a?.id===b?.id;
const sorted=<T extends Node,>(items:readonly T[]):T[]=>items.slice().sort((a,b)=>a.order-b.order||identity(a).localeCompare(identity(b)));
export function orderedPages(d:Definition):C.ComposerPage[]{
 const chapters=sorted(d.chapters??[]);return [null,...chapters.map(c=>identity(c))].flatMap(id=>sorted(d.pages.filter(p=>(p.chapter_id??null)===id)) as C.ComposerPage[]);
}
export function descendants(d:Definition,t:Target):Target[]{
 return (['chapter','page','section','block'] as const).flatMap(kind=>nodes(d,kind).filter(n=>ancestors(d,{kind,id:identity(n)}).some(a=>a.id===t.id)).map(n=>({kind,id:identity(n)})));
}
function replace(d:Draft,kind:Kind,items:Mutable<Node>[]){
 if(kind==='chapter')d.chapters=items as Mutable<C.ComposerChapter>[];
 else if(kind==='page')d.pages=items as Mutable<C.ComposerPage>[];
 else if(kind==='section')d.sections=items as Mutable<C.ComposerSection>[];
 else d.blocks=items as Mutable<C.ComposerBlock>[];
}
function compact(d:Draft,kind:Kind,p:Target|null){sorted(nodes(d,kind).filter(n=>sameParent(parent(d,{kind,id:identity(n)}),p))).forEach((n,i)=>n.order=i);}
function prune(d:Draft){for(const b of d.blocks)if(b.control)b.control.target_block_ids=b.control.target_block_ids.filter(id=>d.blocks.some(t=>t.block_id===id&&t.source));const used=new Set(d.blocks.map(b=>b.source?.definition_id));d.definitions=d.definitions.filter(s=>used.has(s.definition_id));}
function visibleDefault(d:Draft){if(!d.pages.some(p=>p.page_id===d.default_page_id&&!isHidden(d,{kind:'page',id:p.page_id}))){const first=orderedPages(d).find(p=>!isHidden(d,{kind:'page',id:p.page_id}));if(!first)throw Error('Keep one visible page');d.default_page_id=first.page_id;}}
export const overlap=(a:C.GridPlacement,b:C.GridPlacement)=>(a.column??0)<(b.column??0)+(b.span??12)&&(b.column??0)<(a.column??0)+(a.span??12)&&(a.row??0)<(b.row??0)+(b.row_span??1)&&(b.row??0)<(a.row??0)+(a.row_span??1);
export function vacant(d:Definition,section:string,span=6,omit?:string,rowSpan=1):C.GridPlacement|null{
 const s=d.sections.find(s=>s.section_id===section);if(d.pages.find(p=>p.page_id===s?.page_id)?.layout!=='dashboard_grid')return null;
 for(let row=0;;row++)for(let column=0;column+span<=(d.grid_columns??12);column+=span){const candidate={column,span,row,row_span:rowSpan};if(!d.blocks.some(b=>b.block_id!==omit&&b.section_id===section&&b.placement&&overlap(candidate,b.placement)))return candidate;}
}
function assignParent(d:Draft,t:Target,p:Target|null){
 const n=node(d,t);
 if(t.kind==='chapter'){if(p)throw Error('Chapters are top-level');return;}
 if(p){node(d,p);if(p.id===t.id||ancestors(d,p).some(a=>a.id===t.id))throw Error('Invalid destination');if(isLocked(d,p))throw Error('Unlock destination first');}
 if('block_id'in n){if(p?.kind!=='section')throw Error('Choose a section');if(n.section_id!==p.id){const placement=n.placement;n.section_id=p.id;const grid=d.pages.find(page=>page.page_id===d.sections.find(section=>section.section_id===p.id)?.page_id)?.layout==='dashboard_grid';n.placement=grid&&placement&&!d.blocks.some(b=>b.block_id!==t.id&&b.section_id===p.id&&b.placement&&overlap(placement,b.placement))?placement:vacant(d,p.id,placement?.span??6,t.id,placement?.row_span??1);}}
 else if('section_id'in n){if(!p||!['page','section'].includes(p.kind))throw Error('Choose a page or section');const page=p.kind==='page'?p.id:(node(d,p) as Mutable<C.ComposerSection>).page_id;const changesGrid=(d.pages.find(p=>p.page_id===n.page_id)?.layout==='dashboard_grid')!==(d.pages.find(p=>p.page_id===page)?.layout==='dashboard_grid');const nested=descendants(d,t).filter(x=>x.kind==='section');n.page_id=page;n.parent_section_id=p.kind==='section'?p.id:null;for(const child of nested)(node(d,child) as Mutable<C.ComposerSection>).page_id=page;if(changesGrid)for(const section of [n,...nested.map(x=>node(d,x) as Mutable<C.ComposerSection>)])repack(d,section.section_id);}
 else if('page_id'in n){if(p&&p.kind!=='chapter')throw Error('Choose a chapter');n.chapter_id=p?.id??null;}
}
function repack(d:Draft,section:string){const list=sorted(d.blocks.filter(b=>b.section_id===section)) as Mutable<C.ComposerBlock>[];for(const b of list)b.placement=null;for(const b of list)b.placement=vacant(d,section,6,b.block_id);}

/** One immutable authoring transaction. Presentation commands never call Analytics. */
export function structure(d:Definition,command:Command):Definition {
 const next=clone(d);next.chapters??=[];
 if(command.type==='profile'){next.profile=command.profile;return next;}
 if(command.type==='add'){
  const id=crypto.randomUUID();if(!command.title.trim())throw Error('Enter a title');
  if(command.kind==='chapter')next.chapters.push({chapter_id:id,order:Math.max(-1,...next.chapters.map(c=>c.order))+1,title:command.title.trim()});
  else if(command.kind==='page'){
   const p=command.parent??null;if(p&&p.kind!=='chapter')throw Error('Choose a chapter');if(p&&isLocked(next,p))throw Error('Unlock destination first');
   next.pages.push({page_id:id,chapter_id:p?.id??null,title:command.title.trim(),order:Math.max(-1,...next.pages.filter(page=>(page.chapter_id??null)===(p?.id??null)).map(page=>page.order))+1,layout:'flow'});
   next.sections.push({section_id:crypto.randomUUID(),page_id:id,parent_section_id:null,order:0,title:command.title.trim()});

  }else{
   const p=command.parent;if(!p||!['page','section'].includes(p.kind))throw Error('Choose a page or section');if(isLocked(next,p))throw Error('Unlock destination first');
   next.sections.push({section_id:id,page_id:p.kind==='page'?p.id:(node(next,p) as Mutable<C.ComposerSection>).page_id,parent_section_id:p.kind==='section'?p.id:null,order:Math.max(-1,...next.sections.filter(s=>sameParent(parent(next,{kind:'section',id:s.section_id}),p)).map(s=>s.order))+1,title:command.title.trim()});
  }return next;
 }
 const target:Target='target'in command?command.target:command.type==='layout'?{kind:'page',id:command.page}:{kind:'block',id:command.block};
 const current=node(next,target);const unlocking=command.type==='flag'&&command.flag==='locked'&&!command.value;
 if(isLocked(next,target,!unlocking))throw Error('Unlock this item first');
 if(command.type==='rename'){if(!command.title.trim())throw Error('Enter a title');if('block_id'in current)current.presentation.title=command.title.trim();else current.title=command.title.trim();}
 else if(command.type==='flag'){current[command.flag]=command.value;visibleDefault(next);}
 else if(command.type==='delete'){
  const all=[target,...descendants(next,target)];if(all.some(t=>isLocked(next,t)))throw Error('Unlock descendants first');
  const ids=new Set(all.map(t=>t.id));for(const kind of ['chapter','page','section','block'] as const)replace(next,kind,nodes(next,kind).filter(n=>!ids.has(identity(n))));prune(next);visibleDefault(next);Object.assign(next,pruneScopes(next,ids));
 }
 else if(command.type==='reorder'){
  const p=parent(next,target),siblings=sorted(nodes(next,target.kind).filter(n=>sameParent(parent(next,{kind:target.kind,id:identity(n)}),p)));const at=siblings.findIndex(n=>identity(n)===target.id),to=at+command.direction;
  if(to<0||to>=siblings.length)return d;if(isLocked(next,{kind:target.kind,id:identity(siblings[to])}))throw Error('Unlock affected items first');[siblings[at],siblings[to]]=[siblings[to],siblings[at]];siblings.forEach((n,i)=>n.order=i);
 }
 else if(command.type==='move'){
  const previous=parent(next,target);assignParent(next,target,command.parent);const siblings=sorted(nodes(next,target.kind).filter(n=>identity(n)!==target.id&&sameParent(parent(next,{kind:target.kind,id:identity(n)}),command.parent)));
  const index=command.before?siblings.findIndex(n=>identity(n)===command.before):siblings.length;if(index<0)throw Error('Invalid insertion target');siblings.splice(index,0,current);siblings.forEach((n,i)=>n.order=i);if(!sameParent(previous,command.parent))compact(next,target.kind,previous);visibleDefault(next);
 }
 else if(command.type==='duplicate'){
  const tree=[target,...descendants(next,target)],ids=new Map(tree.map(t=>[t.id,crypto.randomUUID()])),sources=new Map<string,string>();
  for(const t of tree){const original=node(d,t),copy=clone(original);copy.copied_from={node_id:t.id,snapshot_id:command.snapshot??null};copy.locked=false;
   if('block_id'in copy){copy.block_id=ids.get(t.id)!;copy.section_id=ids.get(copy.section_id)??copy.section_id;if(copy.source){let source=sources.get(copy.source.definition_id);if(!source){source=crypto.randomUUID();sources.set(copy.source.definition_id,source);next.definitions.push({...clone(d.definitions.find(s=>s.definition_id===copy.source!.definition_id)!),definition_id:source});}copy.source.definition_id=source;}if(t.id===target.id)copy.placement=vacant(next,copy.section_id);}
   else if('section_id'in copy){copy.section_id=ids.get(t.id)!;copy.page_id=ids.get(copy.page_id)??copy.page_id;copy.parent_section_id=copy.parent_section_id?(ids.get(copy.parent_section_id)??copy.parent_section_id):null;}
   else if('page_id'in copy){copy.page_id=ids.get(t.id)!;copy.chapter_id=copy.chapter_id?(ids.get(copy.chapter_id)??copy.chapter_id):null;}
   else copy.chapter_id=ids.get(t.id)!;
   if(t.id===target.id)copy.order=Math.max(-1,...nodes(next,t.kind).filter(n=>sameParent(parent(next,{kind:t.kind,id:identity(n)}),parent(d,t))).map(n=>n.order))+1;
   replace(next,t.kind,[...nodes(next,t.kind),copy]);
  }
  for(const b of next.blocks)if(Array.from<string>(ids.values()).includes(b.block_id)&&b.control)b.control.target_block_ids=b.control.target_block_ids.map(id=>ids.get(id)??id);
  Object.assign(next,copyScopes(d,next,ids));
 }
 else if(command.type==='layout'){const p=current as Mutable<C.ComposerPage>;if(p.layout===command.layout)return d;const changesGrid=(p.layout==='dashboard_grid')!==(command.layout==='dashboard_grid');p.layout=command.layout;if(changesGrid)for(const section of next.sections.filter(s=>s.page_id===p.page_id))repack(next,section.section_id);}
 else if(command.type==='density')(current as Mutable<C.ComposerBlock>).presentation.density=command.density;
 else if(command.type==='placement'){
  const p=command.placement,block=current as Mutable<C.ComposerBlock>;
  const section=next.sections.find(s=>s.section_id===block.section_id)!;
  if(next.pages.find(p=>p.page_id===section.page_id)?.layout!=='dashboard_grid')throw Error('Choose grid layout');
  if(![p.column??0,p.span??12,p.row??0,p.row_span??1].every(Number.isInteger)||(p.column??0)<0||(p.span??12)<1||(p.column??0)+(p.span??12)>(next.grid_columns??12)||(p.row??0)<0||(p.row_span??1)<1||next.blocks.some(b=>b.block_id!==block.block_id&&b.section_id===block.section_id&&b.placement&&overlap(p,b.placement)))throw Error('Position overlaps or is outside the grid');
  block.placement=p;
 }
 for(const kind of ['chapter','page','section','block'] as const)for(const original of nodes(d,kind)){
  const t:Target={kind,id:identity(original)};if(unlocking&&t.id===target.id)continue;
  if(isLocked(d,t)&&JSON.stringify(original)!==JSON.stringify(nodes(next,kind).find(n=>identity(n)===t.id)))throw Error('Unlock affected items first');
 }
 return next;
}
export type History={past:Definition[];present:Definition;future:Definition[];revision:number};
export const startHistory=(present:Definition):History=>({past:[],present,future:[],revision:0});
export function record(history:History,next:Definition):History{
 if(JSON.stringify(history.present)===JSON.stringify(next))return history;
 // Bounded transient undo depth does not limit document pages or blocks.
 return {past:[...history.past,history.present].slice(-50),present:next,future:[],revision:history.revision+1};
}
export function travel(history:History,direction:'undo'|'redo'):History{
 if(direction==='undo'){const previous=history.past.at(-1);return previous?{past:history.past.slice(0,-1),present:previous,future:[history.present,...history.future],revision:history.revision+1}:history;}
 const next=history.future[0];return next?{past:[...history.past,history.present].slice(-50),present:next,future:history.future.slice(1),revision:history.revision+1}:history;
}
export function resultOrigin(previous:Definition,next:Definition,block:C.ComposerBlock):string|undefined{return previous.blocks.find(b=>queryKey(previous,b)===queryKey(next,block))?.block_id;}

export const sectionDepth=(d:Definition,id:string)=>ancestors(d,{kind:'section',id}).filter(a=>a.kind==='section').length;
export function orderedSections(d:Definition,page:string):C.ComposerSection[]{
 const result:C.ComposerSection[]=[];const stack=(sorted(d.sections.filter(s=>s.page_id===page&&!s.parent_section_id)) as C.ComposerSection[]).reverse();
 while(stack.length){const current=stack.pop()!;result.push(current);stack.push(...(sorted(d.sections.filter(s=>s.parent_section_id===current.section_id)) as C.ComposerSection[]).reverse());}return result;
}
