import requests
import os
from config.celery import app, logger
from tasks.token_distribution import distribute_tokens

COOKIE_API_KEY = os.getenv("COOKIE_API_KEY")
BASE_URL = "https://api.cookie.fun/v1/hackathon/search"


@app.task(name="track_tweet_engagement")
def track_tweet_engagement(video_topic, tweet_id):
    """Tracks engagement for the tweet related to the video."""
    logger.info(f"🔍 Tracking engagement for tweet: {tweet_id} ({video_topic})")

    headers = {"x-api-key": COOKIE_API_KEY}
    # Adjust date range dynamically
    url = f"{BASE_URL}/{video_topic}?from=2025-01-01&to=2025-12-31"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.error(
                f"❌ API Request Failed: {response.status_code} - {response.text}")
            return

        data = response.json()
        if not data or "ok" not in data or not data["ok"]:
            logger.warning("⚠️ No tweets found.")
            return

        # Search for the tweet ID in the response
        for tweet in data["ok"]:
            if tweet["tweetUrl"].endswith(str(tweet_id)):
                engagement = {
                    "likes": tweet["likesCount"],
                    "retweets": tweet["retweetsCount"],
                    "comments": tweet["repliesCount"],
                    "impressions": tweet["impressionsCount"],
                    "smart_engagement": tweet["smartEngagementPoints"]
                }

                logger.info(f"✅ Found tweet engagement: {engagement}")

                # Trigger token distribution based on engagement
                distribute_tokens.delay(video_topic, engagement)

                return engagement

        logger.warning(f"⚠️ Tweet {tweet_id} not found in search results.")

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Exception while fetching tweet engagement: {e}")
