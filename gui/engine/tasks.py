# tasks.py
from celery.result import AsyncResult
from services.celeryconfig import celery_app
from services.settings import *
from engine.utils.serializers import post_celery_serialize
from services.services import send_file_controller

labels = ["dirty", "potholes", "clean"]@celery_app.task
def process_file_task(file_info):
    # TODO: will be removed
    original_file_info = post_celery_serialize(file_info)

    # Perform the file processing logic here
    response = send_file_controller.send(original_file_info)
    predictions = response.predictions  # list of prediction objects
    results = []
    for prediction in predictions:
        results.append(f"Classification: {labels[int(prediction.classification)]}")
    return {"result": results}

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
