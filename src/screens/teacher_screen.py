# Here Inside this src folder, we write all our project source code actually
# This screens folder contains the screens or webpages for teachers, student and home page

# This is teacher login page.

import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import  style_base_layout, style_background_dashboard


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    # Now we will create a session state variable for login which will show what is the type of teacher login
    if 'teacher_login_type' not in st.session_state  or  st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()
    



def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

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
        st.button('Login', icon=':material/passkey:',  shortcut="control+enter",  width='stretch')

    with btncol2:
        if st.button('Register Instead', type='primary',  icon=':material/passkey:',  width='stretch'):
            st.session_state.teacher_login_type = "register"


    footer_dashboard()



def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

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

    with btncol1:
        st.button('Register now', icon=':material/passkey:',  shortcut="control+enter",  width='stretch')

    with btncol2:
        if st.button('Login Instead', type='primary',  icon=':material/passkey:',  width='stretch'):
            st.session_state.teacher_login_type = "login"


    footer_dashboard()