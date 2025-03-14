import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
    
table = soup.find('div', "ds-overflow-x-auto ds-scrollbar-hide")
print(table)
table = table.find_all('table')

match_summary = []
for t in table:
    rows = t.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        match_summary.append({
            'team1': tds[0].text.strip(),
            'team2': tds[1].text.strip(),
            'winner': tds[2].text.strip(),
            'margin': tds[3].text.strip(),
            'ground': tds[4].text.strip(),
            'matchDate': tds[5].text.strip(),
            'scorecard': tds[6].text.strip()
        })

df = pd.DataFrame(match_summary)
df.to_csv("csv_files/t20_csv_files/dim_match_summary.csv", index= False)

print(df)