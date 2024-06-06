import json
from time import sleep
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils import *


class Searcher:
    def __init__(self, driver: webdriver.Firefox) -> None:
        self.driver = driver

    def __get_element_by_path(self, driver: webdriver.Firefox | WebElement, path: str, timeout=5., by=By.XPATH):
        try:
            return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, path)))
        except:
            return None

    def get_ids(self, keyword: str):
        self.driver.get(
            f"https://www.linkedin.com/search/results/all/?keywords={keyword}")

        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul[2]")
        if ul_element is None:
            return []

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        ul_element = soup.select(
            "body > div:nth-of-type(4) > div:nth-of-type(3) > div:nth-of-type(2) > div > div:nth-of-type(1) > main > div > div > div:nth-of-type(2) > div > ul:nth-of-type(2)")
        if ul_element:
            ul_element = ul_element[0]
        else:
            return []

        li_list: list[Tag] = ul_element.find_all("li")
        ids = []
        for li in li_list:
            a_tag = li.select_one(
                'div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > span:nth-of-type(1) > span > a[href^="https://www.linkedin.com/in/"]')
            if a_tag:
                href = a_tag['href']
                ids.append(extract_linkedin_id(href))

        return ids
