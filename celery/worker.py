from app.celery.celery import celery
from app.celery import signal  # noqa: F401 

__all__ = ["celery"]