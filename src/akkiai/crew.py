from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.tasks.task_output import TaskOutput
from supabase import create_client, Client
import os
import kickoff_ids
import uuid

#from langchain_anthropic import ChatAnthropic

# Uncomment the following line to use an example of a custom tool
# from akkiai.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class Akkiai():
    """Akkiai crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-5-sonnet-20240620")
    
    def task_output_callback(self,task_output: TaskOutput,task_input=None):
        """
            Pushes the task output to the database.

            Args:
                task_id (Optional[str]): Unique identifier for the task. If not provided, a new UUID will be generated.
                task_input (Optional[Any]): Input data for the task.
                output (TaskOutput): The output of the task.

            Returns:
                None
        """

        url: str= os.environ.get("SUPABASE_URL")
        key: str= os.environ.get("SUPABASE_KEY")
        kickoff_id= kickoff_ids.kickoff_id
        task_id=str(uuid.uuid4())
        supabase: Client= create_client(url, key)
        supabase.table("run_details").insert({"kickoff_id": kickoff_id,'task_id':task_id, 'input':task_input,'output':task_output.raw}).execute()


    @before_kickoff # Optional hook to be executed before the crew starts
    def pull_data_example(self, inputs):
        # Example of pulling data from an external API, dynamically changing the inputs
        inputs['extra_data'] = "This is extra data"
        return inputs

    @after_kickoff # Optional hook to be executed after the crew has finished
    def log_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Results: {output}")
        return output
        
    #Agent1
    @agent
    def TargetAudienceAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TargetAudienceAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #Agent2
    @agent
    def BuyerPersonaAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BuyerPersonaAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def B2CPersonaAnalystAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['B2CPersonaAnalystAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent4
    @agent
    def B2BPersonaAnalystAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['B2BPersonaAnalystAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent5
    @agent
    def JTBDAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['JTBDAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent6
    @agent
    def StagesofAwarenessAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['StagesofAwarenessAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #Agent7
    @agent
    def TGAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TGAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #task1
    @task
    def TargetAudienceAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['finding_target_audience'],
            output_format='json',
            output_file='output/target_audience.json',
            callback=self.task_output_callback
        )

    #task2
    @task
    def BuyerPersonaAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['creating_buyer_persona'],
            output_format='json',
            input_file='output/target_audience.json',
            output_file='output/buyer_persona.json',
            context= [self.TargetAudienceAgent_task()],
            callback=self.task_output_callback
        )

    #task3
    @task
    def B2CPersonaAnalystAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['creating_b2c_persona'],
            output_format='json',
            #input_file='persona_input.txt',
            output_file='output/b2c_persona_output.json',
            context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )

    #task4
    @task
    def B2BPersonaAnalystAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['creating_b2b_persona'],
            #input_file='persona_input.txt',
            output_format='json',
            output_file='output/b2b_persona_output.json',
            context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
 
    #task5
    @task
    def JTBDAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysing_jtbd'],
            output_format='json',
            input_file='output/buyer_persona.json',
            output_file='output/jtbd_output.json',
            context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
    
    #task6
    @task
    def StagesofAwarenessAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysing_stages_of_awareness'],
            output_format='json',
            input_file='output/jtbd_output.json',
            output_file='output/awareness_output.json',
            context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task(),self.JTBDAnalysisAgent_task()],
            callback=self.task_output_callback
        )

    #task7
    @task
    def TGAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysing_TG'],
            output_format='json',
            input_file='output/awareness_output.json',
            output_file='output/tg_output.json',
            context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task(),self.JTBDAnalysisAgent_task(),self.StagesofAwarenessAgent_task()],
            callback=self.task_output_callback
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AkkiAi crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )