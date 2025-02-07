from inputs.video_spec import generate_video_spec
from config.celery import app, logger
from tasks.generate_input import generate_input_task
from tasks.assemble_video import assemble_video_task
from tasks.generate_content import create_voices, create_images
from tasks.tracker import get_task_status, TaskKeys, TaskStatus


@app.task(name="generate_video")
def generate_video_task(query, days):
    logger.info(f"🔄 Starting `generate_video` with query='{
        query}', days={days}")
    input_path = generate_input_task(query, days)
    logger.info(f"✅ `generate_video_input` returned input_path={input_path}")
    generate_video_spec_task.delay(input_path)


@app.task(name="generate_video_spec")
def generate_video_spec_task(input_path):
    """Task 1: Generate video spec."""
    logger.info("🎬 Generating video spec...")
    video_spec = generate_video_spec(input_path)

    execution_folder = video_spec["execution_folder"]
    logger.info(f"🎥 Creating video in {execution_folder}")

    create_voices.delay(video_spec["voice_specs"], execution_folder)

    # generate images
    image_prompts = video_spec["image_prompts"]
    image_paths = image_paths = [
        f"{execution_folder}/images/image_{i}.png" for i in range(len(image_prompts))
    ]
    create_images.delay(image_prompts, execution_folder, image_paths)

    # ✅ Monitor & assemble when ready
    monitor_tasks_and_assemble.delay(execution_folder, video_spec, image_paths)


@app.task(name="monitor_tasks_and_assemble")
def monitor_tasks_and_assemble(execution_folder, video_spec, image_paths):
    """Monitors task completion & assembles video when ready."""
    task_status = get_task_status(execution_folder)

    if task_status.get(TaskKeys.IMAGES_DONE.value) == TaskStatus.DONE.value and \
       task_status.get(TaskKeys.VOICES_DONE.value) == TaskStatus.DONE.value:
        logger.info(f"🎥 All assets ready for {
                    video_spec['topic']}. Starting assembly...")
        assemble_video_task.delay(video_spec, image_paths)
    else:
        logger.info(f"⏳ Waiting for assets to be ready for {
                    video_spec['topic']}...")
