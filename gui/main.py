import os
import time
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
from engine.utils.serializers import pre_celery_serialize

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)

labels = ["dirty", "potholes", "clean"]

import json
import base64


def process_file(file_info):
    # Send the file processing task to Celery
    # TODO: Handle serialization from source
    file_info_json = pre_celery_serialize(file_info)
    result = process_file_task.delay(file_info_json)
    return result.id


def display_dev_options():
    st.sidebar.subheader("Developer Environment")

    task_id_input = st.sidebar.text_input("Debug Task ID:", value="")
    if st.sidebar.button("Get Result"):
        if task_id_input:
            # Get the result using the provided task_id
            result = get_result(task_id_input)
            # Display the result
            if result is not None:
                st.sidebar.write(f"Task ID: {task_id_input}")
                st.sidebar.write("Result:")
                st.sidebar.write(result)
            else:
                st.sidebar.write(f"No result available for Task ID: {task_id_input}")
        else:
            st.sidebar.write("Please enter a valid Task ID.")

    for key, value in os.environ.items():
        st.sidebar.text(f"{key}: {value}")

def gui():
    st.set_page_config(
        page_title="Road Scanner",
        page_icon="",
        layout="wide",
    )
    st.title("Road Detection CNN")

    if DEBUG:
        display_dev_options()

    with st.form("upload-form", clear_on_submit=True):
        file = st.file_uploader(
            "Choose a video file", type=["mp4", "avi", "png", "jpg"]
        )
        submitted = st.form_submit_button("Upload")

    response_container = st.empty()

    if submitted and file is not None:
        response_container.empty()  # clear response container
        bytes_data = file.getvalue()
        file_info = FileInfo(file.name, bytes_data)
        task_id = process_file(file_info)

        with response_container:
            st.write("Processing Video please hold")
            # st.write(get_result(task_id=task_id))
            while True:
                result = get_result(task_id=task_id)
                if result:
                    st.write(result)
                    break
                time.sleep(4)
        # st.rerun()  # Uncomment to batch test requests


if __name__ == "__main__":
    gui()
