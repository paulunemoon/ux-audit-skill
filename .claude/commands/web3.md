---
description: Onchain UX audit — wallet, transactions, costs, approvals, security posture
argument-hint: "[url, path, or scope description]"
---

Run the `ux-audit` skill in **web3** mode (SKILL.md §6).

Target: $ARGUMENTS

1. Confirm the product is actually onchain (gate §0e) before applying any of
   this. Check the code first — wallet SDKs, chain libraries, contract
   directories, or onchain copy in the product. If nothing onchain is there,
   say so and offer a general audit instead.
2. Load `references/web3.md` and
   `references/dimensions/trust-and-dark-patterns.md`.
3. Walk the transaction lifecycle end to end: compose → review → sign → pending
   → resolved, plus every entry in the onchain error taxonomy you can trigger
   or trace.

This module **layers on** the general dimensions — it does not replace them. If
a full audit hasn't been run, say which general dimensions remain uncovered.
