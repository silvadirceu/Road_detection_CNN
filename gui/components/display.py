from typing import List
import streamlit as st
from abstractions.component import Component

class DisplayComponent(Component):
    def __init__(self):
        pass

    def render(self, file_bytes, file_format: str, start_time=0):
        if file_format in ["mp4", "avi"]:
            st.video(file_bytes)
        else:
            st.image(file_bytes)