import streamlit as st

padding_css = """
    <style>
        .main > div {
            padding-top: 0rem;
        }
    </style>
"""

upload_file_css = """
        <style>
            section[data-testid="stFileUploadDropzone"]{
                text-align: center;
            }
            button[data-testid="baseButton-secondary"]{
                text-align: center;
                width: 100%;
            }
        </style>"""

center_h1 = """"
        <style>
            h1 {
                text-align: center;
            }
        </style>
        """

def apply_css_component():
    st.markdown(padding_css, unsafe_allow_html=True)
    st.markdown(upload_file_css, unsafe_allow_html=True)
