# Raw Sample Data — Map and Quality Report

*What is in our own pXRF measurement files, where every reading came from, and
what problems exist — recorded **before** any cleaning. Produced 2026-07-21 by
`analysis/02_map_raw_samples.py`. No raw file was modified.*

---

## 1. The question we asked

`data/samples/obsidian_pxrf_master_2017-2018.xlsx` (renamed from
`data manipulation.xlsx`, §6) is the workbook where all measurements were
assembled by hand. Before cleaning we wanted to know:

1. Does it really contain everything from the separate session files?
2. Are there samples that exist **only** in it, with no separate file?
3. What condition is the data in?

---

## 2. The short answer

**The master workbook is complete, and it contains nothing extra.**

- Every one of its **1227 readings** traces back to a session file. **Zero
  master-only readings.** The suspicion that some samples exist only in the
  master turned out to be false — which is good news: nothing is unsourced.
- It is a **filtered subset**, not a merge. 1745 distinct readings exist across
  the session files; 1227 were kept, **518 excluded**.
- Of those 518 exclusions, **515 are correct** — they are not obsidian. **Three
  are obsidian**, and **two of those are a genuine loss** needing your decision
  (§4).

---

## 3. Where each reading came from

The instrument's `Reading No` counter was **reset**, so it is *not* a unique ID:
94 reading numbers appear twice — once in 2017 and once in 2018. Example:
reading 1682 is both Yiftahel (2017-02-09) and Motza (2018-02-19).

> **Rule for the cleaning step: the unique key is `Reading No` + `Time`, never
> `Reading No` alone.** Using it alone would silently merge a Yiftahel tool with
> a Motza tool.

| Session file | Readings | In master |
|---|---:|---:|
| 01 Yiftahel MPPNB 9.2.2017 | 53 | 52 |
| 02 Einan Natufian 23.2.17 | 30 | 30 |
| 03 Eynan 9.3.17 | 57 | 57 |
| 04 Einan 30.3.17 | 38 | 38 |
| 05 Einan 5.4.17 | 56 | 56 |
| all 19.2.2018–5.3.2018 | 342 | 170 |
| Avishai_Obsidian 12.2017 | 883 | 880 |
| all analyses 13.3.18 | 793 | 449 |

The last two files overlap heavily with the others — they are cumulative
instrument dumps, not new sessions. That is why the totals do not simply add up.

### Why 516 readings were excluded

The pXRF machine was used for **other projects too**, and those readings sit in
the same dumps. The excluded set is:

| What it is | Count |
|---|---:|
| General Metals — Roman bronze sculpture from Caesarea, metal rings, Chalcolithic metal from Fazael, a Byzantine die, Persian anklets | 332 |
| "Mining" mode, unlabelled — **not obsidian** (see below) | 143 |
| System Check (machine self-test) | 14 |
| Electronics Metals | 13 |
| "Mining" mode, labelled — pottery from Tel Tsaf (4), one 9 s abort | 5 |
| Precious Metals | 5 |
| Soil | 3 |
| **Obsidian-labelled readings** | **3** |
| **Total** | **518** |

**The 148 unlabelled "Mining" readings are not obsidian.** We checked their
chemistry rather than trusting the blank label: their median Calcium is **4.8%**,
with individual values of 16%, 30%, 34% — that is limestone/carbonate. Obsidian
is volcanic glass with very low Calcium and high Rubidium/Zirconium. Their median
Rubidium is 0.002% (~20 ppm) against ~90+ ppm for our obsidian. They are a
different material and were correctly left out.

---

## 4. ⚠️ The real loss — one whole Motza object — needs your decision

### Where it is

> **File:** `data/samples/Avishai_Obsidian 12.2017.xlsx`
> **Sheet:** `Sheet1`
> **Excel rows 832 and 833** (reading numbers 1489 and 1490)

It exists in **only that one file** — no other workbook contains it.

### What it is

Both rows carry the label `obidian motza 27.11.17` — **"obsidian" is mistyped as
"obidian"**, which is almost certainly why they were missed when the master was
assembled by hand. They are the **only two readings from 27.11.2017** in the
entire dataset, and the master contains nothing at all from that date.

Two readings with one label is exactly the **dorsal/ventral pair** pattern seen
everywhere else in this data (§5.2). So this is most likely **one Motza object,
measured twice, missing entirely.**

