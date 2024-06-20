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

    def get_ids(self, keyword: str, limit=3):
        self.driver.get(
            f"https://www.linkedin.com/search/results/people/?keywords={keyword}")

        a_element = self.__get_element_by_path(
            self.driver, "//a[starts-with(@href, 'https://www.linkedin.com/in/')]")
        if a_element is None:
            return []

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        a_tags = soup.find_all('a', href=lambda href: href and href.startswith(
            'https://www.linkedin.com/in/'))
        a_tags = [tag for tag in a_tags if not tag.find('strong')]
        ids = set()
        for a in a_tags:
            ids.add(extract_linkedin_id(a['href']))

        limit = min(limit, len(ids))
        return list(ids)[:limit]
