import requests
from bs4 import BeautifulSoup
import pandas as pd

# Example URL of a Counter-Strike player page on Liquipedia
url = 'https://liquipedia.net/counterstrike/Player_Name'

# Function to scrape data from a Liquipedia CS:GO player page
def scrape_csgo_player_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract player name
    player_name = soup.find('h1', class_='firstHeading').text.strip()
    
    # Extract the infobox table
    infobox = soup.find('table', class_='infobox')
    
    # Extracting specific stats from the infobox (actual selectors will vary)
    team = infobox.find('th', text='Team').find_next('td').text.strip()
    total_kills = infobox.find('tr', text='Total Kills').find_next('td').text.strip()
    total_deaths = infobox.find('tr', text='Total Deaths').find_next('td').text.strip()
    kill_death_ratio = infobox.find('tr', text='K/D Ratio').find_next('td').text.strip()
    headshot_percentage = infobox.find('tr', text='Headshot %').find_next('td').text.strip()

    # Clean and structure the data
    player_data = {
        'Player Name': player_name,
        'Team': team,
        'Total Kills': int(total_kills.replace(',', '')),
        'Total Deaths': int(total_deaths.replace(',', '')),
        'K/D Ratio': float(kill_death_ratio),
        'Headshot %': float(headshot_percentage.replace('%', '')) / 100,
        # Add more fields as needed
    }
    
    return player_data

# Example usage
player_data = scrape_csgo_player_data(url)
print(player_data)

# Save data to a DataFrame
players_df = pd.DataFrame([player_data])

# Further cleaning if necessary
# Example: Calculating additional stats such as average kills per match if match data is available
# Assuming we have 'Total Matches' in the data

players_df['Kills per Match'] = players_df['Total Kills'] / players_df['Total Matches']
players_df['Deaths per Match'] = players_df['Total Deaths'] / players_df['Total Matches']

# If match data is not available directly, consider other metrics to add depth to the analysis
# Example: Analyzing K/D Ratio and Headshot Percentage
team_stats = players_df.groupby('Team').agg({
    'K/D Ratio': 'mean',
    'Headshot %': 'mean',
    'Total Kills': 'sum',
    'Total Deaths': 'sum',
}).reset_index()

# Calculate overall team K/D Ratio
team_stats['Team K/D Ratio'] = team_stats['Total Kills'] / team_stats['Total Deaths']

# Further analysis could include looking at player consistency, clutch success rates, etc.
# Export player-level data to CSV
players_df.to_csv('csgo_player_data.csv', index=False)

# Export team-level data to CSV for comparison and team analysis
team_stats.to_csv('csgo_team_stats.csv', index=False)
