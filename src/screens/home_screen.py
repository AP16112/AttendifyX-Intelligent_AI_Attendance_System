# This is Home page.

import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():

    header_home()

    # This will override the default styling of streamlit with this custom styling
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")

        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png",  width=120)

        # So when only this button is clicked, this 'login_type' session variable will get set to 'student'
        if st.button('Student Portal', type='primary',  icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()  # so after setting the login type, we are also rerunning the app


    with col2:
        st.header("I'm Teacher")

        # Another way to add image is by using st.image() instead of using st.markdown() & then writing html in that.
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png",  width=145)

        # So when only this button is clicked, this 'login_type' session variable will get set to 'teacher'
        # Here material refers to Material Symbols, which are Google’s official Material Design icon set.
        # Streamlit supports icons from Material Symbols and Emoji shortcodes. You specify them with the icon argument using the :material/...: format.
        if st.button('Teacher Portal', type='primary',  icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()  # so after setting the login type, we are also rerunning the app


    # Here we are adding the footer using this fn for home page
    footer_home()