from dotenv import load_dotenv
import os
from google.genai import Client

load_dotenv()
client = Client(api_key=os.getenv('GOOGLE_API_KEY'))
models = list(client.models.list())
print(len(models))
for m in models:
    print(m.name)
