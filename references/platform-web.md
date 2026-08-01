# D13 · Platform conventions — web

> **When to read:** The product under audit is a marketing website, a web app,
> or a desktop app. Mobile-native and mobile-web divergences are in
> `platform-mobile.md` — a responsive web product needs both. Finding IDs:
> `PLAT-nn`.
>
> A convention is only worth flagging when breaking it **costs the user
> something**. "That's not how it's usually done" is not a finding.

## Table of contents
1. [PLAT-A · Which surface is this?](#plat-a--which-surface-is-this)
2. [PLAT-B · Responsive behaviour](#plat-b--responsive-behaviour)
3. [PLAT-C · Pointer, hover, and the touch-capable desktop](#plat-c--pointer-hover-and-the-touch-capable-desktop)
4. [PLAT-D · Browser conventions](#plat-d--browser-conventions)
5. [PLAT-E · Keyboard conventions](#plat-e--keyboard-conventions)
6. [PLAT-F · Cross-browser and cross-OS](#plat-f--cross-browser-and-cross-os)
7. [PLAT-G · Marketing sites — the job](#plat-g--marketing-sites--the-job)
8. [PLAT-H · Marketing sites — hero](#plat-h--marketing-sites--hero)
9. [PLAT-I · Marketing sites — section structure](#plat-i--marketing-sites--section-structure)
10. [PLAT-J · Marketing sites — motion and header behaviour](#plat-j--marketing-sites--motion-and-header-behaviour)
11. [PLAT-K · Brand assets — favicon, logo, store badges](#plat-k--brand-assets--favicon-logo-store-badges)
12. [PLAT-L · Brand coherence between site and product](#plat-l--brand-coherence-between-site-and-product)
13. [PLAT-M · Desktop applications](#plat-m--desktop-applications)
14. [Severity calibration](#severity-calibration-for-this-file)

---

## PLAT-A · Which surface is this?

**Check.** Establish it before applying any rule below, because the three have
genuinely different jobs and most of the criteria don't transfer:

| Surface | Job | Judge by |
|---|---|---|
| **Marketing website** | Communicate value, hand off to the product | Comprehension speed, conversion path, trust signals. Not feature density. |
| **Web app** | Be the product in a browser | Task efficiency, density, keyboard, state coverage. Not expressiveness. |
| **Desktop app** (Electron, native) | Be the product with OS integration | Everything web-app plus OS conventions (PLAT-M). |

A repo often holds several. Audit the one you were asked about; note the others
only where the brand-coherence check (PLAT-L) applies.

**Fails like.** Marketing chrome inside the authenticated product (a mega-footer
on every app screen, a marketing header reused as the app shell); a product
screen's density applied to a landing page; a marketing site trying to behave
like the app.

---

## PLAT-B · Responsive behaviour

**Check.** Resize continuously from the widest supported width to 320px. Don't
just check the design breakpoints — the failures live between them. At each
notable width: does content reflow to a usable layout, does anything overlap or
clip, does horizontal scroll appear, do touch targets remain adequate on
touch-capable devices?

**Why it matters.** The two-width design (desktop and phone) is the norm, and
the widths in between are where real users sit — laptops at 1280 and 1366,
tablets in both orientations, split-screen windows, and browsers with a sidebar
open.

**Fails like.**
- Horizontal scroll on the page body at any width.
- A fixed-width element (a table, a code block, an embed) forcing the whole page
  wide.
- Multi-column layouts that don't collapse, producing 90px columns.
- Content that disappears at narrow widths rather than reflowing — information
  loss, not adaptation.
- A sidebar that neither collapses nor scrolls, eating a laptop's width.
- Sticky headers and footers consuming most of a short viewport, especially at
  zoom.
- Modals wider than the viewport.
- Images without `max-width: 100%`.
- Layout that breaks with a browser sidebar or devtools open.

**Fix.** Name the width and the element. Fluid containers, `max-width: 100%` on
media, and a deliberate answer for wide fixed-width content (horizontal scroll
inside its own container, never on the body). Cross-reference `navigation-and-
ia.md` NAV-G for the nav's own transformation, and `accessibility.md` A11Y-M for
reflow at 400% zoom, which is the same problem measured differently.

---

## PLAT-C · Pointer, hover, and the touch-capable desktop

**Check.** Is any information or action available **only** on hover? Do
interactive elements have a resting affordance? Do hover-dependent patterns have
a touch path — remembering that laptops with touchscreens exist, so "desktop"
does not mean "has hover"?

**Fails like.**
- Row actions revealed only on hover — invisible and unreachable on touch.
- Tooltips carrying information needed to complete the task.
- A clickable card with no affordance until hovered.
- Hover-open menus with no click/tap alternative.
- Hover-only truncation reveal, so the full value is unreachable on touch.
- `:hover` styles applied on touch devices and sticking after a tap.
- A drag-only interaction with no alternative (also A11Y-C, A11Y-P).

**Fix.** Hover is an enhancement, never the only channel. Resting affordances
for anything interactive. Every hover-revealed action also reachable by focus
and by tap. Use `@media (hover: hover)` to scope hover styling rather than
assuming pointer type from viewport width.

---

## PLAT-D · Browser conventions

**Check.** Does the product respect what the browser provides? Back and forward,
bookmarkable URLs, refresh, open-in-new-tab, find-in-page, the browser's own
zoom and text settings, autofill and password managers, the print stylesheet
where printing is plausible.

**Why it matters.** These are the affordances users bring with them. Breaking
them costs nothing to fix and everything in the moment they fail.

**Fails like.**
- Browser Back exiting the app or losing a multi-step flow's state.
- Modal or drawer state absent from the URL, so Back closes the whole page.
- No URL representation for tabs, filters, sort, or pagination — nothing is
  shareable or bookmarkable.
- Refresh losing state, or resubmitting a form.
- Links implemented as JS click handlers, so cmd/ctrl-click and middle-click
  don't open a new tab.
- Custom scrolling that breaks find-in-page or the scrollbar.
- Blocking or hijacking browser zoom.
- `autocomplete="off"` on fields users want filled (also FORM-F).
- A right-click override with no benefit.
- Virtualized lists where find-in-page can't reach content — worth noting as a
  known tradeoff rather than a defect, but say it.

**Fix.** URL as state for anything shareable. Real `<a href>` for navigation.
Preserve state across refresh. Never block the browser's own capabilities.

---

## PLAT-E · Keyboard conventions

**Check.** Do standard shortcuts do standard things? `Escape` closes the topmost
layer; `Enter` submits from a single-line field; `Tab`/`Shift+Tab` move focus;
arrows navigate within composite widgets; `⌘/Ctrl+K` opens command or search
where one exists. Are custom shortcuts discoverable and non-conflicting?

**Fails like.**
- `Escape` doing nothing in a modal.
- `Enter` in a form field triggering the wrong control.
- Custom shortcuts overriding browser or OS ones (`⌘W`, `⌘T`, `⌘L`, `⌘F`).
- Single-character shortcuts that fire while typing in a field (also A11Y-C).
- Shortcuts with no discoverability — no help panel, no hints in menus.
- Shortcuts assuming a US keyboard layout, unreachable on others.
- No keyboard path at all in a product whose expert audience lives in it all
  day.

**Fix.** Standard keys do standard things. Custom shortcuts documented in a help
overlay and shown next to their menu items. Never override browser/OS
reservations. Weight this dimension by the audience call — an expert daily-use
product with no keyboard support is a real finding; a consumer site without a
command palette is not.

---

## PLAT-F · Cross-browser and cross-OS

**Check.** Where evidence allows: does the product work in Safari, Firefox, and
Chromium? Do form controls, date inputs, scrollbars, and fonts render
acceptably across OSes? Are there vendor-specific APIs with no fallback?

**Fails like.** Safari-specific layout breakage (a recurring flexbox/gap or
`dvh` difference); date and colour inputs rendering completely differently with
no accommodation; custom scrollbars that only style on WebKit; fonts falling
back to something illegible on one platform; a feature silently unavailable on
one browser with no message.

**Fix.** State which browsers you could actually check and which you couldn't —
cross-browser findings from a single browser are `Inferred` at best. Where a
capability genuinely isn't available, the requirement is a graceful message, not
silence.

---

## PLAT-G · Marketing sites — the job

**Check.** Within a few seconds, can a visitor say what this is, who it's for,
and what to do next? Is there one primary call to action? Is the trust evidence
real (verifiable metrics, named customers, audits, credentials) or vanity?

**Why it matters.** A marketing site's success is comprehension plus conversion.
Feature density is not the goal, and a beautiful site that doesn't say what the
product does has failed at its only job.

**Fails like.**
- A hero slogan that could describe any product in the category.
- No clear primary action, or five equally-weighted ones.
- Value proposition below the fold.
- Feature lists before the product has been explained.
- Unverifiable claims ("trusted by thousands") with nothing behind them.
- Logos of companies with no stated relationship.
- Contact and support routes absent or hidden.

**Fix.** Thesis, not slogan: what it does and for whom, in a line. One primary
CTA plus at most one secondary. Trust through specifics.

---

## PLAT-H · Marketing sites — hero

**Check.** Does the hero show the product, or a generic abstraction? Is the
layout chosen for this brief, or the default? Does the hero fill the viewport
with no cue that anything is below? Does any mockup stay inside its section at
every width?

**Why it matters.** The hero is the most valuable space on the site and the most
templated. A hero that's a stock illustration and a slogan spends that space on
nothing.

**Fails like.**
- A generic 3D orb, particle field, or abstract gradient blob instead of the
  product.
- A hero exactly `100vh` (rather than `100dvh`) on mobile, so browser chrome
  crops it.
- A full-height hero with no scroll cue, reading as the whole site.
- A short hero forced to full height, leaving a void.
- A mockup spilling into the next section at some breakpoint — a containment
  bug, not a design device, unless it holds at every width.
- The same two-column-split-with-tinted-panel layout used by default. **It's one
  option among many** — centred stack, inset canvas, typographic, tonal wash,
  full-bleed media, asymmetric offset. If you can't say why this brief got this
  layout, it was defaulted.
- An eyebrow pill above the H1 carrying no information (see `content-and-copy.md`,
  COPY-G).

**Fix.** Show the real product. Contain mockups at every breakpoint. Leave a
scroll cue. Grade layout choice as **Opportunity or Taste**, not a defect —
unless the hero measurably fails to communicate, which is PLAT-G.

---

## PLAT-I · Marketing sites — section structure

**Check.** Read the page as a sequence. Does it build an argument — what it is,
proof, how it works, why this one, evidence, act — or is it a stack of
undifferentiated bands? Do consecutive sections share a layout? Are sections
separated by spacing and background, or by horizontal rules?

**Fails like.**
- Left-title-plus-two-columns repeated six times; even with good content, the
  page reads as a template.
- No proof section — nothing that shows the product working.
- "How it works" that describes the mechanism rather than the outcome.
- A horizontal divider between every band, slicing the page into slices.
- A rule laid on top of a background change that already separates the sections —
  redundant.
- Every section centred, or every section left-aligned, with no variation in
  rhythm or density.

**Fix.** Vary layout by what each section contains, with **no more than two
consecutive sections sharing a layout**. Alternate density. Separate bands with
spacing and background change; a rule earns its keep only above the footer or
between rows of a dense comparison table.

---

## PLAT-J · Marketing sites — motion and header behaviour

**Check.** Does motion serve comprehension — revealing structure, demonstrating
the product — or is it ornament? Does it respect `prefers-reduced-motion`? Does
it jank the first paint or the scroll? Does the header behave sensibly on
scroll?

**Fails like.**
- Floating particles, glowing orbs, laser lines, endless gradient shimmer.
- Scroll-jacking that overrides the user's scroll speed or position.
- Animations firing on every scroll pass, so scrolling back up replays
  everything.
- Motion that delays content appearing.
- No reduced-motion path (also A11Y-L).
- A header that scrolls away and never returns, so the CTA is unreachable
  without scrolling to the top.
- A heavy blurred-glass header slab over content, hurting legibility.
- A completely static page, which reads as unfinished on a marketing site.

**Fix.** Motion that explains. Reduced-motion fallback. A header that either
stays (ideally condensing on scroll past the fold) or returns on scroll up.
Keep the primary CTA reachable at every scroll position and width.

---

## PLAT-K · Brand assets — favicon, logo, store badges

**Check.** Is there a favicon, and is it derived from the same mark as the logo?
Is it legible at 16px? Are `apple-touch-icon` and the PWA icon set present? Are
any app-store badges official assets used per their rules?

**Why it matters.** A logo in the header next to a default browser-globe tab
icon reads as unfinished, and it's an entirely avoidable S-effort fix. It
applies to the web app as much as the marketing site.

**Fails like.**
- No favicon, or the framework's default.
- A full wordmark shrunk to 16px, illegible.
- Favicon differing from the product's mark.
- No `apple-touch-icon`, so a home-screen bookmark shows a screenshot.
- No dark-variant handling where the browser supports it.
- App-store badges recoloured, redrawn, rotated, animated, or translated —
  these are governed brand assets with strict rules, and an approximation is
  both wrong and off-brand.
- A "Download on the App Store" badge fetched from a CDN — **none of the store
  publishers offers a runtime asset endpoint.** They're static assets to bundle
  and theme-swap. Apple provides black and white variants; Google Play ships one
  canonical full-colour badge (the monochrome one was discontinued), so a
  fabricated light/dark pair for it is wrong.

**Fix.** Generate the favicon from the same mark, simplified for 16px — use the
symbol, not the wordmark. Ship SVG plus PNG fallbacks and an `apple-touch-icon`.
Bundle official store badges as local assets and verify the current rules at the
publisher's own brand page when placing them.

---

## PLAT-L · Brand coherence between site and product

**Check.** Moving from the marketing site into the product: same palette, same
typography, same logo, same favicon, same voice? Does the transition feel like
one company?

**Why it matters.** The moment after "Get started" is where a visitor becomes a
user, and a jarring visual discontinuity there reads as a bait-and-switch even
when it isn't.

**Fails like.** Different brand colours between site and app; a site refreshed
and the app left behind; different logo versions; a different favicon in each; a
warm marketing voice against a cold system voice inside.

**Fix.** Name the specific divergences. The site can legitimately push
personality further than the product — expressive type, more motion — while the
product pulls back to utility. They should rhyme, not match exactly. Where the
finding is that one is stale, say which and recommend a direction rather than
restyling both.

---

## PLAT-M · Desktop applications

**Check.** Only where the product is a real desktop app (Electron, Tauri,
native). Does it behave like a desktop application, or like a website in a
window?

**Fails like.**
- No native menu bar, or one that omits the platform's expected items.
- Platform shortcuts unimplemented (`⌘,` for preferences on macOS, `Ctrl+,` on
  Windows/Linux; `⌘Q`, `Alt+F4`).
- No multi-window support where the workflow implies it.
- Window state (size, position) not persisted.
- Ignoring the OS theme, accent colour, or reduced-motion setting.
- No offline capability in an app whose whole premise was being an app.
- Web-style scrollbars, tooltips, and context menus where native ones are
  expected.
- No auto-update, or an update flow that interrupts work.
- Missing OS integrations the workflow implies: notifications, file
  associations, drag-and-drop from the file system, deep links.
- Traffic-light or window-control placement wrong for the platform.

**Fix.** Name the platform conventions being broken and the cost of each. Grade
by whether users will notice: a missing preferences shortcut is Low; no offline
support in a desktop app sold on offline is a Blocker.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Product unusable at a common viewport width | **Blocker** |
| Browser Back destroys work or exits mid-flow | **Blocker** |
| A task achievable only on hover, on a touch-capable device | **Blocker** if it blocks the task, else **High** |
| Content lost rather than reflowed at narrow widths | **High** |
| Horizontal scroll on the page body | **High** |
| No URL state for filters, tabs, or pagination in a product people share links from | **High** |
| Refresh loses state or resubmits | **High** |
| Escape doesn't close overlays; shortcuts override browser reservations | **Medium** |
| Links as JS handlers, breaking new-tab | **Medium** |
| Missing or default favicon alongside a logo | **Medium** — S effort |
| Marketing site whose value proposition isn't legible in seconds | **High** |
| Header scrolls away, CTA unreachable | **Medium** |
| Repeated section layout, dividers between every band | **Low**–**Medium** |
| Hero layout choice, motion style | **Taste** — label it |
| Desktop app missing platform shortcuts | **Low**–**Medium** by frequency of use |
