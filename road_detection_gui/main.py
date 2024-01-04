import base64
import json
import os
from dotenv import load_dotenv
import streamlit as st
import requests

from utils.file_utils import bytes_to_base64_utf8encoded


load_dotenv()
API_URL = os.environ.get("API_URL")


st.title("Road Detection CNN")
uploaded_file = st.file_uploader(
    "Choose a image/video file", type=["mp4", "avi", "png", "jpg"]
)
if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension in ["mp4", "avi"]:
        st.video(uploaded_file)
    elif file_extension in ["png", "jpg"]:
        st.image(uploaded_file)
    else:
        st.write("Wrong format")
    
    file_base64 = bytes_to_base64_utf8encoded(uploaded_file.getvalue())
    
    response = requests.post(API_URL+"predict", data={"file_base64": file_base64})
    if response.status_code == 200:
        st.write(response.content)
    else:
        st.write(f"Failed to send file. Status code: {response.status_code}")
