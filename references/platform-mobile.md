# D13 · Platform conventions — mobile

> **When to read:** The product is a native iOS or Android app, a React Native /
> Flutter app, or a mobile-first web experience. A responsive web product needs
> this file **and** `platform-web.md`. Finding IDs: `PLAT-nn`.
>
> This file holds what **diverges** on mobile. Everything else — forms, states,
> copy, hierarchy, accessibility — is graded by the dimension files, with the
> mobile notes each carries.

## Table of contents
1. [PLAT-N · Touch targets and the thumb zone](#plat-n--touch-targets-and-the-thumb-zone)
2. [PLAT-O · No hover, and what replaces it](#plat-o--no-hover-and-what-replaces-it)
3. [PLAT-P · Safe areas and system chrome](#plat-p--safe-areas-and-system-chrome)
4. [PLAT-Q · Navigation model](#plat-q--navigation-model)
5. [PLAT-R · Sheets over modals](#plat-r--sheets-over-modals)
6. [PLAT-S · The on-screen keyboard](#plat-s--the-on-screen-keyboard)
7. [PLAT-T · Input on mobile](#plat-t--input-on-mobile)
8. [PLAT-U · Gestures](#plat-u--gestures)
9. [PLAT-V · Platform idioms — iOS and Android](#plat-v--platform-idioms--ios-and-android)
10. [PLAT-W · System settings and accessibility features](#plat-w--system-settings-and-accessibility-features)
11. [PLAT-X · Type, spacing, and density on mobile](#plat-x--type-spacing-and-density-on-mobile)
12. [PLAT-Y · Home screen and headers](#plat-y--home-screen-and-headers)
13. [PLAT-Z · Lifecycle, connectivity, and permissions](#plat-z--lifecycle-connectivity-and-permissions)
14. [Severity calibration](#severity-calibration-for-this-file)

---

## PLAT-N · Touch targets and the thumb zone

**Check.** Measure hit areas, not glyphs. Platform minimums: **44×44pt on iOS,
48×48dp on Android** (WCAG 2.2's 24×24 CSS px is the floor, not the goal). Then
check placement: are the actions people perform most often reachable
one-handed, in the bottom third? Are destructive and primary actions adjacent
and similarly sized?

**Why it matters.** Under-sized targets produce mis-taps, and a mis-tap next to
a destructive action is a data-loss event.

**Fails like.**
- Icon-only controls at the glyph's size with no padding.
- Table or list row actions sized for a cursor.
- Adjacent targets with no spacing between them.
- Delete adjacent to a frequently-used action at the same size.
- The primary action in the top-right corner, out of thumb reach on a large
  phone.
- A close control in the top corner of a full-screen sheet, unreachable
  one-handed.
- Small targets sitting inside a swipe or scroll gesture area.

**Fix.** Pad the target even where the glyph stays small. Space adjacent
targets. Primary actions in the bottom third. Destructive actions separated from
routine ones by distance, treatment, or a confirmation.

---

## PLAT-O · No hover, and what replaces it

**Check.** Anything the web version reveals on hover — tooltips, row actions,
truncation reveal, menus, affordance — must have an explicit mobile path. Is
pressed feedback perceptible on every interactive element?

**Why it matters.** On touch there is no hover, so a hover-dependent affordance
simply doesn't exist. And with no hover, **pressed feedback is the only
acknowledgement a tap gets** — its absence makes every control feel broken.

**Fails like.**
- A tooltip carrying necessary information, unreachable on touch.
- Row actions revealed on hover, invisible on mobile.
- Truncated values whose full form is hover-only.
- A card that looks static because its only affordance was `:hover`.
- No pressed/active state, so a slow response is indistinguishable from a dead
  control.
- `:hover` styles applied on tap and sticking afterwards.

**Fix.** Tap-to-open popovers or sheets in place of tooltips. Actions visible at
rest or behind a persistent per-row trigger. Perceptible pressed state on
everything tappable. Scope hover styling with `@media (hover: hover)` on mobile
web.

---

## PLAT-P · Safe areas and system chrome

**Check.** Does content respect the safe-area insets — notch, dynamic island,
status bar, home indicator, rounded corners, and on Android the gesture
navigation bar? Is anything critical underneath system chrome? Does the layout
hold in landscape and on tablets?

**Fails like.**
- A bottom action bar or CTA under the home indicator.
- The top bar under the status bar or notch.
- Content clipped by the display's rounded corners.
- A bottom sheet's footer actions inside the gesture-navigation area, so the
  swipe-up gesture intercepts the tap.
- Toasts outside the safe area.
- Safe areas handled in portrait but not landscape (the insets differ).
- Mobile web using `100vh`, which overshoots because of browser chrome — `dvh`
  (or `svh`/`lvh`) is the fix for *that* problem. **Note this is separate from
  the keyboard problem, PLAT-S.**

**Fix.** Insets applied on all four edges, in both orientations, and tested on a
notched device and a gesture-navigation Android device. Add the inset **on top
of** the design margin rather than replacing it.

---

## PLAT-Q · Navigation model

**Check.** Is the primary navigation a bottom tab bar (3–5 destinations),
appropriate to the product? Is essential functionality buried in a hamburger?
Is back behaviour correct — the system back gesture on Android, the swipe-back
gesture on iOS, and a visible back affordance where the stack is deep?

**Fails like.**
- More than five bottom tabs, so labels truncate.
- Everything behind a hamburger while a bottom bar would fit.
- A "More" tab holding most of the product.
- Android hardware/gesture back not handled, or exiting the app mid-flow.
- iOS edge-swipe-back disabled with no visible back control.
- Deep navigation stacks with no breadcrumb of where the user is.
- Modal presentation used where a push belongs, so back feels wrong.
- Tab state reset on every switch, losing the user's position in each tab.

**Fix.** Bottom tabs for the top destinations; the rest reachable within them.
Preserve per-tab navigation state. Handle system back explicitly — on Android
this is a Blocker-adjacent defect when unhandled mid-flow.

---

## PLAT-R · Sheets over modals

**Check.** Does the product use bottom sheets for contextual decisions, rather
than centred desktop-style modals? Is there a drag handle, swipe-to-dismiss, and
scrim dismissal? Does a tall sheet scroll internally with its footer actions
pinned? Are full-screen covers used for immersive flows rather than sheets?

**Fails like.**
- A centred modal box with margins, ported straight from the web.
- A sheet with no dismissal affordance.
- A sheet taller than the screen with no internal scroll, so the actions are
  unreachable.
- Footer actions outside the safe area.
- Swipe-to-dismiss on a sheet containing unsaved input, with no confirmation.
- A confirmation or signature rendered as an inline expander rather than its own
  focused surface.

**Fix.** Bottom sheet for contextual actions, full-screen cover for immersive
flows. Drag handle, swipe and scrim dismissal, internal scrolling, footer within
the safe area, and stacked full-width actions with the primary on top.

---

## PLAT-S · The on-screen keyboard

**Check.** Open every input the product has. Does the keyboard cover the focused
field or the primary action? Does the layout rise, and return cleanly on
dismiss? Does the focused field scroll into view — including the third and
fourth fields of a long form? Test on a small device with a large system font
size, which is where it breaks.

**Why it matters.** This is the most common mobile layout defect. A confirm
button hidden behind the keyboard makes the flow a **dead end** on small
devices, and it's far cheaper to design in than to retrofit.

**Two distinct problems on mobile web — the fix for one does not fix the other,
and getting this backwards is the usual reason a "fixed" layout still breaks:**

| Problem | Fix |
|---|---|
| Browser chrome (URL bar) showing/hiding makes `100vh` overshoot the visible area | **`dvh`** (or `svh`/`lvh`). `100vh` remains wrong on mobile browsers. |
| The on-screen keyboard covers a bottom-pinned element | **The `VisualViewport` API** — nothing else. |

**Viewport units do not react to the keyboard.** `dvh`, `svh`, and `lvh` all
resolve against the *layout* viewport; the keyboard shrinks the *visual*
viewport. A footer sized with `100dvh` still ends up underneath it. Read
`window.visualViewport` (`height`, `offsetTop`, and the `resize`/`scroll`
events) and offset the container.

**On React Native / Expo**, the recurring specifics:
- With `@gorhom/bottom-sheet`, use its **`BottomSheetTextInput`** rather than a
  plain `TextInput` — the sheet tracks focus through its own input component,
  and a raw `TextInput` is the single most common cause of a sheet that won't
  lift. `keyboardBehavior="interactive"`, `keyboardBlurBehavior="restore"`, and
  `android_keyboardInputMode="adjustResize"` (Android defaults to `adjustPan`).
- Outside a sheet library, `react-native-keyboard-controller` is more reliable
  than the built-in `KeyboardAvoidingView`, which needs different `behavior`
  props per platform and handles Android inconsistently.
- **These two libraries conflict.** Mounting
  `react-native-keyboard-controller`'s `KeyboardProvider` can break
  `@gorhom/bottom-sheet`'s own keyboard handling unless the sheet's scrollable is
  wrapped in gorhom's provided HOCs.
- Check the app isn't in a mode that blocks resizing — on Android the activity's
  `windowSoftInputMode`, on iOS an inset-management conflict inside a scroll
  view.
- **Test on a real Android device.** Keyboard-overlap bugs persist on Android
  even with the configuration above, and the iOS simulator will not reveal them.

---

## PLAT-T · Input on mobile

**Check.** Does each field bring up the right keyboard? Is input text at least
16px (below that, iOS Safari zooms on focus and doesn't zoom back)? Are
autocorrect, autocapitalize, and spellcheck disabled on exact-match fields? Does
the OS suggest saved credentials and SMS codes? Are trailing affordances
(clear, paste, max, unit) at least 44pt?

**Fails like.**
- An alphabetic keyboard on a numeric field.
- Input text at 14px, causing a zoom that strands the user zoomed in.
- Autocapitalize on a username, code, or identifier field — silent corruption of
  input.
- Autocorrect rewriting an exact-match value.
- A custom-built field the password manager can't see.
- An OTP field that doesn't accept the OS-suggested SMS code.
- Paste blocked in a password field.
- A custom picker replacing the native one, losing the OS behaviour users know.

**Fix.** Correct `inputmode`/`keyboardType` per field; 16px floor; autocorrect,
autocapitalize, and spellcheck off for exact-match fields; standard autofill and
one-time-code support; native pickers unless there's a specific reason not to.
See `forms-and-input.md` FORM-F and FORM-G.

---

## PLAT-U · Gestures

**Check.** Is any function available **only** by gesture? Are gestures
discoverable? Do they conflict with system gestures (edge swipe for back, swipe
up for home, pull down for notifications)? Does every gesture have a visible
alternative?

**Why it matters.** Gestures are invisible — they exist only for users who
already know them. As enhancements they're excellent; as the only path they hide
functionality and fail accessibility (A11Y-P).

**Fails like.**
- Swipe-to-delete as the only delete.
- A carousel with no visible pagination or arrows.
- A custom horizontal swipe near the screen edge, fighting the system back
  gesture.
- Pull-to-refresh on a view where it isn't expected, or missing where it is.
- Long-press as the only route to a menu, with no affordance.
- Drag-to-reorder as the only reordering method.
- No haptic or visual confirmation on a gesture that commits something.

**Fix.** Every gesture has a visible button alternative. Keep gestures out of
system gesture zones. Make discoverable ones discoverable (a peek, a hint on
first use, a visible handle). A swipe-to-confirm slider is a strong pattern for
a terminal irreversible action — it prevents accidental taps and fits the thumb
— but it needs a button fallback for assistive technology.

---

## PLAT-V · Platform idioms — iOS and Android

**Check.** Does the app follow the conventions of the platform it's on, or apply
one platform's idioms to both? On cross-platform frameworks, this is where
divergence is most often skipped.

| Concern | iOS | Android |
|---|---|---|
| Back | Nav-bar back button + edge-swipe | System back gesture / button — **must be handled** |
| Primary nav | Bottom tab bar | Bottom navigation bar |
| Sheets | Sheets with drag handle | Bottom sheets, Material spec |
| Feedback | Subtle haptics | Ripple on press |
| Icons | SF Symbols | Material Symbols |
| Type | SF Pro + Dynamic Type | Roboto + font scaling |
| Share | Share sheet | Share intent |
| Date/time | Native wheel/inline pickers | Material pickers |
| Settings | In-app, or the iOS Settings app where the OS puts them | In-app, plus system app settings |

**Fails like.** Android back unhandled or exiting mid-flow; iOS-style back
chevrons as the only back affordance on Android; a hamburger where a bottom bar
is the platform norm; a custom share UI instead of the system sheet; a
third-party icon set replacing SF Symbols on native iOS, breaking weight and
optical matching with system chrome; ripple missing on Android; haptics fired on
every tap.

**Fix.** Name the specific idiom and the cost. Where a cross-platform codebase
deliberately unifies the two, that's a legitimate tradeoff — **name the
tradeoff** and audit whether the unified choice works on both, rather than
assuming ignorance. Some divergences (system back, share, pickers) aren't
negotiable and should be graded accordingly.

---

## PLAT-W · System settings and accessibility features

**Check.** Does the app respect the OS-level settings users have already set?
Dynamic Type / font scale, bold text, increase contrast, reduce motion, reduce
transparency, dark mode, and the platform screen reader (VoiceOver / TalkBack).

**Why it matters.** These are settings a user has already chosen because they
need them. An app that ignores them is telling that user it doesn't apply to
them.

**Fails like.**
- Dynamic Type disabled to force a fixed size — a common shortcut that breaks
  the platform's primary accessibility affordance.
- Layouts that clip or overlap at the largest system font size.
- `prefers-reduced-motion` / Reduce Motion ignored.
- Dark mode unsupported, or supported with unreadable contrast.
- Custom controls with no accessibility traits, so the screen reader announces
  nothing.
- Focus order in the screen reader diverging from visual order.
- Reduce Transparency ignored on a blur-heavy interface.

**Fix.** Support dynamic type and test at the largest setting. Honour reduce
motion and reduce transparency. Full accessibility traits on custom controls.
Run VoiceOver or TalkBack through one core task — see `accessibility.md` A11Y-Q.

---

## PLAT-X · Type, spacing, and density on mobile

**Check.** Is body text at least 16 for primary content? Is the screen-edge
margin appropriate (~16, 20 at most) plus safe-area insets? Is section spacing
compressed relative to web, given vertical space is scarce? Are big numbers
still tabular?

**Fails like.** Web spacing values ported to mobile, so a screenful holds almost
nothing; 24–32px screen margins eating the width; body text below 16; multi-
column metric grids at three or four across, truncating every value; a single
screen carrying six competing colours (see `visual-hierarchy.md`, VIS-F — this
fails worst on mobile).

**Fix.** Mobile rhythm: 4–8 compact · 12–16 component padding · 16–20 between
elements · 24–32 between sections. Edge margin ~16 plus insets. One or two
columns for metric grids. Vertical-stack first.

---

## PLAT-Y · Home screen and headers

**Check.** Does the home screen's header do a job, or is it a large title and
nothing else? Does it reflect the user's state (signed in or not, empty or
populated)? Is the primary content within the first screenful?

**Why it matters.** The default — one large page title top-left and nothing
else — is a reflex rather than a decision, and it spends the most valuable
screen area in the app on a word the user already knows.

**Options worth considering** (as a remediation proposal, not a mandate): a
personal greeting with the account affordance, for consumer apps; **value-
forward**, where the primary number or status *is* the header; **contextual**,
where search or a segmented control leads because that's the primary action; or
a **plain title** — legitimate for a utility screen, as a chosen option rather
than a fallback.

**Fails like.** A large title with an empty header band beneath it; the primary
metric pushed below the fold by decoration; a header that doesn't change between
signed-out and signed-in; a title that duplicates the tab label directly beneath
it.

**Fix.** Match the header to what the screen is for. Where the screen exists to
show one number, that number leads by position and size — if it's the same size
as everything else, the hierarchy has failed.

---

## PLAT-Z · Lifecycle, connectivity, and permissions

**Check.** Backgrounding and returning: is state preserved? Is a sensitive
screen protected in the app switcher? On a cold start after a kill, does the app
restore usefully? What happens on connection loss mid-task? Are permissions
requested in context and is refusal a supported path?

**Fails like.**
- State lost on backgrounding, so a half-completed form is gone.
- Sensitive content visible in the app-switcher snapshot.
- No offline handling in a product used on the move.
- An action taken offline that appears to succeed and is silently lost (also
  `feedback-and-states.md`, STATE-E).
- Permission dialogs on launch with no context (`onboarding-and-flows.md`,
  ONB-C).
- Refusal breaking the app rather than degrading it.
- No route to system settings after a permanent denial.
- Push notifications requested before the app has demonstrated why.

**Fix.** Persist in-progress state across backgrounding and cold start. Obscure
sensitive content in the switcher. Detect connectivity, queue or clearly reject
writes, recover on reconnect. Pre-prompt before the OS dialog; define the
degraded path for every refusal; offer a deep link to settings once denied
permanently.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| Primary action unreachable behind the keyboard | **Blocker** |
| Android system back unhandled, exiting or breaking a flow | **Blocker** |
| In-progress work lost on backgrounding or rotation | **Blocker** |
| Content permanently under the notch, home indicator, or gesture bar | **Blocker** if it blocks the task, else **High** |
| Action available only by gesture, with no alternative | **High** |
| Touch targets below the platform minimum on core actions | **High** |
| Dynamic Type disabled, or layout breaking at the largest font size | **High** |
| No pressed feedback on interactive elements | **High** |
| Input text below 16px causing iOS zoom | **High** |
| Autocapitalize/autocorrect on exact-match fields | **High** — silent data corruption |
| Hover-dependent affordance with no touch path | **High** |
| Sensitive content exposed in the app switcher | **High** |
| Centred web modal instead of a sheet | **Medium** |
| More than five bottom tabs; essentials behind a hamburger | **Medium** |
| Platform idioms unified across iOS and Android by deliberate choice | **Medium** at most — name the tradeoff |
| Web spacing values on mobile | **Medium** |
| Home header defaulted to a lone large title | **Low**–**Medium** |
| Haptics on every tap; ripple missing | **Low** |
