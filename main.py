import os
import pickle

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from utils import *
from getter import *
from searcher import *


if not os.path.exists('linkedin_cookies.pkl'):
    driver = webdriver.Firefox()
    driver.get('https://www.linkedin.com/login/')
    wait_until_redirect(
        driver, "https://www.linkedin.com/feed/", timeout=float('inf'))

    f = open('linkedin_cookies.pkl', 'wb')
    cookies = driver.get_cookies()
    pickle.dump(driver.get_cookies(), f)
    driver.quit()
else:
    f = open('linkedin_cookies.pkl', 'rb')
    cookies = pickle.load(f)

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options)
driver.get('https://www.linkedin.com/')
for cookie in cookies:
    driver.add_cookie(cookie)

searcher = Searcher(driver)
ids = searcher.get_ids('Developer')
print(ids)

"""
getter = Getter(driver)
getter.driver.get('https://www.linkedin.com/')
for cookie in cookies:
    getter.driver.add_cookie(cookie)

getter.get_users_info(
    ["https://www.linkedin.com/in/felipe-carvalho-6249a5147/",
     "https://www.linkedin.com/in/rafael-santos-6089bb24a/"
     ],
    output_file="results.json")
"""

# getter.quit()
driver.quit()
