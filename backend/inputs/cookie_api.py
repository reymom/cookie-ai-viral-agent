import os
import requests
import urllib.parse
import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COOKIE_API_KEY")
BASE_URL = "https://api.cookie.fun/v1/hackathon/search"


def fetch_trending_topics(query="ai agents", days=7):
    """Fetches trending Web3 topics from Cookie DataSwarm API."""
    end_date = datetime.now(datetime.timezone.utc).isoformat()
    start_date = end_date - datetime.timedelta(days=days)

    headers = {"x-api-key": API_KEY}
    encoded_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/{encoded_query}?from={start_date}&to={end_date}"

    fallback_topic = ["AI Agents", "Web3 Automation"]
    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ API Request Failed: {
                  response.status_code} - {response.text}")
            return fallback_topic

        data = response.json()

        if not data or "ok" not in data or not data["ok"]:
            print("❌ API returned an empty response.")
            return fallback_topic

        trending_topics = [topic["text"] for topic in data["ok"][:5]]
        return trending_topics

    except requests.exceptions.RequestException as e:
        print(f"❌ Exception occurred while fetching topics: {e}")
        return fallback_topic


def get_top_agents():
    """Fetches top AI agents based on mindshare ranking."""
    headers = {"x-api-key": API_KEY}
    response = requests.get(
        f"{BASE_URL}/agents/agentsPaged?interval=_7Days&page=1&pageSize=5", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
