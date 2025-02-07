import os
import logging
from celery import Celery

os.environ["VIDEO_GENERATOR_PATH"] = "/home/reymon/Projects/inSphere/viralyzer/video-generator"

# Ensure logs directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "celery_tasks.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Celery setup (Redis as broker)
app = Celery("tasks", broker="redis://localhost:6379/0",
             backend="redis://localhost:6379/0")

app.conf.imports = (
    "tasks.generate_video",
    "tasks.generate_content",
    "tasks.generate_input",
    "tasks.assemble_video",
    "tasks.upload_video",
)
app.autodiscover_tasks()

# Task execution settings
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_expires=3600,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/celery_tasks.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
