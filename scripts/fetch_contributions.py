import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = "shivangdidthat"
URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")

    if date and level is not None:
        days.append({
            "date": date,
            "level": int(level)
        })

os.makedirs("data", exist_ok=True)

output = {
    "username": USERNAME,
    "updated": datetime.utcnow().isoformat(),
    "days": days
}

with open("data/contributions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Fetched {len(days)} contribution days.")