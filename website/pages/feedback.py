import streamlit as st
from website.local_functions import *

def feedback_response(question, options, key, number_labels=True):
    
    if number_labels:
        labels=['1','5']
        width = 5
    else:
        labels=['Disagree', 'Agree']
        width = 60

    st.write(question)
    with st.container(horizontal=True, horizontal_alignment="left", width=300):
        with st.container(width=width): st.write(labels[0])
        output = st.feedback(options, key=f'response_{key}')
        st.write(labels[1])

    return output



st.header('Feedback')

st.write('Thank you for using _Wrth Sgwrs_! Use this page to give us feedback on how the app could be improved.')

with st.form("feedback_form"):

    welsh_ability = st.selectbox(
    "How would you describe your Welsh ability?",
    ["None", "Beginner", "Intermediate", "Advanced", "Fluent/Native"],
    index=None,
    accept_new_options=False,
    key="response_welsh_ability"
)
    st.divider() # --------------------

    overall_rating = feedback_response(
        question="How would you rate _Wrth Sgwrs_ overall?",
        options="stars",
        key="overall_rating"
    )

    ease_of_use = feedback_response(
        question="How much do you agree with the statement: '_Wrth Sgwrs_ is easy to use and navigate'?",
        options="faces",
        key="ease_of_use",
        number_labels=False
    )

    improves_welsh = feedback_response(
        question="Do you think _Wrth Sgwrs_ would help you improve your Welsh?",
        options="faces",
        key="improves_welsh"
    )

    st.divider() # --------------------

    st.write("Do you have any general feedback?")
    general_feedback = st.text_area('Write feedback here', key="response_general_feedback")

    submit = st.form_submit_button()


if submit:
    st.write(st.session_state)