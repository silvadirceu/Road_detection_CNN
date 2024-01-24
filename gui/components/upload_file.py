from typing import Callable
import streamlit as st
from abstractions.component import Component
from engine.utils.file import FileInfo


class UploadFileComponent(Component):
    def __init__(self):
        self.upload_response = None
        self.video_bytes = None

    def __upload_file(
        self, send_file_handler: Callable[[FileInfo], any], uploaded_file
    ):
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            file_info = FileInfo(uploaded_file.name, bytes_data)
            self.video_bytes = uploaded_file.read()
            self.upload_response = send_file_handler(file_info)

    def render(self, send_file_handler: Callable[[FileInfo], any]):
        uploaded_file = st.file_uploader(
            "Choose a image/video file",
            type=["mp4", "avi", "png", "jpg"],
            label_visibility="hidden",
        )
        st.button(
            "Send",
            use_container_width=True,
            type="primary",
            on_click=self.__upload_file,
            args=(send_file_handler, uploaded_file),
        )

        return self.upload_response, self.video_bytes
