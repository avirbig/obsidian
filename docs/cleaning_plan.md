# Plan — Cleaning and Preparing Our Own Samples

*Written 2026-07-21, after the raw-data map
(`raw_sample_data_map_and_quality.md`). This is the plan for **Step 5**: turning
1227 raw machine readings into an analysis-ready table of obsidian **objects**.*

**Rule that governs everything below:** `data/` is never modified. The cleaning
code reads the raw workbooks and writes new files into `samples_db/`. Every
number stays traceable to its original Excel row.

---

## The shape of the job

```
1227 raw readings  ->  drop non-obsidian & bad readings  ->  ~1150 good readings
                   ->  combine the 2 faces of each object ->  ~520 objects
                   ->  ready for source attribution
```

The single most important change: **we stop counting readings and start counting
objects.** Everything after this step is per-object.

---

## Where the data comes from — exactly

Two files, nothing else:

| Source | What we take | Rows |
|---|---|---:|
| `data/samples/obsidian_pxrf_master_2017-2018.xlsx` → sheet **`Original`** | everything | 1227 |
| `data/samples/Avishai_Obsidian 12.2017.xlsx` → `Sheet1`, **Excel row 832** | reading 1489 only | 1 |
| | **total input** | **1228** |

**Why the `Original` sheet and not `First Changes` or `Ordered by Site`:**

- `Original` is the **fullest** version (1227 rows vs 1224). The other two sheets
  already have three readings removed.
- Those three removals we have now **reviewed one by one** (1730, 1779, 1790) and
  agreed with. So we apply them **ourselves, in code, with the reason recorded**
  rather than inheriting them silently. Someone reading the cleaning report will
  see *why* each row went, instead of finding it already gone.
- The only thing `First Changes` adds is a `Period` column, and that is derived
  directly from `site` (motza→EPPNB, einan→Natufian, yiftahel→MPPNB, exactly 1:1)
  — so we recreate it in code.
- `Ordered by Site` is `First Changes` sorted; sorting carries no information.

The principle: **start from the fullest raw version, and make every removal an
explicit, documented step.** That way the cleaning is reproducible from the raw
file alone.

Everything is read-only. Output goes to a new `samples_db/` folder.

---

## Stage A — Load, honestly

**A1. Read the two sources above** into one table of 1228 rows, each row keeping
its origin file and original Excel row number so any number can be traced back.

**A2. Key every reading on `Reading No` + `Time`.** Never `Reading No` alone —
94 numbers are reused across 2017/2018 and would merge tools from different
sites. The 3 rows with a blank/annotated `Time` get a fallback key
(`Reading No` + `Duration` + label).

**A3. Read annotations before parsing.** Avishai marks bad readings *in place*
in the cells: `Invalid` in a Time cell, `aborted` in a Locus cell. Standard
parsing silently turns these into blanks — that is how reading 1490 hid from the
first audit. So: scan every context column for non-standard text first, record
each annotation as an explicit `author_flag`, **then** parse. His marks are
better evidence than anything we infer.

**A4. Convert `< LOD` to missing — never to zero.** Zero is chemically false and
would drag averages down. Keep a parallel `_lod` boolean per element so we always
know the difference between "not measured" and "measured, below detection".

---

## Stage B — Decide which readings are usable

Each rule is applied as a **flag**, not a silent deletion. Nothing disappears;
`samples_readings.csv` keeps every row with the reason it was excluded.

