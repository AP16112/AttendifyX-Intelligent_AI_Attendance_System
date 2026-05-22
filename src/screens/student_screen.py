# Here Inside this src folder, we write all our project source code actually
# This screens folder contains the screens or webpages for teachers, student and home page

# This is Student login page.

import streamlit as st

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import  style_base_layout, style_background_dashboard

# here This PIL is actually pillow library which is used for image processing in python, so here we will use this library to process the image taken from camera input for facial recognition and attendance marking, so here we are importing this library in this student_screen.py file because we will use this library in this file for processing the image taken from camera input for facial recognition and attendance marking
# We actually write pillow in short as PIL, so here we are importing the Image module from PIL library, which will allow us to open and manipulate images in python, so here we will use this Image module to open the image taken from camera input and then we will process that image for facial recognition and attendance marking
from PIL import Image
import numpy as np  # here we are importing numpy library which is used for numerical operations in python, so here we will use this library to convert the image taken from camera input into a numpy array, so that we can use that numpy array for facial recognition and attendance marking


from src.pipelines.face_pipeline import get_face_embeddings, predict_attendance, train_classifier     # here we are importing this predict_attendance() function from this face_pipeline.py file, which will contain the code for facial recognition and attendance marking, so here we will use this predict_attendance() function to process the image taken from camera input for facial recognition and attendance marking, so here we are importing this function in this student_screen.py file because we will use this function in this file to process the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of the student who is trying to login using FaceID on the student screen of our app.
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student      # here we are importing this get_all_students() function from this db.py file, which will contain the code for interacting with the database to get the list of all the student records from the students table in the database, so here we will use this get_all_students() function to get the list of all the student records from the students table in the database, so here we are importing this function in this student_screen.py file because we will use this function in this file to get the list of all the student records from the students table in the database, so that we can compare that list of student records with the face detected from the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of the student who is trying to login using FaceID on the student screen of our app.
import time   # here we are importing this time library which is used for time related operations in python, so here we will use this library to add some delay after the student is successfully logged in using FaceID on the student screen of our app, so that we can show the welcome message to the student for some time before rerunning the app to show the dashboard for logged in student, so here we are importing this library in this student_screen.py file because we will use this library in this file to add some delay after the student is successfully logged in using FaceID on the student screen of our app, so that we can show the welcome message to the student for some time before rerunning the app to show the dashboard for logged in student.


def student_dashboard():
    student_data = st.session_state.student_data  # here this student_data session variable will contain the data of the currently logged in student, so we can use this data to show the student name on the dashboard screen and also we can use this data to fetch the attendance data of that student from the database and then we can show that attendance data on the dashboard screen to the student

    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()

    with c2:
        # st.subheader(f"""Welcome, {student_data['name']}!""")    # it just uses the default h3 tag 
        # ---------OR------------
        st.markdown(f"""
            <div style='display: flex;  align-items: center;  justify-content: left;'>
                <h3 style='color: #1e1e1e;  text-align: center'> Welcome, {student_data['name']}! </h3>
            </div>
            """,
            unsafe_allow_html=True
        ) 

        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False  
            del st.session_state.student_data       # This removes the key student_data (and its value) from the session state.
            # After this line runs, trying to access st.session_state.student_data will raise a KeyError because it no longer exists.
            st.rerun()   # as here state is changing, so we need to rerun it


    st.space()


    footer_dashboard()





