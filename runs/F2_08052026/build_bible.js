const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ExternalHyperlink}=require('docx');
const RUN='/home/user/Rossen/runs/F2_08052026';
let lines=fs.readFileSync(RUN+'/script.txt','utf8').split('\n');

const BLUE="1155CC", RED="C0392B";

const clips=[
 {role:"explainer_demo / horizontal",kind:"pick",src:"Creator (YouTube)",url:"https://www.youtube.com/watch?v=DZ06YW82Qh8",in:"0:00 / 0:49",out:"0:36 / 2:08",outcue:"my item didn't arrive as promised",note:"2 butt-cut segments"},
 {role:"evidence / VERTICAL",kind:"empty",note:"No clip — phantom delivery doorbell cam content lives on TikTok, not YouTube."},
 {role:"victim_interview / horizontal",kind:"pick",src:"CBC Go Public",url:"https://www.youtube.com/watch?v=23OPFKfjQ5I",in:"0:00",out:"1:06",outcue:"a little bit of a slap in the face",note:"Script says HER, victim is male (Matthew Lago) — gender mismatch. CBC Canadian — clearance check."},
 {role:"authority_report / horizontal",kind:"pick",src:"WHAS11 / ABC News",url:"https://www.youtube.com/watch?v=ttBoYQjmaVc",in:"0:14",out:"1:33",outcue:"a clear and conspicuous button to help people decline or cancel their subscription"},
 {role:"first_person_rant / VERTICAL",kind:"weak",src:"Creator Short (YouTube)",url:"https://www.youtube.com/watch?v=mff8NrTcRw0",in:"0:00",out:"0:52",outcue:"the checks have to be cashed in within 60 days",note:"WEAK — news explainer, not first-person reaction. Beat wants TikTok reveal content."},
 {role:"authority_report / horizontal",kind:"pick",src:"Consumer Reports / Affiliate",url:"https://www.youtube.com/watch?v=ggDHtb-4GWQ",in:"0:38",out:"1:50",outcue:"hold online marketplaces accountable in the future"},
 {role:"evidence / VERTICAL",kind:"empty",note:"No clip — Lakkzoom heater fire footage. CPSC emergency action July 22, too recent for video coverage."},
 {role:"evidence / horizontal",kind:"pick",src:"WDIV Click On Detroit",url:"https://www.youtube.com/watch?v=ytkn-av0Dd8",in:"1:05 / 1:41",out:"1:41 / 2:10",outcue:"I saw a metal bristle right on the grate",note:"2 segments: victim story + magnet test. Named victim Linda — bristle in throat, surgery."},
 {role:"evidence / VERTICAL",kind:"pick",src:"YouTube Short",url:"https://www.youtube.com/shorts/55hbVRTDICA",in:"0:00",out:"0:38",outcue:"they go on a shopping spree in your name in real time",note:"From Rossen Reports channel — confirm using own content as source."},
 {role:"authority_report / horizontal",kind:"pick",src:"WBAY",url:"https://www.youtube.com/watch?v=g6n6rFw1MHk",in:"0:00",out:"0:43",outcue:"it is going to be an automatic process"},
 {role:"explainer_demo / horizontal",kind:"pick",src:"WEWS / Affiliate",url:"https://www.youtube.com/watch?v=erKRMlCUNkc",in:"0:23",out:"1:40",outcue:"like i said this is running the whole",note:"Reporter is female, script says WATCH HIM — minor mismatch."},
];

function blueRun(t,{bold=false,underline=false}={}){return new TextRun({text:t,color:BLUE,bold,underline:underline?{}:undefined});}
function redRun(t,{bold=false}={}){return new TextRun({text:t,color:RED,bold});}

function clipParas(c){
 const P=[];
 if(c.kind==="empty"){
   P.push(new Paragraph({spacing:{before:80,after:80},children:[redRun("▶ EMPTY BEAT — "+c.note,{bold:true})]}));
   return P;
 }
 const label=c.kind==="weak"?"▶ WEAK CLIP — "+c.role:"▶ CLIP — "+c.role;
 const labelColor=c.kind==="weak"?RED:BLUE;
 P.push(new Paragraph({spacing:{before:80,after:20},children:[new TextRun({text:label,color:labelColor,bold:true})]}));
 P.push(new Paragraph({spacing:{after:20},children:[blueRun("Source: "+c.src+"  —  "),
   new ExternalHyperlink({link:c.url,children:[blueRun(c.url,{underline:true})]})]}));
 P.push(new Paragraph({spacing:{after:c.note?20:120},children:[blueRun("IN "+c.in+"   OUT "+c.out+'   outcue: “'+c.outcue+'”',{bold:true})]}));
 if(c.note){
   P.push(new Paragraph({spacing:{after:120},children:[new TextRun({text:"⚠ "+c.note,color:c.kind==="weak"?RED:BLUE,italics:true})]}));
 }
 return P;
}

const paras=[]; let ci=0;
paras.push(new Paragraph({children:[new TextRun({text:"F2 TOP STORIES — 08/05/2026  (clips embedded)",bold:true,size:28})],spacing:{after:200}}));
for(let i=0;i<lines.length;i++){
 let l=lines[i];
 if(l.includes("PLAY CLIP")){
   for(const p of clipParas(clips[ci])) paras.push(p);
   ci++;
   if(i+1<lines.length && lines[i+1].trim().startsWith("OUT:")) i++;
   continue;
 }
 if(l.trim()==="BUTT") continue;
 const t=l.replace(/\r/g,'');
 if(t.trim()===''){ paras.push(new Paragraph({children:[]})); continue; }
 const isHeader=/^[A-Z0-9]/.test(t.trim()) && !t.trim().startsWith('-') && !t.startsWith('(((');
 paras.push(new Paragraph({spacing:{after:40},children:[new TextRun({text:t,bold:isHeader})]}));
}
const doc=new Document({sections:[{properties:{page:{size:{width:12240,height:15840}}},children:paras}]});
Packer.toBuffer(doc).then(b=>{
 fs.writeFileSync(RUN+'/F2_TOP_STORIES_08052026_BIBLE.docx',b);
 console.log('wrote docx,',ci,'clip blocks,',paras.length,'paragraphs');
});
