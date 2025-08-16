import streamlit as st
import datetime as dt
from website.local_functions import *
from openai import OpenAI
import pandas as pd

# important guide: https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps 

# Setting up session state ----------------------------------------------------

page_setup()
ss = st.session_state
check_access()

initial_state = {
    'chosen_question': None,
    'openai_model': 'gpt-4o',
    'messages': [],
    'display_messages': []
}

for k,v in initial_state.items():
    if k not in ss:
        ss[k] = v

# Setting OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Display -------------------------------------------------------------------

l,r = st.columns([0.9,0.1])
with l:
    st.title('Wrth Sgwrs')
with r:
    if st.button('Clear'):
        ss.messages = []
        ss.chosen_question = None

prompt = st.chat_input("Type here...")

def return_right_thing(return_question=False):
    ''' If a user has submitted a prompt, the prompt is input to the AI. If they've chosen a random question to start, either a contextual prompt containing the question is returned or just the question itself, depending on the value of return_question'''
    
    if prompt:
        return prompt
    elif ss.chosen_question:

        if return_question:
            return ss.chosen_question[0]
        else:

            if ss.chosen_question[1]['en'] == 'Numbers':
                full_prompt = f"""I am a Welsh learner and I would like to practise speaking Welsh to you.
                Let's have a conversation about the topic of {ss.chosen_question[1]['en']}.
                Please start by asking me the following question, do not return any other text.
                {ss.chosen_question[0]}
                """
            else:
                full_prompt = f"""I am a Welsh learner and I would like to practise speaking Welsh to you.
                Let's have a conversation about the topic of {ss.chosen_question[1]['en']}.
                I'll begin by asking you a question — please respond in Welsh as if you were a Welsh person, not an AI language model. 
                At the end of your first response, ask me the same question in return. In your SECOND, ask another question on the same topic to keep the conversation going, don't ask if there's something else I want to talk about. Do not mention anything about continuing the conversation in your first response.
                {ss.chosen_question[0]}"""

            if "zodiac" in ss.chosen_question[0]:
                zodiac_table = pd.read_csv( 'website/data/zodiac.csv')
                full_prompt += f"\n  In your answer, provide a table using this as the source: {zodiac_table}"""

            return full_prompt
            
    else:
        return "error"

# Ensures user doesn't see the full prompt instead of just their random question on the app rerun
if ss.chosen_question and len(ss.messages) > 1:
    if ss.chosen_question[1]['en'] == 'Numbers':
        ss.messages[0] = {"role": "user", "content": "Gofynna gwestiwn i mi am rifau. (Ask me a question about numbers.)"}
    else:
        ss.messages[0] = {"role": "user", "content": ss.chosen_question[0]}

# Display chat messages from history on app rerun
for message in ss.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt or (ss.chosen_question and len(ss.messages) < 2):
    with st.chat_message("user"):
        st.markdown(return_right_thing(True))
    # Add user message to chat history
    ss.messages.append({"timestamp": dt.datetime.now().strftime('%d-%m-%Y %X'), "role": "user", "content": return_right_thing()})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=ss['openai_model'],
            messages=[{'role': m['role'], 'content': m['content']} for m in ss.messages],
            stream=True
        )
        response = st.write_stream(stream)
        
    # Add assistant response to chat history
    ss.messages.append({"timestamp": dt.datetime.now().strftime('%d-%m-%Y %X'), "role": "assistant", "content": response})
else:
    if len(ss.messages) < 1:
        # Runs before the user has written entered text into the chatbox
        with st.chat_message("assistant"):
            stream_text('''👉 Write something in the chatbox below! _Ysgrifenna rywbeth yn y blwch isod!_''')

if len(ss.messages) > 0:
    # Saves conversation
    saved_conversation = save_conversation(ss.messages)
    st.download_button('Save conversation', data=saved_conversation[0], file_name=saved_conversation[1])