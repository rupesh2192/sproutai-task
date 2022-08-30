import os

from django.conf import settings

from celery import Celery
 
app = Celery(
    name="sproutai",
    include=[],
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)
app.autodiscover_tasks(["posts"])
