# Rationale

## The single idea

**A figure is a ledger line: label · figure · basis.** The home page is not a dashboard with charts
about the data; it is the top of the ledger, three ruled lines that answer «هل سنحقق الرقم؟» in the
order the founder asks it: the number he is chasing (**34,000 ر.س**, one product, one quarter,
13 days left), what has been collected against it (**0**), and the only money that exists in the
pipeline toward it (**4,200**, one line of six, on the same product, at quote, not collected). Every
figure on the page can be clicked to show the records behind it, and every one is re-derived from a
records object at load and outlined in the accent if the markup disagrees. The five prior defects
were all summaries contradicting their tables; this system makes that a runtime error, not a review
finding.

The same rule shapes the ledger: a row is the record, cell by cell, and a cell that has no value
names its kind of absence. Six absences, six word-forms, six drawings. A colour is used exactly once
and means exactly one thing: money someone must act on.

## What I deliberately did not do

- **No attainment percentage, no forecast, no monthly series, no funnel rate.** 34,000 is one
  product's quarter; 4,200 is drawn as a tick on that product's own track and never as a share of
  anything. The campaign prints six counts of one cohort as bars and no drop between them.
- **No SLA comparison in the days column**, although the stage ladder holds SLAs. They are not in
  the brief's dataset, so a column that said «تجاوز المهلة» would have printed six figures nobody
  can trace.
- **No per-product price figures on home.** The brief's product facts (1 unpublished, 4 inferred,
  1 not sold) are printed as counts; the individual price statements would have conflicted with
  the brief's own count.
- **No KPI tiles, no sidebar, no avatar, no search box, no icons, no second colour, no gradient,
  no sticky header, no animated number, no stagger, no animation on sort.** The leading figure is
  76px; the tallest chrome is 48px.
- **No second markup for the phone.** The 400px ledger is the same table re-flowed by CSS.

## Where it is weakest

1. **The per-line days without a stage change are a fixture.** The brief publishes only the range
   3–24; no record anywhere in the repository holds per-line stage-entry dates (the 12/18 August dates
   the old screens used are creation dates and put every line at 30–36 days, which the brief
   overrides). The six dates in `ledger.html`'s records block are chosen so the derived range is
   exactly 3–24, and the summary is derived from them rather than typed — but they are the only six
   figures in this entry that trace to a fixture and not to a record. This is stated in the file.
2. **Currency inside the numeral isolate renders «ر.س 34,000»** with the unit to the right of the
   digits, as the brief instructs. Saudi interfaces are split on this convention; if the founder
   reads it as wrong, it is one span moved outside `.n` — but I followed the brief's rule over the
   old screens' habit.
3. **The accent's second use.** «لا يبيعه المساعد» is accented as "selling is blocked here". It is
   a stop, not money owed; the definition in SYSTEM.md §2 stretches to hold it.
4. **The 400px ledger is tall**: nine labelled fields per line, six lines, about 250px each. No
   field was dropped, so density was traded for completeness on the phone.
5. **Type is loaded from Google Fonts.** The page is self-contained in every other respect; offline
   it falls back to Noto Sans Arabic or the system face, and the tabular-figure alignment in the
   value column depends on the fallback honouring `tnum`.
