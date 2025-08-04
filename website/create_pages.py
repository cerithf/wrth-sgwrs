# %% 

import streamlit as st
from local_functions import *
import os

p(5)
filepath = 'Grammar/Other/bbc.md'
with open(filepath) as file:
    full_text = file.read().split('<!--SPLIT-->')

full_text = {chapter.split('\n')[1].strip('## '):chapter.split('\n') for chapter in full_text[1:]}

titles = full_text.keys()

# %%

for title in titles:

    text_body = '\n'.join(full_text[title])

    with open(f'pages/grammar/{title}.py', 'w') as file:
        file.write(f'''import streamlit as st
                   
st.markdown("""{text_body}""")
''')


p(5)