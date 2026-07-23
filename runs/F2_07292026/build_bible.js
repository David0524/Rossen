const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ExternalHyperlink}=require('docx');
const RUN='/home/user/Rossen/runs/F2_07292026';
let lines=fs.readFileSync(RUN+'/script.txt','utf8').split('\n');

// ---- b02 / b03 script-text swaps (match by distinctive substring) ----
// full-line replacements: if a line contains the key, swap the WHOLE line
const repl=[
 ["ANN DICKHERBER","-GREG BULL IS A DATA-SECURITY EXPERT WHOSE COMPANY SCREENS MORE THAN A BILLION CALLS A DAY."],
 ["LESS THAN TEN SECONDS OF YOUR VOICE","-HE SAYS JUST THREE SECONDS OF YOUR VOICE IS ALL A SCAMMER NEEDS TO FOOL ANYONE."],
 ["SO SHE TOOK A FEW SECONDS OF A TV REPORTER","-SO FOX4'S STEVE NOVIELLO LET THEM CLONE HIS OWN VOICE, RIGHT THERE IN THE STORY…"],
 ["MADE THE CLONE SAY WHATEVER SHE WANTED","-…AND THE FAKE VERSION SAID WHATEVER THEY WANTED IT TO SAY."],
 ["WATCH HER SHOW YOU HOW","-WATCH HIM SHOW YOU HOW."],
 ["THIS MOM RECORDED THE CALL","THIS FAMILY ALMOST LOST IT ALL TO A CLONED VOICE"],
 ["MISSOURI MOTHER NAMED RACHEL","-A HILLSBORO, OREGON MOTHER NAMED TINA GOT THE CALL EVERY PARENT DREADS."],
 ["SHE BELIEVED HER DAUGHTER HAD BEEN TAKEN","-SHE HEARD WHAT SOUNDED LIKE HER DAUGHTER WHIMPERING, AND A MAN SAYING HE HAD HER."],
 ["ACTUAL AUDIO FROM THAT PHONE CALL","-TINA CAUGHT IT — BUT MINUTES LATER THEY CALLED HER HUSBAND, AND HE WIRED $2,500 TO MEXICO. LISTEN TO WHAT HAPPENED TO THEM."],
];
lines=lines.map(l=>{for(const [a,b] of repl){if(l.includes(a))return b;}return l;});

// ---- clip data in marker order (b01..b12) ----
const BLUE="1155CC", RED="C0392B";
const clips=[
 {role:"victim_interview / horizontal",kind:"manual",src:"ABC7 San Francisco",url:"https://abc7news.com/post/bay-area-mom-thousands-scammers-use-ai-mimic-daughters-voice-fake-kidnapping-part-growing-trend/19154381/",note:"Exact case — Deborah Del Mastro, Bay Area, $5,400. No captions; pull the on-camera soundbite by eye."},
 {role:"explainer_demo / horizontal",kind:"pick",src:"FOX 4 Dallas-Fort Worth",url:"https://www.youtube.com/watch?v=gMXuQ4MusPk",in:"2:00",out:"2:12",outcue:"it's my voice artificially generated"},
 {role:"victim_interview / horizontal",kind:"pick",src:"KATU News (Portland)",url:"https://www.youtube.com/watch?v=sPIIFyPyKKE",in:"1:37",out:"2:30",outcue:"It's your child"},
 {role:"authority_report / horizontal",kind:"manual",src:"KMBC 9 (Kansas City)",url:"https://www.kmbc.com/article/olathe-police-warn-scam-child-abduction-money/70238283",note:"Exact case — Olathe PD kids-voice reports. No captions; pull by eye."},
 {role:"victim_interview / horizontal",kind:"manual",src:"FOX 29 Philadelphia",url:"https://www.fox29.com/news/philadelphia-attorney-raises-awareness-after-nearly-falling-victim-to-elaborate-phone-scam",note:"Exact case — Gary Schildhorn, cloned son's voice. No captions; pull by eye."},
 {role:"victim_interview / horizontal",kind:"pick",src:"WFLA News Channel 8 (Tampa)",url:"https://www.youtube.com/watch?v=As4nS5aOVnw",in:"0:38",out:"1:02",outcue:"so she gave it to them"},
 {role:"authority_report / horizontal",kind:"empty",note:"No clip — FBI IC3 alert I-072026-PSA is 5 days old; no case-match video yet."},
 {role:"evidence / VERTICAL",kind:"empty",note:"No clip — no fake-IC3-site / deepfake-official screen recording found."},
 {role:"authority_report / horizontal",kind:"pick",src:"WPRI 12",url:"https://www.youtube.com/watch?v=rkZMNuoNfqA",in:"1:25",out:"1:48",outcue:"deposit money into a Bitcoin ATM"},
 {role:"authority_report / horizontal",kind:"pick",src:"WCNC Charlotte",url:"https://www.youtube.com/watch?v=JUbuCpPGX3g",in:"0:27",out:"0:55",outcue:"the S standing for secure"},
 {role:"evidence / VERTICAL",kind:"empty",note:"No clip — no nurse/coach/tuition scam-text screen recording found."},
 {role:"explainer_demo / horizontal",kind:"empty",note:"No clip — no Target Circle barcode-scan demo found."},
];

