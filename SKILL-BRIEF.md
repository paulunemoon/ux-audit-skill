# SKILL-BRIEF — internal architecture

> For people maintaining this skill. `README.md` is for people using it.
> This document explains why the skill is shaped the way it is, which is the
> part that decays fastest when a repo grows by accretion.

## 1. What this skill is for

**Evaluate an interface that already exists and return findings someone can act
on.** Not design it, not rebuild it, not produce a heuristics essay.

Three constraints shape everything below:

1. **Evidence discipline.** An LLM asked to audit a product it cannot see will
   produce a confident, plausible, entirely fictional audit. That is the primary
   failure mode this skill exists to prevent, and it's why `Confidence` is a
   required field on the finding schema rather than a nicety.
2. **Repeatable grading.** Two audits of the same product should reach similar
   severities. Hence severity definitions written out in `SKILL.md` §3, and a
   severity calibration table at the foot of every dimension file.
3. **Progressive disclosure.** `SKILL.md` is always in context; everything else
   is loaded only when the scope demands it. A full audit that loaded all
   fourteen references at once would spend most of its budget on material it
   never uses.

## 2. Load order

```
SKILL.md (always)
   │
   ├─ §0 gate ──────────────► decides scope, platform, audience, onchain?
   │
   ├─ evidence-intake.md ───► always, before the first finding
   │
   ├─ §2 spine table ───────► routes to dimension files by scope
   │     dimensions/*.md          load only what the scope touches
   │     accessibility.md         always in a full audit
   │     platform-{web,mobile}.md by platform
   │
   ├─ web3.md ──────────────► ONLY if §0e resolved onchain = yes
   │
   └─ report-template.md ───► before writing output
```

The gate runs before any reference is loaded, because the gate is what decides
which references are relevant. Loading `web3.md` before establishing that the
product is onchain would apply onchain criteria to a product that has no chain —
the one failure a conditionally-loaded module has to be built to avoid.

## 3. Why the dimensions are clustered the way they are

Sixteen dimensions, nine dimension files. The clustering follows **what gets
audited in the same pass**, not taxonomy:

| File | Dimensions | Why together |
|---|---|---|
| `onboarding-and-flows.md` | D1, D3 | Same failure mode: steps that exist for the business, not the user. You walk both in one pass. |
| `navigation-and-ia.md` | D2 | Alone — it's the only dimension that requires mapping the whole product before any finding. |
| `forms-and-input.md` | D4 | Alone — high volume, mechanical, and the best source of quick wins. |
| `feedback-and-states.md` | D5, D6, D7, D14 | One subject from four angles: does the interface tell the truth about what it's doing, and does it hold up when things aren't ideal. |
| `content-and-copy.md` | D8 | Alone — it's the only dimension where the deliverable is a rewrite, not a description. |
| `visual-hierarchy.md` | D9 | Alone — plus the generated-UI tells, which are visual-first. |
| `design-system.md` | D10 | Alone — it's the `tokens` mode's whole subject and needs the "audit their system, not ours" framing throughout. |
| `data-display.md` | D11 | Alone — concrete, checkable, and disproportionately consequential (a misread number is a real-world error). |
| `trust-and-dark-patterns.md` | D15, D16 | Same question from opposite ends: does the interface act in the user's interest when the business would benefit from it not doing so. |

`accessibility.md` (D12) and the two platform files (D13) sit at
`references/` root rather than under `dimensions/` because they're loaded by
*mode* and by *platform*, not by scope — `a11y` mode loads one and nothing else.

## 4. Conventions every reference file follows

Break these and the skill degrades unevenly.

- **Front-matter blockquote**: when to read, what it covers, what it doesn't,
  and its finding-ID prefix.
- **Table of contents** with anchor links. Anchors are the slugified heading;
  the `##` level doesn't affect them. Broken TOC links have bitten this repo
  before — check them when you rename a heading.
- **Every check has an ID** (`NAV-A`, `FORM-C`) and four parts: **what to
  check · why it matters · fails like · fix**. The "why" is the user
  consequence, never a rule citation.
- **"Fails like" is a list of observable signatures**, not a restatement of the
  check. It's what makes a dimension usable by someone scanning a screen.
- **Cross-references are explicit** and name both the file and the check ID.
  Many defects are findings in two dimensions; say so rather than duplicating.
- **A severity calibration table closes every file.** This is what makes
  grading repeatable, and it is the first thing to update when real use shows a
  dimension being graded inconsistently.
- **"Anatomy is an example, not a mandate"** appears wherever numbers do. The
  skill audits internal consistency with the system the product chose. A value
  written here is never the standard.

## 5. Deliberate design decisions

