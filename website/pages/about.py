import streamlit as st
import json
from website.local_functions import *

deinitialize_profile_page()

ss = st.session_state
if 'chosen_topic' not in ss: ss.chosen_topic = None

user_logged_in = check_user_attribute()

logged_in = user_logged_in or (cc.get('guest_is_logged_in'))
left, right = st.columns([0.65,0.35])

with right:
    control_options = ['English 🇬🇧', 'Cymraeg 🏴󠁧󠁢󠁷󠁬󠁳󠁿']
    mode = st.segmented_control(label='Language / Iaith',options=control_options,default=control_options[0])

with open('website/data/about_page_text.json') as file:
    page_text = json.load(file)

if mode==control_options[0]:
    page_text = page_text['en']
else:
    page_text = page_text['cy']

st.markdown(page_text['body'])

if not logged_in:
    guest_login_form()
else:
    logout_button('Log out')

        
