# JEFF PLEASE NOTE comments

Jeff often sees the story minutes before he goes on. Some facts don't belong in
the script but he still has to know them, or a live chat question or an ad-lib
catches him out. Those go in a **Word comment anchored on the line they
concern**, opening with `JEFF PLEASE NOTE:`.

Write one when a fact would change **how Jeff says a line or answers a live
question**, and saying it on air would be wrong, confusing or off-story:

- **A nuance that guards a line.** "Medicare cards are paper" — but private
  plan cards are often plastic and legitimate; if the chat says "mine is
  plastic," he must not call it fake.
- **The limit of a number.** "More than a million" is one industry analysis,
  not CMS — don't round it up or call it official. Outlets disagree on a
  company's count, which is why the copy gives none.
- **What we deliberately left out, and why.** The new cards are going out
  because of a data breach; we kept it out of the script, but if asked, that's
  the answer.
- **Who is talking.** The guest's company is a sponsor, so "our advice isn't
  driven by commission" is their claim, not ours.
- **Story context he'd otherwise lack.** What happened before or after the clip,
  a victim's situation the clip doesn't explain, a legal status (arrested, not
  charged).

Rules:

- **Short and top-loaded** — one or two sentences, the point first. He reads it
  in the minutes before air. The checker warns over 45 words.
- **Anchored, not floating.** Put it on the exact line it guards. In the
  markdown draft, append it to that line: `-YOUR CARD IS PAPER.
  {{JEFF PLEASE NOTE: Private plan cards are often plastic and real. If the chat
  says "mine's plastic," that's fine.}}` `build_bible.py` turns it into a Word
  comment; it never prints in the copy.
- **Not a dumping ground.** Verification status and URLs stay in the source log;
  staging and preference calls stay as red `(((DECIDE …)))` / `(((JEFF - …)))`
  open decisions. A comment is background for Jeff, not a question to him.
- **Judgment, not quota.** Most stories need one to three. Don't comment a line
  that's self-explanatory.

### The aphorism trap

These all came out of one draft:

> A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS. REMEMBER THAT.
> THAT IS BRILLIANT, AND IT IS EVIL.
> THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.

Well-built lines — that is the problem. Each is a constructed symmetry that
collapses the moment Jeff paraphrases it. The aired equivalent is `THIS IS
GENIUS AND SCARY!!` — a **reaction cue**. It tells Jeff how to feel about the
fact above it and leaves the wording to him. If a line would sit comfortably in
a well-edited magazine article, cut it.

#### The paraphrase test

A permitted mechanism reveal and a banned aphorism look almost identical. **Say
the line in flat plain words. If the point survives, the contrast was in the
facts — keep it. If the point evaporates, the contrast was in the sentence — cut
it.**

| Line | Said flatly | Verdict |
|---|---|---|
| `EVERY OTHER SCAM TEXT THREATENS YOU. THIS ONE GIVES YOU SOMETHING.` | "unlike the others, this one offers you money" | **Keep.** A fact about the scam. |
| `YOUR GUARD DROPS, BECAUSE NOBODY EXPECTS FREE MONEY TO BE THE TRAP.` | "people don't suspect free money" | **Keep.** |
| `A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS.` | "they're different things" | **Cut.** The line was the point. |
| `THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.` | "this affects all of them" | **Cut.** |

**Watch for this when adding intensity.** A draft told to add spikes reaches for
sentence architecture (`NOT TWENTY DOLLARS. NOT FIVE. ZERO.`). **Intensity comes
from punctuation, caps and bold, which survive paraphrase — never from a built
sentence.** `check_bible.py` lists aphorism candidates; run the test on each.
