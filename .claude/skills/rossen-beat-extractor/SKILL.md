---
name: rossen-beat-extractor
description: Segment a Rossen Reports live show script into clip beats, assign a clip role and visual spec to each, and emit structured beat records for downstream clip search. Use this whenever a Rossen Reports script, rundown, or show doc is provided and the user wants beats extracted, clips sourced, a clip pull list built, or asks anything like "what clips do I need for this script." Also use when back-filling an eval set from past scripts that already contain aired clip URLs and timecodes.
---

# Rossen Reports beat extractor

Turn a finalized show script into a list of clip beats. One beat equals one moment where a clip rolls. Downstream, each beat gets searched on four platforms, so the beat record has to carry enough context that a search engine can find footage the script never names.

The script is always upstream and finalized. Never infer that a clip existed first.

## Input

A `.docx` or plain text script. Convert with `pandoc -t plain --wrap=none`. Scripts are near-entirely uppercase, dash-bulleted, and carry production markers in triple parens.

**`pandoc` is frequently not installed** — this has hit multiple independent runs of this pipeline. Check with `which pandoc` before relying on it. Fallback: unzip the `.docx` and extract `word/document.xml` with Python's `zipfile`, then strip the XML tags:

```python
import zipfile, re
from xml.etree import ElementTree as ET
z = zipfile.ZipFile("script.docx")
xml = z.read("word/document.xml").decode("utf-8")
ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
tree = ET.fromstring(xml)
lines = ["".join(n.text or "" for n in p.iter(ns + "t")) for p in tree.iter(ns + "p")]
script_text = "\n".join(lines)
```

This loses pandoc's paragraph-style hints (bold, headers) but preserves every line and marker, which is all the extraction below needs.

## Markers, and what each one means

| Marker | Meaning |
|---|---|
| `(((PLAY CLIP XXX HORIZONTAL)))` | A beat. Landscape source. In every observed case this resolved to YouTube or a news site. |
| `(((PLAY CLIP XXX VERTICAL)))` | A beat. Portrait source. In every observed case this resolved to TikTok or Facebook video. |
| `(((TAKE ... SCREENSHOT)))` | **Not a beat.** Still image, sourced separately. Skip. |
| `(((CREATE FULL SCREEN GRAPHIC)))` | **Not a beat.** Art department. Skip. |
| `WHOLE CLIP` | Segment runs start to end. |
| `:38-2:01 (THIS IS WHAT THE SCAMMERS DID)` | In point, out point, and the outcue phrase spoken at the out point. |
| `BUTT` | Butt-cut. The segments above and below come from the **same source** and are stitched. One clip, many segments. |
| `TEASE`, `SPONSOR`, `CHAPTER` | Non-beat production blocks. Skip. |

The orientation marker is producer-authored ground truth. **Treat it as a hard constraint on the platform list, not a hint.** Horizontal beats never search TikTok. Vertical beats never search YouTube long-form.

## Two structural traps

**The cold open.** Every script opens with a rundown block that restates each segment in tease language. It contains no `PLAY CLIP` markers but reads like beat text. Everything before the first `HIT LIKE AND SUBSCRIBE` or `JOIN THE CHAT` line is tease. Drop it. If you extract beats from it you will roughly double the beat count with unresolvable duplicates.

**Mid-show teases.** Blocks headed `TEASE // SPONSOR` or `TEASE//CHAPTER SPONSOR BREAK` restate upcoming segments. Same rule: no clip beat lives inside them.

## Extracting beat text

Walk backward from the `PLAY CLIP` marker, collecting dash-bulleted lines, and stop at whichever comes first: the previous clip block, a section header, or a sponsor or tease block. Six to ten lines is typical.

Keep the whole run. The specific dollar figure, the relationship, the object, the location, and the current-events anchor are all in there and all of them are searchable. `THIS COUPLE LOST $850,000` and `A RETIRED POLICE OFFICER JUST LOST NEARLY $10,000` are the two most searchable strings in their respective beats.

