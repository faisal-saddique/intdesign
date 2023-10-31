import openai
import tiktoken
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def apply_persona_to_article(raw_article, person, original_articles, persona_prompt, container):
    tokens = num_tokens_from_string(raw_article)
    container.info(f"No. of Tokens in the raw article: {tokens}")
    if tokens > 1000:
        # Consider the first 7500 tokens of content
        container.info("Chunking to put it under the limit.")
        raw_article = raw_article[:700]

    tokens = num_tokens_from_string(original_articles)
    container.info(f"No. of Tokens in the original articles: {tokens}")
    if tokens > 2000:
        # Consider the first 7500 tokens of content
        container.info("Chunking to put it under the limit.")
        original_articles = original_articles[:1800]

    report = []
    for resp in openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": persona_prompt
            },
            {
                "role": "user",
                "content": f"Here are a few articles written by {person}:\n\n{original_articles}\n\n\nPlease now edit the following article as if it was written by {person}. Watch closely how he writes and then replicate his writing style so that you don't loose the essence of his persona. Here is the article to be refined:\n\n{raw_article}"
            }
        ],
        temperature=.7,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    ):
        if "content" in resp.choices[0].delta:
            report.append(resp.choices[0].delta.content)
            result = "".join(report)      
            container.markdown(result)

    return "".join(report)

def get_initial_persona_from_articles(person, content, container):
    tokens = num_tokens_from_string(content)
    container.info(f"No. of Tokens in the prompt: {tokens}")
    if tokens > 2000:
        # Consider the first 7500 tokens of content
        container.info("Chunking to put it under the limit.")
        content = content[:1500]
        
    SYSTEM_PROMPT = f"""Analyze {person}'s Articles and Craft His Persona in 200 Words!

Your task: Delve deep into {person}'s articles with a sharp focus! Examine his writing style closely, break down his sentences, and closely examine the structure of his content. Your objective is to create a persona that mirrors {person}'s unique writing style. Pay close attention to the core of his writing; your designated writer must flawlessly emulate {person}'s voice.

In less than 200 words, provide a thorough analysis and breakdown of {person}'s writing style. Leave no detail unturned, capturing every nuance that sets {person}'s writing apart. Remember, this isn't just about writing about {person}; you're composing a manual to help someone embody {person}'s writing style. Make this guide clear and to the point; it should serve as a step-by-step instruction for becoming {person} in his absence. Prepare to analyze, deconstruct, and replicate – the world craves more of {person}!

Begin your analysis with the sentence by asking the person to be {person}, then proceed to dissect and detail the rest of your analysis"""

    report = []
    for resp in openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Here are a few articles written by {person}:\n\n{content}"
            }
        ],
        temperature=.7,
        max_tokens=5000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    ):
        if "content" in resp.choices[0].delta:
            report.append(resp.choices[0].delta.content)
            result = "".join(report)      
            container.markdown(result)

    return "".join(report)

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