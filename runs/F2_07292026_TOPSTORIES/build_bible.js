// Build the filled Bible .docx for F2 07/29/2026 TOP STORIES.
//
// Clip data is read from picks.json, not hand-copied, so the doc cannot drift
// from the graded output. At each (((PLAY CLIP))) marker the marker and its
// following bare "OUT:" line are replaced by a clip block:
//   - pick        -> blue hyperlink + IN/OUT + verbatim outcue
//   - manual      -> blue hyperlink marked MANUAL CLIP, no invented timecode
//   - broll       -> blue hyperlink + window, no outcue (picture only)
//   - empty       -> red "no clip found" line with the reason
// Script setup lines are left exactly as written: every swap in this run
// touches what the show says, so those are the producer's call, not ours.
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink } = require('docx');

const RUN = '/home/user/Rossen/runs/F2_07292026_TOPSTORIES';
const BLUE = '1155CC', RED = 'C0392B', AMBER = 'B8860B';

const picks = JSON.parse(fs.readFileSync(RUN + '/picks.json', 'utf8'));
const byBeat = {};
picks.forEach(p => { byBeat[p.beat_id] = p; });

// Marker order b01..b12 maps to the 12 PLAY CLIP markers in script order.
const ORDER = ['F2t-b01', 'F2t-b02', 'F2t-b03', 'F2t-b04', 'F2t-b05', 'F2t-b06',
               'F2t-b07', 'F2t-b08', 'F2t-b09', 'F2t-b10', 'F2t-b11', 'F2t-b12'];

// Beats whose exact case exists only off captioned YouTube get the manual lane
// alongside the graded pick, so the producer sees both.
//
// URLs are resolved from candidates.json by video_id rather than written out
// here. Hand-typing them produced two wrong article-ID suffixes on the first
// pass; a link in a shooting document has to be the link that was actually
// harvested, not one reconstructed from a pattern.
const cands = JSON.parse(fs.readFileSync(RUN + '/candidates.json', 'utf8'));
const urlById = {};
cands.forEach(c => { urlById[c.video_id] = c.url; });

function altUrl(vid) {
  const u = urlById[vid];
  if (!u) { console.error('MISSING URL for ' + vid); process.exit(1); }
  return u;
}

const MANUAL_ALT = {
  'F2t-b06': { src: 'ABC13 Houston (the exact 2018 package)', vid: 'u3fa6e227e05be86',
    note: 'MANUAL CLIP — no captions. This is the package the script was written to. Pull the in/out by eye; no timecode is given here because none can be verified.' },
  'F2t-b08': { src: 'KTVB / Tegna wire (the two-deaths version)', vid: 'u421d8b48f346666',
    note: 'MANUAL CLIP — no captions. Carries the two deaths and the 122,000 figure the flagged clip does not. Pull by eye.' },
  'F2t-b11': { src: 'WBNS 10TV (158s, the longer package)', vid: 'ud515ebd42a9267f',
    note: 'MANUAL CLIP — no captions. Longer cut of the same sentencing; check whether it carries a sheriff or prosecutor soundbite the flagged 71s cut lacks.' },
  'F2t-b12': { src: 'FTC press release (the script\'s own fallback)', vid: 'u22773b374d84d36',
    note: 'No video exists. Fullscreen this and read it, as the script already plans.' },
};
Object.values(MANUAL_ALT).forEach(a => { a.url = altUrl(a.vid); });

function run(text, color, opts) {
  opts = opts || {};
  return new TextRun({ text: text, color: color, bold: !!opts.bold,
                       italics: !!opts.italics,
                       underline: opts.underline ? {} : undefined });
}
function para(children, after) {
  return new Paragraph({ spacing: { before: 60, after: after === undefined ? 60 : after },
                         children: children });
}

