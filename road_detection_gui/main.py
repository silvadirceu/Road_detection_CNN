import os
import streamlit as st
from dotenv import load_dotenv
from requests import Response
from engine.protocols.rest import Rest
from engine.utils.file import save_uploaded_file, video2image
from engine.protocols.protocol import Protocol


load_dotenv()
API_URL = os.environ.get("API_URL")
rest: Protocol = Rest(API_URL)


def print_response(response: Response, frame=1):
    if response.status_code == 200:
        st.write(f"{frame}: {response.content}")
    else:
        st.write(f"Failed to send file. Status code: {response.status_code}")


def main():
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
                response = rest.send(img_bytes)
                print_response(response, current_frame)

        elif file_extension in ["png", "jpg"]:
            st.image(uploaded_file)
            response = rest.send(uploaded_file.read())
            print_response(response)
        else:
            st.write("Wrong format")


if __name__ == "__main__":
    main()
