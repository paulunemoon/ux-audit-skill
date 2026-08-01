---
description: Full UX audit of an existing product — all 16 dimensions, evidence-based, prioritized
argument-hint: "[url, path, Figma link, or scope description]"
---

Run the `ux-audit` skill in **audit** mode (SKILL.md §6).

Target: $ARGUMENTS

1. Run the audit gate (§0) — audit-vs-creation, scope, platform, evidence,
   onchain?, audience. Ask at most one batched round of questions, and only for
   what you genuinely can't determine.
2. Read `references/evidence-intake.md` and gather evidence before writing any
   finding. Keep the SEEN / NOT SEEN log.
3. Load the dimension files the scope touches (§2 routes to them). Load
   `references/web3.md` only if the gate said the product is onchain.
4. Read `references/report-template.md`, then write the report to a Markdown
   file in the working directory.

Every finding carries evidence. No evidence means it is a hypothesis, labeled as
one and grouped in the Open questions section — never presented as a finding.
