from components.report_features_checkbox import ReportFeatureCheckboxComponent
from components.upload_file import UploadFileComponent
import streamlit as st

report_features_component = ReportFeatureCheckboxComponent()
upload_file_component = UploadFileComponent()

report_features = report_features_component.render
upload_file = upload_file_component.render