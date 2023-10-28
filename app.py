from dotenv import load_dotenv
import streamlit as st
import datetime

from langchain.callbacks.base import BaseCallbackHandler
from utilities.utils import (
    generate_article
)

st.set_page_config(
    page_title='FlipChain Blog Writer',
    page_icon='🪙',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("FlipChain Blog Writer 🪙")


# Load environment variables from .env file
load_dotenv()

st.info("Please adhere to the specified format for prompt input when using the model for fine-tuning. Present your instructions as a list, with each point on a new line and commencing with a hyphen '-' character. After composing your prompt in this manner, proceed by pressing the 'Generate Article' button to initiate the task.")

input = st.text_area("Please enter the prompt here:", height= 400)

if st.button("Generate", use_container_width=True):
    if input:
        res_box = st.empty()
        result = generate_article(input,res_box)

        if result:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            sanitized_datetime = current_datetime.replace(":", "-")
            file_name = f"flipchain_blog_{sanitized_datetime}.md"
            st.download_button(label="Download Article", data=result, file_name=file_name, mime="text/markdown",use_container_width=True)
