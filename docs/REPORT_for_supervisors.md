# Obsidian Provenance Project — Data Preparation Report

**Prepared for supervisory review — 21 July 2026**

Sites: Motza, Einan/Ain Mallaha, Yiftahel (Israel)
Method: portable X-ray fluorescence (pXRF)
Data: 1,228 measurements taken 2017–2018

---

## Summary for the reader in a hurry

We prepared the excavation obsidian measurements for source analysis. The data
is now clean, traceable and ready.

**Two findings must be understood before any conclusion is drawn:**

1. **The measurements are very coarse.** The instrument recorded in percent with
   three decimals, so its smallest step is 10 ppm. Rubidium therefore takes only
   **9 different values** in the entire dataset, and Niobium only **6**.
2. **Our numbers sit below the entire published range.** Our samples read
   Rb ≈ 90 ppm; every Anatolian volcano in the reference literature is 110 ppm or
   more, most 130–270. No certified standard was ever measured, so we cannot
   correct for this.

**Consequence:** we can describe and group the assemblage, but we **cannot yet
name the volcano of origin**. The fix is cheap — one measurement session using a
standard reference glass (RGM-2) on the same instrument — and is described in
Section 8.

---

## 1. What the project is trying to do

Obsidian is natural volcanic glass. It does not occur in Israel, so every
obsidian tool found here was carried from elsewhere — mostly from volcanoes in
Anatolia (modern Turkey). Each volcano has its own chemical "fingerprint": the
proportions of trace elements such as Rubidium (Rb), Zirconium (Zr) and Niobium
(Nb) in the glass.

If we measure the chemistry of a tool and compare it with the fingerprints of
known volcanoes, we can say where the raw material came from. That tells us about
long-distance contact and exchange in the Neolithic and Natufian periods.

**Our task in this stage** was not to answer that question, but to prepare the
measurements so that the answer, when we give it, is trustworthy.

---

## 2. Why the data needed careful preparation

The measurements were made in 2017–2018 over many sessions and later gathered by
hand into one large workbook. Before using it we checked it thoroughly. What we
found:

- The same instrument was also used for **other research projects** — Roman
  bronze from Caesarea, pottery from Tel Tsaf, metal objects. Those readings sit
  in the same files and had to be separated out.
- The instrument's **reading numbers repeat**. Its counter was reset between 2017
  and 2018, so 94 numbers appear twice. Reading 1682, for example, is both a
  Yiftahel tool and a Motza tool. Using the reading number alone as an identifier
  would merge tools from different sites.
- One object had been **lost through a spelling mistake** — its label read
  "obidian" instead of "obsidian", so it was missed when the workbook was
  assembled.
- Most tools were **measured twice**, once on each face.

None of this is unusual for field data. But each point changes the result if it
is not handled deliberately.

---

## 3. What "cleaning" means here, step by step

Our guiding rule: **nothing is deleted silently.** Every original measurement is
still in the output file, marked either *kept* or *removed*, and every removal
carries its reason. Anyone can check our decisions. The original files were never
modified.

### Step 1 — Identify each measurement correctly

We identify a measurement by **reading number together with its timestamp**,
never the number alone. This prevents the 2017/2018 duplicates from merging.

### Step 2 — Read the researcher's own notes first

The researcher marked bad measurements directly in the spreadsheet cells — for
example writing "Invalid" where the time should be, or "aborted" in the location
field. Standard software turns such text into an empty cell, which makes the
warning disappear. We therefore read the raw text **before** any processing, and
treat these notes as decisions by the person who was present at the measurement.
Their judgement outranks any rule we could invent.

### Step 3 — Handle "below detection limit" correctly

When an element is present in too small a quantity, the instrument reports
`< LOD` ("below limit of detection") instead of a number. **We treat these as
missing, never as zero.** Recording them as zero would be chemically false and
would pull the averages down, making samples look poorer in that element than
they are.

### Step 4 — Remove measurements that cannot be used

Three rules. They removed **19 of 1,228** measurements (1.5%):

| Rule | Removed | Reason |
|---|---:|---|
| The researcher marked it bad | 1 | His note at the time of measurement |
| Rb, Zr or Nb was not measured | 17 | Without these there is nothing to compare |
| The run was clearly aborted (< 60 seconds) | 1 | Incomplete measurement |

**The second rule is the important one, and it replaced an earlier idea of ours.**
We had first assumed that a measurement lasting the normal ~120 seconds was
sound. One case proved that wrong: a measurement ran 102.8 seconds — nearly full
length — yet Rb, Zr **and** Nb were all below the detection limit, and its Iron
was three times the normal value. It looked fine by duration and was useless in
fact. **The correct test is whether the elements we need were actually measured,
not how long the instrument ran.**

