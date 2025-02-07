import json
from config.celery import app


def test_video_generation():
    """Runs the full video pipeline using Celery tasks (for debugging)."""

    query = "ai agents"
    days = 7

    print(f"🔍 Fetching trending topics for query '{
          query}' in the last {days} days...")

    # Step 1: Trigger video generation process
    result = app.send_task("generate_video", kwargs={
                           "query": query, "days": days})

    print(json.dumps({
        "task_id": result.id,
        "status": "Video generation process started",
        "query": query,
        "days": days
    }, indent=4))


if __name__ == "__main__":
    test_video_generation()
