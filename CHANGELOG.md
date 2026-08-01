# Changelog

All notable changes to this skill are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] — 2026-08-01

Four more absorptions from live runs, and the first pass where all six modes —
`audit`, `quick`, `flow`, `a11y`, `tokens`, `web3` — were exercised against real
projects. `flow`, `a11y` and `web3` each followed their template on the first
try and produced no corrections, which is why none appear below.

### Changed

- **The report gains a "What's working, and what I left alone" section.** Two
  runs invented it independently, and the second half is the part that earns its
  place: naming what a reader might expect flagged and saying why it wasn't.
  "I left the single-mode palette, the Manrope/Inter split, and the navbar's
  32px radius alone — those read as decisions, and I couldn't name a cost."
  That pre-empts *did you even notice X*, shows the taste discipline was applied
  rather than claimed, and tells the team which of their choices survived
  scrutiny — which a list of defects cannot.
- **Recommendations cite the in-repo precedent when one exists.** "The supplier
  inputs restore a focus ring correctly 185 lines earlier"; "the review screen
  you need is already 500 lines up in this file". It is the strongest form a
  recommendation takes: the fix becomes a copy rather than a design decision, it
  lands consistent with the product's own conventions instead of importing
  ours, and the team cannot argue the pattern doesn't fit them.
- **A description-only review raises nothing below Medium.** A re-run of the
  same description-only prompt produced 13 risks graded 2 Blocker / 6 High /
  5 Medium and no Low at all, which is right: a Low hypothesis about an unseen
  product is speculation about polish and cannot be checked. Written down so it
  survives — the shape is legitimately top-heavy, and a risk not worth opening
  the app for should be dropped rather than graded.
- **`computed` joins the confidence qualifiers, and is distinguished from
  `measured`.** A quick-mode run labelled its contrast findings
  `Observed (code + computed)` and stated in the closing note that the figures
  were "computed from declared hex values rather than measured on screen" — a
  distinction the enumerated list did not offer, so following it literally meant
  writing `measured` for a value nobody had looked at. A ratio read off rendered
  pixels is measured; a ratio produced by running `contrast-check.py` over a
  stylesheet is computed, and it assumes those values reach the screen
  unmodified by opacity, a filter, or a cascade. Usually right, always cheaper,
  still not the same as having looked.

## [1.1.0] — 2026-08-01

Five real audit runs against live projects, and everything below comes from
them. Three of the seven changes are not bug fixes — they are cases where a run
produced something better than the specification described, and the
specification lost.

### Added

- **A description-only review shape** (`report-template.md`). Given three
  sentences about a product and no screen to look at, the previous instruction
  was to push every hypothesis into §6 Open questions — which leaves §2 through
  §5 empty and §6 carrying the entire document. The shape that works is now
  written down: the title says *review*, not *audit*; every ID carries an `H-`
  prefix so a hypothesis survives being quoted into a ticket; the severity field
  reads **"Severity if confirmed"** and repeats that under the section heading;
  **"The questions that settle it"** replaces an Evidence field that cannot
  exist; there is no Confidence column, because a column of one repeated value
  is noise; and the closing note welcomes being wrong — *some of this will be
  invalidated by the first screenshot, which is the point.*
- **Stakes, as an axis in the gate** (SKILL.md §0f). Audience was graded by
  expertise and had nothing for consequence. Health, money, legal standing,
  safety, children, and anything irreversible now raise the bar in four stated
  ways: tone stays sober whatever the product's usual voice, claims about the
  user's body or money commit you, collected data is sensitive by category, and
  **failure is asymmetric** — a discouraging screen can cost the outcome the
  product exists for while registering as ordinary churn. A cheerful tone is Low
  in a to-do app and High on a relapse screen.
- **Real example rows in the quick-mode findings table.** It shipped with a
  single empty row, so there was no Confidence value to copy and the column
  filled with the bare enum word from the schema. Four populated rows now, with
  a compound `Observed (code); 404 Inferred` among them.

### Changed

- **Confidence requires its source, and splits when a finding is part fact and
  part inference.** `Observed` alone hides the difference between reading a line
  of CSS and measuring a rendered pixel, so the qualifier — `(code)`,
  `(rendered)`, `(measured)`, `(design file)`, `(recording)` — is now required,
  and `Observed (code); rendering Inferred` is the form for a finding whose
  existence was read but whose appearance was never seen. Named the failure it
  prevents: a scope section stating that nine of ten screens were never rendered,
  above findings that are all marked Observed anyway.
- **A finding names its primary dimension plus the others it touches.** The
  schema asked for one; real findings routinely span two or three.
