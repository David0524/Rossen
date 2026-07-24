// Build the filled Bible .docx for F2 08-07.
//
// - Blue (1155CC) clickable clip link + IN/OUT + verbatim outcue at each PLAY CLIP.
// - Red (C0392B) for the case-swap, the show-produced beat, and the manual clip
//   that ships without a timecode.
// - b01/b02 are two slices of ONE source (the script's BUTT marker), so the doc
//   says so at both markers — the edit bay pulls the file once.
// - Swapped beats have their setup lines rewritten in place so the doc reads as
//   a shootable rundown rather than a script that contradicts its own footage.
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink } = require('docx');
const RUN = '/home/user/Rossen/runs/F2_08072026';
const BLUE = "1155CC", RED = "C0392B", GREY = "555555";
const TITLE_SIZE = 46;  // 23pt (docx sizes are half-points)
const BODY_SIZE = 36;   // 18pt

const beats = Object.fromEntries(JSON.parse(fs.readFileSync(RUN+'/beats.json')).map(b => [b.beat_id, b]));
const picks = JSON.parse(fs.readFileSync(RUN+'/picks.json'));
const pickBy = Object.fromEntries(picks.map(p => [p.beat_id, p]));
const ORDER = ["b01","b02","b03","b04"];   // PLAY CLIP markers in script order

// ---------------------------------------------------------------- rewrites
// b01 + b02 swapped off the Manatee County / Xin Liu case, which has no video
// in existence (print coverage only). Rewritten to the Bruce Fredy /
// Hillsborough County case that the chosen FOX 13 package actually documents.
const REWRITES = [
 { header: "AND SOMETIMES THEY SEND A REAL PERSON TO YOUR FRONT DOOR", lines: [
   "AND SOMETIMES THEY SEND A REAL PERSON TO YOUR FRONT DOOR   [[SWAP: was Manatee County / Xin Liu — no video exists]]",
   "",
   "-IN RIVERVIEW, FLORIDA, A MAN NAMED BRUCE FREDY GOT A CALL FROM SOMEONE CLAIMING TO BE POLICE.",
   "-THEY TOLD HIM A GOOD FRIEND WAS IN JAIL AND NEEDED BAIL MONEY, RIGHT NOW.",
   "-AND THEN THEY PUT HIS FRIEND ON THE LINE. HE SAYS IT WAS EXACTLY HIS VOICE.",
   "-THE ASK WAS SEVENTY FIVE HUNDRED DOLLARS IN CASH, SEALED IN A BOX.",
   "-THEN THEY SENT A DRIVER TO HIS HOUSE TO PICK IT UP. AND THEN THEY DID IT A SECOND TIME.",
   "-HERE IS HOW THAT SCAM ACTUALLY RUNS.",
 ]},
 { header: "BUT WHAT HAPPENED NEXT IS THE PART THAT STOPPED ME COLD", lines: [
   "-BUT WHAT HAPPENED NEXT IS THE PART THAT STOPPED ME COLD.",
   "-AFTER THE THIRD REQUEST, FREDY CALLED THE HILLSBOROUGH COUNTY SHERIFF'S OFFICE.",
   "-THEY SENT DEPUTIES TO HIS HOUSE IN UNDERCOVER VEHICLES AND SET UP A STING.",
   "-THEY LISTENED IN WHILE THE SCAMMERS CALLED TO ARRANGE A THIRD PICKUP.",
   "-THEN THEY PUT FAKE MONEY IN THE BOX AND WAITED.",
   "-WATCH WHAT HAPPENS WHEN THE COURIER SHOWS UP TO COLLECT.",
 ]},
];

