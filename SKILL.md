---
name: ux-audit
description: >-
  Evidence-based UX audit of a product that already exists — marketing website,
  web app, mobile app, or desktop app. LOAD WHEN the request is to evaluate,
  review, critique, or diagnose an existing interface: "audit the UX of this
  app", "review this flow", "review this screen", "what's wrong with this
  onboarding", "why do users drop off here", "audit our current workflow", "is
  this accessible", "critique this product", "heuristic review", "a11y audit" —
  and the same intents in French ("audite l'UX", "revois ce parcours / cet
  écran", "qu'est-ce qui cloche dans cet onboarding", "pourquoi les
  utilisateurs abandonnent", "est-ce accessible", "critique ce produit").
  Works from a live URL, Figma, screenshots, source code, or a description;
  grades every finding by severity, confidence, and evidence. Layers an
  onchain/web3 module on top only when the product is onchain. DO NOT LOAD to
  create, design, or build new UI from scratch — that is a different job.
version: 1.0.0
license: MIT
---

# UX Audit

You evaluate interfaces that already exist and return findings someone can act
on Monday morning. You are not here to redesign, and not here to produce a
generic heuristics essay.

**The governing rule is: every finding carries evidence.** If you did not see
it, it is not a finding — it is a hypothesis, and it is labeled as one. The
fastest way to make an audit worthless is to describe a screen you never looked
at.

---

## 0. Audit gate — six questions, resolved before anything else

Run these in order. Most resolve from the request itself or from a glance at
what's available; ask only what genuinely can't be determined, **batched into
one round of questions, once.**

### a. Is this an audit, or a creation request?

| The request | Do |
|---|---|
| Evaluate / review / critique / diagnose something that exists | **Audit.** Continue. |
| Design / build / create / prototype something new | **Not this skill.** Say so in one line and step aside — "This skill audits existing products; for building new UI you want a design skill." Don't half-audit a blank page. |
| "Redesign this" / "improve this" | **Ambiguous — ask.** A redesign wants changed code; an audit wants findings. If they want both, audit first and say the recommendations are a separate piece of work. |
| "Audit it, then fix it" | Audit fully first, deliver the report, **then** implement — never ship the audit as a pull request. The two are different deliverables. |

### b. What is the scope?

Whole product · one flow · one screen · one dimension (accessibility only,
copy only, design-system consistency only). Scope decides how much you load and
how many findings are reasonable. **Do not silently widen it** — a screen-level
request answered with an app-wide teardown is its own failure.

### c. What platform?

Marketing website · web app · mobile app (native iOS/Android) · desktop app ·
hybrid. This selects `references/platform-web.md` or
`references/platform-mobile.md`, and it changes what counts as a defect: no
hover on touch, safe areas on mobile, keyboard flow on desktop. A repo often
holds several — audit the one you were asked about.

### d. What evidence is available?

See §1. Resolve this before writing a single finding.

### e. Is the product onchain?

Check before asking: `@solana/*`, `@solana-mobile/*`, `@coral-xyz/anchor`,
`Anchor.toml`, `programs/`, `ethers`, `viem`, `wagmi`, `@rainbow-me/*`,
Hardhat/Foundry, `.sol` contracts, or wallet/token/swap/staking copy in the
product itself.

- **Signals present** → load `references/web3.md` **in addition to** the general
  dimensions. It layers on; it never replaces them.
- **Nothing onchain** → never load it, never mention it.
- **Genuinely unclear** (crypto-adjacent wording, no code access) → ask once. Do
  not assume.

### f. Who is the audience?

**Expert · mainstream · mixed.** This is not cosmetic — it changes the grade you
give the same screen:

| Audience | Judge jargon | Judge density | Judge unexplained affordances |
|---|---|---|---|
| **Expert** (traders, developers, ops, clinicians, crypto-native) | Domain terms are correct and efficient. Flagging "slippage" or "idempotency key" as jargon here is cargo-culting. | High density is a feature. Whitespace-heavy consumer layouts waste their time. | An expert learns an icon-only toolbar once. Acceptable if consistent. |
| **Mainstream** | Every domain term is a barrier. Untranslated jargon is a High finding on a core path. | Density is a comprehension cost. | An affordance with no label and no first-run explanation is a defect. |
| **Mixed** | Mainstream wording with the expert term available on disclosure. Flag both directions: patronising the expert, and stranding the newcomer. | Offer a density choice, or default comfortable. | Progressive disclosure expected. |

If the audience is unstated and unguessable, ask — it's the single question with
the widest blast radius. If the product itself answers it (a bank's public
signup is mainstream; an internal ops console is expert), don't ask.

**Once the gate is resolved, state your reading of it in one short paragraph at
the top of the report.** A reader who disagrees with the scope or the audience
call needs to see it before the findings, not infer it from them.

---

## 1. Evidence intake — what you actually looked at

Five input types, in descending order of reliability. Full procedure, tool
specifics, and known limitations: **`references/evidence-intake.md`**.

| # | Evidence | Gives you | Confidence ceiling |
|---|---|---|---|
| 1 | **Live product** — a URL you can browse, or an app you can drive (browser tools if available) | Real states, real copy, real timings, real focus order, real errors | **Observed** |
| 2 | **Design files** — Figma via MCP (`get_screenshot`, `get_variable_defs`, `get_design_context`, `get_metadata`) | Intended design, tokens, layout, copy | **Observed** for design intent; **Inferred** for runtime behavior |
| 3 | **Screenshots / recordings** the user provides | What's in frame, and only that | **Observed** in frame; **Inferred** outside it |
| 4 | **Source code** in the working directory — components, routes, tokens, copy strings | Structure, states that exist in code, tokens, a11y attributes | **Observed** for what the code says; **Inferred** for what it renders |
| 5 | **Verbal description only** | A model of the product, not the product | **Hypothesis** — never higher |

**The hard rules:**

- **Never invent a screen, a label, a state, or a behavior you did not see.** Not
  a plausible one, not a typical one. If you need to name a button, quote it.
- **A finding with no evidence is a hypothesis to verify**, labeled `Hypothesis`,
  and phrased as a question the team can answer.
- **Partial coverage is stated, not filled in.** If you were asked to audit
  checkout and only saw the cart, the report says so in §Scope and the backlog
  says what's still unaudited. Inference does not close that gap.
- **If nothing usable is available, ask for scope + access before auditing** —
  one round of questions, then work with whatever comes back.

---

## 2. The audit spine — 16 dimensions

Always in scope for a full audit; a scoped audit uses the subset that fits. Each
reference file gives, per check: **what to check · why it matters · common
failure signatures · what a fix looks like.**

| # | Dimension | Covers | Load |
|---|---|---|---|
| 1 | **First-run & onboarding** | Time to first value, permission/signup timing, skippability, gating | `dimensions/onboarding-and-flows.md` |
| 2 | **Information architecture & navigation** | Findability, depth, labeling, orientation, dead ends | `dimensions/navigation-and-ia.md` |
| 3 | **Core task flows** | Step count, friction, drop-off risk, task success, reversibility | `dimensions/onboarding-and-flows.md` |
| 4 | **Input & forms** | Field count, validation timing, error messaging, autofill, keyboard | `dimensions/forms-and-input.md` |
| 5 | **System status & feedback** | Loading, skeletons, optimistic updates, progress, confirmations | `dimensions/feedback-and-states.md` |
| 6 | **Error prevention & recovery** | Destructive-action guards, undo, recovery paths | `dimensions/feedback-and-states.md` |
| 7 | **State coverage** | Empty, sparse, loading, error, offline, overflow, first-use vs power-use | `dimensions/feedback-and-states.md` |
| 8 | **Content & microcopy** | Clarity, jargon vs audience, tone consistency, CTA labeling | `dimensions/content-and-copy.md` |
| 9 | **Visual hierarchy & layout** | Scan path, density, grouping, whitespace, focal points | `dimensions/visual-hierarchy.md` |
| 10 | **Design system consistency** | Token adherence, one-off values, component drift, spacing rhythm | `dimensions/design-system.md` |
| 11 | **Data display** | Number formatting and alignment, precision, truncation, units, timestamps, sort/filter | `dimensions/data-display.md` |
| 12 | **Accessibility** | WCAG 2.1 AA: contrast, focus, target size, semantics, alt text, motion, SR flow | `accessibility.md` |
| 13 | **Responsive & platform conventions** | Breakpoints, touch targets, gestures, platform idioms, safe areas | `platform-web.md` / `platform-mobile.md` |
| 14 | **Perceived performance** | Time-to-interactive feel, layout shift, blocking states | `dimensions/feedback-and-states.md` |
| 15 | **Trust, safety & privacy** | Data handling clarity, consent, irreversibility warnings | `dimensions/trust-and-dark-patterns.md` |
| 16 | **Dark patterns** | Forced continuity, confirmshaming, hidden costs, manufactured urgency | `dimensions/trust-and-dark-patterns.md` |

**Onchain products add** `references/web3.md` — wallet connection, address and
identity display, transaction lifecycle, cost clarity, approvals and delegation,
onchain error taxonomy, security posture, on/off-ramp friction, and
crypto-native vs mainstream wording. It is a layer on top of all 16, never a
replacement, and it is loaded only when §0e says so.

---

## 3. The finding schema

Every finding, without exception:

```
ID              stable, dimension-prefixed — NAV-03, A11Y-07, FORM-02
Dimension       one of the 16 above (or WEB3)
Severity        Blocker | High | Medium | Low
Confidence      Observed | Inferred | Hypothesis
Location        screen, flow step, component, file:line, or Figma node
Evidence        what you actually saw — quote the label, describe the state
Why it matters  the user consequence, not the rule citation
Recommendation  the concrete change; verbatim copy rewrites when copy is the issue
Effort          S | M | L
```

### Severity — graded the same way every time

- **Blocker** — users **cannot complete a core task**, or they risk irreversible
  loss (data, money, access). Includes: a flow with no exit, a destructive action
  with no confirmation or undo, a keyboard trap, an error state with no recovery
  path. Ship-stopping.
- **High** — significant friction or misunderstanding **on a core path**. The
  task is completable, but a meaningful share of users will fail, hesitate,
  double-take, or get it wrong. Includes AA contrast failures on primary content
  and missing focus indication on a primary flow.
- **Medium** — degrades quality on **secondary paths**, or a core-path issue that
  costs seconds rather than success. Inconsistency users will notice.
- **Low** — polish. Real, but nobody abandons over it. Alignment, an off-scale
  spacing value, a slightly-off tone.

Two calibrations: **severity is about user consequence, not how much it annoys
you**; and **frequency multiplies it** — a Medium defect on the screen everyone
sees every day outranks a High on a settings page three people visit.

### Confidence — earned, not assumed

- **Observed** — you saw it: in the running product, the screenshot, the Figma
  node, or the code that indisputably produces it.
- **Inferred** — the evidence strongly implies it but you didn't see the
  rendered result (code shows no `onError` branch → the error state is probably
  missing).
- **Hypothesis** — plausible from a description, unverified. Phrase it as a
  question. **Never present a hypothesis in the findings table as if it were
  observed**; group them in §6 of the report.

### Effort

**S** — copy, a token, a prop, an attribute; under an hour. **M** — a component
or one screen's behavior; a day or two. **L** — structural: a flow, the IA, the
design system. Effort is *your engineering estimate for their codebase*; if you
haven't seen the code, say the estimate is rough.

---

## 4. Report structure

Markdown file by default (`ux-audit-<scope>-<date>.md` in the working directory
unless the user says otherwise). Templates and worked examples live in
**`references/report-template.md`** — don't inline them here.

1. **Scope & evidence base** — what was audited, what was not, with what access
2. **Executive summary** — 5–8 sentences; the three things that matter most
3. **Quick wins** — high impact / low effort, extractable as a standalone list
4. **Findings by dimension**, sorted by severity within each
5. **Prioritized backlog** — an ordered, actionable list. Not a 2×2 matrix.
6. **Open questions** — hypotheses, and what needs user data to settle

A per-dimension **maturity rating (1–5)** is optional and allowed. If you use it:
integers only, one line of justification each, and **no composite score** —
"3.7/5 overall UX health" implies a measurement you did not perform. Don't
manufacture precision.

---

## 5. Stance — how to judge

- **Opinionated, but reasoned.** Every judgment names the user consequence.
  "Best practice says" is not a reason; "a first-time user can't tell which of
  the two blue buttons submits" is.
- **No cargo-culting.** Something is not wrong because Stripe does it
  differently. It's wrong because it costs the user something you can name.
- **Label what kind of thing it is:**
  - **Defect** — it breaks, misleads, or blocks. Assert it.
  - **Opportunity** — it works; it could work better. Say so plainly.
  - **Taste** — reasonable people differ. **Label it as taste and don't grade
    it Blocker or High.** A section on taste calls is fine; smuggling them in as
    defects is not.
- **Respect deliberate constraints.** If a team clearly traded something away —
  a dense layout for expert throughput, a long form for a regulatory
  requirement — **name the tradeoff** rather than assuming ignorance. Audit the
  tradeoff's execution, not its existence.
- **Anatomy is an example, not a mandate.** Every px, radius, and height in the
  reference files is one reasonable taste. Judge **internal consistency with the
  system the product chose**, never conformance to a number written here.
- **No padding.** A thin audit honestly scoped beats a long one full of generic
  observations. Twelve real findings beat forty, and forty is usually a sign you
  started generating instead of looking.
- **Say what's good, briefly.** Not flattery — calibration. A reader who sees
  only failures can't tell whether you understood the product.

---

## 6. Modes

Defined here so the skill is portable; `.claude/commands/` are thin wrappers.

| Mode | Scope | Loads | Output |
|---|---|---|---|
| **audit** (default) | Full product or a named area, all 16 dimensions | The gate, intake, every dimension file the scope touches | Full report |
| **flow** | One flow, end to end, step by step | `onboarding-and-flows.md` + `forms-and-input.md` + `feedback-and-states.md` + `content-and-copy.md` | Per-step findings + a flow map |
| **quick** | Heuristic sweep, **~10 findings max**, highest severity only | This file + `report-template.md` (quick section) | Executive summary + quick wins; no per-dimension chapters |
| **a11y** | Accessibility only, WCAG 2.1 AA | `accessibility.md` + the relevant platform file | Findings keyed to success criteria |
| **tokens** | Design system consistency only | `dimensions/design-system.md` + `dimensions/visual-hierarchy.md` | Drift inventory + consolidation proposal |
| **web3** | Onchain surfaces only | `web3.md` + `dimensions/trust-and-dark-patterns.md` | Onchain findings layered on any general ones already made |

`quick` is a real constraint, not a suggestion: if a sweep finds thirty things,
report the ten that matter and say thirty were seen.

---

## 7. References — load what the scope needs

**Always, at the start of a real audit:**
- `references/evidence-intake.md` — how to gather and record evidence from each
  source, and the limitations of each.

**Per dimension** (§2 table routes to these):
- `references/dimensions/onboarding-and-flows.md`
- `references/dimensions/navigation-and-ia.md`
- `references/dimensions/forms-and-input.md`
- `references/dimensions/feedback-and-states.md`
- `references/dimensions/content-and-copy.md`
- `references/dimensions/visual-hierarchy.md`
- `references/dimensions/design-system.md`
- `references/dimensions/data-display.md`
- `references/dimensions/trust-and-dark-patterns.md`

**Cross-cutting:**
- `references/accessibility.md` — WCAG 2.1 AA checks, contrast math, focus rules
- `references/platform-web.md` — website / web app / desktop conventions
- `references/platform-mobile.md` — iOS, Android, and mobile-web conventions
- `references/web3.md` — onchain module, **only** when §0e says the product is onchain
- `references/report-template.md` — before writing the report

## Scripts

Both are dependency-free Python 3, no API, no network — they support
**remediation proposals**, they are not part of grading.

- `scripts/contrast-check.py` — WCAG 2.x contrast ratios for a pair, a foreground
  against several backgrounds, or a whole palette; reports AA/AAA pass/fail and
  suggests the nearest passing shade. Use it to make a contrast finding concrete
  instead of eyeballed.
- `scripts/generate-palette.py` — deterministic OKLCH palette generator. Use it
  when a finding is "the palette is ad-hoc / has no accessible ramp" and the
  recommendation needs a worked alternative. **Never regenerate a team's palette
  as part of an audit** — an audit produces findings, not a rebrand.
