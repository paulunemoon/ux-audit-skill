# D5 · System status & feedback — D6 · Error prevention & recovery — D7 · State coverage — D14 · Perceived performance

> **When to read:** Every audit. These four dimensions are one subject seen from
> four angles: **does the interface tell the truth about what it's doing, and does
> it hold up when things aren't ideal?** Most products are designed against the
> success state with good data and a fast connection; everything here is what
> happens otherwise. Finding IDs: `FBK-nn`, `ERR-nn`, `STATE-nn`, `PERF-nn`.

## Table of contents
- [D5 · System status & feedback](#d5--system-status--feedback)
  - [FBK-A · Every action is acknowledged](#fbk-a--every-action-is-acknowledged)
  - [FBK-B · Loading — the right indicator for the wait](#fbk-b--loading--the-right-indicator-for-the-wait)
  - [FBK-C · Optimistic updates and their rollback](#fbk-c--optimistic-updates-and-their-rollback)
  - [FBK-D · Progress for long operations](#fbk-d--progress-for-long-operations)
  - [FBK-E · Choosing the feedback channel](#fbk-e--choosing-the-feedback-channel)
  - [FBK-F · Toasts and notifications](#fbk-f--toasts-and-notifications)
  - [FBK-G · Overlays that behave](#fbk-g--overlays-that-behave)
  - [FBK-H · Helper affordances that actually help](#fbk-h--helper-affordances-that-actually-help)
- [D6 · Error prevention & recovery](#d6--error-prevention--recovery)
  - [ERR-A · Destructive action guards](#err-a--destructive-action-guards)
  - [ERR-B · Undo](#err-b--undo)
  - [ERR-C · Prevention beats messaging](#err-c--prevention-beats-messaging)
  - [ERR-D · Recovery paths](#err-d--recovery-paths)
  - [ERR-E · Error taxonomy — not everything is an error](#err-e--error-taxonomy--not-everything-is-an-error)
- [D7 · State coverage](#d7--state-coverage)
  - [STATE-A · The inventory](#state-a--the-inventory)
  - [STATE-B · Loading](#state-b--loading)
  - [STATE-C · Empty and sparse](#state-c--empty-and-sparse)
  - [STATE-D · Error](#state-d--error)
  - [STATE-E · Offline and degraded](#state-e--offline-and-degraded)
  - [STATE-F · Overflow and extremes](#state-f--overflow-and-extremes)
  - [STATE-G · Permission and role states](#state-g--permission-and-role-states)
  - [STATE-H · First-use versus power-use](#state-h--first-use-versus-power-use)
- [D14 · Perceived performance](#d14--perceived-performance)
  - [PERF-A · Time to first meaningful paint](#perf-a--time-to-first-meaningful-paint)
  - [PERF-B · Layout shift](#perf-b--layout-shift)
  - [PERF-C · Blocking states](#perf-c--blocking-states)
  - [PERF-D · Input responsiveness](#perf-d--input-responsiveness)
  - [PERF-E · Motion cost](#perf-e--motion-cost)
- [Severity calibration](#severity-calibration-for-this-file)

---

# D5 · System status & feedback

## FBK-A · Every action is acknowledged

**Check.** Press every interactive thing. Does something visibly change within
~100ms — a pressed state, a spinner, a disabled control, a value updating? Is
there any control that can be pressed with no perceptible response?

**Why it matters.** Silence after an action is indistinguishable from a broken
control. Users respond by pressing again, which is how duplicate orders,
duplicate messages, and duplicate charges happen.

**Fails like.**
- A button with no pressed/active feedback on touch (where there is no hover to
  fall back on).
- A save that completes silently — the user can't tell whether it worked.
- A filter or sort applied with no visible change while the data reloads.
- A link to a slow route with no indication the navigation started.
- An action whose only feedback is a toast that appears a second later.

**Fix.** Immediate local feedback on press, independent of the server round
trip. Then the outcome. Distinguish "received" from "done".

---

## FBK-B · Loading — the right indicator for the wait

**Check.** For each async region: is there a loading state, and is it the right
kind for the duration and the shape of what's coming?

| Wait | Right indicator |
|---|---|
| < ~300ms | Nothing. An indicator that flashes is worse than none. |
| ~0.3–1s, in-place | Inline spinner on the control, label preserved |
| ~1s+, content region | **Skeleton** shaped like the content that's coming |
| Several seconds, known steps | Progress with a step label |
| Unknown, long | Progress plus an honest message and a way to leave |

**Why it matters.** The wrong indicator either makes a fast interface feel
jittery or makes a slow one feel broken. Skeletons in particular reduce
*perceived* wait because they preview the layout instead of hiding it.

**Fails like.**
- A full-page spinner replacing content that was already on screen.
- Generic grey blocks as "skeletons" that look nothing like the final content,
  so the layout jumps when data lands.
- Spinner flash on a 60ms request.
- A skeleton that never resolves because the empty case wasn't handled — an
  infinite skeleton is the classic symptom of "empty state missing".
- Loading indicated only by the absence of content.
- A spinner with no `prefers-reduced-motion` fallback.

**Fix.** Match the indicator to the wait. Skeletons take the shape of the real
content (an avatar circle, two text bars, a value bar) and swap in place without
layout shift. Never let a skeleton be the empty state.

---

## FBK-C · Optimistic updates and their rollback

**Check.** Where the interface updates before the server confirms: what happens
when the server says no? Does the UI revert, and does it tell the user it
reverted and why?

**Why it matters.** Optimistic UI is a good pattern with one hard requirement:
a silent rollback means the user believes something happened that didn't.

**Fails like.**
- A toggle that flips back with no message.
- A message that appears in a thread and vanishes on a later render.
- An item deleted optimistically, restored on failure, with no explanation.
- A counter that drifts because failures aren't reconciled.
- Optimistic updates on operations that genuinely fail often (payments,
  reservations, anything with contention).

**Fix.** Roll back visibly, with a message naming what failed and offering a
retry. Reserve optimism for high-success, low-consequence operations; use a real
pending state for the rest.

---

## FBK-D · Progress for long operations

**Check.** Anything over a few seconds — an import, an export, a render, a
batch job, a payment: is there real progress, an accurate estimate, and a way to
do something else meanwhile? Can it be cancelled?

**Why it matters.** An unbounded wait with no information is where users force-
quit, refresh, and re-submit — often making the situation worse.

**Fails like.**
- A modal spinner blocking the whole app for a 40-second export.
- A progress bar that sits at 90% for most of the operation.
- "This may take a while" with no bound and no way to leave.
- No notification when a background job finishes, so the user has to poll.
- A cancel that stops the UI but not the operation.
- Losing progress entirely if the tab is closed.

**Fix.** Real progress where it's computable; step labels where it isn't
("Uploading 3 of 12"). Let long jobs run in the background with a notification
on completion. Offer cancel, and make cancel actually cancel.

---

## FBK-E · Choosing the feedback channel

**Check.** Is the feedback in the right place for its weight and its subject?

| Message | Belongs |
|---|---|
| Field-level validation | Inline, at the field |
| Result of an action on this screen | In context, near the thing that changed |
| Transient success, non-blocking | Toast |
| Blocking condition the user must resolve | Inline banner in the affected region |
| System-wide condition (offline, outage, expiry) | Persistent banner in the shell |
| A decision the user must make now | Dialog |

**Why it matters.** The channel *is* part of the message. A blocking problem in a
disappearing toast will be missed; a routine success in a modal is an
interruption.

**Fails like.**
- Field errors shown only as a toast at the top of the screen.
- A critical failure in a 3-second auto-dismissing toast.
- A modal to confirm a trivial, reversible action.
- A persistent banner for something already resolved.
- Feedback rendered far from the element it concerns, off-screen on mobile.

**Fix.** Route each message to the right channel. Say which ones to move.

---

## FBK-F · Toasts and notifications

**Check.** Do toasts stay long enough to read (a rough floor: ~4–6s for a short
success, longer or persistent for anything actionable)? Do they stack sanely?
Are they dismissible? Do they contain actions that would be lost when they
auto-dismiss? Are they announced to screen readers?

**Why it matters.** A toast is the least reliable channel — it's peripheral,
timed, and easily missed. Anything the user must act on doesn't belong in one
unless it's also available elsewhere.

**Fails like.**
- A toast carrying the only Undo, auto-dismissing in 2 seconds.
- Toasts stacking indefinitely and covering the interface.
- A new toast per retry rather than updating the existing one in place.
- Toasts obscuring the primary action on mobile, or sitting outside the safe
  area.
- No `aria-live` region, so screen-reader users get nothing.
- A pending toast that auto-dismisses before the operation resolves.

**Fix.** Duration proportional to length and importance. Actionable toasts
persist or duplicate the action elsewhere. Pending → resolved updates the same
toast in place rather than stacking a second one. Live region for announcement.

---

## FBK-G · Overlays that behave

**Check.** For every modal, sheet, drawer, and popover: does the scrim cover the
whole viewport? Is the dialog centered against the viewport (not its parent)?
Does Escape close it? Does clicking the scrim close it? Is background scroll
locked, and restored without jumping? Is focus trapped and returned on close?
Does it scroll internally when tall rather than running off screen?

**Why it matters.** These aren't styling preferences — a modal missing any of
them is broken, and the failures are invisible until someone uses a keyboard, a
small screen, or a long content case.

**The signature defect to look for first — the clipped overlay.** The scrim
covers only the header strip while the rest of the page stays bright, and the
panel hangs off the navbar like a dropdown. **Cause:** the overlay is rendered
inside the header/navbar DOM, so that ancestor's height, `overflow`,
`transform`, or stacking context clips it. **Fix:** render it in a portal at the
document root. This is the most common overlay defect in generated and
hand-rolled UI alike, and it's usually a one-line fix worth flagging as a quick
win.

**Other fails like.**
- `100vh` scrim on mobile web, so it overflows or falls short (`dvh` is the fix
  for browser chrome — but see `platform-mobile.md`, the keyboard is a separate
  problem).
- Escape does nothing.
- Background scrolls behind the modal, or the page jumps to the top on close.
- Focus stays behind the dialog, or is lost to `<body>` on close.
- No `role="dialog"`, no `aria-modal`, no accessible name.
- A tall dialog whose footer actions are off-screen with no internal scroll.
- Scrim-dismiss enabled during an in-flight irreversible operation.
- A sparse dialog: a title, one vague sentence, two buttons — where the user
  needs actual information to decide. **A dialog that looks empty is usually
  missing the information the decision requires**, not padding.

**Fix.** Portal to the document root; full-viewport fixed scrim; centered,
height-capped dialog with an internally scrolling body; Escape and scrim
dismiss; scroll lock; focus trap and return. Where the product hand-rolled this,
the recommendation is to move to a proven accessible primitive rather than to
patch each behavior individually.

---

## FBK-H · Helper affordances that actually help

**Check.** Every `?` / ⓘ / help icon: does it open something, on hover **and**
keyboard focus on desktop, and on **tap** on touch? Is the content written for
that specific field, or is it a restatement of the label? Is essential
information hidden in a hover-only tooltip?

**Why it matters.** A help glyph that does nothing is worse than no glyph — it
advertises an explanation, the user reaches for it, and nothing happens. These
cluster next to exactly the things users don't understand (fees, limits, unusual
terms, disabled controls), which is where the failure costs most.

**Fails like.**
- A `?` with no handler, or one wired to hover only, on a touch device.
- Tooltip content that repeats the label ("Amount — the amount").
- "Coming soon" or placeholder copy behind a help icon.
- Tooltips that clip at the viewport edge instead of flipping.
- A tooltip carrying information the user needs to complete the task, with no
  other route to it.
- No `aria-describedby` linking the explanation to the field.

**Fix.** Real copy per field, one or two plain sentences answering the question
the icon implies. Hover **and** focus on desktop; tap-to-open popover or sheet
on touch. Edge-flipping. Associated to the field for screen readers. **If the
copy doesn't exist, remove the icon** until it does.

---

# D6 · Error prevention & recovery

## ERR-A · Destructive action guards

**Check.** For every action that deletes, cancels, revokes, overwrites,
publishes, or notifies other people: what stands between the click and the
consequence? Is the confirmation specific about *what* and *what happens*? Is
the destructive option pre-focused or styled as the safe default?

**Why it matters.** The guard is the last chance to catch a misclick on
something that can't be taken back.

**Fails like.**
- Immediate deletion on a single click, no confirm, no undo.
- "Are you sure?" with no object named and no consequence stated.
- The destructive button styled as the primary action and pre-focused, so
  `Enter` destroys.
- Confirm and Cancel in a different order than elsewhere in the product.
- A delete icon adjacent to a common action, at a small target size.
- Bulk delete with no count ("Delete items?" — how many?).
- A guard on a trivially reversible action, training users to click through
  every dialog, so the real guard gets clicked through too.

**Fix.** Name the object and the consequence: "Delete *Q3 forecast*? This
removes it for all 12 members of Finance and can't be undone." Danger styling
on the destructive action, focus on the safe one. Proportional friction — typing
the name for the genuinely catastrophic, a plain confirm for the merely
irreversible, **undo instead of a dialog for the recoverable**.

---

## ERR-B · Undo

**Check.** Which actions have undo? How long does the window last, and is it
discoverable at the moment it matters? Where undo is impossible, is that stated
before the commit?

**Why it matters.** Undo lets an interface be fast. It replaces friction with
recovery — usually a better trade for both speed and safety.

**Fails like.**
- No undo anywhere, so every risky action needs a dialog.
- Undo present only in a toast that vanishes in 3 seconds.
- Undo restores the item but loses its position, order, or relationships.
- No bulk undo after a bulk action.
- "Cannot be undone" appearing after the fact.

**Fix.** Add undo where the operation is reversible; where added, the
confirmation dialog can often be removed — say so, since that's the payoff.
Undo window long enough to notice (a soft-delete with a recycle bin beats a
3-second toast for anything valuable).

---

## ERR-C · Prevention beats messaging

**Check.** For each error the product can produce, ask whether the interface
could have made it impossible. Could the invalid dates be disabled in the picker
instead of rejected on submit? Could the unavailable option be hidden or
explained instead of failing after selection? Could the constraint be shown
before the input rather than after?

**Why it matters.** A prevented error costs nothing. A well-worded error still
costs a round trip, a re-read, and a correction.

**Fails like.**
- A date picker offering dates the system rejects.
- A quantity field accepting more than stock, failing at checkout.
- An option selectable then rejected as unavailable for this plan.
- Constraints (min, max, format, allowed characters) revealed only in errors.
- Actions offered that the user's role can't perform, failing on click.

**Fix.** Disable the impossible, with a visible reason. Constrain the input to
valid values. State limits up front. Reserve error messaging for what genuinely
can't be prevented.

---

## ERR-D · Recovery paths

**Check.** Every error state: does it offer a way forward? Retry, an
alternative, a way back, a way to contact someone, a reference to quote? Is the
user's work preserved through the error?

**Why it matters.** An error without a path is a dead end (see `FLOW-F`), and
it's where users leave.

**Fails like.**
- A full-page error with a message and no button.
- Retry that repeats the same failing request with no change and no backoff.
- Errors that discard the input that caused them.
- A 404 with no link to anything.
- "Contact support" with no contact route and no reference id.
- Session expiry dropping the user at a login screen, losing where they were.

**Fix.** Every terminal error gets an action. Preserve input across errors.
After re-authentication, return the user to where they were. Give
support-worthy failures a reference the user can quote.

---

## ERR-E · Error taxonomy — not everything is an error

**Check.** How does the product treat a user cancelling something? A no-results
search? An expected empty state? Are these dressed as failures — red, alarming,
"Error"?

**Why it matters.** Crying wolf devalues real errors. If cancelling looks like
a failure, users stop reading the ones that matter.

**Fails like.**
- "Error: operation cancelled" in red when the user pressed Cancel.
- Zero search results styled as a failure.
- A red alert for an informational condition.
- A warning on every routine action, so warnings become noise.
- The same visual treatment for "we couldn't reach the server" and "that email
  is already taken".

**Fix.** Three tiers, treated differently: **user-initiated cancellation** is
neutral, no alarm; **expected states** (empty, no results) are informational
with a path forward; **actual failures** get error treatment proportional to
consequence. Reserve warnings for genuine risk so they retain meaning.

---

# D7 · State coverage

## STATE-A · The inventory

**Check.** For each significant view, walk the full state set and record which
exist:

| State | Question |
|---|---|
| **Loading** | First load, and reload of already-visible content |
| **Empty (day one)** | Never had data |
| **Empty (result)** | Had data, filter/search returns none |
| **Sparse** | One item where the design assumed many |
| **Error** | Failed to load; failed to save; partial failure |
| **Offline / degraded** | No connection, or a dependency down |
| **Overflow** | Very long strings, very many rows, very large numbers |
| **Permission** | Not allowed to see or do this |
| **Stale** | Data older than it should be |
| **First-use vs power-use** | Zero items vs thousands |

**Why it matters.** This is where the largest volume of real defects lives, and
it's the least likely to have been designed — most products have a success
state and improvise the rest.

**Fix.** Report the inventory as a table in the audit. A grid of views × states
with what exists is often the most actionable single artifact you produce.

**Evidence note.** From code, absence of a branch is `Observed`; from Figma,
absence of a frame is **not** evidence — ask.

---

## STATE-B · Loading

Covered in FBK-B. The state-coverage question is narrower: **does a loading
state exist at all for every async region**, including regions that refresh
after the first load, and including the shell itself on a cold start?

**Fails like.** Content popping in with no prior state; a reload showing stale
data with no indication it's refreshing; the shell rendering before its data and
then rearranging.

---

## STATE-C · Empty and sparse

**Check.** Does every list, table, chart, and content region have a designed
empty state? Does it distinguish **day-one empty** ("nothing here yet, here's
how to start") from **result empty** ("no matches — clear filters") from
**error**? Does a one-item view look deliberate, or like a broken grid?

**Why it matters.** Empty states are the most-seen screens by new users and the
cheapest onboarding surface a product has. They're also where "is this broken?"
gets decided.

**Fails like.**
- A blank region, a bare "No data", or an empty table with headers only.
- Empty and error styled identically, so the user can't tell whether to retry
  or to act.
- An empty chart rendering axes and no message.
- Zeros presented as real data.
- An empty state with no action, or an action the user can't yet perform.
- A three-column grid with one card, stretched or orphaned.
- An infinite skeleton where the empty state should be.

**Fix.** Each empty state: what goes here · why it's useful · the one action
that fills it. Result-empty offers the filter reset. Error offers retry.
Different copy, different affordance, visually distinguishable.

---

## STATE-D · Error

**Check.** Per view: is there a load-failure state, a save-failure state, and a
partial-failure state (some data loaded, some didn't)? Is a failed section
scoped, or does one failure blank the whole screen?

**Fails like.** A single failed request rendering a full-page error; a section
that silently shows nothing on failure, indistinguishable from empty; a partial
failure presented as complete data — the most dangerous of the three, because
the user acts on data they think is whole.

**Fix.** Scope errors to the region that failed, with a retry for that region.
**Never present partial data as complete** — mark what's missing.

---

## STATE-E · Offline and degraded

**Check.** Go offline mid-session. Does the product notice? Does it say so? What
happens to an action taken while offline — queued, rejected clearly, or silently
lost? On reconnect, does it recover without a manual reload?

**Why it matters.** Mobile connectivity is intermittent by default. Silent loss
of a submitted action is a data-loss defect.

**Fails like.**
- No offline detection; requests hang until timeout with a spinner.
- An action taken offline that appears to succeed and is then gone.
- An offline banner that persists after reconnection.
- No recovery on reconnect — the user must reload.
- A native mobile app with no offline behavior at all in a context where it's
  expected.

**Fix.** Detect and announce connection loss. Queue or clearly reject writes.
Recover automatically. Preserve in-progress input across the interruption.

---

## STATE-F · Overflow and extremes

**Check.** Push every container past its comfortable case: a 60-character name,
an email that doesn't break, a number with 12 digits, 500 list rows, a
translation 40% longer than English, a right-to-left string if the product is
localized, three lines where the design assumed one.

**Why it matters.** Real data is messier than design data. Overflow defects are
individually small and collectively make a product feel unfinished — and some of
them lose information silently.

**Fails like.**
- Text overlapping adjacent elements or escaping its container.
- Truncation with no tooltip or full value available anywhere.
- Truncation that hides the distinguishing part (`Invoice_2026_Q3_...` where
  every item starts the same).
- A large number breaking a column layout, or being silently rounded.
- Horizontal scroll appearing on the page body.
- A button label wrapping mid-phrase, or an icon stranded above its word.
- Long content in a modal with no internal scroll.
- Layout collapsing at 200% zoom.

**Fix.** Define truncation per field, truncating the non-distinguishing part,
with the full value available on hover, focus, and tap. Reserve space for the
realistic maximum. Keep icon-plus-label groups non-wrapping. Test with real
production-shaped data.

---

## STATE-G · Permission and role states

**Check.** For a user without permission: is the action hidden, or disabled with
a reason, or offered and then failing? Is "not allowed" distinguishable from
"doesn't exist" and from "broken"?

**Fails like.** Actions that fail with a generic error on click; a 403 rendered
as a 500; an admin-only section visible with every control silently inert; no
route to request access.

**Fix.** Decide per case: hide what's irrelevant to the role, disable-with-
reason what the user could plausibly gain access to, and always offer the path
to request it where one exists.

---

## STATE-H · First-use versus power-use

**Check.** Look at the same screens with zero items and with a realistic heavy
load. Does the design work at both ends? Is there filtering, sorting, search,
pagination, or bulk action once the data is large? Is there guidance when it's
empty?

**Why it matters.** Products are designed against a demo data set — a dozen
tidy rows. The two real populations are day one and year three, and each breaks
differently.

**Fails like.**
- A list with no search or filter that grows unbounded.
- Pagination with no jump, no page size control, and no total.
- No bulk actions where users clearly operate in batches.
- A dashboard that's beautiful with 6 items and unusable with 600.
- No sort on the column everyone would sort by.

**Fix.** Name which views need scale affordances and which need day-one
guidance. Weight by the audience call: an expert audience with heavy data needs
the power tools far more than the tour.

---

# D14 · Perceived performance

> Perceived performance is a UX dimension, not a benchmark. You are auditing
> **what the interface communicates during a wait**, not measuring throughput.
> If you have real metrics, cite them; if not, describe what you observed and
> say on what connection and device.

## PERF-A · Time to first meaningful paint

**Check.** How long from navigation to something the user can read or act on?
Is that first thing meaningful (content, or a skeleton of it) or decorative (a
logo splash, a full-page spinner)?

**Fails like.** A branded splash on every launch; a blank white page for
seconds; the whole app blocking on one slow request; a skeleton for the shell
but nothing for the content, so the frame arrives and stays empty.

**Fix.** Render the shell and the skeleton immediately; stream content as it
arrives; never block the whole view on the slowest request.

---

## PERF-B · Layout shift

**Check.** Watch the page settle. Does anything move after the user could
plausibly have reached for it? Images without dimensions, late-loading fonts,
banners inserted at the top, ads or embeds, content pushed down by a late
render.

**Why it matters.** Shift causes mis-clicks — and mis-clicks on a moved button
land on whatever moved into its place, which is how people accidentally delete
things.

**Fails like.** Images with no width/height or aspect ratio; a cookie or
promotion banner injected above the fold after paint; a font swap resizing every
heading; a list that reflows as items load in.

**Fix.** Reserve space for anything that loads late. Size media. Font-display
strategy that doesn't reflow. Insert banners in reserved space, not by pushing
content.

---

## PERF-C · Blocking states

**Check.** During a wait, how much of the interface is unusable? Is the block
proportionate — a modal spinner for a 30-second export is not.

**Fails like.** A full-screen blocking overlay for a background-able job; nav
disabled during a content load; the whole form locked while one field
validates; a modal that can't be cancelled during a long operation.

**Fix.** Scope the block to what's genuinely affected. Let long operations run
in the background. Keep navigation alive.

---

## PERF-D · Input responsiveness

**Check.** Type into search and heavy inputs. Does the field keep up? Does
scrolling stay smooth on long lists? Is there a lag between press and pressed
state?

**Fails like.** Characters appearing behind the typing; a filter re-running on
every keystroke against a large set; janky scroll on a long list; a control
whose pressed state lags visibly behind the touch.

**Fix.** Debounce expensive work, never the visual feedback. Virtualize long
lists. Keep the pressed state on the main thread and immediate.

---

## PERF-E · Motion cost

**Check.** Do transitions add perceptible delay to routine actions? Is there a
mandatory animation between every screen? Is `prefers-reduced-motion` respected,
with a genuinely calm fallback rather than a slightly shorter animation?

**Why it matters.** Motion that reads as polished on the first use reads as slow
on the hundredth, and unwanted motion is a genuine accessibility problem for
people with vestibular disorders.

**Fails like.** 400ms+ transitions on frequently repeated actions; a page
transition that delays every navigation; parallax or large-scale movement with
no reduced-motion path; auto-playing looping animation in the content area;
`prefers-reduced-motion` unhandled anywhere in the codebase.

**Fix.** Keep routine transitions short. Honour `prefers-reduced-motion` with a
static or cross-fade fallback. Motion should explain a relationship, not
announce itself.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Destructive action with neither confirmation nor undo | **Blocker** |
| Work silently lost (offline write, optimistic rollback, error clearing input) | **Blocker** |
| Partial data presented as complete | **Blocker** |
| Error state with no recovery path on a core flow | **Blocker** |
| Modal with no keyboard exit / focus trap failure | **Blocker** (also A11Y) |
| No loading state on a core async action; users double-submit | **High** |
| Empty state missing on a core view, or indistinguishable from error | **High** |
| Clipped overlay / scrim not covering the viewport | **High** — usually an S-effort fix |
| Raw error strings surfaced to users | **High** |
| Helper icon that opens nothing, next to something users don't understand | **Medium** |
| Toast too short to read, or carrying the only Undo | **Medium** |
| Overflow breaking layout with real-length data | **Medium** |
| Layout shift after paint | **Medium** (**High** if it moves a control users reach for) |
| Cancellation styled as an error | **Medium** |
| Reduced-motion unhandled | **Medium** (also A11Y) |
| Transition durations, skeleton shimmer style | **Low** — often taste; label it |
