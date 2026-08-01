---
description: Fast heuristic UX sweep — ten findings maximum, highest severity only
argument-hint: "[url, path, Figma link, or scope description]"
---

Run the `ux-audit` skill in **quick** mode (SKILL.md §6).

Target: $ARGUMENTS

A heuristic sweep, not a full audit. Load SKILL.md and the quick-mode section of
`references/report-template.md` — **including that file's header block, which
carries the rules that apply to every report** — and don't pull the dimension
files unless something specific demands one.

**Write the report to a file before you summarise it**, even for a five-minute
sweep, even when the target is a bare URL and there's no project directory to be
in. In that case it goes to `~/Documents/ux-audits/`, and you say where. A quick
review that exists only in the conversation has not been delivered.

**Ten findings maximum.** If the sweep surfaces more, report the ten that matter
most and state how many were seen. Output is an executive summary plus quick
wins; no per-dimension chapters.

Close by naming which dimensions were not swept, so nobody mistakes this for
full coverage.