- **The audit-vs-creation row in §0a is scoped to cases that can actually reach
  it.** It carried a rule for "improve this" that could never execute — skill
  selection happens against the request text, so the exact phrasing the rule
  described is the phrasing that prevents the skill loading. §0a now states that
  it runs *after* loading, that a build request will not load the skill by
  design, and that this is not a missed audit. The ambiguous row is replaced by
  a hand-it-back rule: offer the audit in one line, then do the work asked for.
- **Reports are never written into the home directory.** A description-only
  review runs from `~` because there is no repo to be in.

### Fixed

- **Check IDs were being cited as the reason a finding matters.** `WEB3-G calls
  for…` opened a Why-it-matters in a live run. The IDs are internal bookmarks
  the reader has never seen; citing one is the same move as "best practice
  says". §3 now says where they belong (a trailing `Related.` line, or nowhere),
  gives a don't/do table using the real failing sentence, and adds the test: if
  you cannot state the consequence without naming a check, you have found a rule
  the product does not follow, which is not the same thing.
- **Self-reported counts drifted.** A section headed "6 findings" carried seven,
  and a run described its own report as holding 34 when it held 40. Counts are
  now written last, from the finished document, or left out — including when
  describing the report in conversation.

## [1.0.0] — 2026-08-01

First public release.

`ux-audit` evaluates the UX of a product that already exists — a marketing
website, a web app, a mobile app, or a desktop app — and returns evidence-based,
prioritized, actionable findings. It does not design, and it does not rebuild.

### Added

**The skill entry point.** `SKILL.md` carries the audit gate, the evidence
rules, the dimension spine, the finding schema, the report structure, the
critique stance, and the modes. Everything deeper is a reference file loaded on
demand, so a scoped audit doesn't pay for material it never reads.

**A six-question audit gate.** Audit or creation · scope · platform · evidence ·
onchain? · audience. It resolves from the request or from a glance at what's
available, and asks at most one batched round of questions. A request to *create*
new UI gets one line and a hand-off rather than a half-answer.

**The audience call** — expert / mainstream / mixed — with a table of what each
answer changes. It is the highest-leverage decision in the gate: the same
observation about jargon, density, or an unlabelled icon-only control is graded
differently depending on it.

**Evidence discipline, as the governing rule.** `references/evidence-intake.md`
covers five sources in descending order of reliability — live product, Figma via
MCP, screenshots and recordings, source code, verbal description — with the
confidence ceiling of each and its failure modes. Highlights:

- A table of what to actually **do** to a running product (tab through it, empty
  it, overflow it, throttle it, zoom it) rather than only looking at it.
- The Figma MCP limitations that matter in practice: base64 screenshot
  reliability degrades over a long session, so fall back to `get_design_context`
  with a specific `nodeId` instead of retrying; work from a `nodeId` once you
  have one; Figma CDN assets are not fetchable with `curl`; and **a missing frame
  in a design file is not evidence of a missing state**.
- A code inventory table — tokens, styling approach, component library, icon
  set, motion, routes, copy, a11y attributes, state branches — that establishes
  the system a product actually has, since consistency is graded against *it*.
- A SEEN / NOT SEEN log that becomes the report's scope section verbatim, so
  partial coverage is disclosed rather than inferred over.

**Sixteen audit dimensions**, each routed to a reference file that gives, per
check: what to check · why it matters · common failure signatures · what a fix
looks like.

| | |
|---|---|
| D1 First-run & onboarding · D3 Core task flows | `dimensions/onboarding-and-flows.md` |
| D2 Information architecture & navigation | `dimensions/navigation-and-ia.md` |
| D4 Input & forms | `dimensions/forms-and-input.md` |
| D5 Status & feedback · D6 Error prevention & recovery · D7 State coverage · D14 Perceived performance | `dimensions/feedback-and-states.md` |
| D8 Content & microcopy | `dimensions/content-and-copy.md` |
| D9 Visual hierarchy & layout | `dimensions/visual-hierarchy.md` |
| D10 Design system consistency | `dimensions/design-system.md` |
| D11 Data display | `dimensions/data-display.md` |
| D12 Accessibility (WCAG 2.1 AA) | `accessibility.md` |
| D13 Responsive & platform conventions | `platform-web.md` · `platform-mobile.md` |
| D15 Trust, safety & privacy · D16 Dark patterns | `dimensions/trust-and-dark-patterns.md` |

