from celery.schedules import crontab
from config.celery import app


# Celery Beat: Schedule video generation every 3 hours
app.conf.beat_schedule = {
    "generate_video_every_3_hours": {
        "task": "generate_video_specs",
        "schedule": crontab(minute=0, hour="*/3"),  # Every 3 hours
    },
}
