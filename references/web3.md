# Onchain / web3 module

> **When to read:** **Only** when the audit gate (SKILL.md §0e) established that
> the product is onchain. If it isn't, this file is never loaded and never
> mentioned. Finding IDs: `WEB3-nn`.
>
> **This layers on top of the sixteen general dimensions; it does not replace
> them.** An onchain product is still audited for onboarding, IA, forms, states,
> copy, hierarchy, tokens, data display, accessibility, platform conventions,
> trust, and dark patterns. Everything here is *additional*, and it maps back:
> the transaction lifecycle is D3 and D5; cost clarity is D15; the error taxonomy
> is D6 and D8; wallet connection is D1.
>
> **The governing principle to audit against: does the product manage
> *blockchain mechanics* on the user's behalf, or does it hand them over?** Users
> deal in actions and amounts. Hashes, RPC errors, base64 payloads, and raw
> program errors are translated or abstracted — not exposed. How far to push that
> depends on the audience call (§0f), which on an onchain product usually means
> **crypto-native vs mainstream** (see WEB3-P).

## Table of contents
1. [WEB3-A · Wallet connection — discovery and entry](#web3-a--wallet-connection--discovery-and-entry)
2. [WEB3-B · Connection states and session](#web3-b--connection-states-and-session)
3. [WEB3-C · Mobile connection and deep links](#web3-c--mobile-connection-and-deep-links)
4. [WEB3-D · Network and chain clarity](#web3-d--network-and-chain-clarity)
5. [WEB3-E · Address and identity display](#web3-e--address-and-identity-display)
6. [WEB3-F · Domain marks — tokens, protocols, validators, wallets](#web3-f--domain-marks--tokens-protocols-validators-wallets)
7. [WEB3-G · Amount entry](#web3-g--amount-entry)
8. [WEB3-H · The transaction lifecycle](#web3-h--the-transaction-lifecycle)
9. [WEB3-I · The signature preview](#web3-i--the-signature-preview)
10. [WEB3-J · Cost clarity](#web3-j--cost-clarity)
11. [WEB3-K · Pending, confirmed, failed](#web3-k--pending-confirmed-failed)
12. [WEB3-L · The onchain error taxonomy](#web3-l--the-onchain-error-taxonomy)
13. [WEB3-M · Approvals and delegation](#web3-m--approvals-and-delegation)
14. [WEB3-N · Security posture](#web3-n--security-posture)
15. [WEB3-O · On/off-ramp and KYC friction](#web3-o--onoff-ramp-and-kyc-friction)
16. [WEB3-P · Wording calibration](#web3-p--wording-calibration)
17. [WEB3-Q · Onchain data display](#web3-q--onchain-data-display)
18. [WEB3-R · Activity and transaction-type iconography](#web3-r--activity-and-transaction-type-iconography)
19. [Severity calibration](#severity-calibration-for-this-file)

---

## WEB3-A · Wallet connection — discovery and entry

**Check.** Where is the connect entry point, and when does it appear? Can a
visitor see what the product does **before** being asked to connect? Are
multiple wallets offered, with installed ones detected and surfaced first? Is
there a path for someone with no wallet at all?

**Why it matters.** Gating the whole interface behind a wallet connection is the
single most common onchain onboarding mistake: it asks for a security-relevant
action from someone who doesn't yet know what the product is. It maps directly
to `onboarding-and-flows.md`, ONB-B — the connect prompt is a signup wall with
higher stakes.

**Fails like.**
- The app renders nothing until connected.
- Connect demanded on arrival rather than at the action that needs it.
- A single wallet supported with no explanation of why.
- Installed wallets not detected, so the user hunts through a list.
- "No wallet?" as a dead end — no install link, no alternative path.
- Wallet rows rendering as empty circles because the logos were fetched instead
  of read from the adapter (see WEB3-F).
- The wallet-select surface built as a dropdown anchored inside the header, so
  its scrim clips to the navbar — the clipped-overlay defect in
  `feedback-and-states.md`, FBK-G. This is the most common structural bug in
  onchain UI.
- For a mainstream product, **no wallet path at all** — social login only. Users
  who already hold a wallet are locked out of their own funds, and the product
  reads as a walled garden. Downplayed is fine; absent is not.

**Fix.** Show the product first; ask at the point of action, labelled with what
it unlocks ("Connect to swap"). Detect and sort installed wallets first. Make
"no wallet" a path. The wallet-select surface is a **portaled, centred modal**
on web and a **sheet** on mobile — never a header dropdown. On a mainstream
product, keep a discreet but always-reachable "Connect a wallet" option beside
the primary path.

---

## WEB3-B · Connection states and session

**Check.** Walk every state: disconnected · connecting · connected · rejected ·
wrong network · disconnected-by-the-wallet · session expired. Is each one
designed? Does the connection persist across reloads, and is that persistence
communicated? Is disconnect available and does it actually disconnect?

**Fails like.**
- No "connecting" state, so the app looks frozen during the wallet round-trip.
- A cancelled connection treated as an error, with red alarm styling — **the
  user declined; that's a neutral outcome** (see WEB3-L).
- Connection not persisted, so a reload demands reconnection.
- Connection persisted with no indication, so the user doesn't realize they're
  connected.
- No disconnect control, or one that clears local state while the wallet still
  considers the site connected.
- The app not reacting when the user switches accounts in the wallet, so it
  shows one account's data while signing with another — a genuinely dangerous
  desync.
- No handling for the wallet being locked or uninstalled mid-session.

**Fix.** Every state designed. Cancellation neutral. Subscribe to the wallet's
account- and chain-change events and reconcile. Disconnect that clears both
sides. Show which account is active wherever it matters.

---

## WEB3-C · Mobile connection and deep links

**Check.** On mobile, how does connection work — an in-app browser, a deep link
to a wallet app, a mobile wallet adapter hand-off, or an embedded wallet? Are
the **leaving** and **returning** states designed? What happens if the user
never comes back, or comes back having declined?

**Why it matters.** Mobile connection is a cross-app round trip, and every
unhandled return is a dead end at the moment the user was ready to act. This is
`onboarding-and-flows.md`, FLOW-H with worse consequences.

**Fails like.**
- No state shown while the user is in the wallet app; on return, a spinner that
  never resolves.
- No timeout or recovery when the user doesn't return.
- Returning lands on the home screen instead of the step.
- Enumerating a list of wallet logos on native mobile when the OS actually
  presents the installed wallets — fabricating a list the app can't verify.
- The app's own identity (name, URI, icon) missing or generic, so the wallet's
  approval prompt — **a screen rendered by someone else's app, where the user
  decides whether to trust you** — shows a placeholder.
- Biometric signing demanded on every action rather than offered at setup.

**Fix.** Design leaving, waiting, returning, and failing as real states. Handle
the deep-link round trip with a timeout and a retry. Ship a real app identity —
exact name, real icon. Offer biometrics once at setup.

---

## WEB3-D · Network and chain clarity

**Check.** Is the current network shown, discreetly, where it matters? Is
mainnet unmistakably distinguishable from a testnet or devnet? What happens when
the wallet is on a different network than the app expects? Is a network switch
offered, or does the user have to work it out?

**Why it matters.** Confusing test funds with real ones, or signing on the wrong
network, are both concrete losses. **A devnet/testnet badge is required state,
not decoration** — it's the exception to the "status pills as chrome" rule in
`content-and-copy.md`, COPY-G.

**Fails like.**
- No network indicator at all on a chain-specific product.
- A testnet build visually identical to mainnet.
- Wrong-network producing a raw error or a silently failing transaction rather
  than a clear state with a switch action.
- Network shown by colour alone.
- A multi-chain product where the active chain isn't visible at the moment of
  signing.

**Fix.** Network visible near the account control. Unmistakable, labelled
devnet/testnet marking. Wrong-network as a designed state with a one-tap switch.
Never colour-only.

---

## WEB3-E · Address and identity display

**Check.** How are addresses shown? Is the truncation format the same
everywhere? Is there a one-tap copy with confirmation? Is the full address
reachable and verifiable? Where a human-readable name resolves, is the
underlying address still verifiable for anything that moves value? Is an
identicon or avatar derived deterministically and used consistently?

**Why it matters.** Addresses are unverifiable by reading — the user relies
entirely on the interface to present them consistently and let them check. An
inconsistent truncation makes the same address look like two addresses.

**Fails like.**
- Different truncation lengths on different screens (`7xKX…9fGh` here,
  `7xKXtg2C…` there).
- No copy affordance, so users hand-transcribe.
- Copy with no confirmation.
- Copying the truncated string including the ellipsis.
- A resolved name shown with no way to see the underlying address before a send
  — a name can be spoofed or point somewhere unexpected.
- No warning when a name→address resolution looks unusual or unverified.
- Identicons generated differently in different components, so the same account
  looks different in two places — defeating the entire purpose of a
  deterministic avatar.
- The address in a proportional font, so it jitters or is hard to compare
  character by character.

**Fix.** One truncation format, defined once, used everywhere — middle
truncation preserving both ends, since the ends are what distinguishes.
One-tap copy with explicit feedback. Full address reachable, and linkable to an
explorer for verification. Deterministic avatars from one shared function. Set
addresses in tabular figures (a true monospace only where the full untruncated
value is shown as a block — see `design-system.md`, DS-G).

---

## WEB3-F · Domain marks — tokens, protocols, validators, wallets

**Check.** Wherever the product names an asset or a counterparty, is there a
mark, and does it have a working fallback? Look specifically for empty circles
and broken image slots.

**Why it matters.** These fail the same way every time: **the image never loads
and the UI shows an empty circle.** A staking list of twenty validators as
twenty empty circles is a defect, and it costs trust specifically — the mark is
how a user recognizes who they're delegating to. It's `visual-hierarchy.md`
VIS-J with a trust consequence attached.

**Four categories, four sourcing patterns:**

| Mark | Where it comes from | The failure to check |
|---|---|---|
| **Wallet** | **Already in the bundle** — wallet adapters expose the provider's icon as a base64 data URI. No fetch, no CORS, no broken-image state. | Fetching a logo the app already had. Empty wallet rows almost always mean this. |
| **Token** | A resolution chain: bundled assets for a known set → a token metadata API (cached client-side) → on-chain metadata → **a required letter-avatar fallback**. | No fallback, so unknown or unlisted mints render broken. Re-fetching per render, so lists flicker. Relying on an archived token list, so newer tokens render blank. |
| **Protocol / validator / dApp** | Bundle the finite known set first; on-chain validator identity or a directory for the rest; **a required monogram fallback**. | Not implemented at all — this is the one that gets forgotten. |
| **Network** | A small chain badge, often overlaid on the token mark. | Missing on a multi-chain product, so assets are ambiguous. |

**Fails like.** Empty circles anywhere; a layout shift when an image finally
lands; no skeleton while resolving; a broken-image icon; the same token
rendering differently on two screens.

**Fix.** One component per mark type with a **required** fallback rendered both
on missing-URL and on image `onError`, a skeleton while resolving, and a fixed
size per context so nothing shifts. Cache resolved metadata. Keep the resolution
behind a single function so a provider change is a one-file change — these
endpoints and their free-tier terms move, so a recommendation should say to
verify current provider docs rather than hard-code a URL.

---

## WEB3-G · Amount entry

**Check.** The amount field is the defining input of an onchain product and it
is not a plain number field. Does it show the available balance? Is there a
max affordance, and does it leave headroom for fees? Is a fiat equivalent shown?
Are the token's real decimals respected in value but sanely formatted in
display? Does exceeding the balance produce a clear state?

**Fails like.**
- No balance shown, so the user guesses.
- A MAX that fills the literal balance, leaving nothing for the network fee (or
  for rent, on chains with rent), so the transaction fails after the user
  committed. **This is a concrete, avoidable failure with a real cost.**
- No fiat equivalent, so a mainstream user has no sense of the amount.
- Raw decimals rendered (`0.000000045`).
- Rounding in display that silently changes the value actually submitted.
- Over-balance amounts accepted, failing at signature time rather than at input.
- No decimal keyboard on mobile.
- MAX/HALF chips below the touch minimum.

**Fix.** Balance near the label; max that reserves fee (and rent) headroom; live
fiat equivalent — often the *primary* figure for a mainstream audience; sane
display formatting that never diverges from the submitted value; insufficient
state at input time, with the submit disabled and its reason in its own label.

---

## WEB3-H · The transaction lifecycle

**Check.** Every value-moving action follows the same arc. Walk it and note
which stages exist:

```
Compose → Review (preview + simulation) → Sign → Pending → Resolved (confirmed | failed)
                                                                    ↓
                                                            explorer link
```

**Why it matters.** Missing stages are where users sign things they don't
understand and lose track of things they did.

**Fails like.**
- **Review collapsed into Compose** for an irreversible action — the user signs
  straight from the input screen.
- No pending state; the UI returns to idle while the transaction is in flight.
- A second signature triggerable while one is pending.
- No resolution — success or failure never surfaces, and the user reloads to
  find out.
- Success with no explorer link and no record.
- A confirmation that arrives as a toast which auto-dismisses before it's read.
- Balances not refreshed after a confirmed transaction, so the app shows stale
  state.

**Fix.** Every stage designed. Review is non-skippable for anything
irreversible. Lock the trigger while pending. Resolve explicitly, in place.
Refresh dependent data on confirmation.

---

## WEB3-I · The signature preview

**Check.** The most important screen in an onchain product. Before signing, does
the interface show what the transaction will **do**, in human terms? Can the user
tell what they're approving from this screen alone, without reading a payload?

**Fails like.**
- The preview restates the form inputs instead of the outcome.
- Raw instruction data, base64 payloads, or program IDs shown as the primary
  content — that's the payload, not an explanation.
- No counterparty shown for a send, or one shown truncated with no way to
  verify.
- No warning on a first-time recipient, or on a self-send.
- No simulation where simulation is available — so the preview shows *intent*
  rather than *effect*, and a transaction that would drain an account looks
  identical to one that wouldn't.
- A simulation warning present but styled so quietly it's missed.
- A countdown or urgency device on the confirmation — **never** on a
  money-moving signature (`trust-and-dark-patterns.md`, DARK-A4).
- Scrim-dismiss enabled mid-flight.

**Fix.** Outcome first: what leaves, what arrives, to whom. Counterparty
verifiable. Simulation surfaced as "what changes", with warnings given weight
proportional to risk. Raw details available behind an explicit advanced
disclosure for expert users; never the default view. A dedicated surface —
centred modal on web, sheet on mobile — never an inline expander. No timers.

---

## WEB3-J · Cost clarity

**Check.** Are all costs visible before the commitment, in one place, and can
the user tell what they'll actually end up with? Network fee, priority fee, rent
or account-creation deposits, protocol fees, slippage tolerance, price impact,
and the route's own cost.

**Why it matters.** This is `trust-and-dark-patterns.md` TRUST-D applied to a
domain with more cost components than most, several of which are invisible to a
newcomer. Hidden or late-revealed cost is the finding, regardless of how small
the amount is.

**Fails like.**
- Fees revealed only in the wallet's own prompt, after the user committed in the
  app.
- Priority fees added silently with no disclosure.
- Rent or account-creation deposits unexplained — the user sees a deduction they
  can't account for.
- Slippage tolerance set with no explanation and no warning on unusual values
  (too high risks loss; too low risks failure).
- Price impact not surfaced on a large trade, or surfaced without a warning
  threshold.
- A quoted output that doesn't say it's an estimate.
- No total-cost-of-action figure, so the user has to add it up.
- Fees presented so prominently on a low-fee chain that they read as alarming —
  the opposite failure, and also a finding.

**Fix.** All costs before the commitment, with the **net outcome** stated —
what the user ends up with. Detail behind a disclosure, summary always visible.
Warn on unusual slippage and high price impact with a threshold you can name.
Label estimates as estimates. Proportionate prominence.

---

## WEB3-K · Pending, confirmed, failed

**Check.** During and after submission: is there live status? Does the pending
indicator persist until resolution rather than auto-dismissing? Does it update
**in place** on resolution, or stack a second notification? Is the final state
unambiguous, with the actual final amounts?

**Fails like.**
- A pending toast that auto-dismisses, leaving the user with no status.
- Pending and success as two stacked toasts.
- Success showing the quoted amount rather than the received amount.
- No explorer link on success or failure.
- A raw transaction hash printed inline as body text — **the explorer link is
  the one place a hash belongs**, behind a label, not as visible text.
- No next action after success ("Swap again", "View portfolio").
- Failure with no diagnosis and no retry.
- The triggering control returning to its idle state while the transaction is
  still in flight.

**Fix.** Persistent pending status updated in place. Final amounts on success,
plus an explorer link and a next action. The trigger stays locked until
resolution.

---

## WEB3-L · The onchain error taxonomy

**Check.** Force or trace each failure mode and read what the user is shown.
**Every one of these has a distinct cause, a distinct fix, and should have
distinct copy** — a single generic "Transaction failed" for all of them is the
finding.

| Failure | What actually happened | What the user should be told |
|---|---|---|
| **User rejected** | They declined in the wallet | **Not an error.** Neutral: "Cancelled. Nothing was sent." No red, no alarm. |
| **Insufficient funds** | Balance too low for amount + fees | Which balance, how short, and how to fix — including when it's the *fee* token that's short, not the one being sent |
| **Insufficient funds for rent** | Account-creation/rent minimum unmet | Plain: an account needs a small minimum to exist; here's the amount |
| **Expired blockhash / nonce** | Transaction sat too long before submission | "Took too long to confirm — nothing was sent. Try again." Retry, not a dead end |
| **Slippage exceeded** | Price moved beyond tolerance | "The price moved more than your %. Try again, or raise the tolerance." Offer the adjustment inline |
| **Simulation failure** | The transaction would fail if submitted | Explain what would fail, before spending anything. This is a *save*, present it as one |
| **RPC / network failure** | Couldn't reach the node, or a timeout | Distinguish "not submitted" from "submitted, status unknown" — these have completely different consequences. Offer explorer verification |
| **Program / contract error** | The onchain program rejected it | Translate the known cases; for unknown ones, a plain message plus an explorer link. Never the raw error string |
| **Wrong network** | Wallet on a different chain | A switch action, not a failure message |
| **Wallet locked / disconnected** | Session gone | Re-connect prompt in place, preserving the composed transaction |

**Fails like.** One message for all of them; a raw RPC or program string shown
verbatim; a hex error code; user-rejection styled as a failure; "submitted but
unconfirmed" reported as a definite failure when funds may have moved; no exit
from any error state.

**Fix.** Map each failure to specific copy, written verbatim in the finding.
Every error gets a way forward: retry, adjust, verify, or reconnect. Preserve
the composed transaction across the failure. Soften the wording for a mainstream
audience; a native audience can take precise terms.

---

## WEB3-M · Approvals and delegation

**Check.** Where the product asks for a standing permission — a token approval,
a delegation, a session key, an account authority: does the interface say what
it grants, for how much, for how long, and to whom? Is the default scoped to
what's needed, or unlimited? Can the user see and revoke existing permissions?

**Why it matters.** A standing approval is the mechanism behind most onchain
losses. A user who doesn't understand what they granted can't manage the risk,
and one who can't find their existing approvals can't reduce it.

**Fails like.**
- "Approve" with a raw allowance number and no explanation.
- Unlimited approval as the silent default.
- No indication that the permission persists after the current action.
- No screen listing existing approvals, so the user can't audit their own
  exposure.
- Revocation available but hard to find, or requiring a separate tool.
- Revoke styled as a routine action rather than a deliberate one.
- A delegation whose expiry isn't stated.

**Fix.** Plain language: "This lets [app] move up to X of your USDC, until you
revoke it." Scoped by default; unlimited as an explicit, explained opt-in. A
permissions screen listing what's granted, to whom, and how much, with revoke
per item. State expiry where one exists.

---

## WEB3-N · Security posture

**Check.** Does the product ever request a seed phrase or private key? Is the
domain verifiable? Does the interface teach safe habits or unsafe ones? Is
custody clear — who holds the keys? Is irreversibility signalled before the act?

**Why it matters.** Onchain interfaces train user behaviour that carries across
the whole ecosystem. A product that asks for a seed phrase for any reason —
including a legitimate import — normalizes the exact behaviour every phishing
attack relies on.

**Fails like.**
- **Any request for a seed phrase or private key.** A wallet import is the only
  defensible case, and it needs explicit framing, an offline-capable path, and
  strong warnings. Anything else is a Blocker.
- No indication of custody — the user can't tell whether the product holds their
  keys, an embedded-wallet provider does, or they do.
- No domain verification cue on a product routinely targeted by lookalike
  domains.
- Support routes inside the product that could be impersonated (an open comment
  field, an unmoderated chat link) with no warning that support never DMs first.
- Recovery mechanics unexplained on an embedded wallet — the user doesn't know
  what happens if they lose access.
- Irreversibility unstated before a send (`trust-and-dark-patterns.md`, TRUST-C).
- Transaction simulation available but its warnings rendered as quiet
  informational text.
- Trust signals that can't be verified — an "audited" badge with no link to the
  report.

**Fix.** Never request a seed phrase outside an explicit import. State custody
plainly. Signal irreversibility before the commit. Give simulation warnings
weight proportional to risk. Make trust claims verifiable — link the audit,
name the auditor.

---

## WEB3-O · On/off-ramp and KYC friction

**Check.** If the product includes fiat on/off-ramps: when is KYC demanded, and
is that timing disclosed before the user starts? Are the fees and the exchange
rate visible before commitment? What are the failure and rejection states? Are
limits and expected timings stated?

**Why it matters.** A ramp is a hand-off to a third party with the most
demanding requirements in the flow, and it usually arrives after the user has
already invested effort.

**Fails like.**
- KYC requirements discovered mid-flow, after account creation.
- The third-party provider's UI arriving with no warning and no branding
  continuity, so it reads as a phishing redirect.
- The exchange rate and spread not shown, or shown only after commitment.
- No status while a transfer settles, which can take days.
- A rejected KYC with no explanation and no appeal route.
- Region or limit restrictions surfaced only on failure.
- No route back into the product after the provider's flow completes.

**Fix.** Disclose KYC, limits, region restrictions, fees, and expected timing
**before** the user begins. Warn before handing off, and design the return.
Status for in-flight settlements. A path forward on rejection.

---

## WEB3-P · Wording calibration

**Check.** Does the vocabulary match the audience (§0f), consistently across
every screen? This is `content-and-copy.md` COPY-A applied to a domain with an
unusually large jargon surface.

| Concept | Crypto-native | Mainstream |
|---|---|---|
| Entry | "Connect wallet" | "Sign in" / "Get started" — wallet path still present, discreet |
| Signing | "Sign", "Approve" | "Confirm", with what's being confirmed |
| Fee | "Network fee", priority fee named | "Network fee ≈ $0.002", mechanism behind a disclosure |
| Outcome | "You pay 0.5 SOL → receive ≈ 120 USDC" | Lead with the outcome and the fiat value |
| Insufficient fee token | "Insufficient SOL for fees" | "You need a little more [token] to cover the network fee" |
| Network | Shown by default | Hidden unless it matters |
| Address | Truncated address is fine as identity | A resolved name or label, address on demand |
| Approvals | "Approve", allowance shown | "Allow [app] to move up to X" |

**Fails like.** Native jargon throughout a product aimed at newcomers;
patronising simplification in a product for traders; **mixed registers** —
"Connect wallet" next to "Get started" next to "Sign in" for the same action;
translation applied to the buttons but not to the errors, which is where it
matters most; over-translation that removes precision an expert needs.

**Fix.** Decide once, apply everywhere. Mixed audiences get mainstream wording
with the native term available on disclosure. Where the product genuinely serves
natives, don't dumb it down — that's its own finding.

---

## WEB3-Q · Onchain data display

Additions to `data-display.md` specific to this domain:

**Check.** Token amounts formatted per the token's real decimals but displayed
sanely. Fiat equivalents present where they aid understanding. Value change
shown with a **sign and colour**, using directional data colours rather than
status success/error — so a red price candle and a green success toast can share
a screen without collision. Balances refreshed after every confirmed
transaction. Prices throttled so they don't vibrate.

**Fails like.** Raw decimals; a balance that doesn't update after a confirmed
transaction; prices flickering on every tick; P&L by colour alone; chart
positive/negative reusing the status palette; a "● Live" indicator on data that
barely changes; portfolio value shown as one tile in a grid of equals when it's
the number the user opened the app to see (`visual-hierarchy.md`, VIS-A).

**Fix.** Sane display formatting; refresh on confirmation; throttled updates
with a smooth transition; sign plus colour plus a distinct directional palette;
the portfolio's total value leading its screen by position and size.

---

## WEB3-R · Activity and transaction-type iconography

**Check.** Does the activity feed distinguish transaction types by their own
glyphs, or reuse one generic mark (or a coloured dot) for everything? Is each
type's icon the same wherever that type appears — feed, detail, filters, action
buttons?

**Why it matters.** With one glyph for everything, the user must read every
label to tell a deposit from a swap. It's the difference between scanning and
reading, on the screen users check most often.

**Types worth distinguishing:** receive/deposit · send/withdraw · swap/trade ·
stake/delegate · unstake/claim · approve/revoke · mint/burn.

**Fails like.**
- One glyph or a coloured dot for every type.
- **Send and receive sharing a glyph rotated by chance** — the most confused
  pair; make them visually unmistakable.
- Direction inverted between screens (down means "in" on one, "out" on another).
- Type encoded by colour alone.
- The type icon and the status (pending/failed) collapsed into one ambiguous
  mark — the type says *what*, the status says *how it went*.
- Icons drawn from a mix of a library and hand-made SVGs.

**Fix.** One distinct glyph per type, defined once in a single lookup keyed by
transaction type so the feed, the detail view, the filters, and the buttons
can't drift. One family, one weight. Direction consistent app-wide. Status as a
separate, additional signal.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Seed phrase or private key requested outside an explicit wallet import | **Blocker** |
| A signature can be given without any human-readable preview of what it does | **Blocker** |
| Unlimited approval granted as a silent default | **Blocker** |
| Account/wallet desync — displayed account differs from the signing account | **Blocker** |
| MAX that leaves no fee headroom, so the transaction fails after commitment | **Blocker** |
| Costs disclosed only after the commitment point | **Blocker** |
| Whole app gated behind wallet connection before anything is shown | **High** |
| Mainstream product with no wallet path at all | **High** |
| Mainnet and testnet visually indistinguishable | **High** |
| One generic message for all onchain failures; raw RPC/program strings shown | **High** |
| "Submitted but unconfirmed" reported as a definite failure | **High** |
| No existing-approvals screen and no revocation route | **High** |
| Mobile connection round trip with no return handling | **High** |
| User rejection styled as an error | **Medium** |
| Empty circles where token, protocol, or validator marks belong | **Medium** |
| Inconsistent address truncation across screens | **Medium** |
| Pending status auto-dismissing before resolution | **Medium** |
| Raw hash shown inline as text | **Medium** |
| Wallet-select surface built as a header dropdown (clipped scrim) | **Medium** — S effort |
| Balances not refreshed after a confirmed transaction | **Medium** |
| One generic glyph for every transaction type | **Medium** |
| Wording register mixed across screens | **Medium** |
| Fees shown prominently enough to alarm on a low-fee chain | **Low** |
