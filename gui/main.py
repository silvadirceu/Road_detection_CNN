import os
import streamlit as st
from dotenv import load_dotenv
from abstractions.controller import Controller
from controllers.send_file_controller import FileInfo, SendFileController
from engine.protocols.rest import Rest
from abstractions.http_handler import HttpHandler
from proto.grpc_client import Grpc_Client


load_dotenv()
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
API_URL = os.environ.get("API_URL")
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)

labels = ['dirty', 'potholes', 'clean']

def display_dev_options():
    st.sidebar.subheader("All Environment Variables")
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

        # Assuming `controller.send` returns a gRPC response object
        response = controller.send(file_info)
        # Assuming the response has a predictions field
        for prediction in response.predictions:
            # Display each classification in the Streamlit app
            st.write(f"Classification: {labels[int(prediction.classification)]}")

        st.write("Processing complete.")


if __name__ == "__main__":
    gui()
