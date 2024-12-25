from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.tasks.task_output import TaskOutput
from supabase import create_client, Client
import os
import kickoff_ids
import uuid
import requests
import asyncio
from pydantic import BaseModel


'''
The output pydantic models for eachg task
'''
class Task11Pydantic(BaseModel):
    target_audience_list: str

class Task21Pydantic(BaseModel):
    buyer_persona:str
    narrative:str
    demographic_information:str 
    psychographic_information:str
    behavioral_information:str
    buying_process:str
    consumption_patterns:str 
    aspirations:str

class Task24Pydantic(BaseModel):
    jtbd_statement:str

class Task25Pydantic(BaseModel):
    stages_of_awareness_analysis:str
    unaware:str
    problem_aware:str
    solution_aware:str
    product_aware:str
    most_aware:str
    summary_and_recommendations:str

class Task31Pydantic(BaseModel):
    value_proposition_canvas:str
    customer_profile:str
    customer_jobs:str
    customer_pains:str
    customer_gains:str
    value_map:str
    pain_relievers:str
    gain_creators:str
    products_and_services:str
    fit_evaluation:str

class Task32Pydantic(BaseModel):
    product:str
    price:str
    place:str
    promotion:str

class Task33Pydantic(BaseModel):
    swot_analysis:str

class Task34Pydantic(BaseModel):
    buyers_journey:str
    awareness_stage:str
    consideration_stage:str
    decision_stage:str
    post_purchase_stage:str
    key_insights:str

class Task41Pydantic(BaseModel):
    brand_story:str
    hero:str
    problem:str
    guide:str
    call_to_action:str
    result:str

class Task42Pydantic(BaseModel):
    aida_framework:str
    summary:str

class Task43Pydantic(BaseModel):
    platform_recommendations:str

class Task44Pydantic(BaseModel):
    lead_stages:str
    stage_name:str
    audience_behavior:str
    audience_thoughts:str
    content_ideas:str
    call_to_action:str
    example_prompt:str

class Task45Pydantic(BaseModel):
    lead_qualification_checklist:str


'''
Custom methods for human inputs 
'''

class AgentFinish:
        thought: str
        output: str
        text: str

        def __init__(self, thought: str, output: str, text: str):
            self.thought = thought
            self.output = output
            self.text = text

def _handle_human_feedback(self, formatted_answer: AgentFinish) -> AgentFinish:
    """
    Handles the human feedback loop, allowing the user to provide feedback
    on the agent's output and determining if additional iterations are needed.

    Parameters:
        formatted_answer (AgentFinish): The initial output from the agent.

    Returns:
        AgentFinish: The final output after incorporating human feedback.
    """
    while self.ask_for_human_input:
        human_feedback = self._ask_human_input(formatted_answer.output)

        if self.crew and self.crew._train:
            self._handle_crew_training_output(formatted_answer, human_feedback)

        # Make an LLM call to verify if additional changes are requested based on human feedback
        additional_changes_prompt = self._i18n.slice(
            "human_feedback_classification"
        ).format(feedback=human_feedback)

        retry_count = 0
        llm_call_successful = False
        additional_changes_response = None

        while retry_count < 2 and not llm_call_successful:
            print(f"Retry count set to: {2}")
            try:
                # Fix: Add a 'user' role message as the first message
                messages = [
                    self._format_msg(f"Feedback: {human_feedback}", role="user"),  # First message is user feedback
                    self._format_msg(additional_changes_prompt, role="system")  # System prompt follows
                ]

                # Make the LLM call with the updated messages
                additional_changes_response = (
                    self.llm.call(
                        messages,
                        callbacks=self.callbacks,
                    )
                    .strip()
                    .lower()
                )
                llm_call_successful = True
            except Exception as e:
                retry_count += 1

                self._printer.print(
                    content=f"Error during LLM call to classify human feedback: {e}. Retrying... ({retry_count}/{2})",
                    color="red",
                )

        if not llm_call_successful:
            self._printer.print(
                content="Error processing feedback after multiple attempts.",
                color="red",
            )
            self.ask_for_human_input = False
            break

        if additional_changes_response == "false":
            self.ask_for_human_input = False
        elif additional_changes_response == "true":
            self.ask_for_human_input = True
            # Add human feedback to messages
            self.messages.append(self._format_msg(f"Feedback: {human_feedback}", role="user"))
            # Invoke the loop again with updated messages
            formatted_answer = self._invoke_loop()

            if self.crew and self.crew._train:
                self._handle_crew_training_output(formatted_answer)
        else:
            # Unexpected response
            self._printer.print(
                content=f"Unexpected response from LLM: '{additional_changes_response}'. Assuming no additional changes requested.",
                color="red",
            )
            self.ask_for_human_input = False

    return formatted_answer


