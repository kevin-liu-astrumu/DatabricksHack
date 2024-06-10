import os

import requests
import streamlit as st


class ApiKeyHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiKeyHandler, cls).__new__(cls)
        return cls._instance

    def set_api_key_environment_variable(self, openai_api_key):
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key

    def validate_key(self, openai_api_key):
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {openai_api_key}"},
        )
        if response.status_code == 200:
            return True
        else:
            return False


### only a helper function to create_authorization_box.
def authorization_status_box(isvalid):
    """Creates a green or red box depending on the value of the `isvalid` variable."""
    if isvalid:
        color = "green"
        text = "Validated"
    else:
        color = "darkred"
        text = "Not Validated"
    style = f"""
    .{color}-box {{
        background-color: {color};
        border: 1px solid black;
        padding: 10px;
    }}
    """
    st.sidebar.markdown(
        f"""
    <style>{style}</style>
    <div class="{color}-box">{text}</div>
    """,
        unsafe_allow_html=True,
    )


def create_authorization_box():
    authorizer = ApiKeyHandler()
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = None

    st.sidebar.markdown(
        """
        Please enter your OpenAI API key
        -[ need help?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
        """,
        unsafe_allow_html=True,
    )
    input_api_key = st.sidebar.text_input(
        "",
        type="password",
        label_visibility="collapsed",
    )

    if input_api_key:
        st.session_state.api_key = input_api_key
        st.session_state.api_key_valid = authorizer.validate_key(input_api_key)
        if st.session_state.api_key_valid:
            authorizer.set_api_key_environment_variable(st.session_state.api_key)
        authorization_status_box(st.session_state.api_key_valid)
