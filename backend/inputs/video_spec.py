import json

from app.model.types.topic import TopicType
from app.api.content_creation import (
    generate_image_prompts,
    generate_voice_specs,
    generate_subtitles_from_voices,
    process_audio_with_jamendo
)
from inputs.video_input import load_video_input
from config.celery import logger


def generate_video_spec(input_path):
    """Generate structured specification for an AI-generated video based on a YAML config."""

    video_input = load_video_input(input_path)
    if not video_input:
        raise ValueError("⚠️ No video specs found in YAML!")

    logger.info(f"Generating video spec:\n{
                json.dumps(video_input, indent=2)}")

    # Extract parameters from config
    execution_folder = video_input["execution_folder"]
    topic = video_input["topic"]
    theme = video_input["theme"]
    topic_type = TopicType[video_input["topic_type"]]  # Convert string to Enum
    n_images = video_input["n_images"]
    voice_specs = video_input["voice_specs"]
    n_voices = len(voice_specs)
    model_id = video_input["model_id"]
    jamendo_client_id = video_input["jamendo_client_id"]
    audio_params = video_input["audio_params"]
    subtitle_params = video_input["subtitle_params"]

    # Generate image prompts
    image_prompts = generate_image_prompts(
        topic, topic_type, theme, model_id, n_images)

    # Generate voice-over specifications
    voice_generation_specs = generate_voice_specs(
        topic, topic_type, theme, model_id, execution_folder, n_voices,
        [v["voice_model"] for v in voice_specs], [
            v["speaker_model"] for v in voice_specs]
    )

    # ✅ Compute accurate total video duration (max end time of voices, images, subtitles)
    voice_end_times = [voice_spec["start_time"] + voice_spec["duration"]
                       for voice_spec in voice_generation_specs]
    image_durations = [image["duration"] for image in image_prompts]
    subtitle_end_times = [sub["end_time"]
                          for sub in subtitle_params.get("subtitles", [])]

    total_video_duration = max(
        voice_end_times + image_durations + subtitle_end_times)
    logger.info(f"📏 Computed video duration: {total_video_duration} seconds")

    # Generate subtitles dynamically based on voices
    subtitles = generate_subtitles_from_voices(
        voice_generation_specs,
        fonts=subtitle_params.get("fonts"),
        fontsizes=subtitle_params.get("fontsizes"),
        colors=subtitle_params.get("colors"),
        stroke_colors=subtitle_params.get("stroke_colors"),
        stroke_widths=subtitle_params.get("stroke_widths")
    )

    # Process background music from Jamendo
    audio_output_path = f"{execution_folder}/audios/background_audio.mp3"
    processed_audio = process_audio_with_jamendo(
        client_id=jamendo_client_id,
        output_path=audio_output_path,
        duration=total_video_duration,
        **audio_params
    )

    return {
        "execution_folder": execution_folder,
        "topic": topic,
        "theme": theme,
        "image_prompts": image_prompts,
        "voice_specs": voice_generation_specs,
        "subtitles": subtitles,
        "background_audio": processed_audio,
        "total_duration": total_video_duration
    }
