from app.api.content_creation import assemble_video
from config.celery import app, logger
from tasks.upload_video import upload_video_task
from tasks.nft_tasks import generate_nft_metadata_and_mint


@app.task(name="assemble_video_task")
def assemble_video_task(spec, image_paths):
    """Task 3: Assemble the final video."""
    execution_folder = spec["execution_folder"]
    logger.info(f"🎬 Assembling video for {spec['topic']}...")

    images = [{"image_path": path, "duration": 5} for path in image_paths]
    voices = [
        {"file_path": voice["output_path"], "start_time": voice["start_time"]}
        for voice in spec["voice_specs"]
    ]
    output_video_path = assemble_video(
        images=images,
        audio_file=spec["background_audio"],
        output_path=f"{execution_folder}/final_video.mp4",
        voices=voices,
        subtitles=spec["subtitles"],
        title=spec["topic"],
        description=f"AI-generated video about {spec['topic']}.",
        tags=[spec["theme"], spec["topic"]],
    )

    logger.info(f"✅ Video assembled successfully: {output_video_path}")

    # 🔹 Log the path so it can be manually uploaded later if needed
    with open(f"{execution_folder}/video_path.log", "w") as f:
        f.write(output_video_path + "\n")

    # 🔹 Trigger the upload tasks
    upload_video_task.delay(output_video_path, platform="youtube")

    # 🔹 Generate Metadata & Mint NFTs (Trigger after IPFS Upload)
    generate_nft_metadata_and_mint.delay(
        spec["topic"], output_video_path, image_paths)

    return output_video_path
