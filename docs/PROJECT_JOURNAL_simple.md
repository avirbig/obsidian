# Obsidian Project — Simple Journal

*A plain-English record of what this project does, what we did, and what we
decided. Written to be easy to read and to present to others. For the technical
details, see `reference_data_verification_report.md` and `CHANGELOG.md`.*

*Last updated: 2026-07-21.*

---

## 1. What this project is about

Obsidian is a natural volcanic glass. People in the Stone Age used it to make
sharp tools. Obsidian is **not found in Israel** — it had to be carried here from
far away, mostly from **volcanoes in Turkey**.

Every volcano has its own **chemical "fingerprint"** (the amounts of elements
like Rubidium, Zirconium, Niobium in the glass). By measuring the chemistry of an
obsidian tool and comparing it to the fingerprints of the volcanoes, we can find
out **which volcano the tool came from**. This tells us about **ancient trade and
contacts**.

We study obsidian from **three sites in Israel**:
- **Motza** (near Jerusalem)
- **Einan / Ain Mallaha** (Hula Valley)
- **Yiftahel** (Lower Galilee)

Our own tools were measured with a **portable X-ray machine (pXRF)** — a device
that reads the chemistry without destroying the object.

**The goal:** build a trustworthy library of volcano fingerprints, then compare
our tools to it and say where each one came from — honestly, with clear
confidence levels.

---

## 2. Why we started again from the beginning

An earlier version of this analysis was done (with the help of an AI tool called
GitHub Copilot). When we checked it carefully, we found a **serious problem**:

- It compared our tools (measured with the **portable** machine) against
  reference data measured with **different laboratory machines**, as if they were
  the same. Different machines give slightly different numbers, so this can point
  to the **wrong volcano**.
- Only about **40%** of its results were statistically solid; the rest were weak
  guesses presented as answers.
- The old code could **not be run again** on this computer.

So we decided to **keep the old work frozen** (not delete it) and **start fresh**,
carefully. The full check of the old work is in
`prior_work_audit_made_with_github_copilot.md`.

---

## 3. How the project is organized

| Folder | What is inside |
|---|---|
| `data/` | The **raw data — never changed**: the articles, the tables from articles, our own measurements. |
| `docs/` | Explanations and decisions (including this journal). |
| `analysis/` | Our **new** code that builds everything. |
| `reference_db/` | The clean volcano-fingerprint library we are building. |
| `results/` | Figures and the final report (later). |
| `Analysis with GitHub Copilot/` | The **old** work, frozen, for reference only. |

---

## 4. What we have done, step by step

**Step 1 — Tidied the project.** Separated the real raw data from the old
analysis. Froze the old work. Wrote the goal and the rules.

**Step 2 — Checked the reference data from the articles.** For every table of
volcano chemistry taken from a scientific article, we asked: *Does it really
exist? Is it reliable? Can we trace it back to the article?* During this we:
- Found a **wrong label**: a table called "Kenan Tepe" was actually from a
  different site, **Körtik Tepe**. We proved it and corrected it.
- **Removed** papers we cannot trust or use (no article available, or empty
  tables): Oddone 1997, Yellin 1996, Gratuze 1999, Frahm 2014.
- **Fixed messy spreadsheets** (Milic, Körtik, Carter 2006) so the numbers line
  up correctly.
- Made a **ranked list** of all papers, from most useful (portable-machine data
  from Turkish volcanoes) to least useful.

**Step 3 — Built the first version of the fingerprint library.** We wrote new
code that reads each cleaned table and collects the chemistry, **keeping each
paper separate**. The result is in `reference_db/`.

**Step 4 — Checked our own measurement files (before touching them).** Before
cleaning anything, we made a map: where does every measurement come from, and
what condition is it in? Full details in `raw_sample_data_map_and_quality.md`.
What we learned:

- **The big workbook is complete and honest.** All
  **1227 measurements** in it can be traced back to an original machine file.
  We had wondered whether some samples existed *only* there, with no original
  file behind them — **they do not**. Nothing is unsourced.
- It is a **filtered copy**, not a merge. The machine was also used for **other
  projects** (Roman bronze from Caesarea, pottery from Tel Tsaf, metal objects),
  and those readings sit in the same files. 518 readings were left out, and
  515 of them were left out correctly — they are not obsidian.
- **One Motza object was lost.** On 27.11.2017 a tool was measured **twice**
  (the usual two faces), and **both measurements are missing** from the big
  workbook. The reason is almost certainly a **typing mistake**: the label says
  "**obidian** motza" instead of "obsidian", so it was missed when the workbook
  was put together by hand. The measurements are in
  `Avishai_Obsidian 12.2017.xlsx`, rows 832–833.
  **What we decided:** the second measurement (row 833) is **not good** — Avishai
  had marked its time as "Invalid" while working, it ran only 81 seconds instead
  of 120, and part of the machine's reading never finished. So we **leave it
  out**, and we write down *why*. The first measurement (row 832) is complete and
  its chemistry matches normal Motza obsidian, so we **put it back in**, marked
  as slightly lower quality. This object will therefore have **one** measurement
  instead of two.
