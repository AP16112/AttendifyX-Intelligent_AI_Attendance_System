# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the header components for all the pages

import streamlit as st

# Here this fn will define the header for home page only
def header_home():
    # st.header("AttendifyX")
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    # Here we will define the logo of our app and its title i.e "AttendifyX"
    st.markdown(f"""
        <div style='display: flex;  flex-direction: column;  align-items: center;  justify-content: center;  margin-bottom: 30px; margin-top: 30px; '>
            <img src='{logo_url}'  style='height:100px'>
            <h1 style='text-align: center;  color: #E0E3FF;'> AttendifyX </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Here in this img src='{logo_url}'> we need to write {logo_url} inside quotes because logo_url will give the string value without quotes but we want value in src inside quotes like src="" 