### Is it really obsidian? Yes — the sourcing elements say so

| Element | r1489 | r1490 | Motza median | Motza 5–95% |
|---|---:|---:|---:|---|
| **Rb** | 0.009 | 0.009 | 0.009 | 0.008–0.011 |
| **Zr** | 0.007 | 0.007 | 0.007 | 0.006–0.008 |
| **Nb** | 0.003 | 0.002 | 0.002 | 0.002–0.003 |
| Fe | 1.034 | 1.115 | 0.669 | 0.555–1.116 |
| Ti | 0.048 | 0.107 | 0.049 | 0.034–0.120 |
| Ca | 1.552 | 3.100 | 0.818 | 0.429–3.552 |
| K | 1.190 | 2.847 | 3.035 | 2.253–4.414 |
| Si | 11.635 | < LOD | 29.953 | 21.215–41.340 |
| Al | 1.126 | < LOD | 3.523 | 2.159–6.211 |
| Bal | 83.196 | 92.755 | 60.516 | 46.984–71.004 |

**The three elements we actually source on — Rb, Zr, Nb — sit exactly on the
Motza median.** This is genuine Motza obsidian.

The light elements (Si, Al, K) are far too low and `Bal` (the unmeasured
remainder) is far too high. That combination is the classic signature of the
**beam not sitting fully on the sample** — light elements are the most sensitive
to surface geometry and coverage, while the heavier trace elements stay reliable.
Reading 1490 also ran only 81.34 s instead of the usual ~120 s.

### ✅ DECIDED (2026-07-21, by Avishai): drop 1490, keep 1489

**Reading 1490 — dropped.** The author confirms he typed the `Time` cell himself
as the literal text **`Invalid`**. Verified in the file: it is the **only**
non-date value in the entire `Time` column of that sheet — a deliberate
annotation, not missing data.

Two independent facts corroborate it:
- **Duration 81.34 s** instead of the usual ~120 s — the run was cut short.
- **Whole element channels are absent** — no Si, Al, Cl, S, P or Mg at all, not
  even `< LOD`. The instrument runs its beams in sequence and the light-element
  beam runs last, so an abort at 81 s means that beam never completed.

*This corrects an earlier reading in this report, which attributed 1490's odd
light-element values to partial beam coverage. The real cause is simpler: an
incomplete measurement, flagged as such by the author at the time.*

**Reading 1489 — kept**, flagged as lower surface quality. Full 120.58 s, valid
timestamp, complete element suite. Its `Bal` (unmeasured remainder) of 83.2% is
high — the 99th percentile — but **12 accepted readings already exceed 80%**
(max 87.2), so it is unusual rather than disqualifying. Tested empirically on the
946 accepted Motza readings:

| Bal band | n | Rb/Zr median |
|---|---:|---:|
| <55 | 252 | 1.429 |
| 55–65 | 402 | 1.429 |
| 65–75 | 279 | 1.333 |
| 75–85 | 8 | 1.333 |
| 85+ | 5 | 1.333 |

The **Rb/Zr ratio is flat across every band**, so a high `Bal` does not bias it.
Reading 1489's Rb/Zr = **1.286**, inside the accepted 5–95% range (1.125–1.571).

> **Method note worth carrying forward:** *absolute* Rb falls as `Bal` rises
> (0.010 → 0.008) while the **ratio stays stable**. This is an argument for
> basing attribution on **element ratios rather than raw concentrations**.
>
> *The observation is verified; the cause is not. An earlier version of this note
> attributed it to "beam geometry". That was speculation and is not supported —
> `Bal` shows no clean relationship with the recorded `cover` flag (full 57.9,
> tiny 50.7 — not monotonic). What is certain: all measured elements + `Bal` sum
> to 100%, so `Bal` is simply the share the instrument could not identify
> (mostly oxygen, invisible to pXRF), and it tracks Si at r = −0.947. Whatever
> suppresses the absolute numbers, the ratios survive it — which is what
> matters here.*

**Net effect:** the 27.11.2017 Motza object enters the analysis with **one**
usable reading instead of the usual two.

### The third obsidian-labelled exclusion was correctly dropped

