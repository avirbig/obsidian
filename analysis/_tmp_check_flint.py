import pandas as pd

df = pd.read_csv('my_samples/samples_raw.csv')
fl = df[df['remarks'].astype(str).str.contains('Flint', na=False, case=False)]
print(f'Flint-marked rows: {len(fl)}')
print(fl[['item_id', 'site', 'basket', 'reading_no', 'remarks', 'Rb', 'Zr', 'Nb']].to_string())
print()
# Check item_ids that have ANY reading with Flint remark
flint_items = fl['item_id'].unique()
print(f'Unique item_ids with Flint remark: {sorted(flint_items)}')
all_readings = df[df['item_id'].isin(flint_items)]
print(f'\nAll readings for those items:')
print(all_readings[['item_id', 'reading_no', 'remarks', 'Rb', 'Zr', 'Nb']].to_string())
