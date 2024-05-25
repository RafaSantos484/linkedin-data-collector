import json
from bs4 import BeautifulSoup, Tag
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

    def __get_text(self, path: str, by=By.XPATH, driver=None, timeout=3.):
        driver = driver if driver is not None else self.driver
        el = self.__get_element_by_path(driver, path, by=by, timeout=timeout)

        return None if el is None else el.text

    def __get_experiences(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/experience/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
        if ul_element is None:
            return None

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        li_list: list[Tag] = soup.find_all(
            'li', id=lambda x: x and 'profilePagedListComponent' in x)
        if len(li_list) == 0:
            return None

        experiences = []
        for li in li_list:
            title = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > span:nth-of-type(1)")
            if title is None:
                continue
            title = title.text

            hirer = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > span:nth-of-type(1) > span:nth-of-type(1)")
            hirer = hirer.text if hirer is not None else None

            duration = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > span:nth-of-type(2) > span:nth-of-type(1)")
            duration = duration.text if duration is not None else None

            location = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > span:nth-of-type(3) > span:nth-of-type(1)")
            location = location.text if location is not None else None

            info = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(2) > ul > li > div > ul > li > div > div > div > span:nth-of-type(1)")
            info = info.text if info is not None else None

            experiences.append(
                {"title": title, "hirer": hirer, "duration": duration, "location": location, "info": info})

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

            name = None
            title = None
            location = None
            about = None

            loaded_cards = self.__get_element_by_path(
                self.driver, "h2.pvs-header__title", by=By.CSS_SELECTOR, timeout=10) is not None
            if not loaded_cards:
                continue

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            main_element = soup.find("main", class_="scaffold-layout__main")
            if main_element is None:
                continue
            cards: list[Tag] = main_element.find_all("section")
            is_first_card = True
            for card in cards:
                if is_first_card:
                    name_tag = card.find("h1", class_="text-heading-xlarge")
                    if name_tag is None:
                        break

                    title_tag = card.find(
                        "div", class_="text-body-medium break-words")
                    location_tag = card.find(
                        "span", class_="text-body-small inline t-black--light break-words")

                    name = name_tag.get_text().strip()
                    if title_tag is not None:
                        title = title_tag.get_text().strip()
                    if location_tag is not None:
                        location = location_tag.get_text().strip()

                    is_first_card = False
                else:
                    span_tags: list[Tag] = card.find_all(
                        "span", class_="visually-hidden")
                    if len(span_tags) < 2:
                        continue

                    span_texts = [tag.get_text().strip() for tag in span_tags]
                    if span_texts[0].lower() == "sobre":
                        about = span_texts[1]
            if name is None:
                print(f"Failed to obtain info of {url}")
                continue

            # "https://www.linkedin.com/in/{id}/details/experience/"
            experiences = self.__get_experiences(id)
            # "https://www.linkedin.com/in/{id}/details/education/"
            # "https://www.linkedin.com/in/{id}/details/projects/"
            # "https://www.linkedin.com/in/{id}/details/skills/"

            users[id] = {
                "name": name,
                "title": title,
                "location": location,
                "about": about,
                "experiences": experiences
            }

        if output_file is not None:
            f = open('results.json', 'w')
            json.dump(users, f)
            print(f"Exported results to {output_file}")

        return users

    def quit(self):
        self.driver.quit()
