# D4 · Input & forms

> **When to read:** Any screen that collects input — signup, checkout, settings,
> search, filters, composers, uploads. Forms are where the most measurable
> abandonment happens and where fixes are cheapest, so this dimension usually
> produces the best quick wins in an audit. Finding IDs: `FORM-nn`.
>
> Field-level accessibility (label association, error announcement, focus
> management) is cross-referenced here but specified in `accessibility.md`.

## Table of contents
1. [FORM-A · Field count and necessity](#form-a--field-count-and-necessity)
2. [FORM-B · Labels](#form-b--labels)
3. [FORM-C · Validation timing](#form-c--validation-timing)
4. [FORM-D · Error messages](#form-d--error-messages)
5. [FORM-E · Required, optional, and disabled](#form-e--required-optional-and-disabled)
6. [FORM-F · Input types, keyboards, and autofill](#form-f--input-types-keyboards-and-autofill)
7. [FORM-G · Paste, format, and forgiving input](#form-g--paste-format-and-forgiving-input)
8. [FORM-H · Keyboard flow and submission](#form-h--keyboard-flow-and-submission)
9. [FORM-I · Control states](#form-i--control-states)
10. [FORM-J · Choosing the right control](#form-j--choosing-the-right-control)
11. [FORM-K · Long forms, progress, and loss](#form-k--long-forms-progress-and-loss)
12. [FORM-L · Submission and its aftermath](#form-l--submission-and-its-aftermath)
13. [FORM-M · Uploads](#form-m--uploads)
14. [Severity calibration](#severity-calibration-for-this-file)

---

## FORM-A · Field count and necessity

**Check.** Count the fields. For each one ask: does the product need this *now*,
does it already know it, could it derive it, and what happens if it's wrong or
absent? Then count the **required** ones separately — that's the real cost.

**Why it matters.** Field count is the most reliable predictor of abandonment in
any form, and most forms carry fields that exist because someone once asked for
the data, not because the task needs it.

**Fails like.**
- Signup collecting company, role, team size, and phone before the product has
  delivered anything.
- Separate first-name/last-name/middle-initial where one full-name field works.
- Address entered as five fields with no lookup.
- Asking for data the account already holds.
- A "how did you hear about us?" required field.
- Confirm-email and confirm-password fields (they increase typos more than they
  catch them, when the field is unmaskable and validated).

**Fix.** List the specific fields to cut, defer to a later moment, or make
optional, and say what each removal buys. Where a field is legally or
operationally required, name the constraint and audit its execution instead.

---

## FORM-B · Labels

**Check.** Every field has a visible, persistent label. Not a placeholder
standing in for one. Not a label that disappears on focus with no replacement.
The label describes what to enter, not the database column.

**Why it matters.** A placeholder-as-label vanishes the moment the user types,
so anyone who is interrupted, reviewing, or correcting a mistake is left with a
filled field and no idea what it's for. It also fails screen readers and
autofill, and it usually fails contrast.

**Fails like.**
- Placeholder-only fields.
- Floating labels that shrink to an illegible size or contrast on focus.
- A label whose meaning depends on a heading three fields above it.
- Internal vocabulary as labels ("Entity ID", "Principal", "SKU-2").
- Helper text that answers a different question than the field asks.
- Units missing from a numeric field (kg? lb? per month? including tax?).

**Fix.** Persistent visible label above or beside the field, programmatically
associated. Placeholders reserved for *example* input, never instructions.
Helper text below the field, before the user types, when a format or a
constraint applies — not only as an error afterwards.

---

## FORM-C · Validation timing

**Check.** When does each field validate — on every keystroke, on blur, on
submit? Does a half-typed entry get marked wrong? Does a field that's now
correct clear its error immediately? Does submit ever fail with no visible
reason?

**Why it matters.** Validating too early accuses the user of a mistake they're
in the middle of not making; validating too late lets them fill a whole form
before learning the second field was wrong.

**Fails like.**
- An email field showing "Invalid email" after the first character.
- A password field showing every unmet rule in red before typing starts.
- Errors appearing only after submit, with the page scrolled to the top and no
  indication which field failed.
- An error that persists after the user fixes the field, until they submit
  again.
- Server-side-only validation of something checkable client-side, so every
  mistake costs a round trip.
- Silent submit failure — the button does nothing and nothing explains why.

**Fix.** The pattern that works: **validate format on blur, re-validate on
change once a field has already errored, validate cross-field rules on submit.**
Live validation is right for constraints the user is actively working against
(password strength, character count, an amount against a balance). On submit
failure, move focus to the first invalid field and summarize the errors at the
top with links to each.

---

## FORM-D · Error messages

**Check.** Read every error message the form can produce. Does each say what
happened, and what to do about it, in plain language? Is the message attached to
the field it concerns? Is it ever a raw code or a stack trace?

**Why it matters.** An error is the only moment the interface is definitely
being read closely. A message that doesn't tell the user how to proceed converts
a recoverable state into abandonment.

**Fails like.**
- `ERR_VALIDATION_FAILED`, `400 Bad Request`, an exception string, a raw
  provider error surfaced verbatim.
- "Invalid input" — which input, invalid how?
- "Something went wrong" as the entire message, with no retry.
- Blaming the user ("You entered an invalid value").
- A rule revealed only on failure ("Password must contain a symbol") that could
  have been shown up front.
- One generic banner at the top for a form with eight fields.
- Error indicated by a red border alone, with no message (also a D12 failure).

**Fix.** Write the replacement copy verbatim in the finding — this is a place
where "improve the error copy" is worthless and a rewrite is worth its weight.
The shape: what happened · why · what to do. "That email is already registered.
Sign in instead, or use a different address." One message per field, directly
beneath it, with the field marked by more than color.

---

## FORM-E · Required, optional, and disabled

**Check.** Is required-vs-optional marked, consistently, in one direction? (Mark
the minority — if most fields are required, mark the optional ones.) When a
submit button is disabled, does the interface say why? Is anything disabled with
no explanation anywhere on screen?

**Why it matters.** A disabled button with no reason is a dead end that looks
like the product's fault, and users blame the product rather than looking for
the unfilled field.

**Fails like.**
- Asterisks on some required fields and not others.
- Everything marked required, including the optional ones.
- A greyed-out submit with no hint — the user must guess which field is
  incomplete.
- A disabled control whose tooltip is the only explanation, on a touch device.
- Disabled styling at a contrast so low it reads as decoration rather than a
  control.

**Fix.** Mark the minority case, once, consistently. **A disabled primary action
states its reason in its own label** ("Enter an amount", "Select a date",
"Accept the terms to continue") or in adjacent visible text — never a bare grey
button. Better still, keep the button enabled and validate on press, so the
error is explicit rather than mysterious.

---

## FORM-F · Input types, keyboards, and autofill

**Check.** Does each field use the right input type and `inputmode`, so mobile
shows the right keyboard? Are `autocomplete` tokens present and correct
(`email`, `given-name`, `street-address`, `one-time-code`, `cc-number`,
`new-password`, `current-password`)? Does the browser/OS password manager work
on the login and signup forms?

**Why it matters.** This is the highest-leverage, lowest-effort category in the
whole dimension. Correct autofill removes most of the typing from most forms; a
wrong keyboard adds a mis-tap to every character on mobile.

**Fails like.**
- A phone or amount field showing the full alphabetic keyboard.
- No `autocomplete` attributes anywhere, or `autocomplete="off"` on fields users
  want filled.
- A one-time-code field that doesn't accept the OS-suggested SMS code.
- A custom-built select or card input that password managers and autofill can't
  see.
- Address fields in an order or naming that defeats autofill.
- `autocapitalize` and autocorrect left on for case-sensitive fields
  (usernames, codes, identifiers, addresses) — a mobile-specific defect that
  silently corrupts input.
- Password fields with paste disabled.

**Fix.** Correct `type` + `inputmode` + `autocomplete` per field; this is
usually a one-line change each and belongs in Quick wins. Disable autocorrect,
autocapitalize, and spellcheck on exact-match fields. Never block paste.

---

## FORM-G · Paste, format, and forgiving input

**Check.** Paste realistic messy values into every field: a phone number with
spaces and a country code, a card number with spaces, an email with a trailing
space, a date in a different format, an amount with a currency symbol or a comma
decimal separator. Does the field accept and normalize, or reject?

**Why it matters.** The value the user has is the value they have. Rejecting a
format the system could trivially normalize makes the user do the computer's
job, and it's the source of a large share of "invalid input" errors.

**Fails like.**
- Rejecting a pasted card number because it contains spaces.
- Rejecting `+33 6 12 34 56 78` for a phone.
- A date field that accepts only `MM/DD/YYYY` with no picker and no hint.
- Trailing whitespace from a paste causing an "account not found".
- A comma decimal separator rejected in a locale that uses it.
- A field with a strict format and no example of that format.
- Auto-formatting that fights the user — reformatting mid-typing so the caret
  jumps.

**Fix.** Trim, strip separators, and normalize on input; validate the normalized
value. Show the expected format as helper text or a placeholder example before
the error. Where a format is genuinely rigid, provide a picker or a mask that
doesn't move the caret unexpectedly.

---

## FORM-H · Keyboard flow and submission

**Check.** Tab through the form top to bottom. Is the order the visual order?
Does every control receive focus with a visible indicator? Does `Enter` submit
from a single-line field? Do custom controls (comboboxes, date pickers, toggles,
multi-selects) work by keyboard at all?

**Why it matters.** Keyboard flow is how fast users and all keyboard-dependent
users complete forms. It's also the cheapest thing to break with a custom
control and the least likely to be noticed by a mouse-using team.

**Fails like.**
- Tab order jumping around because of DOM order versus CSS order.
- Positive `tabindex` values scattered through the form.
- A custom select that opens on click but not on `Enter`/`Space`/arrows.
- A date picker with no typed-input alternative.
- `Enter` doing nothing, or triggering the wrong button (a secondary action, or
  a "remove" icon that happens to be first in the DOM).
- Focus lost to `<body>` after an inline field is added or removed.
- A modal form that doesn't trap focus, or doesn't return focus on close.

**Fix.** DOM order matches visual order; no positive `tabindex`. Native controls
where possible; ARIA-pattern-complete controls where not. `Enter` submits.
Explicit focus management around dynamic fields and dialogs. Details in
`accessibility.md`.

---

## FORM-I · Control states

**Check.** Each interactive control should have a complete, distinguishable set:
**default · hover (pointer) · focus · filled · disabled · error**, plus
**loading** on anything async. Missing or indistinguishable states are the
defect, whatever the styling.

**Why it matters.** States are how the interface answers "did that work?" and
"can I use this?" Missing focus is an accessibility failure; missing loading
produces double-submits; indistinguishable disabled produces repeated dead
clicks.

**Fails like.**
- Focus ring removed globally (`outline: none`) with nothing replacing it.
- Hover and focus rendered identically, so keyboard users can't see where they
  are.
- Disabled and read-only styled the same, so the user can't tell which is which.
- A submit button with no loading state — pressing twice creates two records.
- A loading state that replaces the label with a bare spinner, so the button's
  meaning disappears and the row reflows.
- Error state carried by border color only.
- A control whose pressed/active state is invisible on touch, where there's no
  hover to fall back on.

**Fix.** Define and ship the full set. On loading: keep the label ("Saving…"),
reserve the width so nothing shifts, and make the control non-interactive to
prevent double-submit. Never remove focus indication — restyle it.

---

## FORM-J · Choosing the right control

**Check.** Does each control match its data? Small fixed set of options that
should stay visible → radios or a segmented control. Longer known list →
select. Long searchable list → a searchable combobox with a filter. Binary
setting applied immediately → toggle. Binary agreement submitted with a form →
checkbox. Free text → input, sized to its content.

**Why it matters.** The wrong control adds interaction cost on every use and
often hides options entirely.

**Fails like.**
- A dropdown for two or three options.
- A plain select with 200 unsearchable entries.
- A toggle that requires a separate Save (toggles imply immediate effect).
- Checkboxes where the choices are mutually exclusive.
- A multi-line textarea for a single-line value.
- A slider for a value that needs precision, with no numeric entry.
- Country/currency pickers with no search and no recents.
- Custom-built replacements for native mobile pickers, which lose the OS
  behavior users expect.

**Fix.** Name the control swap per field. On mobile, prefer native pickers and
sheet-based selection over hover-dependent menus.

---

## FORM-K · Long forms, progress, and loss

**Check.** For anything over one screen: is progress shown and honest? Is
partial input saved? What happens on navigate-away, back, refresh, session
timeout, or a validation failure — is the input still there?

**Why it matters.** Losing entered data is the single most enraging form defect,
and it converts a near-complete task into an abandoned one plus a lost user.

**Fails like.**
- A refresh or a back-navigation clearing the form.
- A validation error clearing the password, or the whole form.
- Session expiry during a long form discarding everything.
- A progress indicator that says "Step 2 of 3" when there are five.
- No progress indication at all on a multi-step flow.
- No unsaved-changes warning when navigating away.

**Fix.** Persist input (local storage or server-side draft) and restore on
return. Never clear fields on a validation error. Warn before discarding.
Progress indicators must be accurate; if the step count varies, say "Step 2"
without a false total.

---

## FORM-L · Submission and its aftermath

**Check.** What happens on submit? Is there immediate feedback? Is
double-submission prevented? Is success unambiguous, and does it say what
happens next? Does the user land somewhere useful?

**Why it matters.** The gap between press and response is where users press
again. The moment after success is where a product either closes the loop or
leaves the user wondering whether it worked.

**Fails like.**
- No feedback between press and the next screen, on a slow connection.
- Double-submit creating duplicates.
- Success indicated only by the form clearing.
- A success toast that auto-dismisses before it's read.
- Success that dumps the user back to an unrelated screen with no confirmation
  they can find again.
- A confirmation with no reference number, no record link, and no email.

**Fix.** Immediate loading state on press; disable re-submission; explicit
success with what happened and what's next; a durable record where the action
matters. See `feedback-and-states.md` for the feedback-channel checks.

---

## FORM-M · Uploads

**Check.** Are accepted types and the size limit stated **before** the user
picks a file? Is there progress for large uploads? Can an upload be cancelled or
removed? What happens on failure mid-upload? Is drag-and-drop, if offered, also
available as a normal file picker?

**Why it matters.** Uploads are slow, failure-prone, and often the last step of
a long task, which makes an unhandled failure maximally expensive.

**Fails like.**
- Constraints revealed only in the rejection message.
- No progress on a multi-megabyte upload — indistinguishable from a hang.
- No cancel, no remove, no replace.
- A failure that loses the rest of the form.
- Drag-and-drop as the only affordance (unusable by keyboard, and on mobile).
- No preview or filename confirmation, so the user can't tell what got attached.
- Silent server-side rejection after an apparently successful upload.

**Fix.** State the constraints up front. Real progress, cancel, remove, retry.
Always offer a standard file input alongside any drop zone. Validate type and
size client-side before the transfer.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Form cannot be submitted on a supported browser/device | **Blocker** |
| Entered data lost on validation error, back, or refresh | **Blocker** on a long form; **High** on a short one |
| Submit disabled with no reason discoverable anywhere | **Blocker** if it blocks the task |
| No focus indication on form controls | **High** (also A11Y) |
| Errors that don't say what to do, on a core form | **High** |
| Double-submit creates duplicate records | **High** |
| Placeholder used as the only label | **High** |
| Wrong keyboard / no autofill on a mobile signup or checkout | **High** |
| Validation on every keystroke of a half-typed field | **Medium** |
| Unnecessary required fields | **Medium** (**High** if on signup or checkout) |
| Rejecting pasted formats the system could normalize | **Medium** |
| Wrong control type for the data | **Medium** |
| Inconsistent required/optional marking | **Low** |
| Field grouping and ordering preferences | **Low** — often taste; label it |
