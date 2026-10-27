const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  ShadingType, HeadingLevel, AlignmentType, LevelFormat, BorderStyle, PageBreak,
} = require("docx");

const FONT = "Arial";
const INK = "1F2933", MUTED = "5B636D", RED = "C8102E", HEAD_FILL = "1F2933", ROW_FILL = "F3F4F6";
const TABLE_W = 9360; // 6.5in
const COLS = [3000, 2900, 2560, 900];

const p = (text, opts = {}) => new Paragraph({
  spacing: { before: 100, after: 120 }, ...opts.para,
  children: (Array.isArray(text) ? text : [text]).map(t =>
    typeof t === "string" ? new TextRun({ text: t, font: FONT, size: 21, color: INK, ...opts.run }) : t),
});
const b = (t) => new TextRun({ text: t, font: FONT, size: 21, bold: true, color: INK });
const r = (t) => new TextRun({ text: t, font: FONT, size: 21, color: INK });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 140 },
  children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: INK })] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 100 },
  children: [new TextRun({ text: t, font: FONT, size: 24, bold: true, color: RED })] });
const bullet = (parts) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60 },
  children: (Array.isArray(parts) ? parts : [parts]).map(t => typeof t === "string" ? r(t) : t) });

const border = { style: BorderStyle.SINGLE, size: 4, color: "D1D5DB" };
const borders = { top: border, bottom: border, left: border, right: border };
const cell = (text, w, { head = false, fill } = {}) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders,
  shading: fill ? { type: ShadingType.CLEAR, color: "auto", fill } : undefined,
  margins: { top: 70, bottom: 70, left: 100, right: 100 },
  children: String(text).split("\n").map(line => new Paragraph({ spacing: { after: 30 },
    children: [new TextRun({ text: line, font: FONT, size: head ? 18 : 18, bold: head,
      color: head ? "FFFFFF" : INK })] })),
});
const table = (rows) => new Table({
  width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: COLS,
  rows: [
    new TableRow({ tableHeader: true, children: ["What", "Where to find it", "Format", "Priority"].map((h, i) =>
      cell(h, COLS[i], { head: true, fill: HEAD_FILL })) }),
    ...rows.map((row, k) => new TableRow({ cantSplit: true, children: row.map((c, i) =>
      cell(c, COLS[i], { fill: k % 2 ? ROW_FILL : undefined })) })),
  ],
});

