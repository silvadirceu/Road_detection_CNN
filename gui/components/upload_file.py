from typing import Any, Callable, List
import streamlit as st
from abstractions.component import Component
from engine.utils.file import FileInfo
from proto.requests_pb2 import VideoPredictResponse
from streamlit.runtime.uploaded_file_manager import UploadedFile


class UploadFileComponent(Component):
    def __init__(self):
        self.upload_response = None
        self.file_bytes = None
        self.file_format = None

    def __upload_file(
        self, send_file_handler: Callable[[FileInfo], any], uploaded_file: UploadedFile
    ):
        if uploaded_file:
            self.file_bytes: bytes = uploaded_file.getvalue()
            file_info = FileInfo(uploaded_file.name, self.file_bytes)
            self.upload_response: VideoPredictResponse = send_file_handler(file_info)
            self.file_format = file_info.format

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

        return self.upload_response, self.file_bytes, self.file_format
