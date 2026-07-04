# app/celery/celery
from celery import Celery
from app.config import settings

celery = Celery(
    settings.celery_app_name,
    backend=settings.celery_result_backend,
    broker=settings.celery_broker_url,
    include=["app.tasks.pipeline"]
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
    task_routes={
    "tasks.pipeline.process":{"queue":"default"}
    }
    #Worker_concurrency
)

celery.conf.task_default_queue = "default"