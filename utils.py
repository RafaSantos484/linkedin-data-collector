import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


def extract_linkedin_id(url):
    match = re.search(r'linkedin\.com/in/([^/?]+)', url)
    if match:
        return match.group(1)
    else:
        return None


def wait_until_redirect(driver: webdriver.Firefox, url: str, timeout=10.):
    WebDriverWait(driver, timeout).until(EC.url_to_be(url))
