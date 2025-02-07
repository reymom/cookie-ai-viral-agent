import os
import uuid
import yaml

from inputs.cookie_api import fetch_trending_topics
from config.celery import logger


def generate_video_input(query="ai agents", days=7):
    """Fetches a trending topic & creates a video input spec as a YAML file."""
    trending_topics = fetch_trending_topics(
        query, days)  # 🔥 Get trending Web3 topics
    selected_topic = trending_topics[0]  # Pick the most popular

    # ✅ Generate a unique execution folder per video
    execution_folder = os.path.join(
        "data/executions", f"video_{uuid.uuid4().hex}")
    os.makedirs(execution_folder, exist_ok=True)

    # Define video input spec structure
    video_input = {
        "execution_folder": execution_folder,
        "topic": selected_topic,
        "theme": "storyteller",
        "topic_type": "EVENT",
        "n_images": 3,
        "voice_specs": [
            {"voice_model": "facebook", "speaker_model": "English"},
            {"voice_model": "microsoft", "speaker_model": "UK Female"}
        ],
        "model_id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "jamendo_client_id": os.getenv("JAMENDO_API_KEY"),
        "audio_params": {"tags": ["electronic"], "language": "en"},
        "subtitle_params": {"fonts": ["data/fonts/pixel.ttf"]}
    }

    spec_path = os.path.join(execution_folder, "video_input.yaml")
    with open(spec_path, "w") as f:
        yaml.dump(video_input, f, default_flow_style=False)

    logger.info(f"✅ Generated video input at: {spec_path}")
    return spec_path


def load_video_input(input_path):
    """
    Load manually configured video input from a YAML file.

    Args:
        input_path (str): Path to the YAML config file.

    Returns:
        list: A list of structured video inputs.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"⚠️ Video input YAML not found: {input_path}")

    with open(input_path, "r") as file:
        config = yaml.safe_load(file)

    return config
