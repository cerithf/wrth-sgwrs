import streamlit as st
import json
from openai import OpenAI
from website.local_functions import *


ss = st.session_state
page_setup()
check_access()
if "messages" not in ss:
    ss.messages = []
    ss.chosen_topic = None

st.header('Test Yourself!')

st.write('Choose a topic!')

topics = list(get_data('conversation_topics',2,'list'))# type: ignore
columns = st.columns(4)

for i in range(len(columns)):
    with columns[i]:
        for topic in topics[i::len(columns)]:
            if st.button(topic['en'], key=f'topic_{topic['index']}', icon=topic['emoji'], use_container_width=True): #type: ignore
                ss.chosen_topic = topic

if ss.chosen_topic:
    st.write('_Here\'s a paragraph in English based on the topic you chose. Try and write the Welsh translation in the box below and see how close you get! Feel free to only tackle part of the paragraph for now, you can always come back to it later._')
    st.divider()

    with open('website/data/paragraphs.json') as file:
        file = json.load(file)
        paragraph = [paragraph for paragraph in file if paragraph['topic'] == ss.chosen_topic['en']][0] #type: ignore

    st.write(paragraph['en'])

    with st.form("form"):
        submitted_text = st.text_area("Write")
        a,b,c = st.columns(3)
        with a: submit_1 = st.form_submit_button('Submit (Exemplar+English)', use_container_width=True)
        with b: submit_2 = st.form_submit_button('Submit (English)',  use_container_width=True)
        with c: submit_3 = st.form_submit_button('Submit (Translation Only)',  use_container_width=True)


    def modify_prompt(prompt_type, paragraph=paragraph, translation=submitted_text) -> str:
        if prompt_type=="exemplar_and_english":
            return f'''
        I am a user who is learning Welsh. The following is a paragraph written in English that I have been asked to translate into Welsh. Please compare the two and tell me where I have made any mistakes or if there are any improvements that can be made. Use the paragraph under the heading "exemplar" to guide your feedback. If I make a mistake regarding mutation, just refer to it as "mutation" rather than "soft mutation", "aspirate mutation", or "nasal mutation", as you often incorrectly label what kind of mutation is present. My translation may only cover part of the original paragraph: this is okay, be encouraging (no need to ask me to do the whole thing). Also remember that I cannot see the exemplar, so do not tell me to refer to it.

        Original English paragraph:
        {paragraph['en']}

        My translation:
        {translation}
        
        Exemplar:
        {paragraph['cy']}
        '''
        elif prompt_type=="english_provided":
            return f'''
        I am a Welsh learner. I have been asked to translate a paragraph from English into Welsh. I'll share the original English paragraph and then the Welsh translation. Please tell me how I can improve my translation.

        Original English paragraph:
        {paragraph['en']}

        My translation:
        {translation}
        '''
        elif prompt_type=="translation_only":
            return f'''
        I am a Welsh learner. I have been asked to translate a paragraph from English into Welsh. Please give me feedback on my translation.

        My translation:
        {translation}
        '''
        else:
            return f'There has been an error.'
        
    # -----

    # Setting OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

    # Setting a default model
    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-4.1'

    if "test_messages" not in st.session_state:
        ss.test_messages = []
    else:
        try:
            messages_to_show = [m for m in ss.test_messages if m['role'] == 'assistant'][-1]
            for message in messages_to_show:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        except:
            pass

    if (submit_1 or submit_2 or submit_3):

        if submit_1:
            prompt_type = "exemplar_and_english"
        elif submit_2:
            prompt_type = "english_provided"
        elif submit_3:
            prompt_type = "translation_only"
        else:
            prompt_type = "error"
    

        # Add user message to chat history
        st.session_state.test_messages.append({"role": "user", "content": modify_prompt(prompt_type)})

        # Display assistant response in chat message container
        with st.chat_message(name="assistant",avatar="👨🏼‍🏫"):
            stream = client.chat.completions.create(
                model=st.session_state['openai_model'],
                messages=[{'role': m['role'], 'content': m['content']} for m in st.session_state.test_messages],
                stream=True
            )
            response = st.write_stream(stream)
        # Add assistant response to chat history
        st.session_state.test_messages.append({"role": "assistant", "content": response})

        if ss.sub == 'guest_cerith':
            save_ai_response(submitted_text,paragraph['topic'],response, model=st.session_state['openai_model'], prompt=prompt_type)