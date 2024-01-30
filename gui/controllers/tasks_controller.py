from celery.result import AsyncResult
from services.celeryconfig import celery_app
from services.settings import *
from engine.utils.schemas import FileInfo
from services.services import send_file_controller


labels = ["dirty", "potholes", "clean"]


@celery_app.task
def process_task(file_info_json):
    file_info = FileInfo.from_dict(file_info_json)
    response = send_file_controller.send(file_info)
    predictions = response.predictions  # list of prediction objects
    results = []
    for prediction in predictions:
        results.append(f"Classification: {labels[int(prediction.classification)]}")

    return {"results": results}


def get_result(task_id):
    # Retrieve the task result
    result = AsyncResult(task_id, app=celery_app)
    # Check the task status
    if result.successful():
        # Task completed successfully, return the result
        return result.result
    elif result.failed():
        # Task encountered an error, return an error message
        return f"Task failed with error: {result.result}"
    elif result.status == "PENDING":
        # Task is still pending
        return False
    else:
        # Handle other task statuses as needed
        return f"Task status: {result.status}"
