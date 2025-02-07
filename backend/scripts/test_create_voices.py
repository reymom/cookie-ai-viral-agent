import json
from config.celery import app


dummy_voice_specs = [
    {
        "voice_text": "Welcome to the future of AI agents in Web3.",
        "output_path": "data/executions/test_video/audio/voice1.mp3",
        "model_name": "microsoft",
        "speaker_name": "US Male"
    },
    {
        "voice_text": "These AI-powered systems are reshaping finance and governance.",
        "output_path": "data/executions/test_video/audio/voice2.mp3",
        "model_name": "facebook",
        "speaker_name": "English"
    }
]

if __name__ == "__main__":
    print("🔍 Sending test data to Celery...")

    result = app.send_task("create_voices", args=[
                           dummy_voice_specs, "data/executions/test_video"])

    # ✅ Use JSON formatting for better readability
    print(f"✅ Task sent! Task ID: {result.id}")
    print(json.dumps({"task_id": result.id,
          "status": "Sent to Celery"}, indent=4))
