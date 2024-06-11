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
            goal='Evaluate LinkedIn profiles and assign a rating from 0 to 10 based on a specified job position',
            backstory="You are a recruitment specialist with a keen eye for detail, adept at assessing professional profiles and matching them to job requirements.",
            verbose=True,
            allow_delegation=False,
        )
        self.task = Task(
            description=f"Evaluate users in the following JSON, rating then from 0 to 10 regarding their suitability for the job '{self.job}':\n {self.users}",
            expected_output='A brief summary and a rate of each user',
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True,
            llm=ai_model
        )

    def analyze_users(self):
        self.crew.kickoff()
