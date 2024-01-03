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


# 设置 WebDriver 路径（以 Chrome 为例）
#driver_path = 'path/to/your/chromedriver'  # 替换为您的 WebDriver 路径

# 创建 WebDriver 实例
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
mainRunes = []
secondaryRunes = []
stats = []

starterItems = []
starterItemsNum = []
boots = []
bootsNum = []
CoreItems = []
CoreItemsNum = []

for champion in championsUrl:

    # 替换 URL 中的英雄名称
    url = f"https://www.op.gg/champions/{champion}/build?region=kr&tier=all"
    driver.get(url)

    # 等待页面加载
    time.sleep(3)

    # 获取页面源代码
    html = driver.page_source

    # 使用 BeautifulSoup 解析页面
    soup = BeautifulSoup(html, "html.parser")

    mainRune_div = soup.find_all(name='div', attrs={'class': 'css-1k1cq3m'})
    if len(mainRune_div) == 5:
        tempMainRune = []
        tempSecondaryRune = []

        championName.append(champions[championIndex])

        for i in range(0, 3):
            mainRune_img = mainRune_div[i].find(name='img') 
            tempMainRune.append(mainRune_img.attrs['alt'])
        
        for i in range(3, 5):
            secondaryRune_img = mainRune_div[i].find(name='img') 
            tempSecondaryRune.append(secondaryRune_img.attrs['alt'])
        
        mainRunes.append(tempMainRune)
        secondaryRunes.append(tempSecondaryRune)

    else:
        mainRunes.append('noWaying')
        print(champion + '-wtfRune')

    stats_div = soup.find_all(name='div', attrs={'class': 'css-1ooi192'})
    if len(stats_div) == 1:
        tempStats = []

        stats_div_2 = stats_div[0].find_all(name='div', attrs={'class': ''})
        if len(stats_div_2) == 9:
            for i in range(0, 9):
                if stats_div_2[i].find(attrs={'class': 'active'}):
                    tempStats.append(i)
        
            stats.append(tempStats)

        else:
            stats.append('noWaying')
            print(champion + '-wtfStats')

    else:
        stats.append('noWaying')
        print(champion + '-wtfStats')


    item_table = soup.find_all(name='table', attrs={'class': 'css-5e55vo'})
    if len(item_table) == 3:
        tempStarterItems = []
        tempStarterItemsNum = []
        tempBoots = []
        tempBootsNum = []
        tempCoreItems = []
        tempCoreItemsNum = []
        for i in range(0, 3):
            item_td = item_table[i].find(name='td', attrs={'class': 'e14sgc0n2'})
            if item_td:
                item_img = item_td.find_all(name='img')
                if item_img:
                    for j in range(0, len(item_img)):
                        url = item_img[j].attrs['src']
                        parts = url.split('/')
                        last_part = parts[-1]
                        item_id = last_part.split('.')[0]
                        if i == 0:
                            tempStarterItems.append(item_img[j].attrs['alt'])
                            tempStarterItemsNum.append(item_id)
                        elif i == 1:
                            tempBoots.append(item_img[j].attrs['alt'])
                            tempBootsNum.append(item_id)
                        elif i == 2:
                            tempCoreItems.append(item_img[j].attrs['alt'])
                            tempCoreItemsNum.append(item_id)
                else:
                    starterItems.append('noWaying')
                    boots.append('noWaying')
                    CoreItems.append('noWaying')
                    starterItemsNum.append('noWaying')
                    bootsNum.append('noWaying')
                    CoreItemsNum.append('noWaying')
                    print('wtfItem')
            else:
                starterItems.append('noWaying')
                boots.append('noWaying')
                CoreItems.append('noWaying')
                starterItemsNum.append('noWaying')
                bootsNum.append('noWaying')
                CoreItemsNum.append('noWaying')
                print('wtfItem')
        
        starterItems.append(tempStarterItems)
        boots.append(tempBoots)
        CoreItems.append(tempCoreItems)
        starterItemsNum.append(tempStarterItemsNum)
        bootsNum.append(tempBootsNum)
        CoreItemsNum.append(tempCoreItemsNum)

    else:
        starterItems.append('noWaying')
        boots.append('noWaying')
        CoreItems.append('noWaying')
        starterItemsNum.append('noWaying')
        bootsNum.append('noWaying')
        CoreItemsNum.append('noWaying')
        print(champion + '-wtfItem')

    championIndex += 1

driver.quit()

df1 = pd.DataFrame(data=[championName, mainRunes, secondaryRunes, stats, starterItems, starterItemsNum, boots, bootsNum, CoreItems, CoreItemsNum], index=['championName', 'mainRunes', 'secondaryRunes', 'stats', 'starterItems', 'starterItemsNum', 'boots', 'bootsNum', 'CoreItems', 'CoreItemsNum'])
df2 = pd.DataFrame(df1.values.T, columns=df1.index)
df2.to_csv('../data/rune3.csv', encoding='utf-8')

