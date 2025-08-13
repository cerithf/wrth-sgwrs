import streamlit as st
from website.local_functions import *
import json
import pandas as pd

ss = st.session_state
page_setup()

search,browse = st.tabs(['Search','Browse'])

with open('website/data/eurfa_dictionary/letter_sort.json') as file:
    letter_sort = json.load(file)

with search:
    with st.form("search_form"):
        search_term = st.text_input(label='Search for a word here:')
        submit = st.form_submit_button()
        if submit:
            try:
                get_word_details(search_term)
            except UnboundLocalError:
                pass
with browse:
    if st.button('Load dictionary'):
        display_dictionary()