Reading **146** (2017-04-05 09:23, row 2 of the same file) ran only **17.17 s**
and returned **no element values at all** — a genuinely aborted measurement.

---

### 📌 Correction to an earlier version of this report

The first pass reported **one** missing obsidian reading and **516** exclusions.
That was wrong. The coverage check matched readings by timestamp, and **reading
1490 has a blank `Time` cell** — so it was invisible to that check.

Re-run with a fallback key (`Reading No` + `Duration` + label) for rows lacking a
timestamp. Corrected figures: **1745** distinct session readings, **518**
excluded, **3** obsidian-labelled, **2** genuinely lost.

Only **3 rows in the whole dataset** have a blank timestamp (two in
`Avishai_Obsidian 12.2017.xlsx`, one in `all analyses 13.3.18 copy.xls`), and the
master itself has none — so the exposure was small, but it was real. The
conclusion that **no reading exists only in the master (0 rows)** was re-verified
with the corrected key and **still holds**.

---

## 5. Condition of the data inside the master

### 5.1 Which elements we can actually use

Out of 1227 readings:

| Element | Usable | Verdict |
|---|---:|---|
| Fe | 100.0% | good |
| Ti | 99.8% | good |
| **Rb** | **98.8%** | **good — key sourcing element** |
| **Zr** | **98.8%** | **good — key sourcing element** |
| **Nb** | **98.6%** | **good — key sourcing element** |
| Pb | 97.5% | good |
| Mn | 78.2% | usable with care |
| Zn | 45.6% | weak |
| **Sr** | **5.4%** | **unusable — 1160 of 1227 below detection** |
| **Ba** | **4.7%** | **unusable — 1165 below detection** |
| **Y** | — | **column does not exist in this workbook** |
| **Ga** | 0% | **empty column** |
| **Th** | 0% | **empty column** |

**This is the most important finding for the analysis.** The good news: the three
elements that matter most for telling Anatolian volcanoes apart — **Rb, Zr, Nb** —
are present in ~99% of readings. The bad news: **Strontium and Barium are
effectively missing**, and **Yttrium was never recorded**. Some published sourcing
schemes lean on Sr and Y; we will not be able to reproduce those directly and must
build our fingerprint comparison on **Rb–Zr–Nb (+Fe, Ti, Mn)**.

This also matches a gap already noted on the reference side: *Milic has no Nb, Y
is sparse*. So **Y is out on both sides** — no loss from dropping it.

### 5.2 The readings are not independent samples

1227 readings map to only **~521 excavation baskets**. The dominant pattern is
**2 readings per object — one `dorsal`, one `ventral`** (393 baskets follow this
exactly). Counts: 395 baskets with 2 readings, 58 with 4, 32 with 1, plus a tail
up to 12.

> **This matters for the statistics.** Treating 1227 readings as 1227 independent
> tools would roughly **double our apparent sample size** and make confidence
> intervals look about √2 times tighter than they are. In the cleaning step we
> must decide how to combine the two faces of one object — average them, or keep
> the better-quality face — and count objects, not readings.

Two baskets have two `ventral` readings and no dorsal — a likely labelling slip
worth a look.

### 5.3 Surface condition — affects pXRF accuracy

pXRF reads the **surface**, so dirt and incomplete beam coverage bias results.
These were recorded, which is excellent:

- **cover:** partial 426, full 282, very partial 161, almost full 132, tiny 12,
  blank 214.
- **Dirt:** flagged on 285 readings (`yes` 279, `dirty` 6); 942 blank.

Only **282 readings have full beam coverage.** "Very partial" and "tiny" coverage
(173 readings) should be treated as low-confidence — this is a natural input to
the honest confidence score we planned.

⚠️ The blanks are ambiguous: a blank `Dirt` probably means "clean", but it could
also mean "not recorded". We should treat blank as *unknown*, not as *clean*.

### 5.4 Smaller issues

- **Sites and periods are consistent** — no spelling variants. Motza 946, Einan
  228, Yiftahel 53; each site maps to exactly one period (Motza=EPPNB,
  Einan=Natufian, Yiftahel=MPPNB).
  ⚠️ Note the **strong imbalance: Motza is 77% of the data.** Yiftahel has only
  53 readings (~25 objects). Conclusions about Yiftahel will be much weaker.
