# IMPORTS AND GLOBAL VARIABLES

import json
import datetime as dt
import os
import streamlit as st
import pandas as pd
from random import choice
import time
from streamlit_cookies_controller import CookieController
from streamlit_gsheets import GSheetsConnection

db_connection = st.connection("gsheets", type=GSheetsConnection)
user_db = db_connection.read(worksheet="Users", usecols=[1])
db_users = user_db[user_db.columns[0]].to_list()

st.session_state["cookie_controller"] = CookieController()
cc = st.session_state["cookie_controller"]

# GENERAL

def deinitialize_profile_page():
    '''Used to set 'initialize' in session state to false on other pages so that the profile page loads correctly.'''
    if 'initialized' in st.session_state:
        del st.session_state.initialized

def check_user_attribute():
    if 'is_logged_in' in st.user:
        return st.user.is_logged_in
    else:
        return None

def get_key_from_value(value, dict):
    return [key for key in dict.keys() if dict[key]==value][0]

def stream_text(text):
    def create_stream():
        for word in text.split(" "):
            yield word+' '
            time.sleep(0.05)
    st.write_stream(create_stream)

def sort_dict(dict):
    sorted_keys = sorted(dict.keys())
    sorted_values = [dict[key] for key in sorted_keys]
    return {k:v for k,v in zip(sorted_keys,sorted_values)}

def page_setup():
    check_access()
    deinitialize_profile_page()


# SAVING CONVERSATIONS

def save_conversation(messages):
    code = dt.datetime.now().strftime('%Y%m%d_%H%M')
    print(messages)
    df = pd.DataFrame(messages).to_csv()

    return pd.DataFrame(messages).to_csv(), f'Wrth_Sgwrs_Conversation_{code}.csv'

def parse_file(filepath):
    '''Parses a markdown file so it's easier to include it in streamlit'''
    with open(filepath) as file:
        return '\n'.join([line.strip() for line in file.readlines()])
    
def files_in_directory(directory):
    filepaths = [entry.path for entry in os.scandir(directory) if entry.is_file()]

    def clean_filename(filename):
        return filename.replace(directory+'/', '').replace('.py', '').replace('_', ' ').title()
    
    return [(clean_filename(filepath), filepath) for filepath in filepaths]

# BUTTON FUNCTIONS

def button_press(result, topic, switch_page=False):
    df = get_data('topic_questions',2,'df')
    question = choice(list(df[df['topic'] == topic['en']]['cy'])) # type: ignore
    st.session_state.chosen_question = (question, topic)
    if switch_page:
        st.switch_page('website/pages/chatbot.py')
   
# INTERACTING WITH JSON DATA

# Getting all data from JSON file
def get_data(json_name, filepath, mode='list'):
    '''Returns a list containing the data from the JSON entry matching the given name.'''

    paths = {0: 'json_data.json'}
    paths[1] = 'data/'+paths[0]
    paths[2] = 'website/'+paths[1]

    with open(paths[filepath]) as file:
        all_data = json.load(file)

    data = [item['data'] for item in all_data if item['name'] == json_name][0]
    if mode=='list':
        return data
    elif mode=='df':
        return pd.DataFrame(data)

def add_json_entry(new_entry, filepath):
    '''Takes an entry as input in dictionary format (keys: name, description, data) and appends it to the data already in the JSON file and updates the file accordingly.'''
    
    paths = {0: 'json_data.json'}
    paths[1] = 'data/'+paths[0]
    paths[2] = 'website/'+paths[1]
    
    with open(paths[filepath]) as file:
        all_data = json.load(file)
    
    all_data.append(new_entry)
    with open(paths[filepath], 'w') as file:
        json.dump(all_data, file, indent=2)

# DICTIONARY

@st.cache_data
def load_dictionary_csv():
    return pd.read_csv('website/data/eurfa_dictionary/simple_dictionary.csv', index_col=0)

@st.cache_data
def get_dictionary_abbreviations():
    abbreviation_records = pd.read_csv('website/data/eurfa_dictionary/abbreviations.csv').to_dict('records')
    return {item['Abbreviation']:item['Meaning (English)'] for item in abbreviation_records}

