import requests
import os

champions = ['Katarina', 'Varus', 'Kassadin', 'Fizz', 'Kled', 'Zac', 'Neeko', 'Wukong', 'Sylas', 'Samira', 'Aurelion Sol', 'Azir', 'Briar', 'Rammus', 'Poppy', 'Gragas', 'Viego', 'Gwen', 'Jinx', 'Singed', 'Warwick', 'Udyr', 'Lux', 'Elise', 'Cassiopeia', 'Miss Fortune', 'Ryze', 'Milio', 'Vladimir', 'Nilah', 'Leblanc', 'Draven', 'Thresh', 'Xayah', 'Rumble', 'Lee Sin', "Cho'gath", 'Zilean', 'Sion', 'Yasuo', 'Dr. Mundo', 'Syndra', 'Olaf', 'Ahri', 'Blitzcrank', 'Swain', 'Diana', 'Zeri', 'Tahm Kench', 'Rell', 'Pantheon', 'Renekton', 'Urgot', 'Talon', 'Garen', 'Fiora', 'Evelynn', 'Kindred', 'Galio', 'Teemo', 'Braum', 'Yorick', 'Nunu & Willump', 'Darius', 'Lissandra', 'Gangplank', 'Nocturne', 'Rakan', 'Alistar', "Vel'koz", 'Volibear', 'Karma', 'Caitlyn', "Kha'zix", 'Twitch', 'Graves', 'Sejuani', 'Janna', 'Zoe', 'Ashe', "Bel'veth", 'Hecarim', 'Taliyah', 'Sett', 'Karthus', 'Akshan', 'Vex', 'Lillia', 'Seraphine', 'Malzahar', 'Tristana', 'Lucian', "Rek'Sai", 'Hwei', 'Ivern', 'Ziggs', 'Vi', 'Qiyana', "Kog'Maw", 'Annie', 'Senna', 'Heimerdinger', 'Riven', 'Kayle', 'Gnar', 'Veigar', 'Leona', "Kai'sa", 'Nidalee', 'Jax', 'Sivir', 'Xin Zhao', 'Soraka', 'Mordekaiser', 'Malphite', 'Naafiri', 'Zed', 'Jayce', 'Tryndamere', 'Kayn', 'Ornn', 'Brand', 'Aphelios', "K'Sante", 'Viktor', 'Corki', 'Morgana', 'Trundle', 'Akali', 'Jhin', 'Taric', 'Sona', 'Irelia', 'Kalista', 'Bard', 'Yone', 'Quinn', 'Aatrox', 'Shaco', 'Shyvana', 'Master Yi', 'Shen', 'Anivia', 'Nami', 'Fiddlesticks', 'Nasus', 'Maokai', 'Renata Glasc', 'Zyra', 'Xerath', 'Ekko', 'Twisted Fate', 'Vayne', 'Amumu', 'Yuumi', 'Jarvan IV', 'Illaoi', 'Orianna', 'Rengar', 'Ezreal', 'Pyke', 'Kennen', 'Nautilus', 'Lulu', 'Camille']

championsUrl = []

for champion in champions:
    if champion == 'Wukong':
        championsUrl.append('MonkeyKing')
    elif champion == 'Renata Glasc':
        championsUrl.append('Renata')
    elif 'Nunu' in champion:
        championsUrl.append('Nunu')
    else:
        championsUrl.append(champion.replace(' ', '').replace("'", "").replace(".", ""))


def get_champion_passive_image(champions):
    passive_images = {}
    base_url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion"

    for champion in champions:
        url = f"{base_url}/{champion}.json"

        print(url)

        response = requests.get(url)
        data = response.json()

        #print(data)

        # Extract the passive ability's image name
        passive_image = data['data'][champion]['passive']['image']['full']
        passive_images[champion] = passive_image

    return passive_images

# Execute the function and print the results
passive_images = get_champion_passive_image(championsUrl)
print(passive_images)

passive_images_directory = "../images/passive"

# Loop through the dictionary and rename each passive image file
for champion, passive_image in passive_images.items():
    # Construct the old file path
    old_file_path = os.path.join(passive_images_directory, passive_image)
    
    # Construct the new file name and path
    new_file_name = f"{champion}P.png"
    new_file_path = os.path.join(passive_images_directory, new_file_name)
    
    # Check if the old file exists before renaming
    if os.path.isfile(old_file_path):
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed {old_file_path} to {new_file_path}")
    else:
        print(f"File {old_file_path} does not exist, cannot rename.")
