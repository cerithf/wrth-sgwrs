# %%
import json
import pandas as pd

with open('json_data.json') as file:
    data = json.load(file)

questions = {topic['name']:topic for topic in data}['topic_questions']['data']

questions = pd.DataFrame(questions)
questions.to_csv('questions.csv')
# %%
