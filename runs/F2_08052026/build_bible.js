// Build the filled Bible .docx for F2 08-05.
// - Blue (1155CC) clickable clip link + IN/OUT + verbatim outcue at each PLAY CLIP.
// - Red (C0392B) annotation for the weak beat and the three case-swaps.
// - Swapped beats have their setup lines rewritten in place (V->H), so the
//   doc reads as a shootable rundown.
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink } = require('docx');
const RUN = '/home/user/Rossen/runs/F2_08052026';
const BLUE = "1155CC", RED = "C0392B";
const TITLE_SIZE = 46;  // 23pt (docx sizes are half-points)
const BODY_SIZE = 36;   // 18pt, everything else

const beats = Object.fromEntries(JSON.parse(fs.readFileSync(RUN+'/beats.json')).map(b => [b.beat_id, b]));
const picks = JSON.parse(fs.readFileSync(RUN+'/picks.json'));
const pickBy = Object.fromEntries(picks.map(p => [p.beat_id, p]));
const ORDER = picks.map(p => p.beat_id).sort();  // markers appear in beat order b01..b11

const WEAK = new Set(["08-05-b01"]);
const SWAP = new Set(["08-05-b02","08-05-b05","08-05-b07"]);

// Setup-line rewrites for the three case-swaps. Replace from the header
// substring up to (not including) the next PLAY CLIP marker.
const REWRITES = [
 { header: "EXCEPT IT WASN", lines: [
   "PACKAGES THAT SAY DELIVERED — BUT NEVER SHOW UP   [[SWAP: was vertical doorbell-cam evidence]]",
   "",
   "-YOUR PHONE BUZZES. DELIVERED. THERE'S EVEN A PHOTO OF YOUR FRONT DOOR. YOU GO OUTSIDE… AND THERE IS NOTHING THERE.",
   "-AMAZON TELLS YOU TO WAIT 24 TO 48 HOURS, BECAUSE SOMETIMES THE SCAN RUNS AHEAD OF THE TRUCK.",
   "-FINE. WAIT. BUT AFTER THAT, YOU ARE NOT BEGGING FOR A FAVOR. YOU ARE OWED.",
   "-AND IT IS NOT ALWAYS AMAZON ITSELF. INVESTIGATORS ARE DIGGING INTO SHIPPERS WHOSE TRACKING SAYS DELIVERED WHEN IT ISN'T.",
   "-LISTEN TO THESE SHOPPERS WHO PAID, WATCHED THE TRACKING MOVE, AND NEVER GOT THEIR PACKAGES.",
 ]},
 { header: "ABOUT THE SIZE OF THESE CHECKS", lines: [
   "NOW — THE SIZE OF THESE CHECKS   [[SWAP: was vertical 'people posting payouts' reaction]]",
   "",
   "-NOW… ABOUT THE SIZE OF THESE CHECKS.",
   "-$51 IS THE MAXIMUM. IT IS NOT WHAT EVERYBODY GETS.",
   "-YOU GET BACK THE PRIME FEES YOU ACTUALLY PAID, MINUS ANY REFUNDS OR CREDITS YOU ALREADY GOT.",
   "-SO IF YOU SIGNED UP ON A CHEAP TRIAL, YOUR CHECK COULD BE A COUPLE OF DOLLARS. OR LESS.",
   "-AND IF A CHECK OR EMAIL SHOWS UP FROM AMAZON — DON'T ASSUME IT'S A SCAM. HERE'S HOW TO KNOW YOURS IS REAL.",
 ]},
 { header: "AND THEY WERE ON SALE THIS MONTH", lines: [
   "IT IS NOT JUST HEATERS — RECALLED LITHIUM BATTERIES THAT CATCH FIRE   [[SWAP: was Lakkzoom immersion heater, no video yet]]",
   "",
   "-THE NEWEST FIRE HAZARD SITTING IN YOUR HOUSE ISN'T A HEATER — IT'S A LITHIUM BATTERY.",
   "-ANKER — SOLD ALL OVER AMAZON — JUST RECALLED HUNDREDS OF THOUSANDS OF POWER BANKS.",
   "-THE LITHIUM-ION BATTERIES CAN OVERHEAT, CATCH FIRE, AND EVEN EXPLODE.",
   "-THE C-P-S-C KNOWS OF DOZENS OF FIRES AND EXPLOSIONS ALREADY — SOME WITH BURNS.",
   "-STOP USING THE RECALLED MODELS TODAY. HERE'S WHAT WE KNOW RIGHT NOW.",
 ]},
];

// Cold-open tease lines that named the (now-swapped-out) Lakkzoom heater.
// Realign them to the Anker power-bank story so the tease matches the segment.
const LINE_REWRITES = [
 { find: "EMERGENCY POWER IT HADN’T TOUCHED IN NEARLY 40 YEARS",
   to: "-AND THIS MONTH, ANOTHER RECALLED PRODUCT SOLD ALL OVER AMAZON WAS CATCHING FIRE — LITHIUM POWER BANKS." },
 { find: "235 FIRES. 98,000 UNITS. AND THEY WERE STILL FOR SALE ON AMAZON IN JULY",
   to: "-DOZENS OF FIRES AND EXPLOSIONS. HUNDREDS OF THOUSANDS OF UNITS. AND THEY WERE STILL FOR SALE ON AMAZON." },
];

let lines = fs.readFileSync(RUN+'/script.txt','utf8').split('\n').map(l => l.replace(/\r/g,''));

