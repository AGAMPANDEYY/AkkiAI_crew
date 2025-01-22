from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, Header
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from crew import crew1, crew2, crew3, crew4, crew5, crew6, crew7, crew8, crew9
import helpercodes.kickoff_ids as kickoff_ids
from pathlib import Path
import os 
from datetime import datetime
import secrets
import traceback 
import hmac
import hashlib
import anthropic
from pytz import timezone 
import uuid
import requests



app = FastAPI(docs_url=None, redoc_url=None)
url: str = os.environ.get("SUPABASE_URL")
key: str= os.environ.get("SUPABASE_KEY")
supabase: Client= create_client(url, key)
feedback_store={"human_feedback":None}

#for api end point security 
security=HTTPBasic()
DOCS_USERNAME=os.getenv("API_USERNAME1", "default_user")
DOCS_PASSWORD=os.getenv("API_PASSWORD1","default_password")
API_KEY=os.getenv("API_KEY", "apikey")
SECRET_KEY=os.getenv("SECRET_KEY")
ANTHROPIC_API= os.getenv("ANTHROPIC_API_KEY")

#Configuration for CORS 

origins=[
    "https://nimble-gnome-f8228f.netlify.app/home",
    "http://localhost:5173",
    "https://api.akki.ai/run",
    "https://beta.akki.ai/",
    "https://beta.akki.ai"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define input models for endpoints
class RunInputs(BaseModel):
    
    SOLUTION_ID: str #added extra input for choosing the solution id 
    INPUT_1: str
    #INPUT_2: str
    #INPUT_3: str
    #INPUT_4: str
    #INPUT_5: str
    #INPUT_6: str
    #INPUT_7: str
    HASH: str

#Anthropic Chat Endpoint Inputs
class ChatInputs(BaseModel):
    MESSAGE: str
    HASH: str

class TrainInputs(BaseModel):
    BUSINESS_DETAILS: str
    PRODUCT_DESCRIPTION: str
    n_iterations: int

class TestInputs(BaseModel):
    BUSINESS_DETAILS: str
    PRODUCT_DESCRIPTION: str
    n_iterations: int
    openai_model_name: str

class FeedbackInputs(BaseModel):
    HUMAN_FEEDBACK: str

#Function to authenticate user 
#Authenticate Doc endpoints
async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401, detail="Unauthorized", 
            headers={"WWW-Authenticate": "Basic"}
        )

#Function to authenticate api and secrets
async def authenticate_api_key(api_key: str = Header(None)):
    """
    Dependency to authenticate API Key and Secret.
    """
    if not (secrets.compare_digest(api_key or "", API_KEY)):
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")


async def compute_hash(data: str,secret_key: str) ->str:
     """
     Computes hash with secret key at backend server with data received. Uses Hmac algorithm
     """
     return hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()

@app.post("/submit_feedback/", dependencies=[Depends(authenticate_api_key)])
async def submit_feedback(human_feedback:FeedbackInputs):
    '''
    Endpoint to accept human feedback
    '''
    feedback_store["human_feedback"] = human_feedback.HUMAN_FEEDBACK
        
    # Prepare the message to send to Anthropic API
    formatted_feedback = human_feedback.HUMAN_FEEDBACK.strip()
    
    # You can add a system prompt if needed
    system_prompt = "You are a helpful assistant. Process the feedback and determine if changes are necessary."

    # Create the structured messages list for the Anthropic API
    messages = [
        {"role": "user", "content": formatted_feedback}  # Add user feedback as the second message
    ]

    return human_feedback.HUMAN_FEEDBACK

