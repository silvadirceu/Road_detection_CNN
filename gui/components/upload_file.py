import os
from typing import Any, Callable, List
import streamlit as st
from abstractions.component import Component
from proto.file_upload_pb2 import UploadVideoResponse
from streamlit.runtime.uploaded_file_manager import UploadedFile
from controllers.tasks_controller import process_task
from engine.utils.schemas import FileInfo


class UploadFileComponent(Component):
    def __init__(self):
        self.upload_response = None
        self.file_bytes = None
        self.file_format = None

    def __upload_file(
        self, send_file_handler: Callable[[FileInfo], any], uploaded_file: UploadedFile
    ):
        if uploaded_file:
            file_info = FileInfo(
                name=uploaded_file.name,
                chunk=uploaded_file.getvalue(),
                path="",
            )
            
            #cant serialize method send_file_handler()
            self.upload_response: UploadVideoResponse = (
                process_task.delay(file_info.to_dict())
            )

            self.file_bytes = file_info.chunk
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
