# Obsidian Project — Simple Journal

*A plain-English record of what this project does, what we did, and what we
decided. Written to be easy to read and to present to others. For the technical
details, see `reference_data_verification_report.md` and `CHANGELOG.md`.*

*Last updated: 2026-07-20.*

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
- ⏳ We have **not yet** touched our own tools' data — that comes next.

---

## 7. What comes next

1. (Optional) Add a few more reference papers if we find gaps.
2. Clean our own tools' measurements (the pXRF data from the three sites).
3. Compare our tools to the fingerprint library and say where each came from —
   with a clear confidence level, and an honest "unknown" when we cannot tell.
4. Make figures and write the final report.
