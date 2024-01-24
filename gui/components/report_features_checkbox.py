from typing import List
import streamlit as st

from abstractions.component import Component


class ReportFeatureCheckbox:
    def __init__(self, name, checked=False):
        self.name = name
        self.checked = checked
        self.enable = False


class ReportFeatureCheckboxComponent(Component):
    def __init__(self):
        self.report_features = []

    def __toggle_feature(self, report_feature: ReportFeatureCheckbox):
        report_feature.checked = not report_feature.checked
        
   
    def render(self, report_features: List[ReportFeatureCheckbox]):
        self.report_features = report_features
        for report_feature in self.report_features:
            st.checkbox(
                report_feature.name,
                report_feature.checked,
                args=(report_feature,),
                on_change=self.__toggle_feature,
                disabled=not report_feature.enable
            )

        return self.report_features
