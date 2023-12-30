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
#champions = ['Nunu & Willump']

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



# 初始化结果列表
champIndex = 0

championName = []
perk1 = []
perk2 = []
perk3 = []

skill1 = []
skill2 = []

sumSpell1 = []
sumSpell2 = []

weak1 = []
weak2 = []
weak3 = []
weak4 = []
weak5 = []

strong1 = []
strong2 = []
strong3 = []
strong4 = []
strong5 = []

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

    #PERKS
    perk_div = soup.find(name='div', attrs={'class': 'css-1d95r1l'})
    if perk_div:
        perk_img = perk_div.find_all(name='img')
        if len(perk_img) == 3:
            championName.append(champions[champIndex])
            perk1.append(perk_img[0].attrs['alt'])
            perk2.append(perk_img[1].attrs['alt'])
            perk3.append(perk_img[2].attrs['alt'])
    else:
        perk1.append('noway')
        perk2.append('noway')
        print(champion + '_WTFperk')

    #SKILL
    skill_strong = soup.find_all(name = 'strong', attrs={'class': 'e8p0atj2'})
    if len(skill_strong) == 18:
        skill1_local = []
        skill2_local = []
        for i in range(0, 3):
            skill1_local.append(skill_strong[i].text)
        for i in range(3, 18):
            skill2_local.append(skill_strong[i].text)
        skill1.append(skill1_local)
        skill2.append(skill2_local)

    else:
        skill1.append('noway')
        skill2.append('noway')
        print(champion + '_WTFskill')

    #SUMMONER SPELLS
    sumSpell_ul = soup.find_all(name='ul', attrs={'class': 'e1qbmy400'})
    if sumSpell_ul:
        sumSpell_img = sumSpell_ul[0].find_all(name='img')
        if len(sumSpell_img) == 2:
            sumSpell1.append(sumSpell_img[0].attrs['alt'])
            sumSpell2.append(sumSpell_img[1].attrs['alt'])
    else:
        sumSpell1.append('noway')
        sumSpell2.append('noway')
        print(champion + '_WTFsumSpell')

    
    weak_against_div = soup.find('div', string='Weak Against')
    if weak_against_div:
        weak_against_ul = weak_against_div.find_next_sibling(name='ul')
        weak_against_li = weak_against_ul.find_all(name='li', attrs={'class': 'e9r595k3'})

    strong_against_div = soup.find('div', string='Strong Against')
    if strong_against_div:
        strong_against_ul = strong_against_div.find_next_sibling(name='ul')
        strong_against_li = strong_against_ul.find_all(name='li', attrs={'class': 'e9r595k3'})
    
    #WEAK AGAINST
    for i in range(0, 5):
        weakData = []
        if len(weak_against_li) > i:
            weak_a = weak_against_li[i].find(name='a')
            weakData.append(weak_a.attrs['href'].split('target_champion=')[1].capitalize())

            weak_winrate_div = weak_a.find(name='div', attrs={'class': 'win-rate'})
            weakData.append(weak_winrate_div.contents[0])

            weak_play_div = weak_a.find(name='div', attrs={'class': 'play'})
            weakData.append(weak_play_div.contents[0])

        if i == 0:
            if len(weakData) > 0:
                weak1.append(weakData)
            else:
                weak1.append('None')
        elif i == 1:
            if len(weakData) > 0:
                weak2.append(weakData)
            else:
                weak2.append('None')
        elif i == 2:
            if len(weakData) > 0:
                weak3.append(weakData)
            else:
                weak3.append('None')
        elif i == 3:
            if len(weakData) > 0:
                weak4.append(weakData)
            else:
                weak4.append('None')
        elif i == 4:
            if len(weakData) > 0:
                weak5.append(weakData)
            else:
                weak5.append('None')


    #STRONG AGAINST
    for i in range(0, 5):
        strongData = []
        if len(strong_against_li) > i:
            strong_a = strong_against_li[i].find(name='a')
            strongData.append(strong_a.attrs['href'].split('target_champion=')[1].capitalize())

            strong_winrate_div = strong_a.find(name='div', attrs={'class': 'win-rate'})
            strongData.append(strong_winrate_div.contents[0])

            strong_play_div = strong_a.find(name='div', attrs={'class': 'play'})
            strongData.append(strong_play_div.contents[0])

        if i == 0:
            if len(strongData) > 0:
                strong1.append(strongData)
            else:
                strong1.append('None')
        elif i == 1:
            if len(strongData) > 0:
                strong2.append(strongData)
            else:
                strong2.append('None')
        elif i == 2:
            if len(strongData) > 0:
                strong3.append(strongData)
            else:
                strong3.append('None')
        elif i == 3:
            if len(strongData) > 0:
                strong4.append(strongData)
            else:
                strong4.append('None')
        elif i == 4:
            if len(strongData) > 0:
                strong5.append(strongData)
            else:
                strong5.append('None')

    

    champIndex += 1

# 关闭浏览器
driver.quit()



# 保存数据到DataFrame
df1 = pd.DataFrame(data=[championName, perk1, perk2, perk3, skill1, skill2, sumSpell1, sumSpell2, weak1, weak2, weak3, weak4, weak5, strong1, strong2, strong3, strong4, strong5], index=['championName', 'perk1', 'perk2', 'perk3', 'skill1', 'skill2', 'sumSpell1', 'sumSpell2', 'weak1', 'weak2', 'weak3', 'weak4', 'weak5', 'strong1', 'strong2', 'strong3', 'strong4', 'strong5'])
df2 = pd.DataFrame(df1.values.T, columns=df1.index)
df2.to_csv('./data/build2.csv')