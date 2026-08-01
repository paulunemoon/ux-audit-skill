# D11 · Data display

> **When to read:** Any product that shows numbers, tables, charts, lists of
> records, or timestamps — which is most of them. This dimension is where a
> professional product separates itself from an amateur one, and where the
> findings are unusually concrete. Finding IDs: `DATA-nn`.

## Table of contents
1. [DATA-A · Number formatting](#data-a--number-formatting)
2. [DATA-B · Alignment and tabular figures](#data-b--alignment-and-tabular-figures)
3. [DATA-C · Precision and rounding](#data-c--precision-and-rounding)
4. [DATA-D · Units and currency](#data-d--units-and-currency)
5. [DATA-E · Timestamps and timezones](#data-e--timestamps-and-timezones)
6. [DATA-F · Truncation and identifiers](#data-f--truncation-and-identifiers)
7. [DATA-G · Change, direction, and sign](#data-g--change-direction-and-sign)
8. [DATA-H · Tables](#data-h--tables)
9. [DATA-I · Sorting and filtering](#data-i--sorting-and-filtering)
10. [DATA-J · Charts](#data-j--charts)
11. [DATA-K · Data freshness](#data-k--data-freshness)
12. [DATA-L · Stat cards and metric grids](#data-l--stat-cards-and-metric-grids)
13. [DATA-M · Data accessibility](#data-m--data-accessibility)
14. [Severity calibration](#severity-calibration-for-this-file)

---

## DATA-A · Number formatting

**Check.** Are numbers formatted, or printed? Thousands separators present and
locale-correct? Consistent decimal places within a column? Large numbers
readable? Any raw float output?

**Why it matters.** Unformatted numbers are slower to read and easy to
misread by an order of magnitude — and an order-of-magnitude misread on a
financial or medical figure is a real-world consequence, not an aesthetic one.

**Fails like.**
- `1240` where `1,240` belongs.
- `0.30000000000000004` — a raw float reaching the UI.
- `0.000000045` shown raw instead of a formatted or collapsed value.
- Mixed decimal places down one column (`12.5`, `12.50`, `12.500`).
- Compact notation applied where exactness matters (a total to pay shown as
  `1.2K`).
- Compact notation *not* applied where it should be, so a dashboard KPI reads
  `1,247,382,910`.
- Locale-wrong separators for the user's locale (`1.240,50` vs `1,240.50`).

**Fix.** Format at the display layer via the platform's locale-aware number
formatting, not by string manipulation. Decimals fixed per column. Compact
notation (`1.24B`, `45.3K`) for dashboards and summaries; full precision
wherever the number is being agreed to or acted on. Collapse tiny values to a
threshold (`< 0.001`) rather than printing a string of zeros — and show `0.00`
only when the value is genuinely zero.

---

## DATA-B · Alignment and tabular figures

**Check.** Are numeric columns right-aligned? Do digits use `font-variant-
numeric: tabular-nums`? Do changing numbers (counters, live prices, timers)
shift width as they update?

**Why it matters.** Right-aligned tabular numbers let the eye compare magnitude
by column position without reading. Proportional digits also make any
frequently-updating number jitter, which reads as instability.

**Fails like.**
- Left-aligned numeric columns, so magnitude can't be compared.
- Proportional figures in a table, so decimal points don't line up.
- A live-updating value whose width changes with each digit, shifting its
  neighbours.
- **A monospace font used to align numbers** — the wrong fix. It costs a second
  family and a weight mismatch for something one CSS property provides. See
  `design-system.md`, DS-G.
- Currency symbols aligned with the digits instead of held at the column edge.

**Fix.** `font-variant-numeric: tabular-nums` on every number that changes or
aligns; right-align numeric columns; left-align text columns; headers align with
their content. Searching the codebase for `tabular-nums` and finding nothing in a
number-heavy product is a reliable, quick finding.

---

## DATA-C · Precision and rounding

**Check.** Is the displayed precision appropriate to the quantity and the
decision? Does precision stay consistent between where a value is shown and
where it's acted on? Does a rounded total match the sum of its rounded parts?

**Why it matters.** Over-precision is noise; under-precision loses information;
inconsistent precision breaks trust in the number the moment a user notices two
places disagree.

**Fails like.**
- A percentage to six decimal places.
- A total that doesn't equal the visible line items because each was rounded
  independently.
- A summary showing `1.2K` and the detail showing `1,247` with no explanation
  they're the same.
- Rounding that hides a meaningful difference (two items both showing `$0.00`
  when one is `$0.004` and the other is zero).
- Precision that varies within one column.

**Fix.** Set precision per quantity type and hold it. Where a rounded summary
and an exact detail coexist, make the relationship visible (the exact value on
hover, focus, or in the detail view). Where rounding could mislead, show the
qualifier (`≈`, `<`).

---

## DATA-D · Units and currency

**Check.** Does every quantity carry its unit? Is currency identified when more
than one is possible? Are units consistent within a view, or mixed (MB and GB in
one column)? Is any unit implied by context that might not hold?

**Fails like.**
- A bare number where the unit is only in a heading three rows up.
- `$` with no currency code in a product handling multiple currencies.
- Mixed units in one column, so values can't be compared.
- Unit stated in the header but the sort operating on the raw value with a
  different unit.
- Amounts shown in one currency and charged in another with no conversion note.

**Fix.** Unit with the value, or unambiguously in the column header with
consistent units throughout the column. Currency code where ambiguity is
possible. State the conversion and its rate where one occurs.

---

## DATA-E · Timestamps and timezones

**Check.** Is every timestamp unambiguous? Which timezone is it in — the user's,
the server's, the account's — and does the interface say? Are relative times
("2 hours ago") backed by an absolute on hover or nearby? Do dates use an
unambiguous format?

**Why it matters.** Timezone ambiguity causes missed meetings, wrong-day
filings, and misread logs. It's one of the highest consequence-to-effort ratios
in this whole dimension.

**Fails like.**
- `03/04/2026` — 3 April or 4 March, depending on the reader.
- No timezone indicated anywhere in a product used across timezones.
- Server time displayed as if it were local.
- Relative time only, so "3 days ago" can't be pinned to a date.
- Relative time that doesn't update, or updates on every render causing churn.
- A deadline shown without a timezone.
- Durations formatted inconsistently (`1h 30m`, `90 min`, `1.5 hours`).

**Fix.** Unambiguous date format (`4 Mar 2026`) or an explicit ISO form.
Timezone shown wherever coordination is possible, with the user's own timezone
as the default and the ability to see the source timezone. Relative time for
recency with the absolute available on hover, focus, and tap. One duration
format.

---

## DATA-F · Truncation and identifiers

**Check.** Where values are truncated, is the truncation consistent, does it
preserve the distinguishing part, and is the full value reachable? Are long
identifiers (order numbers, hashes, keys, file paths) copyable in one action?

**Why it matters.** Truncation that removes the distinguishing characters makes
a list of items indistinguishable — and it's usually the *end* that
distinguishes them.

**Fails like.**
- `Invoice_2026_Q3_Draft_v2_fi…` where every row shares the first 25
  characters.
- Truncation with no tooltip, no title attribute, and no detail view — the value
  is simply unrecoverable.
- Different truncation lengths for the same field on different screens.
- An identifier shown truncated with no copy affordance, so the user
  hand-transcribes it.
- Copy that includes the ellipsis, or the surrounding whitespace.
- No confirmation that a copy succeeded.

**Fix.** Truncate the non-distinguishing part — middle-truncation (`7xKX…9fGh`)
for opaque identifiers, end-truncation for prose, front-truncation for paths.
One format per field type, used everywhere. Full value on hover, focus, and tap.
One-tap copy with explicit feedback.

---

## DATA-G · Change, direction, and sign

**Check.** Where a value has a direction — up/down, gain/loss, better/worse,
pass/fail — is it carried by **more than colour**? Is the sign always shown? Is
the reference period stated ("+5.2%" — since when)?

**Why it matters.** Colour-only direction is invisible to a significant share of
users and in greyscale. And a percentage change with no stated baseline is
uninterpretable.

**Fails like.**
- Green and red numbers with no `+`/`−` and no arrow.
- An arrow whose direction means "increase" in one place and "good" in another
  — a real ambiguity when a decrease is good.
- A change with no period ("+12%" since yesterday? last month? launch?).
- Directional colours identical to status success/error, so a normal decline
  looks like a system failure (see `design-system.md`, DS-F).
- Colour-only sparklines with no accessible values.

**Fix.** Sign **and** colour **and** an icon or label. State the comparison
period. Keep directional data colours distinct from status colours. Decide once
whether arrows mean direction or sentiment, and hold it.

---

## DATA-H · Tables

**Check.** Does the header stay visible on a long table? Is it clear which
columns are sortable? Are row actions discoverable without hover? What happens
to a wide table at narrow widths? Is there a designed empty state, a loading
state, and a per-row error state?

**Fails like.**
- Header scrolling out of view on a 200-row table.
- Row actions revealed only on hover — invisible on touch.
- A wide table becoming a tiny horizontal-scroll mess on mobile, with the
  identifying column scrolled out of view.
- No zebra striping, row hover, or grouping on a wide table, so the eye loses
  its row.
- Column widths jumping between pages of results.
- Row selection with no count, and no clear way to select all versus all
  matching.
- No indication that a table is paginated, or what the total is.

**Fix.** Sticky header. Sortable columns marked, with the active sort and its
direction visible. Actions visible at rest, or in a per-row menu with a
persistent trigger. At narrow widths, either stack rows into cards or choose
priority columns deliberately and pin the identifying one. Define which columns
survive at each breakpoint.

---

## DATA-I · Sorting and filtering

**Check.** Is the current sort visible? Is the default sort sensible and stated?
Do filters show what's currently applied, and can each be removed individually?
Do sort and filter survive navigation and reload? Does sorting work correctly on
the underlying value rather than the formatted string?

**Why it matters.** Invisible filter state is a data-correctness problem — the
user reads a filtered view as the whole set and draws a wrong conclusion.

**Fails like.**
- Filters applied but not displayed, so the view silently excludes data.
- No "clear all" on a filter set.
- Sort reset on every navigation.
- Sorting a formatted string, so `$1,000` sorts before `$9` and `2 Jan` sorts
  before `10 Jan`.
- Sorting that ignores case or locale inconsistently.
- Filters that return nothing with no way to widen, and no indication which
  filter is responsible.
- Filter and sort state absent from the URL, so a view can't be shared.

**Fix.** Applied filters as removable chips with a clear-all. Active sort marked
in the header. Sort on the underlying typed value. Persist state in the URL.
Zero-results state naming the filters in play and offering to relax them.

---

## DATA-J · Charts

**Check.** Is the chart type right for the question? Does it have axis labels,
units, and a scale that doesn't mislead? Can the user get the exact value at a
point? Is the data available in a non-visual form? Do the colours come from a
data palette rather than the UI/status palette?

**Why it matters.** A chart the user can't interrogate is decoration — the whole
reason to plot a series is to ask "what was it *there*".

**Fails like.**
- No hover or tap tooltip on a time series, so exact values are unavailable.
- A truncated y-axis with no indication, exaggerating a small change.
- Unlabelled axes, or units only in the title.
- A legend keyed by colour alone with no labels or patterns.
- 3D effects, gratuitous gradient fills, or decorative animation obscuring the
  data.
- A pie chart with twelve slices, or one used for values that aren't parts of a
  whole.
- Chart colours pulled from status tokens, so a red series reads as an error.
- No empty state, no loading state, no failure state for the chart.
- The chart present but the concrete number it illustrates absent.

**Fix.** A hover/tap tooltip as the default for any time-series or multi-point
chart, showing the point's label, each series with its swatch and name, and the
value right-aligned in tabular figures; an active-point indicator; edge-flipping
so it never clips; and on touch, press-and-drag along the series with the last
value staying visible. Label axes with units. Start the axis at zero or mark the
break. Use a dedicated categorical data palette. Pair every chart with the
concrete number it illustrates. Make the underlying values reachable as text or
a table (DATA-M).

Tooltips are legitimately optional only where they'd be meaningless — a
single-value donut, or a sparkline used purely as a trend glyph.

---

## DATA-K · Data freshness

**Check.** Does the interface say how current the data is, where that matters?
Does it refresh, and on what trigger? Do live values update smoothly or
flicker? Is stale data distinguishable from current data?

**Why it matters.** A user acting on data they believe is live, when it's ten
minutes old, makes a decision the interface caused.

**Fails like.**
- No "last updated" anywhere on a dashboard people act on.
- Data cached indefinitely with no refresh after a related action.
- Live values vibrating as they update at high frequency.
- A stale view after an action that should have invalidated it (a balance
  unchanged after a transfer).
- Fake liveness — a blinking "Live" indicator on data that changes hourly (see
  `content-and-copy.md`, COPY-G).
- No manual refresh where automatic refresh isn't feasible.

**Fix.** Show freshness where it's material. Refresh on a sensible interval and
after any action that changes the data. Throttle high-frequency updates and
transition value changes smoothly — a brief highlight is fine, constant flicker
is not. Mark stale data as stale.

---

## DATA-L · Stat cards and metric grids

**Check.** Does each stat card carry one clear metric with a label, a value, and
the context needed to interpret it? In a grid of metrics, is there a hierarchy,
or are they all equal weight when one dominates?

**Fails like.**
- A number with no label, or a label that doesn't say what's being counted.
- No comparison or baseline, so the number is uninterpretable.
- Six equal-weight tiles where one is the metric the screen exists for.
- A metric grid on mobile at three columns, truncating every value.
- Stat cards whose values don't use tabular figures, so a grid of them
  misaligns.

**Fix.** Label, value, and one piece of context (comparison, target, or period)
per card. Give the dominant metric visual precedence (see `visual-hierarchy.md`,
VIS-A). Drop to one or two columns on mobile.

---

## DATA-M · Data accessibility

**Check.** Is any data locked in a purely visual encoding? Do tables use real
table semantics with header associations? Are chart values reachable by screen
reader? Do data colours meet contrast on their actual backgrounds?

**Why it matters.** Data visualizations are the most common place where
information is genuinely unavailable to non-visual users — not degraded,
unavailable.

**Fails like.**
- A chart with no text alternative and no accessible data table.
- A table built from `<div>`s with no header semantics, so screen-reader
  navigation gives no column context.
- Meaning by colour alone (DATA-G).
- Data colours that fail contrast against the chart background.
- A heatmap or status grid whose only encoding is hue.
- Sortable headers that aren't buttons and don't announce sort state.

**Fix.** Real table semantics with `<th>` and scope. A text summary or a
toggleable data table alongside each chart. Second encoding channels — pattern,
shape, direct labels — alongside colour. Verify data colour contrast with
`scripts/contrast-check.py`. Sort controls as buttons with `aria-sort`. Details
in `accessibility.md`.

---

## Severity calibration for this file

| Situation | Typical grade |
|---|---|
| A number is wrong or misleading as displayed (rounding that hides a difference, a total that doesn't match its parts) | **Blocker** |
| Filters applied but invisible, so a partial view reads as complete | **Blocker** |
| Ambiguous date or timezone on something time-critical | **High** |
| Currency or unit ambiguous where money is involved | **High** |
| Truncation that makes items indistinguishable with no full value available | **High** |
| Direction or status by colour alone | **High** (also A11Y) |
| Chart data unavailable to screen readers | **High** (also A11Y) |
| Misleading axis (truncated, unlabelled) | **High** |
| Sorting on the formatted string rather than the value | **High** |
| No exact values obtainable from a time-series chart | **Medium** |
| No tabular figures in a number-heavy product | **Medium** |
| Stale data with no freshness indication | **Medium** |
| Table header not sticky on long tables | **Medium** |
| Row actions hover-only | **Medium** (**High** on touch platforms) |
| Inconsistent decimals within a column | **Low**–**Medium** |
| Compact-notation thresholds, chart type preferences | **Low** — often taste; label it |
