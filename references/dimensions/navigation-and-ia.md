# D2 · Information architecture & navigation

> **When to read:** Any audit that covers more than one screen. IA defects are
> the most expensive to fix and the least visible in a screen-by-screen review,
> so map the structure before grading the pixels. Finding IDs: `NAV-nn`.
>
> Platform conventions for the shell itself live in `platform-web.md` and
> `platform-mobile.md`; this file is the structure and the labels.

## Table of contents
1. [NAV-A · Map the IA first](#nav-a--map-the-ia-first)
2. [NAV-B · Findability](#nav-b--findability)
3. [NAV-C · Depth and breadth](#nav-c--depth-and-breadth)
4. [NAV-D · Labeling](#nav-d--labeling)
5. [NAV-E · Orientation — where am I?](#nav-e--orientation--where-am-i)
6. [NAV-F · The shell and what belongs in it](#nav-f--the-shell-and-what-belongs-in-it)
7. [NAV-G · Responsive transformation](#nav-g--responsive-transformation)
8. [NAV-H · Dead links and stub destinations](#nav-h--dead-links-and-stub-destinations)
9. [NAV-I · Search](#nav-i--search)
10. [NAV-J · Tabs and in-page section switching](#nav-j--tabs-and-in-page-section-switching)
11. [NAV-K · Footer](#nav-k--footer)
12. [Severity calibration](#severity-calibration-for-this-file)

---

## NAV-A · Map the IA first

**Check.** Write down the actual structure before judging it: the top-level
destinations, what's under each, how deep it goes, and what exists but isn't
reachable from the nav. On a codebase, read the route tree or navigator config —
that is the IA as built, and it is often wider than the nav suggests.

**Why it matters.** Nearly every real IA finding is comparative: this is two
clicks and that is five; these three items are siblings but behave like
parent-and-children; this route has no entry point. None of that is visible from
one screen.

**Fails like** (in the audit): findings about "confusing navigation" with no
structure behind them. **Fix:** produce the map. It goes in the report — it is
frequently the artifact teams find most useful, because many have never seen
their own IA written out.

Note anything you find in the routes that has **no navigational entry point at
all**. Orphan routes are usually either dead code or a feature nobody can find,
and both are worth reporting.

---

## NAV-B · Findability

**Check.** Pick the five things a user most needs to do. For each, count the
clicks/taps from a cold start and note whether the path is guessable — could a
first-time user find it without exploring, from the labels alone?

**Why it matters.** A feature that can't be found doesn't exist, and the team
usually can't see this because they know where everything is.

**Fails like.**
- A core action reachable only from a context menu or a hover-revealed control.
- A destination that exists in the product but appears in no navigation, only
  via a link inside a specific screen.
- Settings for a feature living somewhere other than the feature.
- Two paths to the same thing with different names, so the user can't tell if
  they're the same.
- The primary action of a screen hidden inside an overflow menu.
- On mobile, essential destinations buried in a hamburger when a bottom bar or a
  primary action would fit.

**Fix.** Name the specific item, its current path, and the proposed path. Where
something is genuinely secondary, say so — not everything belongs in primary
nav, and a bloated nav is its own defect (NAV-C).

---

## NAV-C · Depth and breadth

**Check.** How many levels deep does the structure go, and how wide is each
level? Rough working range: **4–7 primary destinations** on web, **3–5** in a
mobile bottom bar, and **no more than two or three levels** before the user is
navigating a filesystem. Count how many taps from home to the deepest routine
task.

**Why it matters.** Too wide and nothing is scannable; too deep and everything
requires memory of where it lives. Both push users onto search, and search is a
worse experience than a structure that fits.

**Fails like.**
- Nine top-level nav items, several of which are the same category split.
- A bottom tab bar with six or seven tabs, so labels truncate.
- Four levels of nesting to reach a routine setting.
- A "More" tab that contains most of the product.
- One nav item that opens a page which is only a menu of more nav items.
- Categories with one child each.

**Fix.** Propose a specific regrouping, not "simplify the nav". Say which items
merge, which demote to a secondary slot, and which become a filter or a tab
inside a sibling. Where the product genuinely has many destinations (an admin
console, an ERP), the fix is usually grouping with section labels plus search,
not fewer destinations.

---

## NAV-D · Labeling

**Check.** Read every nav label cold. Does it name a thing the user wants, in
their vocabulary, at the audience's level? Are the labels **parallel** (all
nouns, or all verbs — not a mix)? Do the same concepts use the same word
everywhere, including in the page title the link leads to?

**Why it matters.** A label is the only information the user has before
clicking. A wrong or internal label costs a round trip every time, forever.

**Fails like.**
- Internal or org-chart names: "Platform", "Console", "Hub", "Workspace 2.0",
  team names as section names.
- Invented brand words for standard concepts ("Nexus" for search).
- Mixed grammar: `Dashboard · Reports · Create new · Settings`.
- The nav says "Analytics", the page title says "Insights", the docs say
  "Reporting".
- Vague catch-alls: "More", "Other", "Tools", "General" — each hiding unrelated
  things.
- Jargon above the audience's level (mainstream product using "Entities",
  "Objects", "Resources").
- Labels so long they truncate at the default width.

**Fix.** Propose the replacement label verbatim. Where a rename ripples (docs,
support articles, URLs), say so — that's the constraint, and it changes the
effort estimate, not the correctness of the finding.

---

## NAV-E · Orientation — where am I?

**Check.** On every screen: is the current location marked in the navigation? Is
there a title that matches what the user clicked? For nested content, is there a
breadcrumb or a labeled back affordance? Does the browser tab title / document
title reflect the page?

**Why it matters.** Orientation is what lets a user build a mental model instead
of navigating by trial. Without it, every visit is a first visit.

**Fails like.**
- No active state on the nav item for the current page.
- Active state indicated by color alone, at low contrast (also a D12 failure).
- A back arrow that goes to a fixed screen rather than where the user came from.
- Deep content with no breadcrumb and a generic title.
- Every browser tab reading the product name with no page name.
- A modal or drawer that changes context with no title saying what it is.
- After a filter or a search, no indication of what's currently applied.

**Fix.** Active state on the current destination, using position/weight/fill and
not color alone. Page title matching the nav label that led there. Breadcrumbs
past two levels. Document title as `Page · Product`. Persist and display active
filters as removable chips.

---

## NAV-F · The shell and what belongs in it

**Check.** Is the shell (sidebar/top bar/tab bar) consistent across routes, or
does it change shape between screens? Does the primary nav hold **destinations**
only, with utilities (settings, help, theme, account, status) in secondary
slots? Does shell state — auth, selected workspace, notifications — survive
navigation?

**Why it matters.** The shell is the one constant. When it moves or re-renders
between routes, the product feels like several products stitched together, and
users lose the one thing they'd learned.

**Fails like.**
- Sidebar present on some routes, absent on others, with no reason.
- Nav flashing or re-mounting on every route change.
- Settings, Help, Docs, Support, Theme all in the primary nav alongside real
  destinations.
- A logo that isn't a link home, or links to the marketing site from inside the
  product.
- The account control in a different corner on different screens.
- Marketing header reused as the app header, or vice versa — two different
  components doing different jobs.
- Full-bleed content where a readable max-width is needed, or a cramped
  max-width on a deliberately dense data screen.

**Fix.** One shell, persistent, with destinations in primary and utilities in an
account menu or a sidebar footer. Name the specific items to move.

---

## NAV-G · Responsive transformation

**Check.** At each breakpoint, what does each destination become? The
transformation should be deliberate — **visible → icon-only → drawer item →
bottom tab** — not an arbitrary reflow. Resize continuously and watch for the
widths where the nav is broken rather than merely different.

**Why it matters.** A nav that only works at the designer's two widths strands
everyone on a laptop at 1180px or a phone in landscape.

**Fails like.**
- Nav items wrapping to a second line and overlapping content.
- Icon-only collapse with no tooltip and no label, so nothing is identifiable.
- A hamburger appearing at desktop widths where the full nav would fit.
- Bottom tab labels truncating to ellipses.
- A drawer that opens under the header, or one that can't be closed.
- Horizontal scroll introduced by the nav at a common width.
- The active-state indicator disappearing in the collapsed form.

**Fix.** Specify the form at each breakpoint per destination. Icon-only requires
an accessible name and a tooltip. Test 320px, 375px, 768px, 1024px, 1280px, and
the awkward widths in between.

---

## NAV-H · Dead links and stub destinations

**Check.** Click every link in the nav, the footer, and the account menu. Does
each go somewhere real? Any 404s, any anchors to sections that don't exist, any
`href="#"`, any "coming soon" pages presented as live destinations?

**Why it matters.** A dead link is a small, unambiguous signal that nobody
checked — and it's the kind of defect users generalize from. On any product
handling money, identity, or health data, it directly costs trust.

**Fails like.**
- A footer of `Docs · Careers · Blog · Terms · Privacy` where half 404.
- Links to a status page or changelog that was never built.
- Social icons linking to accounts that don't exist or are empty.
- In-app help links to a docs site with no matching article.
- Anchor links pointing at ids that aren't on the page.
- Legal pages (Terms, Privacy) missing entirely on a product that collects
  personal data — that's a D15 finding too, and a serious one.

**Fix.** Only link what exists. For expected-but-unbuilt items: omit them, or
render them as non-interactive placeholder text clearly marked as a stub — never
a live link into the void. List every stub explicitly in the report so the team
can decide to build or remove. "Fine at this stage" is not a defense: a
placeholder that isn't clickable is honest; a link that 404s is a shipped bug.

---

## NAV-I · Search

**Check.** If the product has search: what does it search over? Does it tolerate
typos, partial words, and synonyms? Are results ranked usefully or by database
order? Is there a zero-results state with a way forward? Is search a substitute
for a broken IA?

**Why it matters.** Search is the recovery mechanism for everything navigation
fails to expose. When it's also poor, there is no recovery.

**Fails like.**
- Exact-substring matching only, so one typo returns nothing.
- Zero results with no suggestions, no "clear filters", no fallback.
- Results with no context — bare titles, no type, no location, no snippet.
- Search that silently applies a scope the user can't see or change.
- No keyboard access (no `/` or `⌘K`) in a product where power users live.
- Search present *because* the IA is unnavigable, and doing all the work.

**Fix.** Tolerant matching, meaningful ranking, results that say what and where
each thing is, and a zero-results state that offers the nearest useful action.
If search is carrying the IA, say that plainly — it's an IA finding wearing a
search costume.

---

## NAV-J · Tabs and in-page section switching

**Check.** Tabs are in-content section switching, not app navigation. Is the
selected tab unmistakable? Does tab state survive a reload or a deep link? Is
there exactly one tab style in the product, used consistently?

**Why it matters.** Tabs that look like navigation, or navigation that looks
like tabs, teaches the user a model that then fails.

**Fails like.**
- Selected tab distinguished only by a subtle color shift.
- Tab state lost on reload; no URL representation, so a tab can't be shared.
- Three different tab styles (underline, pill, segmented) in one product with no
  rule.
- Scrolling tab strips with more items than fit, hiding the ones on the right.
- Tabs used for a sequential flow, where steps should be.
- Tabs not reachable or operable by keyboard.

**Fix.** One tab style per role, chosen deliberately: underline for content
sections, segmented for view toggles. Selected state carried by more than color.
Reflect the tab in the URL. Keyboard support per the WAI-ARIA tabs pattern
(`accessibility.md`).

---

## NAV-K · Footer

**Check.** In-product: is the footer minimal (or absent), rather than a marketing
mega-footer dropped inside the app? On a marketing site: does the footer carry
the real secondary IA — nav columns, legal, status, contact — and does all of it
resolve (NAV-H)?

**Why it matters.** A mega-footer inside a product is dead weight on every
screen; a thin footer on a marketing site drops the secondary IA that search and
scanning both rely on.

**Fails like.** A full marketing footer inside the authenticated app; a
marketing site with no footer nav and no legal links; legal links present but
404 (see NAV-H); a footer that's the only place a critical destination appears.

**Fix.** App footer: nothing, or a thin bar with version, status, and a docs
link. Marketing footer: complete, grouped, and fully live.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| A core destination is unreachable by any navigation | **Blocker** |
| Nav unusable at a common breakpoint (overlap, no close, horizontal scroll) | **Blocker** if it blocks the task, else **High** |
| A core task is not findable without prior knowledge | **High** |
| No orientation at all — no active state, no titles, no breadcrumbs | **High** |
| Labels that misdescribe their destination on a core path | **High** |
| Dead links in footer or nav | **Medium** (**High** on a trust-sensitive product; **High** if legal pages are missing) |
| Structure too deep or too wide, workable but costly | **Medium** |
| Search intolerant of typos, poor zero-results state | **Medium** |
| Inconsistent tab styles, non-parallel label grammar | **Low** |
| Footer composition, nav ordering preferences | **Low** — often taste; label it |
