from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.tasks.task_output import TaskOutput
from supabase import create_client, Client
import helpercodes.kickoff_ids as kickoff_ids
import uuid
import requests
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os


'''
The output pydantic models for eachg task
'''

class TargetGroupsPydantic(BaseModel):
    characteristics: str
    reasons: str

# Define the main model that contains target_audience as a key
class Task11Pydantic(BaseModel):
    target_audience: Dict[str,TargetGroupsPydantic]

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

class Task35Pydantic(BaseModel):
    market_analysis:str

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


@CrewBase
class crew1():
    """
    Target Audience Specialist 
    """
    
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
            output_json=Task11Pydantic,
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
        )
    
@CrewBase
class crew2():
    
    """
    Customer Persona Journey Crew
    """
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
            output_pydantic=Task21Pydantic,
            callback=self.task_output_callback
        )

    #task2
    @task
    def B2CPersonaAnalystAgent_task(self) -> Task:

        return Task(
            config=self.tasks_config['creating_b2c_persona'],
            context= [self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
    #task3
    @task
    def B2BPersonaAnalystAgent_task(self) -> Task:
        
        return Task(
            config=self.tasks_config['creating_b2b_persona'],
            context= [self.BuyerPersonaAgent_task()],
            callback=self.task_output_callback
        )
 
    #task4
    @task
    def JTBDAnalysisAgent_task(self) -> Task:
        
        return Task(
            config=self.tasks_config['analysing_jtbd'],
            context= [self.BuyerPersonaAgent_task()],
            output_pydantic=Task24Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def StagesofAwarenessAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysing_stages_of_awareness'],
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
        )


@CrewBase
class crew3():
    '''
     USP,Value Proposition Analysis Mult-Agent
    '''

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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def ValuePropCanvasAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ValuePropCanvas'],
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
    def USPRoseFrameworkAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['USPRoseFrameworkAgent'],
            llm=self.claude_llm,
            verbose=True
        )
        
    #Agent5
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
            output_pydantic=Task31Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def Market4PAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_4p_analysis'],
            output_pydantic=Task32Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def SWOTAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['swot_analysis'],
            output_pydantic=Task33Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def MappingBuyerJourneyAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['mapping_buyer_journey'],
            output_pydantic=Task34Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def USPRoseFrameworkAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['usp_rose_framework'],
            output_pydantic=Task35Pydantic,
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
        )
    
@CrewBase
class crew4():
    '''
    Branding and GTM Framework 
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def BrandMessageSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BrandMessageSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def GTMSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['GTMSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def BrandStoryAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_story'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def MarketMessageAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_message_aida'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def PlatformSlecetionAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['platform_selection'],
            output_pydantic=Task43Pydantic,
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
        )
    
@CrewBase
class crew5():
    '''
    Market Readiness and Tech Advancements Multi-agents
    '''

    """Akkiai crew"""
    agents_config = 'config/agents5.yaml'
    tasks_config = 'config/tasks5.yaml'
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def MarketReadinessAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['MarketReadinessAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def TechnologyAdoptionSpecilistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TechnologyAdoptionSpecilistAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def RiskAssesmentSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['RiskAssesmentSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def BlueOceanSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BlueOceanSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def MarketReadinessAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_readiness'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def TechnologyAdoptionSpecilistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['technology_adoption_specilist'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def RiskAssesmentSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_assessment_specialist'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def BlueOceanSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['blue_ocean_specialist'],
            output_pydantic=Task44Pydantic,
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
        )
        
@CrewBase
class crew6():
    '''
    Competition Research Multi-agents
    '''

    """Akkiai crew"""
    agents_config = 'config/agents6.yaml'
    tasks_config = 'config/tasks6.yaml'
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def TamSamSomAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TamSamSomAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def FutureCompetitorsAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['FutureCompetitorsAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def TamSamSomAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['tam_sam_som'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def FutureCompetitorsAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['future_competitors'],
            output_pydantic=Task42Pydantic,
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
        )
    
@CrewBase
class crew7():
    '''
    Product Frameworks - MVP (Definition), Roadmap (Now, Next, Later framework), PRD (MVP), Tech Stack (Framework)
    '''

    """Akkiai crew"""
    agents_config = 'config/agents7.yaml'
    tasks_config = 'config/tasks7.yaml'
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def YCPromptAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['YCPromptAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def VCFeedbackAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['VCFeedbackAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def TechTitanFeedbackAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TechTitanFeedbackAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def UpdatedApplicationAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['UpdatedApplicationAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def YCPromptAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['yc_prompt'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def VCFeedbackAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['vc_feedback'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def TechTitanFeedbackAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['tech_titan_feedback'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def UpdatedApplicationAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['updated_application'],
            output_pydantic=Task44Pydantic,
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
        )
    
@CrewBase
class crew8():
    '''
    YC Application prompt, VC Feedback Prompt, Revised Application, Tech Titan Feedback and Application Prompt
    '''

    agents_config = 'config/agents8.yaml'
    tasks_config = 'config/tasks8.yaml'
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
    def YCPromptAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['YCPromptAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def VCFeedbackAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['VCFeedbackAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def TechTitanFeedbackAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TechTitanFeedbackAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def UpdatedApplicationAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['UpdatedApplicationAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def YCPromptAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['yc_prompt'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def VCFeedbackAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['vc_feedback'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def TechTitanFeedbackAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['tech_titan_feedback'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def UpdatedApplicationAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['updated_application'],
            output_pydantic=Task44Pydantic,
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
        )
    
@CrewBase
class crew9():
    '''
    Pitch Deck - Investment Frameworks (3), Pitch Deck (3 versions) 
    '''

    """Akkiai crew"""
    agents_config = 'config/agents9.yaml'
    tasks_config = 'config/tasks9.yaml'
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
                    "task_output": str(task_output.json_dict) #This will now send strings
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
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def MarketMessageAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_message_aida'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def PlatformSlecetionAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['platform_selection'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def LeadStagesAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_stages'],
            output_pydantic=Task44Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def LeadQualificationAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_qualification_checklist'],
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
        )