### Step 5 — Combine the two faces into one object

Most tools were measured on both faces (dorsal and ventral). These are **not two
independent samples** — they are one object measured twice.

We group measurements that share **site + locus + basket**, which the excavator
confirms identifies a single object. Site is part of the key, so measurements
from different sites can never be combined.

**Result: 1,209 measurements represent 521 objects.**

This matters statistically. Treating 1,209 measurements as independent would
overstate our sample size by more than double and make our confidence intervals
appear roughly **1.4 times narrower** than they truly are — a false impression of
precision. All results below count **objects**.

### Step 6 — Score the quality of every object

Each object receives a score from 0 to 1, combining six things we actually
recorded (Section 6). Low-quality objects are **not deleted** — they are carried
forward with wider uncertainty. This keeps the decision visible instead of hidden.

---

## 4. The mathematics and statistics we use — and why

This section explains every calculation in the analysis in plain terms.

### The median (not the average)

The **median** is the middle value when numbers are placed in order. The
**average (mean)** adds everything and divides by the count.

We use the **median** to combine the measurements of one object.

*Why:* the average is easily distorted by a single wrong value. If one face of a
tool gives a bad reading, the average moves towards it and the final number
describes neither face. The median simply takes the middle and ignores how
extreme the outlier is.

> **Important limitation, stated honestly:** when an object has exactly **two**
> measurements, the median and the average are the same number. So for the 392
> two-measurement objects, the median gives no protection at all. Those objects
> depend entirely on the disagreement rule described next.

### Percentiles

The **95th percentile** is the value below which 95% of the data falls. We use
percentiles instead of minimum and maximum because a single extreme value can
make the true range look far wider than it is.

### Standard deviation (sd)

A measure of **spread** — how far values typically sit from their centre. A small
sd means the values cluster tightly; a large sd means they are scattered.

### Ratios instead of raw amounts

Rather than comparing raw concentrations, we mainly compare the **ratio Rb ÷ Zr**.

*Why:* raw amounts are affected by how the instrument sits on the object — the
angle, the surface, how much of the beam actually strikes the sample. We
demonstrated this in the data: as the unmeasured fraction rises, the absolute
Rubidium value drops from 0.010% to 0.008%, but **the Rb/Zr ratio stays constant
at about 1.33 throughout**. Both elements are affected together, so dividing one
by the other cancels much of the distortion.

This is standard practice in obsidian provenance work, and our data supports it
independently.

### The "fold-difference" and why we do not average across disagreement

The **fold-difference** is how many times larger the biggest measurement is than
the smallest. Two readings of 0.008 and 0.1 differ by 12.5-fold.

We measured how much the two faces of one object **normally** disagree, across
392 two-measurement objects:

| Element | median disagreement | worst case observed |
|---|---:|---:|
| Rb | 0% | 1.38× |
| Zr | 0% | 1.57× |
| Nb | 0% | 1.50× |

The two faces of a tool normally agree almost perfectly. This is expected:
obsidian is **glass**, chemically uniform by its nature — which is precisely why
provenance study is possible at all.

**Our threshold is therefore 1.6×**, taken from the data rather than chosen
arbitrarily. Beyond that, the readings are treated as disagreeing.

**When they disagree we do not average them.** Averaging 0.008 and 0.1 produces
0.054 — a value describing neither measurement and matching no real material. It
would then be compared against the volcano fingerprints and could yield a
confident but entirely wrong answer.

Instead we ask which reading is implausible **on independent grounds** — is it
outside the range of everything else we measured? If yes, that reading is
removed. If both readings are individually plausible and still disagree, we
**flag the object for human inspection and produce no value**, because the
disagreement may mean the basket contains two different pieces rather than one.

*This distinction matters:* "it disagrees with its partner" is not a valid reason
to delete a measurement — that would assume the conclusion. "It lies outside the
plausible range of the entire assemblage" is a valid reason.

### The quality score

A weighted average of six components, each between 0 and 1:

| Component | Weight | Meaning |
|---|---:|---|
| Agreement between measurements | 35% | Does the object agree with itself? The strongest evidence we have |
| Surface coverage | 25% | How much of the beam struck the sample |
| Dirt recorded | 15% | pXRF reads the surface, so dirt biases it |
| `Bal` within normal range | 15% | See below |
| Number of measurements | 10% | More measurements, more confidence |

