# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the header components for all the pages

import streamlit as st

# Here this fn will define the header for home page only
def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    # Here we will define the logo of our app and its title i.e "AttendifyX"
    st.markdown(f"""
        <div style='display: flex;  flex-direction: column;  align-items: center;  justify-content: center;  margin-bottom: 30px; margin-top: 30px; '>
            <img src='{logo_url}'  style='height:100px'>
            <h1 style='text-align: center;  color: #E0E3FF;'>AttendifyX</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Here in this img src='{logo_url}'> we need to write {logo_url} inside quotes because logo_url will give the string value without quotes but we want value in src inside quotes like src="" 
    # Here if we write this <img> tag for logo directly inside the st.markdown() without writing this inside div, then it will not show the logo image & instead just show the text
    # Streamlit’s st.markdown(..., unsafe_allow_html=True) still places your HTML inside a Markdown container (<div data-testid="stMarkdownContainer">).
    # If you only write <img src="..."> without wrapping it, Streamlit’s default CSS sometimes treats it like inline text, and the image can collapse or not display properly depending on spacing.
    # When you wrap it in a <div> with flex or block styling, you’re explicitly telling the browser: “Render this as a block element, center it, and give it space.” That’s why it shows up correctly.


# Here this fn will define the header for dashboard page only
def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    # Here we will define the logo of our app and its title i.e "AttendifyX"
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;   gap: 10px;'>
            <img src='{logo_url}'  style='height:85px'>
            <h2 style='display:flex; text-align: left; justify-content: center; color: #5865F2;'>AttendifyX</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Here in this img src='{logo_url}'> we need to write {logo_url} inside quotes because logo_url will give the string value without quotes but we want value in src inside quotes like src="" 