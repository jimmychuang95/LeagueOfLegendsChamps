import requests
import pandas as pd

# URL of the JSON data
url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/runesReforged.json"

# Function to fetch and parse the JSON data from the URL
def fetch_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch the data
data = fetch_json_data(url)

# Process the data to extract the required information
def process_runes(data):
    rows = []
    for category in data:
        for slot in category['slots']:
            for rune in slot['runes']:
                rows.append({
                    'key': rune['key'],
                    'name': rune['name'],
                    'shortDesc': rune['shortDesc'],
                    'longDesc': rune['longDesc']
                })
    return pd.DataFrame(rows, columns=['key', 'name', 'shortDesc', 'longDesc'])

# Process and display the data
df_runes = process_runes(data)
df_runes.to_csv('../data/runesDescription.csv', index=False)