**Pull the news anchor separately.** Several beats exist because a dated event happened: a $232 million EU fine against Temu, the Spirit Airlines shutdown, Maryland banning dynamic pricing. When the beat text names a company, a dollar figure, an agency, a state, or a regulatory action, put it in `news_anchor`. The query generator searches that string directly and it is usually the single highest-recall query in the whole set.

## Clip roles

Seven roles. The first four are the show's bread and butter.

**`victim_interview`** — A person describing what was taken from them. Local affiliate package, occasionally national. Horizontal, YouTube or affiliate site. The largest single share of what airs. Lead-in tells: *listen to what happened to him*, *think what you would do if you were her*, *this woman lost*.

**`confrontation_bust`** — Someone catching the scammer live, or law enforcement running a sting, or a reporter confronting the operator. Rossen loves these and they close segments. Either orientation. Lead-in tells: *watch what happens when*, *he set up a real sting*, *busted one of them in the act*, *and confronts the seller*.

**`evidence`** — The artifact itself. Doorbell cam, security cam, fire damage, a screen recording of the scam message, a photo of the destroyed product. Usually vertical, TikTok or Facebook. Lead-in tells: *have a look*, *here you can see*, *this is the family's first reaction*.

**`explainer_demo`** — Someone showing how the scam works or how to defend against it. Splits hard by platform and you must pick one:
- *creator_short* — 15 to 60 second vertical demo, TikTok or Reels. The pen test, the UV light trick.
- *creator_long* — multi-minute horizontal walkthrough from a fraud-focused YouTube channel.

**`authority_report`** — Network news or wire coverage of a development. Not a victim, not an affiliate. Today.com, NBC, CNBC, Reuters. Lead-in tell: *here's what we know right now*. Note that these often live on network sites rather than YouTube, so flag `offsite_likely: true` and let the harvester know a plain YouTube search may not reach it.

**`debunk`** — A viral claim being disproven. Inverted search: you want the takedown, not the claim. Snopes, fact-check desks, local news debunk segments.

**`first_person_rant`** — Someone venting to camera about what happened to them. Vertical, TikTok. Distinct from `victim_interview` in that nobody is interviewing them.

If a beat genuinely fits none of these, emit `role: other` with a one-line description rather than forcing a fit. Forced fits corrupt the query generator downstream.

## Visual spec

One sentence describing what a producer would see in the thumbnail. This is what makes a contact sheet scannable, so write it for the eye, not for the search engine.

Good: `older couple seated at home, local news lower-third, interview setup`
Good: `handheld vertical, burned garage interior, daylight`
Bad: `footage related to FBI imposter scams`

## Output

One JSON object per beat.

```json
{
  "beat_id": "06-03-b03",
  "episode": "06-03",
  "segment_title": "SCAMMERS ARE IMPERSONATING THE FBI",
  "script_text": "FAKE US MARSHALLS KNOCK ON YOUR DOOR... / THEY SAY THERE'S A WARRANT FOR YOUR ARREST / ...THEN THEY TURN YOUR MONEY INTO GOLD BARS SO IT'S NOT TRACEABLE...AND DISAPPEAR.",
  "orientation": "horizontal",
  "clip_role": "victim_interview",
  "news_anchor": "US Marshals impersonation gold bars",
  "visual_spec": "victim on camera at home describing door knock, local affiliate interview setup",
  "platforms": ["youtube", "news_web"],
  "offsite_likely": false,
  "priority": 1,
  "expected_segments": 1
}
```

`priority` 1 means the segment does not work without this clip. 2 means supporting. 3 means nice to have. A beat that Jeff verbally sets up over three or more lines is priority 1.

`expected_segments` comes from counting `BUTT` markers when back-filling a past script. For a new script, default 1 and let the timecode extractor decide.

## Sourcability scan

Run this immediately after extraction, before handing beats to the query generator. The purpose is to catch dead-end beats early — victims who never did a TV interview, events too recent for YouTube — so the producer can swap or plan instead of discovering the gap at grading time.

