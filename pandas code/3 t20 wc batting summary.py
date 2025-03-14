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

links = pd.read_csv("csv_files/extra/summary_links.csv")

# For each match summary link, fetch the match details
batting_summary = []

for match_url in links['links']:
    x = get_html(match_url)
    soup = BeautifulSoup(x, 'html.parser')

    # Extracting match details (team names)
    match_details = soup.find_all('div', string='Match Details')
    x = soup.find_all("span", "ds-text-title-xs ds-font-bold ds-capitalize")
    t = [y.get_text() for y in x]
    team1 = t[0]
    team2 = t[1]
    match_info = team1 + ' Vs ' + team2

    # Extracting batting details for both innings
    tables = soup.select('div > table.ci-scorecard-table')
    first_inning_rows = tables[0].select('tbody > tr')
    second_inning_rows = tables[1].select('tbody > tr')

    # Parsing first innings
    for index, row in enumerate(first_inning_rows):
        tds = row.find_all('td')
        if len(tds) >= 8:  # Ensure the row has enough data
            # Check if dismissal element exists
            dismissal = tds[1].find('span')
            dismissal_text = dismissal.text.strip() if dismissal else "Not Out"  # Default to "Not Out" if no dismissal is found

            batting_summary.append({
                "match": match_info,
                "teamInnings": team1,
                "battingPos": index + 1,
                "batsmanName": tds[0].find('a').find('span').text.strip(),
                "dismissal": dismissal_text,
                "runs": tds[2].find('strong').text.strip(),
                "balls": tds[3].text.strip(),
                "4s": tds[5].text.strip(),
                "6s": tds[6].text.strip(),
                "SR": tds[7].text.strip()
            })

    # Similarly for the second innings
    for index, row in enumerate(second_inning_rows):
        tds = row.find_all('td')
        if len(tds) >= 8:
            # Check if dismissal element exists
            dismissal = tds[1].find('span')
            dismissal_text = dismissal.text.strip() if dismissal else "Not Out"  

            batting_summary.append({
                "match": match_info,
                "teamInnings": team2,
                "battingPos": index + 1,
                "batsmanName": tds[0].find('a').find('span').text.strip(),
                "dismissal": dismissal_text,
                "runs": tds[2].find('strong').text.strip(),
                "balls": tds[3].text.strip(),
                "4s": tds[5].text.strip(),
                "6s": tds[6].text.strip(),
                "SR": tds[7].text.strip()
            })


df_batting_summary = pd.DataFrame(batting_summary)
df_batting_summary.to_csv("csv_files/t20_csv_files/batting_summary.csv")
print(df_batting_summary.head())
