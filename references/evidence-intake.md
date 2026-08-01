# Evidence Intake

> **When to read:** At the start of every audit, before the first finding. This
> file is how you turn "here's our app" into a record of what you actually
> observed. SKILL.md §1 states the rules; this file is the procedure and the
> failure modes of each source.

## Table of contents
1. [The evidence log](#the-evidence-log)
2. [Source 1 — live product](#source-1--live-product)
3. [Source 2 — design files (Figma via MCP)](#source-2--design-files-figma-via-mcp)
4. [Source 3 — screenshots & recordings](#source-3--screenshots--recordings)
5. [Source 4 — source code](#source-4--source-code)
6. [Source 5 — verbal description](#source-5--verbal-description-only)
7. [Mixing sources](#mixing-sources)
8. [When there is nothing usable](#when-there-is-nothing-usable)
9. [Do / Don't](#do--dont)

---

## The evidence log

Keep a running list as you go. It costs nothing and it is what makes §Scope of
the report honest:

```
SEEN
  /checkout/cart          live, Chrome 1440×900, logged in, 2 items    2026-08-01
  /checkout/payment       live, same session — card form only, saved-card path untried
  CartRow.tsx:12-88       code
  Figma 214:3901          "Checkout / empty" frame

NOT SEEN
  /checkout/confirmation  couldn't reach — needs a real payment
  mobile viewport         no device access, no responsive screenshots provided
  error states            not reproducible without a failing backend
```

Two rules make it useful:
- **Record the conditions**, not just the URL. Viewport, auth state, data state,
  locale. A screen with three rows and a screen with three hundred are different
  screens, and most state-coverage findings live in that gap.
- **Write the NOT SEEN column as you discover it**, not at the end. It becomes
  §1 "what was not audited" verbatim, and it's the section people skip when
  they reconstruct it from memory.

---

## Source 1 — live product

The strongest evidence. A finding from a running product can be `Observed` at
full confidence, and it's the only source that shows timing, focus order, and
real error behavior.

**Drive it deliberately, not just look at it.** A pass that only loads pages
misses most of the spine:

| Do this | Reveals |
|---|---|
| Complete the core task end to end, counting steps and fields | D1, D3, D4 |
| Complete it **again**, on the return-visit path | D1 (does onboarding repeat?), D7 (first-use vs power-use) |
| Tab through every interactive element from the top | D12 focus order, focus visibility, keyboard traps |
| Submit every form empty, then with one bad field | D4 validation timing, D6 recovery, D8 error copy |
| Trigger the destructive action and stop at the confirmation | D6 guards, D15 irreversibility |
| Throttle the network, then go offline mid-task | D5 loading, D7 offline, D14 perceived performance |
| Resize from widest to 320px, or open the responsive emulator | D13 |
| Empty the data (new account, cleared filters, search with no results) | D7 empty states |
| Overflow the data (long name, 200 rows, huge number, long translation) | D7 overflow, D11 truncation |
| Zoom the browser to 200% and set the OS font size large | D12 reflow, D13 |
| Toggle OS dark mode and `prefers-reduced-motion` | D9, D12 |

**Recording the evidence:** quote exact labels and error strings. Note the URL
and the state. When something is timing-dependent ("the spinner runs ~4s with no
message"), say roughly how long and on what connection.

**Limitations to state honestly:** you are one user on one device with one data
set. You cannot see: real drop-off rates, whether *your* confusion generalizes,
performance on the devices their users actually own, or anything behind a
paywall, a real payment, or a role you don't have. Those become **Open
questions**, not findings.

---

## Source 2 — design files (Figma via MCP)

Second-strongest, with one structural caveat: **a design file shows intent, not
what shipped.** A finding sourced only from Figma is `Observed` about the design
and `Inferred` about the product. Say which you mean.

### The four tools and what each is for

| Tool | Returns | Audit use |
|---|---|---|
| `get_screenshot` | A rendered image of a node | Visual hierarchy, layout, density, scan path, contrast candidates (D9, D12) |
| `get_variable_defs` | The variables/tokens bound in the selection | **The single best design-system-drift signal** (D10) — what's a token vs a raw value |
| `get_design_context` | Structured description of a node: layers, text, layout, styles | Copy verbatim, spacing values, component names, hierarchy (D8, D9, D10) |
| `get_metadata` | The node tree — names, types, ids, sizes | Mapping the file, finding the frames worth reading, resolving `nodeId`s |

**Order that works:** `get_metadata` on the file or page to see what exists →
pick the frames that match the audit scope → `get_screenshot` for the visual
read → `get_design_context` on the specific node for exact copy and values →
`get_variable_defs` on the same node for token adherence.

### Known limitations — plan around these, don't fight them

- **Screenshot reliability degrades over a long session.** Base64 image returns
  get less reliable the longer the conversation runs. When a screenshot comes
  back empty, truncated, or malformed, **do not retry it three times** — fall
  back to `get_design_context` with a **specific `nodeId`**, which returns the
  structure as text and stays reliable. You lose the visual read; you keep the
  copy, the spacing, and the token bindings.
- **Always pass a specific `nodeId` once you have one.** Whole-file or
  whole-page calls return too much, cost a lot, and are the calls most likely to
  fail. `get_metadata` first exists to get you that id.
- **Figma CDN assets are not fetchable with `curl`.** Image fills and exported
  asset URLs from a Figma file are signed and short-lived — a shell fetch gets a
  403 or an empty body. Use the MCP tools' own output; don't build a workflow
  that shells out for images.
- **A design file is not a state inventory.** Most Figma files contain the happy
  path and, if you're lucky, an empty state. Absence of an error frame in Figma
  is **not** evidence that the product lacks an error state — it's a question for
  the team. This is the single most common way a Figma-only audit produces false
  findings.
- **Naming ≠ implementation.** A layer named `Button/Primary` may or may not be
  the shipped component. Component *drift* findings need either the code or the
  live product to confirm.
- **Interactions and prototype flows are partial.** Step order from a prototype
  is `Inferred` unless the user confirms it matches the build.

### What Figma is uniquely good for

Design-system consistency (D10). `get_variable_defs` across several frames tells
you immediately whether spacing, color, and type are bound to variables or typed
in by hand — and a raw `#3B82F6` sitting next to `color/brand/primary` in the
same frame is a token-drift finding with an exact location.

---

## Source 3 — screenshots & recordings

Reliable for exactly what's in frame, and nothing else.

- **Read what's actually there.** Quote the labels. Note the viewport if it's
  inferable (browser chrome, device frame). Note the data state.
- **Never extrapolate past the crop.** "The nav presumably continues below" is
  not evidence. If the screenshot cuts off, the finding is scoped to what's
  visible or it's a question.
- **A recording is stronger than a screenshot** because it carries timing and
  sequence: how long the spinner ran, whether the layout shifted after load,
  what the user had to do twice. Watch for those specifically — they're D5, D14,
  and D3 evidence you cannot get from stills.
- **Ask for the states you're missing.** One round: "Can you send the empty
  state, the error state, and the mobile width for this screen?" is a far better
  use of a question than guessing.
- Screenshots are usually the *happy path with good data*. Assume state coverage
  is unaudited until you see otherwise, and say so.

---

## Source 4 — source code

Excellent for structure, tokens, semantics, and what states *exist*. Weak for
what any of it looks like or feels like.

### The read-before-you-judge inventory

Find these before writing findings. They are the system the product actually
has, and D10 is graded against *it*, not against any ideal:

| What | Where to look | Feeds |
|---|---|---|
| **Design tokens** | `tailwind.config.*` (`theme.extend`), CSS custom properties in `globals.css`/`:root`, a `tokens.*`/`theme.*` file, a Figma-exported JSON | D10 |
| **Styling approach** | Tailwind · CSS Modules · styled-components/emotion · vanilla-extract · plain CSS. More than one in active use is itself a finding | D10 |
| **Component library** | shadcn/ui (`components/ui/` + `components.json`), Radix, MUI, Chakra, Mantine — or bespoke/hand-rolled with no library behind it | D10, D12 |
| **Icon set** | A real library (`lucide-react`, `@phosphor-icons/*`, `react-icons`) vs hand-drawn inline `<svg>` with inconsistent stroke and size | D10 |
| **Charts / data-viz** | Recharts, visx, Chart.js, D3, tremor — or hand-coded SVG/canvas/divs | D11 |
| **Fonts** | `next/font`, `@font-face`, a Google Fonts link; whether `tabular-nums` appears anywhere | D10, D11 |
| **Motion** | framer-motion/`motion`, react-spring, Reanimated, or CSS transitions — and whether `prefers-reduced-motion` is handled anywhere | D12 |
| **Dark/light** | `next-themes`, a `data-theme`/`.dark` strategy, or none | D9, D12 |
| **Routes** | The route tree / navigator config — the IA as built | D2 |
| **Copy strings** | i18n files, or strings inline in components | D8 |
| **A11y attributes** | `aria-*`, `role`, `alt`, `<label>` association, focus management, `tabIndex` | D12 |
| **State branches** | Does each async view have `isLoading` / `isError` / empty branches, or only the success render? | D7 |

**Then read two or three neighbouring components.** They teach the local dialect
— naming, variant expression, how much abstraction the team tolerates — and that
dialect is the baseline for every consistency judgment you make.

### What code evidence can and cannot support

- **Can, at `Observed`:** a missing `alt`, a `<div onClick>` with no role or key
  handler, a hard-coded `#3B82F6` where tokens exist, an async view with no
  error branch, a form with no `<label>`, a `100vh` on a mobile layout.
- **Only `Inferred`:** anything about rendered appearance, contrast (computed
  colors may cascade), focus visibility (a global reset may kill it or a `:focus-
  visible` rule may restore it), perceived performance, whether the empty state
  a branch renders is any good.
- **Never:** "users are confused by this" from code alone.

Cite `file.tsx:42`. A code finding without a line number is half a finding.

---

## Source 5 — verbal description only

The weakest input, and the one most likely to produce a confident-sounding
audit about a product that doesn't exist.

- **Everything is `Hypothesis`.** No exceptions, no "well, they clearly meant".
- **Phrase findings as questions**, and put them in the report's §6 Open
  questions, not in the findings tables: "If the confirmation step shows only
  the total and not the line items, users can't catch a wrong quantity before
  paying — does it show line items?"
- **Say it once, at the top**, plainly: this is a review of a described product,
  the findings are hypotheses, and they need ten minutes with the real thing to
  become findings.
- **Push once for anything better.** A single screenshot moves more findings to
  `Observed` than an hour of reasoning from a description.

A verbal-only audit is legitimate work — it can surface the right questions and
the known-risky patterns. It is not legitimate to present it as an audit of what
shipped.

---

## Mixing sources

Common and good: code plus a live URL, or Figma plus screenshots.

- **Confidence is per finding, from the evidence behind *that* finding** — not a
  session-wide setting. A code-derived missing-`alt` is `Observed` in the same
  report where a flow-order claim is `Inferred`.
- **When sources disagree, that is itself a finding.** Figma shows an error
  state the code has no branch for; the design system defines four text tokens
  and the code uses eleven greys. Design/build drift is a real D10 defect —
  report it as one, with both locations.
- **Prefer the live product for anything about behavior**, the code for anything
  about semantics and tokens, Figma for anything about intent.

---

## When there is nothing usable

Ask, **once**, for the minimum that unblocks a real audit — and make the ask
specific enough to be answerable in one message:

> To audit this properly I need three things:
> 1. **Scope** — the whole product, one flow, or one screen? Any dimension you
>    especially care about (accessibility, conversion, consistency)?
> 2. **Access** — a URL I can browse, a Figma link, screenshots of the key
>    screens, or the repo path. Any one of these works; more is better.
> 3. **Audience** — who uses this, and are they expert users of the domain or
>    the general public?
>
> If you can also send the empty, error, and mobile states of the main screen,
> that covers most of what usually goes unchecked.

Then work with whatever comes back — including nothing, in which case run the
verbal-only path above and be explicit about it. **Do not ask a second round.**
An audit that arrives late because it interviewed the user three times has
already lost.

---

## Do / Don't

- DO keep a SEEN / NOT SEEN log from the first minute; it becomes §Scope.
- DO record conditions (viewport, auth, data state), not just page names.
- DO drive the product — tab through it, break it, empty it, overflow it —
  rather than only looking at it.
- DO run `get_metadata` first in Figma, then work from specific `nodeId`s.
- DO fall back to `get_design_context` with a `nodeId` when a screenshot returns
  empty; DON'T retry the screenshot repeatedly.
- DO treat a Figma file as intent, and say when a finding is about the design
  rather than the build.
- DO quote exact labels, error strings, and file:line.
- DO report design/build disagreement as a finding in its own right.
- DON'T fetch Figma CDN assets with curl — they're signed and short-lived.
- DON'T treat a missing frame in Figma as proof of a missing state.
- DON'T extrapolate past the edge of a screenshot.
- DON'T upgrade confidence because a finding feels obviously true.
- DON'T ask more than one round of intake questions.
