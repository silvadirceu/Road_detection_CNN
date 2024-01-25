from typing import List
import streamlit as st
from abstractions.component import Component


class ReportFeatureCheckbox:
    def __init__(self, name, checked=False):
        self.name = name
        self.checked = checked

class ReportFeatureCheckboxComponent(Component):
    def __init__(self):
        self.report_features = []

    def render(self, report_features: List[ReportFeatureCheckbox], enabled):
        self.enabled = enabled
        self.report_features = report_features
        for report_feature in self.report_features:
            checked = st.checkbox(
                report_feature.name,
                report_feature.checked,
                disabled=not self.enabled,
            )
            report_feature.checked = checked
        return self.report_features
