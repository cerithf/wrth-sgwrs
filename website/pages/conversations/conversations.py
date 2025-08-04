import streamlit as st
from deep_translator import GoogleTranslator
import json
import datetime as dt
from website.local_functions import *
from openai import OpenAI

# important guide: https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps 

st.title('Wrth Sgwrs')

# Setting OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Setting a default model
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-4o'

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state['openai_model'],
            messages=[{'role': m['role'], 'content': m['content']} for m in st.session_state.messages],
            stream=True
        )
        response = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Saves conversationges)
    saved_conversation = save_conversation(st.session_state.messages)
    st.download_button('Save conversation', data=saved_conversation[0], file_name=saved_conversation[1])

else:
    # Runs before the user has written entered text into the chatbox
    st.write('''👉 Write something in the chatbox below! _Ysgrifenna rywbeth yn y blwch isod!_''')
