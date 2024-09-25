import streamlit as st
import random, time
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os


# Streamed response emulator
def response_generator(prompt):
    token = os.getenv("HF_API_TOKEN")
    client = InferenceClient(
        "microsoft/Phi-3-mini-4k-instruct",
        token=token,
    )

    response = "".join(message.choices[0].delta.content for message in client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        stream=True,
    ))
    return response


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    response = response_generator(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})