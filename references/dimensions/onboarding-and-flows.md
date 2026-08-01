# D1 · First-run & onboarding — D3 · Core task flows

> **When to read:** Any audit whose scope includes how a new user gets started,
> or how anyone completes the product's main job. These two dimensions share a
> file because they share a failure mode: steps that exist for the business
> rather than the user. Finding IDs: `ONB-nn` and `FLOW-nn`.
>
> Grade against the audience call (SKILL.md §0f). An expert product may
> legitimately have no onboarding at all; a mainstream one may not.

## Table of contents
- [D1 · First-run & onboarding](#d1--first-run--onboarding)
  - [ONB-A · Time to first value](#onb-a--time-to-first-value)
  - [ONB-B · Gating — what's locked before signup](#onb-b--gating--whats-locked-before-signup)
  - [ONB-C · Permission and account-request timing](#onb-c--permission-and-account-request-timing)
  - [ONB-D · Skippability and resumability](#onb-d--skippability-and-resumability)
  - [ONB-E · Is the onboarding a decision or a template?](#onb-e--is-the-onboarding-a-decision-or-a-template)
  - [ONB-F · Progressive education](#onb-f--progressive-education)
  - [ONB-G · The empty product on day one](#onb-g--the-empty-product-on-day-one)
- [D3 · Core task flows](#d3--core-task-flows)
  - [FLOW-A · Map the flow before judging it](#flow-a--map-the-flow-before-judging-it)
  - [FLOW-B · Step count and required input](#flow-b--step-count-and-required-input)
  - [FLOW-C · Review before commit](#flow-c--review-before-commit)
  - [FLOW-D · Reversibility](#flow-d--reversibility)
  - [FLOW-E · Drop-off risk](#flow-e--drop-off-risk)
  - [FLOW-F · Dead ends](#flow-f--dead-ends)
  - [FLOW-G · The second time through](#flow-g--the-second-time-through)
  - [FLOW-H · Cross-surface and interrupted flows](#flow-h--cross-surface-and-interrupted-flows)
- [Severity calibration](#severity-calibration-for-this-file)

---

# D1 · First-run & onboarding

## ONB-A · Time to first value

**Check.** From landing on the product cold, how long until the user understands
what it does and gets something useful out of it? Time it. Count the screens and
the required inputs before anything of value appears. The working benchmark:
**a newcomer should understand what this is for and why it's worth their time
in about 30 seconds, without creating an account, reading docs, or sitting
through a tutorial.**

**Why it matters.** First-run is where the largest single drop-off in almost
every product happens, and it is the one moment the user has zero investment to
protect. Every screen before value is a place to quit at no cost.

**Fails like.**
- A multi-screen tutorial carousel before the product is visible.
- A signup wall on arrival, before the product has said what it does.
- A setup wizard that demands configuration decisions the user can't yet make
  ("Choose your workspace type") because they don't know what the options mean.
- A "welcome" screen whose only content is the logo, a title, a subtitle, and a
  Get Started button — a screen that costs a tap and delivers nothing.
- Value that requires data the user doesn't have yet (an analytics product that
  is blank until an integration is connected, with no sample data).

**Fix.** Move value earlier and setup later. Show the product working —
real screens with sample or read-only data — before asking for anything. Defer
every configuration decision to the moment it's actually needed. If a tutorial
is genuinely required, replace it with in-context hints at the point of use.

---

## ONB-B · Gating — what's locked before signup

**Check.** What can a logged-out visitor actually do? Browse, search, view a
sample, see the interface with placeholder or empty states? Or does the product
present a login form and nothing else? **The ask should appear at the moment an
action genuinely requires it**, not on arrival.

**Why it matters.** Gating the whole interface behind an account converts the
signup decision into a blind one — the user is asked to commit before they have
any basis to. It is the most common and most expensive onboarding mistake.

**Fails like.**
- The route `/` redirects to `/login` with no marketing or preview behind it.
- The app shell renders but every panel says "Sign in to view".
- A read-only capability that plainly could be public (browsing a catalogue,
  reading a doc, seeing prices) is behind the wall.
- The CTA says "Get started" and goes to a signup form, so the user still
  doesn't know what they're starting.

**Fix.** Let the shell and the read paths render for logged-out users, with
sample or public data. Move the account ask to the first write action, and label
it with the action it unlocks — "Sign in to save this", not "Sign in".

**Legitimate constraint to respect:** some products genuinely have nothing to
show without identity (a bank, a personal health record, an internal tool behind
SSO). Don't flag those. Flag the ones that gate a browsable product out of
habit.

---

## ONB-C · Permission and account-request timing

**Check.** When does the product ask for notifications, location, camera,
contacts, calendar, or payment details? Is the ask preceded by a reason the user
can evaluate? Is refusing it a supported path, or a dead end?

**Why it matters.** A permission prompt fired on launch is refused by most
people, permanently, and on mobile the OS often won't let you ask twice. An
unexplained ask trades a durable capability for a moment of impatience.

**Fails like.**
- The native permission dialog fires on first launch, before any context.
- No pre-prompt: the app goes straight to the OS dialog with no in-app screen
  explaining what it wants and why.
- Refusal breaks the app, or drops the user into a screen that just repeats the
  request.
- Payment details collected before the value is demonstrated, on a product that
  advertises a free tier.

**Fix.** Tie each ask to the moment it pays off ("Turn on notifications so we
can tell you when the report is ready" — at the point of running a report).
Precede the OS dialog with an in-app explanation you control, so a "no" there is
recoverable. Make every permission optional in fact, not just in theory: define
what the product does when refused.

---

## ONB-D · Skippability and resumability

**Check.** Can the user skip the onboarding? Is Skip visible without hunting, on
every step? If they quit halfway and come back, do they resume or start over? Is
the onboarding reachable again later for someone who skipped it?

**Why it matters.** Unskippable onboarding punishes exactly the users who are
most ready to convert — returning users, evaluators, and anyone who has already
been told what the product does.

**Fails like.**
- No skip control, or one rendered in low-contrast small text in a corner.
- Skip on the first screen only, disappearing on screens 2 and 3.
- Closing the app mid-onboarding restarts the whole sequence.
- The tour, once skipped, is unreachable — nothing in Help or Settings restores
  it.
- A "required" step that isn't (a profile photo, an invite-your-team screen)
  with no way past.

**Fix.** Skip on every step, at a legible size and contrast, with a real target
size. Persist progress. Put a "Take the tour" entry in Help so skipping is safe.
Distinguish genuinely required steps (accepting terms) from optional ones and
let the optional ones be optional.

---

## ONB-E · Is the onboarding a decision or a template?

**Check.** Does the onboarding show what *this* product does, or is it a generic
shape that would fit any product? The recognizable default:
**logo → title → subtitle → three icon-and-text boxes → Get started.** If the
screens would work unchanged for a different app in a different category, it was
defaulted, not designed.

**Why it matters.** A generic onboarding communicates nothing specific, so it
occupies the user's most valuable 30 seconds without moving them. It also reads
as unfinished, which costs trust on a first impression.

**Fails like.**
- Three feature cards with abstract icons and one-word titles ("Fast",
  "Secure", "Simple").
- Illustrations of generic people at generic desks in place of the product.
- Copy that describes a category ("Manage your finances effortlessly") rather
  than this product's actual job.
- The same layout repeated for three screens with different words.

**Fix.** Choose a pattern that fits what the product does, and use real product
visuals over icon-in-a-box triplets. The options worth considering:

| Pattern | Fits |
|---|---|
| **Value carousel** | 2–4 swipeable panels, each one concrete benefit shown with a real screen. Progress dots, skip always available. |
| **Live / animated preview** | The product doing its actual thing — a looping micro-demo. Strongest for "understand in 30 seconds". |
| **Single strong screen** | One confident value statement, one real product shot, one CTA. Best when the value is obvious. |
| **Interactive peek** | Drop the user into a read-only version of the product before any account step. Pairs with ONB-B. |
| **Data- or proof-led** | For a serious/expert audience: a real metric, a chart, credibility markers — not childlike feature cards. |
| **No onboarding at all** | Legitimate when the product is self-evident and the empty states do the teaching. |

Grade every screen individually: if it doesn't add understanding, it's a step to
cut, not a step to redesign.

---

## ONB-F · Progressive education

**Check.** Are concepts explained at the moment they're needed, inline and once —
or front-loaded into a tutorial and then never repeated? When a domain term
first appears in the interface, is there a way to find out what it means without
leaving the flow?

**Why it matters.** Nobody retains a definition given five screens before it's
relevant. Education delivered at the point of need is used; education delivered
up front is skipped and then missed.

**Fails like.**
- A five-screen glossary intro, followed by an interface full of unexplained
  terms.
- A term that appears for the first time in a confirmation dialog, undefined,
  at the exact moment the user must decide.
- Help that exists but only in a separate docs site, opening in a new tab and
  losing the flow.
- Education that blocks: a modal the user must dismiss to continue, on every
  visit.

**Fix.** Explain inline, at first encounter, once. A discreet help affordance
next to the term, opening real copy written for that field. Make it available,
never mandatory. See `content-and-copy.md` for the jargon calibration and
`feedback-and-states.md` for the "helper icon that opens nothing" defect.

---

## ONB-G · The empty product on day one

**Check.** What does the product look like the first time, with no data? Is the
day-one empty state an onboarding surface pointing at the first useful action —
or a blank region, a spinner that never resolves, or a table with headers and no
rows?

**Why it matters.** For most products the real onboarding *is* the first empty
screen. It's where the user decides whether this thing is worth populating.

**Fails like.**
- A blank content area with no explanation.
- "No data" as the entire empty state, with no action.
- An empty state that looks identical to a failed load, so the user can't tell
  whether to wait, retry, or act.
- A dashboard of zeros presented as if it were real data.

**Fix.** Every first-run empty state names what goes here, why it's worth it,
and offers the single action that fills it. Distinguish empty from error
unmistakably. Detailed checks in `feedback-and-states.md` (STATE-C).

---

# D3 · Core task flows

## FLOW-A · Map the flow before judging it

**Check.** Before any finding, write the flow down as observed: every screen,
every required input, every decision point, every exit. Count the steps. Note
where the user must leave the flow to get something (a code from email, a
document, a number they don't have memorized).

**Why it matters.** Most flow findings are only defensible against a map — "six
steps, three of them collecting information the system already has" is a finding;
"the flow feels long" is an opinion. The map also goes in the report, where it's
often the most useful artifact in it.

**Fails like** (in the audit, not the product): findings that name a problem
without naming the step it occurs at; a step count that doesn't match what the
user experiences because you counted screens instead of decisions.

**Fix.** Record it as a numbered list with the input required at each step, and
mark each step **necessary / deferrable / removable**. That marking is the
recommendation.

---

## FLOW-B · Step count and required input

**Check.** For each step: is it necessary *here*? Could it be deferred, defaulted,
derived from data the system already has, or removed? For each required field:
does the product already know this, or could it?

**Why it matters.** Every required input is a place to abandon, and the cost is
not linear — a field the user has to leave the app to answer costs far more than
one they can answer from memory.

**Fails like.**
- Asking for information the product already stores (re-entering an address on
  every order).
- Two steps that could be one screen, split for no reason the user can see.
- A required field with no bearing on the task (company size on a support form).
- Required-by-default fields that the business wants and the user doesn't need,
  unmarked as optional.
- A step whose only content is "Are you sure you want to continue?" on a
  non-destructive action.

**Fix.** Name the specific steps to merge, defer, default, or drop, and say what
each removal saves. Where a step is required for a real reason (legal, fraud,
payment), say so and audit its execution instead — that's respecting a
constraint, not excusing it.

---

## FLOW-C · Review before commit

**Check.** For any action that is irreversible, costs money, notifies other
people, or changes something shared: is there a review step that shows what will
happen, in the user's terms, before it happens? Can the user tell from that
screen exactly what they're agreeing to?

**Why it matters.** The review step is where a user catches their own mistake.
Removing it moves every typo into production.

**Fails like.**
- Submit fires immediately from the compose screen with no summary.
- A review that restates the form fields rather than the outcome ("Quantity: 3"
  instead of "You'll be charged $147.00 today, then $49/month").
- A confirmation dialog with a generic body ("Are you sure?") that doesn't name
  the object or the consequence.
- The review shows a total but not what's in it, so an error in a line item
  can't be caught.
- A step that *is* the review but is skippable by keyboard `Enter` on the
  previous screen.

**Fix.** A dedicated review surface, showing the outcome first and the mechanics
second, with a way back to change each part. It carries no countdown and no
urgency pressure — see `trust-and-dark-patterns.md`. On money-moving actions,
this is a Blocker when it's absent.

---

## FLOW-D · Reversibility

**Check.** After each committing action: can the user undo it, and for how long?
Is the undo discoverable at the moment it's needed, or buried in a settings page?
Where undo is genuinely impossible, is that stated *before* the commit?

**Why it matters.** Undo converts a catastrophic mistake into a two-second
annoyance, and it lets a product be fast — a flow with undo can drop
confirmations that a flow without it needs.

**Fails like.**
- A destructive action with neither a confirmation nor an undo.
- Undo exists but only via a toast that auto-dismisses in three seconds.
- "This cannot be undone" appearing only *after* the action.
- Cancel on a subscription that requires an email to support.
- A "draft" that is actually published on save.

**Fix.** Prefer undo over confirmation where the action is recoverable (softer,
faster, fewer interruptions). Where it truly isn't recoverable, say so plainly
in the confirmation, require a deliberate act (typing the name, a distinct
Danger-styled button), and never pre-focus the destructive option. Full checks in
`feedback-and-states.md` (ERR-A).

---

## FLOW-E · Drop-off risk

**Check.** At each step, ask what fraction of users would stop here and why. The
recurring causes, in rough order of severity: a required credential or code the
user doesn't have to hand; an unexplained cost appearing late; a form that
rejects input without saying how to fix it; a decision the user can't make with
the information on screen; a wait with no progress indication; a mandatory
account for something that looked free.

**Why it matters.** This is the dimension a team most wants from an audit, and
the one where you must be most careful about confidence: **you can identify
drop-off risk from the interface; you cannot measure drop-off without their
analytics.** Say which you're doing.

**Fails like** (in the interface): a late-revealed cost; a "create an account to
continue" at step 4 of 5; a required field validated only on submit that clears
the form; an OTP step with no resend and no fallback.

**Fix.** Name the step, the mechanism, and the change. Then put the measurement
in Open questions: "If you have funnel data for these steps, step 3 is where
I'd expect the largest loss — worth checking before investing in step 5."

---

## FLOW-F · Dead ends

**Check.** Every screen: can the user get out, forward, and back? Does every
error state offer a next action? Does the back gesture or button do what the
user expects at every step, including after a submit? Is there any state the
user can reach that has no exit but a page reload?

**Why it matters.** A dead end doesn't just fail this task — it costs the trust
that makes the user try again.

**Fails like.**
- An error screen with a message and no button.
- A modal with no visible close, no Escape handler, and a scrim that doesn't
  dismiss.
- A step that requires an unmet prerequisite ("Add a payment method first") with
  no link to where you'd do that.
- Browser Back after a submit resubmitting, or landing on a stale expired form.
- A "not found" for a resource that used to exist, with no path to the list it
  came from.
- A search with zero results and no way to broaden or clear the filters.

**Fix.** Every terminal state gets at least one forward action. Every error gets
a retry or an alternative. Every prerequisite gets a link to its own resolution.
Test browser Back explicitly on web; test the system back gesture on Android.

---

## FLOW-G · The second time through

**Check.** Run the flow twice. Does the product remember anything — recent
choices, defaults, the last-used option? Does onboarding or a tour reappear?
Are there shortcuts for the repeat user, or is step 1 identical every time?

**Why it matters.** Most products are designed and demoed against the first
run, and used against the hundredth. A flow optimized only for the newcomer
becomes a daily tax on the people who actually pay.

**Fails like.**
- No recents, no defaults, no "same as last time".
- A tooltip tour that reappears every session.
- The most common option not being the default.
- No keyboard path for a task an expert repeats twenty times a day.
- Confirmation prompts that can't be suppressed on a routine, reversible action.

**Fix.** Persist and default from history. Offer a fast path (keyboard,
duplicate, templates, bulk) once the audience call says repeat use is real.
Weight this heavily for an expert audience and lightly for a one-time
transactional flow.

---

## FLOW-H · Cross-surface and interrupted flows

**Check.** Does the flow require leaving the product — for an email, an SMS
code, an authenticator, a document upload, an external payment page, a wallet
app? For each hand-off: is the return path defined, does state survive, and does
the product say what's about to happen before it happens?

**Why it matters.** Every hand-off is a place where the user's context — and
often their session — is destroyed. Unhandled returns are among the most
expensive defects in a flow, because the user has already invested.

**Fails like.**
- Clicking an emailed link opens a new session with the form state gone.
- No indication that the user is about to leave the app.
- Returning from an external page lands on the home screen, not the step.
- No resend on an OTP, or a resend that resets a timer with no feedback.
- A mobile hand-off to another app with no loading or failure state on return.
- The flow starts on desktop and must finish on mobile, with no continuity.

**Fix.** Design the leaving state and the returning state as real screens. Hold
the flow state server-side or in a resumable token. Tell the user what will
happen ("We'll email you a code — keep this tab open"). On mobile, handle the
deep-link round trip and its failure explicitly.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Flow cannot be completed at all on a supported path or device | **Blocker** |
| Irreversible action with no review and no undo | **Blocker** |
| Dead end reachable in normal use with no exit but reload | **Blocker** |
| Whole product gated behind signup with nothing shown first | **High** |
| Permission demanded on launch with no context and no recovery | **High** |
| Onboarding unskippable, or restarts on every session | **High** |
| Required input the system already has, on a core flow | **High** |
| Generic template onboarding that teaches nothing | **Medium** (High if it's also unskippable) |
| No defaults or recents for a repeat task, expert audience | **Medium** |
| Onboarding copy that could describe any product | **Medium** |
| Step order that's suboptimal but workable | **Low** — often taste; label it |
