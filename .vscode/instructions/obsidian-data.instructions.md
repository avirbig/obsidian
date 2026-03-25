---
applyTo: "analysis/**,reference_database/**,my_samples/**,changelog.md"
---

# Obsidian Data Handling Rules

## Changelog Discipline — MANDATORY

Every time you create, modify, or delete data in this project, you MUST update `changelog.md`.

1. Open `changelog.md`
2. Add a new entry at the TOP of the log section (newest first), in this exact format:
   ```
   [YYYY-MM-DD] | TYPE | File or target | What was done | Why / which article justifies it
   ```
3. If the action was triggered by a user request, FIRST log the prompt:
   ```
   [YYYY-MM-DD] | USER_PROMPT | — | "exact user text here"
   ```

Entry types: `USER_PROMPT` | `STRUCTURE` | `DATA_ADD` | `DATA_EDIT` | `DATA_REMOVE` | `VERIFICATION` | `BUG_FIX` | `NOTE`

---

## Raw Data Rules

- Files in `articles/` are **READ-ONLY** — never modify them
- Files in `obsidian_minerales_component_tables_from_articles/` are **READ-ONLY** — never modify them
- `my_samples/samples_raw.csv` is **READ-ONLY** once placed — all cleaning goes to `samples_clean.csv`
- All cleaned outputs go to `reference_database/`, `my_samples/samples_clean.csv`, or `analysis/`

---

## Column Naming Standards

When extracting or cleaning data, always use these exact column names:

**Trace elements (ppm)**: `Rb`, `Sr`, `Zr`, `Nb`, `Y`, `Fe`, `Mn`, `Ba`, `Zn`, `Ti`, `Th`, `U`, `Pb`

**Major oxides (wt%)**: `SiO2_pct`, `TiO2_pct`, `Al2O3_pct`, `FeO_pct`, `MnO_pct`, `MgO_pct`, `CaO_pct`, `Na2O_pct`, `K2O_pct`

**Required metadata columns**: `sample_id`, `source`, `site`, `paper`, `year`, `method`, `method_tier`, `units`, `notes`, `verification_flag`

---

## Source Label Standards

Always normalize to these exact labels — no exceptions:

| Use this | Instead of |
|----------|-----------|
| `EGD` | East Göllü Dağ, GLD-E, Gollu Dag East, WGD-E |
| `WGD` | West Göllü Dağ, GLD-W, Gollu Dag West |
| `ND` | Nenezi Dağ, Nenezi Dag, NND |
| `BingolA` | Bingöl A, Bingol-A |
| `BingolB` | Bingöl B, Bingol-B |
| `NemrutDag` | Nemrut Dağ, Lake Van, NMRD, Nemrut Dag |
| `Urmia` | Lake Urmia |
| `Sevan` | Lake Sevan, ZNKT |

---

## Method Tier Tags

Every row must have a `method_tier` column set to one of these integers:

| Value | Methods |
|-------|---------|
| `1` | pXRF |
| `2` | EDXRF (laboratory) |
| `3` | LA-ICP-MS, ICP-AES/MS, PIXE, WDXRF |
| `4` | NAA/INAA, Electron Microprobe |

---

## Handling Range Strings (e.g., Milic 2014)

When a cell contains a range like `"166-194"`:
1. Parse to numeric midpoint: `(166 + 194) / 2 = 180`
2. Store the midpoint in the element column (e.g., `Rb = 180`)
3. Preserve original string in a companion column: `Rb_range_flag = "166-194"`
4. Log in changelog:
   ```
   [date] | DATA_EDIT | Milic 2014.xlsx | Parsed range "166-194" to midpoint 180 for Rb, sample M14-XX | Milic 2014 Table X, range format
   ```

---

## Missing Data Rules

- Empty cells → always store as `NaN` — **never fill with 0**
- Below detection limit (BDL / <LOD) → `NaN` + note `"BDL"` in `notes` column
- Empty xlsx sheets (Frahm 2014, Gratuze 1999) → skip entirely; log:
  ```
  [date] | DATA_REMOVE | data2.xlsx | Sheet "Frahm 2014" is empty, skipped | audit_cross_reference.md Section D item 1
  ```

---

## Unit Conversion

If oxide wt% must be converted to element ppm, use these formulas:

- **FeO → Fe ppm**: `Fe_ppm = FeO_pct * 10000 * (55.845 / 71.844)`
- **Fe2O3 → Fe ppm**: `Fe_ppm = Fe2O3_pct * 10000 * (2 * 55.845 / 159.692)`
- **MnO → Mn ppm**: `Mn_ppm = MnO_pct * 10000 * (54.938 / 70.937)`

Always log the conversion formula in changelog.

---

## Verification Protocol

After extracting a table from an xlsx into a reference CSV:
1. Spot-check at least **3–5 values** against the matching article `.txt` file
2. Compare: sample IDs, element values, and source labels
3. Always log the verification:
   ```
   [date] | VERIFICATION | reference_database/sources/EGD.csv | Spot-checked 5 rows against Carter_and_Shackley_2007.txt Table 2 — no discrepancies | Carter_and_Shackley_2007.txt
   ```
4. If a discrepancy is found:
   - Use the **article value** as authoritative (xlsx may have a copy error)
   - Set `verification_flag = True` for that row
   - Log: `[date] | BUG_FIX | file | Corrected Rb for sample X from Y to Z — xlsx had typo, article p.N confirms Z`

---

## Sample Cleaning Rules (researcher's pXRF data)

When working with `my_samples/samples_raw.csv`:
1. Never modify `samples_raw.csv` — write output only to `samples_clean.csv`
2. Check for:
   - Duplicate `sample_id` values → flag, do not silently merge
   - Column names that don't match reference database → rename and log
   - Values below the typical pXRF detection floor (Rb < 0, Sr < 0, etc.) → flag as suspect
   - Units — confirm all values are in ppm, not wt%
3. Log every cleaning step with the sample_id affected

---

## Outlier Handling

Never silently remove outliers. Protocol:
1. Flag the value with `notes = "outlier_suspect: X SD from source mean"`
2. Check against the original article — was it correctly copied?
3. Consult audit_cross_reference.md for known issues with that paper
4. Log the decision:
   - If kept: `[date] | NOTE | file | Sample X Rb=450 kept despite being 3.2 SD from EGD mean — confirmed in article Table 2`
   - If removed: `[date] | DATA_REMOVE | file | Removed sample X — Rb=450 is 3.2 SD from EGD mean, likely misassigned source label in original paper`
