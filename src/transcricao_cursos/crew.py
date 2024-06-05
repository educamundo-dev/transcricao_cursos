from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from transcricao_cursos.tools.custom_tool import MyCustomTool
# from transcricao_cursos.tools.pdf_reader_tool import PDFReaderTool

# Check our tools documentations for more information on how to use them

from crewai_tools import ScrapeWebsiteTool,  SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool, FileReadTool
#PDFSearchTool #, , DirectoryReadTool, 
scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()
web_read = WebsiteSearchTool()
#search_pdf = PDFSearchTool()
#pdf_reader_tool = PDFReaderTool()
search_yt = YoutubeVideoSearchTool()
file_read = FileReadTool()
#file_search = DirectoryReadTool()


@CrewBase
class TranscricaoCursosCrew():
	"""TranscricaoCursos crew"""
	agents_config='config/agents.yaml'
	tasks_config='config/tasks.yaml'

	@agent
	def reader_agent(self) -> Agent:
		return Agent(
			agent_name="reader agent",
			config=self.agents_config['reader_agent'],
			tools=[scrape_tool],
			allow_delegation=False,
			#max_iterations=10,  # Aumenta o número de iterações permitidas
            #max_time=600,  # Aumenta o tempo máximo permitido (em segundos)
			max_rpm=1,
			verbose=True
		)
	
	@agent
	def script_creation_agent(self) -> Agent:
		return Agent(
			agent_name ="script creation agent",
			config=self.agents_config['script_creation_agent'],
			#tools=[web_read],
			allow_delegation=False,
			#max_rpm=1,
			verbose=True
		)

	@agent
	def review_agent(self) -> Agent:
		return Agent(
			agent_name="review agent",
			config=self.agents_config['review_agent'],
			allow_delegation=False,
			#max_rpm=1,
			verbose=True
		)
	
	@agent
	def translator_agent(self) -> Agent:
		return Agent(
			agent_name="translator agent",
			config=self.agents_config['translator_agent'],
			allow_delegation=False,
			#max_rpm=1,
			verbose=True
		)
	
	
	@task
	def reader_task(self) -> Task:
		return Task(
			config=self.tasks_config['reader_task'],
			agent=self.reader_agent(),
			output_file='tests/arq_txt.txt'
		)
	
	@task
	def script_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['script_creation_task'],
			agent=self.script_creation_agent()
		)

	@task
	def review_task(self) -> Task:
		return Task(
			config=self.tasks_config['review_task'],
			agent=self.review_agent()
		)
	
	@task
	def translator_task(self) -> Task:
		return Task(
			config=self.tasks_config['translator_task'],
			agent=self.translator_agent(),
			output_file='tests/report_ptBR.md'
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the TranscricaoCursos crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,  # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			verbose=2
			
		)