Where information is missing, we score it **0.5 = unknown** — never "good". An
unrecorded dirt field does not mean the object was clean.

### `Bal` — what it means

`Bal` ("balance") is the share of the sample the instrument **could not
identify**. We verified this: all measured elements plus `Bal` sum to exactly
100% (median 99.993%).

For obsidian, that unidentified share is mostly **oxygen**. Volcanic glass is
about 46% oxygen by mass, and pXRF cannot detect oxygen at all. A `Bal` of 55–65%
is therefore completely normal — not an error.

> *We initially believed `Bal` indicated how well the beam covered the sample.
> We tested this against the recorded coverage field and it was not supported
> (full coverage 57.9, "tiny" coverage 50.7 — no consistent pattern). We
> corrected this and now use `Bal` only as a signal that a reading is unusual.*

---

## 5. Results of the cleaning

| | Count |
|---|---:|
| Measurements examined | 1,228 |
| Removed (with reason recorded) | 19 |
| Measurements used | 1,209 |
| **Objects for analysis** | **521** |
| Objects flagged for inspection | 2 |

**Quality distribution:** 367 high, 135 medium, 19 low. Mean score 0.78.

### Chemistry by site — the central result so far

| Site | Objects | Rb (ppm) | Zr (ppm) | **Rb/Zr** | sd |
|---|---:|---:|---:|---:|---:|
| Motza | 388 | 90 | 65 | **1.375** | 0.118 |
| Einan | 105 | 100 | 70 | **1.357** | 0.124 |
| Yiftahel | 28 | 88 | 60 | **1.393** | 0.351 |

**The three sites are chemically indistinguishable.** Their Rb/Zr ratios differ
by less than 3%, while the spread within each site is around 9%.

**How this should be interpreted.** It is consistent with all three sites drawing
obsidian from the same source. But we must state the limitation plainly: the
spread (sd ≈ 0.12) is approximately **one step of the instrument's resolution**.
The apparent variation may be nothing but rounding. The honest formulation is:

> *We find no evidence of more than one source, and we do not have the resolution
> to rule one out.*

It is **not** proof of a single source.

Note also the sample imbalance: Motza contributes 388 objects, Yiftahel only 28.
Any statement about Yiftahel is correspondingly weaker, and its larger spread
(sd 0.351) may simply reflect the small number.

---

## 6. First serious limitation — the measurements are very coarse

The instrument recorded concentrations in **percent with three decimal places**.
The smallest step it can express is 0.001% = **10 ppm**. For trace elements
present at 20–90 ppm, that step is enormous.

| Element | Distinct values in 1,212 measurements | Typical value | One step equals |
|---|---:|---:|---:|
| Rb | **9** | 90 ppm | **11%** of the value |
| Zr | **15** | 70 ppm | **14%** |
| Nb | **6** | 20 ppm | **50%** |

Niobium is effectively binary — 829 measurements read 0.002 and 372 read 0.003.

**This cannot be repaired.** We checked every original instrument export: the
same resolution appears throughout, so nothing was lost in transcription. The
instrument's own error columns confirm it — they contain only 0.001 or 0.002,
meaning **the stated uncertainty is the same size as the rounding step**.

In practical terms:
- Rb = 90 ± 10–20 ppm → **±11–22%**
- Zr = 70 ± 10–20 ppm → **±14–29%**
- Nb = 20 ± 10–20 ppm → **±50–100%**

**Consequences:** Niobium cannot support a fine distinction and is demoted to a
rough check only. Rb and Zr carry real but blunt information. We can separate
volcanoes whose chemistry differs substantially; we cannot resolve volcanoes that
are chemically similar. For many objects the honest answer will be
**"undetermined"** — and reporting that is the correct scientific outcome, not a
failure.

---

## 7. Second and more serious limitation — the calibration gap

We compared our measurements with the reference database of volcano fingerprints
(326 geological samples from published studies).

**Our samples read Rb ≈ 90 ppm. Every Anatolian source in the literature is
110 ppm or higher, and the main candidates are 155–270 ppm.**

| Source | Rb (ppm) | Zr (ppm) |
|---|---:|---:|
| **Our samples** | **90** | **70** |
| Kars-Digor (lowest published) | 110 | 172 |
| Nenezi Dağ | 155 | 137 |
| Göllü Dağ | 178 | 75 |
| Acıgöl | 270 | 65 |
| Bingöl A | 243 | 1354 |

