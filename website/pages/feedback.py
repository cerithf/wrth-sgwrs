import streamlit as st
from website.local_functions import *

def feedback_response(question, options, key, label_type):
    
    if label_type == "numbers":
        labels=['1','5']
        width = 5
    elif label_type == "agreement":
        labels=['Disagree', 'Agree']
        width = 60
    else:
        labels = label_type
        width = int(len(labels[0])*7)

    st.markdown(f'**{question}**')
    with st.container(horizontal=True, horizontal_alignment="center", width="stretch"):
        with st.container(width=width): st.write(labels[0])
        output = st.feedback(options, key=f'response_{key}')
        st.write(labels[1])
    st.write(' ')

    return output

st.header('Feedback 📋')

st.write('Thank you for using _Wrth Sgwrs_! Use this page to give us feedback on how the app could be improved.')

with st.form("feedback_form"):

    welsh_ability = st.selectbox(
    "**How would you describe your Welsh ability?**",
    ["None", "Beginner", "Intermediate", "Advanced", "Fluent/Native"],
    index=None,
    accept_new_options=False,
    key="response_welsh_ability"
)
    st.divider() # --------------------

    overall_rating = feedback_response(
        question="How would you rate _Wrth Sgwrs_ overall?",
        options="stars",
        key="overall_rating",
        label_type="numbers"
    )

    improves_welsh = feedback_response(
        question="Do you think _Wrth Sgwrs_ would help you improve your Welsh?",
        options="faces",
        key="improves_welsh",
        label_type="numbers"
    )

    ease_of_use = feedback_response(
        question="How much do you agree with the statement: \"_Wrth Sgwrs_ is easy to use and navigate\"?",
        options="faces",
        key="ease_of_use",
        label_type="agreement"
    )

    freedom = feedback_response(
        question="How much do you agree with the statement: \"I appreciate the freedom the app gives me to learn independently\"?",
        options="faces",
        key="freedom",
        label_type="agreement"
    )

    structure = feedback_response(
        question="How much do you agree with the statement: \"The app could use more structure or guidance so I know what to do\"?",
        options="faces",
        key="structure",
        label_type="agreement"
    )

    resources = feedback_response(
        question="Is the convenience of having multiple resources in one place important to you when learning a language?",
        options="faces",
        key="resources",
        label_type=['Not at all', 'Yes, very']
    )



    st.divider() # --------------------
    
    positive_feedback = st.text_area("**What do you like about the app?**", key="response_positive_feedback")

    constructive_feedback = st.text_area("**What could be improved about the app?**", key="response_constructive_feedback")

    submit = st.form_submit_button()


if submit:
    st.write(st.session_state)