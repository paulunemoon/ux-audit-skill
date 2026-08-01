# D8 · Content & microcopy

> **When to read:** Every audit — copy is where the cheapest, highest-impact
> findings live, and it's the dimension where a recommendation can be delivered
> complete rather than described. Finding IDs: `COPY-nn`.
>
> **Rule for this dimension: when copy is the problem, write the replacement
> verbatim.** "Improve the error message" is not a finding; the new sentence is.
> Every judgment here is calibrated against the audience call (SKILL.md §0f).

## Table of contents
1. [COPY-A · Jargon, calibrated to the audience](#copy-a--jargon-calibrated-to-the-audience)
2. [COPY-B · Button and CTA labels](#copy-b--button-and-cta-labels)
3. [COPY-C · Vocabulary consistency](#copy-c--vocabulary-consistency)
4. [COPY-D · Error and empty-state copy](#copy-d--error-and-empty-state-copy)
5. [COPY-E · Headings, titles, and scanability](#copy-e--headings-titles-and-scanability)
6. [COPY-F · Tone and voice consistency](#copy-f--tone-and-voice-consistency)
7. [COPY-G · Decorative microcopy](#copy-g--decorative-microcopy)
8. [COPY-H · Numbers, dates, and units in prose](#copy-h--numbers-dates-and-units-in-prose)
9. [COPY-I · Mechanics](#copy-i--mechanics)
10. [COPY-J · Localization readiness](#copy-j--localization-readiness)
11. [COPY-K · Legal and required copy](#copy-k--legal-and-required-copy)
12. [Severity calibration](#severity-calibration-for-this-file)

---

## COPY-A · Jargon, calibrated to the audience

**Check.** List every domain term the interface uses. For each, ask whether the
audience (§0f) knows it *before* using the product. Mark the ones that are
internal vocabulary, the ones that are real domain terms, and the ones that are
invented brand words for standard concepts.

**Why it matters.** An unknown word at a decision point stops the user, and most
people won't leave to look it up — they guess, or they leave.

**Grade differently by audience.** This is the most common place an audit goes
wrong in both directions:

| | Expert | Mainstream | Mixed |
|---|---|---|---|
| **Real domain term** ("slippage", "idempotency", "titration") | Correct and efficient. **Flagging it is cargo-culting.** | Barrier. High finding on a core path unless explained at first use. | Use it, explain it once at first encounter. |
| **Internal vocabulary** ("Entity", "Principal", "Object", the team's name for a screen) | Still wrong — experts know the *domain*, not your org chart. | Wrong. | Wrong. |
| **Invented brand word for a standard thing** ("Nexus" for search, "Pulse" for the dashboard) | Costs a learning step for no gain. | Worse — no prior model to attach it to. | Worse. |
| **Over-simplification** ("your money thingy") | Patronising; costs credibility. | Fine. | Lead simple, expert term on disclosure. |

**Fails like.**
- A mainstream product using its data model as its vocabulary.
- A term appearing for the first time inside a confirmation dialog, undefined,
  at the moment of decision.
- Acronyms with no expansion on first use.
- Technical failure language leaking into user-facing copy ("null", "payload",
  "token expired", "request failed with status 500").
- An expert product padded with explanations of things every user knows.

**Fix.** For each flagged term: the replacement word, or the one-sentence
explanation and where it appears. Progressive disclosure for mixed audiences —
plain word in the label, precise term available on a help affordance.

---

## COPY-B · Button and CTA labels

**Check.** Read every button label out of context. Does it say what will happen
when pressed? Does the label match the heading of the screen it leads to? Are
there two buttons on the same screen whose labels don't distinguish them?

**Why it matters.** The label is what the user commits to. A generic label moves
the decision cost onto the surrounding text, which people don't read.

**Fails like.**
- `Submit`, `OK`, `Continue`, `Done`, `Go`, `Yes` where a verb+object would fit.
- `Save` and `Apply` on the same screen with no stated difference.
- A confirmation dialog offering `Yes` / `No` for a destructive action instead
  of naming it.
- `Cancel` used for both "close this dialog" and "cancel my subscription" — a
  genuinely dangerous ambiguity.
- `Learn more` as the only affordance on three different cards.
- A destructive button labelled neutrally (`Continue` for "delete").
- A label that doesn't survive its own loading state (label replaced by a
  spinner).
- Label wrapping mid-phrase, or an icon stranded above its word.

**Fix.** Verb plus object: `Delete forecast`, `Send invitation`, `Pay $147.00`.
In a confirmation, the primary button repeats the destructive verb so the dialog
is readable at a glance: `Delete` / `Keep`. Never `Cancel` for an operation
called cancellation — use `Close` for dismissal. Keep the label in the loading
state (`Saving…`) and reserve its width.

---

## COPY-C · Vocabulary consistency

**Check.** Pick the five most important nouns in the product. Track each across
nav, page titles, buttons, empty states, errors, tooltips, emails, and docs. Do
they use the same word everywhere? Does an action's past tense match its verb —
`Archive` → "Archived", not "Moved to storage"?

**Why it matters.** Two words for one thing makes users wonder whether they're
two things. It's a small cost, paid constantly, and it compounds into a product
that feels like it was built by people who didn't talk to each other.

**Fails like.**
- Nav says "Analytics", page says "Insights", email says "Report", docs say
  "Dashboard".
- `Delete` in one place, `Remove` in another, for the same operation.
- `Organization` / `Workspace` / `Team` / `Account` used interchangeably.
- Confirmation copy in a different register than the button that opened it.
- Singular/plural inconsistency in list headers and counts.

**Fix.** Produce the term inventory as a small table — current variants, the one
to standardize on, and where each appears. This is a strong candidate for the
Quick wins section: low effort, immediately visible, and it prevents the
inconsistency recurring because there's now a written answer.

---

## COPY-D · Error and empty-state copy

**Check.** Collect every error string and every empty-state string. Does each
say what happened, and what to do? Is any of them a raw code, a stack trace, or
a vendor message passed straight through? Does the tone blame the user?

**Why it matters.** These are read more carefully than any other copy in the
product, by users who are already stuck.

**Fails like.**
- `Error 500`, `ERR_VALIDATION`, `undefined`, a JSON fragment, a database
  constraint name.
- "Something went wrong." — with no retry and no detail.
- "You entered an invalid value." — blames, doesn't help.
- "No data" as an entire empty state.
- A cancellation reported as an error.
- Cutesy failure copy on something serious ("Oopsie! 🙈" on a failed payment).

**Fix.** Rewrite verbatim. The shape:

| Bad | Better |
|---|---|
| `Error: authentication failed` | `That password doesn't match. Try again, or reset it.` |
| `Something went wrong` | `We couldn't save your changes — the connection dropped. Your text is still here. Retry` |
| `No data` | `No invoices yet. They'll appear here once you send your first one. — Create invoice` |
| `Invalid input` | `Enter a date on or after today.` |
| `Error: operation cancelled` | `Cancelled. Nothing was changed.` |

Match the tone to the stakes: neutral and specific for a routine failure, plain
and unembellished for anything involving money, data loss, or safety.

---

## COPY-E · Headings, titles, and scanability

**Check.** Read only the headings on each screen, in order. Do they tell you
what the page is and what's on it? Do headings describe content or restate the
nav? Is body copy scannable — front-loaded, chunked, short paragraphs — or a
wall?

**Why it matters.** Nobody reads interfaces linearly. Headings are the interface
to the text, and if they carry no information the text may as well not exist.

**Fails like.**
- "Overview", "Details", "Information", "Settings" as every heading.
- A heading duplicating the nav label with nothing added.
- Long explanatory paragraphs where a list would work.
- The important sentence buried at the end of a paragraph.
- Marketing prose inside a functional screen.
- No heading hierarchy at all — everything one size, or heading levels chosen by
  appearance rather than structure (also a D12 finding).

**Fix.** Headings that carry information. Front-load the conclusion. Break prose
into lists where the content is a list. Keep functional screens functional.

---

## COPY-F · Tone and voice consistency

**Check.** Is the voice the same across the product, or does it shift between
screens — marketing enthusiasm on the landing, terse system language in the app,
apologetic in errors, jokey in empty states? Does the tone modulate correctly by
stakes (lighter in a success toast, plain in a payment confirmation)?

**Why it matters.** Inconsistent voice reads as inconsistent product. And humour
in the wrong place — a failed payment, a data-loss warning, a security prompt —
undermines the seriousness the moment requires.

**Fails like.**
- Playful empty states next to legalistic errors.
- First person plural in some copy, passive voice in others.
- Exclamation marks in a financial or medical context.
- Emoji in system-critical copy.
- A different register in emails and notifications than in the product.

**Fix.** Name the specific screens that fall outside the dominant voice, and say
which direction to move them. Note where tone must be plain regardless of the
product's general voice: money, deletion, security, health, legal.

---

## COPY-G · Decorative microcopy

**Check.** Look for copy that occupies space without carrying information: the
small pill above a headline ("✦ New", "Now live", "Introducing…"), reassurance
tags under CTAs ("No credit card", "Cancel anytime", "Free to start"), status
chrome ("● Live", "Beta", "Demo", "Preview") worn as decoration, and section
kickers that restate the heading. Ask of each: **does the user act differently
because this is here?**

**Why it matters.** Decorative microcopy is filler that dilutes the copy that
matters, and it's one of the clearest signals of an interface assembled from
templates rather than written.

**The distinction that matters:**
- **Earns its place** — a "● Live" indicator where data genuinely streams and
  the user needs to know it's current; a "Beta" badge where it changes what the
  user should trust; "No credit card required" where users would otherwise
  reasonably assume one is.
- **Doesn't** — the same elements as ambient texture, to make a section "feel
  finished".

**Fails like.**
- An eyebrow pill above every H1 on a marketing page.
- A pulsing "Live" dot on static or trivially-changing data.
- A "Beta" pill on a product that shipped two years ago.
- Reassurance tags under buttons where nothing was at stake.
- Status conveyed by a coloured dot with no label (also a D12 failure).

**Fix.** Remove the ones that carry nothing. For the ones that stay, make them
specific ("Beta — data may reset weekly") and never colour-only.

---

## COPY-H · Numbers, dates, and units in prose

**Check.** Where copy contains a number, a date, a duration, or a unit: is it
unambiguous? Does a relative time ("2 days ago") also give the absolute on
hover or nearby? Are currencies labelled? Are units stated?

**Why it matters.** Ambiguity here causes concrete mistakes — the wrong date, the
wrong currency, the wrong quantity — not just confusion.

**Fails like.**
- `03/04/2026` with no indication of the format (D/M or M/D).
- "$" with no indication whether it's USD, CAD, AUD.
- "Expires in 30 days" with no date.
- "Last updated recently".
- A quantity with no unit.
- A timestamp with no timezone in a product used across timezones.

**Fix.** Absolute dates in an unambiguous format (`4 Mar 2026`) alongside
relative ones; currency codes where more than one is possible; explicit units;
timezone on anything a user might coordinate around. Formatting rules for
tabular data are in `data-display.md`.

---

## COPY-I · Mechanics

**Check.** Sentence case or title case — consistently, one or the other. No
typos. No placeholder text (`Lorem ipsum`, `TODO`, `Coming soon`) in shipped UI.
Consistent punctuation of list items, labels, and helper text. Consistent use of
sentence-ending periods in short strings.

**Why it matters.** Individually trivial, collectively a legibility and
credibility problem. Placeholder text in production is a category of its own —
it reads as unfinished and, in a trust-sensitive product, as unsafe.

**Fails like.** Mixed casing in one nav; typos in high-traffic labels; `Lorem
ipsum` on a live page; some helper texts ending in a period and some not; a
stray `{{variable}}` or `undefined` in rendered copy.

**Fix.** State the convention (sentence case is the usual right answer for UI)
and list the exceptions to fix. Placeholder text in production is always at
least a Medium finding, and a High one on any page a customer sees before
signing up.

---

## COPY-J · Localization readiness

**Check.** Only if the product is or plans to be localized. Are strings
externalized or concatenated in code? Do layouts survive strings 30–40% longer?
Are dates, numbers, currencies, and names formatted per locale? Is any meaning
carried by a word order that won't survive translation?

**Fails like.** Sentences assembled from fragments ("You have " + n + " items"),
which break in languages with different plural rules and word order; fixed-width
buttons sized to English; hard-coded date formats; flags used to mean languages;
no RTL consideration in a product shipping to RTL locales.

**Fix.** Full-sentence keys with interpolation and plural forms; flexible
layouts; locale-aware formatting. If the product isn't localized and has no
plan to be, skip this — don't pad the audit.

---

## COPY-K · Legal and required copy

**Check.** Does the product have Terms, Privacy, and (where applicable) cookie
and consent copy — and do the links work? Is consent language accurate about
what's collected? Is required regulatory disclosure present and legible rather
than buried at 10px grey-on-grey?

**Why it matters.** This is a trust and compliance dimension as much as a copy
one, and its absence is a concrete finding, not a nitpick. See
`trust-and-dark-patterns.md` for consent-pattern checks.

**Fails like.** Missing or 404ing Terms/Privacy on a product collecting personal
data; consent copy that describes less than what's actually collected;
disclosure rendered at a contrast that fails AA; "By continuing you agree to…"
with no link.

**Fix.** Present, linked, legible. Flag missing legal pages explicitly — this is
one of the few findings a team can't argue is taste.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Copy that causes an irreversible mistake (`Cancel` meaning two things on a destructive path) | **Blocker** |
| Missing Terms/Privacy on a product collecting personal data | **High** |
| Raw error codes or stack traces shown to users | **High** |
| Untranslated jargon at a decision point, mainstream audience | **High** |
| Destructive button labelled neutrally | **High** |
| Placeholder text (`Lorem ipsum`, `TODO`) on a customer-facing page | **High** |
| Generic CTA labels on core actions | **Medium** |
| Vocabulary inconsistency across the product | **Medium** |
| Empty-state copy with no action | **Medium** |
| Ambiguous dates, currencies, or units | **Medium** (**High** where a mistake costs money) |
| Tone inconsistency | **Low**–**Medium** by stakes |
| Decorative microcopy | **Low** |
| Casing and punctuation inconsistency | **Low** |
| Voice preferences within a consistent register | **Low** — taste; label it |
