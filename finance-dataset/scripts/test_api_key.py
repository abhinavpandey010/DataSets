import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if api_key:
    print("sucess")
    print("Key length:", len(api_key))
else:
    print("API key NOT loaded")