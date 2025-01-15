from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.tasks.task_output import TaskOutput
from supabase import create_client, Client
import helpercodes.kickoff_ids as kickoff_ids
import uuid
import requests
from custompydantics import *
import os

@CrewBase
class crew1():
    """
    Target Audience Specialist 
    """
    
    agents_config = 'config/agent/agents1.yaml'
    tasks_config = 'config/task/tasks1.yaml'
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
    agents_config = 'config/agent/agents2.yaml'
    tasks_config = 'config/task/tasks2.yaml'
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

    agents_config = 'config/agent/agents3.yaml'
    tasks_config = 'config/task/tasks3.yaml'
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
    agents_config = 'config/agent/agents4.yaml'
    tasks_config = 'config/task/tasks4.yaml'
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

    #Agent4
    @agent
    def BABFrameworkAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BABFrameworkAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent5
    @agent
    def PASStoryFrameworkAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['PASStoryFrameworkAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #Agent6
    @agent
    def STPAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['STPAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent7
    @agent
    def CustomerJourneyMappingAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['CustomerJourneyMappingAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent8
    @agent
    def BrandArchetypesModelAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BrandArchetypesModelAgent'],
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
    def BrandMessageSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_message_specialist'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def GTMSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['gtm_specialist'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def BABFrameworkAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['bab_framework'],
            output_pydantic=Task44Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def PASStoryFrameworkAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['pas_story_framework'],
            output_pydantic=Task45Pydantic,
            callback=self.task_output_callback
        )
    
    #task6
    @task
    def STPAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['stp'],
            output_pydantic=Task46Pydantic,
            callback=self.task_output_callback
        )
    
    #task7
    @task
    def CustomerJourneyMappingAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['customer_journey_mapping'],
            output_pydantic=Task47Pydantic,
            callback=self.task_output_callback
        )
    
    #task8
    @task
    def BrandArchetypesModelAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_archetypes_model'],
            output_pydantic=Task48Pydantic,
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
    agents_config = 'config/agent/agents5.yaml'
    tasks_config = 'config/task/tasks5.yaml'
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
    agents_config = 'config/agent/agents6.yaml'
    tasks_config = 'config/task/tasks6.yaml'
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
    def FutureCompetitorsAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['FutureCompetitorAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def BottomUpAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['BottomUpAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def StrategicGroupAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['StrategicGroupAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent5
    @agent
    def PorterFiveForcesAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['PorterFiveForcesAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent6
    @agent
    def SWOTAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['SWOTAnalysisAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent7
    @agent
    def TopDownAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TopDownAnalysisAgent'],
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
    def FutureCompetitorsAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['future_competitors_analysis'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def BottomUpAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['bottom_up_analysis'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def StrategicGroupAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['strategic_group_analysis'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def PorterFiveForcesAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['porters_five_forces'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task6
    @task
    def SWOTAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['swot_analysis'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task7
    @task
    def TopDownAnalysisAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['top_down_analysis'],
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
    agents_config = 'config/agent/agents7.yaml'
    tasks_config = 'config/task/tasks7.yaml'
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
    def LeanCanvasMVPAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['LeanCanvasMVPAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def RoadmapMVPAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['RoadmapMVPAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def PRDTemplateAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['PRDTemplateAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def TechStackFrameworkAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TechStackFrameworkAgent'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def LeanCanvasMVPAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['lean_canvas_mvp'],
            output_pydantic=Task41Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def RoadmapMVPAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['roadmap_mvp'],
            output_pydantic=Task42Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def PRDTemplateAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['prd_template'],
            output_pydantic=Task43Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def TechStackFrameworkAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['techstack_framework'],
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

    agents_config = 'config/agent/agents8.yaml'
    tasks_config = 'config/task/tasks8.yaml'
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
    def ExperiencedStartupFounderSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ExperiencedStartupFounderSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    #Agent2
    @agent
    def SiliconValleyInvestorAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['SiliconValleyInvestorAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent3
    @agent
    def StartupSpecialistAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['StartupSpecialistAgent'],
            llm=self.claude_llm,
            verbose=True
        )
    
    #Agent4
    @agent
    def FamousSiliconValleyTechTitan(self) -> Agent:
        return Agent(
            config=self.agents_config['FamousSiliconValleyTechTitan'],
            llm=self.claude_llm,
            verbose=True
        )

    #task1
    @task
    def ExperiencedStartupFounderSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['experienced_startup_founder_specialist'],
            output_pydantic=Task81Pydantic,
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def SiliconValleyInvestorAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['silicon_valley_investor'],
            output_pydantic=Task82Pydantic,
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def StartupSpecialistAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['startup_specialist'],
            output_pydantic=Task83Pydantic,
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def FamousSiliconValleyTechTitan_task(self) -> Task:
        return Task(
            config=self.tasks_config['famous_silicon_valley_tech_titan'],
            output_pydantic=Task84Pydantic,
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
    agents_config = 'config/agent/agents9.yaml'
    tasks_config = 'config/task/tasks9.yaml'
    claude_llm=LLM(api_key=os.getenv("ANTHROPIC_API_KEY"), model="anthropic/claude-3-haiku-20240307", max_tokens=4096)

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
        #print(str(task_output.json_dict))
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
    def SequoiaCapitalPitchDeckAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['SequoiaCapitalPitchDeckAgent'],
            llm=self.claude_llm,
            #verbose=True
        )
    #Agent2
    @agent
    def GuyKawasaki102030RuleAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['GuyKawasaki102030RuleAgent'],
            llm=self.claude_llm,
            #verbose=True
        )
    
    #Agent3
    @agent
    def VentureCapitalMethodAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['VentureCapitalMethodAgent'],
            llm=self.claude_llm,
            #verbose=True
        )
    
    #Agent4
    @agent
    def FirstChicagoMethodAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['FirstChicagoMethodAgent'],
            llm=self.claude_llm,
            #verbose=True
        )
    
    #Agent5
    @agent
    def RiskFactorSummationMethodAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['RiskFactorSummationMethodAgent'],
            llm=self.claude_llm,
            #verbose=True
        )
    
    #Agent6
    @agent
    def YCombinatorTemplateAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['YCombinatorTemplateAgent'],
            llm=self.claude_llm,
            #verbose=True
        )

    #task1
    @task
    def SequoiaCapitalPitchDeckAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['sequoia_capital_pitch_deck'],
            output_pydantic=Task91Pydantic,
            output_file="outputs/task1.json",
            callback=self.task_output_callback
        )
    
    #task2
    @task
    def GuyKawasaki102030RuleAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['guy_kawasaki102030_rule'],
            #context=[self.] ADD CONTEXT ONLY WHEN TASK TAKES INPUTS FROM OTHER TASK
            output_pydantic=Task92Pydantic,
            output_file="outputs/task2.json",
            callback=self.task_output_callback
        )
    
    #task3
    @task
    def VentureCapitalMethodAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['venture_capital_method'],
            output_pydantic=Task93Pydantic,
            output_file="outputs/task3.json",
            callback=self.task_output_callback
        )
    
    #task4
    @task
    def FirstChicagoMethodAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['chicago_method_agent'],
            output_pydantic=Task94Pydantic,
            output_file="outputs/task4.json",
            callback=self.task_output_callback
        )
    
    #task5
    @task
    def RiskFactorSummationMethodAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_factor_summation_method'],
            output_pydantic=Task95Pydantic,
            output_file="outputs/task5.json",
            callback=self.task_output_callback
        )
    
    #task6
    @task
    def YCombinatorTemplateAgent_task(self) -> Task:
        return Task(
            config=self.tasks_config['ycombinator_template'],
            output_pydantic=Task96Pydantic,
            output_file="outputs/task6.json",
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