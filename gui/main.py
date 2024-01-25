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
from engine.tasks import process_file_task, get_result

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)

labels = ["dirty", "potholes", "clean"]

import json
import base64
def process_file(file_info):
    # Send the file processing task to Celery
    # data = {"name": file_info.name, "chunk": file_info.chunk, "path": file_info.path}
    chunk_base64 = base64.b64encode(file_info.chunk).decode('utf-8')
    file_info_dict = {
        "name": file_info.name,
        "chunk": chunk_base64,  # Assuming chunk is bytes; convert to str
        "path": file_info.path
    }
    file_info_json = json.dumps(file_info_dict)
    result = process_file_task.delay(file_info_json)
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
        return st.write(task_id)

    task_id_input = st.text_input("Enter Task ID:", value="")

    # Button to get result
    if st.button("Get Result"):
        if task_id_input:
            # Get the result using the provided task_id
            result = get_result(task_id_input)

            # Display the result
            if result is not None:
                st.write(f"Task ID: {task_id_input}")
                st.write("Result:")
                st.write(result)
            else:
                st.write(f"No result available for Task ID: {task_id_input}")
        else:
            st.write("Please enter a Task ID.")
    
        # response = controller.send(file_info)
        # prediction = response.predictions
        # st.write(f"Classification: {labels[int(prediction.classification)]}")
        # st.write("Processing complete.")


if __name__ == "__main__":
    gui()
