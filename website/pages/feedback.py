import streamlit as st
from website.local_functions import *

st.header('Feedback')

st.write('Thank you for using _Wrth Sgwrs_! Use this page to give us feedback on how the app could be improved.')

with st.form("feedback_form"):

    welsh_ability = st.selectbox(
    "How would you describe your Welsh ability?",
    ["None", "Beginner", "Intermediate", "Advanced", "Fluent/Native"],
    index=None,
    accept_new_options=False,
)
    st.divider() # --------------------

    st.write("How would you rate _Wrth Sgwrs_ overall?")
    overall_rating = st.feedback("stars", key="overall_rating")

    st.write("Would you say that _Wrth Sgwrs_ is easy to use?")
    ease_of_use = st.feedback("faces", key="ease_of_use")

    st.write("Do you think _Wrth Sgwrs_ would help you improve your Welsh?")
    improves_welsh = st.feedback("faces", key="improves_welsh")

    st.divider() # --------------------

    st.write("Do you have any general feedback?")
    general_feedback = st.text_area('Write feedback here')

    submit = st.form_submit_button()


with st.container(horizontal=True, horizontal_alignment="left", width=100):
    st.write('0')
    st.feedback('faces', key="test")
    st.write('5')