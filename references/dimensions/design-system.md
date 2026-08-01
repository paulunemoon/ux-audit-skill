# D10 · Design system consistency

> **When to read:** Whenever you have code, Figma variables, or enough screens
> to compare. This is the `tokens` mode's whole subject. Finding IDs: `DS-nn`.
>
> **You audit the product against the system it chose, not against this file.**
> Every value here is one reasonable taste. A product on a base-5 spacing scale
> with fully-square corners and one typeface is not wrong; a product with four
> spacing systems and eleven greys is. **The finding is drift, not deviation from
> a number written here.**

## Table of contents
1. [DS-A · Does a system exist?](#ds-a--does-a-system-exist)
2. [DS-B · Token layering](#ds-b--token-layering)
3. [DS-C · Colour drift](#ds-c--colour-drift)
4. [DS-D · Fill legibility](#ds-d--fill-legibility)
5. [DS-E · Neutrals](#ds-e--neutrals)
6. [DS-F · Status and data colours](#ds-f--status-and-data-colours)
7. [DS-G · Typography — the four hard checks](#ds-g--typography--the-four-hard-checks)
8. [DS-H · Type scale and roles](#ds-h--type-scale-and-roles)
9. [DS-I · Spacing scale and rhythm](#ds-i--spacing-scale-and-rhythm)
10. [DS-J · Radius, border, and shape language](#ds-j--radius-border-and-shape-language)
11. [DS-K · Component drift](#ds-k--component-drift)
12. [DS-L · Component foundation — hand-rolled versus proven](#ds-l--component-foundation--hand-rolled-versus-proven)
13. [DS-M · Breakpoints](#ds-m--breakpoints)
14. [DS-N · Design-to-build drift](#ds-n--design-to-build-drift)
15. [How to report drift](#how-to-report-drift)
16. [Severity calibration](#severity-calibration-for-this-file)

---

## DS-A · Does a system exist?

**Check.** Before grading adherence, establish what there is: a token file, a
Tailwind theme, CSS custom properties, Figma variables, a component library, a
documented set of rules — or none of it. Find it via the inventory table in
`evidence-intake.md`.

**Why it matters.** "Inconsistent with the design system" is meaningless when
there isn't one. In that case the finding is different and larger: there's no
shared vocabulary, so every screen re-decides everything and the drift will
keep growing.

**Three situations, three different findings:**
- **A system exists and is followed** → audit the gaps and the edges.
- **A system exists and is bypassed** → the finding is adherence. Quantify it:
  how many raw values, in how many files.
- **No system exists** → the finding is the absence. Recommend establishing the
  minimum (colour, spacing, type, radius) before anything else, because every
  other D10 finding is downstream of it.

---

## DS-B · Token layering

**Check.** Do components consume **semantic** tokens (`bg/surface`,
`text/secondary`, `brand/primary`) or **primitives** (`blue-500`, `gray-200`) —
or raw values? A healthy layering:

```
Primitive  →  Theme  →  Semantic  →  Component
(raw ramp     (brand ramp +   (bg / text /      (button uses
 50…950)       neutrals)       border / brand,    brand/primary,
                               resolved per       never brand-500)
                               dark & light)
```

**Why it matters.** The layering is what makes a rebrand or a mode switch a
token change instead of a codebase change. When components reach past the
semantic layer, dark mode and theming are permanently manual.

**Fails like.**
- Components referencing `gray-700` directly, so there is no single place to
  change "secondary text".
- Semantic names that are really primitives in disguise (`color-blue` as the
  brand token).
- Dark mode implemented as per-component overrides rather than a remapped
  semantic layer.
- A semantic layer that exists in Figma but not in code (or vice versa).
- One-off tokens created per feature (`checkout-button-bg`).

**Fix.** Name the specific components reaching past the layer, and the semantic
token each should use. Where the semantic layer is missing entirely, that's the
recommendation — a small set (four background steps, three or four text levels,
three border weights, the brand states) covers most products.

---

## DS-C · Colour drift

**Check.** Count the distinct colour values actually used, and compare against
the palette that's defined. Search for hex literals, `rgb()`, and `hsl()` in
component code. In Figma, run `get_variable_defs` across several frames and note
what's bound versus typed in.

**Why it matters.** Drift is what makes a product feel subtly assembled rather
than designed, and it makes global changes impossible — a "make the borders
lighter" request becomes a hunt.

**Fails like.**
- Eleven greys where the scale defines six.
- Near-duplicates: `#3B82F6` next to `#3C82F7`.
- A hard-coded hex sitting in the same file as the token that means the same
  thing.
- Opacity used to fake a shade (`brand at 40%`) instead of a ramp step, so the
  result depends on whatever is behind it.
- Colours defined in the theme and never used, alongside raw values that
  duplicate them.

**Fix.** Deliver the drift inventory: value, count, locations, and the token it
should map to. This is one of the few D10 findings that is genuinely mechanical
to fix and therefore an excellent quick win — but say honestly whether it's S
(a few dozen occurrences) or M/L (spread across a large codebase).

---

## DS-D · Fill legibility

**Check.** For every filled control — buttons, badges, chips, tags, status
fills, chart legend swatches — does the text on it meet **AA (≥4.5:1 for normal
text, ≥3:1 for large)**? Test the fill's actual on-colour, not an assumed one.

**Why it matters.** **A fill whose best on-colour — black *or* white — still
fails AA is not a usable text-bearing fill.** The failure to catch is a
**mid-tone** fill (a medium teal, olive, slate) where neither black nor white
reaches AA. Teams ship these because both options look "fine".

**Fails like.**
- White text on a mid-tone brand fill at 4.1:1.
- Dark text on a bright accent that measures 3.9:1.
- An on-colour picked by eye or by a lightness threshold rather than by measured
  contrast — the classic error is handing white ink to a colour that black
  clears more comfortably.
- Status fills (`warning` especially — amber is the usual culprit) with text
  that fails.
- A disabled state so low-contrast it's unreadable even as a disabled control.

**Fix.** Run `scripts/contrast-check.py` and put the measured ratios in the
finding — "4.12:1, AA needs 4.5" is unarguable where "looks low contrast" is
not. Where neither ink passes, the fix is to **shift the fill lighter or darker**
(a different ramp step) until one does, or to keep that shade as a non-text
surface only.

---

## DS-E · Neutrals

**Check.** Are the greys a deliberate ramp, or ad hoc? Are they pure grey, or
carrying a slight tint? Are there enough steps to express the elevation the
product needs (page background, surface, raised, muted) without opacity hacks?

**Why it matters.** Neutrals are 80% of the pixels. Pure `#FFFFFF`/`#000000`
with pure greys reads as unbranded and, at the dark end, gives no room for
elevation. A small consistent tint toward the brand hue is the cheapest
distinctiveness device there is — a fixed low chroma, not a share of the
accent's own, so a neon brand doesn't get neon greys.

**Fails like.**
- Pure `#000` page background with no surface steps above it.
- Greys sampled from different sources, some warm, some cool.
- Only three neutral steps, forcing opacity for everything else.
- Borders and text sharing the same neutral, so borders are too strong or text
  too weak.

**Fix.** A tinted neutral ramp with distinct steps for base, surface, raised,
muted, three border weights, and three or four text levels.
`scripts/generate-palette.py` produces one from any anchor hex if the
recommendation needs a worked example — **as an illustration, not a rebrand.**

---

## DS-F · Status and data colours

**Check.** Are status colours (success, error, warning, info) defined
independently of the brand hue? Is there a **separate palette for data
visualization**, or are UI and status colours reused for chart series?

**Why it matters.** Status must stay readable as green/amber/red/blue whatever
the brand is — a green-branded product whose success state is the brand colour
has no success state. And a red data point that shares a hex with the error
colour means a normal negative value looks like a failure.

**Fails like.**
- Success = brand colour on a green-branded product.
- Chart series pulled from status tokens, so a red line reads as an error.
- Positive/negative financial colours identical to success/error.
- Status colours defined for one mode only.
- No `/subtle` variants, so status backgrounds are made with opacity.

**Fix.** Fixed status hues, independent of brand, with base and subtle variants
per mode. A separate categorical data palette (rotating from the brand hue is a
good way to make it rhyme without colliding), plus distinct
positive/negative direction colours. Grid and axis colours mapped to neutrals.

---

## DS-G · Typography — the four hard checks

These four are worth checking on every product regardless of scope.

**1 · Script, handwriting, or cursive faces in the UI.** Flag on sight. They
read cheap, they're hard to read at small sizes, and they destroy the precision
any data-bearing or transactional interface needs. Legitimate only as a logotype
or in a deliberately expressive marketing moment the brand owns — never as UI or
body text.

**2 · Is the typeface a decision?** The defect is the **absence of a decision**,
not the number of families. One face chosen deliberately and used with real
hierarchy is good design. What to flag: a display or serif face added to make
headings look "designed" that appears nowhere in the brand and serves no
hierarchy the sans couldn't; more than two families in an app; or an
unmistakable default reached for by reflex with no evidence of a choice. When
the brand supplies a display face, check it's used for headings only and never
in running text.

**3 · Numbers use tabular figures — via `font-variant-numeric: tabular-nums`,
not a monospace font.** Any number that changes or aligns in a column
(balances, prices, table cells, timers, counters) needs fixed-width digits so
the value doesn't jitter and columns compare. **A monospace font is the wrong
fix**: it costs a second family, a weight mismatch, and a design compromise for
something one CSS property does. Most modern sans faces ship tabular figures; a
face without them is disqualified for a data-heavy product. Search the codebase
for `tabular-nums` — its complete absence in a product full of numbers is a
reliable finding.

**4 · Monospace only for genuinely code-like content.** Full untruncated
identifiers, hashes, or addresses shown as a block; raw signatures; actual code.
A truncated identifier doesn't need it. A product that surfaces no raw code
needs no mono token at all — its absence is correct, not a gap.

**Also check:** ultra-thin weights used as body text; more weights in use than
the system defines; a web font with no system fallback stack, so first paint is
broken or invisible; fonts loaded but never used.

---

## DS-H · Type scale and roles

**Check.** Is there a defined scale, and does the product use it? Count the
distinct font sizes actually rendered. Are sizes chosen from the scale, or typed
per component? Is the line height defined with each size?

**Why it matters.** An undefined scale produces a screen with nine sizes and no
hierarchy, and it makes responsive type impossible to reason about.

**Fails like.**
- Fourteen distinct font sizes across the product.
- Sizes that differ by 1px, which reads as a mistake rather than a step.
- Body text below 16px on mobile (which also makes iOS zoom on input focus —
  see `platform-mobile.md`).
- Line height unset or uniform across sizes, so headings are loose and body is
  cramped.
- Emphasis achieved with a heavier weight than the system defines.
- Heading *levels* chosen by appearance rather than structure (an `<h4>` used
  because it's the right size) — also a D12 semantics finding.

**Fix.** Report the size inventory and propose the consolidation. A working
shape: `xs 12/16 · sm 14/20 · md 16/24 · lg 18/26 · xl 20/28 · 2xl 24/32 ·
3xl 32/40`, three weights (regular, medium, semibold), one large moment per
screen. On mobile, 16 is the floor for primary body text; web can use 14 as a
dense base. Anything above 32 is display territory, set per project rather than
inside the app scale.

---

## DS-I · Spacing scale and rhythm

**Check.** Is spacing drawn from a scale (base-4 and base-8 are the common
ones)? Search for off-scale values. Is the rhythm consistent — the same gap
between comparable things across screens?

**Why it matters.** Off-scale spacing is the highest-volume drift in most
codebases and the most visible in aggregate. It's also the easiest to quantify,
which makes it a persuasive finding.

**Fails like.**
- `13px`, `27px`, `35px` in a base-4 system.
- Padding defined per component rather than from tokens.
- Two components at the same level using different internal padding.
- Section gaps varying with no meaning.
- Margins that collapse or double unintentionally between stacked components.
- Mobile using web spacing values, so screens waste scarce vertical space.

**Fix.** List the off-scale values and their locations. A workable rhythm:
compact internals 4–8 · component padding 12–16 · between related elements
16–24 · between sections 32–48 · between page regions 64. Mobile compresses the
top end (sections 24–32, rarely more) and uses a smaller screen-edge margin
(~16, 20 max) plus safe-area insets.

---

## DS-J · Radius, border, and shape language

**Check.** Is there a radius scale, and is it applied consistently at each
component level? Does nesting step down (a child inside a rounded parent takes a
smaller radius)? Is border weight consistent, and does the product use borders,
shadows, or background steps to separate — consistently?

**Why it matters.** Shape is one of the strongest brand signals a UI has, and
it's binary: consistent shape reads as designed, mixed shape reads as assembled.
**Any radius is right** — square, soft, fully round — as long as it's chosen and
held.

**Fails like.**
- Buttons at 6px, inputs at 8px, cards at 12px, modals at 16px, with no rule.
- A child element with a larger radius than its parent, so the corners fight.
- Pill-shaped and square-cornered controls at the same level.
- Border widths of 1px and 1.5px and 2px with no meaning.
- Card separation done by border in some places and shadow in others (see
  `visual-hierarchy.md`, VIS-H).
- One-sided borders on rounded surfaces (VIS-I).

**Fix.** Name the levels and the value each should take; list the components
that deviate.

---

## DS-K · Component drift

**Check.** Find every variant of the same conceptual component. How many button
implementations exist? How many card shells, input styles, modal containers,
empty-state layouts? Are they variants of one component, or separate
implementations that have diverged?

**Why it matters.** Component drift is the compounding cost — every divergent
copy has to be fixed separately, and each one will drift further.

**Fails like.**
- Three button components with overlapping variants.
- A component in the library plus several bespoke re-implementations in feature
  code.
- The same visual variant achieved by different means in different places.
- Props that mean different things in different components (`variant` /
  `type` / `kind` / `intent` for the same concept).
- A component library where half the product doesn't use it.
- One-off components created because the shared one was 90% right and nobody
  extended it.

**Fix.** Inventory: concept, implementations, locations, and which one should
become canonical. Say which of the divergences are legitimate variants worth
absorbing into the shared component versus accidental duplication to delete.

---

## DS-L · Component foundation — hand-rolled versus proven

**Check.** For overlays (modal, dialog, popover, dropdown, tooltip), toasts, and
charts: is the product using an established accessible primitive, or a
hand-rolled implementation? This determines what you find in D5 and D12 — the
accessibility plumbing (focus trap, scroll lock, portal, keyboard navigation,
ARIA) is where hand-rolled components reliably fail.

**Why it matters.** Almost every clipped-overlay, focus-trap, and
keyboard-navigation finding traces back to a hand-rolled dialog or menu. Naming
the root cause once is more useful than reporting eight symptoms.

**Three cases, three recommendations:**
- **An established library is in use** (Radix, shadcn/ui, MUI, Chakra, Mantine,
  Recharts, a native platform component) → match it. **Do not recommend
  migrating** an established library as an audit outcome; that's a project, not
  a finding. Report the specific gaps instead.
- **Hand-rolled with no library behind it** → the individual accessibility and
  behaviour failures are real findings, and "move to a proven primitive" is a
  legitimate recommendation — framed as the cheaper route to fixing them all,
  with the effort stated honestly.
- **Nothing wired at all** (no toast system, logos never loaded, no chart
  tooltip) → that's broken rather than inconsistent; it's a plain defect.

Where a remediation proposal needs a concrete suggestion for a React/Next
codebase, shadcn/ui over Radix is a reasonable default — it copies source into
the repo rather than adding a runtime dependency, so it can be styled with the
product's existing tokens. Offer it; don't impose it, and never propose it for a
React Native codebase or one already on another established library.

---

## DS-M · Breakpoints

**Check.** Are breakpoints defined once, or duplicated as magic numbers across
components? Do the values match between CSS, JS, and the design file? Are there
more breakpoints than the layout actually needs?

**Fails like.** `768px` hard-coded in six files; a JS media query at 767 and a
CSS one at 768, producing a one-pixel dead zone; a design file built at two
widths while the code has five breakpoints; components with their own private
breakpoints.

**Fix.** One source of truth, referenced everywhere. Reference frames of desktop
1440 and mobile 375 are a common convention; the values matter less than there
being one set.

---

## DS-N · Design-to-build drift

**Check.** Only when you have both Figma and code. Do the token values match?
Do component names correspond? Does a variant exist in one and not the other?
Are there states in the design that the code has no branch for, or code states
the design never covered?

**Why it matters.** Drift between design and build is a process finding as much
as a product one, and it's invisible from either side alone — which makes it
uniquely valuable output from an audit that has both.

**Fails like.** Spacing scale differing between Figma variables and the Tailwind
theme; a component with five variants in Figma and three in code; colours
renamed in one place only; the design file two redesigns behind the product.

**Fix.** Report the specific mismatches with both locations. Where the design
file is simply stale, say so — the recommendation is about which is the source
of truth, not about fixing every difference.

**Judge each mismatch on merit; the design file is not automatically the
authority.** The reflex is that code drifted and code is wrong. Often it's the
reverse: a real audit found a navbar control at 46px in code against 54px in
Figma, and the code was the better artefact — 46px clears the 44px touch
minimum, the Figma's 42px mobile variant does not. Another mismatch traced to
the design file being one commit behind a change the code had already shipped.

So for each difference, say **which side you'd keep and why**, in user terms.
And where the pattern across the file is that code leads and Figma trails, the
finding is not "reconcile these values" — it is **"decide which one is the
source of truth"**, which is a process decision the team has to make once and
which costs far less than a tokenization project. Two questions usually gate the
recommendation and are worth asking rather than assuming: is the design file
still maintained, and is the thing you're flagging a deliberate house style?

---

## How to report drift

Drift findings are weak one at a time and strong in aggregate. Deliver them as
**one consolidated inventory per category**, not forty individual findings:

```
DS-03 · Colour drift — 34 raw hex values alongside a 12-token palette   Medium · S
  #3B82F6  ×11  Button.tsx, Link.tsx, Badge.tsx …   → color/brand/primary
  #6B7280  ×8   6 files                             → text/secondary
  #E5E7EB  ×7   4 files                             → border/subtle
  … 9 more values ×1–2, listed in appendix
  Why: no single place to change secondary text or borders; dark mode is
  manual per component as a result.
  Fix: map to existing tokens (mechanical); the 9 singletons need a decision.
```

One finding, one severity, one effort, with the detail attached. That's usable;
forty `Low` findings are not.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Filled control whose best on-colour fails AA | **High** (also A11Y) |
| No semantic layer, so dark mode / theming is per-component | **High** if the product ships both modes; else **Medium** |
| Script/handwriting face used as UI or body text | **High** |
| Body text below 16px on mobile | **High** (also A11Y) |
| No design system at all in a product past a certain size | **High** — one structural finding, not many |
| Substantial colour or spacing drift against an existing system | **Medium** |
| Component drift — several implementations of one concept | **Medium** |
| Hand-rolled overlays causing the D5/D12 failures | **Medium** as a root cause; the symptoms carry their own severity |
| No tabular figures in a number-heavy product | **Medium** |
| Radius/border inconsistency | **Low**–**Medium** |
| Breakpoints duplicated as magic numbers | **Low** |
| Design/build drift on a stale design file | **Low** — process note |
| Which scale, which radius, which typeface | **Taste** — never a finding on its own |
