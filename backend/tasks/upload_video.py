from config.celery import app, logger
from uploader.upload_video import upload_video


@app.task(name="upload_video_task")
def upload_video_task(video_path, platform="youtube"):
    """Uploads the video to a given platform."""
    logger.info(f"🚀 Uploading video '{video_path}' to {platform}...")

    upload_result = upload_video(video_path, platform)
    logger.info(upload_result)

    return upload_result
