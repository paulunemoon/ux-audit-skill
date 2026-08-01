# D15 · Trust, safety & privacy — D16 · Dark patterns

> **When to read:** Any product that handles money, personal data, identity,
> health, children, or anything irreversible — and any product with a
> subscription, a consent flow, or a growth team. Finding IDs: `TRUST-nn` and
> `DARK-nn`.
>
> These two dimensions sit together because they're the same question from
> opposite ends: **does the interface act in the user's interest when the
> business would benefit from it not doing so?**

## Table of contents
- [D15 · Trust, safety & privacy](#d15--trust-safety--privacy)
  - [TRUST-A · Data collection clarity](#trust-a--data-collection-clarity)
  - [TRUST-B · Consent](#trust-b--consent)
  - [TRUST-C · Irreversibility signalling](#trust-c--irreversibility-signalling)
  - [TRUST-D · Cost and commitment transparency](#trust-d--cost-and-commitment-transparency)
  - [TRUST-E · Verifiability](#trust-e--verifiability)
  - [TRUST-F · Warning discipline](#trust-f--warning-discipline)
  - [TRUST-G · Account security surfaces](#trust-g--account-security-surfaces)
  - [TRUST-H · Sharing, visibility, and audience](#trust-h--sharing-visibility-and-audience)
  - [TRUST-I · Data export and deletion](#trust-i--data-export-and-deletion)
  - [TRUST-J · Signals of unfinishedness](#trust-j--signals-of-unfinishedness)
- [D16 · Dark patterns](#d16--dark-patterns)
  - [The register](#the-register)
  - [DARK-A · Judging intent — and why you mostly shouldn't](#dark-a--judging-intent--and-why-you-mostly-shouldnt)
- [Severity calibration](#severity-calibration-for-this-file)

---

# D15 · Trust, safety & privacy

## TRUST-A · Data collection clarity

**Check.** At each point the product collects something: does the user know
what's being collected, why, and what happens to it? Are optional fields
distinguishable from required ones? Does the product collect anything the user
would be surprised by — location, contacts, device identifiers, analytics,
session recording, a third-party pixel?

**Why it matters.** Surprise is the mechanism by which trust is lost. A
collection the user would have accepted if asked becomes a betrayal when
discovered.

**Fails like.**
- Permissions requested with no stated purpose (see `onboarding-and-flows.md`,
  ONB-C).
- A privacy policy that describes less than what's actually collected.
- Third-party trackers with no disclosure.
- A field whose purpose is unguessable and unexplained ("Why do you need my date
  of birth?").
- Data collected "to improve your experience" with no specifics.
- Session recording or heatmapping with no notice.

**Fix.** State the purpose at the point of collection, in one line, in the
user's terms. Mark optional fields as optional. Disclose third parties. Where
the policy and the practice diverge, that's the finding — and it's a legal
exposure, not just a UX one.

---

## TRUST-B · Consent

**Check.** Is consent freely given — is refusing as easy as accepting? Are
consents granular, or bundled? Is anything pre-checked? Can consent be withdrawn
as easily as it was given, and is the withdrawal route discoverable?

**Why it matters.** Consent obtained through friction asymmetry isn't consent,
and in several jurisdictions it isn't legally valid either. This is the single
most common dark pattern in production software.

**Fails like.**
- "Accept all" as a prominent button, "Manage preferences" as a small grey link
  leading to a multi-step panel where everything must be toggled off
  individually.
- No "Reject all" at the same level as "Accept all".
- Pre-ticked marketing and data-sharing boxes.
- Consent bundled with terms acceptance, so the user can't take one without the
  other.
- A cookie banner that reappears every visit because refusal isn't stored.
- Withdrawal requiring an email to support.
- Consent language written to be uninterpretable.

**Fix.** Symmetric options at the same visual weight and the same number of
clicks. Granular toggles, all default off. Persist refusal. A visible route to
change the decision later. **Asymmetry here is a High finding on its own** —
it doesn't need a legal argument to be a UX defect.

---

## TRUST-C · Irreversibility signalling

**Check.** Before anything irreversible: does the interface say so, *before* the
commit, in language the user will register? Is the friction proportional to the
consequence? Is the destructive option ever the path of least resistance?

**Why it matters.** The user's model of reversibility comes entirely from the
interface. If it doesn't say "this is permanent", they'll assume it isn't.

**Fails like.**
- "This cannot be undone" appearing only in the success message.
- Permanent deletion behind the same single click as a reversible archive.
- The destructive button pre-focused, so `Enter` fires it.
- A confirmation naming neither the object nor the consequence.
- Account deletion that also deletes other people's data, unmentioned.
- A publish or send action with no distinction from a save.

**Fix.** State permanence before the act, in the confirmation. Friction
proportional to consequence — typing the name for the catastrophic, a plain
confirm for the merely irreversible, undo instead of a dialog for the
recoverable. Never pre-focus the destructive option. See
`feedback-and-states.md`, ERR-A.

---

## TRUST-D · Cost and commitment transparency

**Check.** Is the total cost visible before the commitment point, including
fees, taxes, shipping, and any recurring component? Is the renewal date, the
renewal price, and the cancellation route stated before purchase? Does a free
trial say what happens at the end, and when?

**Why it matters.** Late-revealed cost is the highest-abandonment moment in
commerce and the most-complained-about pattern in subscriptions. It is also
increasingly regulated.

**Fails like.**
- Fees appearing only on the final step.
- "From $9" where nobody pays $9.
- A trial that converts to an annual plan, with the term shown only in the
  terms.
- Renewal price differing from the introductory price, disclosed in small grey
  text.
- No cancellation route in the account settings.
- A price shown per month and billed annually with no clear indication.
- Currency conversion applied at an undisclosed rate.

**Fix.** Total cost, including everything, at the earliest point it's
computable. Renewal terms — date, amount, cadence — stated at purchase and
visible in the account. Cancellation reachable in the same product where signup
happened, in a comparable number of steps.

---

## TRUST-E · Verifiability

**Check.** Can the user confirm what they're agreeing to, from what's on
screen? Is the recipient, the amount, the object, and the scope visible at the
moment of commitment? Is there a durable record afterwards — a receipt, a
confirmation number, an email, an activity log?

**Why it matters.** A user asked to confirm something they can't verify is
being asked to trust, not to decide.

**Fails like.**
- A confirmation showing a total with no line items.
- A recipient shown truncated with no way to see the full value.
- An action affecting "12 items" with no way to see which twelve.
- No record after a completed transaction.
- An activity log that omits security-relevant events (logins, permission
  changes, exports).
- A claim in the interface (a metric, a certification, a guarantee) with no way
  to check it.

**Fix.** Show the full particulars at the commitment point, or make them one
interaction away. Issue a durable record with a reference. Log
security-relevant events where the user can see them.

---

## TRUST-F · Warning discipline

**Check.** How many warnings does the product show in normal use? Are they
reserved for genuine risk, or fired on routine actions? Is the visual weight
proportional to the risk — is everything red?

**Why it matters.** Over-warning is a safety failure with the opposite shape to
under-warning: users learn to dismiss without reading, so the one warning that
mattered gets dismissed too.

**Fails like.**
- A confirmation dialog on every save.
- Red error styling for informational messages.
- A warning on an action the user performs twenty times a day, with no way to
  suppress it.
- Multiple stacked warnings on one screen, none of which is more urgent-looking
  than the others.
- The same treatment for "this will notify 200 people" and "this field is
  optional".

**Fix.** Three tiers with distinct treatments: informational, caution (proceed
knowingly), blocking (genuine risk). Suppressible for routine reversible
actions. Reserve the strongest treatment for the smallest number of cases.

---

## TRUST-G · Account security surfaces

**Check.** Is there a visible route to change a password, enable two-factor,
review active sessions, and see recent security events? Are password
requirements stated up front rather than on rejection? Is the login flow free of
patterns that train unsafe behaviour?

**Fails like.**
- No MFA option on a product holding money or personal data.
- No session list and no way to sign out other devices.
- Password rules revealed only on failure.
- Paste blocked in password fields, which defeats password managers.
- No notification on a password change, a new device login, or an email change.
- A "security question" flow as the only recovery route.
- Any flow that asks the user for a credential a legitimate product would never
  request — training users to hand credentials to whoever asks.

**Fix.** Standard security surfaces present and findable. Requirements stated
before input. Never block paste. Notify on security-relevant changes through a
channel the attacker doesn't control.

---

## TRUST-H · Sharing, visibility, and audience

**Check.** Where content can be shared or made visible to others: is the current
audience unambiguous *before* posting? Is the default private or the narrowest
sensible scope? Is a visibility change confirmed?

**Why it matters.** Audience mistakes are unrecoverable in the way that matters
— you can delete the post, not the fact that it was seen.

**Fails like.**
- Default visibility set to public or organization-wide with no prominent
  indicator.
- A share link that's actually public to anyone with the URL, described as
  "share with your team".
- Visibility shown only as an icon with no label.
- Changing a folder's visibility silently changing every item inside it.
- No way to see who currently has access.

**Fix.** Current audience stated in words at the point of publishing. Narrowest
sensible default. Explicit confirmation when widening access, naming who gains
it. A visible access list.

---

## TRUST-I · Data export and deletion

**Check.** Can the user get their data out, in a usable format, without
contacting support? Can they delete their account, and is what deletion actually
does stated? Is the deletion route in the product, or hidden behind an email?

**Why it matters.** Export and deletion are the concrete test of whether the
product treats data as the user's. They're also legally required in several
jurisdictions.

**Fails like.**
- No export at all.
- Export in a format nobody can use, or one that omits the substance.
- Account deletion only by emailing support.
- "Delete account" that deactivates instead, with no explanation.
- No statement of what's retained after deletion and for how long.
- A deletion flow with more retention offers than steps.

**Fix.** Self-serve export in an open format. Self-serve deletion, with a plain
statement of what's deleted, what's retained, for how long, and why. One
retention offer at most.

---

## TRUST-J · Signals of unfinishedness

**Check.** Broken links, placeholder text, missing legal pages, a default
favicon, broken images, empty logo slots, `Lorem ipsum`, a "Beta" badge on a
mature product, a copyright year years out of date.

**Why it matters.** These aren't cosmetic on a trust-sensitive product. Users
generalize from small visible failures to invisible ones: if nobody checked the
footer links, who checked the encryption? On a product handling money or
personal data, this is a real conversion and trust cost, not a nitpick.

**Fails like.** Any of the above, plus: a support email that bounces; a status
page that hasn't been updated in a year; a changelog that stops eighteen months
ago; a blank browser tab icon next to a logo in the header.

**Fix.** List them. They're almost always S-effort and they belong in Quick
wins. Generate the favicon from the same mark as the logo — a logo in the header
with a default tab icon is a recurring and entirely avoidable version of this.

---

# D16 · Dark patterns

## The register

For each pattern: what it looks like, what it costs the user, and what the
honest version is. **A pattern is only a finding when you can point at where it
occurs** — not because the category exists.

### DARK-A1 · Forced continuity
**Looks like.** A free trial requiring payment details, converting silently;
auto-renewal with no reminder; cancellation harder than signup (more steps, a
phone call, an email, a retention gauntlet, business-hours-only).
**Costs.** Money the user didn't intend to spend, and the discovery arrives as
a charge.
**Honest version.** Reminder before renewal. Cancellation in the same product,
in comparable effort to signup. One retention offer, skippable.

### DARK-A2 · Confirmshaming
**Looks like.** A decline option worded to shame — "No thanks, I don't want to
save money", "I prefer to stay disorganized".
**Costs.** Nothing material; it's a small hostile act that reliably annoys, and
it reads as manipulation, which colours everything else.
**Honest version.** "No thanks." Neutral, same visual weight as accept.

### DARK-A3 · Hidden costs / drip pricing
**Looks like.** Fees, taxes, shipping, service charges appearing only at the
last step; a "from" price nobody pays; a mandatory add-on presented as optional
until checkout.
**Costs.** A wasted flow, and a purchase made under a misapprehension.
**Honest version.** Total cost as early as it's computable. Where it genuinely
can't be known upfront, state that and give a range.

### DARK-A4 · Manufactured urgency and scarcity
**Looks like.** Countdown timers that reset; "3 people are viewing this"; "only
2 left" that's always 2; a discount that never expires but always says it's
about to.
**Costs.** Decisions made under false pressure, which produce regret and
returns.
**Honest version.** Real deadlines and real stock counts, or nothing. **Any
urgency device on an irreversible or money-moving action is a finding
regardless** — never rush a commitment.

### DARK-A5 · Misdirection and false hierarchy
**Looks like.** The option the business prefers styled as primary and the user's
likely intent as a faint text link; a pre-selected upsell; a "recommended" plan
that's just the expensive one; the decline option below the fold.
**Costs.** Choices made by visual default rather than intent.
**Honest version.** Visual weight follows the user's likely intent, or is
neutral between real alternatives. Nothing pre-selected that costs money.

### DARK-A6 · Roach motel
**Looks like.** Easy in, hard out — an account created in one click and deleted
by emailing support; a subscription started online and cancelled by phone; data
imported instantly and exported never.
**Costs.** Lock-in by friction rather than by value.
**Honest version.** Symmetry. If it took one screen to start, it takes one
screen to stop.

### DARK-A7 · Privacy zuckering
**Looks like.** Consent bundled with terms; defaults set to maximum sharing;
privacy settings scattered across pages; a "personalization" toggle that's
actually tracking; granular controls that only granularly *reduce*.
**Costs.** Data shared the user didn't intend to share.
**Honest version.** Granular, default-off, in one place, described accurately.
See TRUST-B.

### DARK-A8 · Nagging
**Looks like.** Repeated prompts for the same permission, review, upgrade, or
app install; a dismissal that lasts one session; an interstitial on every visit.
**Costs.** Interruption tax on every session, and eventual blindness to all
prompts including useful ones.
**Honest version.** Ask once, respect the answer, ask again only after
something changed. "Don't show again" that works.

### DARK-A9 · Trick questions and inverted controls
**Looks like.** "Untick if you do not wish to not receive emails"; consent
checkboxes with inverted polarity next to each other; an opt-out styled as an
opt-in.
**Costs.** The user does the opposite of what they intended.
**Honest version.** Positive phrasing, consistent polarity, unambiguous labels.

### DARK-A10 · Bait and switch / forced action
**Looks like.** A control that does something other than what it says; an X that
opens the thing instead of closing it; a required action inserted into an
unrelated flow ("verify your phone to continue reading").
**Costs.** Loss of the basic contract that controls do what they're labelled to
do — the most corrosive of the set.
**Honest version.** Controls do what they say. Requirements appear where
they're relevant.

### DARK-A11 · Obstruction of comparison
**Looks like.** Pricing pages where plans can't be compared side by side;
different units per plan; feature lists in different orders; the real limits
only in a footnote.
**Costs.** A choice the user can't make well.
**Honest version.** Same features, same order, same units, one table.

---

## DARK-A · Judging intent — and why you mostly shouldn't

You're auditing **effect**, not motive. Most of these patterns arrive through
accretion — a growth experiment, a legal review, a form that grew — rather than
malice, and an audit that reads as an accusation gets dismissed along with its
findings.

**How to write a dark-pattern finding:**
- Describe **what the interface does** and **what it costs the user**. Don't
  assert intent.
- Where the pattern plausibly serves a legitimate purpose, say so and audit the
  execution — a countdown on a genuinely time-limited offer is legitimate; the
  finding is whether the deadline is real and whether it appears on an
  irreversible action.
- Where the asymmetry is stark and structural (accept-all versus a six-click
  refusal), the effect speaks for itself and doesn't need intent attached.
- **Flag the regulatory exposure where it exists** — consent symmetry,
  subscription cancellation, and drip pricing are legislated in multiple
  jurisdictions. State it as a factor the team should check with counsel, not as
  a legal opinion.

**Do not manufacture findings here.** A product with no dark patterns should get
a one-line "none found" and nothing more. Padding this dimension is how an audit
loses credibility on every other one.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Irreversible action with no permanence signalling before the commit | **Blocker** |
| A control that does something other than what it says | **Blocker** |
| Cost or commitment concealed until after the point of no return | **Blocker** |
| Content published to a wider audience than the user intended, by default | **Blocker** |
| Consent asymmetry (accept-all vs multi-step refusal), or pre-ticked consent | **High** |
| No self-serve cancellation where signup was self-serve | **High** |
| Manufactured urgency on a money-moving or irreversible action | **High** |
| Missing Terms/Privacy on a product collecting personal data | **High** |
| No MFA, no session management on a product holding money or personal data | **High** |
| Paste blocked in password fields | **High** |
| No data export or self-serve deletion | **High** where required by law; else **Medium** |
| Over-warning that trains dismissal | **Medium** |
| Nagging prompts with no durable dismissal | **Medium** |
| Confirmshaming | **Medium** |
| Unfinishedness signals (dead links, placeholder text, default favicon) | **Medium** on a trust-sensitive product; **Low** otherwise |
| Obstruction of plan comparison | **Medium** |