function clipBlock(beatId) {
  const p = byBeat[beatId];
  const out = [];
  const label = p.clip_role + ' / ' + (p.orientation === 'vertical' ? 'VERTICAL' : 'horizontal')
              + '  ·  priority ' + p.priority;

  if (!p.flagged) {
    out.push(para([run('▶ NO CLIP — ' + beatId + '  (' + label + ')', RED, { bold: true })], 20));
    out.push(para([run(p.no_pick_reason, RED)], 20));
    out.push(para([run('Query that would find better: ' + p.suggested_query, RED, { italics: true })], 40));
  } else {
    const isBroll = p.outcue_required === false;
    out.push(para([run('▶ CLIP — ' + beatId + '  (' + label + ')'
                       + (isBroll ? '   [PICTURE ONLY — JEFF TALKS OVER]' : ''),
                       BLUE, { bold: true })], 20));
    out.push(para([
      run('Source: ' + (p.uploader || '') + '  —  ', BLUE),
      new ExternalHyperlink({ link: p.flagged,
        children: [run(p.flagged, BLUE, { underline: true })] }),
    ], 20));
    out.push(para([run('“' + p.title + '”', BLUE, { italics: true })], 20));

    p.segments.forEach((s, i) => {
      const tag = p.segments.length > 1 ? ('BUTT ' + (i + 1) + '/' + p.segments.length + '   ') : '';
      if (s.outcue === null) {
        out.push(para([run(tag + 'IN ' + s.in + '   OUT ' + s.out
                           + '   (no outcue — picture only)', BLUE, { bold: true })], 20));
      } else {
        out.push(para([run(tag + 'IN ' + s.in + '   OUT ' + s.out, BLUE, { bold: true }),
                       run('   outcue: “' + s.outcue + '”', BLUE)], 20));
      }
    });

    // Flags that change what a producer does get amber, not blue.
    (p.ranked[0].flags || []).forEach(f => {
      out.push(para([run('⚠ ' + f, AMBER, { bold: true })], 20));
    });
    if (p.producer_notes && /SWAP|DISCREPANCY|CAVEAT|corrections|PICTURE ONLY/.test(p.producer_notes)) {
      out.push(para([run('⚠ ' + p.producer_notes, AMBER)], 20));
    }
  }

  const alt = MANUAL_ALT[beatId];
  if (alt) {
    out.push(para([run('▶ ALSO — ' + alt.src, BLUE, { bold: true })], 20));
    out.push(para([
      new ExternalHyperlink({ link: alt.url,
        children: [run(alt.url, BLUE, { underline: true })] }),
    ], 20));
    out.push(para([run(alt.note, BLUE, { italics: true })], 120));
  }
  return out;
}

const lines = fs.readFileSync(RUN + '/script.txt', 'utf8').split('\n');
const paras = [];
paras.push(new Paragraph({ spacing: { after: 120 }, children: [
  new TextRun({ text: '07/29 F2 BIBLE - TOP STORIES', bold: true, size: 30 }) ] }));
paras.push(new Paragraph({ spacing: { after: 240 }, children: [
  new TextRun({ text: 'WEDNESDAY · clips embedded · 12 beats · 11 flagged, 1 empty. '
    + 'Blue = clip cue. Red = no clip. Amber = needs your ruling before air.',
    italics: true, size: 20 }) ] }));

let ci = 0;
for (let i = 0; i < lines.length; i++) {
  const l = lines[i];
  if (l.includes('PLAY CLIP')) {
    clipBlock(ORDER[ci]).forEach(p => paras.push(p));
    ci++;
    if (i + 1 < lines.length && lines[i + 1].trim().startsWith('OUT:')) i++;
    continue;
  }
  if (l.trim() === 'BUTT') continue;           // structural marker, not script copy
  if (l.trim() === '') { paras.push(new Paragraph({ children: [] })); continue; }
  const t = l.replace(/\r/g, '');
  const isHeader = /^[A-Z0-9]/.test(t.trim()) && !t.trim().startsWith('-')
                   && !t.startsWith('(((');
  paras.push(new Paragraph({ spacing: { after: 40 },
    children: [new TextRun({ text: t, bold: isHeader })] }));
}

if (ci !== ORDER.length) {
  console.error('MARKER MISMATCH: filled ' + ci + ' of ' + ORDER.length);
  process.exit(1);
}

const doc = new Document({ sections: [{
  properties: { page: { size: { width: 12240, height: 15840 } } },
  children: paras } ] });
Packer.toBuffer(doc).then(b => {
  const out = RUN + '/F2_TOP_STORIES_07292026_BIBLE_FILLED.docx';
  fs.writeFileSync(out, b);
  console.log('wrote ' + out);
  console.log(ci + ' clip blocks, ' + paras.length + ' paragraphs');
});
