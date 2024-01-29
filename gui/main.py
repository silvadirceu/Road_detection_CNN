import folium
import streamlit as st
from streamlit_folium import st_folium
from services.celeryconfig import celery_app
from components.report_features_checkbox import ReportFeatureCheckbox
from components import components as st_components
from services.services import geolocator, send_file_controller
from PIL import Image

from services.settings import *

potholes_locations = [
    [-7.56074, -35.01794],
    [-7.56072, -35.01800],
    [-7.56068, -35.01807],
    [-7.56064, -35.01814],
]
dirty_locations = [[-7.56054, -35.01828], [-7.56050, -35.01837], [-7.56044, -35.01846]]
all_locations = potholes_locations + dirty_locations

def main():
    st.set_page_config(
        page_title="Road Condition",
        page_icon="",
        layout="wide",
    )
    st_components.styles()
    st.title("Road Condition")
    with st.sidebar:
        logo = Image.open("assets/logo.png")
        st.image(logo)
        st.divider()

        st.header("Load Data")
        upload_response, file_bytes, file_format = st_components.upload_file(
            send_file_controller.send
        )

        st.header("Data Analysis")
        report_features = st_components.report_features(
            [ReportFeatureCheckbox(f"Potholes"), ReportFeatureCheckbox(f"Dirty")],
            bool(upload_response),
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        if not report_features[0].checked and not report_features[1].checked:
            map = folium.Map(location=potholes_locations[0], zoom_start=18, min_zoom=15)
            st_data = st_folium(map, use_container_width=True, height=600)
        elif report_features[0].checked and not report_features[1].checked:
            map = folium.Map(location=potholes_locations[0], zoom_start=18, min_zoom=15)
            for i in range(4):
                marker = folium.CircleMarker(location=potholes_locations[i])
                marker.add_to(map)
            st_data = st_folium(map, use_container_width=True, height=600)
        elif not report_features[0].checked and report_features[1].checked:
            map = folium.Map(location=dirty_locations[0], zoom_start=18, min_zoom=15)
            for i in range(3):
                marker = folium.CircleMarker(location=dirty_locations[i])
                marker.add_to(map)
            marker.add_to(map)
            st_data = st_folium(map, use_container_width=True, height=600)
        else:
            map = folium.Map(
                location=all_locations[int(len(all_locations) / 2)],
                zoom_start=18,
                min_zoom=15,
            )
            for i in range(7):
                marker = folium.CircleMarker(location=all_locations[i])
                marker.add_to(map)
            marker.add_to(map)
            st_data = st_folium(map, use_container_width=True, height=600)

    with col2:
        address = geolocator.adress(-7.56074, -35.01794)
        street = address.split(",")[0] or None
        with st.container():
            st_components.table(
                ["Street", "Pothole", "Dirty", "Latitude", "Longitude"],
                [
                    [
                        street,
                        i < 4,
                        i >= 4,
                        all_locations[i][0],
                        all_locations[i][1],
                    ]
                    for i in range(0, 7)
                ],
            )
        with st.container():
            if upload_response:
                st_components.display(file_bytes, file_format)


if __name__ == "__main__":
    main()
