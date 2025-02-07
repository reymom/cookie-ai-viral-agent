from config.celery import app, logger
from inputs.video_input import generate_video_input


@app.task(name="generate_input")
def generate_input_task(query="ai agents", days=7):
    """Fetches trending topics and generates video input spec."""
    logger.info(f"🔍 Fetching trending topics for query '{
        query}' (last {days} days)...")

    topic_yaml = generate_video_input(query, days)
    return topic_yaml
