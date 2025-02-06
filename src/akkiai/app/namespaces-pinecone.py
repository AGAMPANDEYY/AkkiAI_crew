from pinecone import Pinecone 
import os 
from dotenv import load_dotenv

load_dotenv()

pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index=pc.Index(host="https://akkiai-chat-py172ny.svc.aped-4627-b74a.pinecone.io")

index_stats=index.describe_index_stats()

namespaces= list(index_stats["namespaces"].keys())

print(namespaces)