**A strict finding schema** with severity defined in writing (Blocker / High /
Medium / Low, by user consequence), and a **Confidence** field (Observed /
Inferred / Hypothesis) kept separate from severity so an inference can never
masquerade as an observation. Every reference file closes with a **severity
calibration table**, which is what makes grading repeatable across audits.

**`references/accessibility.md`** — WCAG 2.1 AA as seventeen checks keyed to
success criteria, the contrast thresholds, the 2.x contrast math, and the three
traps that produce wrong measurements (alpha compositing, text over
gradients and images, and the known limits of the 2.x formula on some hue
pairs). Includes how to write an accessibility finding so it survives being
called theoretical, and the instruction to make no conformance claim in either
direction.

**`references/dimensions/trust-and-dark-patterns.md`** — an eleven-entry dark
pattern register, each with what it looks like, what it costs the user, and the
honest version, plus a rule against judging intent and against padding the
dimension when a product has none.

**`references/platform-web.md` and `references/platform-mobile.md`** — the
conventions worth flagging only when breaking them costs the user something.
The mobile keyboard section keeps the distinction that trips most teams up:
viewport units and the on-screen keyboard are two different problems (`dvh`
fixes browser chrome; only the `VisualViewport` API addresses the keyboard),
plus the React Native specifics including the
`@gorhom/bottom-sheet` / `react-native-keyboard-controller` conflict.

**`references/web3.md`** — a conditionally-loaded onchain module, applied only
when the gate establishes the product is onchain, and never mentioned otherwise.
Wallet connection and session, mobile deep-link round trips, network and devnet
clarity, address and identity display, the four domain-mark categories with
their required fallbacks, amount entry, the transaction lifecycle, signature
preview, cost clarity, a ten-case onchain error taxonomy with the copy each
should carry, approvals and delegation, security posture, on/off-ramp friction,
and wording calibration. It opens by stating it **layers on** the sixteen
general dimensions rather than replacing them.

**`references/report-template.md`** — six report shapes (full, quick, flow,
a11y, tokens), a fully worked finding annotated with what makes it usable, the
state-coverage matrix, and the rules for the optional maturity rating: integers
only, one line of justification per row, and **no composite score**, because a
decimal implies a measurement that was not performed.

**Six modes** — `audit`, `flow`, `quick`, `a11y`, `tokens`, `web3` — defined in
`SKILL.md` so the skill stays portable across harnesses, with thin
`.claude/commands/` wrappers. `quick` is capped at ten findings and required to
say how many more were seen.

**Two scripts**, both Python 3 with no dependencies, no network, and no API key.
They make recommendations concrete; they do not grade anything.

- `scripts/contrast-check.py` — WCAG 2.x contrast for a pair, one-to-many, or a
  whole palette as a matrix. Handles alpha compositing (opacity is not colour),
  picks a fill's on-colour by **measured** contrast rather than a lightness
  threshold, warns when a shade has no AA-legible ink at all, and suggests the
  nearest passing shade of the same hue. Exits non-zero on failure so it can
  gate a check.
- `scripts/generate-palette.py` — deterministic OKLCH palette generator. The
  anchor hex is preserved exactly as the `500` step; out-of-gamut steps have
  their chroma reduced until they fit sRGB rather than clipping to mud. In an
  audit it exists to illustrate a remediation — **an audit never regenerates a
  team's palette**, because an audit produces findings, not a rebrand.

**`SKILL-BRIEF.md`** — the architecture document: load order, why the dimensions
cluster as they do, the conventions every reference file follows, the deliberate
decisions behind the design, where to extend, and the known gaps.

### Known gaps at 1.0.0

Tracked in [SKILL-BRIEF.md](SKILL-BRIEF.md) §8:

1. No worked end-to-end example audit in the repo — the report template has a
   worked finding, not a whole report.
2. Perceived performance (D14) is judged from observation with no measurement
   path; wiring in real metrics would need a network dependency the skill
   deliberately avoids.
3. No dedicated internationalization / RTL dimension — localization readiness is
   one check inside `content-and-copy.md`.
4. Desktop-app conventions are one section of `platform-web.md` rather than
   their own file.
5. The dark-pattern register flags regulatory exposure as a factor to check with
   counsel; it deliberately does not map patterns to specific regulations.
6. Nothing enforces that a report is written to a file rather than printed into
   the conversation — it is stated as a rule, not checked.

[1.2.0]: https://github.com/paulunemoon/ux-audit-skill/releases/tag/v1.2.0
[1.1.0]: https://github.com/paulunemoon/ux-audit-skill/releases/tag/v1.1.0
[1.0.0]: https://github.com/paulunemoon/ux-audit-skill/releases/tag/v1.0.0
