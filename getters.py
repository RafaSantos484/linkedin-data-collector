import re
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


def extract_linkedin_id(url):
    pattern = r'(https?://)?(www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(3)
    else:
        return None


def get_element_by_path(driver: webdriver, path: str, timeout=3., by=By.XPATH) -> WebElement | None:
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, path)))
    except:
        return None


def get_text(driver: webdriver, xpath: str):
    el = get_element_by_path(driver, xpath)

    return None if el is None else el.text


def get_experiences(driver: webdriver, id: str):
    driver.get(f"https://www.linkedin.com/in/{id}/details/experience/")
    ul_element = get_element_by_path(
        driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
    if ul_element is None:
        return None

    li_list = ul_element.find_elements(By.XPATH, "./child::*")
    experiences = []
    for li in li_list:
        info_div = get_element_by_path(li, "div/div/div[2]/div[1]/div", timeout=.1) or\
            get_element_by_path(li, "div/div/div[2]/div[1]/a")
        if info_div is not None:
            try:
                spans = info_div.find_elements(
                    By.CLASS_NAME, "visually-hidden")
                set_info = set(
                    [span.text for span in spans if span.tag_name == "span"])
                experiences.append(tuple(set_info))
            except:
                print('error...')
        else:
            print("no info...")

    for experience in experiences:
        print(experience)
        print("\n\n")
    print(len(experiences))

    return experiences
