from app.api.content_creation import generate_voice, generate_images
from config.celery import app, logger
from tasks.tracker import set_task_status, TaskKeys, TaskStatus


@app.task(name="create_voices")
def create_voices(voice_specs, execution_folder):
    """Task 2b: Generate voice-overs."""
    logger.info(f"Generating voice-overs")

    for voice_spec in voice_specs:
        generate_voice(
            voice_text=voice_spec.get("voice_text", ""),
            output_path=voice_spec.get("output_path", ""),
            model_name=voice_spec.get("model_name", ""),
            speaker_name=voice_spec.get("speaker_name", "")
        )

    set_task_status(execution_folder,
                    TaskKeys.VOICES_DONE, TaskStatus.DONE)
    logger.info(f"✅ Voice-overs completed.")


@app.task(name="create_images")
def create_images(image_prompts, execution_folder, image_paths):
    """Task 2a: Generate images."""
    logger.info(f"Generating images in {execution_folder}")

    generate_images(image_prompts, image_paths)

    set_task_status(execution_folder, TaskKeys.IMAGES_DONE, TaskStatus.DONE)
    logger.info(f"✅ Images generated successfully.")

    return image_paths
