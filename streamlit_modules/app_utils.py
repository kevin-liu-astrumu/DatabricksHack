import base64
import gc
from tempfile import NamedTemporaryFile

import streamlit as st
from streamlit_float import *

from rag_modules.rag import RAG


def display_pdf(file):
    # Opening file from file path
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    # Embedding PDF in HTML
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="100%" type="application/pdf"
                        style="height:100vh; width:100%"
                    >
                    </iframe>"""
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()


def chat_content():
    st.session_state["contents"].append(st.session_state.content)


def setup_bot(uploaded_file, llm, params):
    with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
        f.write(uploaded_file.getbuffer())
        bot = RAG(pdf_file=f.name, llm=llm, params=params)
    return bot


def chat_experience(bot, key="resume"):
    if "messages" not in st.session_state:
        reset_chat()
        border = False
    else:
        border = True
    with st.container(border=border):
        with st.container():
            button_b_pos = "0rem"
            button_css = float_css_helper(
                width="2.2rem", bottom=button_b_pos, transition=2
            )
            float_parent(css=button_css)
        if prompt := st.chat_input("Ask me question", key=key):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            full_response = bot.respond_query(prompt)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
            with st.chat_message("assistant"):
                st.markdown(full_response)
                # Add assistant response to chat history
        grouped_pairs = list(
            zip(st.session_state.messages[0::2], st.session_state.messages[1::2])
        )[0:-1][::-1]
        for user_message, assistant_message in grouped_pairs:
            with st.chat_message("user"):
                st.markdown(user_message["content"])
            with st.chat_message("assistant"):
                st.markdown(assistant_message["content"])
