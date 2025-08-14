import streamlit as st
from website.local_functions import *


# Creates a cleaner layout for feedback field
def feedback_field(question, options, key, label_type):
    
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

# Creating a dictionary to collect user's responses
feedback_response = {'user_id': [st.user.sub if check_user_attribute() else cookie_controller.get('sub')][0]}

# ------------------------------------------------------------------------------------------------------------------------------------------------------

st.header('Feedback 📋')

st.write('Thank you for using _Wrth Sgwrs_! Use this page to give us feedback on how the app could be improved.')

with st.form("feedback_form"): # -----------------------------------------------------------------------------------------------------------

    feedback_response["welsh_ability"] = st.selectbox(
    label="**How would you describe your Welsh ability?**",
    options=['No Knowledge', 'Beginner', 'Intermediate', 'Advanced', 'Fluent/Native'],
    index=None,
    accept_new_options=False,
    key="response_welsh_ability"
)
    
    uses_other_resources = st.segmented_control(
        label="**Do you use (or have you used) other resources to learn Welsh? If so, which one(s)?**",
        options=['Yes', 'No'],
        default=None
        )
    
    if uses_other_resources == 'Yes':
        feedback_response["other_resources_used"] = st.text_input('Which other resources do you use to learn Welsh?')
    elif uses_other_resources == 'No':
        feedback_response["other_resources_used"] = "None"

    st.divider()

    feedback_response["overall_rating"] = feedback_field(
        question="How would you rate _Wrth Sgwrs_ overall?",
        options="stars",
        key="overall_rating",
        label_type="numbers"
    )

    feedback_response["improves_welsh"] = feedback_field(
        question="Do you think _Wrth Sgwrs_ would help you improve your Welsh?",
        options="faces",
        key="improves_welsh",
        label_type="numbers"
    )

    feedback_response["ease_of_use"] = feedback_field(
        question="How much do you agree with the statement: \"_Wrth Sgwrs_ is easy to use and navigate\"?",
        options="faces",
        key="ease_of_use",
        label_type="agreement"
    )

    feedback_response["freedom"] = feedback_field(
        question="How much do you agree with the statement: \"I appreciate the freedom the app gives me to learn independently\"?",
        options="faces",
        key="freedom",
        label_type="agreement"
    )

    feedback_response["structure"] = feedback_field(
        question="How much do you agree with the statement: \"The app could use more structure or guidance so I know what to do\"?",
        options="faces",
        key="structure",
        label_type="agreement"
    )

    feedback_response["resources"] = feedback_field(
        question="Is the convenience of having multiple resources in one place important to you when learning a language?",
        options="faces",
        key="resources",
        label_type=['Not at all', 'Yes, very']
    )

    st.divider()

    feedback_response["positive_feedback"] = st.text_area("**What do you like about the app?**", key="response_positive_feedback")

    feedback_response["constructive_feedback"] = st.text_area("**What could be improved about the app?**", key="response_constructive_feedback")

    submit = st.form_submit_button()

if submit:
    feedback_response["submitted"] = dt.datetime.now()
    feedback_db = db_connection.read(worksheet="Feedback", ttl=0)
    df = pd.concat([feedback_db, pd.DataFrame([feedback_response])], ignore_index=True)
    db_connection.update(worksheet="Feedback",data=df)

    st.toast('Thank you for submitting your feedback!', icon="🎉")
    st.balloons()