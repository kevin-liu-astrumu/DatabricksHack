import streamlit as st
from streamlit_float import *

from rag_modules.setup_llm import setup_llm
from rag_modules.setup_params import params
from streamlit_modules.app_utils import *
from streamlit_modules.streamlit_helper_functions import *


def setup_page_configurations():
    st.set_page_config(
        page_title="Home GPT",
        page_icon="🧙‍♂️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"About": "Home GPT"},
    )
    # ---- HIDE STREAMLIT STYLE ----
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def setup_header_area():
    st.title("Home GPT")


def setup_sidebar():
    st.sidebar.markdown("# Home GPT")
    st.sidebar.markdown("### Authorization")

    reset_chat_button = st.sidebar.button("Clear Chat↺", on_click=reset_chat)
    st.sidebar.write(
        "API keys are not stored, and their use is limited to your present browser session."
    )
    create_authorization_box()


def report_inquisition_display():
    uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")
    if uploaded_file is None:
        st.session_state.clear()
        st.info("Please upload your home inspection report")
        st.stop()
    llm = setup_llm()
    bot = setup_bot(uploaded_file, llm, params)
    resume_viewer, chat_box = st.columns([5, 5])
    with resume_viewer:
        display_pdf(uploaded_file)

    with chat_box:
        with st.container():
            chat_experience(bot)


def job_inquisition_display(key):

    chat_experience(key)
