import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

DATA_EXECUTIONS_PATH = os.path.join(BASE_DIR, "data/executions")
os.makedirs(DATA_EXECUTIONS_PATH, exist_ok=True)

VIDEO_INPUTS_PATH = os.path.join(DATA_EXECUTIONS_PATH, "video_inputs")
os.makedirs(VIDEO_INPUTS_PATH, exist_ok=True)
