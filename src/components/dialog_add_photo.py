# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for adding photos for taking face attendance

import streamlit as st

from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project

# here This PIL is actually pillow library which is used for image processing in python, so here we will use this library to process the image taken from camera input for facial recognition and attendance marking, so here we are importing this library in this student_screen.py file because we will use this library in this file for processing the image taken from camera input for facial recognition and attendance marking
# We actually write pillow in short as PIL, so here we are importing the Image module from PIL library, which will allow us to open and manipulate images in python, so here we will use this Image module to open the image taken from camera input and then we will process that image for facial recognition and attendance marking
from PIL import Image


@st.dialog("Capture or upload photos")   # here this st.dialog() is used to create a dialog box with the title "Capture or upload photos"
def add_photos_dialog():  
    st.write('Add classroom photos to scan for attendance')

    # Now we will create a state in session_state for checking which mode user choose for adding photos
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'upload'    # here default mode we are taking to be 'upload'

    t1, t2 = st.columns(2)    # here we are creating two tabs (i.e columns) actually

    with t1:
        # here this type_camera means the type of this camera opening button
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else "tertiary"

        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
        # here this type_upload means the type of this upload photos button
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else "tertiary"

        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        # st.camera_input() → renders a camera interface in the browser so the user can capture an image.
        # key='dialog_cam' → assigns a unique key so Streamlit can track the widget state.
        # Return value → if the user takes a photo, cam_photo will hold the image as a BytesIO object (we can process it with PIL, OpenCV, etc.). If no photo is taken, it will be None.
        cam_photo = st.camera_input('Take Snapshoot', key='dialog_cam')

        if cam_photo:   # if photo is taken using camera then we will add that photo to attendance_images state
            # we cannot directly store this cam_photo, we need to convert this into usable format
            # Image.open(cam_photo) → uses PIL (Python Imaging Library) to open the captured image into a usable format (PIL Image object).
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured')
            st.rerun()   # so that this dialog gets closed automatically


    if st.session_state.photo_tab == 'upload':
        # 'Choose image files' → label shown above the uploader.
        # type=['jpg', 'png', 'jpeg'] → restricts uploads to image formats only.
        # accept_multiple_files=True → allows users to select and upload more than one file at once.
        # key='dialog_upload' → unique identifier for this widget so Streamlit can track its state.
        # Return value → uploaded_files will be a list of uploaded files (or empty list if none uploaded). Each file is a UploadedFile object that you can read or process.
        uploaded_files = st.file_uploader('choose image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True,  key='dialog_upload')

        if uploaded_files:
            for f in uploaded_files:
                # we cannot directly store this f, we need to convert this into usable format
                # Image.open(f) → uses PIL (Python Imaging Library) to open the captured image into a usable format (PIL Image object).
                st.session_state.attendance_images.append(Image.open(f))
            
            st.toast('Photos Uploaded Successfully')
            st.rerun()   # so that this dialog gets closed automatically


    st.divider()

    if st.button('Done', type='primary', width='stretch'):
        st.rerun()    # so that this dialog gets closed automatically









