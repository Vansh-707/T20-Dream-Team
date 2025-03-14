import pandas as pd

df_match = pd.read_csv('csv_files/t20_csv_files/dim_match_summary_1.csv', index_col= False)

# Rename 'scorecard' column to 'match_id' :- 
df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)

# Create a match ids dictionary that maps team names to a unique match id :- 
match_ids_dict = {}

for index, row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']

df_match.to_csv('csv_files/clean/match_summary.csv', index= None)

df_batting = pd.read_csv('csv_files/t20_csv_files/batting_summary.csv', index_col= False)

# Create 'out/not_out' column
df_batting['out/not_out'] = df_batting.dismissal.apply(lambda x: "out" if len(x) > 0 else "not_out")

# Map match_id using match names
df_batting['match_id'] = df_batting['match'].map(match_ids_dict)

# Remove 'dismissal' column
df_batting.drop(columns=["dismissal"], inplace=True)

# Remove weird characters from batsmanName
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0', ''))

df_batting.to_csv('csv_files/clean/batting_summary.csv', index= None)

df_bowling = pd.read_csv('csv_files/t20_csv_files/bowling_summary.csv', index_col= False)

df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)

df_bowling.to_csv('csv_files/clean/bowling_summary.csv', index= None)

df_players = pd.read_csv('csv_files/t20_csv_files/detailed_players_data.csv', index_col= False)

df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))

print(df_players[df_players['team'] == 'India'])

df_players.to_csv('csv_files/clean/players_no_images.csv', index= None)
