import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

BASE_URL = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY
}

response = requests.get(BASE_URL, params=params)

data = response.json()
df = pd.DataFrame(data['Time Series (Daily)'])

df = df.T
df.shape
df.index.name = 'date'
df.columns = ["open", "high", "low", "close", "volume"]
df = df.reset_index()
print(df)