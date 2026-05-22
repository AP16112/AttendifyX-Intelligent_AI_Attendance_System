# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for creating subject for teachers

import streamlit as st
# here we are importing the create_subject function from the db.py file, which will help us to create a new subject record in the subjects table in the database, so that we can use that function to create a new subject record in the subjects table in the database when the teacher fills the form and submits it.
from src.database.db import create_subject


@st.dialog("Create New Subject")   # here this st.dialog() is used to create a dialog box with the title "Create New Subject", and this dialog box will contain the form for creating a new subject, and this dialog box will be shown when the teacher clicks on the "Create Subject" button in the manage subjects tab in the teacher dashboard.
def create_subject_dialog(teacher_id):   # so this create_subject_dialog() function will take the teacher_id as a parameter, which will be used to associate the newly created subject with the teacher who created it, so that we can later show only those subjects to the teacher which are associated with that teacher in the manage subjects tab in the teacher dashboard.    
    st.write("Enter the details of new subject")     # this st.write() is used to show this text inside the dialog box, which will be shown above the form for creating a new subject, so that it will give some instruction to the teacher about what to do in this dialog box.
    sub_id = st.text_input("Subject code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type='primary', width='stretch'):
        if sub_id and sub_name and sub_section:    # if all the fields are filled, then only we will create the subject, otherwise we will show a warning message to the teacher to fill all the fields.
            try:    # as here we are storing this in database, so it can fail also, that's why we are using try and catch block here
                create_subject(sub_id, sub_name, sub_section, teacher_id)       # here this create_subject() function is used to create a new subject record in the subjects table in the database with the given subject id, subject name, subject section and teacher id, so that we can later show this newly created subject in the manage subjects tab in the teacher dashboard, and also we can use this subject record to take attendance for that subject in the take attendance tab in the teacher dashboard.
                st.toast("Subject Created Successfully!")   # this st.toast() is used to show this success message to the teacher when the subject is created successfully, and this message will be shown as a toast notification at the bottom of the screen, and it will disappear automatically after a few seconds.
                st.rerun()   # This will make this toast message to disappear after a few seconds, and also it will refresh the page to show the updated list of subjects in the manage subjects tab in the teacher dashboard, so that the teacher can see the newly created subject in the list of subjects in the manage subjects tab in the teacher dashboard.
            except Exception as e:
                st.error(f"Error : {str(e)}")   # str(e) is used to convert this exception object into a string format, so that we can show this error message to the teacher in a readable format using this st.error() function, and this message will be shown as an error message at the bottom of the screen, and it will disappear automatically after a few seconds.
        else:
            st.warning("Please fill all the fields")


