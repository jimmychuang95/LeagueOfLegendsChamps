from selenium import webdriver
import pandas as pd  #导入pandas库
import bs4  # 导入bs4库
from bs4 import BeautifulSoup  # 导入BeautifulSoup库
import time

def askurl(urlbase):
    import urllib.request  # 正确的导入语句

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
    }

    request = urllib.request.Request(urlbase, headers=header)

    try:
        response = urllib.request.urlopen(request, timeout=5)
        # 如果有需要，可以根据Content-Type来选择编码
        charset = response.headers.get_content_charset()
        if charset is None:
            charset = 'utf-8'
        html = response.read().decode(charset)
    except Exception as e:
        print(e)
        html = ""  # 在异常情况下返回空字符串

    return html

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

#champions = ['Rengar', 'Wukong', 'Shyvana', 'Vex', 'Kalista', 'Jayce', 'Ezreal', 'Rell', 'Kled', 'Gragas', 'Xerath', 'Olaf', 'Veigar', 'Syndra', 'Ornn', 'Jarvan IV', 'Gwen', 'Lux', 'Vayne', 'Ivern', 'Seraphine', 'Shen', 'Yone', 'Master Yi', 'Nocturne', 'Zyra', 'Maokai', 'Xin Zhao', 'Twisted Fate', 'Akali', 'Ziggs', 'Sylas', 'Taliyah', 'Lulu', 'Riven', 'Poppy', 'Karma', 'Dr. Mundo', 'Mordekaiser', 'Shaco', 'Akshan', 'Nidalee', 'Draven', 'Azir', 'Zoe', 'Diana', 'Nami', 'Katarina', 'Twitch', 'Qiyana', 'Renekton', "Bel'Veth", 'Aphelios', 'Lucian', 'Viego', 'Cassiopeia', 'Singed', 'Fizz', 'Vladimir', "Kog'Maw", 'Sett', 'Sona', 'Kayn']
#champions = ['Sion', 'Senna', 'Fiddlesticks', 'Galio', 'Yasuo', 'Elise', 'Teemo', 'Sejuani', 'Naafiri', 'Renata Glasc', 'Morgana', "Cho'Gath", 'Warwick', 'Nautilus', 'Thresh', 'Xayah', 'Graves', 'Evelynn', 'Tahm Kench', 'Corki', 'Brand', 'Kayle', 'Tryndamere', 'Quinn', 'Viktor', 'Camille', 'Yuumi', "Kai'Sa", 'Janna', 'Kassadin', 'Darius', 'Zilean', 'Ryze', 'Rakan', 'Blitzcrank', 'Kindred', 'Irelia', 'Vi', 'Trundle', 'Lissandra', 'Sivir', 'Rumble', 'Gnar', "Vel'Koz", 'Soraka', 'Taric', 'Varus', 'Nilah', 'Zac', 'Milio', 'Zed', 'Annie', 'Neeko', 'Ashe', 'Braum', 'Anivia', 'Volibear', 'Karthus', 'Hecarim', 'Rammus', 'Orianna', 'Talon']
champions = ['Pantheon', 'Urgot', "Kha'Zix", 'Caitlyn', 'Tristana', 'LeBlanc', 'Garen', 'Pyke', 'Udyr', 'Malzahar', 'Kennen', "Rek'Sai", 'Heimerdinger', 'Bard', 'Gangplank', 'Nunu & Willump', 'Zeri', 'Yorick', 'Jax', 'Hwei', 'Lillia', 'Jinx', 'Briar', 'Leona', 'Alistar', 'Aatrox', 'Malphite', 'Nasus', 'Samira', 'Ahri', 'Miss Fortune', 'Swain', 'Lee Sin', 'Fiora', 'Jhin', 'Amumu', 'Illaoi', "K'Sante", 'Ekko', 'Aurelion Sol']
#champions = ['cassiopeia']

championsUrl = []

for champion in champions:
    if champion == 'Wukong':
        championsUrl.append('monkeyking')
    elif champion == 'Renata Glasc':
        championsUrl.append('renata')
    elif 'Nunu' in champion:
        championsUrl.append('nunu')
    else:
        championsUrl.append(champion.replace(' ', '').lower().replace("'", "").replace(".", ""))

championIndex = 0

championName = []
bestDuo1 = []
bestDuo2 = []
bestDuo3 = []
bestDuo4 = []
bestDuo5 = []
bestDuo6 = []

for champion in championsUrl:

    url = f"https://mobalytics.gg/lol/champions/{champion}/build"
    driver.get(url)

    time.sleep(2)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    championName.append(champions[championIndex])

    bestDuo_div = soup.find_all(name = 'div', attrs = {'class': 'm-gumcrk'})

    if len(bestDuo_div) == 3:
        bestDuo_a = bestDuo_div[2].find_all(name = 'a', attrs = {'class': 'm-di7nx6'})
        if len(bestDuo_a) == 6:
            tempBestDuo1 = []
            tempBestDuo2 = []
            tempBestDuo3 = []
            tempBestDuo4 = []
            tempBestDuo5 = []
            tempBestDuo6 = []
            for i in range(0, 6):
                if i == 0:
                    tempBestDuo1.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo1.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo1.append(position_div.find(name = 'img').attrs['alt'])
                elif i == 1:
                    tempBestDuo2.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo2.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo2.append(position_div.find(name = 'img').attrs['alt'])
                elif i == 2:
                    tempBestDuo3.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo3.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo3.append(position_div.find(name = 'img').attrs['alt'])
                elif i == 3:
                    tempBestDuo4.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo4.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo4.append(position_div.find(name = 'img').attrs['alt'])
                elif i == 4:
                    tempBestDuo5.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo5.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo5.append(position_div.find(name = 'img').attrs['alt'])
                elif i == 5:
                    tempBestDuo6.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-v1s0fv'}).text)
                    tempBestDuo6.append(bestDuo_a[i].find(name = 'p', attrs = {'class': 'm-d1usi'}).text)
                    position_div = bestDuo_a[i].find(name = 'div', attrs = {'class': 'm-amdtug'})
                    tempBestDuo6.append(position_div.find(name = 'img').attrs['alt'])

            bestDuo1.append(tempBestDuo1)
            bestDuo2.append(tempBestDuo2)
            bestDuo3.append(tempBestDuo3)
            bestDuo4.append(tempBestDuo4)
            bestDuo5.append(tempBestDuo5)
            bestDuo6.append(tempBestDuo6)
        
        else:
            print(champion + '-wtfBestDuo')
            bestDuo1.append('noWaying')
            bestDuo2.append('noWaying')
            bestDuo3.append('noWaying')
            bestDuo4.append('noWaying')
            bestDuo5.append('noWaying')
            bestDuo6.append('noWaying')
    
    else:
        print(champion + '-wtfBestDuo')
        bestDuo1.append('noWaying')
        bestDuo2.append('noWaying')
        bestDuo3.append('noWaying')
        bestDuo4.append('noWaying')
        bestDuo5.append('noWaying')
        bestDuo6.append('noWaying')

    championIndex += 1

driver.quit()

df1 = pd.DataFrame({'championName': championName, 'bestDuo1': bestDuo1, 'bestDuo2': bestDuo2, 'bestDuo3': bestDuo3, 'bestDuo4': bestDuo4, 'bestDuo5': bestDuo5, 'bestDuo6': bestDuo6})
df1.to_csv('../data/championBestDuo2.csv', encoding='utf-8', index=False)
            