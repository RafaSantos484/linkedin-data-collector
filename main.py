import json
import re
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def extract_linkedin_id(url):
    pattern = r'(https?://)?(www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(3)
    else:
        return None


load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument("headless")

exe_path = ChromeDriverManager().install()
service = Service(exe_path)
driver = webdriver.Chrome(service=service, options=options)
w = WebDriverWait(driver, 30)


def get_element_by_xpath(xpath: str, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        return None


driver.get("https://www.linkedin.com/login")

# login credentials
linkedin_username = os.environ['LINKEDIN_EMAIL']
linkedin_password = os.environ['LINKEDIN_PASSWORD']

get_element_by_xpath(
    "/html/body/div/main/div[2]/div[1]/form/div[1]/input").send_keys(linkedin_username)
get_element_by_xpath(
    "/html/body/div/main/div[2]/div[1]/form/div[2]/input").send_keys(linkedin_password)
get_element_by_xpath(
    "/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()

# place profile URLS here
# example: profile_urls = ["https://www.linkedin.com/in/user1-aavfwd/", "https://www.linkedin.com/in/user2-z344vdC/"]
profile_urls = []
profiles = []

for url in profile_urls:
    driver.get(url)
    title = get_element_by_xpath(
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1").text
    description = get_element_by_xpath(
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]").text
    about = get_element_by_xpath(
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]")
    if about is not None:
        about = about.text

    profiles.append({
        "id": extract_linkedin_id(url), "title": title, "description": description, "about": about
    })

driver.close()
print(profiles)

with open('results.json', 'w') as f:
    json.dump(profiles, f)
