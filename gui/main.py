import os
import streamlit as st
from dotenv import load_dotenv
from abstractions.controller import Controller
from controllers.send_file_controller import FileInfo, SendFileController
from engine.protocols.rest import Rest
from abstractions.http_handler import HttpHandler
from proto.grpc_client import Grpc_Client
from services.settings import *
from services.celeryconfig import celery_app
from engine.tasks import process_file_task

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)

labels = ["dirty", "potholes", "clean"]

def process_file(file_info):
    # Send the file processing task to Celery
    # data = {"name": file_info.name, "chunk": file_info.chunk, "path": file_info.path}
    result = process_file_task.delay({"some": "thing"})
    return result.id

def display_dev_options():
    st.sidebar.subheader("Environment Variables")
    for key, value in os.environ.items():
        st.sidebar.text(f"{key}: {value}")

def gui():
    st.title("Road Detection CNN")

    if DEBUG:
        display_dev_options()

    uploaded_file = st.file_uploader(
        "Choose a image/video file", type=["mp4", "avi", "png", "jpg"]
    )

    if uploaded_file:
        st.write("Processing Video please hold")

        bytes_data = uploaded_file.getvalue()
        file_info = FileInfo(uploaded_file.name, bytes_data)

        task_id = process_file(file_info)
        return task_id
        # response = controller.send(file_info)
        # prediction = response.predictions
        # st.write(f"Classification: {labels[int(prediction.classification)]}")
        # st.write("Processing complete.")


if __name__ == "__main__":
    gui()
