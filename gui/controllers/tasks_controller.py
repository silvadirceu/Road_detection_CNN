from celery.result import AsyncResult
from services.celeryconfig import celery_app
from services.settings import *
from engine.utils.serializers import post_celery_serialize
from services.services import send_file_controller

labels = ["dirty", "potholes", "clean"]

@celery_app.task
def process_file_task(file_info):
    #TODO: Review serialization pipeline
    original_file_info = post_celery_serialize(file_info)

    # # Perform the file processing logic here
    response = send_file_controller.send(original_file_info)
    predictions = response.predictions  # list of prediction objects
    results = []
    for prediction in predictions:
        results.append(f"Classification: {labels[int(prediction.classification)]}")
    return {"results": results}