**Confidence is separate from severity.** A Blocker you inferred from code is
different from a Blocker you watched happen. Collapsing them would let inference
masquerade as observation, which is exactly the failure in §1.

**Severity is user consequence, modulated by frequency — not annoyance.** The
calibration tables exist because "how bad is this" is the judgment an LLM is
least consistent about, and consistency here is most of what makes an audit
trustworthy.

**Taste is a labeled category, not a severity.** The reference files carry
strong aesthetic positions, and left ungraded those turn into High-severity
findings about radius values. Labeling taste as taste is what lets the skill
keep the opinions without weaponising them.

**Every generated-UI tell names a user cost.** "Don't use a purple-to-green
gradient" is not an audit criterion. "Text over a two-colour gradient has
non-deterministic contrast" is. Any tell whose only cost is that it looks
templated is graded Opportunity or Taste — see `visual-hierarchy.md`, VIS-I.

**Drift is reported as consolidated inventories.** Forty individual `Low`
findings for forty off-scale spacing values is technically complete and
practically useless. `design-system.md` specifies the aggregate format.

**Modes live in `SKILL.md`, not in `.claude/commands/`.** The commands are Claude
Code-specific; the modes must work in any harness that loads a skill. The
commands are thin on purpose — if a command file starts containing instructions,
they belong in `SKILL.md` instead.

**Scripts are for remediation, not grading.** `contrast-check.py` turns "that
looks low contrast" into a measurement, which is what makes an accessibility
finding unarguable. `generate-palette.py` illustrates an alternative when the
finding is "there's no accessible ramp". Neither decides anything. The rule that
an audit never regenerates a team's palette is stated in `SKILL.md`, in
`design-system.md`, and in the README, because it's the most tempting thing to
get wrong with a generator in the box.

**The web3 module opens by stating it layers on.** Without that line, an onchain
audit tends to become *only* an onchain audit, and the product's forms,
accessibility, and IA go unexamined. Same reason `.claude/commands/web3.md`
closes by naming the uncovered dimensions.

## 6. The audience call

`SKILL.md` §0f (expert / mainstream / mixed) is the highest-leverage decision in
the gate. It changes the grade of the same observation across at least four
dimensions:

- **D8** — whether a domain term is efficient or a barrier.
- **D9** — whether high density is a feature or a comprehension cost.
- **D2/D4** — whether an unlabelled icon-only control is learnable or a defect.
- **D3** — how much repeat-use optimization is worth.

`web3.md` narrows it to crypto-native-vs-mainstream, which is the same mechanism
applied to one domain — a pattern any future domain module should follow rather
than inventing its own audience axis. Getting the call wrong in either direction
produces a bad audit: patronising an expert product, or judging a mainstream one
by expert tolerances. It is one of the few things worth asking about when it
can't be determined.

## 7. Where to extend

- **A new check** goes in an existing dimension file. Give it an ID, the four
  parts, and a row in that file's severity table.
- **A new dimension** means editing `SKILL.md` §2 (the spine table), adding the
  file, and deciding whether it needs a mode. Seventeen dimensions is not
  automatically better than sixteen — the bar is that it can't be graded inside
  an existing one.
- **A new mode** goes in `SKILL.md` §6 plus a thin command wrapper. It should
  change *what is loaded*, not just what is emphasized; otherwise it's a
  scope argument to `/audit`.
- **A new platform** (TV, watch, voice, XR) gets a `platform-*.md` and a row in
  the gate's §0c. D13 is the only dimension designed to be extended by platform.
- **A new domain module** follows `web3.md`: conditionally loaded, opens by
  stating it layers on the general dimensions, ends with its own severity table.
  The gate needs a detection step that checks the evidence before asking.

## 8. Known gaps

1. **No worked end-to-end example audit** in the repo. The report template has a
   worked finding, not a whole report.
2. **Perceived performance (D14) has no measurement path.** It's judged from
   observation, which is honest but weaker than the rest. Wiring in Lighthouse
   or CrUX data would need a network dependency the skill deliberately avoids.
3. **No i18n/RTL dimension.** Localization readiness is one check inside
   `content-and-copy.md`. A product shipping to RTL locales probably needs more.
4. **Desktop-app conventions are one section** of `platform-web.md`, not their
   own file. Fine at current depth; a real desktop audit would outgrow it.
5. **The dark-pattern register is descriptive, not jurisdictional.** It flags
   regulatory exposure as a factor to check with counsel; it doesn't map
   patterns to specific regulations, and shouldn't try to.
6. **No verification that a report was actually written to a file** rather than
   printed into the conversation. Stated as a rule in `report-template.md`;
   nothing enforces it.