- **Two elements we hoped to use are not really there.** *Strontium* and
  *Barium* were below the machine's detection limit in ~95% of measurements,
  and *Yttrium* was never recorded at all. **But the three most important ones
  — Rubidium, Zirconium, Niobium — are present in 99%.** Those are exactly the
  elements that separate the Turkish volcanoes best, so the plan still works.
- **Each tool was usually measured twice** (both faces, "dorsal" and "ventral").
  So 1227 measurements are really about **521 objects**. We must count objects,
  not measurements — otherwise our results would look twice as certain as they
  really are.
- **The three sites are very unequal:** Motza 946, Einan 228, Yiftahel only 53
  measurements. Anything we say about Yiftahel will be much less certain, and
  we will say so.

---

## 5. Decisions we made (and why)

| Decision | What we chose | Why |
|---|---|---|
| Start over vs. fix the old work | **Start over** | The old work had a method mistake we could not trust. |
| Raw data | **Never change it** (read-only) | So we can always trace every number back to its origin. |
| Comparing machines | **Compare same machine type to same type** (portable-to-portable) as the main result | Mixing machine types was the old work's main mistake. |
| Sources per paper | **Keep each paper's sources separate for now** | Cleaner; we can join them later on purpose, not by accident. |
| Göllü Dağ East vs. general | **Keep them separate** | "East Göllü Dağ" may not be exactly the same as general "Göllü Dağ". |
| Which reference data to use | **Decision B: only real volcano-rock samples** (not tools that were *guessed* to come from a volcano) | Most certain data. We accept that we have fewer samples for some volcanoes (e.g. Bingöl A, Nemrut). |

*Note:* Decision B can be changed later — we kept **all** the data in
`reference_long.csv` (marked as either "source sample" or "artifact"), so nothing
is lost. The active reference is `reference_source_only.csv`.

---

## 6. Where we are now

- ✅ Project tidy; old work frozen.
- ✅ Reference data checked, corrected, and ranked.
- ✅ First version of the fingerprint library built:
  **326 real volcano-rock measurements** from 3 papers, covering the main Turkish
  sources (Göllü Dağ, Nenezi, Acıgöl, Hasan, Bingöl, Nemrut, Meydan, Sarıkamış,
  Suphan, and others).
- ⚠️ Two volcanoes have few samples: **Bingöl A (4)** and **Nemrut (5)**.
- ✅ Our own measurements are **mapped and checked** — we know where every number
  comes from and what its problems are. Nothing has been changed yet.
- ⏳ Cleaning our own measurements is the **next** step.

---

## 7. What comes next

1. **Decisions for Avishai** (from Step 4):
   - ✅ *Decided:* the lost Motza object — keep the good measurement, drop the
     one marked "Invalid" (see Step 4).
   - ✅ *Decided:* the Einan measurement from 23.2.2017 (the one Avishai had
     already removed) **stays out**. We checked it: even though the machine ran
     almost the full time, the three elements we need (Rb, Zr, Nb) were **all
     too weak to measure**, and its Iron was 3 times too high. Avishai's original
     judgement was right. *Lesson: a long measurement is not automatically a good
     one — what matters is whether the useful elements were actually detected.*
   - **A question we need Avishai to answer before cleaning:** is one excavation
     basket always **one** obsidian object? We plan to combine measurements that
     share a basket, assuming they are the two faces of the same tool. If a
     basket can contain several different pieces, we would wrongly mix them
     together — so this needs checking first.
   - ✅ *Done:* the big workbook was **renamed** from `data manipulation.xlsx` to
     **`obsidian_pxrf_master_2017-2018.xlsx`**. "Manipulation" sounded bad in a
     scientific project, and the file is really the faithful master record. Only
     the name changed — the contents are untouched.
2. (Optional) Add a few more reference papers if we find gaps.
3. Clean our own tools' measurements — the full plan is written in
   `cleaning_plan.md`. In short: throw out measurements where the useful
   elements were not detected, **combine the two faces of each tool into one
   object** (about 521 objects, not 1227 measurements), use **ratios between
   elements** instead of raw amounts (they are far less affected by dirt and by
   how the machine was held), and give every object a **quality score**.
4. Compare our tools to the fingerprint library and say where each came from —
   with a clear confidence level, and an honest "unknown" when we cannot tell.
5. Make figures and write the final report.
