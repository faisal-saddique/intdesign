import openai
import tiktoken
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_content_and_get_gpt_response(content, container):
    tokens = num_tokens_from_string(content)
    container.info(f"No. of Tokens in the prompt: {tokens}")
    if tokens > 600:
        # Consider the first 7500 tokens of content
        container.info("Chunking to put it under the limit.")
        content = content[:400]
        
    SYSTEM_PROMPT = """As a blog writer for Chainflip, your task is to create an immediate professional blog about Chainflip from the given list of points. Chainflip is a revolutionary cryptocurrency exchange platform. It offers low slippage swaps, a native cross-chain swap protocol, and operates in a decentralized manner. Chainflip also has a JIT AMM to reduce slippage and a native $FLIP token for ecosystem security and validator rewards, making it a game-changer in decentralized exchanges."""

    report = []
    for resp in openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal:chainflip-model:8EaOmtaa",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    ):
        # join method to concatenate the elements of the list 
        # into a single string, 
        # then strip out any empty strings
        if "content" in resp.choices[0].delta:
            # container.text += resp.choices[0].delta.content
            # container.markdown(resp.choices[0].delta.content)

            report.append(resp.choices[0].delta.content)
            result = "".join(report)
            # result = result.replace("\n", "")       
            container.markdown(result)

    return "".join(report)
    
def num_tokens_from_string(content: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(content))
    return num_tokens

def generate_article(content, container):
    return process_content_and_get_gpt_response(content=content,container=container)