def _ask_human_input(self,final_answer:str)->str:
    print(f"## Final Result: {final_answer}")
    print("Waiting for feedback via FastAPI...")

    feedback=None
    feedback_url = "http://127.0.0.1:8000/submit_feedback/"
    while not feedback:
        try:
            response = requests.get(feedback_url)
            if response.status_code == 200:
                feedback_data = response.json()
                feedback = feedback_data.get("feedback", None)
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching feedback: {e}")
        asyncio.sleep(1)

    return feedback

@CrewBase
class crew1():
    """Akkiai crew"""
    
    agents_config = 'config/agents1.yaml'
    tasks_config = 'config/tasks1.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-haiku-20240307")


    def task_output_callback(self, task_output: TaskOutput, task_input=None):
        """
            Pushes the task output to the database.

            Args:
                task_id (Optional[str]): Unique identifier for the task. If not provided, a new UUID will be generated.
                task_name(Optional[str]): Name of the task. 
                task_input (Optional[Any]): Input data for the task.
                output (TaskOutput): The output of the task.

            Returns:
                None
        """

        url: str= os.environ.get("SUPABASE_URL")
        key: str= os.environ.get("SUPABASE_KEY")
        kickoff_id= kickoff_ids.kickoff_id_temp
        job_id=str(uuid.uuid4())
        task_name=task_output.name
        print(f"Job ID: {job_id}")
        supabase: Client= create_client(url, key)
        supabase.table("run_details").insert({"kickoff_id": kickoff_id,'task_name':task_name,'job_id':job_id, 'input':task_input,'output':task_output.raw}).execute()

        '''
        Pushing the {kickoff_id, tak_name, task_output} to the Webhook URL with POST request
        '''
        webhook_url =os.environ.get("WEBHOOK_URL")
        
        try:
            response=requests.post(
                webhook_url,
                json={
                    "kickoff_id": kickoff_id,
                    "task_name": task_name,
                    "task_output": task_output.raw
                },
                timeout=10
                )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            # Log the success
            print(f"Webhook sent successfully: {response.status_code}, {response.json()}")

        except requests.exceptions.RequestException as e:
            # Log any errors during the webhook call
            print(f"Error sending webhook: {str(e)}")

    #Agent1
    @agent
    def TargetAudienceAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TargetAudienceAgent'],
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
            #human_input=True,
            output_pydantic=Task11Pydantic,
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
    
