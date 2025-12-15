import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

BASE_URL = "https://www.alphavantage.co/query"

final_data = []
TOP_20_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "TSLA", "NVDA", "BRK.B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA",
    "DIS", "BAC", "XOM", "NFLX", "ADBE"
]


for symbol in TOP_20_SYMBOLS:
    print(f"Fetching data for {symbol}...")
    params = {
        "function":"TIME_SERIES_DAILY",
        "symbol":symbol,
        "apikey":API_KEY,
        "outputsize":"compact"
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
      print(f"API error / limit hit for {symbol}")
      continue

    symbol_data = data["Time Series (Daily)"]
    
    if symbol_data is None:
        print(f"No data for {symbol}")
        continue
    else:
        df = pd.DataFrame(symbol_data).T
        df.columns = ["open", "high", "low", "close", "volume"]
        df.index.name = 'date'
        df = df.reset_index()
        df["symbol"] = symbol
        df = df[["date", "symbol", "open", "high", "low", "close", "volume"]]
        
        df['date'] = pd.to_datetime(df['date'])
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric)
        df = df.sort_values(by="date")
        df = df.drop_duplicates(subset=['date','symbol'], keep='last') 
        df = df.reset_index(drop=True)
        final_data.append(df)
        time.sleep(12)


final_df = pd.concat(final_data, ignore_index=True)
os.makedirs("finance-dataset/data/processed", exist_ok=True)

final_df.to_csv(
      "finance-dataset/data/processed/top_20_stocks.csv",
    index=False
)
print(final_df.head())
print(final_df.shape)























