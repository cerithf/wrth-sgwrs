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
        df = pd.read_csv('website/data/eurfa_dictionary/simple_dictionary.csv', index_col=0)
        abbs = pd.read_csv('website/data/eurfa_dictionary/abbreviations.csv').to_dict('records')
        abbs = {item['Abbreviation']:item['Meaning (English)'] for item in abbs}
        all_words = [tuple(entry.values()) for entry in df.to_dict('records')]
        divisions = sorted(set([entry[0] for entry in df['sort']]))
        for char in divisions:
            letter = get_key_from_value(char, letter_sort)
            left,right = st.columns([0.1,0.9])
            with left:
                st.write(['## \#' if letter == '#' else f'## {letter}'][0]) # type: ignore
            with right:
                with st.expander(letter):
                    words = [word for word in all_words if word[3][0] == char]
                    one,two,three,four = st.columns(4)
                    with one:
                        for word in words[::4]:
                            display_word(word, abbreviations=abbs)
                    with two:
                        for word in words[1::4]:
                            display_word(word, abbreviations=abbs)
                    with three:
                        for word in words[2::4]:
                            display_word(word, abbreviations=abbs)
                    with four:
                        for word in words[3::4]:
                            display_word(word, abbreviations=abbs)
            st.divider()