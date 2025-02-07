import os
import json

from config.celery import app, logger
from uploader.pinata import upload_to_pinata
from tasks.tracker import update_task_status, TaskKeys, TaskStatus


@app.task(name="upload_video_to_ipfs")
def upload_video_to_ipfs_task(video_path, execution_folder, image_paths):
    """Uploads video to IPFS via Pinata and triggers image upload if successful."""
    logger.info(f"📤 Uploading video to IPFS: {video_path}")

    ipfs_cid = upload_to_pinata(video_path)

    if not ipfs_cid:
        logger.error("❌ Video upload to IPFS failed. Retrying...")
    else:
        logger.info(f"✅ Video successfully uploaded to IPFS: {ipfs_cid}")
        update_task_status(
            execution_folder, TaskKeys.VIDEO_IPFS_CID.value, ipfs_cid)

    # Trigger image upload
    upload_images_to_ipfs_task.delay(execution_folder, image_paths)


@app.task(name="upload_images_to_ipfs")
def upload_images_to_ipfs_task(execution_folder, image_paths):
    """Uploads images used in the video to IPFS and tracks their CIDs."""
    logger.info(f"📤 Uploading images to IPFS for {execution_folder}")

    image_cids = {}
    for image_path in image_paths:
        ipfs_cid = upload_to_pinata(image_path)

        if not ipfs_cid:
            logger.error(f"❌ Failed to upload {image_path} to IPFS")
            return

        logger.info(f"✅ Image uploaded: {image_path} -> {ipfs_cid}")
        image_cids[image_path] = ipfs_cid

    # Store image CIDs in progress tracker
    update_task_status(
        execution_folder, TaskKeys.IMAGE_IPFS_CID.value, image_cids)
    logger.info("✅ All images uploaded to IPFS successfully.")
