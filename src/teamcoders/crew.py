import os
import time
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_openai import ChatOpenAI

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def task_callback(output):
    """Callback to add delay between tasks to respect API rate limits."""
    # Wait 7 seconds between tasks to stay under 8 RPM limit
    time.sleep(7)

@CrewBase
class Teamcoders():
    """Teamcoders crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Initialize LLM for Ollama
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen3-coder-next:cloud")

        self.llm = ChatOpenAI(
            model=ollama_model,
            openai_api_key="sk-not-needed",
            openai_api_base=ollama_base_url,
            temperature=0.7
        )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'], # type: ignore[index]
            llm=self.llm,
            verbose=True,
            max_iter=5,
            max_rpm=8
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'], # type: ignore[index]
            llm=self.llm,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3,
            max_iter=5,
            max_rpm=8
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'], # type: ignore[index]
            llm=self.llm,
            verbose=True,
            max_iter=5,
            max_rpm=8
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'], # type: ignore[index]
            llm=self.llm,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3,
            max_iter=10,
            max_rpm=8
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'], # type: ignore[index]
            async_execution=False,
            callbacks=[task_callback]
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'], # type: ignore[index]
            async_execution=False,
            callbacks=[task_callback]
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'], # type: ignore[index]
            async_execution=False,
            callbacks=[task_callback]
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'], # type: ignore[index]
            async_execution=False,
            callbacks=[task_callback]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Teamcoders crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
