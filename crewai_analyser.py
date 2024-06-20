import json
from crewai import Agent, Task, Crew
import os

from langchain_community.llms import Ollama

os.environ["OPENAI_API_KEY"] = "null"
os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] = "crewai-llama2"

ai_model = Ollama()


class CrewaiAnalyser:
    def __init__(self, users: dict, job: str) -> None:
        self.users = users
        self.job = job
        self.agent = Agent(
            role='LinkedIn Profiles Analyst',
            goal='Evaluate a LinkedIn profile and assign a rating from 0 to 10 based on a specified job position',
            backstory="You are a recruitment specialist with a keen eye for detail, adept at assessing professional profiles and matching them to job requirements.",
            verbose=True,
            allow_delegation=False,
        )

    def user_to_string(self, user_id):
        user_info = self.users[user_id]
        str_user = f'Username: {user_info["name"]}\n'
        str_user += f'User job: {user_info["title"]}\n'
        str_user += f'About the user: {user_info["about"]}\n'

        return str_user

    def analyze_users(self):
        results = dict()
        for user_id in self.users.keys():
            task = Task(
                description=f'Evaluate the following linkedin user, rating him from 0 to 10 regarding their suitability for the job "{self.job}":\n {self.user_to_string(user_id)}',
                expected_output='A brief summary and a rate of each user',
                agent=self.agent,
            )
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True,
                llm=ai_model
            )
            results[user_id] = crew.kickoff()

        f = open("crewai_results.json", "w")
        json.dump(results, f)
        print(f"Exported CrewAi results to crewai_results.json")