const children = [
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "ROSSEN REPORTS", font: FONT, size: 18, bold: true, color: RED })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Audience Data Request: YouTube + Facebook", font: FONT, size: 40, bold: true, color: INK })] }),
  p("Prepared for the team, October 12, 2026. One-time pull, then a lighter weekly refresh.", { run: { color: MUTED } }),

  h1("Why we want this"),
  p("Today the scripts are tuned by notes and instinct: what Jeff, Ryan and TJ flag after the fact. This data lets us tune them to what our own audience actually does. Specifically:"),
  bullet([b("Titles and thumbnails: "), r("which wording and images earn clicks from our 55+ audience.")]),
  bullet([b("The first 60 seconds: "), r("where viewers leave the open, and which openings hold.")]),
  bullet([b("Story order and pacing: "), r("where viewers drop during a show (first clip, guest, sponsor read, deals), lined up against the bible.")]),
  bullet([b("Topics: "), r("which scam categories over- and under-perform, so pitches rank on evidence.")]),
  bullet([b("Facebook vs YouTube: "), r("whether the same story should be framed differently on each.")]),
  p("Aggregate numbers only. We don't need any viewer's personal information."),

  h1("How to send it"),
  bullet([b("Where: "), r("a shared Drive folder named \"Audience Data – Oct 2026\". Raw exports, not summaries.")]),
  bullet([b("Format: "), r("CSV or Google Sheets for numbers; PNG screenshots for graphs; image files for thumbnails.")]),
  bullet([b("Names: "), r("start each file with the platform and what it is, e.g. \"YT – per-video export – 12mo.csv\", \"FB – retention – 10-07 show.png\".")]),
  bullet([b("Date range: "), r("the last 12 months for exports. If that's too much, every live show since March 18, 2026.")]),
  bullet([b("Separate "), r("live streams and regular uploads. Their numbers aren't comparable.")]),
  bullet([b("Leave out revenue. "), r("Remove estimated revenue, RPM and CPM columns before sending. We only need audience numbers.")]),
  bullet([b("Don't send logins. "), r("If you'd rather grant access than export, see \"Ongoing access\" at the end.")]),
  p([b("What we already have, so please skip it: "), r("final titles, current thumbnails, show transcripts, and the bibles. We'll build the segment timestamps from the transcripts and send you a draft episode map to correct (section 3).")]),
  p([b("Priority key: "), r("MUST = we can't do the work without it. HIGH = big improvement. NICE = if it's easy.")]),

  new Paragraph({ children: [new PageBreak()] }),
  h1("1. YouTube"),
  p("Everything below is in YouTube Studio → Analytics. Most of it is in Advanced mode (\"See more\" / \"Advanced mode\" on any analytics card), which has an Export button at the top right. Metric names can vary slightly by account; the closest match is fine."),

  h2("1A. Per-video performance export"),
  table([
    ["One row per video, last 12 months, with: views, impressions, impressions click-through rate, average view duration, average percentage viewed, watch time (hours), unique viewers, subscribers gained and lost, likes, comments, shares", "Studio → Analytics → Advanced mode → Content tab → add metrics → Export", "CSV / Sheet", "MUST"],
    ["Same export, split by content type (live, videos, Shorts)", "Advanced mode → filter by content type, or the Content tab's Live / Videos / Shorts sub-tabs", "CSV / Sheet", "MUST"],
    ["Same metrics for the first 7 days after publish (so new and old videos compare fairly)", "Advanced mode → set the date range per video, or the \"first 7 days\" comparison if offered", "CSV / Sheet", "HIGH"],
    ["Returning vs new viewers per video", "Advanced mode → Audience tab, filtered per video", "CSV / Sheet", "HIGH"],
  ]),

  h2("1B. Audience retention (the most valuable piece)"),
  table([
    ["Audience retention graph for every live show since March 18. Not needed if we get API access (section 4). If screenshots are the only option, 20 shows spread across Wednesday, Friday, F2 and call-in, and across high and low views (not just the best and worst)", "Open a video → Analytics → Engagement → Audience retention. Screenshot the full graph with the time axis visible", "PNG per video", "MUST"],
    ["\"Key moments\" panel for the same videos (intro, top moments, spikes, dips). Needed even with API access: it gives the exact share still watching at 0:30", "Same screen, below the graph", "Screenshot", "MUST"],
    ["For 3 live shows: the retention graph twice, once filtered to \"On demand\" and once to \"Live & on demand\" (tells us whether the graph counts live viewers)", "Same screen → the view-type filter at the top", "Screenshot", "HIGH"],
    ["Relative retention (vs similar-length videos), if shown", "Same screen", "Screenshot", "HIGH"],
  ]),
  p([b("How we'll use it: "), r("we line each retention dip up against our timestamped transcript of the show, so we can see what was on screen when viewers left.")]),

  h2("1C. Packaging: titles and thumbnails"),
  p("We already have the current titles and thumbnails. What we can't see is what changed."),
  table([
    ["Any title or thumbnail changes after publish, with dates and the earlier version", "Team memory / change log / design files", "Sheet + image files", "MUST"],
    ["Thumbnail and title test results (\"Test & compare\"), if used", "Video → Analytics → Test results", "Screenshot", "HIGH"],
  ]),

  h2("1D. How people find us"),
  table([
    ["Traffic sources per video: browse, suggested, search, external, notifications, playlists", "Advanced mode → Traffic source tab, split by video", "CSV / Sheet", "HIGH"],
    ["Impressions and click-through rate by traffic source", "Advanced mode → Traffic source → add impressions + CTR", "CSV / Sheet", "HIGH"],
    ["YouTube search terms that brought viewers", "Advanced mode → Traffic source: YouTube search → terms", "CSV / Sheet", "HIGH"],
    ["Top suggested-video sources (which other videos send us traffic)", "Advanced mode → Traffic source: Suggested videos", "CSV / Sheet", "NICE"],
    ["External sources (Facebook, Google, newsletters)", "Advanced mode → Traffic source: External", "CSV / Sheet", "NICE"],
  ]),

  h2("1E. Who watches"),
  table([
    ["Age and gender, channel-wide and for the top and bottom 5 episodes", "Advanced mode → Demographics", "CSV / Sheet", "HIGH"],
    ["Top countries and US states / cities", "Advanced mode → Geography", "CSV / Sheet", "NICE"],
    ["Device type (TV, mobile, computer, tablet)", "Advanced mode → Device type", "CSV / Sheet", "HIGH"],
    ["When the audience is on YouTube (day and hour)", "Analytics → Audience tab → \"When your viewers are on YouTube\"", "Screenshot", "NICE"],
    ["Other channels and videos our audience watches", "Analytics → Audience tab", "Screenshot", "HIGH"],
  ]),
  p([b("Device matters more than it sounds: "), r("if a large share watches on a TV, small on-screen text and fast graphics don't land, and that changes how we write graphic cues.")]),

  h2("1F. Live shows"),
  table([
    ["Per live stream: peak concurrent viewers, average concurrent viewers, live watch time, live vs on-demand views, chat messages", "Video → Analytics (live streams show live metrics) or Advanced mode → Live", "CSV / screenshots", "HIGH"],
    ["Concurrent-viewer graph over the stream", "Video → Analytics → Engagement / Live", "Screenshot", "HIGH"],
    ["Chat export or a sample of chat (to see what questions viewers ask)", "Live chat replay, or a chat-export tool the team already uses", "Text / CSV", "NICE"],
  ]),

  h2("1G. Community"),
  table([
    ["Community tab post performance, if used", "Analytics → Content → Posts", "Screenshot", "NICE"],
    ["End screen and card click-through rates", "Advanced mode → End screen elements / Cards", "CSV / Sheet", "NICE"],
  ]),

  new Paragraph({ children: [new PageBreak()] }),
  h1("2. Facebook"),
  p("Everything below is in Meta Business Suite (or Professional Dashboard) → Insights → Content, which can export to CSV. Meta renames metrics often (e.g. \"impressions\" became \"views\" in many accounts); the closest match is fine."),

  h2("2A. Per-video performance export"),
  table([
    ["One row per video, last 12 months, with: reach, views (impressions), 3-second views, 1-minute views, ThruPlays (15-second views), average watch time, reactions, comments, shares, link clicks, follows gained", "Business Suite → Insights → Content → choose date range → Export", "CSV", "MUST"],
    ["Split organic vs paid/boosted (and which posts were boosted)", "Same export, organic/paid columns or filter", "CSV", "MUST"],
    ["What each post is: the full live show, a crosspost of the YouTube video, a different edit, or a clip", "Team knowledge / post type column", "Sheet column", "MUST"],
  ]),

  h2("2B. Retention"),
  table([
    ["Audience retention graph for the last 30 videos (or 20 spread across high and low views)", "Click a video in Insights → Video retention / \"Audience retention\" graph", "PNG per video", "MUST"],
    ["Retention by audience (followers vs non-followers), if shown", "Same screen", "Screenshot", "HIGH"],
    ["Average watch time and the share watched to 15 seconds and 1 minute", "Same screen / export", "CSV / screenshot", "HIGH"],
  ]),

  h2("2C. Packaging"),
  table([
    ["Caption / title and the thumbnail (cover image) each video ran with", "Each post, or the export's title/description columns", "Sheet + image files", "MUST"],
    ["Whether the Facebook version was edited differently from YouTube (shorter, captioned, different open)", "Editor", "Sheet column", "HIGH"],
  ]),

  h2("2D. Distribution and audience"),
  table([
    ["Where views came from: followers vs non-followers, feed, Watch, shares, groups, search", "Insights → video → Distribution / Audience", "Screenshot / CSV", "HIGH"],
    ["Audience age, gender, location", "Insights → Audience", "Screenshot / CSV", "HIGH"],
    ["Live videos: peak concurrent viewers, live vs replay views, comments during live", "Each live video → Insights", "Screenshot / CSV", "HIGH"],
    ["Reels: plays, average watch time, replays, follows", "Insights → Content → Reels", "CSV", "NICE"],
  ]),

  new Paragraph({ children: [new PageBreak()] }),
  h1("3. Our own records (to connect the data to the scripts)"),
  p("The platform numbers only become useful when each video is matched to what we made. We'll do most of this matching ourselves."),
  table([
    ["Corrections to our draft episode map (air date, F1/F2/call-in, YouTube URL, stories, guest, sponsor), plus the Facebook URL for each show", "We'll send the draft", "Edits in the sheet", "MUST"],
    ["The August 2026 back-catalog teardown sheet (the YouTube Studio analysis behind our channel facts), if it's still on file", "Content team files / Drive", "Sheet / link", "HIGH"],
    ["Notes after each show from Jeff, Ryan, TJ (emails or docs)", "Inbox / Drive", "Forward or link", "HIGH"],
    ["Thumbnail and title options that were considered but not used", "Design / producer files", "Images / sheet", "NICE"],
    ["Newsletter or other promotion per episode, if any", "Marketing", "Sheet", "NICE"],
  ]),

  h1("4. Read-only access (saves the most work)"),
  p("This saves the most work. With read-only access, nobody has to take retention screenshots (1B), now or each week:"),
  bullet([b("YouTube: "), r("add our account to the channel with a read-only role that can see analytics (Studio → Settings → Permissions). For full retention curves on every video, the channel owner can authorize the YouTube Analytics API once; it returns the retention curve for any video, which Studio can't bulk-export.")]),
  bullet([b("Facebook: "), r("grant analytics / insights access to the Page in Business Suite → Settings → People. The Meta Graph API can then pull per-video insights.")]),
  p("Either way: read-only, no ability to publish or change anything."),

  h1("5. Minimum version (if time is short)"),
  p("If the full list is too much this week, these five give most of the value:"),
  bullet("YouTube per-video export (1A), live shows and uploads separated, last 12 months."),
  bullet("Retention: API access (section 4), or screenshots for 20 shows spread across show types (1B), plus the Key moments panel."),
  bullet("Title and thumbnail changes after publish (1C)."),
  bullet("Facebook per-video export (2A), with what each post is (full show, crosspost, edit or clip)."),
  bullet("Corrections to our draft episode map, with Facebook URLs (section 3)."),
];

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1200, bottom: 1200, left: 1440, right: 1440 } } },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(process.argv[2], buf); console.log("wrote", process.argv[2]); });
