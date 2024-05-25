import os
import pickle

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from utils import *
from getter import *

if not os.path.exists('linkedin_cookies.pkl'):
    getter = Getter(webdriver.Firefox())
    getter.driver.get('https://www.linkedin.com/login/')
    getter.wait_until_redirect(
        "https://www.linkedin.com/feed/", timeout=float('inf'))

    f = open('linkedin_cookies.pkl', 'wb')
    cookies = getter.driver.get_cookies()
    pickle.dump(getter.driver.get_cookies(), f)
    getter.quit()
else:
    f = open('linkedin_cookies.pkl', 'rb')
    cookies = pickle.load(f)

options = Options()
options.add_argument("--headless")
getter = Getter(webdriver.Firefox(options))
getter.driver.get('https://www.linkedin.com/')
for cookie in cookies:
    getter.driver.add_cookie(cookie)

getter.get_users_info(
    ["https://www.linkedin.com/in/felipe-carvalho-6249a5147/",
     "https://www.linkedin.com/in/rafael-santos-6089bb24a/"
     ],
    output_file="results.json")

getter.quit()

""""
Generating .exe file:
    pyinstaller main.py -F --onefile
    or
    python -m pyinstaller main.py -F --onefile
"""
