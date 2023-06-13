from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from login import account_name,password

def get_html(driver, url):
    driver.get(url)
    time.sleep(1)
    return driver.page_source

def login(driver, url): # 登录个人账户
    driver.get(url)
    driver.find_element(By.ID, "ls_username").send_keys(account_name) # 你的账户
    driver.find_element(By.ID, "ls_password").send_keys(password) # 你的密码
    driver.find_element(By.XPATH, "//form[@id='lsform']/div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[3]/button[1]").click()
    time.sleep(5)

def count_posts(driver, url_template, start_index, end_index):
    post_counts = {}
    for i in range(start_index, end_index + 1):
        print(f"===page{i}===")
        url = url_template.format(i)
        html = get_html(driver, url)
        soup = BeautifulSoup(html, "html.parser")
        authi_divs = soup.find_all('a', {'class': 'xw1'})
        for authi_div in authi_divs:
            username = authi_div.text.strip()
            print(username)
            if username in post_counts:
                post_counts[username] += 1
            else:
                post_counts[username] = 1
    df = pd.DataFrame.from_dict(post_counts, orient='index', columns=['post_count'])
    df.sort_values(by='post_count', ascending=False, inplace=True)

    df.to_csv('post_counts.csv') # 输出统计表

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
    service = ChromeService(executable_path='./driver/')
    driver = webdriver.Chrome(options=options, service=service)
    login(driver, "https://bbs.saraba1st.com/")

    # b74
    url="https://bbs.saraba1st.com/2b/thread-2134542-{}-1.html"
    count_posts(driver, url, 1, 778)
