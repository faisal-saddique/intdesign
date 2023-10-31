from dotenv import load_dotenv
import streamlit as st
import datetime
from utilities.utils import (
    get_initial_persona_from_articles,
    apply_persona_to_article
)

# Set Streamlit page configuration
st.set_page_config(
    page_title='PersonaForge',
    page_icon='🧙‍♂️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Main title
st.title("PersonaForge - Craft Your Writing Style 🧙‍♂️📖")

# Load environment variables from .env file
load_dotenv()

with st.sidebar:
    st.subheader("About")
    st.markdown("Welcome to PersonaForge, your gateway to crafting a distinctive writing style. Whether you're an aspiring author or a seasoned wordsmith, our platform empowers you to emulate the essence of your favorite writers. Unleash your creativity, harness their genius, and embark on a literary journey like no other. Join us as we help you breathe life into your words and turn your writing dreams into reality. Explore the magic of language and discover the art of storytelling at PersonaForge.")

# Input fields and labels
person_name = st.text_input(
    "Enter the name of the person you want to emulate:")
articles = st.text_area(
    "Enter the articles written by them (max 1500 words):", height=400)
raw_article = st.text_area(
    f"Enter the raw article to convert to the subject's style:", height=400)

# Error handling and button label
if st.button("Generate", use_container_width=True):
    if person_name and articles and raw_article:
        if "created_persona" not in st.session_state:
            # Generate initial persona
            with st.expander("Creating Persona"):
                res_box = st.empty()
                system_prompt_for_generation_step = get_initial_persona_from_articles(
                    person_name, articles, res_box)
                st.session_state["created_persona"] = system_prompt_for_generation_step
        else:
            system_prompt_for_generation_step = st.session_state["created_persona"]
        # Generate refined article
        st.subheader("Refined Article")
        final_res_box = st.empty()
        final_article = apply_persona_to_article(raw_article=raw_article, person=person_name,
                                                    original_articles=articles, persona_prompt=system_prompt_for_generation_step,
                                                    container=final_res_box)
        if final_article:
            # Download button
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            sanitized_datetime = current_datetime.replace(":", "-")
            file_name = f"{person_name}_styled_article_{sanitized_datetime}.md"
            st.download_button(label="Download Refined Article", data=final_article, file_name=file_name, mime="text/markdown",
                                use_container_width=True)
    else:
        st.warning(
            "Please fill in all required fields: Person name, articles, and raw article.")