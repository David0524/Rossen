const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ExternalHyperlink}=require('docx');
const RUN='/home/user/Rossen/runs/F1_07312026';
const lines=fs.readFileSync(RUN+'/script.txt','utf8').split('\n');

// No script-text swaps applied. b04's case swap was NOT taken — see report.md.
// The producer's setup lines are untouched.

const BLUE="1155CC", RED="C0392B", AMBER="B7791F";

const clips=[
 {role:"victim_interview / horizontal",kind:"pick",src:"Scripps 'Don't Waste Your Money' (John Matarese) — carried by WCPO 9",
  url:"https://www.wcpo.com/money/consumer/dont-waste-your-money/fake-rental-listings-targeting-summer-travelers-on-airbnb-vrbo",
  alt:"https://www.youtube.com/watch?v=uWnVyoPqOcw",
  in:"0:18",out:"0:55",outcue:"straight to voicemail",
  note:"BUTT segment 1 of 2 — same package as the next clip."},

 {role:"authority_report / horizontal",kind:"pick",src:"Same Scripps package — Kevin Brasler, Consumers' Checkbook",
  url:"https://www.wcpo.com/money/consumer/dont-waste-your-money/fake-rental-listings-targeting-summer-travelers-on-airbnb-vrbo",
  alt:"https://www.youtube.com/watch?v=uWnVyoPqOcw",
  in:"0:59",out:"1:19",outcue:"not really part of this transaction",
  note:"BUTT segment 2 of 2. Producer question at this marker is ANSWERED: Gentry and Brasler are one package, so this is one source, two segments."},

 {role:"victim_interview / horizontal",kind:"manual",src:"Inside Edition — 'The Genius Way This Reporter Uncovered Airbnb Scammers'",
  url:"https://www.youtube.com/watch?v=VfwRWgw_M3I",
  note:"Conti on camera, 8:15. ANSWERS the producer question at this marker: the video DOES exist, so the Jeff-read-over-screenshots fallback is not needed. No timecode given — this environment could not pull captions or media to verify an outcue (YouTube bot-wall). Pull the in/out on a machine with normal YouTube access."},

 {role:"victim_interview / horizontal",kind:"manual",src:"CBS Los Angeles — 'Exclusive: Family Discovers Home Listed On Airbnb Without Their Permission'",
  url:"https://www.youtube.com/watch?v=WMofFj3FJDQ",
  note:"Confirmed as the Jeff Branch case (Santa Monica Mountains, $450/night, 'modern masterpiece', pet sitter — cross-checked against KNX's write-up of the CBS LA investigation). Option A taken; beat stays HORIZONTAL. No timecode — same YouTube bot-wall. See report.md for the ABC15 swap option, which was NOT applied."},
];

function blue(t,o={}){return new TextRun({text:t,color:BLUE,bold:!!o.bold,underline:o.underline?{}:undefined});}

function clipParas(c){
 const P=[];
 if(c.kind==="empty"){
   P.push(new Paragraph({spacing:{before:80,after:120},children:[new TextRun({text:"▶ "+c.note,color:RED,bold:true})]}));
   return P;
 }
 const tag = c.kind==="manual" ? "   (MANUAL CLIP — no verified timecode)" : "";
 P.push(new Paragraph({spacing:{before:80,after:20},
   children:[blue("▶ CLIP — "+c.role+tag,{bold:true})]}));
 P.push(new Paragraph({spacing:{after:20},
   children:[blue("Source: "+c.src+"  —  "),
             new ExternalHyperlink({link:c.url,children:[blue(c.url,{underline:true})]})]}));
 if(c.alt){
   P.push(new Paragraph({spacing:{after:20},
     children:[blue("Also on YouTube: "),
               new ExternalHyperlink({link:c.alt,children:[blue(c.alt,{underline:true})]})]}));
 }
 if(c.kind==="pick"){
   P.push(new Paragraph({spacing:{after:20},
     children:[blue("IN "+c.in+"   OUT "+c.out+'   outcue: "'+c.outcue+'"',{bold:true})]}));
 }
 if(c.note){
   P.push(new Paragraph({spacing:{after:120},
     children:[new TextRun({text:c.note,color:c.kind==="manual"?AMBER:BLUE})]}));
 }
 return P;
}

const paras=[];
let ci=0;
paras.push(new Paragraph({spacing:{after:200},
  children:[new TextRun({text:"07/31 LIVE — THE AIRBNB & VRBO RENTAL SCAM  (clips embedded)",bold:true,size:28})]}));

for(const l of lines){
  if(l.includes("PLAY CLIP")){
    paras.push(new Paragraph({spacing:{before:60},
      children:[new TextRun({text:l.trim(),bold:true})]}));
    if(ci<clips.length) paras.push(...clipParas(clips[ci++]));
    continue;
  }
  const t=l.replace(/\s+$/,'');
  const isHead = t && !t.startsWith('-') && !t.startsWith('(((') && t===t.toUpperCase() && t.length>12;
  paras.push(new Paragraph({spacing:{after:t?40:0},
    children:[new TextRun({text:t,bold:isHead})]}));
}

const doc=new Document({sections:[{children:paras}]});
Packer.toBuffer(doc).then(b=>{
  const out=RUN+'/F1_AIRBNB_VRBO_07312026_BIBLE_updated.docx';
  fs.writeFileSync(out,b);
  console.log('wrote '+out+'  ('+b.length+' bytes, '+ci+' clip blocks embedded)');
});
