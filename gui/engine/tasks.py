# tasks.py
from celery.result import AsyncResult
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

import json
import base64
from engine.utils.file import FileInfo

@celery_app.task
def process_file_task(file_info):
    # Assume you have received file_info_json
    file_info_dict = json.loads(file_info)

    # Decode base64-encoded chunk back to bytes
    chunk_bytes = base64.b64decode(file_info_dict["chunk"])

    # Create the original file_info object
    original_file_info = FileInfo(
        name=file_info_dict["name"],
        chunk=chunk_bytes,
        path=file_info_dict["path"]
    )

    # Perform the file processing logic here
    response = controller.send(original_file_info)
    predictions = response.predictions #list of prediction objects
    print(predictions)
    results = []
    for prediction in predictions:
        results.append(labels[int(prediction.classification)])
    # result = f"Classification: {labels[int(prediction.classification)]}"
    return {"result": results}

def get_result(task_id):
    result = AsyncResult(task_id, app=celery_app)
    print(result.status)
    return result.result