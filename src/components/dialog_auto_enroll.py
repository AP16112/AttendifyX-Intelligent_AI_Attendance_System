# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for auto enroll in some subject

import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project
import time


@st.dialog("Quick Enrollment")   # here this st.dialog() is used to create a dialog box with the title "Quick Enrollment"
def auto_enroll_dialog(subject_code):  
    student_id = st.session_state.student_data['student_id']

    # Now we will check whether this subject having this subject code exists in database or not
    res = supabase.table('subjects').select('subject_id', 'name').eq('subject_code', subject_code).execute()

    if not res.data:    # it means that if this response doesn't comes i.e if this subject doesn't exists in database
        st.error('Subject Code not found!')

        if st.button('Close'):
            st.query_params.clear()     # wipes out any query parameters currently in the URL (like ?join-code=ABC123).
            st.rerun()   # forces the app to restart from the top of the script, now without those query parameters.
        return     # and then we will stop & return back
    

    # But if res.data found, then we will enroll that student to the subject 
    subject = res.data[0]     # although in this case, it will only have one subject but in the form of list actually & is present at 0th index

    # This line queries the 'subject_students' table in Supabase to check if a specific student is already enrolled in a specific subject. It selects all columns, applies two filters:
    # one where the subject_id matches the current subject's ID and another where the student_id matches the given student, and then executes the query to return any matching record.
    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

    if check.data:   # if some data exits, then it means that this student is already enrolled in this subject
        st.info("You are already enrolled!")
         
        if st.button('Got it!'):
            st.query_params.clear()     # wipes out any query parameters currently in the URL (like ?join-code=ABC123).
            st.rerun()   # forces the app to restart from the top of the script, now without those query parameters.
        return     # and then we will stop & return back
    
    
    # Now if check.data doesn't exists, then it means that student is not enrolled in this subject
    st.markdown(f"Would you like to enroll in **{subject['name']}**")      # ** in markdown is used to make the content bold just like <b>

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            st.query_params.clear()     # wipes out any query parameters currently in the URL (like ?join-code=ABC123).
            st.rerun()   # forces the app to restart from the top of the script, now without those query parameters.
    

    with col2:
        if st.button("Yes enroll now!", type='primary', width='stretch'):
            # now we will enroll this currently logged in student to this subject
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('Joined Successfully!')
            st.query_params.clear()     # wipes out any query parameters currently in the URL (like ?join-code=ABC123).
            time.sleep(2)
            st.rerun()   # forces the app to restart from the top of the script, now without those query parameters.



