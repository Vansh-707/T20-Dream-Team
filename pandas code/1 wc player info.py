import requests
from bs4 import BeautifulSoup
import pandas as pd

# Helper function to get the HTML content from a URL
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Send the GET request with the headers
    response = requests.get(url, headers=headers)
    
    # Check if the page was fetched successfully
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    return response.content

# Stage 1: Extract match summary links
def get_match_summary_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Send the GET request with the headers
    response = requests.get(url, headers=headers)
    
    # Check if the page was fetched successfully
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    # Step 2: Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Find all match summary links
    all_rows = soup.find_all('a', "ds-inline-flex ds-items-start ds-leading-none")

    match_summary_links = []
    for x in all_rows:
        if x['href'].startswith("/series"):
            full_url = f"https://www.espncricinfo.com{x['href']}"
            match_summary_links.append(full_url)
    
    return match_summary_links

# Stage 2: Extract players data from the match details
def get_players_data(url):
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    players_data = []
    
    # Extract teams
    match_details = soup.find_all('div', string='Match Details')
    x = soup.find_all("span", "ds-text-title-xs ds-font-bold ds-capitalize")
    t = [y.get_text() for y in x]

    team1 = t[0]
    team2 = t[1]
    
    # Extract batting players
    tables = soup.select('div > table.ci-scorecard-table')
    first_innings_rows = tables[0].select('tbody > tr')
    second_innings_rows = tables[1].select('tbody > tr')
    
    for row in first_innings_rows:
        tds = row.find_all('td')
        if len(tds) >= 8:
            players_data.append({
                "name": tds[0].find('a').get_text(strip=True),
                "team": team1,
                "link": "https://www.espncricinfo.com" + tds[0].find('a')['href']
            })
    
    for row in second_innings_rows:
        tds = row.find_all('td')
        if len(tds) >= 8:
            players_data.append({
                "name": tds[0].find('a').get_text(strip=True),
                "team": team2,
                "link": "https://www.espncricinfo.com" + tds[0].find('a')['href']
            })
    
    # Extract bowling players
    bowling_tables = soup.select('div > table.ds-table')
    first_innings_bowling_rows = bowling_tables[1].select('tbody > tr')
    second_innings_bowling_rows = bowling_tables[3].select('tbody > tr')
    
    for row in first_innings_bowling_rows:
        tds = row.find_all('td')
        if len(tds) >= 11:
            players_data.append({
                "name": tds[0].find('a').get_text(strip=True),
                "team": team2,
                "link": "https://www.espncricinfo.com" + tds[0].find('a')['href']
            })
    
    for row in second_innings_bowling_rows:
        tds = row.find_all('td')
        if len(tds) >= 11:
            players_data.append({
                "name": tds[0].find('a').get_text(strip=True),
                "team": team1,
                "link": "https://www.espncricinfo.com" + tds[0].find('a')['href']
            })
    
    return players_data

# Stage 3: Extract detailed player data
def get_player_details(player_url):
    html_content = get_html(player_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extracting specific player information
    batting_style = soup.find('p', string='Batting Style')
    if batting_style:
        batting_style = batting_style.find_next('span').text.strip()
    bowling_style = soup.find('p', string='Bowling Style')
    if bowling_style:
        bowling_style = bowling_style.find_next('span').text.strip()
    playing_role = soup.find('p', string='Playing Role')
    if playing_role:
        playing_role = playing_role.find_next('span').text.strip()
    
    description = soup.select_one('div.ci-player-bio-content p')
    if description:
        description = description.text.strip()
    
    player_info = {
        "battingStyle": batting_style,
        "bowlingStyle": bowling_style,
        "playingRole": playing_role,
        "description": description
    }
    
    return player_info


# Main function to gather and structure all data
def main():
    match_summary_url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament'
    
    # Step 1: Get match summary links :- use it only single time to avoid web request overload . 
    
    # match_summary_links = get_match_summary_links(match_summary_url)
    # summary = pd.DataFrame(match_summary_links, columns=['links'])
    # summary.to_csv("csv_files/extra/summary_links.csv", index= False)


    # extract data from csv :- 
    match_summary_links = pd.read_csv("csv_files/extra/summary_links.csv", index_col= False)
    print(match_summary_links.head())

    # Step 2: Get player data :- use it only single to avoid web request overload . 
    # all_players_data = []
    # for link in match_summary_links['links']:
    #     players_data = get_players_data(link)
    #     all_players_data.extend(players_data)
    
    # all_data = pd.DataFrame(all_players_data)
    # all_data.to_csv("csv_files/extra/all_players_data.csv", index = False)

    all_players_data = pd.read_csv("csv_files/extra/all_players_data.csv", index_col= False)
    print(all_players_data.head())

    # Step 3: Get detailed player data :- use this once, and, store data in csv files . 
    # detailed_player_data = []
    # for index, row in all_players_data.iterrows():
    #     player_details = get_player_details(row['link'])
    #     detailed_player_data.append({
    #         "name": row['name'],
    #         "team": row['team'],
    #         "battingStyle": player_details.get('battingStyle'),
    #         "bowlingStyle": player_details.get('bowlingStyle'),
    #         "playingRole": player_details.get('playingRole'),
    #         "description": player_details.get('description')
    #     })

    # Convert the result to a pandas DataFrame
    # df = pd.DataFrame(detailed_player_data)
    # print(df.head())

    # df.to_csv("csv_files/t20_csv_files/detailed_players_data.csv", index_col= False)

    df = pd.read_csv("csv_files/t20_csv_files/detailed_players_data.csv", index_col= False)
    print(df.head())

if __name__ == "__main__":
    main()
