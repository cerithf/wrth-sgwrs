import streamlit as st
import json
from website.local_functions import *

def check_user_attribute():
    if 'is_logged_in' in st.user:
        return st.user.is_logged_in
    else:
        return None

st.set_page_config(
    page_title='Wrth Sgwrs',
    page_icon='🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    initial_sidebar_state="collapsed"
)

if 'guest_is_logged_in' not in cc.getAll():
    cc.set('guest_is_logged_in', False)

pages = {
    'About': [st.Page('website/pages/about.py', title='About')],
    'Profile': [st.Page('website/pages/profile.py', title='Profile')],
    'Quick Translate': [st.Page('website/pages/quick_translate.py', title='Quick Translate')],
    'Dictionary': [st.Page('website/pages/dictionary.py', title='Dictionary')],
    'Grammar': [st.Page('website/pages/grammar.py', title='Grammar')],
    'Conversations': [st.Page('website/pages/chatbot.py', title='Conversations')],
    'Test Yourself': [st.Page('website/pages/test_yourself.py', title='Test Yourself!')],
    'Feedback': [st.Page('website/pages/feedback.py', title='Feedback')] # Used to test code, doesn't appear to user
}

st.navigation(pages, position='hidden').run()
path = 'website/assets/'
st.logo(path+"Wordmark.png", icon_image=path+"Icon.png")

user_logged_in = check_user_attribute()
logged_in = user_logged_in or cc.get('guest_is_logged_in')

if logged_in:
    with st.sidebar:
        st.title("Navigation 🧭")
        st.subheader('Home')
        st.page_link(pages['About'][0], icon="🏡")
        st.page_link(pages['Profile'][0], icon="👤")
        st.divider()
        st.subheader('Resources')
        st.page_link(pages['Quick Translate'][0], icon="🔀")
        st.page_link(pages['Dictionary'][0], icon="📖")
        st.page_link(pages['Grammar'][0], icon="📏")
        st.divider()
        st.subheader('Practice')
        st.page_link(pages['Conversations'][0], icon="🗣️")
        st.page_link(pages['Test Yourself'][0], icon="🧪")
        st.divider()
        st.page_link(pages['Feedback'][0], icon="📋")
        logout_button('Log out')