function blueRun(t,{bold=false,underline=false}={}){return new TextRun({text:t,color:BLUE,bold,underline:underline?{}:undefined});}
function clipParas(c){
 const P=[];
 if(c.kind==="empty"){
   P.push(new Paragraph({spacing:{before:80,after:80},children:[new TextRun({text:"▶ "+c.note,color:RED,bold:true})]}));
   return P;
 }
 P.push(new Paragraph({spacing:{before:80,after:20},children:[blueRun("▶ CLIP — "+c.role+(c.kind==="manual"?"   (MANUAL CLIP — no captions)":""),{bold:true})]}));
 P.push(new Paragraph({spacing:{after:20},children:[blueRun("Source: "+c.src+"  —  "),
   new ExternalHyperlink({link:c.url,children:[blueRun(c.url,{underline:true})]})]}));
 if(c.kind==="pick"){
   P.push(new Paragraph({spacing:{after:120},children:[blueRun("IN "+c.in+"   OUT "+c.out+'   outcue: "'+c.outcue+'"',{bold:true})]}));
 } else {
   P.push(new Paragraph({spacing:{after:120},children:[blueRun(c.note)]}));
 }
 return P;
}

// ---- walk lines -> paragraphs ----
const paras=[]; let ci=0;
paras.push(new Paragraph({children:[new TextRun({text:"F2 TOP STORIES — 07/29/2026  (clips embedded)",bold:true,size:28})],spacing:{after:200}}));
for(let i=0;i<lines.length;i++){
 let l=lines[i];
 if(l.includes("PLAY CLIP")){ // replace marker + following OUT: line with clip block
   for(const p of clipParas(clips[ci])) paras.push(p);
   ci++;
   if(i+1<lines.length && lines[i+1].trim().startsWith("OUT:")) i++; // skip OUT:
   continue;
 }
 if(l.trim()==="BUTT") continue; // structural, drop
 const t=l.replace(/\r/g,'');
 if(t.trim()===''){ paras.push(new Paragraph({children:[]})); continue; }
 const isHeader=/^[A-Z0-9]/.test(t.trim()) && !t.trim().startsWith('-') && !t.startsWith('(((');
 paras.push(new Paragraph({spacing:{after:40},children:[new TextRun({text:t,bold:isHeader})]}));
}
const doc=new Document({sections:[{properties:{page:{size:{width:12240,height:15840}}},children:paras}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(RUN+'/F2_TOP_STORIES_07292026_BIBLE_updated.docx',b);console.log('wrote docx,',ci,'clip blocks,',paras.length,'paragraphs');});