// Cold-open and closing lines that referenced the swapped-out Florida case.
const LINE_REWRITES = [
 { find: "-TWO MORE COURIERS ARRESTED. XIN LIU GOT 27 MONTHS IN FEDERAL PRISON IN JUNE.",
   to:   "-THE DRIVER WAS FOLLOWED FROM RIVERVIEW TO ORLANDO, ARRESTED, AND CHARGED WITH GRAND THEFT." },
 { find: "-THAT IS WHAT ONE PHOTOGRAPH FROM ONE SUSPICIOUS NEIGHBOR CAN DO.",
   to:   "-THAT IS WHAT ONE PHONE CALL TO YOUR SHERIFF'S OFFICE CAN DO." },
 { find: "-IF YOU CAN DO IT SAFELY, PHOTOGRAPH THEM AND THEIR CAR. THAT CRACKED THE FLORIDA CASE.",
   to:   "-IF YOU CAN DO IT SAFELY, PHOTOGRAPH THEM AND THEIR CAR. THAT IS WHAT CRACKS THESE CASES." },
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

// ------------------------------------------------------------ clip blocks
function para(children, after=20) { return new Paragraph({spacing:{after}, children}); }
function run(text, color, opts={}) {
  return new TextRun(Object.assign({text, color, size:BODY_SIZE}, opts));
}

function clipParas(bid) {
  const p = pickBy[bid], b = beats[bid];
  const P = [];

  // --- b03: show-produced, no clip to pull ------------------------------
  if (p.disposition === "production_task") {
    P.push(para([run("▶ NO CLIP — SHOW-PRODUCED PRODUCTION TASK", RED, {bold:true})], 20));
    P.push(para([run("Screen-record a live fake IC3 / FBI recovery page on set.", RED)], 20));
    P.push(para([run("Must show both tells the script names: every other link bounces back to the home page, and the intake form is ONE step (name, phone, email, scam type, amount lost).", RED, {italics:true})], 20));
    P.push(para([run("Why no clip: no third-party footage can be guaranteed to show those specific tells. Approved as a production assignment at Checkpoint 1 — this is not a search failure.", GREY, {italics:true})], 140));
    return P;
  }

  // --- b04: manual clip, no captions, no timecode ------------------------
  if (p.manual_clip) {
    P.push(para([run("▶ MANUAL CLIP — NO CAPTIONS", RED, {bold:true})], 20));
    P.push(para([
      run(`Source: ${p.uploader} (${p.source_type}, ${p.platform})  —  `, BLUE),
      new ExternalHyperlink({link:p.flagged, children:[
        new TextRun({text:p.flagged, color:BLUE, underline:{}, size:BODY_SIZE})]}),
    ], 20));
    P.push(para([run(`“${p.title}”`, BLUE, {italics:true})], 20));
    P.push(para([run(`Runs ${p.duration}s. Reporter: ${p.reporter}.`, BLUE)], 20));
    P.push(para([run("NO IN/OUT AND NO OUTCUE PROPOSED. This is a CBS video page, not YouTube — there is no caption track to verify an outcue against, so none was invented. Editor sets in/out on pull.", RED, {italics:true})], 20));
    P.push(para([run("⚠ VINTAGE UNCONFIRMED — the script flags this as a 2024 package and asks confirm-or-swap. The page did not expose a publication date.", RED, {italics:true})], 20));
    P.push(para([run("Longer 197s cut of the same case: https://www.cbsnews.com/newyork/video/scam-victim-loses-even-more-to-fake-online-romance-scam-support-group/", GREY, {italics:true})], 140));
    return P;
  }

  // --- b01 / b02: verified picks ----------------------------------------
  const swap = p.requires_script_change;
  P.push(para([run((swap ? "▶ CLIP (CASE-SWAP) — " : "▶ CLIP — ") +
    `${b.clip_role}  /  ${b.orientation.toUpperCase()}`, swap ? RED : BLUE, {bold:true})], 20));
  P.push(para([
    run(`Source: ${p.uploader} (${p.source_type}, ${p.platform})  —  `, BLUE),
    new ExternalHyperlink({link:p.flagged, children:[
      new TextRun({text:p.flagged, color:BLUE, underline:{}, size:BODY_SIZE})]}),
  ], 20));
  for (const s of p.segments) {
    P.push(para([run(`IN ${s.in}   OUT ${s.out}   outcue: “${s.outcue}”`, BLUE, {bold:true})], 20));
  }
  P.push(para([run(`“${p.title}”`, BLUE, {italics:true})], 20));
  if (p.butt_cut_with) {
    P.push(para([run(`⧉ BUTT-CUT: same source as ${p.butt_cut_with.toUpperCase()} — pull the file once, cut two slices.`, BLUE, {italics:true})], 20));
  }
  P.push(para([run("✓ Outcue verified verbatim against the auto-caption transcript.", BLUE, {italics:true})], 20));
  if (swap) {
    P.push(para([run(`⚠ CASE-SWAP: ${p.script_change}`, RED, {italics:true})], 140));
  } else {
    P.push(para([], 140));
  }
  return P;
}

// ------------------------------------------------------------------ doc
const paras = [];
paras.push(new Paragraph({spacing:{after:80}, children:[
  new TextRun({text:"F2 BIBLE — FRIDAY, AUGUST 7", bold:true, size:TITLE_SIZE})]}));
paras.push(new Paragraph({spacing:{after:200}, children:[new TextRun({
  text:"Bible with clips embedded. Blue = clip to pull (IN/OUT + verbatim outcue). Red = case-swap, show-produced beat, or a clip shipping without a verified timecode. Clips were located and timecoded for a human to pull and cut — nothing was downloaded or auto-cut.",
  italics:true, size:BODY_SIZE, color:GREY})]}));

let ci = 0;
for (let i = 0; i < lines.length; i++) {
  const l = lines[i];
  if (l.includes("PLAY CLIP")) {
    for (const p of clipParas(ORDER[ci])) paras.push(p);
    ci++;
    if (i+1 < lines.length && lines[i+1].trim().startsWith("OUT:")) i++;
    // drop the producer's stale note under b04's marker; the clip block says it now
    if (i+1 < lines.length && lines[i+1].trim().startsWith("[NOTE:")) i++;
    continue;
  }
  if (l.trim() === "BUTT") continue;
  if (l.trim() === "") { paras.push(new Paragraph({children:[]})); continue; }
  if (l.includes("[[SWAP")) {
    const idx = l.indexOf("[[SWAP");
    paras.push(new Paragraph({spacing:{after:40}, children:[
      new TextRun({text: l.slice(0, idx).trim()+"  ", bold:true, size:BODY_SIZE}),
      new TextRun({text: l.slice(idx), color:RED, italics:true, size:BODY_SIZE})]}));
    continue;
  }
  const isHeader = /^[A-Z0-9]/.test(l.trim()) && !l.trim().startsWith('-') && !l.startsWith('(((');
  paras.push(new Paragraph({spacing:{after:40}, children:[
    new TextRun({text:l, bold:isHeader, size:BODY_SIZE})]}));
}

const doc = new Document({sections:[{properties:{page:{size:{width:12240,height:15840}}}, children:paras}]});
Packer.toBuffer(doc).then(b => {
  const out = RUN + '/F2_BIBLE_FRIDAY_08072026_FILLED.docx';
  fs.writeFileSync(out, b);
  console.log("wrote", out, b.length, "bytes;", ci, "clip blocks emitted");
});
