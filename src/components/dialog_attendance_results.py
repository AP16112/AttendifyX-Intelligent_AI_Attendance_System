# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for showing the final attendance result 

import streamlit as st

from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project
from src.database.db import create_attendance


@st.dialog("Attendance Reports")   
def attendance_result_dialog(df, logs):
    st.write("Please review attendance before confirming.")  

    # st.dataframe(df, ...) → renders your Pandas DataFrame (df) as an interactive table in the Streamlit app.
    # hide_index=True → hides the default numeric index column (0, 1, 2, …) so only your defined columns like "Name", "ID", "Source" show up.
    st.dataframe(df, hide_index=True, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.rerun()   

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            # here we will use try and catch block because we are working with database & saving attendance in database can give error also
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                # Now as attendance is taken, so now there is no use of images taken for attendance & which we store in attendance_images state in session_state, so we will clear them
                st.session_state.attendance_images = []
                st.rerun()
                # Clear attendance_images from session_state after saving.
                # Use st.rerun() to immediately refresh the app so the cleared state is reflected in the UI.
            except Exception as e:
                st.error('Sync Failed!')






