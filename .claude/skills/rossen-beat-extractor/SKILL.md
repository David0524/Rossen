---
name: rossen-beat-extractor
description: Segment a Rossen Reports live show script into clip beats, assign a clip role and visual spec to each, and emit structured beat records for downstream clip search. Use this whenever a Rossen Reports script, rundown, or show doc is provided and the user wants beats extracted, clips sourced, a clip pull list built, or asks anything like "what clips do I need for this script." Also use when back-filling an eval set from past scripts that already contain aired clip URLs and timecodes.
---

# Rossen Reports beat extractor

Turn a finalized show script into a list of clip beats. One beat equals one moment where a clip rolls. Downstream, each beat gets searched on four platforms, so the beat record has to carry enough context that a search engine can find footage the script never names.

The script is always upstream and finalized. Never infer that a clip existed first.

## Input

A `.docx` or plain text script. Convert with `pandoc -t plain --wrap=none`. Scripts are near-entirely uppercase, dash-bulleted, and carry production markers in triple parens.

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

## Back-filling past scripts

When the script already contains aired URLs and timecodes, also emit `aired_url`, `aired_platform`, and a `segments` array of in/out/outcue objects. These rows are the eval set. The outcue phrase is the verification anchor for the timecode extractor: a correct out point is one where the outcue text appears in the Whisper transcript within about a second of the proposed timestamp.

`reference/aired_examples.md` holds 24 worked beats from three episodes. Read it before extracting.