Our values fall **below the entire published range**. The only two sources
overlapping ours are Melos Adamas and Giali — both **Aegean**, which for
Levantine Neolithic obsidian would be an extraordinary claim requiring
extraordinary evidence.

**The ordinary explanation is instrumental.** The measurements were taken using
the instrument's factory "Mining" calibration, which is designed for soils and
ores, not for rhyolitic glass. Reading 50–75% low on trace elements in such
circumstances is well documented.

We tested this hypothesis formally: if a single calibration offset explains the
discrepancy, then for the true source the correction factor for Rb must equal the
factor for Zr. Of 32 sources, **five** satisfy this (Acıgöl2, Nenezi Dağ,
Carpathian 2, Sarıkamış, Giali), implying the instrument reads roughly **50–75%
of true concentration**.

**But we cannot confirm it.** Confirmation requires a certified reference
material measured on the same instrument. We searched every original workbook for
any such measurement — RGM, NIST, SRM, standard, control. **There is none.** The
only non-sample readings are 14 instrument self-tests reported in
counts-per-second, which contain no concentrations.

**Ratios do not solve this.** Our earlier plan assumed they would, but two things
prevent it: the implied offset is **not uniform** across elements, and our Rb/Zr
of 1.33 is compatible with **6 of the 32 sources** in any case.

---

## 8. What we propose to do next

### Immediate priority — measure a reference standard

**Measure RGM-2 on the same pXRF instrument, with the same settings.**

RGM-2 is a rhyolite glass reference material distributed by the United States
Geological Survey. It is obsidian, matrix-matched to our samples, and is the
standard used throughout this literature. A single short session would give the
correction factor for Rb, Zr and Nb, and would place our measurements on the same
scale as the published fingerprints.

**This is the single highest-value action available to the project.** It is
inexpensive and would probably resolve the entire difficulty.

*If the instrument is no longer accessible:* measuring several obsidian pieces of
independently known source would serve the same purpose. *If neither is possible:*
a small subset analysed by ICP-MS or NAA would anchor the dataset, at greater
cost.

### A second question requiring a decision

Our methodological rule is to compare like with like — portable instrument
against portable instrument — because mixing instrument types was the flaw in the
project's earlier analysis. However, of the reference database:

| Method | Measurements | Sources |
|---|---:|---:|
| pXRF (portable) | 52 | 8 |
| Multiple methods | 230 | 17 |
| EDXRF (laboratory) | 44 | 11 |

Only one study (Milic 2014) used a portable instrument, and its Anatolian
coverage is limited to **Göllü Dağ and Nenezi Dağ**. A strict like-for-like
comparison therefore has very few relevant sources. We must decide whether to
relax the rule and state the added uncertainty, or to seek further portable-
instrument reference data.

### What can be reported now, without further measurement

The following is defensible on the present data:

> *The obsidian assemblages from Motza, Einan and Yiftahel are chemically
> homogeneous at the resolution available, showing no evidence of more than one
> raw-material source across the three sites and the periods represented. The
> source itself cannot be identified from these measurements, because the
> instrument was not calibrated against a reference standard.*

The following is **not** currently defensible:

> ~~*The obsidian derives from Göllü Dağ.*~~

We recommend against publishing any named-source attribution until the
calibration question is resolved.

---

## 9. Files produced

| File | Contents |
|---|---|
| `samples_db/obsidian_samples_CLEAN.xlsx` | The cleaned data, formatted for reading. Six sheets: README, Objects, Site_summary, Needs_review, Readings, Dropped |
| `samples_db/samples_objects.csv` | 521 objects — the analysis table |
| `samples_db/samples_readings.csv` | All 1,228 measurements with keep/remove decisions |
| `samples_db/cleaning_report.txt` | Full log of every step and every removal |
| `analysis/03_clean_samples.py` | The code, re-runnable from the raw files |

The Excel workbook is the one to open. Its **Objects** sheet is the analysis
table; **Needs_review** lists the two objects requiring inspection; **Dropped**
shows every removed measurement with its reason.

All original files in `data/` remain unmodified. Every number can be traced back
to its source file and original spreadsheet row.

---

## 10. Assessment

The data preparation is complete and sound. The assemblage is well characterised
and internally consistent.

The obstacle to source attribution is not the quality of the excavation data or
of the preparation — it is a missing calibration measurement, which was simply
not taken at the time and could not have been anticipated then. It is
straightforward to remedy.

We consider it preferable to identify this now than to discover it after
publishing source attributions that could not be supported. The earlier analysis
of this material, which we set aside, made precisely that error: it produced
confident assignments resting on differences smaller than the instrument could
measure.