@app.post("/run", dependencies=[Depends(authenticate_api_key)])
async def run(inputs: RunInputs, background_tasks: BackgroundTasks):
    try:
        solution_id=inputs.SOLUTION_ID
        input1=inputs.INPUT_1
        received_hash=inputs.HASH
         
        #if not (solution_id and input1 and input2 and input3 and received_hash):
        if not (solution_id and input1 and received_hash):
            raise HTTPException(status_code=400, detail="Invalid input data")
        
        #computing hash from received data
        data_string=f"{solution_id}|{input1}"

        #compute hash from data string
        computed_hash= await compute_hash(data_string,SECRET_KEY)

        # Validate the hash
        if not hmac.compare_digest(received_hash, computed_hash):
            raise HTTPException(status_code=401, detail="Unauthorized: Hash does not match")
        
        else: 
            if solution_id == "1":
               akkiai_instance = crew1()

            elif solution_id == "2":
                akkiai_instance = crew2()

            elif solution_id == "3":
                akkiai_instance = crew3()

            elif solution_id == "4":
                akkiai_instance = crew4()
            
            elif solution_id == "5":
                akkiai_instance = crew5()
            
            elif solution_id == "6":
                akkiai_instance = crew6()

            elif solution_id == "7":
                akkiai_instance = crew7()
            
            elif solution_id == "8":
                akkiai_instance = crew8()
            
            elif solution_id == "9":
                akkiai_instance = crew9()

            else:
                return f"Solution id must be 1-9"
            
            crew_instance = akkiai_instance.crew()
            
            if crew_instance is None:
                raise ValueError("Failed to initialize Crew instance.")
            
            # Generate kickoff ID and metadata 
            kickoff_id=crew_instance.id
            kickoff_id=str(kickoff_id)
            kickoff_ids.kickoff_id_temp = str(crew_instance.id)
            print("kickoff id temp is :",kickoff_ids.kickoff_id_temp)
            create_date = datetime.utcnow().isoformat()
            update_date = create_date #what does this mean
            job_status = "on"

            supabase.table("kickoff_details").insert({"kickoff_id": kickoff_id, "job_status": job_status, "create_date":create_date, "update_date":update_date}).execute()
            
            background_tasks.add_task(run_crew_bg, crew_instance, inputs, solution_id, kickoff_id)
            
            return {"kickoff_id": kickoff_id}
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Exception in /run: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error running crew: {str(e)}. Traceback: {error_details}")

async def run_crew_bg(crew_instance, inputs, solution_id, kickoff_id ):
    try: 
        if solution_id == "1":
            # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
                #"BUSINESS_DETAILS": inputs.INPUT_1,
                #"PRODUCT_DESCRIPTION": inputs.INPUT_2
            })

        elif solution_id == "2":
             # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
                #"TARGET_AUDIENCE": inputs.INPUT_1,
                #"BUSINESS_DETAILS": inputs.INPUT_2,
                #"PRODUCT_DESCRIPTION": inputs.INPUT_3
            })

        elif solution_id == "3":

            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
                #"TARGET_AUDIENCE": inputs.INPUT_2,
                #"PRODUCT_DESCRIPTION": inputs.INPUT_3
            })
        
        elif solution_id == "4":
              # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
            })

        elif solution_id == "5":
            # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
            })
        elif solution_id == "6":
            # Pass the inputs to the backend agent (replace with your actual logic)
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
            })
        elif solution_id == "7":
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
            })
        elif solution_id == "8":
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
            })
        elif solution_id == "9":
            result = await crew_instance.kickoff_async(inputs={
                "STARTUP_INFO": inputs.INPUT_1,
                #"BUSINESS_DETAILS": inputs.INPUT_2,
                #"PRODUCT_DESCRIPTION": inputs.INPUT_3,
                #"TARGET_AUDIENCE": inputs.INPUT_4,
                #"CUSTOMER_PERSONA": inputs.INPUT_5,
                #"VALUE_PROPOSITION": inputs.INPUT_6,
                #"MESSAGING": inputs.INPUT_7

            })
        
        job_status = "off"
        update_date =  datetime.utcnow().isoformat()
        supabase.table("kickoff_details").update({'job_status':job_status, 'update_date':update_date}).eq("kickoff_id",kickoff_ids.kickoff_id_temp).execute()
   
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Exception in run_kickoff: {error_details}")

