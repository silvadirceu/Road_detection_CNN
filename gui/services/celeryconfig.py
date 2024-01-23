from celery import Celery
from services.settings import *

celery_app = Celery(CELERY_WORKER_NAME, namespace=CELERY_NAMESPACE)
celery_conf = dict()
celery_conf["broker_url"] = CELERY_BROKER
celery_conf["result_backend"] = CELERY_BACKEND
celery_conf["enable_utc"] = CELERY_ENABLE_UTC
celery_conf["task_serializer"] = CELERY_TASK_SERIALIZER
celery_conf["result_serializer"] = CELERY_RESULT_SERIALIZER
celery_conf["accept_content"] = CELERY_ACCEPT_CONTENT


celery_app.conf.update(celery_conf)

celery_app.conf.task_routes = {
    # Celery App route configuration (starting on config.celery_app.py)
    "process_file_task": {"queue": "qroad-detection"},
}