- **Below-detection values are stored as the text `< LOD`**, which makes the whole
  column text instead of numbers. The cleaning code must convert these
  deliberately (recommend: treat as missing, not as zero — zero would drag
  averages down and is chemically false).
- **One stray value `s` in the Ba column** — a typing slip.
- **Missing context:** side blank on 37 readings, Basket blank on 8, Locus blank
  on 3.
- **Two very short readings** kept in the master: 1730 (12.73 s) and 1779
  (23.2 s). Both were already removed in the "First Changes" sheet — correctly.

### 5.5 The three sheets inside the master

| Sheet | Rows | What it is |
|---|---:|---|
| `Original` | 1227 | assembled raw readings |
| `First Changes` | 1224 | + `Period` column, elements reordered, 3 rows removed |
| `Ordered by Site` | 1224 | same as above, sorted |

The 3 removed rows are: 1730 (12.73 s, marked `aborted`), 1779 (23.2 s), and
1790 (102.8 s, no sample label but with locus N95c / basket 7835).

Rows 1730 and 1779 are clearly aborted (12.7 s and 23.2 s).

**Row 1790 — reviewed 2026-07-21, removal CONFIRMED correct.** It is at
`Original` **Excel row 959** (and in `02 obsidian einan natufian 23.2.17.xlsx`
row 27). An earlier version of this report flagged its removal as questionable
because it ran 102.8 s — nearly full length. That was judged on duration alone
and was wrong. Its chemistry is unusable:

| | r1790 | Einan median | Einan 5–95% |
|---|---|---:|---|
| **Rb** | **< LOD** | 0.010 | 0.008–0.012 |
| **Zr** | **< LOD** | 0.007 | 0.006–0.009 |
| **Nb** | **< LOD** | 0.003 | 0.002–0.003 |
| Fe | 3.822 | 1.114 | 0.752–1.701 |
| Ca, K, Si, Bal | all < LOD | — | — |

**All three sourcing elements are below detection** and Fe is 3.4× the Einan
median, well outside the normal range. Side, cover and Dirt are all blank. The
author dropped it deliberately when building `First Changes`; that judgement
stands.

> **Lesson recorded:** duration alone is a poor quality test. A near-full-length
> run can still be unusable. **Judge readings by whether Rb/Zr/Nb are actually
> measured**, not by how long the instrument ran.

---

## 6. ✅ The master workbook was renamed

**`data manipulation.xlsx` → `obsidian_pxrf_master_2017-2018.xlsx`**
(done 2026-07-21 by Avishai's instruction, via `git mv` so the file history is
preserved).

The old name described *an activity* rather than *contents*, and "manipulation"
reads badly in a scientific project where the file is in fact the faithful
assembled record. The new name states the material, the method, that it is the
master compilation, and the date range.

Only the filename changed — the contents are untouched, and all three sheets
(`Original`, `First Changes`, `Ordered by Site`) verified intact afterwards.

*Note: the frozen `Analysis with GitHub Copilot/` folder still refers to the old
name. That is deliberate — it is a historical record and is not edited.*

---

## 7. What this means for the cleaning step

1. Key every reading on **`Reading No` + `Time`**. Never `Reading No` alone —
   and handle the **3 rows with a blank `Time`** explicitly rather than letting
   them drop out silently (that is what hid reading 1490).
2. Build on **Rb, Zr, Nb** (+ Fe, Ti, Mn as support). **Drop Sr, Ba, Y, Ga, Th.**
3. Convert `< LOD` to **missing**, never to zero.
4. Aggregate **to the object** (site+locus+basket), not the reading — and report
   object counts as the sample size.
5. Carry `cover` and `Dirt` through as **quality flags** feeding the confidence
   score; treat blanks as *unknown*.
6. Add **reading 1489** back (flagged low quality); leave **1490** out with the
   reason recorded (§4). **Row 1790 stays out** — confirmed correct (§5.5).
8. Prefer **element ratios over raw concentrations** — raw values drift with
   `Bal`/beam geometry, ratios do not (§4).
7. Expect weak statistics for **Yiftahel** (~25 objects) and say so plainly.

---

## 8. How to reproduce this

```
python analysis/02_map_raw_samples.py
```

Reads only from `data/samples/`, writes nothing there, and prints every table in
this report.
