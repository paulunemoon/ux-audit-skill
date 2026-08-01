# D9 · Visual hierarchy & layout

> **When to read:** Any audit with visual evidence — screenshots, a live
> product, or Figma. Finding IDs: `VIS-nn`.
>
> **Anatomy is an example, not a mandate.** No number in this file is a
> requirement. Radius can be 0 or fully round; density can be tight or generous;
> a product can be dark, light, or both. You are auditing whether the choices
> **read as choices and hold consistently**, not whether they match a taste
> written here. Token-level consistency is `design-system.md` (D10); this file is
> what the eye does on the screen.

## Table of contents
1. [VIS-A · Scan path and the focal point](#vis-a--scan-path-and-the-focal-point)
2. [VIS-B · Spending the hierarchy tools in order](#vis-b--spending-the-hierarchy-tools-in-order)
3. [VIS-C · Grouping and proximity](#vis-c--grouping-and-proximity)
4. [VIS-D · Density and whitespace](#vis-d--density-and-whitespace)
5. [VIS-E · Alignment and rhythm](#vis-e--alignment-and-rhythm)
6. [VIS-F · Colour count and meaning](#vis-f--colour-count-and-meaning)
7. [VIS-G · Action hierarchy](#vis-g--action-hierarchy)
8. [VIS-H · Elevation and depth language](#vis-h--elevation-and-depth-language)
9. [VIS-I · Generated-UI tells](#vis-i--generated-ui-tells)
10. [VIS-J · Imagery, icons, and illustration](#vis-j--imagery-icons-and-illustration)
11. [VIS-K · Dark mode as a decision](#vis-k--dark-mode-as-a-decision)
12. [Severity calibration](#severity-calibration-for-this-file)

---

## VIS-A · Scan path and the focal point

**Check.** Look at each key screen for two seconds and note what you saw first,
second, third. Compare that to what the screen is *for*. Is there one clear
focal point, or does everything compete? On a screen whose job is a single
number (a balance, a total, a score, a status), is that number unmistakably the
thing?

**Why it matters.** Hierarchy is how a user skips the 90% of the screen that
isn't their business today. Without it every visit costs a full read.

**Fails like.**
- Every card the same size, weight, and colour, so the important one doesn't
  lead.
- The primary metric rendered as one tile in a grid of equals, when it's the
  reason the screen exists.
- Two or three elements all styled as the hero.
- The most visually prominent element being decorative — an illustration, a
  banner, a chart with no reading — while the actual content sits quiet.
- A screen where the eye lands on the nav or a promotional banner before the
  content.
- On mobile, the primary action below the fold or in the top corner rather than
  in reach.

**Fix.** Name the intended focal point per screen and what should change to make
it lead — usually position and size before anything else. One hero per screen.
If the hierarchy needs colour to read, it hasn't been established yet.

---

## VIS-B · Spending the hierarchy tools in order

**Check.** Hierarchy has four levers, strongest first: **position → size →
weight → colour.** Audit whether the product spends them in that order, or
reaches for colour to fix a layout problem.

**Why it matters.** Position and size work for everyone, including in
greyscale, at a glance, and for colour-blind users. Colour is the weakest and
least accessible lever, so a hierarchy built on it fails first.

**Fails like.**
- Importance signalled only by a coloured background on otherwise identical
  cards.
- Everything at the same size, differentiated by tint.
- Three type sizes doing the work of seven levels of meaning.
- A hierarchy that disappears entirely when you view the screen in greyscale —
  a fast, cheap test worth running on every key screen.

**Fix.** Establish the hierarchy in position and size first; use weight for the
next step; keep colour for meaning (state, interactivity, direction) rather than
for rank.

---

## VIS-C · Grouping and proximity

**Check.** Are related things visually related? Is the gap *within* a group
smaller than the gap *between* groups? Are labels closer to their own fields
than to the field above? Do borders and backgrounds group things that belong
together, or slice things that don't?

**Why it matters.** Proximity is read pre-attentively — before the user has
read a word. Wrong grouping actively misinforms.

**Fails like.**
- Equal spacing everywhere, so nothing groups.
- A label equidistant between two fields, ambiguously belonging to either.
- A helper message closer to the next field than the one it describes.
- Related actions split across opposite ends of a toolbar.
- A card border around unrelated content, or none around genuinely related
  content.
- Dividers doing grouping work that spacing should do (see VIS-I).

**Fix.** Enforce the spacing relationship — within < between — as a rule, not
per screen. Name the specific groups that read wrong.

---

## VIS-D · Density and whitespace

**Check.** Is the density appropriate to the audience and the task, and
consistent within a view? An expert data screen may legitimately be dense; a
mainstream onboarding shouldn't be. The defect is not "too dense" or "too airy"
— it's density that **fights the task** or **changes mid-screen**.

**Why it matters.** Density is where the audience call becomes visible. Judging
a trading terminal by a consumer app's whitespace is exactly the cargo-culting
this skill forbids.

**Fails like.**
- Comfortable and dense treatments mixed in one view, so rows look
  inconsistently important.
- A data table with so much padding that a screenful shows five rows, for users
  who compare fifty.
- A mainstream signup with expert-terminal density.
- Whitespace so uniform that no grouping reads (see VIS-C).
- Fixed-height rows that force truncation of content that would fit.
- Vertical space on mobile spent on decoration, pushing content below the fold.

**Fix.** State the intended density per surface, and flag the surfaces that
deviate. Where the product serves both audiences, a density toggle is a real
answer — say so rather than picking one.

---

## VIS-E · Alignment and rhythm

**Check.** Do elements align to a consistent grid? Are spacing values drawn from
a scale, or arbitrary? Is the vertical rhythm regular between comparable
sections? Do optical alignments (icon to text baseline, number to number) hold?

**Why it matters.** Misalignment reads as carelessness before it reads as
anything specific, and it's cumulative — a screen with twenty near-misses feels
wrong without the user being able to say why.

**Fails like.**
- Left edges that almost line up — 16px here, 18px there.
- Off-scale spacing (13px, 27px) among a base-4 or base-8 system.
- Icons vertically centred by container rather than optically to the text.
- Numbers in a column not right-aligned, so magnitude can't be compared.
- Section gaps varying with no meaning.
- Card grids where the last row's items stretch or orphan.

**Fix.** Report off-scale values with locations — this overlaps D10 and is
usually best delivered as one consolidated drift list (`design-system.md`).
Right-align numeric columns; optically align icons.

---

## VIS-F · Colour count and meaning

**Check.** Count the distinct hues on a single screen. Does each one mean
something, or is colour being used as decoration? Is any meaning carried by
colour **alone** — status, direction, category, selection?

**Why it matters.** A screen where every card, icon, badge, and stat wears a
different bright colour has no hierarchy left: when everything is emphasized,
nothing is. And colour-only meaning is inaccessible to a significant share of
users and invisible in greyscale printing.

**A working budget for a typical screen:** neutrals do most of the work · one
accent on the key and interactive elements · status colours only where there is
real status · a data palette only inside data visualization.

**Fails like.**
- Six differently-coloured stat cards where none of the colours mean anything.
- A screen speckled with coloured badges.
- Up/down, positive/negative, or pass/fail shown by colour with no sign, icon,
  or label.
- Selection indicated only by a tint.
- Brand accent applied to non-interactive elements, so users can't tell what's
  clickable.
- Status colours reused for data series, so a red data point looks like an
  error.

**Fix.** Pull colour out until the hierarchy reads through position and size,
then add it back only where it carries meaning. Pair every colour-coded meaning
with a second channel (sign, icon, label, pattern). This is simultaneously a D12
finding — cross-reference it.

---

## VIS-G · Action hierarchy

**Check.** Per screen: how many actions look primary? Is the primary action the
one the screen is for? Are destructive actions visually distinct from
constructive ones? Is it possible to tell what's clickable without hovering?

**Why it matters.** If two things look primary, neither is, and the user has to
read to decide — which is exactly what visual hierarchy exists to avoid.

**Fails like.**
- Multiple filled brand-coloured buttons on one screen.
- The destructive action styled identically to the safe one.
- `Cancel` styled as prominently as `Confirm`.
- Ghost/text buttons indistinguishable from static labels.
- Clickable cards or rows with no affordance until hover — and therefore no
  affordance at all on touch.
- The primary action of a screen sitting in an overflow menu.
- A disabled control styled so faintly it reads as a heading.

**Fix.** One primary per view; everything else steps down. Destructive gets its
own treatment and is never the pre-focused default. Interactive elements are
identifiable at rest, not only on hover.

---

## VIS-H · Elevation and depth language

**Check.** Does the product have one coherent way of expressing layers — borders,
shadows, background steps, or nothing — used consistently? Or do different
surfaces use different mechanisms at the same level?

**Fails like.**
- Some cards with shadows, some with borders, some with both, at the same
  elevation.
- Shadow direction or colour varying between components.
- Grey shadows in dark mode (they should be heavier and black; light mode wants
  a tinted ink, not pure grey).
- An overlay that doesn't read as above the content.
- Nested surfaces with no elevation difference, so the nesting doesn't read.

**Fix.** Name the elevation levels the product actually uses and the mechanism
for each; list the components that deviate.

---

## VIS-I · Generated-UI tells

**Check.** These are patterns that reliably indicate an interface assembled from
defaults rather than designed. **Each one is only a finding when it costs the
user something** — say what the cost is, don't cite the pattern. Where the cost
is purely that it looks templated, that's an Opportunity or Taste, not a defect.

| Tell | What it costs |
|---|---|
| **Two-colour diagonal gradient on near-black** (especially two ecosystem/brand colours) | No differentiation — the product is visually interchangeable with its category. Often also a contrast problem for text laid over it. |
| **Glassmorphism everywhere** — translucent blurred panels stacked on a busy backdrop | Text contrast varies with whatever scrolls behind it, so legibility is non-deterministic. A real D12 failure, not just a look. |
| **Glow / neon** — outer glow on CTAs, glowing borders, laser lines | Visual noise competing with the actual hierarchy; glow around a button obscures its edge and its focus ring. |
| **Pure `#000` plus one saturated accent, no tinted neutrals** | No elevation hierarchy is expressible; surfaces can't be distinguished, and high-chroma-on-pure-black vibrates. |
| **Status pills as chrome** — "● Live", "Beta", "Demo", "Preview" as ambient decoration | Devalues real status indication; users stop reading badges. Also colour-only if the dot carries the meaning. |
| **One-sided borders on rounded cards** — a top hairline or left stripe that follows the radius and dies mid-curve | Reads as a rendering artefact rather than a decision; it's one of the clearest generated-UI signals. **A card's stroke is on all four sides or on none.** |
| **Decorative schematic diagrams** — node graphs, isometric 3D "how it works", floating boxes and arrows | Occupies the space where an explanation or a real product view would go, and explains nothing. |
| **Unrequested decorative microcopy** — eyebrow pills above headlines, reassurance tags under CTAs | Dilutes the copy that matters (see `content-and-copy.md`, COPY-G). |
| **A typeface chosen by reflex** rather than for this product | The defect is the *absence of a decision*, not the number of families. One face used with real hierarchy is good design; a second display face nobody chose is decoration. |
| **Dark mode by reflex** | See VIS-K. |
| **Dividers between every section** | Slices the page into template bands; where the next section already has its own background, a border on top of it is redundant. |

**On the one-sided border specifically** — when an edge accent genuinely carries
meaning (a status row, a selected item), give it its **own geometry**: a
full-height stripe clipped inside the radius with square ends, a `/subtle`
background tint, or a leading icon. Any of those survives the corner. A
single-edge line is still correct as a *separator* between stacked list items,
and on square-cornered surfaces where there's no curve to break.

**On diagrams** — the one that earns its place connects **real UI cards** with
quiet flow lines to show sequence: thin border-weight strokes, no glow, no
gradient, no animated dashes. The cards are the content; the lines only clarify
order. Free-floating node-graph art is decoration.

---

## VIS-J · Imagery, icons, and illustration

**Check.** Is the icon set one family at one weight and one size scale, or a mix
of a library and hand-drawn one-offs? Are icons ever used where a label is
needed? Are images sized, cropped consistently, and meaningful? Is there any
place an emoji stands in for a functional icon?

**Why it matters.** Mixed icon stroke weights are one of the most visible
inconsistencies in an interface, and icon-only controls without labels are a
recurring findability and accessibility failure.

**Fails like.**
- Two icon libraries in one product (different stroke language, different
  optical sizes).
- Hand-drawn inline SVGs alongside library icons.
- Icon-only controls with no label, no tooltip, and no accessible name.
- The same icon meaning two things, or two icons meaning one thing.
- Directional pairs (send/receive, in/out, up/down) sharing a rotated glyph, so
  they're confusable at a glance.
- Meaning carried by icon colour alone.
- Generic stock illustration where the product should be shown.
- Placeholder or broken images, empty avatar circles, missing logos.

**Fix.** One set, one weight, one size scale. Define each meaning once in a
single lookup so the same concept can't drift between screens. Every icon-only
control gets an accessible name and, on desktop, a tooltip. Every image slot
gets a defined fallback — a monogram, initials, or a shaped placeholder — so a
missing asset never renders as a broken slot.

**Sensible defaults for a remediation proposal** (offer, don't impose): a single
well-built icon library for web and cross-platform work — Phosphor is a
reasonable default where it ships natively; **SF Symbols on native iOS and
Material Symbols on native Android**, where a third-party set breaks the
platform's weight and optical matching.

---

## VIS-K · Dark mode as a decision

**Check.** If the product is dark: is that a decision the product's use case
supports (prolonged use, data-dense, low-light contexts, a deliberate brand
position) or a default? If it offers both modes, is the light mode actually
finished, or a mechanical inversion? Does it follow the OS preference, and can
that be overridden?

**Why it matters.** A half-finished second mode is worse than one good mode —
users who prefer it get a degraded product, and it doubles the surface where
contrast failures hide.

**Fails like.**
- Light mode with dark-mode contrast ratios inverted and never re-checked.
- Pure `#000` backgrounds with a high-chroma accent and no tinted neutral steps,
  so no elevation hierarchy exists.
- Images, charts, illustrations, or logos that only work in one mode.
- No OS-preference detection, or detection with no manual override.
- Mode preference not persisted.
- Shadows unchanged between modes (dark needs heavier black; light wants a
  tinted ink rather than flat grey).

**Fix.** Audit both modes independently for contrast (`accessibility.md`) — a
palette that passes in one can fail in the other. If only one mode is real,
recommend committing to it rather than shipping a broken second.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Text illegible over a variable background (glass, gradient, image) | **High** (also A11Y) |
| Meaning carried by colour alone on a core path | **High** (also A11Y) |
| No visible affordance for the primary action on touch | **High** |
| The screen's purpose is unreadable at a glance — no focal point | **High** on a core screen, else **Medium** |
| Multiple competing primary actions | **Medium** |
| Density fighting the task for the stated audience | **Medium** |
| Mixed icon families / hand-drawn one-offs alongside a library | **Medium** |
| Broken image slots, empty avatars, missing marks | **Medium** |
| Light mode unfinished while offered | **Medium**–**High** by how it's surfaced |
| Grouping that misleads (proximity wrong) | **Medium** |
| One-sided borders, decorative diagrams, glow, gradient tells | **Low**–**Medium** — grade by the cost you can name, and label pure-look items as Taste |
| Off-scale spacing, minor misalignment | **Low** (consolidate into the D10 drift list) |
| Dark-vs-light preference, radius and shape choices | **Taste** — label it, never grade High |
