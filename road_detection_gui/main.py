import os
import streamlit as st
from dotenv import load_dotenv
from requests import Response
from engine.protocols.rest import Rest
from engine.utils.file import save_uploaded_file, video2image
from engine.protocols.protocol import Protocol
from proto.grpc_client import Grpc_Client


load_dotenv()
API_URL = os.environ.get("API_URL")
GRPC_HOST = os.environ.get("GRPC_HOST")
GRPC_PORT = os.environ.get("GRPC_PORT")

rest: Protocol = Rest(API_URL)
grpc: Protocol = Grpc_Client(GRPC_HOST, GRPC_PORT)


def main(protocol: Protocol):
    st.title("Road Detection CNN")
    uploaded_file = st.file_uploader(
        "Choose a image/video file", type=["mp4", "avi", "png", "jpg"]
    )
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension in ["mp4", "avi"]:
            st.video(uploaded_file)
            file_path = save_uploaded_file(uploaded_file)
            bytes_frames_generator = video2image(file_path, 5)
            for img_bytes, current_frame in bytes_frames_generator:
                response = protocol.send(img_bytes)
                st.write(current_frame, response)
                # response = rest.send(img_bytes)
                # print_response(response, current_frame)

        elif file_extension in ["png", "jpg"]:
            st.image(uploaded_file)
            response = protocol.send(uploaded_file.read())
            st.write(response)
        else:
            st.write("Wrong format")


if __name__ == "__main__":
    main(grpc)
