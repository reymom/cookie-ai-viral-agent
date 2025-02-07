import redis
import json
from enum import Enum


redis_client = redis.Redis(host="localhost", port=6379, db=0)


class TaskStatus(Enum):
    """Enum for tracking task completion."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskKeys(Enum):
    """Enum for task status keys in Redis."""
    IMAGES_DONE = "images_done"
    VOICES_DONE = "voices_done"


def set_task_status(task_id, key: TaskKeys, status: TaskStatus):
    """Store task progress in Redis."""
    task_status = redis_client.get(task_id)
    if task_status:
        task_status = json.loads(task_status)
    else:
        task_status = {}

    task_status[key.value] = status.value
    redis_client.set(task_id, json.dumps(task_status))


def get_task_status(task_id):
    """Retrieve task progress from Redis."""
    task_status = redis_client.get(task_id)
    if task_status:
        return json.loads(task_status)
    return {}
