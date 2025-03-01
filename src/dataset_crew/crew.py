from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    SerperDevTool,
    PDFSearchTool,
    ScrapeWebsiteTool,
    WebsiteSearchTool,
    FileReadTool,
    DirectoryReadTool,
)
from dataset_crew.tools.dataset_tool import DatasetTool
from dataset_crew.tools.custom_tool import PDFReaderTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class DatasetCrew:
    """DatasetCrew crew for collecting language-specific text data"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def project_manager(self) -> Agent:
        return Agent(config=self.agents_config["project_manager"], verbose=True)

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
            ],
            verbose=True,
        )

    @agent
    def text_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config["text_extractor"],
            tools=[
                SerperDevTool(),
                DatasetTool(),
                PDFSearchTool(),
                ScrapeWebsiteTool(),
                FileReadTool(),
                DirectoryReadTool(),
                # Keep the custom PDFReaderTool as a fallback
                PDFReaderTool(),
            ],
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"],
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["extraction_task"],
            output_file="{language}_dataset.csv",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DatasetCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