for (const lr of LINE_REWRITES) {
  const i = lines.findIndex(l => l.includes(lr.find));
  if (i < 0) { console.error("LINE_REWRITE not found:", lr.find); continue; }
  lines[i] = lr.to;
}

for (const rw of REWRITES) {
  const hi = lines.findIndex(l => l.includes(rw.header));
  if (hi < 0) { console.error("REWRITE header not found:", rw.header); continue; }
  let mi = hi;
  while (mi < lines.length && !lines[mi].includes("PLAY CLIP")) mi++;
  lines.splice(hi, mi - hi, ...rw.lines);
}

function segLine(p) {
  return p.segments.map(s => `IN ${s.in}  OUT ${s.out}  outcue: “${s.outcue}”`);
}
function roleLabel(bid) {
  const p = pickBy[bid], b = beats[bid];
  return `${(p.clip_role || b.clip_role)}  /  ${(p.orientation || b.orientation).toUpperCase()}`;
}

function clipParas(bid) {
  const p = pickBy[bid];
  const P = [];
  const swap = SWAP.has(bid), weak = WEAK.has(bid);
  const headColor = (swap || weak) ? RED : BLUE;
  const head = swap ? "▶ CLIP (CASE-SWAP) — " : weak ? "▶ CLIP (WEAK — RE-CHECK) — " : "▶ CLIP — ";
  P.push(new Paragraph({spacing:{before:120,after:20},
    children:[new TextRun({text: head + roleLabel(bid), color: headColor, bold:true, size:BODY_SIZE})]}));
  P.push(new Paragraph({spacing:{after:20}, children:[
    new TextRun({text:`Source: ${p.uploader} (${p.source_type}, ${p.platform})  —  `, color:BLUE, size:BODY_SIZE}),
    new ExternalHyperlink({link:p.flagged, children:[new TextRun({text:p.flagged, color:BLUE, underline:{}, size:BODY_SIZE})]}),
  ]}));
  for (const s of segLine(p)) {
    P.push(new Paragraph({spacing:{after:20}, children:[new TextRun({text:s, color:BLUE, bold:true, size:BODY_SIZE})]}));
  }
  P.push(new Paragraph({spacing:{after:20}, children:[new TextRun({text:`“${p.title}”`, color:BLUE, italics:true, size:BODY_SIZE})]}));
  if (swap) {
    P.push(new Paragraph({spacing:{after:20}, children:[new TextRun({
      text:`⚠ CASE-SWAP: original beat was ${p.swapped_from}. Setup lines above rewritten to match the new clip.`,
      color:RED, italics:true, size:BODY_SIZE})]}));
  }
  if (weak) {
    P.push(new Paragraph({spacing:{after:20}, children:[new TextRun({
      text:`⚠ WEAK FIT: ${p.flags.join('; ')}. Producer should confirm or treat as show-produced.`,
      color:RED, italics:true, size:BODY_SIZE})]}));
  }
  if (!weak && p.flags && p.flags.length) {
    P.push(new Paragraph({spacing:{after:140}, children:[new TextRun({text:`note: ${p.flags.join('; ')}`, color:BLUE, italics:true, size:BODY_SIZE})]}));
  } else {
    P.push(new Paragraph({spacing:{after:120}, children:[]}));
  }
  return P;
}

const paras = [];
paras.push(new Paragraph({spacing:{after:80}, children:[new TextRun({text:"F2 TOP STORIES — WEDNESDAY, AUGUST 5", bold:true, size:TITLE_SIZE})]}));
paras.push(new Paragraph({spacing:{after:200}, children:[new TextRun({
  text:"Bible with clips embedded. Blue = clip to pull (IN/OUT + verbatim outcue). Red = weak fit or case-swap. Clips are located and timecoded for a human to pull and cut — nothing was auto-downloaded.",
  italics:true, size:BODY_SIZE, color:"555555"})]}));

let ci = 0;
for (let i = 0; i < lines.length; i++) {
  const l = lines[i];
  if (l.includes("PLAY CLIP")) {
    for (const p of clipParas(ORDER[ci])) paras.push(p);
    ci++;
    if (i+1 < lines.length && lines[i+1].trim().startsWith("OUT:")) i++;
    continue;
  }
  if (l.trim() === "BUTT") continue;
  if (l.trim() === "") { paras.push(new Paragraph({children:[]})); continue; }
  const t = l;
  const isHeader = /^[A-Z0-9]/.test(t.trim()) && !t.trim().startsWith('-') && !t.startsWith('(((');
  if (t.includes("[[SWAP")) {
    const idx = t.indexOf("[[SWAP");
    paras.push(new Paragraph({spacing:{after:40}, children:[
      new TextRun({text: t.slice(0, idx).trim()+"  ", bold:true, size:BODY_SIZE}),
      new TextRun({text: t.slice(idx), color:RED, italics:true, size:BODY_SIZE})]}));
    continue;
  }
  paras.push(new Paragraph({spacing:{after:40}, children:[new TextRun({text:t, bold:isHeader, size:BODY_SIZE})]}));
}

const doc = new Document({sections:[{properties:{page:{size:{width:12240,height:15840}}}, children:paras}]});
Packer.toBuffer(doc).then(b => {
  const out = RUN + '/F2_TOP_STORIES_08052026_BIBLE.docx';
  fs.writeFileSync(out, b);
  console.log("wrote", out, b.length, "bytes;", ci, "clip blocks emitted");
});