def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:   # here we are checking that if this student_data variable is present in session state, then it means that the student is logged in, so we will show the content for logged in student, otherwise we will show the content for student login using FaceID on the student screen of our app.
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None    # so now it will show the home screen as for home screen login_type is set to None actually
            st.rerun()   # as here state is changing, so we need to rerun it


    # st.header('Login using FaceID')    # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;  text-align: center'> Login using FaceID </h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.space()    # similar to <br> tag
    st.space()

    show_registration = False   

    # here we will add the camera input for student to take their picture for attendance marking using facial recognition, so here we are using st.camera_input() function of streamlit which will allow us to take input from camera and then it will return the image file which we can use for facial recognition and attendance marking
    photo_source = st.camera_input("Position your face in the center")

    if photo_source: # here this photo_source variable will contain the image file which we can use for facial recognition and attendance marking, so here we are checking that if photo_source variable is not empty, then it means that student has taken the picture using camera and then we can use this photo_source variable for facial recognition and attendance marking
        img = np.array(Image.open(photo_source))  # here we are opening the image file using Image.open() function of PIL library and then we are converting that image into a numpy array using np.array() function of numpy library, so that we can use that numpy array for facial recognition and attendance marking

        # here we are applying this spinner of streamlit which will show the loading animation while the AI is scanning the image for facial recognition and attendance marking, so here we are using this st.spinner() function of streamlit which will show the loading animation while the AI is scanning the image for facial recognition and attendance marking, so here we are using this st.spinner() function as a context manager with the "with" statement, so that it will automatically start the spinner when we enter the block of code inside the "with" statement and it will automatically stop the spinner when we exit the block of code inside the "with" statement, so here we are writing our code for facial recognition and attendance marking inside this "with" block, so that it will show the loading animation while the AI is scanning the image for facial recognition and attendance marking.
        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)   # here we are calling this predict_attendance() function and passing the image taken from camera input as an argument to this function, so that it can process that image for facial recognition and attendance marking, so here we will write the code for facial recognition and attendance marking inside this predict_attendance() function, so that it can process the image taken from camera input for facial recognition and attendance marking

            if num_faces == 0:  # if no face is detected in the image taken from camera input, then we will show this message to the student
                st.warning("Face not found!")
            elif num_faces > 1:   # if multiple faces are detected in the image taken
                st.warning("Multiple faces found")
            else:
                if detected:  
                    # here detected variable will contains the student_id of the student whose face is detected from the image taken from camera input 
                    # but here we are only considering one face for login for that student
                    student_id = list(detected.keys())[0]   
                    all_students = get_all_students()   # here we are calling this get_all_students() function to get the list of all the student records from the students table in the database, so that we can compare that list of student records with the face detected from the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of the student who is trying to login using FaceID on the student screen of our app.
                    # so here we are using this next() function to get the student record from the list of all the student records which has the same student_id as the one detected from the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of that student who is trying to login using FaceID on the student screen of our app, so here we are using this next() function with a generator expression to iterate through the list of all the student records and find the student record which has the same student_id as the one detected from the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of that student who is trying to login using FaceID on the student screen of our app, so here we are using this next() function with a generator expression to find the student record which has the same student_id as the one detected from the image taken from camera input for facial recognition and attendance marking, so that we can mark the attendance of that student who is trying to login using FaceID on the student screen of our app.
                    student = next((s for s in all_students if s['student_id'] == student_id), None) 

                    if student:
                        st.session_state.is_logged_in = True   # here we are setting this is_logged_in variable in session state to true, so that we can use this variable to check whether the student is logged in or not in other parts of our app, so that we can show the appropriate content to the student based on whether they are logged in or not, so here we are setting this variable to true when the student is successfully logged in using FaceID on the student screen of our app.
                        st.session_state.user_role = "student"   # here we are setting this user_role variable in session state to "student", so that we can use this variable to check the role of the user in other parts of our app, so that we can show the appropriate content to the user based on their role, so here we are setting this variable to "student" when the student is successfully logged in using FaceID on the student screen of our app.
                        st.session_state.student_data = student  # here we are setting this student_data variable in session state to the student record which we got from the list of all the student records, so that we can use this variable to access the student data in other parts of our app, so that we can show the appropriate content to the student based on their data, so here we are setting this variable to the student record which we got from the list of all the student records when the student is successfully logged in using FaceID on the student screen of our app.
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()   # as here state is changing, so we need to rerun it

                else:   # if the face is detected but not recognized, then we will show this info message to the student
                    st.info("Face not recognized! You might be a new student!")
                    show_registration = True   # here we are setting this show_registration variable to true, so that we can show the registration form to the student for registering themselves in the database, so that they can login using FaceID on the student screen of our app in future, so here we are setting this variable to true when the face is detected but not recognized, so that we can show the registration form to the student for registering themselves in the database, so that they can login using FaceID on the student screen of our app in future.


    if show_registration: 
        with st.container(border=True):   # this st.container is just same as div element of html
            # st.header("Register new Profile")      # it just uses the default h2 tag 
            # ---------OR------------
            st.markdown(f"""
                <div style='display: flex;  align-items: center;  justify-content: center;'>
                    <h2 style='color: #1e1e1e;  text-align: center'>Register new Profile</h2>
                </div>
                """,
                unsafe_allow_html=True
            ) 

            new_name = st.text_input("Enter your name", placeholder="e.g. Arpit Pal")

            st.divider()    # it adds a horizontal line similar to <hr> tag

            # st.subheader('Optional : Voice Enrollment')    # it just uses the default h3 tag 
            # ---------OR------------
            st.markdown(f"""
                <div style='display: flex;  align-items: center;  justify-content: left;'>
                    <h3 style='color: #1e1e1e;  text-align: center'>Optional : Voice Enrollment</h3>
                </div>
                """,
                unsafe_allow_html=True
            ) 

            st.info("Enroll for voice for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase (e.g. "Hello, My name is Arpit Pal & this is my voice. Speak something for 10-20 seconds")')
            except Exception as e:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    # here we will write the code for creating the student record in the database with the name entered by the student in the text input field and also with the audio data taken from the audio input for voice enrollment, so that we can use that audio data for voice recognition and attendance marking in future when the student tries to login using voice on the student screen of our app, so here we will write this code for creating the student record in the database inside this if block, so that it will be executed when the student clicks on this "Create Account" button after entering their name in the text input field and also after recording their audio data for voice enrollment using the audio input.
                    with st.spinner("Creating profile..."):  
                        img = np.array(Image.open(photo_source))  # here we are opening the image file using Image.open() function of PIL library and then we are converting that image into a numpy array using np.array() function of numpy library, so that we can use that numpy array for storing that face in database
                        encodings = get_face_embeddings(img) 
                        # here this will actually return the list of embeddings one for each of the faces detected in the img

                        if encodings:
                            face_emb = encodings[0].tolist()  # here we are taking the first encoding from the list of encodings and converting that encoding into a list format using .tolist() function, so that we can store that encoding in the database in list format
                            # but here we will only consider the first encoding i.e only 1 student encoding who is actually registering

                            voice_emb = None   # currently we are taking voice embeddings to be None as voice is optional

                            if audio_data:   # if audio_data exists, then only we will add the voice embeddings into the database
                                # here this .read() fn will convert the audio_data to bytes format actually
                                voice_emb = get_voice_embedding(audio_data.read())

                            # here this create_student() fn will actually create this new student & add it into the database
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:  # so if this new student gets added into database then we need to again train our model with new student database now
                                train_classifier()
                                st.session_state.is_logged_in = True   # here we are setting this is_logged_in variable in session state to true, so that we can use this variable to check whether the student is logged in or not in other parts of our app, so that we can show the appropriate content to the student based on whether they are logged in or not, so here we are setting this variable to true when the student is successfully logged in using FaceID on the student screen of our app.
                                st.session_state.user_role = "student"   # here we are setting this user_role variable in session state to "student", so that we can use this variable to check the role of the user in other parts of our app, so that we can show the appropriate content to the user based on their role, so here we are setting this variable to "student" when the student is successfully logged in using FaceID on the student screen of our app.
                                st.session_state.student_data = response_data  # here we are setting this student_data variable in session state to the response_data 
                                st.toast(f"Profile Created!, Hi {new_name}")
                                time.sleep(1)
                                st.rerun()   # as here state is changing, so we need to rerun it
                        else:  # if face embeddings not found
                            st.error("Couldn't capture your facial features for registration")
                else:
                    st.warning("Please enter your name!")


    footer_dashboard()