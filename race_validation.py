import pandas as pd
import csv

df = pd.read_csv('race_2018.csv', encoding="SHIFT_JIS")

max_race_id = df.max()['Race_num']
print(max_race_id)

with open('race_valid_2018.csv', 'w') as f:
    valid_writer = csv.writer(f)
    valid_writer.writerow(['Race_num', 'Valid'])
    for race_id in range(1, max_race_id+1):
        target_race_df = df[df['Race_num'] == race_id]
        race_valid = True
        for race_rank in (target_race_df['Rank']):
            if not race_rank[0].isdigit():
                race_valid = False
                break
        
        if len(target_race_df) <= 0:
            race_valid = False
        valid_writer.writerow([race_id, race_valid])