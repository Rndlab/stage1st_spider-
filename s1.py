from selenium import webdriver
from Liver import liver,secretWord
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from login import account_name,password
import os
import pandas as pd

def get_html(driver, url):
    driver.get(url)
    time.sleep(1)
    return driver.page_source

def get_keyword_count(url, driver):
    html = get_html(driver, url)
    soup = BeautifulSoup(html, "html.parser")
    for blockquote in soup.find_all('blockquote'): # 剔除回复引用
        blockquote.decompose()
    for i in soup.find_all('i', class_="pstatus"):  # 编辑记录
        i.decompose()
    for ignore in soup.find_all('ignore_js_op'): # 剔除图片标签
        ignore.decompose()
    for a in soup.find_all('a'): # 剔除三方客户端挂链
        a.decompose()
    tds = soup.find_all("td", class_="t_f") # 获取正文文本列表
    try:
        date = soup.find('div', {'class': 'pti'}).em.text.split()[1] # 获取日期
    except:
        date = ''
    counts = [0 for _ in range(len(liver) + 1)]
    counts[0] = date
    for td in tds: # 遍历楼层内容
        for i, name in enumerate(liver):
            for keyword in liver[name]:
                if re.search(rf"\b{keyword}\b" if keyword in secretWord else rf"{keyword}", td.text):
                    print(f"===match {keyword}===")
                    counts[i + 1]+=1
                    break
    return counts

def login(driver, url): # 登录个人账户
    driver.get(url)
    driver.find_element(By.ID, "ls_username").send_keys(account_name) # 你的账户
    driver.find_element(By.ID, "ls_password").send_keys(password) # 你的密码
    driver.find_element(By.XPATH, "//form[@id='lsform']/div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[3]/button[1]").click()
    time.sleep(5)

def addCounts(counts,page_counts):
    for i in range(1,len(counts)):
        if len(counts[i]) == 1:
            counts[i].append(page_counts[i])
        else:
            counts[i].append(counts[i][-1] + page_counts[i])
    counts[0].append(page_counts[0])
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
    # options.add_argument('--headless')
    service = ChromeService(executable_path='./driver/')
    driver = webdriver.Chrome(options=options, service=service)
    login(driver, "https://bbs.saraba1st.com/")

    counts = [[] for _ in range(len(liver) + 1)] # 总统计矩阵
    counts[0].append('')
    for i in range(1, len(counts)):
        counts[i].append(list(liver.keys())[i-1]) # 添加首行表头
    # b67
    for i in range(1, 761):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2108937-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b68
    for i in range(1, 11):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2112012-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b69
    for i in range(1, 1190):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2112070-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b70
    for i in range(1, 1278):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2115994-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b71
    for i in range(1, 359):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2118910-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b72
    for i in range(1, 1482):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2119861-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b73
    for i in range(1, 1617):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2126250-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b74
    for i in range(1, 778):
        print(f'page{i}')
        url = f"https://bbs.saraba1st.com/2b/thread-2134542-{i}-1.html"
        page_counts = get_keyword_count(url, driver)
        counts = addCounts(counts, page_counts)
    # b75
    # for i in range(1, 10):
    #     print(f'page{i}')
    #     url = f"https://bbs.saraba1st.com/2b/thread-2138754-{i}-1.html"
    #     page_counts = get_keyword_count(url, driver)
    #     counts = addCounts(counts, page_counts)

    # 整理数据
    pageNum = len(counts[0])-1

    # sorted_counts = sorted(counts, key=lambda x: x[-2], reverse=True) # 排序

    df = pd.DataFrame(counts)
    df.to_csv('liver.csv',encoding='utf_8_sig') # 输出统计表
    
    for i in range(1,len(counts)):
        if counts[i][pageNum] > 3: # 过滤 n 次出现以上的
            plt.plot(counts[i][1:], label=f"{counts[i][0]}({counts[i][pageNum]})") # 添加折线
    plt.legend()
    plt.show()
