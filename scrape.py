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