@CrewBase
class crew2():
    
    """Akkiai crew"""
    agents_config = 'config/agents2.yaml'
    tasks_config = 'config/tasks2.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-haiku-20240307")
    
    def task_output_callback(self, task_output: TaskOutput, task_input=None):
        """
            Pushes the task output to the database.

            Args:
                task_id (Optional[str]): Unique identifier for the task. If not provided, a new UUID will be generated.
                task_name(Optional[str]): Name of the task. 
                task_input (Optional[Any]): Input data for the task.
                output (TaskOutput): The output of the task.

            Returns:
                None
        """

        url: str= os.environ.get("SUPABASE_URL")
        key: str= os.environ.get("SUPABASE_KEY")
        kickoff_id= kickoff_ids.kickoff_id_temp
        job_id=str(uuid.uuid4())
        task_name=task_output.name
        print(f"Job ID: {job_id}")
        supabase: Client= create_client(url, key)
        supabase.table("run_details").insert({"kickoff_id": kickoff_id,'task_name':task_name,'job_id':job_id, 'input':task_input,'output':task_output.raw}).execute()

        '''
        Pushing the {kickoff_id, tak_name, task_output} to the Webhook URL with POST request
        '''
        webhook_url =os.environ.get("WEBHOOK_URL")
        
        try:
            response=requests.post(
                webhook_url,
                json={
                    "kickoff_id": kickoff_id,
                    "task_name": task_name,
                    "task_output": task_output.raw
                },
                timeout=10
                )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            # Log the success
            print(f"Webhook sent successfully: {response.status_code}, {response.json()}")

        except requests.exceptions.RequestException as e:
            # Log any errors during the webhook call
            print(f"Error sending webhook: {str(e)}")
        
    
    #Agent1
    @agent
    def BuyerPersonaAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BuyerPersonaAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent2
    @agent
    def B2CPersonaAnalystAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['B2CPersonaAnalystAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent3
    @agent
    def B2BPersonaAnalystAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['B2BPersonaAnalystAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent4
    @agent
    def JTBDAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['JTBDAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent5
    @agent
    def StagesofAwarenessAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['StagesofAwarenessAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #task1
    @task
    def BuyerPersonaAgent_task(self) -> Task:

        return Task(
            config=self.tasks_config['creating_buyer_persona'],
            output_format='json',
            input_file='output/target_audience.json',
            output_file='output/buyer_persona.json',
            #context= [self.TargetAudienceAgent_task()],
            output_pydantic=Task21Pydantic,
            callback=self.task_output_callback
        )

    #task2
    @task
    def B2CPersonaAnalystAgent_task(self) -> Task:

        return Task(
            config=self.tasks_config['creating_b2c_persona'],
            output_format='json',
            #input_file='persona_input.txt',
            output_file='output/b2c_persona_output.json',
            #context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            context= [self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
    #task3
    @task
    def B2BPersonaAnalystAgent_task(self) -> Task:
        
        return Task(
            config=self.tasks_config['creating_b2b_persona'],
            #input_file='persona_input.txt',
            output_format='json',
            output_file='output/b2b_persona_output.json',
            #context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            context= [self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
 
    #task4
    @task
    def JTBDAnalysisAgent_task(self) -> Task:
        
        return Task(
            config=self.tasks_config['analysing_jtbd'],
            output_format='json',
            input_file='output/buyer_persona.json',
            output_file='output/jtbd_output.json',
            #context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task()],
            context= [self.BuyerPersonaAgent_task()],
            output_pydantic=Task24Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def StagesofAwarenessAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysing_stages_of_awareness'],
            output_format='json',
            input_file='output/jtbd_output.json',
            output_file='output/awareness_output.json',
            #context= [self.TargetAudienceAgent_task(),self.BuyerPersonaAgent_task(),self.JTBDAnalysisAgent_task()],
            context= [self.BuyerPersonaAgent_task(),self.JTBDAnalysisAgent_task()],
            output_pydantic=Task25Pydantic,
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


@CrewBase
class crew3():
    '''
    This is a third crew class that inherits from CrewBase. It contains the same agents and tasks as crew1, but with different configurations.
    '''

    """Akkiai crew"""
    agents_config = 'config/agents3.yaml'
    tasks_config = 'config/tasks3.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-haiku-20240307")
    
    def task_output_callback(self, task_output: TaskOutput, task_input=None):
        """
            Pushes the task output to the database.

            Args:
                task_id (Optional[str]): Unique identifier for the task. If not provided, a new UUID will be generated.
                task_name(Optional[str]): Name of the task. 
                task_input (Optional[Any]): Input data for the task.
                output (TaskOutput): The output of the task.

            Returns:
                None
        """

        url: str= os.environ.get("SUPABASE_URL")
        key: str= os.environ.get("SUPABASE_KEY")
        kickoff_id= kickoff_ids.kickoff_id_temp
        job_id=str(uuid.uuid4())
        task_name=task_output.name
        supabase: Client= create_client(url, key)
        supabase.table("run_details").insert({"kickoff_id": kickoff_id,'task_name':task_name,'job_id':job_id, 'input':task_input,'output':task_output.raw}).execute()

        '''
        Pushing the {kickoff_id, tak_name, task_output} to the Webhook URL with POST request
        '''
        webhook_url =os.environ.get("WEBHOOK_URL")
        
        try:
            response=requests.post(
                webhook_url,
                json={
                    "kickoff_id": kickoff_id,
                    "task_name": task_name,
                    "task_output": task_output.raw
                },
                timeout=10
                )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            # Log the success
            #print(f"Webhook sent successfully: {response.status_code}, {response.json()}")

        except requests.exceptions.RequestException as e:
            # Log any errors during the webhook call
            print(f"Error sending webhook: {str(e)}")
        
    #Agent1
    @agent
    def ProductAudienceFitAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ProductAudienceFitAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def Market4PAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['Market4PAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def SWOTAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['SWOTAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def MappingBuyerJourneyAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['MappingBuyerJourneyAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def ProductAudienceFitAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_audience_fit'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task31Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def Market4PAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_4p_analysis'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task32Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def SWOTAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['swot_analysis'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task33Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def MappingBuyerJourneyAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['mapping_buyer_journey'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task34Pydantic,
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
    
@CrewBase
class crew4():
    '''
    This is 4th crew class that inherits from CrewBase. It contains the same agents and tasks as crew1, but with different configurations.
    '''

    """Akkiai crew"""
    agents_config = 'config/agents4.yaml'
    tasks_config = 'config/tasks4.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-haiku-20240307")
    
    def task_output_callback(self, task_output: TaskOutput, task_input=None):
        """
            Pushes the task output to the database.

            Args:
                task_id (Optional[str]): Unique identifier for the task. If not provided, a new UUID will be generated.
                task_name(Optional[str]): Name of the task. 
                task_input (Optional[Any]): Input data for the task.
                output (TaskOutput): The output of the task.

            Returns:
                None
        """

        url: str= os.environ.get("SUPABASE_URL")
        key: str= os.environ.get("SUPABASE_KEY")
        kickoff_id= kickoff_ids.kickoff_id_temp
        job_id=str(uuid.uuid4())
        task_name=task_output.name
        print(f"Job ID: {job_id}")
        supabase: Client= create_client(url, key)
        supabase.table("run_details").insert({"kickoff_id": kickoff_id,'task_name':task_name,'job_id':job_id, 'input':task_input,'output':task_output.raw}).execute()

        '''
        Pushing the {kickoff_id, tak_name, task_output} to the Webhook URL with POST request
        '''
        webhook_url =os.environ.get("WEBHOOK_URL")
        
        try:
            response=requests.post(
                webhook_url,
                json={
                    "kickoff_id": kickoff_id,
                    "task_name": task_name,
                    "task_output": task_output.raw
                },
                timeout=10
                )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            # Log the success
            print(f"Webhook sent successfully: {response.status_code}, {response.json()}")

        except requests.exceptions.RequestException as e:
            # Log any errors during the webhook call
            print(f"Error sending webhook: {str(e)}")

    #Agent1
    @agent
    def BrandStoryAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BrandStoryAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def MarketMessageAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['MarketMessageAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def PlatformSlecetionAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['PlatformSlecetionAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def LeadStagesAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['LeadStagesAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent5
    @agent
    def LeadQualificationAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['LeadQualificationAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def BrandStoryAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_story'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def MarketMessageAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_message_aida'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def PlatformSlecetionAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['platform_selection'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def LeadStagesAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_stages'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task44Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def LeadQualificationAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_qualification_checklist'],
            output_format='json',
            output_file='output/target_audience.json',
            output_pydantic=Task45Pydantic,
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