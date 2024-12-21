from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
#from src.akkiai.crew import Akkiai
from crew import Akkiai, crew2, crew3
import kickoff_ids
from pathlib import Path
import os 
from datetime import datetime
import uuid
import traceback



app = FastAPI()
url: str = os.environ.get("SUPABASE_URL")
key: str= os.environ.get("SUPABASE_KEY")
supabase: Client= create_client(url, key)

# Define input models for endpoints
class RunInputs(BaseModel):
    SOLUTION_ID: int #added extra input for choosing the solution id 
    INPUT_1: str
    INPUT_2: str
    INPUT_3: str
    INPUT_4: str

class TrainInputs(BaseModel):
    BUSINESS_DETAILS: str
    PRODUCT_DESCRIPTION: str
    n_iterations: int

class TestInputs(BaseModel):
    BUSINESS_DETAILS: str
    PRODUCT_DESCRIPTION: str
    n_iterations: int
    openai_model_name: str

@app.post("/run")
async def run(inputs: RunInputs):
    try:
        solution_id=inputs.SOLUTION_ID
        if solution_id == 1:
           akkiai_instance = Akkiai()

        elif solution_id == 2:
           akkiai_instance = crew2()

        elif solution_id == 3:
            akkiai_instance = crew3()

        else:
            return f"Solution id must be 1-3"
        
        crew_instance = akkiai_instance.crew()
        
        if crew_instance is None:
            raise ValueError("Failed to initialize Crew instance.")
        print("Crew instance initialized successfully.")

        # Generate kickoff ID and metadata 
        kickoff_id=crew_instance.id
        kickoff_id=str(kickoff_id)
        kickoff_ids.kickoff_id_temp = str(crew_instance.id)
        print("kickoff id temp is :",kickoff_ids.kickoff_id_temp)
        create_date = datetime.utcnow().isoformat()
        update_date = create_date #what does this mean
        job_status = "on"

        supabase.table("kickoff_details").insert({"kickoff_id": kickoff_id, "job_status": job_status, "create_date":create_date, "update_date":update_date}).execute()
        
        if solution_id == 1:
             # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "BUSINESS_DETAILS": inputs.INPUT_1,
                "PRODUCT_DESCRIPTION": inputs.INPUT_2
            })

        elif solution_id == 2:
             # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "MARKET_DATA_URL": inputs.INPUT_1,
                "RESEARCH_FOCUS": inputs.INPUT_2
            })

        elif solution_id == 3:
            # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "MARKET_DATA_URL": inputs.INPUT_1
            })
      
        
        job_status = "off"
        update_date =  datetime.utcnow().isoformat()
        supabase.table("kickoff_details").update({'job_status':job_status, 'update_date':update_date}).eq("kickoff_id",kickoff_ids.kickoff_id_temp).execute()

        return {"kickoff_id": kickoff_id}
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Exception in /run: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error running crew: {str(e)}. Traceback: {error_details}")

@app.post("/train")
async def train(inputs: TrainInputs):
    try:
        Akkiai().crew().train(
            n_iterations=inputs.n_iterations,
            filename=inputs.filename,
            inputs={"BUSINESS_DETAILS": inputs.BUSINESS_DETAILS, "PRODUCT_DESCRIPTION": inputs.PRODUCT_DESCRIPTION},
        )
        return {"message": "Training completed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training crew: {str(e)}")

@app.post("/replay")
async def replay(task_id: str):
      try:
        Akkiai().crew().replay(task_id=task_id)
        return {"message": "Replay executed successfully!"}
      except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error replaying crew: {str(e)}")

@app.post("/test")
async def test(inputs: TestInputs):
    try:
        Akkiai().crew().test(
            n_iterations=inputs.n_iterations,
            openai_model_name=inputs.openai_model_name,
            inputs={"BUSINESS_DETAILS": inputs.BUSINESS_DETAILS, "PRODUCT_DESCRIPTION": inputs.PRODUCT_DESCRIPTION},
        )
        return {"message": "Test executed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing crew: {str(e)}")
    
@app.get("/")
async def root():
    return {"message": "Welcome to the CrewAI API!"}