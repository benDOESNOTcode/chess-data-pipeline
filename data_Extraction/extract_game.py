from datetime import datetime, timedelta, timezone
import requests
import json
import os
import shutil
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

#############
#Block A: Date Calculation
############
now_utc = datetime.now(timezone.utc)
yesterday_utc = now_utc - timedelta(days=2)
yesterday = yesterday_utc.date()

month = yesterday.month
year = yesterday.year

print("Yesterday (UTC):", yesterday)
print("Month:", month)
print("Year:", year)

############
#Block B: Session Setup
############
chess_url = f"https://api.chess.com/pub/player/Hikaru/games/{year}/{month:02d}"
headers = {"User-Agent": "MyChessApp/1.0 (contact: beniels2713.com)"}

session = requests.Session()
retry_strategy = Retry(
    total=5, 
    backoff_factor=1, 
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

############
#Block C: Download Data
############
output_filename = "chess_data.json"

try:
    response = session.get(chess_url, headers=headers)
    response.raise_for_status()
    
    with open(output_filename, "wb") as file:
        file.write(response.content)
    print(f"Successfully downloaded {output_filename}")
    
    data = response.json()

except requests.exceptions.HTTPError as e:
    print(f"Request failed: {e}")
    data = {"games": []}

############
#Block D: Filter Games (UTC Standardized)
############
yesterdays_games = []

for game in data.get("games", []):
    epoch_time = game.get("end_time")
    game_date = datetime.fromtimestamp(epoch_time, tz=timezone.utc).date()
    
    if game_date == yesterday:
        yesterdays_games.append(game)
        print(f"Found game: {game.get('url')}")

print(f"Total games found from yesterday: {len(yesterdays_games)}")

############
#Block E: Storage & Eraser
############
save_dir = f"data/games/date={yesterday.strftime('%Y-%m-%d')}"

if os.path.exists(save_dir):
    print(f"Directory {save_dir} exists. Erasing contents...")
    shutil.rmtree(save_dir)

os.makedirs(save_dir)
print(f"Created directory: {save_dir}")

if yesterdays_games:
    df = pd.DataFrame(yesterdays_games)
    parquet_filename = os.path.join(save_dir, "games.parquet")
    
    df.to_parquet(parquet_filename, index=False)
    print(f"Successfully saved {len(yesterdays_games)} games to {parquet_filename}")
else:
    print("No games found for yesterday. Nothing to save.")