def display_dictionary():

    with open('website/data/eurfa_dictionary/letter_sort.json') as file:
        letter_sort = json.load(file)

    df = load_dictionary_csv()
    abbs = get_dictionary_abbreviations()
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
                    for word in words[::4]: display_word(word, abbreviations=abbs)
                with two:
                    for word in words[1::4]: display_word(word, abbreviations=abbs)
                with three:
                    for word in words[2::4]: display_word(word, abbreviations=abbs)
                with four:
                    for word in words[3::4]: display_word(word, abbreviations=abbs)
        st.divider()

def display_word(word_tuple, abbreviations):

    if (word_tuple[2] != 'noun') or (word_tuple[4] not in abbreviations):
        word = (word_tuple[0], word_tuple[1], word_tuple[2])
    else:
        noun_type = abbreviations[word_tuple[4]]
        word = (word_tuple[0], word_tuple[1], f'{noun_type} noun')

    word_info = f'''**{word[0]}**\n| {word[1]} | _{word[2]}_
'''
    with st.container(border=True):
        st.markdown(word_info)
    
def find_word_forms(lemma):
    df = pd.read_csv('website/data/eurfa_dictionary/cylist20131111.csv')
    df = df[df['lemma'] == lemma]
    st.dataframe(df)

def get_sort(lemma):
    '''Takes a Welsh word and returns a code that can be sorted accurately due to the difference between alphabetical order in Welsh and English.'''
    
    def remove_accent(char) -> str :
        '''Removes accent if character is a vowel with an accent, otherwise returns character as it is.'''
        accents = {
            'âáàä': 'a',
            'êéèë': 'e',
            'îíìï': 'i',
            'ôóòö': 'o',
            'ûúùü': 'u',
            'ŵ': 'w',
            'ŷ': 'y'
        }
        
        for k in accents.keys():
            if char in k:
                return accents[k]
        
        return char

    welsh_alphabet = ['-', 'a', 'b', 'c', 'ch', 'd', 'dd', 'e', 'f', 'ff', 'g', 'ng', 'h', 'i', 'j', 'k', 'l', 'll',
                    'm', 'n', 'o', 'p', 'ph', 'r', 'rh', 's', 't', 'th', 'u', 'w', 'y']
    sort_codes = [str(x) for x in list(range(10))] + list('abcdefghijklmnopqrstuvwxyz')
    letter_sort = {k:v for k,v in zip(welsh_alphabet,sort_codes[:len(welsh_alphabet)])}
    output = ''
    i = 0
    lemma = lemma.lower()
    while i < len(lemma):
        if lemma[i:i+2] in welsh_alphabet:
            output += letter_sort[lemma[i:i+2]]
            i += 2
        else:
            char = remove_accent(lemma[i])
            if char in welsh_alphabet:
                output += letter_sort[char]
            else:
                output += '0'
            i += 1

    return output

def get_word_details(searchterm):
    df = load_dictionary_csv()

    if searchterm in df['lemma'].unique():
        df = df[df['lemma'] == searchterm]
        search_language = 'cy'
    elif searchterm in df['enlemma'].unique():
        df = df[df['enlemma'] == searchterm]
        search_language = 'en'
    else:
        st.write('Word not found')
        return

    for i,row in df.iterrows():
        with st.container(border=True): show_searched_word(row)


def show_searched_word(row):
    lemma = row['lemma']
    english = row['enlemma']
    word_type = row['pos']

    abbs = get_dictionary_abbreviations()

    if word_type in abbs:
        word_type = abbs[word_type]

    if lemma:
        st.write('**Welsh:**', lemma)
        st.write('**English:**', english)
        st.write('**Word type:**', word_type)
    
    if word_type == 'verb':
        get_verb_details(row)
    elif word_type in ['noun', 'n']:
        st.write(f'**Gender:** {row['gender'][0]}')


