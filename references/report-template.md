# Report templates

> **When to read:** Before writing the report. SKILL.md §4 defines the structure
> and §3 the finding schema; this file is the shapes to fill in and the worked
> examples.
>
> Default deliverable: **a Markdown file** in the working directory, named
> `ux-audit-<scope>-<YYYY-MM-DD>.md` unless the user asks otherwise. Write the
> file; don't only print the report into the conversation.
>
> **Never write it into the home directory.** A description-only review often
> runs from `~` because there's no repo to be in — dropping a report there
> clutters somewhere the user doesn't curate. If the working directory is `~`
> or otherwise isn't a project, say where you're putting it and use a sensible
> subdirectory, or ask.

## Table of contents
1. [Full audit report](#full-audit-report)
2. [A worked finding](#a-worked-finding)
3. [Quick mode report](#quick-mode-report)
4. [Flow mode report](#flow-mode-report)
5. [Description-only review](#description-only-review)
6. [Accessibility mode report](#accessibility-mode-report)
7. [Tokens mode report](#tokens-mode-report)
8. [The state-coverage matrix](#the-state-coverage-matrix)
9. [Maturity ratings, if used](#maturity-ratings-if-used)
10. [Writing rules](#writing-rules)

---

## Full audit report

````markdown
# UX audit — <product or scope>

<one line: what was audited, when, by what means>

## 1. Scope & evidence base

**Audited:** <the flows, screens, or areas covered>
**Platform:** <website / web app / mobile app / desktop / hybrid>
**Audience:** <expert / mainstream / mixed> — <one line on how this was determined>
**Evidence:** <live URL at these viewports · Figma file/nodes · N screenshots ·
repo at commit X · description only>
**Dates:** <when the evidence was gathered — products change>

**Not audited, and why:**
- <area> — <no access / not in scope / not reproducible without production data>
- <state> — <couldn't trigger without a failing backend>

<If evidence was thin, say so here in one plain sentence rather than hedging
every finding. If any part of the requested scope went uncovered, say that here
too — this section is where partial coverage is disclosed, not inferred over.>

No conformance claim is made for accessibility; this is a sampled review.

## 2. Executive summary

<5–8 sentences. The three things that matter most, what they cost, and the
overall shape of the product's UX. Written for someone who will read only this
section. No lists, no hedging, no restatement of the scope.>

## 3. Quick wins

High impact, low effort. Each is independently shippable.

| ID | Finding | Dimension | Severity | Effort |
|---|---|---|---|---|
| A11Y-04 | Focus indicator removed globally by a CSS reset | Accessibility | High | S |
| FORM-02 | No `autocomplete` attributes on the signup form | Forms | High | S |
| NAV-07 | Four footer links 404 | Navigation | Medium | S |

## 4. Findings

### 4.1 <Dimension> — <n findings>

<Findings in the schema below, sorted Blocker → High → Medium → Low.>

### 4.2 <Dimension> — <n findings>

…

<Dimensions with no findings get one line: "**Data display** — no findings.
Numbers are formatted consistently, tabular figures are used throughout, and
timestamps carry timezones." Say what was checked, so the reader knows the
dimension wasn't skipped.>

## 5. Prioritized backlog

An ordered list. Work top to bottom.

| # | ID | What to do | Severity | Effort | Why it's here |
|---|---|---|---|---|---|
| 1 | FLOW-01 | Add a review step before the transfer is executed | Blocker | M | Users can send to the wrong recipient with no chance to catch it |
| 2 | A11Y-04 | Restore a visible focus indicator | High | S | Keyboard users cannot see where they are, anywhere in the product |
| 3 | … | | | | |

<Order by severity × frequency ÷ effort, then adjust by judgment and say where
you did. A Blocker behind a large refactor may sit below three High/S items that
ship this week — if you reorder for that reason, note it in a line beneath the
table.>

## 6. What's working, and what I left alone

Brief, and meant as calibration rather than balance.

**What's working.** <Two or three specifics, named precisely enough that the
team recognises them. A reader who sees only failures cannot tell whether you
understood the product, and cannot tell which of their decisions to keep.>

**What I left alone, and why.** <The things a reader might expect to see
flagged, that you deliberately didn't. "I left the single-mode palette, the
Manrope/Inter split, and the navbar's 32px radius alone — those read as
decisions, and I couldn't name a cost.">

This second part does more work than it looks. It pre-empts *"did you even
notice X?"*, it shows the taste discipline was applied rather than claimed, and
it tells the team which of their choices survived scrutiny — which is
information they cannot get from a list of defects.

## 7. Open questions

Things that need the team's data, or access I didn't have.

- **<Question>** — <why it matters, and what answer would change>
- **Hypothesis (unverified):** <phrased as a question> — <what evidence would
  settle it>

## Appendix — evidence log

<The SEEN / NOT SEEN list, with conditions. Optional but useful, and it makes
the audit reproducible.>
````

---

## A worked finding

The schema rendered as prose. Keep this density — enough to act on, no padding.

````markdown
#### FLOW-01 · No review step before a transfer executes

| | |
|---|---|
| **Dimension** | Core task flows (D3) |
| **Severity** | Blocker |
| **Confidence** | Observed (rendered + code) |
| **Effort** | M |
| **Location** | `/transfer` — compose screen; `TransferForm.tsx:88–142` |

**Evidence.** On `/transfer`, entering a recipient and an amount and pressing
**Send** executes immediately. No confirmation dialog, no summary screen. The
button label is "Send" throughout, and the only feedback is a success toast
reading "Transfer complete" 1–2 seconds later. Tested at 1440×900, signed in,
with a $10 transfer to a new recipient. `TransferForm.tsx:131` calls the
mutation directly from `onSubmit` with no intermediate state.

**Why it matters.** A transfer is irreversible. A user who mistypes an amount or
selects the wrong recipient from the autocomplete has no moment to notice before
the money leaves — the first they learn of the error is the success toast. The
recipient field autocompletes on a single keystroke, which makes selecting an
adjacent wrong contact a realistic slip rather than a hypothetical one.

**Recommendation.** Insert a review step between compose and execute, showing:
the recipient's full name and account (not truncated), the exact amount with
currency, any fee, and the total leaving the account. Primary button reads
**"Send $10.00 to Maria Chen"**; secondary is **"Back"**. Do not pre-focus the
primary. If a review screen is too heavy for small transfers, a confirmation
dialog carrying the same four facts is an acceptable lighter form — but the
generic "Are you sure?" is not, because it doesn't let the user check anything.

**Related.** FORM-05 (recipient autocomplete fires on one character),
ERR-02 (no undo window on transfers). Fixing FLOW-01 reduces the severity of
both.
````

**What makes this usable, and what to imitate:**
- The evidence is specific enough that someone can reproduce it.
- The consequence is concrete and tied to an observed detail (the aggressive
  autocomplete), not a general principle.
- The recommendation includes the actual button copy.
- The lighter alternative is offered, with the reason the cheap version fails.
- Related findings are named, so the team can batch.

---

## Quick mode report

**Ten findings maximum.** If the sweep surfaced more, report the ten that matter
and say how many were seen.

````markdown
# UX quick review — <product>

<what was looked at, for how long, with what access — two lines>

## The three things that matter most

1. **<Finding>** — <consequence in one sentence>
2. **<Finding>** — <consequence>
3. **<Finding>** — <consequence>

## Findings

| ID | Finding | Dimension | Severity | Confidence | Effort |
|---|---|---|---|---|---|
| NAV-01 | `/videos` deleted; four call sites still link to it | Navigation & IA | **Blocker** | Observed (code); 404 Inferred | S |
| A11Y-01 | Secondary text at 3.19:1, ~50 uses on the core path | Accessibility | High | Observed (measured) | S |
| FBK-01 | "Stop" button wired to the send handler; no-ops while streaming | Feedback & states | High | Observed (code) | M |
| STATE-01 | No empty state on the main list | State coverage | Medium | Inferred (no branch in code) | S |

**Fill the Confidence cell the same way** — it carries the source, and it splits
when the finding is part fact and part inference (SKILL.md §3). A column of
identical bare `Observed` in a sweep where nothing was run is the tell that the
label was typed rather than judged.

<One short paragraph per finding beneath the table: evidence, consequence,
fix. Three or four sentences each — no full schema blocks in quick mode.>

## Quick wins

<The subset that is High/Medium impact and S effort.>

---

*A heuristic sweep, not a full audit. <N> further issues were noted and not
reported here; the ten above are the ones worth acting on first. A full audit
would additionally cover <the dimensions not swept>.*
````

---

## Flow mode report

Structured by step rather than by dimension, because that's how the flow is
experienced and fixed.

````markdown
# Flow audit — <flow name>

**Entry point:** <where the flow starts>
**Goal state:** <what completion looks like>
**Steps observed:** <n> · **Required inputs:** <n> · **Exits available:** <n>

## The flow as observed

| # | Step | Required input | Decisions | Exit available | Notes |
|---|---|---|---|---|---|
| 1 | Landing → "Start" | — | — | Yes | |
| 2 | Account details | email, password, name | — | Back only | Password rules not shown up front |
| 3 | Verify email | 6-digit code | — | **No** | No resend; back loses account |
| … | | | | | |

## Findings by step

### Step 2 — Account details
<Findings in the full schema.>

### Step 3 — Verify email
<Findings.>

## Cross-cutting

<Findings that belong to the flow as a whole rather than any one step: total
step count, state loss across steps, inconsistent copy between steps.>

## The flow as it could be

<A revised step table. Which steps merge, which defer, which are removed, and
what the count becomes. This is usually the most useful artifact in a flow
audit — but only propose it where you have enough evidence to be concrete.>

## Prioritized backlog
## Open questions
````

---

## Description-only review

When there is no product to look at — no URL, no repo, no screenshot, no Figma —
the document is not an audit and must not be shaped like one. **Forcing a
description-only review into the standard structure produces an empty §2–§5 and
a §6 carrying everything**, which is unreadable. Change the shape instead:

````markdown
# UX review — <product> <!-- "review", never "audit" -->

## 1. Scope & evidence base

**Evidence available:** <a three-sentence description. No URL, no repo, no
Figma, no screenshot.>

**What that means, in one sentence:** I have seen no screen, so **there is not a
single observation in this document.** Only hypotheses and the questions that
settle them. <Name what you don't know: what a button says, what day one looks
like, whether an error state exists.> Ten minutes with the real product would
turn half of these into observations — and would invalidate some of them, which
is also information.

**What I could not assess at all:** <list the dimensions — usually nine or ten
of the sixteen.> No accessibility conformance claim is made.

**What reads as well judged, from the description alone:** <two or three
sentences. Say what's good even here — it shows you engaged with the product
rather than pattern-matching the category.>

## 2. The structural risk <!-- optional, when one dominates -->

<Some products have one problem that precedes every interface question. If there
is one, it goes here, before the list, and it is a product finding rather than a
UX one. Say so.>

## 3. Risks

Each is a hypothesis. **The severity shown is the severity if the risk is
confirmed** — not a judgment on the product as it stands.

**Nothing below Medium belongs here.** A Low hypothesis about a product nobody
has seen is speculation about polish — "their radius scale might be
inconsistent" — and it costs the reader's attention without being checkable.
A description-only review is legitimately top-heavy: raise only what is worth
raising blind. If a risk isn't worth the user opening the app to check, drop it.

#### H-FLOW-01 · <the risk, named as a claim>

| | |
|---|---|
| **Dimension** | <primary · secondary> |
| **Severity if confirmed** | **Blocker** |
| **Effort** | M |

**The risk.** <The mechanism, and the failure mode it produces. Be specific
about *how* it fails — a failure mode named precisely is what makes a hypothesis
worth checking.>

**The questions that settle it.** <Two or three questions someone with the
product open can answer in a minute.>

**If the answer is <the bad one>.** <The concrete change, conditional on the
answer. Copy rewrites verbatim, as always.>

## 4. What I'd do first
## 5. What I need to turn this into an audit

<The specific evidence, named: which screens, which states, which flows.>

---

*Review from a description, not an audit. No screen was observed. The risks
above are hypotheses drawn from the known traps of this product category — not
observed defects — and some will be invalidated by the first screenshot, which
is the point.*
````

**The five things that make this work:**
- **`H-` prefix on every ID.** The hypothesis is marked in the identifier, so it
  survives being quoted out of context into a ticket.
- **"Severity if confirmed"**, not "Severity" — and said again under the section
  heading. The grade is conditional and the field name says so.
- **"The questions that settle it"** replaces Evidence, which cannot exist here.
- **No Confidence column.** Every row would read `Hypothesis`; a column of one
  repeated value is noise. State the level once at the top and once at the
  bottom instead, prominently.
- **The closing note welcomes being wrong.** "Some will be invalidated by the
  first screenshot, which is the point" is the sentence that keeps the document
  honest, and it makes the ask for evidence land as collaboration rather than
  as a caveat.

## Accessibility mode report

Keyed to success criteria so it can be checked against a conformance obligation.

````markdown
# Accessibility audit — <product or scope>

**Standard:** WCAG 2.1 Level AA
**Scope:** <pages/flows tested>
**Method:** <manual keyboard pass · screen reader (which, on what OS) ·
contrast measurement · code review · automated tool output, if provided>
**Not tested:** <what, and why>

**This is a sampled review. It is not a conformance evaluation and no
conformance claim is made.**

## Summary

<3–5 sentences: the pattern of failures, not a count. "Focus management is the
systemic issue — it fails the same way in every custom component" is more useful
than "14 issues found".>

## Findings by criterion

### 1.4.3 Contrast (Minimum) — AA — **Fail**

| Location | Foreground | Background | Measured | Required |
|---|---|---|---|---|
| Secondary text, all screens | `#8A8F98` | `#F5F5F7` | 2.98:1 | 4.5:1 |
| Placeholder text, all inputs | `#A1A6AD` | `#FFFFFF` | 2.45:1 | 4.5:1 |
| "Warning" badge text | `#FFFFFF` | `#F0A500` | 2.08:1 | 4.5:1 |

**Affects.** Anyone with reduced contrast sensitivity, and everyone in bright
light. Placeholder text carries the format hint on three fields, so the
information is effectively unavailable.

**Fix.** `#65696F` on `#F5F5F7` measures 5.07:1 and remains one visible step in
from primary. The warning badge needs dark ink: `#1A1A1A` on `#F0A500` measures
8.36:1. Verified with `scripts/contrast-check.py`.

### 2.4.7 Focus Visible — AA — **Fail**
### 4.1.2 Name, Role, Value — A — **Fail**
### 1.3.1 Info and Relationships — A — **Pass with notes**

<Criteria that pass are worth one line each — it shows what was checked.>

## Prioritized backlog
## Open questions
````

---

## Tokens mode report

Drift is reported as consolidated inventories, never as forty individual
findings.

````markdown
# Design system consistency review — <product>

**System found:** <tokens file / Tailwind theme / Figma variables / none>
**Consumed by:** <n components, m files>
**Method:** <what you searched, and where>

## Summary

<Is there a system, is it followed, and what is the shape of the drift.>

## Drift inventory

### Colour — 34 raw values alongside a 12-token palette

| Value | Uses | Files | Should be |
|---|---|---|---|
| `#3B82F6` | 11 | `Button.tsx`, `Link.tsx`, `Badge.tsx`, +3 | `color/brand/primary` |
| `#6B7280` | 8 | 6 files | `color/text/secondary` |
| … | | | |
| *9 singletons* | 9 | 7 files | Need a decision — listed in appendix |

### Spacing — 18 off-scale values in a base-4 system
### Type — 14 distinct sizes against a 7-step scale
### Radius — 5 values, no defined scale
### Component drift — 3 button implementations, 2 modal shells

## Contrast check

<Every token pair that carries text, measured. Ties D10 to D12 — this is where
a design-system review earns its keep.>

## Recommendation

<Ordered: what to consolidate first, what needs a decision from the team, and
what should be left alone. Separate the mechanical from the judgment calls.>
````

---

## The state-coverage matrix

Often the highest-value single artifact in an audit. Include it whenever the
scope covers more than a couple of views.

```markdown
| View | Loading | Empty (day 1) | Empty (filtered) | Error | Offline | Overflow |
|---|---|---|---|---|---|---|
| Dashboard | Skeleton | **Missing** | n/a | **Missing** | **Missing** | OK |
| Invoices | Spinner | Text only, no action | **Missing** | Full-page | **Missing** | Truncates badly |
| Settings | **Missing** | n/a | n/a | Toast only | **Missing** | OK |

✅ present and adequate · ⚠️ present but weak · **Missing** · n/a not applicable
```

State how each cell was determined — observed, or inferred from the absence of a
code branch. Absence of a Figma frame is not evidence.

---

## Maturity ratings, if used

Optional. If included:

- **Integers 1–5 only.** No decimals.
- **One line of justification each**, anchored to findings.
- **No composite or overall score.** "3.7/5 overall UX health" implies a
  measurement that was not performed.
- **Only rate dimensions you actually audited.** An unaudited dimension gets
  "not assessed", not a guess.

```markdown
| Dimension | Rating | Why |
|---|---|---|
| First-run & onboarding | 2 | Product is gated behind signup; nothing is visible before an account exists |
| Navigation & IA | 4 | Structure is shallow and labels are clear; orientation is weak in nested views |
| Accessibility | 1 | Focus indication removed globally; several core controls unnamed |
| Data display | — | Not assessed — no data-bearing screens in scope |
```

The scale, stated once so the numbers mean something:
**1** systematically broken · **2** significant gaps on core paths · **3**
works, with known weaknesses · **4** solid, minor issues · **5** exemplary.

---

## Writing rules

- **Findings are self-contained.** A reader who opens on FLOW-01 shouldn't have
  to read the summary to understand it.
- **When the product already solves this correctly somewhere, say where.**
  "The supplier inputs restore a focus ring correctly 185 lines earlier"; "the
  review screen you need is already 500 lines up in this file". This is the
  strongest form a recommendation takes: the fix is now a copy rather than a
  design decision, it lands consistent with the product's own conventions
  instead of importing yours, and the team cannot argue the pattern doesn't fit
  them. Look for the in-repo precedent before proposing anything from outside.
- **Never cite a check ID as the reason.** `WEB3-G`, `FORM-B`, `A11Y-D` are this
  skill's internal bookmarks; the team reading the report has never seen them and
  owes them nothing. "Why it matters" opens on what happens to the person. Check
  IDs belong in a trailing `Related.` line or nowhere (SKILL.md §3).
- **Count anything you state a number for.** Section headings that carry a count
  ("Accessibility — 6 findings"), the total in the summary, the backlog length:
  these drift as findings are added, and a heading that says six above seven
  findings costs the reader's trust in every other number in the report.
  **Write the counts last, from the finished document, or leave them out.** The
  same applies to what you say about the report in conversation — if you tell
  someone it holds 34 findings, count them.
- **Quote, don't paraphrase.** "The button reads *Continue*", not "the button
  has generic copy".
- **Locations are precise.** URL, screen name, `file.tsx:42`, Figma node id.
- **One finding per finding.** If the recommendation has three parts, either
  it's three findings or one finding with three steps — not three problems
  bundled under one ID.
- **IDs are stable and dimension-prefixed**, numbered in the order you wrote
  them. They'll be quoted in tickets; don't renumber between drafts.
- **No severity inflation.** If everything is High, nothing is. Expect most
  audits to be mostly Medium.
- **Label taste as taste**, in the finding itself, and never grade it above Low.
- **Say what's good, briefly** — one short section or a line per dimension.
  It's calibration, not flattery: a reader who sees only failures can't tell
  whether you understood the product.
- **Don't recommend a redesign** unless one was asked for. An audit produces
  findings; a redesign is separate work.
- **Don't ship the audit as a pull request.** If the user wants fixes too,
  deliver the report first, then implement — as two deliverables.
