---
description: Deep-dive audit of a single user flow, step by step
argument-hint: "<flow name> [+ url, path, or access details]"
---

Run the `ux-audit` skill in **flow** mode (SKILL.md §6).

Flow: $ARGUMENTS

1. Run the audit gate (§0), then gather evidence per
   `references/evidence-intake.md` — **walk the flow end to end**, then walk it
   a second time as a returning user.
2. Load `references/dimensions/onboarding-and-flows.md`,
   `forms-and-input.md`, `feedback-and-states.md`, and `content-and-copy.md`.
   Add `web3.md` if the flow involves a signature or a wallet.
3. Map the flow first — every screen, required input, decision point, and exit —
   before writing a single finding. Mark each step **necessary / deferrable /
   removable**.
4. Report per step, not per dimension, using the flow template in
   `references/report-template.md`.
