import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    return response.content

url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament'
x = get_html(url)
soup = BeautifulSoup(x, 'html.parser')

summary_links = pd.read_csv("csv_files/extra/summary_links.csv")

bowling_summary = []

for link in summary_links['links']:
    x = get_html(link)
    soup = BeautifulSoup(x, 'html.parser')
    
    # Extract match details
    match_details = soup.find_all('div', string='Match Details')
    x = soup.find_all("span", "ds-text-title-xs ds-font-bold ds-capitalize")
    t = [y.get_text() for y in x]
    team1 = t[0]
    team2 = t[1]
    match_info = team1 + ' Vs ' + team2
    
    # Extract bowling data
    tables = soup.select('div > table.ds-table')
    
    if len(tables) >= 4:
        first_inning_rows = tables[1].select('tbody > tr')
        second_inning_rows = tables[3].select('tbody > tr')
        
        # Parse bowling data for first innings
        for row in first_inning_rows:
            tds = row.find_all('td')
            if len(tds) >= 11:

                bowling_summary.append({
                    "match": match_info,
                    "bowlingTeam": team2,
                    "bowlerName": tds[0].find('a').text.strip(),
                    "overs": tds[1].text.strip(),
                    "maiden": tds[2].text.strip(),
                    "runs": tds[3].text.strip(),
                    "wickets": tds[4].text.strip(),
                    "economy": tds[5].text.strip(),
                    "0s": tds[6].text.strip(),
                    "4s": tds[7].text.strip(),
                    "6s": tds[8].text.strip(),
                    "wides": tds[9].text.strip(),
                    "noBalls": tds[10].text.strip()
                })
        
        # Parse bowling data for second innings
        for row in second_inning_rows:
            tds = row.find_all('td')
            if len(tds) >= 11:
                bowling_summary.append({
                    "match": match_info,
                    "bowlingTeam": team1,
                    "bowlerName": tds[0].find('a').text.strip(),
                    "overs": tds[1].text.strip(),
                    "maiden": tds[2].text.strip(),
                    "runs": tds[3].text.strip(),
                    "wickets": tds[4].text.strip(),
                    "economy": tds[5].text.strip(),
                    "0s": tds[6].text.strip(),
                    "4s": tds[7].text.strip(),
                    "6s": tds[8].text.strip(),
                    "wides": tds[9].text.strip(),
                    "noBalls": tds[10].text.strip()
                })

bowling_df = pd.DataFrame(bowling_summary)
bowling_df.to_csv("csv_files/t20_csv_files/bowling_summary.csv")

print(bowling_df)

