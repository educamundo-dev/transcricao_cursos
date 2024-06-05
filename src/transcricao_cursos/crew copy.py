from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from transcricao_cursos.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SerperDevTool
scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

@CrewBase
class TranscricaoCursosCrew():
	"""TranscricaoCursos crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def transcriber(self) -> Agent:
		return Agent(
			config=self.agents_config['transcriber'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			tools=[
				scrape_tool,
				search_tool,
							],
			verbose=True
		)
 #
#	@agent
#	def translator(self) -> Agent:
#		return Agent(
#			config=self.agents_config['translator'],
#			# max_rpm=None,
#			verbose=True
#		)

	@task
	def transcriber_task(self) -> Task:
		return Task(
			config=self.tasks_config['transcriber_task'],
			agent=self.transcriber(),
			output_file='report.md'
		)

#	@task
#	def translator_task(self) -> Task:
#		return Task(
#			config=self.tasks_config['translator_task'],
#			agent=self.translator(),
#			output_file='report.md'
#		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TranscricaoCursos crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)