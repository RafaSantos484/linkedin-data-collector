import json
import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager

from getters import *

options = Options()
options.add_argument("--headless")

# service = Service(GeckoDriverManager().install())

driver = webdriver.Firefox(options)
driver.get('https://www.linkedin.com')
with open('linkedin_cookies.pkl', 'rb') as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# place profile URLS here
# example: profile_urls = ["https://www.linkedin.com/in/user1-aavfwd/", "https://www.linkedin.com/in/user2-z344vdC/"]
profile_urls = ["https://www.linkedin.com/in/felipe-carvalho-6249a5147/"]

profiles = []
for url in profile_urls:
    id = extract_linkedin_id(url)

    driver.get(url)
    title = get_text(
        driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1")
    description = get_text(driver,
                           "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]")
    about = get_text(driver,
                     "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]")
    experiences = get_experiences(driver, id)

    profiles.append({
        "id": id, "title": title, "description": description, "about": about, "experiences": experiences
    })

driver.quit()
# print(profiles)

with open('results.json', 'w') as f:
    json.dump(profiles, f)
    print("exported to results.json")
