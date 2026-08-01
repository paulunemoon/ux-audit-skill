---
description: Design system consistency review — token drift, component drift, spacing rhythm
argument-hint: "[repo path, Figma link, or both]"
---

Run the `ux-audit` skill in **tokens** mode (SKILL.md §6).

Target: $ARGUMENTS

1. Establish what system exists (`references/evidence-intake.md`, the code
   inventory table). If there isn't one, that absence is the finding — don't
   grade adherence to nothing.
2. Load `references/dimensions/design-system.md` and
   `references/dimensions/visual-hierarchy.md`.
3. Audit the product **against the system it chose**, not against any values
   written in the reference files. Drift is the finding; deviation from a
   number in the skill is not.
4. Measure every text-bearing token pair with `scripts/contrast-check.py` — this
   is where a design-system review earns its keep.

Report drift as **consolidated inventories per category** (value, count,
locations, target token), never as forty individual Low findings. Where both
Figma and code are available, report design/build drift as its own finding.
