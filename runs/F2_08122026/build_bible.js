const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ExternalHyperlink}=require('docx');
const RUN=__dirname;
const BLUE="1155CC", RED="C0392B", AMBER="B7791F";
const picks=JSON.parse(fs.readFileSync(RUN+'/picks.json','utf8'));
const beats=JSON.parse(fs.readFileSync(RUN+'/beats.json','utf8'));
const byId=Object.fromEntries(picks.map(p=>[p.beat_id,p]));
const beatById=Object.fromEntries(beats.map(b=>[b.beat_id,b]));
const lines=fs.readFileSync(RUN+'/script.txt','utf8').split('\n');

// PLAY CLIP markers appear in script order and map to B01..B09.
const ORDER=["F2c-b01","F2c-b02","F2c-b03","F2c-b04","F2c-b05","F2c-b06","F2c-b07","F2c-b08","F2c-b09"];
let clipIdx=0;

const P=(text,opts={})=>new Paragraph({spacing:{after:opts.after??80},
  children:[new TextRun({text,bold:opts.bold,color:opts.color,italics:opts.italics,size:opts.size??22})]});

function clipBlock(bid){
  const p=byId[bid], b=beatById[bid], out=[];
  const tag=`${b.clip_role} / ${b.orientation}`;
  if(p && p.flagged){
    const r=p.ranked.find(x=>x.url===p.flagged);
    const gated=p.status==="producer_gated";
    out.push(new Paragraph({spacing:{after:40},children:[
      new TextRun({text:`${bid.toUpperCase()} — ${tag}${gated?"  ·  PRODUCER-GATED, DO NOT CUT UNTIL APPROVED":""}`,
        bold:true,color:gated?AMBER:BLUE,size:20})]}));
    out.push(new Paragraph({spacing:{after:40},children:[
      new TextRun({text:`${p.title}  —  `,color:BLUE,size:20}),
      new ExternalHyperlink({link:p.flagged,children:[
        new TextRun({text:p.flagged,color:BLUE,underline:{},size:20})]})]}));
    for(const s of r.segments){
      out.push(new Paragraph({spacing:{after:40},children:[
        new TextRun({text:`IN ${s.in} – OUT ${s.out}`,bold:true,color:BLUE,size:20}),
        new TextRun({text:`   OUTCUE: “${s.outcue}”`,color:BLUE,size:20})]}));
    }
    if(r.flags && r.flags.length)
      out.push(P("NOTE: "+r.flags.join("  ·  "),{color:AMBER,italics:true,size:18}));
  } else if(p && p.status==="manual_clip"){
    const unver = bid==="F2c-b07";
    out.push(new Paragraph({spacing:{after:40},children:[
      new TextRun({text:`${bid.toUpperCase()} — ${tag}  ·  MANUAL CLIP — NO CAPTIONS`,bold:true,color:BLUE,size:20})]}));
    out.push(new Paragraph({spacing:{after:40},children:[
      new TextRun({text:`${p.title}  —  `,color:BLUE,size:20}),
      new ExternalHyperlink({link:p.manual_url,children:[
        new TextRun({text:p.manual_url,color:BLUE,underline:{},size:20})]})]}));
    out.push(P(unver
      ? "OUTCUE UNVERIFIED — native TikTok post, no caption track and no local transcription available. Producer to set IN/OUT by eye. No timecode invented."
      : "No caption track on this source, so no verifiable outcue. Producer to set IN/OUT by eye. No timecode invented.",
      {color:AMBER,italics:true,size:18}));
  } else {
    out.push(new Paragraph({spacing:{after:40},children:[
      new TextRun({text:`${bid.toUpperCase()} — ${tag}  ·  NO CLIP FOUND`,bold:true,color:RED,size:20})]}));
    const why=(p&&p.flagged_reason||"no reason recorded").split(". ").slice(0,2).join(". ")+".";
    out.push(P("no clip found — "+why,{color:RED,size:18}));
  }
  out.push(P(""));
  return out;
}

const body=[];
body.push(new Paragraph({spacing:{after:200},children:[new TextRun({
  text:"F2 TOP STORIES — AIRDATE 08/12/2026 (WEDNESDAY) — CLIP BIBLE",bold:true,size:28})]}));
body.push(P("Clip cues filled by the Rossen pipeline, run F2_08122026. Blue = located clip with verified outcue. Amber = manual pull or gated. Red = no clip.",{italics:true,size:18}));
body.push(P(""));

for(const raw of lines){
  const line=raw.replace(/\s+$/,"");
  if(/^\(\(\(PLAY CLIP XXX/.test(line)){
    const bid=ORDER[clipIdx++];
    body.push(P(line,{bold:true,size:20}));
    if(bid) body.push(...clipBlock(bid));
    continue;
  }
  if(/^OUT:\s*$/.test(line)) continue;               // superseded by the filled block
  if(/^\(\(\(B0\d\s/.test(line)){ body.push(P(line,{italics:true,size:18})); continue; }
  if(/^\(\(\(DECIDE - DO WE ADD A BUST BEAT/.test(line)){
    body.push(P(line,{italics:true,size:18}));
    body.push(...clipBlock("F2c-b10"));
    continue;
  }
  if(/^\(\(\(JEFF SCREEN SHARE\)\)\)/.test(line)){
    body.push(P(line,{bold:true,size:20}));
    body.push(new Paragraph({spacing:{after:40},children:[new TextRun({
      text:"F2C-B11 — SHOW-PRODUCED  ·  no clip to source. Jeff walks missingmoney.com live.",
      bold:true,color:AMBER,size:20})]}));
    body.push(P(""));
    continue;
  }
  if(/^\(\(\(/.test(line)){ body.push(P(line,{bold:true,size:20})); continue; }
  if(line===""){ body.push(P("")); continue; }
  if(/^-/.test(line)){ body.push(P(line)); continue; }
  body.push(P(line,{bold:true,size:24}));            // segment headers
}

const doc=new Document({sections:[{children:body}]});
Packer.toBuffer(doc).then(b=>{
  const out=RUN+'/F2_TOP_STORIES_08122026_BIBLE_updated.docx';
  fs.writeFileSync(out,b);
  console.log("wrote",out,b.length,"bytes; clip markers filled:",clipIdx);
});
