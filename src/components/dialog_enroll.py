# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for enroll in some subject

import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project
import time


@st.dialog("Enroll in Subject")   # here this st.dialog() is used to create a dialog box with the title "Enroll in Subject"
def enroll_dialog():  
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:     # checking whether student input the subject code or not
            # Now we will check whether this subject having this subject code exists in database or not
            res = supabase.table('subjects').select('subject_id', 'name', 'subject_code').eq('subject_code', join_code).execute()
            # so if we get some result from this query then it means that this particular subject exists in database whose code is same as this join code
            # so this res.data will contains the list of subjects 
            if res.data:    # it means that if this response conatins some data of subject
                subject = res.data[0]     # as we know that subject_code is unique, so this res.data will always only contains 1 subject info list only in this case, so that subject will be present at 0th index
                student_id = st.session_state.student_data['student_id']

                # This line queries the 'subject_students' table in Supabase to check if a specific student is already enrolled in a specific subject. It selects all columns, applies two filters:
                # one where the subject_id matches the current subject's ID and another where the student_id matches the given student, and then executes the query to return any matching record.
                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

                if check.data:   # if some data exits, then it means that this student is already enrolled in this subject
                    st.warning("You are already enrolled in this program")
                else:
                    # so student is not enrolled then we will enroll that student in this subject
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success('Successfully enrolled!')
                    time.sleep(1)
                    st.rerun()      # here we are reruning , so that the list containing in how subjects student is enrolled must get updated.

        else:
            st.warning("Please enter a subject code")


