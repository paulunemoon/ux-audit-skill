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
# the skill
git clone https://github.com/paulunemoon/ux-audit-skill.git ~/.claude/skills/ux-audit

# the six mode commands, prefixed so they don't collide with your own
for f in audit flow quick a11y tokens web3; do
  cp ~/.claude/skills/ux-audit/.claude/commands/$f.md ~/.claude/commands/ux-$f.md
done
```

Then **restart your agent** — a skill already loaded in a session isn't re-read.

To update later: `cd ~/.claude/skills/ux-audit && git pull`, re-run the `for`
loop, restart. If you're modifying the skill yourself, symlink it instead of
cloning so your edits are live:

```bash
ln -s /path/to/your/checkout ~/.claude/skills/ux-audit
```

The skill triggers on requests to audit, review, critique, or diagnose an
existing interface — in English or French. It deliberately **does not** trigger
on requests to design or build new UI, and hands those back rather than
substituting an unrequested audit for the change you asked for.

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
replaces them — and it's gated by scope, not just by signal, so a token review
of a repo that happens to ship a wallet SDK doesn't pull it in.

## What it needs from you

Evidence, in descending order of usefulness:

| Evidence | What it buys you |
|---|---|
| **A live URL** it can browse, or an app it can drive | Real states, real copy, real focus order, real timing |
| **A Figma file** via the Figma MCP tools | Design intent and tokens; excellent for drift. Runtime behaviour still inferred |
| **Screenshots or a recording** | Exactly what's in frame — and explicitly nothing beyond it |
| **The repo** | Structure, tokens, semantics, which states exist in code. Appearance inferred |
| **A description** | The weakest input. You get a *review* of hypotheses, not an audit |

Any one works. More is better. The most useful extra you can send is the
**empty, error, and mobile states** of your main screen — that's where most real
defects live and where evidence is usually missing.

If you provide nothing usable, the skill asks for scope, access and audience —
**once**, with each option's confidence ceiling attached so you can decide
whether the cheap answer is good enough — then works with whatever comes back.

Before grading anything it also reads the **stakes**: health, money, legal
standing, safety, children, and anything irreversible raise the bar
independently of who the users are. A cheerful tone is a Low finding in a to-do
app and a High one on a relapse screen.

## What it produces

**A Markdown file. Always** — in your working directory, or `~/Documents/ux-audits/`
when there's no project to be in. Evidence a finding rests on (screenshots,
fetched sources, measurement dumps) lands in a `-evidence/` directory beside it,
so the proof still exists when someone reopens the report next week.

1. **Scope & evidence base** — what was audited, what wasn't, with what access
2. **Executive summary** — the three things that matter most
3. **Quick wins** — high impact, low effort, extractable as a standalone list
4. **Findings by dimension**, sorted by severity
5. **Prioritized backlog** — an ordered list you can work top to bottom
6. **What's working, and what it deliberately left alone** — the second half
   names what you might expect flagged and says why it wasn't
7. **Open questions** — hypotheses, and what needs your analytics to settle

Every finding carries a stable ID, its dimensions, a severity (Blocker / High /
Medium / Low, each defined in writing), a **confidence**, a precise location,
the evidence, the user consequence, a concrete recommendation, and an effort
estimate. When copy is the problem, the recommendation contains the replacement
copy verbatim. When your own codebase already solves the problem correctly
somewhere else, the recommendation points there instead of importing a pattern.

**Confidence names its source, and splits when a finding is part fact and part
inference:**

```
Observed (measured)                        a ratio read off rendered pixels
Observed (computed)                        the same ratio, run over a stylesheet
Observed (code); rendering Inferred        the branch exists; nobody saw it draw
Inferred (no error branch in the code)     strongly implied, not witnessed
Hypothesis                                 plausible from a description, unverified
```

A **description-only** request produces a different document: a *review* rather
than an audit, with `H-` prefixed IDs, a "severity if confirmed" field, the
questions that would settle each risk instead of an evidence field, and a
closing note saying that some of it will be invalidated by the first screenshot
— which is the point.

## Modes

| Command | What it does |
|---|---|
| `/ux-audit` | Full audit, all sixteen dimensions |
| `/ux-flow` | One flow end to end, findings per step, plus a step map and a proposed shorter version |
| `/ux-quick` | Heuristic sweep, **ten findings maximum**, and it says how many more it saw |
| `/ux-a11y` | WCAG 2.1 AA only, keyed to success criteria |
| `/ux-tokens` | Design system consistency — token and component drift, as consolidated inventories |
| `/ux-web3` | Onchain surfaces, layered on any general findings |

You can also just ask in plain language; the commands are shortcuts, not the
entry point. **Every mode writes a file**, including `quick` — a shorter report
is still a report.

The modes are defined inside `SKILL.md` so the skill stays portable across
harnesses; `.claude/commands/` holds thin wrappers over them.

## How it judges

- **Every finding carries evidence.** No evidence means it's a hypothesis,
  labeled as one — never presented as an observation. It will not invent a
  screen, a label, or a behaviour it did not see, and it states what it couldn't
  cover rather than filling the gap by inference.
- **Every judgment names the user consequence.** Not "best practice says", and
  not a citation of its own checklist — "a first-time user can't tell which of
  the two blue buttons submits".
- **No cargo-culting.** Something isn't wrong because a well-known app does it
  differently; it's wrong because it costs the user something nameable.
- **Defect, opportunity, and taste are labeled as what they are.** Taste is
  never graded Blocker or High, and things it can't name a cost for are left
  alone — and *said* to have been left alone.
- **Deliberate tradeoffs are named as tradeoffs**, not treated as ignorance. A
  dense expert interface is audited as a dense expert interface.
- **Anatomy is an example, not a mandate.** It audits internal consistency with
  the system your product chose, not conformance to any number written in its
  reference files. Where a design file and the code disagree, it judges each
  mismatch on merit rather than assuming the design is the authority.
- **Scope is respected.** A one-screen request gets a one-screen audit. Anything
  found outside it that would change an in-scope finding is named as out of
  scope, not quietly audited and not withheld.
- **An audit is not a pull request.** Ask for both and you get the report first,
  then the changes — two deliverables, in that order.
- **No padding.** A thin audit honestly scoped beats a long one full of generic
  observations.

## Script

One, in Python 3, with no dependencies, no network and no API key. It exists to
make recommendations concrete — it doesn't grade anything.

```bash
# WCAG 2.x contrast — a pair, one-to-many, a whole palette, or a fill's best ink
python3 scripts/contrast-check.py "#8A8F98" "#F5F5F7" --suggest
python3 scripts/contrast-check.py --matrix "#111827" "#6B7280" "#FFFFFF"
python3 scripts/contrast-check.py --on "#F0A500"
```

It handles alpha compositing (opacity is not colour), picks a fill's on-colour
by **measured** contrast rather than a lightness threshold, warns when a shade
has no AA-legible ink at all, and suggests the nearest passing shade of the same
hue. It exits non-zero when something fails, so it can gate a check.

**There is deliberately no palette generator.** One shipped through 1.3.1 and
was never invoked in twenty-two runs — not even on a product whose ink ramp
failed AA at three of its four levels, which was exactly the case it was kept
for. That audit proposed three replacement values verified with
`contrast-check`, which is the right shape: the smallest change that clears AA
inside the system the product already has. **An audit produces findings, not a
rebrand**, and a generator in the box invites the opposite.

## What it's been exercised against

Version 1.4.0 follows twenty-two audit runs across seven real projects: a
marketing site, two web apps, a native React Native app, an Electron desktop
app, an onchain product, and one product that existed only as three sentences of
description. All six modes and all five evidence sources were used. Twelve
changes came out of it, eight of which were cases where a run produced something
better than the specification described.

That is testing, not proof. It says the machinery works on real products; it
doesn't say the findings are right for yours.

## Honest limitations

- **It is one reviewer on one device with one data set.** It can identify
  drop-off *risk* from the interface; it cannot measure drop-off. Anything
  needing your analytics goes in Open questions, not in the findings.
- **It is not a conformance evaluation.** The accessibility mode samples against
  WCAG 2.1 AA and says so. It makes no conformance claim in either direction.
- **Automated accessibility tooling catches roughly a third of real issues.**
  The skill spends its effort on the rest, but a screen-reader pass it couldn't
  run is reported as untested rather than assumed.
- **A Figma file shows intent, not what shipped.** Findings sourced only from
  design are marked as such, and a missing frame is never treated as proof of a
  missing state.
- **Code shows what exists, not what it looks like.** Contrast, focus
  visibility, and perceived performance can't be graded from source alone —
  which is why confidence labels distinguish computed from measured.
- **Two runs will not find the same things.** An audit samples. For anything
  high-stakes, two passes surface more than one.
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
  report-template.md                     output structures, including quick,
                                         flow, a11y, tokens and description-only
scripts/
  contrast-check.py                      WCAG contrast, the only script
.claude/commands/                        thin wrappers over the modes
```

## Contributing & internals

[SKILL-BRIEF.md](SKILL-BRIEF.md) documents the architecture: load order, why the
dimensions cluster as they do, the conventions every reference file follows, and
where to extend. Read it before adding a check, a dimension, a platform, or a
domain module — the conventions are what keep the audit gradeable.

One lesson from testing is worth repeating here: **a rule written in a section a
mode never loads is not a rule.** If you add a constraint that must hold
everywhere, put it where every mode reads, not only in the file it belongs to
topically.

[CHANGELOG.md](CHANGELOG.md) tracks releases.

## License

[MIT](LICENSE) © Pauline Mila Alonso

Independent and unofficial. Not affiliated with or endorsed by any organisation
named in its reference material.
