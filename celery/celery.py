# celery_app.py — shared by both FastAPI and worker
from celery import Celery
from config import settings

celery = Celery(
    settings.CELERY_APP_NAME,
    backend=settings.CELERY_RESULT_BACKEND,
    broker=settings.CELERY_BROKER_URL,
    include=["tasks.pipline.py"]
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    task_routers={
    "tasks.pipline.process":{"queue":"default"}
    }
    #Worker_concurrency
)

celery.conf.task_default_queue = "defualt"