#running all the chats simultaneously in the background
async def chat_bg( input,input_message, kickoff_id,create_date):
    
    client= anthropic.Anthropic(api_key=ANTHROPIC_API)
    MODEL_NAME="claude-3-haiku-20240307"

    message = client.messages.create(
                model=MODEL_NAME,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": input.MESSAGE}
                ]
            )
    
    message_id= message.id
    anthropic_response= message.content[0].text

    """
    Push the message id and the anthropic response to the SUPABASE db
    kickoff_id column --> message_id
    task_name column ---> the model that is being used here Haiku 3
    task_input column --> the input provided by the user
    
    """
    update_date= datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    job_status="off"
    task_name= message.model
    job_id= str(uuid.uuid4())
    supabase.table("kickoff_details").update({'kickoff_id':message_id,'job_status':job_status, 'update_date':update_date,}).eq("create_date",create_date).execute()
    supabase.table("run_details").insert({"kickoff_id": message_id,'task_name':task_name,'job_id':job_id, 'input':input_message,'output':anthropic_response}).execute()
    webhook_url =os.environ.get("WEBHOOK_URL")
        
    try:
        response=requests.post(
            webhook_url,
            json={
                "kickoff_id": message_id,
                "task_name": task_name,
                "task_output": message.content[0].text #This will now send strings
            },
            timeout=10
            )
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        # Log the success
        #print(f"Webhook sent successfully: {response.status_code}, {response.json()}")

    except requests.exceptions.RequestException as e:
        # Log any errors during the webhook call
        print(f"Error sending webhook: {str(e)}")

#Chat endpoint for AkkiAI
@app.post("/chat", dependencies= [Depends(authenticate_api_key)])
async def chat(input: ChatInputs, background_tasks: BackgroundTasks):
    try:
        input_message=input.MESSAGE
        received_hash= input.HASH

        if not (input_message and received_hash):
            raise HTTPException(status_code=400, detail="Invalid input data")
        
        data_string=f"{input_message}"
        #compute hash from data string
        computed_hash= await compute_hash(data_string,SECRET_KEY)

        # Validate the hash
        if not hmac.compare_digest(received_hash, computed_hash):
            raise HTTPException(status_code=401, detail="Unauthorized: Hash does not match")
        else: 
            if not ANTHROPIC_API:
                raise ValueError("ANTHROPIC_API environment variable not found. Please set it with your API key.")

 
            """
            Pushing the data into Kickoff_id table
            """
            create_date = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
            update_date = create_date #what does this mean
            job_status = "on"
            kickoff_id= str(uuid.uuid4())
           

            supabase.table("kickoff_details").insert({"kickoff_id": kickoff_id, "job_status": job_status, "create_date":create_date, "update_date":update_date}).execute()
            background_tasks.add_task(chat_bg,input,input_message,kickoff_id,create_date)
     
            return {"The Chat has been submitted. Message ID:": kickoff_id}
        
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/train", dependencies=[Depends(authenticate_api_key)])
async def train(inputs: TrainInputs):
    try:
        crew1().crew().train(
            n_iterations=inputs.n_iterations,
            filename=inputs.filename,
            inputs={"BUSINESS_DETAILS": inputs.BUSINESS_DETAILS, "PRODUCT_DESCRIPTION": inputs.PRODUCT_DESCRIPTION},
        )
        return {"message": "Training completed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training crew: {str(e)}")

@app.post("/replay", dependencies=[Depends(authenticate_api_key)])
async def replay(task_id: str):
      try:
        crew1().crew().replay(task_id=task_id)
        return {"message": "Replay executed successfully!"}
      except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error replaying crew: {str(e)}")

@app.post("/test", dependencies=[Depends(authenticate_api_key)])
async def test(inputs: TestInputs):
    try:
        crew1().crew().test(
            n_iterations=inputs.n_iterations,
            openai_model_name=inputs.openai_model_name,
            inputs={"BUSINESS_DETAILS": inputs.BUSINESS_DETAILS, "PRODUCT_DESCRIPTION": inputs.PRODUCT_DESCRIPTION},
        )
        return {"message": "Test executed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing crew: {str(e)}")
    
@app.get("/", dependencies=[Depends(authenticate)])
async def root():
    return {"message": "Welcome to the CrewAI API!"}

@app.get("/{username}/{password}")
async def solution_page(username: str, password: str):
    if username == DOCS_USERNAME and password == DOCS_PASSWORD:
        return {"message": "Access granted to the solution page"}
    raise HTTPException(
        status_code=401, detail="Unauthorized access"
    )

@app.get("/docs", dependencies=[Depends(authenticate)])
async def fastapi_docs():
    """
    Custom route for /docs to protect it with authentication.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="AkkiAI Multi Agents"
    )
@app.get("/redoc", dependencies=[Depends(authenticate)])
async def custom_redoc():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Secure API Docs")