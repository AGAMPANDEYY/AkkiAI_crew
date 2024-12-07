import os 
import datetime
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str= os.environ.get("SUPABASE_KEY")
supabase: Client= create_client(url, key)

#Insert data
kickoff_id=1234
job_status="on"
create_date=datetime.datetime.now()
update_date=datetime.datetime.now()
response = (
    supabase.table("kickoff_details")
    .insert({"kickoff_id": kickoff_id, "job_status": job_status, "create_date":create_date, "update_date":update_date})
    .execute()
)

task_id=1234
input="aass"
output="aass"
response = (
    supabase.table("run_details")
    .insert({"kickoff_id": kickoff_id, "task_id": task_id, "input":input, "output":output})
    .execute()
)

#Fetch data

response = supabase.table("kickoff_details").select("*").execute()

