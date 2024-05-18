import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils import *


class Getter:
    def __init__(self, driver: webdriver.Firefox) -> None:
        self.driver = driver

    def wait_until_redirect(self, url: str, timeout=10.):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def __get_element_by_path(self, driver: webdriver.Firefox | WebElement, path: str, timeout=3., by=By.XPATH):
        try:
            return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, path)))
        except:
            return None

    def __get_text(self, xpath: str, driver=None):
        driver = driver or self.driver
        el = self.__get_element_by_path(driver, xpath)

        return None if el is None else el.text

    def __get_experiences(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/experience/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
        if ul_element is None:
            return None

        li_list = ul_element.find_elements(By.XPATH, "./child::*")
        experiences = []
        for li in li_list:
            info_div = self.__get_element_by_path(li, "div/div/div[2]/div[1]/div", timeout=.1) or\
                self.__get_element_by_path(li, "div/div/div[2]/div[1]/a")
            if info_div is not None:
                spans = info_div.find_elements(
                    By.CLASS_NAME, "visually-hidden")
                set_info = set(
                    [span.text for span in spans if span.tag_name == "span"])
                if len(set_info) > 0:
                    experiences.append(tuple(set_info))

        return experiences

    def get_users_info(self, user_urls: list[str], output_file: str | None = None):
        print("Extracting users info...")
        users = {}
        for url in user_urls:
            id = extract_linkedin_id(url)
            if id is None:
                print(f"Invalid URL: {url}")
                continue
            else:
                print(f"Getting info of {url}")

            self.driver.get(url)
            title = self.__get_text(
                "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1")
            if title is None:
                print(f"Failed to obtain info of {url}")
                continue

            description = self.__get_text(
                "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]")
            about = self.__get_text(
                "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]")
            experiences = self.__get_experiences(id)

            users[id] = {
                "title": title, "description": description, "about": about, "experiences": experiences
            }

        if output_file is not None:
            f = open('results.json', 'w')
            json.dump(users, f)
            print(f"Exported results to {output_file}")

        return users

    def quit(self):
        self.driver.quit()
