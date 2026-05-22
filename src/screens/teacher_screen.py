# Here Inside this src folder, we write all our project source code actually
# This screens folder contains the screens or webpages for teachers, student and home page

# This is teacher login page.

import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.ui.base_layout import  style_base_layout, style_background_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()


    if "teacher_data" in st.session_state:  # here this teacher_data session variable will contain the data of the currently logged in teacher, so if this session variable is present in the st.session_state, then it means that teacher is logged in and we can show the teacher dashboard screen to the teacher, so here we are checking that if "teacher_data" session variable is present in st.session_state or not, if it is present, then we will show the teacher dashboard screen to the teacher
        teacher_dashboard()
    # Now we will create a session state variable for login which will show what is the type of teacher login
    elif 'teacher_login_type' not in st.session_state  or  st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()
    


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data  # here this teacher_data session variable will contain the data of the currently logged in teacher, so we can use this data to show the teacher name on the dashboard screen and also we can use this data to fetch the attendance data of that teacher from the database and then we can show that attendance data on the dashboard screen to the teacher

    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()

    with c2:
        # st.subheader(f"""Welcome, {teacher_data['name']}!""")    # it just uses the default h3 tag 
        # ---------OR------------
        st.markdown(f"""
            <div style='display: flex;  align-items: center;  justify-content: center;'>
                <h3 style='color: #1e1e1e;  text-align: center'> Welcome, {teacher_data['name']}! </h3>
            </div>
            """,
            unsafe_allow_html=True
        ) 

        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False  
            del st.session_state.teacher_data       # This removes the key teacher_data (and its value) from the session state.
            # After this line runs, trying to access st.session_state.teacher_data will raise a KeyError because it no longer exists.
            st.rerun()   # as here state is changing, so we need to rerun it


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary"  if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button('Take Attendance', type=type1,  width='stretch',  icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary"  if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button('Manage subjects', type=type2,  width='stretch',  icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
        
    with tab3:
        type3 = "primary"  if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button('Attendance Records', type=type3,  width='stretch',  icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
 

    footer_dashboard()



def teacher_tab_take_attendance():
    # st.header("Take AI Attendance")    # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;  text-align: center'> Take AI Attendance </h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']   # here this teacher_data session variable will contain the data of the currently logged in teacher, so we can use this data to get the id of the currently logged in teacher, so that we can use that id to fetch the subjects created by that teacher from the database and then we can show those subjects on the manage subjects tab of the dashboard screen to the teacher

    col1, col2 = st.columns(2)

    with col1:
        # st.header("Manage Subjects")    # it just uses the default h2 tag 
        # ---------OR------------
        st.markdown(f"""
            <div style='display: flex;  align-items: center;  justify-content: left;'>
                <h2 style='color: #1e1e1e;  text-align: center'> Manage Subjects </h2>
            </div>
            """,
            unsafe_allow_html=True
        ) 


    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # List ALL Subjects
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            # here we are creating a share button for each subject, so that teacher can share the subject code with their students, so that students can use that subject code to join that subject and then they can take attendance for that subject using FaceID on the student screen of our app, so here we are creating a share button for each subject, and when the teacher clicks on that button, then it will open a dialog box which will show the subject code and also it will have a copy button to copy that subject code to clipboard, so that teacher can easily share that subject code with their students.
            def share_btn(current_sub=sub):
                # Here we are defining this share_btn() function which will return a button component with the label "Share Code: {subject name}" and when the teacher clicks on that button, then it will open a dialog box which will show the subject code and also it will have a copy button to copy that subject code to clipboard, so that teacher can easily share that subject code with their students.
                if st.button(f"Share Code: {current_sub['name']}", key=f"share_{current_sub['subject_code']}", type='secondary', icon=':material/share:'):
                    share_subject_dialog(current_sub['name'], current_sub['subject_code'])

                st.space()

            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,   # here stats means the extra values that we want to show
                footer_callback = share_btn
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")





def teacher_tab_attendance_records():
    # st.header("Attendance Records")    # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;  text-align: center'> Attendance Records </h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 




def login_teacher(username, password):
    if not username or not password:   # here we are checking that if username or password is empty, then we will return false, because both username and password are required for login
        return False
    
    teacher = teacher_login(username, password)   # here this teacher_login() function will check that the teacher with this username and password exists in the database or not, if it returns something, then it means that teacher with this username and password exists in the database, so we will return that teacher record, otherwise it will return None

    if teacher:   # if this teacher variable is not None, then it means that teacher with this username and password exists in the database, so we will return true, otherwise we will return false
        st.session_state.user_role = "teacher"   # so here we are setting this user_role session variable to "teacher", so that we can use this session variable to check the role of the currently logged in user in other parts of the app, so that we can show different UI to the teacher and different UI to the student based on their role   
        st.session_state.teacher_data = teacher   # so here we are setting this teacher_data session variable to the data of the currently logged in teacher, so that we can use this data to show the teacher name on the dashboard screen and also we can use this data to fetch the attendance data of that teacher from the database and then we can show that attendance data on the dashboard screen to the teacher
        st.session_state.is_logged_in = True   # so here we are setting this is_logged_in session variable to true, so that we can use this session variable to check whether any user is logged in or not in other parts of the app, so that we can show different UI to the logged in user and different UI to the non-logged in user based on their login status
        return True
    
    return False


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None    # so now it will show the home screen as for home screen login_type is set to None actually
            st.rerun()   # as here state is changing, so we need to rerun it


    # st.header('Login using password')    # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;  text-align: center'> Login using password </h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.space()    # similar to <br> tag
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='@arpitpal')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter your password")

    st.divider()    # it adds a horizontal line similar to <hr> tag


    btncol1, btncol2 = st.columns(2)

    with btncol1:
        if st.button('Login', icon=':material/passkey:',  shortcut="control+enter",  width='stretch'):
            if login_teacher(teacher_username, teacher_pass):  # here this login_teacher() function will check that the teacher with this username and password exists in the database or not, if it returns something, then it means that teacher with this username and password exists in the database, so we will set the login type to 'teacher' and then we will show a toast message "welcome back!" with a waving hand emoji and then after some time we will rerun the app, so that it will starts with the entry point of app.py and then it will check the login type and then it will show the teacher dashboard screen as for teacher login type is set to 'teacher' now
                st.toast("welcome back!", icon="👋")  # toast is actually a small notification that appears on the screen
                import time
                time.sleep(1)   # it will wait for 1 second before executing the next line of code, so that user can see the toast message for 1 second
                st.rerun()   # as here state is changing, so we need to rerun it
            else:
                st.error("Invalid username and password combo!")

    with btncol2:
        if st.button('Register Instead', type='primary',  icon=':material/passkey:',  width='stretch'):
            st.session_state.teacher_login_type = "register"


    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    # here it will check that all the fields are filled or not, if any of the field is empty, then it will return false with a message "All fields are required"
    if not teacher_username  or  not teacher_name  or  not teacher_pass  or  not teacher_pass_confirm:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):   # here this fn check_teacher_exists() will check that the teacher with this username already exists in the database or not, if it returns true, then it means that teacher with this username already exists in the database, so we will return false with a message "Username already taken"
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    # Here we need to put this create_teacher() function inside try catch block because it may throw some error if there is some problem with database connection or something else, so to handle that error, we need to put it inside try catch block
    try:
        # Here we are calling this create_teacher() function from db.py file to create a new teacher in the database with the given username, name and password, so we need to pass these parameters to that function, so that it can create a new teacher in the database with these details
        create_teacher(teacher_username, teacher_pass, teacher_name)
        # so if teacher is created successfully, then it will return true with a message "Successfully Created! Login Now"
        return True, "Successfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"



