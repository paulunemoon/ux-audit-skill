# D12 · Accessibility — WCAG 2.1 AA

> **When to read:** Every audit (accessibility is always in scope), and as the
> whole subject of `a11y` mode. Finding IDs: `A11Y-nn`, tagged with the success
> criterion where one applies.
>
> **What this file is.** The checks worth running by hand, the ones a tool
> can't do, and how to write the finding so it's fixable. It is not a
> substitute for the specification — cite criteria, don't paraphrase them into
> something subtly wrong.
>
> **Automated tooling catches roughly a third of real issues.** If the user has
> axe, Lighthouse, or similar output, use it as a starting inventory and spend
> your effort on the two-thirds it can't see: focus order, keyboard operability
> of custom controls, meaningful alt text, screen-reader flow, and whether the
> semantics actually describe the thing.

## Table of contents
1. [A11Y-A · Contrast](#a11y-a--contrast)
2. [A11Y-B · Colour as the only channel](#a11y-b--colour-as-the-only-channel)
3. [A11Y-C · Keyboard operability](#a11y-c--keyboard-operability)
4. [A11Y-D · Focus visibility](#a11y-d--focus-visibility)
5. [A11Y-E · Focus order and management](#a11y-e--focus-order-and-management)
6. [A11Y-F · Target size and spacing](#a11y-f--target-size-and-spacing)
7. [A11Y-G · Semantics and structure](#a11y-g--semantics-and-structure)
8. [A11Y-H · Names, labels, and descriptions](#a11y-h--names-labels-and-descriptions)
9. [A11Y-I · Images and alt text](#a11y-i--images-and-alt-text)
10. [A11Y-J · Forms and errors](#a11y-j--forms-and-errors)
11. [A11Y-K · Dynamic content and live regions](#a11y-k--dynamic-content-and-live-regions)
12. [A11Y-L · Motion and animation](#a11y-l--motion-and-animation)
13. [A11Y-M · Zoom, reflow, and text spacing](#a11y-m--zoom-reflow-and-text-spacing)
14. [A11Y-N · Timing](#a11y-n--timing)
15. [A11Y-O · Media](#a11y-o--media)
16. [A11Y-P · Pointer, gesture, and orientation](#a11y-p--pointer-gesture-and-orientation)
17. [A11Y-Q · Screen-reader flow](#a11y-q--screen-reader-flow)
18. [Contrast math](#contrast-math)
19. [Writing an accessibility finding](#writing-an-accessibility-finding)
20. [Severity calibration](#severity-calibration-for-this-file)

---

## A11Y-A · Contrast

**Criteria.** 1.4.3 Contrast (Minimum) AA · 1.4.11 Non-text Contrast AA.

**Thresholds.**

| Content | Minimum |
|---|---|
| Normal text (< 18.66px bold / < 24px regular) | **4.5:1** |
| Large text (≥ 18.66px bold / ≥ 24px regular) | **3:1** |
| UI component boundaries, control states, focus indicators | **3:1** |
| Meaningful graphics — icons, chart marks, data lines | **3:1** |
| Disabled controls, pure decoration, logotypes | Exempt — but see below |

**Check.** Every text/background pair, in **both** colour modes, on the
background it actually sits on. Measure with `scripts/contrast-check.py` rather
than eyeballing. Priorities: secondary and tertiary text (the usual failures),
placeholder text, text on brand fills, text on images or gradients, status
colours (amber is the reliable offender), disabled states, focus rings against
their surroundings, and chart series against the plot background.

**Fails like.**
- Grey-on-grey secondary text at 3.8:1.
- Placeholder text used to carry information, at 2.9:1.
- White text on a mid-tone brand fill at 4.1:1 — the fill-legibility failure in
  `design-system.md`, DS-D.
- Text over a photo or gradient where contrast varies across the image, so it
  passes in one region and fails in another.
- A light mode that was never re-measured after the dark mode was tuned.
- A focus ring at 2:1 against the surface it appears on.
- Disabled controls so faint they're unreadable — technically exempt, still a
  usability defect, so report it as one rather than as a criterion failure.

**Fix.** Give the measured ratio and the required one, and propose a specific
replacement value. "Secondary text `#8A8F98` on `#F5F5F7` measures 2.98:1;
AA needs 4.5:1. `#65696F` measures 5.07:1 and remains visibly one step in from
primary."

---

## A11Y-B · Colour as the only channel

**Criterion.** 1.4.1 Use of Colour A.

**Check.** Any meaning carried by colour alone: status, direction, validity,
selection, category, required fields, links within body text, chart series
identity.

**A fast test:** view the screen in greyscale. Anything that becomes ambiguous is
a finding.

**Fails like.** Red/green values with no sign or icon; a coloured dot as the
only status indicator; links distinguished from text by colour alone; a chart
legend keyed only by swatch; error state shown only as a red border; a selected
item marked only by a tint; required fields marked only in red.

**Fix.** Add a second channel: sign, icon, label, underline, pattern, weight,
or direct labelling. Cross-references: `data-display.md` DATA-G,
`visual-hierarchy.md` VIS-F.

---

## A11Y-C · Keyboard operability

**Criteria.** 2.1.1 Keyboard A · 2.1.2 No Keyboard Trap A · 2.1.4 Character Key
Shortcuts A.

**Check.** Unplug the mouse. Complete each core task using only the keyboard.
Every interactive element must be reachable and operable; nothing may trap
focus.

**Where it breaks, reliably:** custom selects and comboboxes, date pickers,
sliders, drag-and-drop, carousels, tree views, canvas-based interfaces,
`<div onClick>` with no role or key handler, hover-only menus, modals, rich text
editors, and anything with a custom scroll container.

**Fails like.**
- A control reachable but not operable (focus lands, `Enter`/`Space` do
  nothing).
- Arrow keys not working in a composite widget (menu, tabs, listbox, grid).
- Focus entering a widget and unable to leave.
- Drag-and-drop as the only way to reorder or upload.
- A single-character shortcut that fires while typing in a field.
- Hover-revealed actions with no keyboard equivalent.
- A modal that lets focus escape to the page behind.

**Fix.** Native elements first. Where custom, implement the full WAI-ARIA
Authoring Practices pattern for that widget — role, states, and the complete key
set. Every drag interaction gets a keyboard alternative. Single-key shortcuts
must be remappable, disableable, or active only on focus.

---

## A11Y-D · Focus visibility

**Criterion.** 2.4.7 Focus Visible AA. (2.4.11 Focus Appearance is AAA in 2.2 —
useful as guidance for sizing the indicator, not as an AA requirement.)

**Check.** Tab through. Is the focused element **always** obviously identifiable?
Does the indicator meet 3:1 against its background? Is it visible against every
surface it can appear on — including inside modals, on brand fills, and in dark
mode?

**Fails like.**
- `outline: none` in a global reset with nothing replacing it. The single most
  common accessibility defect in production web software.
- A focus style that only works on white, invisible on dark surfaces or coloured
  fills.
- Focus and hover styled identically, so keyboard users can't tell where they
  are.
- The default outline replaced with a 1px low-contrast border.
- Focus indicator clipped by `overflow: hidden` on a parent.
- Focus visible on some component types and not others.
- Custom controls with no focus style at all.

**Fix.** Never remove focus indication — restyle it. A ring meeting 3:1 against
adjacent colours, offset so it isn't clipped, adapted per surface.
`:focus-visible` is the right selector for suppressing it on mouse clicks while
keeping it for keyboard — check the product isn't using `:focus { outline: none }`
and calling that the same thing.

---

## A11Y-E · Focus order and management

**Criteria.** 2.4.3 Focus Order A · 3.2.1 On Focus A · 2.4.1 Bypass Blocks A.

**Check.** Does tab order follow visual reading order? When a dialog, drawer, or
menu opens, does focus move into it and return to the trigger on close? When
content is inserted or removed, where does focus go? Is there a skip link past
repeated navigation?

**Fails like.**
- DOM order diverging from visual order (CSS `order`, `flex-direction: reverse`,
  absolute positioning).
- Positive `tabindex` values creating an unpredictable sequence.
- A modal opening with focus left behind it, so a keyboard user tabs through the
  page underneath.
- Focus lost to `<body>` after closing a dialog or removing a row — the user is
  returned to the top of the document.
- No skip link, so every page starts with 30 tab stops through the nav.
- Focus jumping automatically on typing (auto-advancing OTP fields that then
  can't be corrected by backspace).
- A route change that doesn't move focus or announce the new page — a
  single-page-app defect that's invisible to sighted mouse users.

**Fix.** DOM order matches visual order; no positive `tabindex`. Explicit focus
management on open, close, insert, remove, and route change. A skip link as the
first focusable element. On SPA navigation, move focus to the new main heading
and announce it.

---

## A11Y-F · Target size and spacing

**Criterion.** 2.5.5 Target Size is AAA in 2.1; **2.5.8 Target Size (Minimum) is
AA in WCAG 2.2** at 24×24 CSS px. Platform guidance is stricter and is the
better standard to hold: **44×44pt on iOS, 48×48dp on Android.**

**Check.** Measure the actual hit area — not the glyph. Icon buttons, close
controls, checkboxes and radios, table row actions, inline links in dense text,
carousel controls, and anything in a toolbar.

**Fails like.**
- A 16px close icon with no padding.
- Adjacent small targets with no spacing, so the wrong one is hit.
- A checkbox where only the box is clickable, not the label.
- Row actions sized for a cursor on a touch-capable device.
- A tap target that overlaps a scroll or swipe gesture area.

**Fix.** Pad the hit area even where the visual glyph stays small. Associate
labels with their controls so the label is part of the target. Space adjacent
targets. Note that 2.5.8 has exemptions (inline text links, targets whose size is
determined by the user agent) — apply them rather than over-reporting.

---

## A11Y-G · Semantics and structure

**Criteria.** 1.3.1 Info and Relationships A · 4.1.2 Name, Role, Value A ·
2.4.6 Headings and Labels AA · 3.1.1 Language of Page A.

**Check.** Is the page built from elements that mean what they are? Headings in
a logical order with no skipped levels? Landmarks present (`main`, `nav`,
`header`, `footer`)? Lists as lists, tables as tables with header associations?
Is `lang` set, and updated for inline foreign-language content?

**Fails like.**
- `<div onClick>` as a button — no role, no keyboard, no focus.
- `<a>` used for an action, `<button>` used for navigation.
- Heading level chosen for its size (`<h4>` because it looked right).
- Multiple `<h1>`s, or none.
- A table built from `<div>`s, so screen-reader table navigation gives no column
  context.
- A list built from `<div>`s, so the count isn't announced.
- No landmarks, so there's no way to skip regions.
- ARIA applied over the wrong element to patch it (`role="button"` on a `<div>`
  with no `tabindex` and no key handler is still broken).
- `aria-hidden` on something focusable.
- Missing `lang`, so a screen reader reads French with English phonemes.

**Fix.** Native semantics first — a `<button>` gets keyboard, focus, and role
for free. Heading levels reflect structure, size comes from CSS. Landmarks
present. ARIA only where no native element exists, and then complete: role,
states, and keyboard behaviour together. **The first rule of ARIA is not to use
ARIA when HTML would do.**

---

## A11Y-H · Names, labels, and descriptions

**Criteria.** 4.1.2 Name, Role, Value A · 2.5.3 Label in Name A · 1.3.5 Identify
Input Purpose AA.

**Check.** Does every interactive element have an accessible name? For elements
with visible text, does the accessible name **contain** that visible text (so
voice control works)? Do inputs have `autocomplete` tokens where a standard
purpose applies?

**Fails like.**
- Icon-only buttons with no `aria-label`.
- An `aria-label` of "Click here" or "Button".
- A visible label of "Send" with an `aria-label` of "Submit form" — voice
  control users saying "click Send" get nothing.
- A label associated by proximity rather than `for`/`id`.
- Placeholder as the only label (see `forms-and-input.md`, FORM-B).
- Multiple elements with identical accessible names on one page ("Edit" ×12,
  with no indication of what).
- Missing `autocomplete` on name, email, address, and payment fields.

**Fix.** Every control named; the name describes the action and its object
("Edit invoice 3312"). Where visible text exists, it's part of the accessible
name. `autocomplete` tokens on standard-purpose inputs — this is both an AA
criterion and a large usability win (FORM-F).

---

## A11Y-I · Images and alt text

**Criterion.** 1.1.1 Non-text Content A.

**Check.** Every image: is it informative, decorative, or functional? Informative
images need alt text conveying the information; decorative images need `alt=""`;
functional images (an icon that is the button) need alt describing the *action*.

**Fails like.**
- Missing `alt` entirely, so screen readers read the filename.
- `alt="image"`, `alt="photo"`, `alt="icon"`.
- Decorative images with descriptive alt, adding noise.
- A chart with `alt="chart"` and no data alternative (see `data-display.md`,
  DATA-M).
- Text baked into an image with no text equivalent.
- An icon inside a labelled button also having alt text, so it's announced
  twice.
- Alt text describing appearance rather than meaning ("green circle" rather than
  "online").

**Fix.** Alt conveys the *function or information*, not the appearance. `alt=""`
for decoration. Complex images (charts, diagrams, infographics) get a longer
text alternative nearby or a data table.

---

## A11Y-J · Forms and errors

**Criteria.** 3.3.1 Error Identification A · 3.3.2 Labels or Instructions A ·
3.3.3 Error Suggestion AA · 3.3.4 Error Prevention AA.

**Check.** Are errors identified in text (not colour alone)? Are they
programmatically associated with their field? Are they announced when they
appear? Is a correction suggested? For legal, financial, or data-modifying
submissions: is the submission reversible, checked, or confirmed?

**Fails like.**
- Error shown as a red border only.
- Error text visually adjacent but not linked by `aria-describedby`.
- Errors appearing on submit with no announcement and no focus move.
- An error summary at the top that isn't focused and doesn't link to fields.
- Required state conveyed only by a red asterisk with no `required` attribute.
- Instructions and format requirements only appearing after failure.
- A financial or destructive submission with no review, no confirmation, and no
  reversal (also `feedback-and-states.md`, ERR-A).

**Fix.** Text error, associated via `aria-describedby`, announced via a live
region or by moving focus. Suggest the correction where it's knowable. `required`
and `aria-invalid` set programmatically. Error summary focused on submit, with
links to each field.

---

## A11Y-K · Dynamic content and live regions

**Criterion.** 4.1.3 Status Messages AA.

**Check.** When something changes without a page reload — a toast, a validation
result, a search result count, a loading completion, a cart total — is it
announced? Are live regions present and at the right politeness?

**Fails like.**
- Toasts with no `aria-live`, so screen-reader users never learn the action
  succeeded.
- Search results updating silently.
- A loading spinner with no `aria-busy` and no completion announcement.
- Everything in `aria-live="assertive"`, interrupting constantly.
- A live region injected *with* its content, so nothing is announced (the region
  must exist in the DOM before the content changes).
- Infinite scroll appending content with no announcement and no way to reach the
  footer.

**Fix.** `role="status"` / `aria-live="polite"` for the ordinary case;
`assertive` only for genuine interruptions. Region present in the DOM before
content arrives. Announce result counts, completion, and failure.

---

## A11Y-L · Motion and animation

**Criteria.** 2.3.1 Three Flashes A · 2.2.2 Pause, Stop, Hide A · 2.3.3
Animation from Interactions AAA (worth checking regardless).

**Check.** Is `prefers-reduced-motion` respected, with a genuinely calm
fallback? Can auto-playing motion be paused? Does anything flash more than three
times per second? Is there large-scale parallax or zoom on scroll?

**Fails like.**
- `prefers-reduced-motion` unhandled anywhere in the codebase — searchable, and
  a reliable finding.
- A reduced-motion fallback that just shortens the animation.
- Auto-playing carousels with no pause.
- Parallax, scroll-jacking, or full-screen transitions with no reduced path.
- Looping animation in the content area with no stop.
- Skeleton shimmer with no reduced-motion fallback to a static fill.

**Fix.** Honour the media query with a static or simple cross-fade alternative.
Pause controls on anything auto-playing over five seconds. This matters
materially for people with vestibular disorders — it's not a preference setting.

---

## A11Y-M · Zoom, reflow, and text spacing

**Criteria.** 1.4.4 Resize Text AA · 1.4.10 Reflow AA · 1.4.12 Text Spacing AA.

**Check.** Zoom to 200%: is all content and functionality available? At 400%
(equivalent to 320px width): does content reflow to one column with no
two-dimensional scrolling? Apply the 1.4.12 text-spacing overrides (line height
1.5×, paragraph spacing 2×, letter spacing 0.12em, word spacing 0.16em): does
anything clip or overlap?

**Fails like.**
- Fixed-height containers clipping text at larger sizes.
- Horizontal scrolling required at 320px equivalent.
- A layout locked with `user-scalable=no` or `maximum-scale=1` in the viewport
  meta — a straightforward failure and a one-line fix.
- Text in `px` inside containers sized in `px`, so nothing scales.
- Sticky headers consuming most of the viewport when zoomed.
- Overlap when line height increases.

**Fix.** Remove zoom restrictions. Relative units for text and containers.
Containers that grow with content. Test at 200% and 400%, and with the text
spacing overrides applied.

---

## A11Y-N · Timing

**Criteria.** 2.2.1 Timing Adjustable A · 2.2.6 Timeouts AAA (worth checking).

**Check.** Are there time limits — session expiry, OTP windows, carousels,
auto-dismissing messages, checkout holds? Can they be extended, turned off, or
at least warned about? Is data lost on timeout?

**Fails like.** Session expiry with no warning, losing form data; an OTP window
too short to retrieve the code from another device; auto-dismissing
notifications carrying the only route to an action; a countdown on a form with
no extension.

**Fix.** Warn before expiry with an extend option. Preserve data across
timeouts. Make auto-dismiss durations proportional and provide a persistent
alternative for anything actionable.

---

## A11Y-O · Media

**Criteria.** 1.2.2 Captions A · 1.2.3 Audio Description or Media Alternative A
· 1.2.5 Audio Description AA · 1.4.2 Audio Control A.

**Check.** Do videos have captions? Are they real captions, or auto-generated
and uncorrected? Is there a transcript? Does visual-only information have an
audio description or a text equivalent? Does anything auto-play with sound?

**Fails like.** No captions; auto-captions with domain terms mangled; a product
demo video whose content exists nowhere in text; auto-playing audio with no
immediate stop; a video player whose controls aren't keyboard operable.

**Fix.** Corrected captions, transcripts, no auto-play with sound, keyboard-
operable player controls.

---

## A11Y-P · Pointer, gesture, and orientation

**Criteria.** 2.5.1 Pointer Gestures A · 2.5.2 Pointer Cancellation A · 2.5.4
Motion Actuation A · 1.3.4 Orientation AA.

**Check.** Does anything require a multi-point or path-based gesture (pinch,
two-finger, swipe-along-a-path) with no single-pointer alternative? Does anything
activate on `pointerdown` rather than `pointerup`, so it can't be aborted by
dragging away? Is any function triggered only by device motion (shake, tilt)?
Is the product locked to one orientation without a good reason?

**Fails like.** Pinch-zoom as the only way to see detail; swipe-to-delete with
no button alternative; a slider operable only by drag; an action firing on touch
down so a mis-tap can't be cancelled; shake-to-undo as the only undo;
orientation locked to portrait on a tablet.

**Fix.** Single-pointer alternative for every path or multipoint gesture.
Activate on up, not down. A UI alternative for every motion trigger. Support
both orientations unless the content genuinely requires one.

---

## A11Y-Q · Screen-reader flow

**Check.** Where possible, run a screen reader (VoiceOver on macOS/iOS, NVDA on
Windows, TalkBack on Android) through one core task. Listen for: elements
announced with no name or as "clickable"; reading order diverging from visual
order; state changes not announced; decorative content announced; a
never-ending list because it isn't marked up as one.

**Why it matters.** This is where the difference between "passes an automated
check" and "is usable" appears, and it's the evidence that makes an
accessibility audit credible.

**If you cannot run one** — say so explicitly. Semantic findings from code are
`Inferred`, not `Observed`. Don't describe an announcement you didn't hear.

---

## Contrast math

WCAG 2.x contrast ratio, for reference and for checking a tool's output:

```
For each sRGB channel c in {R, G, B}, normalized to 0–1:
    c_lin = c / 12.92                    if c <= 0.03928
    c_lin = ((c + 0.055) / 1.055) ^ 2.4  otherwise

L = 0.2126·R_lin + 0.7152·G_lin + 0.0722·B_lin

ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

Range 1:1 (identical) to 21:1 (black on white).

**Use `scripts/contrast-check.py`** rather than computing by hand — it takes a
pair, a foreground against several backgrounds, or a whole palette, reports
AA/AAA pass/fail for normal, large, and non-text, and suggests the nearest
passing shade.

**Three traps:**
- **Opacity is not colour.** A colour at 60% alpha composites against whatever is
  behind it — compute the composited value, not the source colour.
- **Text over an image or gradient** varies across its area. It must pass at the
  worst point, not the average.
- **WCAG 2.x contrast is known to be imperfect** for some hue pairs (it can pass
  combinations that read poorly, and fail some that read fine). It is
  nonetheless the AA standard and what a conformance claim is measured against —
  report against it, and note perceptual concerns separately rather than
  substituting your own threshold.

---

## Writing an accessibility finding

Accessibility findings are the most likely in the whole audit to be dismissed as
theoretical, so make them concrete:

- **Name the criterion and level** — `1.4.3 Contrast (Minimum), AA`. It makes
  the finding checkable and connects it to whatever conformance obligation the
  team has.
- **Give the measurement**, not an impression. "3.21:1, AA needs 4.5:1."
- **Name who it affects and how** — "a keyboard user cannot reach the Save
  control on this screen at all", not "this is an accessibility issue".
- **Give the fix as a value or an attribute**, not a principle.
- **Say how you tested.** Automated tool, manual keyboard pass, screen reader,
  or code reading — each supports a different confidence.
- **Don't claim conformance either way.** An audit samples; it doesn't certify.
  "No conformance claim is made" belongs in the scope section.
- **Where the product has a legal obligation** (public sector, EAA, ADA
  exposure, procurement requirements), note it as a factor — as context for
  prioritization, not as legal advice.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| A core task cannot be completed by keyboard alone | **Blocker** |
| Keyboard trap | **Blocker** |
| A core task cannot be completed with a screen reader | **Blocker** |
| Form errors neither identified in text nor associated with fields, blocking submission | **Blocker** |
| No focus indication anywhere (global `outline: none`) | **High** |
| Body text failing 4.5:1 on primary content | **High** |
| Interactive controls with no accessible name | **High** |
| Meaning by colour alone on a core path | **High** |
| `user-scalable=no` / zoom disabled | **High** — one-line fix |
| Missing alt on informative images | **High** |
| Focus lost or unmanaged around dialogs and route changes | **High** |
| Custom widget missing its ARIA keyboard pattern | **High** |
| Status messages not announced | **Medium** |
| `prefers-reduced-motion` unhandled | **Medium** |
| Target size under platform minimum | **Medium** (**High** on touch-primary products) |
| Heading structure wrong or levels skipped | **Medium** |
| Reflow issues at 400% zoom | **Medium** |
| Missing landmarks or skip link | **Medium** |
| Non-text contrast (borders, icons) below 3:1 | **Medium** |
| Redundant or verbose alt text | **Low** |

Accessibility findings are graded on **user consequence like everything else** —
but note that a criterion failure is a criterion failure regardless of severity,
and a team with a conformance obligation may need to fix Lows they'd otherwise
defer. Say so where it applies; don't inflate severity to force the point.
