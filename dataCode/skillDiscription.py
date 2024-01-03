import pandas as pd
import requests

# List of champion names (example list, please replace with your actual list of champion names)
champion_names = ['Katarina', 'Varus', 'Kassadin', 'Fizz', 'Kled', 'Zac', 'Neeko', 'Wukong', 'Sylas', 'Samira', 'Aurelion Sol', 'Azir', 'Briar', 'Rammus', 'Poppy', 'Gragas', 'Viego', 'Gwen', 'Jinx', 'Singed', 'Warwick', 'Udyr', 'Lux', 'Elise', 'Cassiopeia', 'Miss Fortune', 'Ryze', 'Milio', 'Vladimir', 'Nilah', 'Leblanc', 'Draven', 'Thresh', 'Xayah', 'Rumble', 'Lee Sin', "Cho'gath", 'Zilean', 'Sion', 'Yasuo', 'Dr. Mundo', 'Syndra', 'Olaf', 'Ahri', 'Blitzcrank', 'Swain', 'Diana', 'Zeri', 'Tahm Kench', 'Rell', 'Pantheon', 'Renekton', 'Urgot', 'Talon', 'Garen', 'Fiora', 'Evelynn', 'Kindred', 'Galio', 'Teemo', 'Braum', 'Yorick', 'Nunu & Willump', 'Darius', 'Lissandra', 'Gangplank', 'Nocturne', 'Rakan', 'Alistar', "Vel'koz", 'Volibear', 'Karma', 'Caitlyn', "Kha'zix", 'Twitch', 'Graves', 'Sejuani', 'Janna', 'Zoe', 'Ashe', "Bel'veth", 'Hecarim', 'Taliyah', 'Sett', 'Karthus', 'Akshan', 'Vex', 'Lillia', 'Seraphine', 'Malzahar', 'Tristana', 'Lucian', "Rek'Sai", 'Hwei', 'Ivern', 'Ziggs', 'Vi', 'Qiyana', "Kog'Maw", 'Annie', 'Senna', 'Heimerdinger', 'Riven', 'Kayle', 'Gnar', 'Veigar', 'Leona', "Kai'sa", 'Nidalee', 'Jax', 'Sivir', 'Xin Zhao', 'Soraka', 'Mordekaiser', 'Malphite', 'Naafiri', 'Zed', 'Jayce', 'Tryndamere', 'Kayn', 'Ornn', 'Brand', 'Aphelios', "K'Sante", 'Viktor', 'Corki', 'Morgana', 'Trundle', 'Akali', 'Jhin', 'Taric', 'Sona', 'Irelia', 'Kalista', 'Bard', 'Yone', 'Quinn', 'Aatrox', 'Shaco', 'Shyvana', 'Master Yi', 'Shen', 'Anivia', 'Nami', 'Fiddlesticks', 'Nasus', 'Maokai', 'Renata Glasc', 'Zyra', 'Xerath', 'Ekko', 'Twisted Fate', 'Vayne', 'Amumu', 'Yuumi', 'Jarvan IV', 'Illaoi', 'Orianna', 'Rengar', 'Ezreal', 'Pyke', 'Kennen', 'Nautilus', 'Lulu', 'Camille']

championsUrl = []

for champion in champion_names:
    if champion == 'Wukong':
        championsUrl.append('MonkeyKing')
    elif champion == 'Renata Glasc':
        championsUrl.append('Renata')
    elif 'Nunu' in champion:
        championsUrl.append('Nunu')
    else:
        championsUrl.append(champion.replace(' ', '').replace("'", "").replace(".", ""))

# Base URL for the Data Dragon JSON files for champions
base_url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion"

# Initialize an empty list to store champion abilities data
champion_abilities = []

# Loop over each champion to get their ability data
for champion in championsUrl:
    # Fetch the champion data from the Data Dragon API
    response = requests.get(f"{base_url}/{champion}.json")

    print(f"{base_url}/{champion}.json")
    champion_data = response.json()['data'][champion]
    
    # Append the ability data to the list
    champion_abilities.append({
        'Champion': champion,
        'Q Name': champion_data['spells'][0]['name'],
        'Q Description': champion_data['spells'][0]['description'],
        'W Name': champion_data['spells'][1]['name'],
        'W Description': champion_data['spells'][1]['description'],
        'E Name': champion_data['spells'][2]['name'],
        'E Description': champion_data['spells'][2]['description'],
        'R Name': champion_data['spells'][3]['name'],
        'R Description': champion_data['spells'][3]['description'],
        'Passive Name': champion_data['passive']['name'],
        'Passive Description': champion_data['passive']['description']
    })

# Convert the list to a DataFrame
df_abilities = pd.DataFrame(champion_abilities)

# Specify the output file name
output_file = 'champion_abilities.csv'
# Save the DataFrame to a CSV file
df_abilities.to_csv(output_file, index=False)