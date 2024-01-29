import os
from typing import Any, Callable, List
import streamlit as st
from abstractions.component import Component
from engine.utils.file import FileInfo
from proto.file_upload_pb2 import UploadVideoResponse
from streamlit.runtime.uploaded_file_manager import UploadedFile
from engine.utils.serializers import json_celery_serializer
from controllers.tasks_controller import process_file_task

class UploadFileComponent(Component):
    def __init__(self):
        self.upload_response = None
        self.file_bytes = None
        self.file_format = None

    def __upload_file(
        self, send_file_handler: Callable[[FileInfo], any], uploaded_file: UploadedFile
    ):
        if uploaded_file:
            #TODO: Review serialization pipeline
            json_data = json_celery_serializer(uploaded_file)
            self.upload_response: UploadVideoResponse = process_file_task.delay(json_data)
            
            self.file_bytes = uploaded_file.getvalue()
            self.file_format = os.path.basename(uploaded_file.name).split(".")[-1]

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
