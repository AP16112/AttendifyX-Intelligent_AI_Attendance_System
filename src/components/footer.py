# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project like header or footer etc.

# Here this file contains the footer component for all the pages

import streamlit as st

# Here this fn will define the footer for home page only
def footer_home():

    st.markdown("""
        <div style='margin-top: 4rem;  display: flex;  gap: 6px;  justify-content: center;  align-items: center;'>
            <p style='font-weight: bold;  color: white;'> Created with ❤️ by </p>
            <p style='font-weight: 900;  font-size: 20px;  color: yellow;'>Arpit Pal </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Here this fn will define the footer for dashboard page only
def footer_dashboard():

    st.markdown("""
        <div style='margin-top: 4rem;  display: flex;  gap: 6px;  justify-content: center;  align-items: center;'>
            <p style='font-weight: bold;  color: black;'> Created with ❤️ by </p>
            <p style='font-weight: 900;  font-size: 20px;  color: #FF8C00;'>Arpit Pal </p>
        </div>
        """,
        unsafe_allow_html=True
    )