from selenium import webdriver
import pandas as pd  #导入pandas库
import bs4  # 导入bs4库
from bs4 import BeautifulSoup  # 导入BeautifulSoup库
import time
from selenium.webdriver.chrome.options import Options

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
driver = webdriver.Chrome(options=options)

# 打开网页
url = "https://www.op.gg/champions?region=kr&tier=all"
driver.get(url)

# 等待页面加载（根据需要调整等待时间）
time.sleep(3)


# 获取页面源代码并关闭浏览器
html = driver.page_source
driver.quit()

# 使用 BeautifulSoup 解析页面
soup = BeautifulSoup(html, "html.parser")
tbody = soup.find('tbody')

top = []
name = []       #建立空列表用于储存数据
tier = []
position = []
winRate = []
pickRate = []
banRate = []

# 检查是否找到tbody
if tbody:
    # 遍历tbody标签的子标签
    for tr in tbody.children:
        # 判断tr是否为标签类型，去除空行
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            # 提取数据
            top.append(tds[0].find('span').string)

            name.append(tds[1].find('strong').string)
            
            tier.append(tds[2].get_text().strip())  # 获取文本，去除两端的空白字符
            
            img_tag = tds[3].find('img')
            trimed = img_tag['alt'].replace('ROLE-', '')  # 获取alt属性
            position.append(trimed)

            win_rate_contents = tds[4].contents
            win_rate = win_rate_contents[0]  # 假设数值是第一个元素
            winRate.append(win_rate.strip())  # 去除可能的空白字符

            pick_rate_contents = tds[5].contents
            pick_rate = pick_rate_contents[0]
            pickRate.append(pick_rate.strip())

            ban_rate_contents = tds[6].contents
            ban_rate = ban_rate_contents[0]
            banRate.append(ban_rate.strip())

else: 
    print('fail to find body')

# 保存数据到DataFrame
df1 = pd.DataFrame(data=[top, name, tier, position, winRate, pickRate, banRate], index=['top', 'name', 'tier', 'position', 'winRate', 'pickRate', 'banRate'])
df2 = pd.DataFrame(df1.values.T, columns=df1.index)
df2.to_csv('all.csv')