def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None    # so now it will show the home screen as for home screen login_type is set to None actually
            st.rerun()   # as here state is changing, so we need to rerun it


    # st.header('Register your teacher profile')    # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;'> Register your teacher profile </h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.space()    # similar to <br> tag
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='@arpitpal')

    teacher_name = st.text_input("Enter name", placeholder='Arpit Pal')
    
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter your password")

    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter your password")
    
    st.divider()    # it adds a horizontal line similar to <hr> tag


    btncol1, btncol2 = st.columns(2)

    with btncol1:   # since default type of button is 'secondary', so we don't need to write type='secondary' here, it will automatically consider it as secondary button
        if st.button('Register now', icon=':material/passkey:',  shortcut="control+enter",  width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)

            if success:   # if success is true, then it means that teacher is registered successfully, so we will show the success message and then after some time we will set the teacher_login_type to "login", so that it will show the login screen to the teacher, so that teacher can login with the newly created profile
                st.success(message) # it will show the success message in green color
                import time
                time.sleep(2)   # it will wait for 2 seconds before executing the next line of code, so that user can see the success message for 2 seconds
                st.session_state.teacher_login_type = "login"   # so after successful registration, it will set the teacher_login_type to "login", so that it will show the login screen to the teacher, so that teacher can login with the newly created profile
                st.rerun()   # as here state is changing, so we need to rerun it
            else:
                st.error(message)   # it will show the error message in red color

    with btncol2:
        if st.button('Login Instead', type='primary',  icon=':material/passkey:',  width='stretch'):
            st.session_state.teacher_login_type = "login"


    footer_dashboard()
