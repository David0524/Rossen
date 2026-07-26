const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink } = require('docx');
const RUN = '/home/user/Rossen/runs/FRIDAY_08072026';
const lines = fs.readFileSync(RUN + '/script.txt', 'utf8').split('\n');

const BLUE = "1155CC", RED = "C0392B", AMBER = "B7791F";

// clip blocks in marker order (clip 1..5). Only clip 1 was run this pass.
const clips = [
  {
    kind: "pick",
    role: "explainer_demo / creator_long / horizontal",
    src: "In the Black — \"DO THIS every time a Amazon package arrives late\" (270s)",
    url: "https://www.youtube.com/watch?v=_8W0-cK5XTQ",
    in: "1:02", out: "1:41", outcue: "worth a shot though",
    note: "Outcue verified against captions — phrase lands 1:39.6–1:41.5, immediately before “so let's get into how to do this.”"
  },
  { kind: "outofscope", role: "VERTICAL", url: "https://www.tiktok.com/@johnsfinancetips/video/7028390544061730095", in: "0:00", out: "0:30", outcue: "thank you" },
  { kind: "outofscope", role: "VERTICAL", url: "https://www.tiktok.com/t/ZP8tHoohG/", in: "0:00", out: "0:52", outcue: "around this time" },
  { kind: "outofscope", role: "HORIZONTAL — $12,000 tiny home, denied twice", url: "https://abc7.com/post/socal-woman-asks-for-help-after-spending-12k-on-tiny-home-that-never-arrived/15409472/", in: "0:22", out: "1:55", outcue: "was denied twice" },
  { kind: "outofscope", role: "VERTICAL — Latest on the $309.5M returns settlement", url: "https://www.tiktok.com/t/ZP8txTTEr/", in: "0:00", out: "0:27", outcue: "after a refund." },
];

function run(text, color, opts = {}) {
  return new TextRun({ text, color, bold: opts.bold, underline: opts.underline ? {} : undefined });
}

function clipParas(c) {
  const P = [];
  if (c.kind === "pick") {
    P.push(new Paragraph({ spacing: { before: 100, after: 20 },
      children: [run("▶ CLIP 1 — " + c.role, BLUE, { bold: true })] }));
    P.push(new Paragraph({ spacing: { after: 20 },
      children: [run("Source: " + c.src, BLUE)] }));
    P.push(new Paragraph({ spacing: { after: 20 },
      children: [new ExternalHyperlink({ link: c.url, children: [run(c.url, BLUE, { underline: true })] })] }));
    P.push(new Paragraph({ spacing: { after: 20 },
      children: [run("IN " + c.in + "   OUT " + c.out + "   outcue: “" + c.outcue + "”", BLUE, { bold: true })] }));
    P.push(new Paragraph({ spacing: { after: 140 },
      children: [run("✓ " + c.note, BLUE)] }));
    return P;
  }
  // clips 2-5: not processed this run, draft values retained untouched
  P.push(new Paragraph({ spacing: { before: 100, after: 20 },
    children: [run("▶ CLIP — " + c.role + "   (NOT RUN THIS PASS — clip 1 only; draft value retained, unverified)", RED, { bold: true })] }));
  P.push(new Paragraph({ spacing: { after: 20 },
    children: [new ExternalHyperlink({ link: c.url, children: [run(c.url, RED, { underline: true })] })] }));
  P.push(new Paragraph({ spacing: { after: 140 },
    children: [run("IN " + c.in + "   OUT " + c.out + "   outcue: “" + c.outcue + "”", RED)] }));
  return P;
}

const paras = [];
paras.push(new Paragraph({ spacing: { after: 60 },
  children: [new TextRun({ text: "AMAZON OWES YOU MONEY — FRIDAY, AUGUST 7  (clips embedded)", bold: true, size: 28 })] }));
paras.push(new Paragraph({ spacing: { after: 200 },
  children: [run("Pipeline run scoped to CLIP 1 only — its outcue is caption-verified. Clips 2-5 carry their draft values and were not searched or verified.", AMBER, { bold: true })] }));

let ci = 0;
for (let i = 0; i < lines.length; i++) {
  const t = lines[i].replace(/\r/g, '');
  const isClipMarker = /\(\(\(PLAY CLIP \d/.test(t) || /^CLIP \d+ [—-]/.test(t.trim());
  if (isClipMarker) {
    for (const p of clipParas(clips[ci])) paras.push(p);
    ci++;
    // consume the draft url / IN-OUT / OUTCUE lines that follow the marker
    let j = i + 1;
    while (j < lines.length) {
      const n = lines[j].trim();
      if (n === '' || /^https?:\/\//.test(n) || /^IN\s+\d/.test(n) || /^OUTCUE:/.test(n)) { j++; continue; }
      break;
    }
    i = j - 1;
    continue;
  }
  if (t.trim() === '') { paras.push(new Paragraph({ children: [] })); continue; }
  const isHeader = /^[A-Z0-9]/.test(t.trim()) && !t.trim().startsWith('-') && !t.startsWith('(((');
  paras.push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: t, bold: isHeader })] }));
}

const doc = new Document({ sections: [{ properties: { page: { size: { width: 12240, height: 15840 } } }, children: paras }] });
Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(RUN + '/FRIDAY_08072026_BIBLE_updated.docx', b);
  console.log('wrote docx,', ci, 'clip blocks,', paras.length, 'paragraphs');
});