def get_verb_details(row):
    df = pd.read_csv(filepath_or_buffer='website/data/eurfa_dictionary/geiriadur.csv', index_col=0)
    df = df[(df['lemma'] == row['lemma']) & (df['enlemma'] == row['enlemma'])]
    
    df = df.sort_values('number').sort_values('tense')
    tenses = {'pres': 'Present',
              'past': 'Past',
              'fut': 'Future',
              'imper': 'Imperative (Commands)',
              'imperf': 'Imperfect',
              'pluperf': 'Pluperfect',
              'subj': 'Subjunctive'}
    number = ['1s', '2s', '3s','1p', '2p', '3p', '0', '\\N']
    pronoun_dict = {k:v for k,v in zip(number[:-2],['i', 'di', 'fe/fo/hi', 'ni', 'chi', 'nhw'])}

    impersonal_forms = df[df['number'] == '0']

    verb_forms = {}

    for tense in tenses:
        # st.write('\n\n#### '+tenses[tense]+':')
        verb_forms[tenses[tense]] = []
        filtered = df[df['tense']==tense].drop(['tense','lemma','enlemma'],axis=1)
        for pronoun in pronoun_dict:
            for i,row in filtered.iterrows():
                if row_info := return_row_info(row,pronoun,pronoun_dict):
                    # st.write(row_info)
                    # st.write()
                    verb_forms[tenses[tense]].append(row_info)
        try:
            impersonal_form = list(impersonal_forms[impersonal_forms['tense']==tense]['surface'])[0]
            # st.write(f'Impersonal form: {impersonal_form}')
            verb_forms[tenses[tense]].append(impersonal_form)
        except IndexError:
            pass

    max_value_length = max([len(v) for v in verb_forms.values()])
    for k,v in verb_forms.items():
        verb_forms[k].extend(['']*(max_value_length-len(v)))

    verb_forms = pd.DataFrame(verb_forms)
    st.dataframe(verb_forms, hide_index=True)
    st.write('_* Spoken form_')

def return_row_info(row,pronoun,pronoun_dict):
    if row['number'] == pronoun:
        if row['surface'][-1] == 't' and pronoun == '2s':
            output =  f'{row['surface']} ti'
        elif row['surface'][-1] == 't' and pronoun == '3p':
            output =  f'{row['surface']} hwy'
        else:
            output = f'{row['surface']} {pronoun_dict[pronoun]}'
        if row['notes'] == 'spoken':
            output += '*' # type: ignore
        return output
    
# AUTHENTICATION

def logout_button(label):
    if st.button(label, icon="🔒"):
        if 'guest_is_logged_in' in cc.getAll():
            cc.set('guest_is_logged_in', False)
            if 'sub' in cc.getAll(): cc.remove('sub')
            st.switch_page('website/pages/about.py')
            st.sidebar('Close')
            st.rerun()
        elif check_user_attribute():
            st.logout()

def guest_login_form():
    with st.form("guest_log_in"):
        guest_username = st.text_input(label='Choose a username')
        l,r = st.columns(2)
        with l: register = st.form_submit_button("Register", use_container_width=True)
        with r: log_in = st.form_submit_button(label="Log in", use_container_width=True)
    if register or log_in:
        guest_id = 'guest_'+guest_username
        if register:
            if guest_id in db_users:
                st.error("Username already taken, please use another one!", icon="⚠️")
            else:
                st.info(f"Username set. Welcome, {guest_username}!")
                guest_login(guest_id)
                save_user_topics([])
        elif log_in:
            if guest_id in db_users:
                st.info(f'User found. Welcome back, {guest_username}!')
                guest_login(guest_id)
            else:
                st.error("User not found, try checking your spelling or registering a new username.", icon="⚠️")

def guest_login(guest_id):
    cc.set('sub', guest_id)
    cc.set('guest_is_logged_in', True)
    cc.set('user_topics', load_user_topics())

def check_access():
    '''Fixes issue where guest is viewing page other than 'about' and sidebar disappears.'''
    if (not check_user_attribute()) and (not cc.get('guest_is_logged_in')):
        st.switch_page('website/pages/about.py')

# SAVING & LOADING USER TOPICS

def save_user_topics(input_topics):
    topics = ';'.join([str(num) for num in sorted(input_topics)])
    user_id = [st.user.sub if check_user_attribute() else cc.get('sub')][0]
    now = dt.datetime.now()
    data = [{'user_id': user_id, 'topics': topics, 'last_updated': now}]

    df = db_connection.read(worksheet="Users", ttl=0)
    if input_topics == []:
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        i = df[df['user_id'] == user_id].index.to_list()[0]
        df.loc[i, 'topics'] = topics
        df.loc[i, 'last_updated'] = now
    
    db_connection.update(worksheet="Users",data=df)

def load_user_topics():
    user_id = [st.user.sub if check_user_attribute() else cc.get('sub')][0]
    df = db_connection.read(worksheet="Users", ttl=0)

    if user_id in db_users:
        try:
            learnt_topics = df[df['user_id']==user_id]['topics'].to_list()[0]
            if type(learnt_topics) == None:
                return []
            else:
                learnt_topics = [int(x) for x in learnt_topics.split(';')]
                return learnt_topics
        except AttributeError:
            return []
    else:
        return []