| # | Rule | Why |
|---|---|---|
| B1 | Drop rows with an author annotation (`Invalid`, `aborted`) | His judgement at the bench beats our inference |
| B2 | **Drop if Rb, Zr or Nb is missing/`< LOD`** | This is the real quality test. Without the sourcing elements the reading is useless regardless of how good it looks otherwise |
| B3 | Flag (don't drop) `Duration` < 100 s | Short runs may truncate the light-element beam |
| B4 | Flag extreme `Bal` (> ~80%) | Anomaly signal — see the `Bal` box below |
| B5 | Flag `cover` = *very partial* / *tiny*, or `Dirt` = *yes* | Surface effects; blanks treated as **unknown**, never as clean |
| B6 | Flag chemical outliers vs. that site's own distribution | Catches readings that hit the mount, a bad spot, or another material |

**B2 is the rule that matters.** Reading 1790 taught us this: it ran 102.8 s —
almost full length — and still had Rb, Zr *and* Nb all below detection. Duration
is a bad quality test; **measured sourcing elements** is a good one.

Expected loss is small: only 14–17 readings have Rb/Zr/Nb below detection.

---

## Stage C — Combine the readings of one object

**Confirmed by Avishai (2026-07-21): readings that share a site + locus + basket
are measurements of the *same object* and should agree. Where two such readings
differ a lot, that is not something to average away — it must be flagged and
checked.**

**C1. Group by `site` + `Locus\Square` + `Basket`.** Site is part of the key, so
readings from different sites can never be combined even if locus and basket
numbers happen to coincide. This yields ~521 groups: 395 dorsal+ventral pairs,
58 with 4 readings, 32 single, a tail up to 12.

**C2. Check agreement *before* combining.** For each group, compare its readings
on the sourcing ratios (Rb/Zr, Rb/Nb, Zr/Nb). Readings of one object should sit
close together. We measure the spread and compare it against how much *repeat
measurements of the same object normally vary* in this dataset — a threshold
taken from the data itself, not invented.

**C3. Combine with the *median*** of the agreeing readings, not the mean. The
median cannot be dragged by a single bad reading.

**C4. When readings disagree — the 3-measurements problem.**

*Avishai's question: what if an item was measured 3 times and only 2 agree?*

The median already handles the arithmetic correctly — with three values it lands
on the middle one, which sits with the agreeing pair, so the odd reading cannot
drag the result. But **arithmetic is not the interesting part.** A disagreeing
reading means one of two very different things, and we should say which:

| The odd reading is… | Most likely meaning | What we do |
|---|---|---|
| **poor quality** — high `Bal`, dirt, partial cover, an element at `< LOD`, short duration | a **bad measurement** of the right object | exclude it, keep the agreeing two, note it |
| **good quality** — clean flags, full coverage, all elements measured | ⚠️ possibly a **different object** in the same basket, or a genuinely heterogeneous piece | **do not silently average.** Flag for Avishai to inspect |

So the rule is: **let the quality flags decide, not the majority vote.** Two
readings agreeing is not automatically proof they are right — but if the third
also looks clean, we have a real question about the object, not a measurement
error, and that deserves a human eye.

Every such case is listed in `cleaning_report.txt` with all three readings side
by side, so the decisions are reviewable rather than buried.

**C5. Other awkward groups, logged explicitly:**
- Groups with >4 readings — possibly several objects in one basket; listed for
  inspection rather than assumed.
- The 2 baskets with two `ventral` readings and no dorsal — likely a labelling
  slip.
- The 8 rows with a blank `Basket` and 3 with a blank `Locus` cannot be grouped;
  kept as single-reading objects, flagged.

---

## Stage D — Build the comparison values

**D1. Use only the elements that exist.** Sourcing runs on **Rb, Zr, Nb**
(~99% present), with Fe, Ti, Mn as support. **Sr (5.4%), Ba (4.7%), Y, Ga and Th
are dropped** — they are below detection or were never recorded. Y is absent on
the reference side too, so nothing is lost there.

**D2. Prefer ratios over raw concentrations.** Demonstrated on the 946 accepted
Motza readings: absolute Rb falls as `Bal` rises (0.010 → 0.008), but **Rb/Zr
stays flat at ~1.33 across every `Bal` band**. Whatever suppresses the absolute
numbers, the ratios survive it. Primary values: **Rb/Zr, Rb/Nb, Zr/Nb**.

---

### 📖 What `Bal` means (Avishai asked)

**`Bal` = "Balance" — the share of the sample the machine could NOT identify.**

Verified in your data: every measured element **plus `Bal` sums to exactly
100.0%** (median 99.993% across 1226 readings). So the instrument reports what it
recognised, and dumps everything else into `Bal`.

For obsidian, that unidentified share is mostly **oxygen**. Volcanic glass is
roughly 46% oxygen by mass, and pXRF **cannot see oxygen at all** — it is too
light for the technique. Add sodium and other light elements and a `Bal` around
55–65% is completely normal for your samples. It is not an error; it is the
expected shape of the measurement.

`Bal` moves opposite to Si (correlation **−0.947**): the less silicon the machine
accounts for, the more falls into `Bal`.

**How we use it:** only as an **anomaly signal**. A `Bal` far outside the usual
55–65% band means the reading is unusual and worth a second look — but we do
**not** claim to know why.

> ⚠️ *Correction:* an earlier draft called `Bal` a proxy for beam coverage. The
> data does not support that. Median `Bal` by recorded `cover` is: full 57.9,
> almost full 63.1, partial 62.3, very partial 58.2, tiny 50.7 — no clean
> pattern, and "tiny" is the *lowest*. `Bal` and `cover` are **independent**
> quality signals, and both go into the score in Stage E on their own terms.

**D3. Keep raw concentrations too**, for plots and for comparison with published
work — but attribution decisions rest on the ratios.

**D4. Convert units once, explicitly.** The workbook is in **%**; the reference
database is in **ppm**. This conversion is a classic silent error — it happens in
one documented place, with a unit test.

---

## Stage E — Quality score per object

A single 0–1 score, built from things we actually measured, carried into
attribution so that a confident answer from a poor reading is impossible:

- were all three of Rb/Zr/Nb measured (not `< LOD`)
- `cover` (full > partial > very partial > tiny; blank = unknown)
- `Dirt` flag (blank = unknown, not clean)
- `Bal` inside the normal 55–65% band (an independent signal from `cover`)
- **agreement between the readings of the object** (Stage C2) — the strongest
  signal we have, because it is the object checking itself
- number of usable readings

Objects with a low score are not deleted — they are **reported with wider
uncertainty**, and may land in "unassigned" at the attribution step.

---

## Outputs

Written to a new `samples_db/` folder:

| File | What it is |
|---|---|
| `samples_readings.csv` | all 1228 readings, every flag, keep/drop + reason, original file and Excel row |
| `samples_objects.csv` | **~521 objects** — the analysis-ready table, ratios + quality score |
| `cleaning_report.txt` | counts at each stage, every dropped reading with its reason, all open questions |

Code: `analysis/03_clean_samples.py`.

---

## Honest expectations

- **Motza dominates: 946 of 1227 readings (77%).** Einan 228, **Yiftahel only 53
  (~25 objects)**. Any conclusion about Yiftahel will be weak and we will say so
  plainly rather than presenting three sites as equally solid.
- Readings are paired, so our real sample size is **~521, not 1227**. Treating
  them as independent would make our confidence intervals look about √2 times
  tighter than they truly are.
- Surface quality is mixed: only **282 readings have full beam coverage**.
- We are sourcing on **three elements**. That is enough to separate the main
  Anatolian sources, but it will leave some objects genuinely ambiguous — and
  those get "unassigned", not a forced answer.

---

## What we need from Avishai before starting

1. ✅ **Answered:** same site + locus + basket = the **same object**; readings
   should agree, and big disagreements must be **flagged, not averaged away**
   (Stage C).
2. ✅ **Done:** workbook renamed to `obsidian_pxrf_master_2017-2018.xlsx`.
3. ✅ **Answered:** `Bal` explained above (Stage D) — and our earlier claim about
   it corrected.
4. ⏳ **Still open:** any other in-cell annotations to look for besides `Invalid`
   and `aborted`? The code will also scan for unexpected text on its own and
   report anything it finds.

---

## Decisions already made (for the record)

| Item | Decision | Date |
|---|---|---|
| Reading 1489 (Motza 27.11.17) | **Keep**, flagged low surface quality | 2026-07-21 |
| Reading 1490 (`Invalid`, 81 s) | **Drop** — author-annotated, beam incomplete | 2026-07-21 |
| Row 1790 (Einan, 102.8 s) | **Stays out** — Rb/Zr/Nb all < LOD | 2026-07-21 |
| Readings 1730, 1779 | **Stay out** — aborted (12.7 s, 23.2 s) | earlier |
