import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv("DEBUG", "False") == "True"
API_URL = os.environ.get("API_URL")
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")

RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")
RABBITMQ_SERVER = os.environ.get("RABBITMQ_SERVER")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")

CELERY_NAMESPACE: str = "CELERY"
CELERY_WORKER_NAME: str = "road-detection-gui"
CELERY_BROKER = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER}:{RABBITMQ_PORT}"
)
CELERY_BACKEND = "rpc://"
CELERY_ENABLE_UTC: bool = False
CELERY_TASK_SERIALIZER: str = "json"
CELERY_RESULT_SERIALIZER: str = "json"
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
