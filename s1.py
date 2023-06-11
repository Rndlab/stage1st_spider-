from selenium import webdriver
from Liver import liver,secretWord
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from login import account_name,password

def get_html(driver, url):
    driver.get(url)
    time.sleep(1)
    return driver.page_source

def get_keyword_count(url, driver):
    html = get_html(driver, url)
    soup = BeautifulSoup(html, "html.parser")
    for blockquote in soup.find_all('blockquote'): # 剔除回复引用
        blockquote.decompose()
    for ignore in soup.find_all('ignore_js_op'): # 剔除图片标签
        ignore.decompose()
    for a in soup.find_all('a'): # 剔除三方客户端挂链
        a.decompose()
    tds = soup.find_all("td", class_="t_f") # 获取正文文本列表
    counts = [0 for _ in range(len(liver))]
    for td in tds: # 遍历楼层内容
        for i, name in enumerate(liver):
            for keyword in liver[name]:
                if re.search(rf"\b{keyword}\b" if keyword in secretWord else rf"{keyword}", td.text):
                    print(td.text)
                    print(f"===match {keyword}===")
                    counts[i]+=1
                    break
    return counts

def login(driver, url): # 登录个人账户
    driver.get(url)
    driver.find_element(By.ID, "ls_username").send_keys(account_name) # 你的账户
    driver.find_element(By.ID, "ls_password").send_keys(password) # 你的密码
    driver.find_element(By.XPATH, "//form[@id='lsform']/div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[3]/button[1]").click()
    time.sleep(5)

def addCounts(counts,page_counts):
    for j in range(len(counts)):
        if len(counts[j]) == 0:
            counts[j].append(page_counts[j])
        else:
            counts[j].append(counts[j][-1] + page_counts[j])
    return counts

if __name__ == "__main__":
    plt.rc("font",family='MicroSoft YaHei',weight="bold")
    options = Options()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'permissions.default.stylesheet': 2,
            'javascript': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./driver/", options=options)
    login(driver, "https://bbs.saraba1st.com/")

    counts = [[] for _ in range(len(liver))] # 总统计矩阵
    # b74
    for i in range(1, 50):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2134542-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)

    # 整理数据
    pageNum = len(counts[0])
    for i in range(len(counts)):
        counts[i].append(list(liver.keys())[i])
    sorted_counts = sorted(counts, key=lambda x: x[-2], reverse=True) # 排序

    for i in range(len(sorted_counts)):
        if sorted_counts[i][pageNum-1] > 50: # 过滤 n 次出现以上的
            plt.plot(sorted_counts[i][:-1], label=f"{sorted_counts[i][pageNum]}({sorted_counts[i][pageNum-1]})") # 添加折线
    plt.legend()
    plt.show()
