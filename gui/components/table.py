from typing import List
import streamlit as st
import pandas as pd
from abstractions.component import Component


class TableComponent(Component):
    def __init__(self):
        self.columns = []
        self.rows = [[]]

    @st.cache_data
    @staticmethod
    def __data_frame(columns: List[str], rows: List[List[str]]):
        return pd.DataFrame(
            rows,
            columns=columns,
    )

    def render(self, columns: List[str], rows: List[List[str]]):
        self.rows = rows
        self.columns = columns
        st.dataframe(TableComponent.__data_frame(self.columns, self.rows), use_container_width=True)
