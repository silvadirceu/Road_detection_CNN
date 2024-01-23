# tasks.py

from controllers.send_file_controller import FileInfo, SendFileController
from engine.protocols.rest import Rest
from abstractions.http_handler import HttpHandler
from proto.grpc_client import Grpc_Client
from services.celeryconfig import celery_app
from services.settings import *


rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)

labels = ["dirty", "potholes", "clean"]

@celery_app.task(bind=True, name="process_file_task")
def process_file_task(self, file_info):
    # Perform the file processing logic here
    response = controller.send(file_info)
    prediction = response.predictions
    result = f"Classification: {labels[int(prediction.classification)]}"
    return result

# def get_result(task_id):
#     result = AsyncResult(task_id, app=celery_app)
#     return result.result
