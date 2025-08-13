#%% 

import streamlit as st
from local_functions import *
import pandas as pd
import json

# Applicable functions are in local_functions.py under heading 'INTERACTING WITH JSON DATA'
# Variable all_data imported from local_functions contains the data in the file json_data.json

df = pd.read_csv('website/data/questions.csv', index_col=0)
data = df.to_dict('records')
# %%

json_entry = {
    'name': 'topic_questions',
    "description": "Automatically generated questions to start a conversation, matching up to each of the topics in conversation_topics.",
    'data': data
}

with open('website/data/json_data.json') as file:
    all_data = json.load(file)

all_data[1] = json_entry
all_data

# %%
with open('website/data/json_data.json', 'w') as file:
    json.dump(all_data,file,indent=2)
