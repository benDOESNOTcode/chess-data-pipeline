import requests

# Use a session to keep headers consistent
session = requests.Session()
session.headers.update({"User-Agent": "MyChessApp/1.0 (contact: your-email@example.com)"})

# 1. Test the Archives endpoint first
archives_url = "https://api.chess.com/pub/player/SlyC00per2713/games/archives"
response = session.get(archives_url)

print(f"Status Code: {response.status_code}")
print(f"Response Data: {response.text}")