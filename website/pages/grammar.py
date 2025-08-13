import streamlit as st
import json
from website.local_functions import *
import os

ss = st.session_state
page_setup()

# Creating a list of markdown files in the appropriate folder

md_files = []
directory = os.fsencode('website/pages/grammar')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename[-2:] == 'md':
        md_files.append(filename[:-3])
md_files = sorted(md_files)

# Creating a selectbox out of the list of files

option = st.selectbox(
    "Select a grammatical element to read about!",
    md_files,
    index=None,
    accept_new_options=False,
)

# Displays text once file is chosen

if option:
    with open(f'website/pages/grammar/{option}.md') as file:
        text = file.read()

    st.markdown(text)