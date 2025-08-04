import streamlit as st
import json
from website.local_functions import *

st.set_page_config(
    page_title='Wrth Sgwrs',
    page_icon='🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    initial_sidebar_state="expanded"
)

if 'guest_is_logged_in' not in cookie_controller.getAll():
    cookie_controller.set('guest_is_logged_in', False)

pages = {
    'About': [st.Page('website/pages/about.py', title='About')],
    'Profile': [st.Page('website/pages/profile.py', title='Profile')],
    'Quick Translate': [st.Page('website/pages/quick_translate.py', title='Quick Translate')],
    'Dictionary': [st.Page('website/pages/dictionary.py', title='Dictionary')],
    'Grammar': [st.Page('website/pages/grammar.py', title='Grammar')],
    'Conversations': [st.Page('website/pages/chatbot.py', title='Conversations')],
    'Test Yourself': [st.Page('website/pages/test_yourself.py', title='Test Yourself!')],
    'Test': [st.Page('website/pages/test.py', title='Test')]

}

st.navigation(pages, position='hidden').run()
path = 'website/assets/'
st.logo(path+"Wordmark.png", icon_image=path+"Icon.png")

logged_in = (st.user.is_logged_in) or (cookie_controller.get('guest_is_logged_in'))

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
        st.page_link(pages['Test'][0], icon="🚧")
        logout_button('Log out')