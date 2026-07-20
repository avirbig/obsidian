import json

nb_path = r'c:\work\code\obsidian\analysis\notebooks\01_data_extraction.ipynb'
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

new_source = (
    "# Spot-check Schechter et al. 2016 against article (Schechter_et_al_2016.txt)\n"
    "# Article Table (line 690): EZPR 10585.1: Mn=447, Fe=5127, Zn=30, Ga=21, Th=15, Rb=126\n"
    "article_vals = {'Mn': 447, 'Fe': 5127, 'Zn': 30, 'Ga': 21, 'Th': 15, 'Rb': 126}\n"
    "row = df_schechter[df_schechter['sample_id'] == 'EZPR 10585.1'].iloc[0]\n"
    "for el, expected in article_vals.items():\n"
    "    actual = row[el]\n"
    "    status = 'PASS' if abs(actual - expected) < 0.5 else f'FAIL got {actual}'\n"
    "    print(f'  {el:3s}: expected={expected}  {status}')\n"
    "print()\n"
    "print('NOTE: Schechter 2016 labels Gollu Dag without E/W distinction -> mapped to GolluDag')\n"
    "print('VERIFICATION: 2026-03-25 | EZPR 10585.1 spot-check | log in changelog')\n"
)

updated = False
for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if 'Spot-check: compare a few values against article (Schechter' in src:
        cell['source'] = [line + '\n' for line in new_source.splitlines() if line]
        cell['source'][-1] = cell['source'][-1].rstrip('\n')
        updated = True
        print('Cell updated')
        break

if not updated:
    print('Cell not found!')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved')
