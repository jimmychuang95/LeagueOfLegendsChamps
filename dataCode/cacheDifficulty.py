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

championName = []
difficulty = []

url = "https://mobalytics.gg/lol/champions"
driver.get(url)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

champion_div = soup.find_all(name = 'div', attrs = {'class': 'm-12dr3gi'})
if champion_div:
    for i in range(0, len(champion_div)):
        championName.append(champion_div[i].find(name = 'div', attrs = {'class': 'm-123baga'}).text)
        difficulty.append(champion_div[i].find(name = 'p', attrs = {'class': 'm-1nj5h5j'}).text)


df1 = pd.DataFrame({'championName': championName, 'difficulty': difficulty})
df1.to_csv('championDifficulty.csv', encoding='utf-8', index=False)