### What to check

For every beat that names a specific person (`victim_interview`, `first_person_rant`, and any beat where the script says "listen to him/her" or "watch what she says"):

1. Run `yt-dlp --print id --print title "ytsearch5:FIRSTNAME LASTNAME scam"` (and a variant without "scam" if the name is distinctive enough).
2. If zero results mention the person → `sourcability: none`. The person has no video presence. This beat will be empty unless the show produces its own interview.
3. If results exist but are all creator commentary or narrated readouts (generic channel names, the person is discussed but never appears) → `sourcability: commentary_only`. There is coverage but no on-camera interview. Flag it.
4. If at least one result is from an affiliate or network and the title suggests an interview package → `sourcability: high`. Proceed normally.

For beats that reference an event, company, or regulatory action rather than a named person (`authority_report`, `evidence`, `debunk`):

1. Run `yt-dlp --print id --print title "ytsearch5:COMPANY_OR_EVENT scam"`.
2. These are almost always sourceable. Flag only if the event is very recent (within the last 2 weeks) and nothing surfaces.

For vertical beats, also check YouTube Shorts: `yt-dlp --print id --print title --match-filter "duration<60" "ytsearch5:TOPIC #shorts"`.

### Self-recorded beats: check the subject's own social first

If the script says the subject filmed themselves (*"he recorded this on his phone,"* *"she posted this to her followers,"* any `first_person_rant` where nobody is interviewing them) — before running any YouTube search, check whether the subject has a public Instagram, X, or TikTok account and whether they posted the clip there. A web search for `"NAME" instagram scam video` or `"NAME" posted video scam` usually surfaces it, often via press coverage that names the platform and date even when the exact permalink isn't indexable.

Tag this `source_native: instagram | x | tiktok | none`. When a native post exists, that is the pick — not a YouTube repost. Aggregator channels (New York Post, and AI-narrator repost channels) frequently carry the only *findable* copy on YouTube, but they either re-narrate over the subject's own audio or are DRM/bot-walled from download, and neither is a clean, clearable source. Hand the producer the direct link to the original post (or profile + date + caption fragment if the exact permalink can't be pinned) instead of scraping and cropping a repost.

### Output

Add two fields to every beat record:

```json
{
  "sourcability": "high | commentary_only | none | unchecked",
  "sourcability_note": "ABC7 Chicago affiliate package found with Owen on camera"
}
```

### What happens when sourcability is low

Do not silently proceed. Surface the problem in the Checkpoint 1 beat table with a row color or flag. The producer's options:

- **Swap victim.** The script says "listen to this woman who lost $400k." There are dozens of women who lost comparable amounts and DID do a TV interview. Suggest two or three with confirmed YouTube affiliate coverage. The script writer adjusts the name and dollar figure.
- **Mark as show-produced.** The show will interview this person themselves. Remove the beat from the clip pipeline entirely — it becomes a production task, not a search task.
- **Drop the beat.** If neither option works, cut it. An empty beat at Checkpoint 1 costs nothing. An empty beat discovered at Checkpoint 3 wasted every search and download in between.

### Why this matters

In the F2 pipeline run, three beats (b01, b04, b05) reached Checkpoint 3 as `flagged: null` after full search, download, and transcript grading. All three failures were predictable from a five-second YouTube search: the Winnebago County case was 15 days old with no YouTube upload, the Cook couple and Barry Heitin had only print coverage. The sourcability scan would have caught all three at Checkpoint 1 and saved the entire downstream effort.

## Back-filling past scripts

When the script already contains aired URLs and timecodes, also emit `aired_url`, `aired_platform`, and a `segments` array of in/out/outcue objects. These rows are the eval set. The outcue phrase is the verification anchor for the timecode extractor: a correct out point is one where the outcue text appears in the Whisper transcript within about a second of the proposed timestamp.

`reference/aired_examples.md` holds 24 worked beats from three episodes. Read it before extracting.
