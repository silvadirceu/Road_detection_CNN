import streamlit as st

from abstractions.component import Component


class StylesComponent(Component):        
    __padding_css = """
            <style>
                .main > div {
                    padding-top: 0rem;
                }
            </style>"""

    __upload_file_css = """
            <style>
                section[data-testid="stFileUploadDropzone"]{
                    text-align: center;
                }
                button[data-testid="baseButton-secondary"]{
                    text-align: center;
                    width: 100%;
                }
            </style>"""

    __padding_top_sidebar_css = """
            <style>
                div[data-testid="stSidebarUserContent"]{
                    padding-top: 1rem;
                }
            </style>"""
    
    __drag_and_drop_background_color = """
            <style>
                section[data-testid="stFileUploadDropzone"]{
                    background-color: rgb(186, 247, 216);
                    border: solid;
                    border-color: rgb(99, 185, 128);
                }
            </style>"""
    
    
    def render(self):
        st.markdown(self.__padding_css, unsafe_allow_html=True)
        st.markdown(self.__upload_file_css, unsafe_allow_html=True)
        st.markdown(self.__padding_top_sidebar_css, unsafe_allow_html=True)
        st.markdown(self.__drag_and_drop_background_color, unsafe_allow_html=True)


