import json
from time import sleep
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

    def __get_element_by_path(self, driver: webdriver.Firefox | WebElement, path: str, timeout=5., by=By.XPATH):
        try:
            return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, path)))
        except:
            return None

    def __get_experiences(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/experience/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
        if ul_element is None:
            return []

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        li_list: list[Tag] = soup.find_all(
            "li", id=lambda x: x and "profilePagedListComponent" in x)

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

    def __get_skills(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/skills/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul")
        if ul_element is None:
            return []

        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        for _ in range(10):
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        li_list: list[Tag] = soup.find_all(
            "li", id=lambda x: x and "profilePagedListComponent" in x)

        skills = set()
        for li in li_list:
            skill = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > a > div > div > div > div > span:nth-of-type(1)")
            if skill is None:
                continue
            skill = skill.text

            skills.add(skill)

        return sorted(list(skills))

    def __get_projects(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/projects/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
        if ul_element is None:
            return []

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        li_list: list[Tag] = soup.find_all(
            "li", id=lambda x: x and "profilePagedListComponent" in x)

        projects = []
        for li in li_list:
            title = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > span:nth-of-type(1)")
            if title is None:
                continue
            title = title.text

            duration = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > div > span:nth-of-type(1) > span:nth-of-type(1)")
            duration = duration.text if duration is not None else None

            association = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(2) > ul > li:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > span:nth-of-type(1)")
            association = association.text[15:]\
                if association is not None else None

            about = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(2) > ul > li:nth-of-type(3) > div > ul > li > div > div > div > span:nth-of-type(1)")
            about = about.text if about is not None else None

            projects.append(
                {"title": title, "duration": duration, "association": association, "about": about})

        return projects

    def __get_education(self, id: str):
        self.driver.get(
            f"https://www.linkedin.com/in/{id}/details/education/")
        ul_element = self.__get_element_by_path(
            self.driver, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul")
        if ul_element is None:
            return []

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        li_list: list[Tag] = soup.find_all(
            "li", id=lambda x: x and "profilePagedListComponent" in x)

        education = []
        for li in li_list:
            institution = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > a > div > div > div > div > span:nth-of-type(1)")
            if institution is None:
                continue
            institution = institution.text

            course = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > a > span:nth-of-type(1) > span:nth-of-type(1)")
            course = course.text if course is not None else None

            duration = li.select_one(
                "div > div > div:nth-of-type(2) > div:nth-of-type(1) > a > span:nth-of-type(2) > span:nth-of-type(1)")
            duration = duration.text if duration is not None else None

            education.append(
                {"institution": institution, "course": course, "duration": duration})

        return education

    def get_users_info(self, user_ids: list[str], output_file: str | None = None):
        print("Extracting users info...")
        users = {}
        for id in user_ids:
            url = f"https://www.linkedin.com/in/{id}/"
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
            education = self.__get_education(id)
            # "https://www.linkedin.com/in/{id}/details/projects/"
            projects = self.__get_projects(id)
            # "https://www.linkedin.com/in/{id}/details/skills/"
            skills = self.__get_skills(id)

            users[id] = {
                "name": name,
                "title": title,
                "location": location,
                "about": about,
                "experiences": experiences,
                "skills": skills,
                "projects": projects,
                "education": education,
            }

        if output_file is not None:
            f = open("results.json", "w")
            json.dump(users, f)
            print(f"Exported results to {output_file}")

        return users

    def quit(self):
        self.driver.quit()
