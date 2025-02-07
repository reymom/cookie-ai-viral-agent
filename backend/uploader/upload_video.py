import subprocess
import os

UPLOADER_BIN = os.path.join(os.path.dirname(__file__), "uploadercli")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def upload_video(video_path, platform="youtube"):
    """
    Uploads a video to YouTube or Twitter using the uploadercli Go binary.

    Args:
        video_path (str): Path to the video file.
        platform (str): Target platform ('youtube' or 'twitter').

    Returns:
        str: Upload response or error message.
    """
    if not os.path.exists(video_path):
        return f"❌ Error: Video file '{video_path}' not found."

    if not os.path.exists(UPLOADER_BIN):
        return "❌ Error: uploadercli binary not found."

    command = [
        UPLOADER_BIN,
        "-c", CONFIG_FILE,
        "-key", video_path,
        "-storage", "local",
        "-platform", platform
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Video uploaded successfully!\nResponse: {result.stdout}"
        else:
            return f"❌ Upload failed!\nError: {result.stderr}"
    except Exception as e:
        return f"❌ Exception while uploading: {str(e)}"
