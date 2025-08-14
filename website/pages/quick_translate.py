import streamlit as st
from website.local_functions import *
from deep_translator import GoogleTranslator, DeeplTranslator
from datetime import datetime as dt
import pandas as pd

ss = st.session_state
page_setup()

if 'translations' not in ss:
    ss.translations = []
if 'translation_df' not in ss:
    ss.translation_df = pd.DataFrame(columns=['Timestamp', 'Entered text', 'Translated output', 'Mode'])

with st.container(horizontal=True):
    st.title('Quick Translate')
    translators = ['DeepL', 'Google Translate']
    chosen_translator = st.segmented_control('Choose a translation method:',translators,default=translators[0])

control_options = ['English -> Welsh', 'Welsh -> English']
mode = st.segmented_control(label='',options=control_options,default=control_options[0])

if mode == control_options[0]:
    source_lang = 'English','en'
    targ_lang = 'Welsh','cy'
    text_area_label = f'_Write something in the box to translate it into Welsh. Type ⌘↵ to enter text._'
    history_label = '**History**'
else:
    source_lang = 'Welsh','cy'
    targ_lang = 'English', 'en'
    text_area_label = f'_Ysgrifennwch rywbeth yn y blwch isod i\'w gyfieithu i Saesneg. Defnyddiwch ⌘↵ i fewnfudo\'r testun._'
    history_label = '**Hanes**'

entered_text = st.text_area(label=text_area_label)

def translated_text():
    if chosen_translator == 'DeepL':
        return DeeplTranslator(source=source_lang[1], target=targ_lang[1],api_key=st.secrets['DEEPL_API_KEY'],use_free_api=True)
    elif chosen_translator == 'Google Translate':
        return GoogleTranslator(source=source_lang[1], target=targ_lang[1]).translate(entered_text)

data = {
    'Timestamp': dt.now().strftime('%Y-%m-%d %H:%M%:%S'),
    'Entered text': entered_text,
    'Translated output': translated_text(),
    'Mode': mode
}

welsh_data_labels = {
    'Timestamp': 'Amser mewnfudwyd',
    'Entered text': 'Testun mewnbwn',
    'Source language': 'Iaith wreiddiol',
    'Translated output': 'Allbwn a gyfieithwyd',
    'Output language': 'Iaith yr allbwn'
}

if entered_text != '':
    st.markdown('#### Translated output:')
    st.write(data['Translated output'])
    st.session_state.translation_df.loc[len(st.session_state.translation_df)] = data
    if entered_text not in [entry['Entered text'] for entry in st.session_state.translations]:
        st.session_state.translations.append(data)


with st.expander(label=history_label, expanded=False, icon=':material/history:'):
    st.dataframe(st.session_state.translation_df.sort_values('Timestamp', ascending=False), hide_index=True)
    pass