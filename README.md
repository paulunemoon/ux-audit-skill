# UX Audit Skill

An agent skill that **evaluates the UX of a product that already exists** and
returns evidence-based, prioritized, actionable findings — for any digital
product: a marketing website, a web app, a mobile app, or a desktop app.

It audits against sixteen dimensions, grades every finding by severity and by
how well the evidence actually supports it, and writes a report you can hand to
a team. When the product happens to be onchain, it layers a web3 module on top;
when it isn't, that module is never loaded.

Written as an [Agent Skill](https://code.claude.com/docs/en/skills) — a
`SKILL.md` entry point plus references loaded on demand.

## Install

```bash
git clone https://github.com/paulunemoon/ux-audit-skill.git ~/.claude/skills/ux-audit
```

Then restart your agent. The skill triggers on requests to audit, review,
critique, or diagnose an existing interface — in English or French. It
deliberately **does not** trigger on requests to design or build new UI, and
says so rather than half-answering.

## What it audits

Sixteen dimensions, always in scope for a full audit:

| | | |
|---|---|---|
| First-run & onboarding | Information architecture & navigation | Core task flows |
| Input & forms | System status & feedback | Error prevention & recovery |
| State coverage | Content & microcopy | Visual hierarchy & layout |
| Design system consistency | Data display | Accessibility (WCAG 2.1 AA) |
| Responsive & platform conventions | Perceived performance | Trust, safety & privacy |
| Dark patterns | | |

Each dimension file gives, per check: **what to check · why it matters · common
failure signatures · what a fix looks like** — plus a severity calibration table
so the same problem gets the same grade twice.

**Onchain products** additionally get `references/web3.md`: wallet connection,
address and identity display, the transaction lifecycle, cost clarity, approvals
and delegation, a ten-case onchain error taxonomy, security posture, on/off-ramp
friction, and native-vs-mainstream wording. It layers on the sixteen; it never
replaces them.

## What it needs from you

Evidence, in descending order of usefulness:

1. **A live URL** it can browse, or an app it can drive — the only source that
   shows timing, focus order, and real error behaviour.
2. **A Figma file** via the Figma MCP tools — good for design intent and
   excellent for token drift.
3. **Screenshots or a screen recording** — reliable for exactly what's in frame.
4. **The repo** — structure, tokens, semantics, and which states exist in code.
5. **A description** — the weakest input. Findings become hypotheses, and the
   report says so.

Any one of these works. More is better. The most useful extra you can send is
the **empty, error, and mobile states** of your main screen — that's where most
of the real defects live and where evidence is usually missing.

If you provide nothing usable, the skill asks for scope and access — **once** —
then works with whatever comes back.

## What it produces

A Markdown report in your working directory:

1. **Scope & evidence base** — what was audited, what wasn't, with what access
2. **Executive summary** — the three things that matter most
3. **Quick wins** — high impact, low effort, extractable as a standalone list
4. **Findings by dimension**, sorted by severity
5. **Prioritized backlog** — an ordered list you can work top to bottom
6. **Open questions** — hypotheses, and what needs your analytics to settle

Every finding carries a stable ID, a dimension, a severity (Blocker / High /
Medium / Low, each defined in writing), a **confidence** (Observed / Inferred /
Hypothesis), a precise location, the evidence, the user consequence, a concrete
recommendation, and an effort estimate. When copy is the problem, the
recommendation contains the replacement copy verbatim.

## Modes

| Command | What it does |
|---|---|
| `/audit` | Full audit, all sixteen dimensions |
| `/flow` | One flow, end to end, findings per step, plus a flow map |
| `/quick` | Heuristic sweep, **ten findings maximum** |
| `/a11y` | WCAG 2.1 AA only, keyed to success criteria |
| `/tokens` | Design system consistency — token and component drift |
| `/web3` | Onchain surfaces, layered on any general findings |

The modes are defined inside `SKILL.md` so the skill stays portable;
`.claude/commands/` holds thin wrappers over them.

## How it judges

- **Every finding carries evidence.** No evidence means it's a hypothesis,
  labeled as one — never presented as an observation. The skill will not invent
  a screen, a label, or a behaviour it did not see, and it states what it
  couldn't cover rather than filling the gap by inference.
- **Every judgment names the user consequence.** Not "best practice says" —
  "a first-time user can't tell which of the two blue buttons submits".
- **No cargo-culting.** Something isn't wrong because a well-known app does it
  differently; it's wrong because it costs the user something nameable.
- **Defect, opportunity, and taste are labeled as what they are.** Taste is
  never graded Blocker or High.
- **Deliberate tradeoffs are named as tradeoffs**, not treated as ignorance. A
  dense expert interface is audited as a dense expert interface.
- **Anatomy is an example, not a mandate.** The skill audits internal
  consistency with the system a product chose, not conformance to any number
  written in its reference files.
- **No padding.** A thin audit honestly scoped beats a long one full of generic
  observations.

## Scripts

Both are Python 3 with no dependencies, no network, and no API key. They exist
to make recommendations concrete — they don't grade anything.

```bash
# WCAG 2.x contrast — a pair, one-to-many, a whole palette, or a fill's best ink
python3 scripts/contrast-check.py "#8A8F98" "#F5F5F7" --suggest
python3 scripts/contrast-check.py --matrix "#111827" "#6B7280" "#FFFFFF"
python3 scripts/contrast-check.py --on "#F0A500"

# Deterministic OKLCH palette — for when a finding needs a worked alternative
python3 scripts/generate-palette.py "#7C5CFF" --css
```

`contrast-check.py` handles alpha compositing (opacity is not colour), picks a
fill's on-colour by **measured** contrast rather than a lightness threshold, and
suggests the nearest passing shade of the same hue. It exits non-zero when
something fails, so it can gate a check.

`generate-palette.py` is kept from this repo's previous life as a design skill.
In an audit it's for illustrating a remediation — **an audit never regenerates a
team's palette**, because an audit produces findings, not a rebrand.

## Honest limitations

- **It is one reviewer on one device with one data set.** It can identify
  drop-off *risk* from the interface; it cannot measure drop-off. Anything that
  needs your analytics goes in Open questions, not in the findings.
- **It is not a conformance evaluation.** The accessibility mode samples against
  WCAG 2.1 AA and says so. It makes no conformance claim in either direction.
- **Automated accessibility tooling catches roughly a third of real issues.**
  The skill spends its effort on the rest, but a screen-reader pass it couldn't
  run is reported as untested rather than assumed.
- **A Figma file shows intent, not what shipped.** Findings sourced only from
  design are marked as such, and a missing frame in Figma is never treated as
  proof of a missing state.
- **Code shows what exists, not what it looks like.** Contrast, focus
  visibility, and perceived performance can't be graded from source alone.
- **It doesn't do user research.** Heuristic evaluation finds problems experts
  can see; it doesn't tell you what your users actually do.
- **The audit is a snapshot.** Products change; the report records when the
  evidence was gathered.

## Repository layout

```
SKILL.md                                 gate · intake · spine · schema · modes
references/
  evidence-intake.md                     browser · Figma MCP · screenshots · code
  dimensions/
    onboarding-and-flows.md              D1 · D3
    navigation-and-ia.md                 D2
    forms-and-input.md                   D4
    feedback-and-states.md               D5 · D6 · D7 · D14
    content-and-copy.md                  D8
    visual-hierarchy.md                  D9
    design-system.md                     D10
    data-display.md                      D11
    trust-and-dark-patterns.md           D15 · D16
  accessibility.md                       D12
  platform-web.md                        D13 — web, desktop, marketing
  platform-mobile.md                     D13 — iOS, Android, mobile web
  web3.md                                onchain module, conditionally loaded
  report-template.md                     output structures
scripts/
  contrast-check.py
  generate-palette.py
.claude/commands/                        thin wrappers over the modes
```

## Contributing & internals

[SKILL-BRIEF.md](SKILL-BRIEF.md) documents the architecture: load order, why the
dimensions cluster as they do, the conventions every reference file follows, and
where to extend. Read it before adding a check, a dimension, a platform, or a
domain module — the conventions are what keep the audit gradeable.

[CHANGELOG.md](CHANGELOG.md) tracks releases.

## License

[MIT](LICENSE) © Pauline Mila Alonso

Independent and unofficial. Not affiliated with or endorsed by any organisation
named in its reference material.
