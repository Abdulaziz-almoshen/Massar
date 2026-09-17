# Review record — not build inputs

Nothing here is served or read by `gen.py`. These are the papers behind the
redesign, kept so the next person can check the work rather than take it on
trust.

| File | What it is |
| --- | --- |
| `BRIEF.md` | The brief Astra was given: the product, the founder's question, every hard constraint, the real dataset, and the eight rejected directions. |
| `ASTRA.md` | The full transcript. |
| `ASTRA-FINAL.md` | The final answer, including the **Block** verdict and its five HIGH findings. |
| `astra.css` | The foundations Astra wrote. **Already merged into `../massar.css`** — do not link it. A second stylesheet that only overrides the first is how `revamp.ts §8` ended up with 39 card classes it could never reconcile. |
| `astra-home.html.txt` | Astra's home markup sketch. `gen.py` generates the real thing. |

## The five HIGH findings, and where each was answered

All five were factual, not cosmetic: the page computed figures the records do
not contain. Restyling could not have fixed any of them.

1. **A monthly target series invented by dividing by 12.** 34,000 is recorded
   on one product for one quarter. Deleted; `PERIODS` in `gen.py` now shows the
   target only for the quarter that has one, and every other period reads
   «لا مستهدف مسجّل لهذه الفترة» — no target recorded, which is not zero.
2. **«6 على المسار» labelled six stationary lines healthy.** Replaced with
   «ستة بنود بلا حركة منذ 29–35 يومًا · آخر حركة في 18 أغسطس».
3. **A funnel drop of «▾ 75%» between stage populations that were never a
   tracked cohort.** Both home funnels deleted.
4. **A weighted forecast with no probability model, and «six lines aged 30+»
   counting a line that has stood 29 days.** Forecast deleted; the count is
   now `N_AGED_30`, which is five.
5. **Counts disagreeing with their own tables** — the rail said six products,
   home said "five of six", the truth was eight and seven. Every count now
   derives from the records in `gen.py`'s DERIVED block, the rail's badges
   included (`gen.py` writes them into `shell.js`).
