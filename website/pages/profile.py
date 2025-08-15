import streamlit as st
from website.local_functions import *

if is_logged_in():
    guest_username = str(st.session_state["sub"]).replace('guest_','')
    st.title(f'Hey, {guest_username.title()}! 👋')
else:
    st.title(f'Hey there! 👋')

# list of indices of the topics already learnt by user
learnt_topics = load_user_topics()

# list of data about topics themselves
topics = list(get_data('conversation_topics',2,'list'))# type: ignore

# setting session state to reflect topics already learnt in previous session(s)
ss = st.session_state

if "initialized" not in ss:
    ss["initialized"] = True
    for topic in topics:
        ss[f'checkbox_{topic['index']}'] = topic['index'] in learnt_topics # type: ignore

checkboxes = {int(k.split('_')[1]):v for k,v in ss.items() if k[:8] == 'checkbox'} # type: ignore
checked_boxes = [k for k,v in checkboxes.items() if v == True]
score = len(checked_boxes)
total_topics = len(topics)

with st.container(border=True):
    st.html(f'''
<html>
    <style>
        .text {{
            font-size: 20px;
        }}
        .score {{
            font-size: 40px;
            font-weight: bold;
        }}
    </style>
    <span style="font-size: 18px;">Number of topics learnt:</span>
    <br>
    <span class="score">{score}</span>
    <span class="text">/ {total_topics}</span>
</html>
''')
    st.progress(score/total_topics)
    emojis = [topic['emoji'] for topic in topics if topic['index'] in checked_boxes] #type: ignore
    st.write('\t'.join(emojis))


def topic_container(topic):
    with st.container(border=True):
        br = ['<br>' if len(topic['en']) > 14 else '<span> | </span>'][0]
        st.html(f'''
        <span style="font-size: 25px;">{topic['emoji']} </span>
        <span style="font-size: 20px; font-weight: bold;"> {topic['en']}</span>
        {br}
        <span style="font-size: 15px; font-style: italic; color: gray; text-indent: 123em;">{topic['cy']}</span>
''')
        l,r = st.columns(2)
        with l:
            result = st.button('Practice', icon='🗣️', key=f'practice_{topic['index']}')
            if result: button_press(result, topic, True)
        with r:
            check = st.checkbox('Learnt?', key=f'checkbox_{topic['index']}', value= topic['index'] in checked_boxes)

st.subheader('Topics')
left,right = st.columns(2)
with left:
    for topic in topics[::2]: topic_container(topic)
with right:
    for topic in topics[1::2]: topic_container(topic)

if score == total_topics:
    st.balloons()
    
st.divider()
logout_button('Log out')

if len(checked_boxes) > 0:
    checked_boxes = sorted(checked_boxes)
    save_user_topics(checked_boxes)
