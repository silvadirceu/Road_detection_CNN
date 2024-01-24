import os
import folium
import streamlit as st
from dotenv import load_dotenv
from components.css import apply_css_component
from components.report_features_checkbox import ReportFeatureCheckbox
from controllers.send_file_controller import SendFileController
from engine.protocols.rest import Rest
from abstractions.http_handler import HttpHandler
from proto.grpc_client import Grpc_Client
import pandas as pd
from streamlit_folium import st_folium
from components import components as st_components


load_dotenv()
API_URL = os.environ.get("API_URL")
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")
GOOGLE_MAPS_API_KEY = "https://maps.googleapis.com/maps/api/js?key=&callback=initMap"

rest: HttpHandler = Rest(API_URL)
grpc_cv_client = Grpc_Client(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
controller = SendFileController(grpc_cv_client)


dropdown_css = """
        <style>
            section[data-testid="stFileUploadDropzone"]{
                text-align: center;
            }
            button[data-testid="baseButton-secondary"]{
                text-align: center;
                width: 100%;
            }
        </style>"""


def main():
    st.set_page_config(layout="wide")
    apply_css_component()

    st.title("Road Condition")

    with st.sidebar:
        st.header("Load Data")
        upload_response, video_bytes = st_components.upload_file(controller.send)
        st.write(upload_response)

        st.divider()

        st.header("Data Analysis")
        report_features_list = st_components.report_features(
            [ReportFeatureCheckbox(f"Potholes"), ReportFeatureCheckbox(f"Dirty")]
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        m = folium.Map(location=[39.9, -75.1], zoom_start=16)
        st_data = st_folium(m, use_container_width=True, height=600)

    with col2:
        with st.container():
            df = pd.DataFrame(
                [[None for i in range(6)] for i in range(10)],
                columns=[
                    "Street",
                    "Clean",
                    "Pothole",
                    "Dirty",
                    "Latitude",
                    "Longitude",
                ],
            )
            st.dataframe(df, use_container_width=True)

        with st.container():
            if upload_response:
                st.video(video_bytes)


if __name__ == "__main__":
    main()
