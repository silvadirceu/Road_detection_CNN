import os
import streamlit as st
from dotenv import load_dotenv
from abstractions.controller import Controller
from controllers.send_file_controller import FileInfo, SendFileController
from engine.protocols.rest import Rest
from abstractions.http_handler import HttpHandler
from proto.grpc_client import Grpc_Client


load_dotenv()
API_URL = os.environ.get("API_URL")
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)


def gui():
    st.title("Road Detection CNN")
    st.title(f"{COMPUTER_VISION_SERVICE}")
    uploaded_file = st.file_uploader(
        "Choose a image/video file", type=["mp4", "avi", "png", "jpg"]
    )
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        file_info = FileInfo(uploaded_file.name, bytes_data)
        response = controller.send(file_info)
        st.write(response)


if __name__ == "__main__":
    gui()
