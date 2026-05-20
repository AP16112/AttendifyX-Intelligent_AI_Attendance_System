# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Project Name  :- "AttendifyX : Intelligent AI Attendance System"
# It uses face and voice recognition for marking whether user is present or not.

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Here we will use this app.py file to write out streamlit deployment code here
# Actually Streamlit wants some entry point and this app.py is actually acting as the entry point for this project

# Streamlit is an open‑source Python framework designed to make it easy to build and share data apps, dashboards, and interactive machine learning demos with just a few lines of code.

# What Streamlit does :-
# - Lets you turn a Python script into a web app instantly.
# - Focuses on simplicity — you don’t need HTML, CSS, or JavaScript.
# - Perfect for data scientists, ML engineers, and analysts who want to showcase models or visualizations interactively.

# Key Features :-
# - Widgets: Sliders, buttons, text inputs, file uploaders.
# - Charts: Native support for Matplotlib, Plotly, Altair, and more.
# - Live updates: Apps auto‑refresh when you change code.
# - Deployment: Easy to share via Streamlit Cloud or run locally.

import streamlit as st

# Here we are importing these functions from these python files, so that we can use those functions here
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen 


def main():
    # Initialization of session store
    # Check if 'key' i.e here 'login_type' already exists in session_state
    # If not, then initialize it because by-default this session_state is empty like a blank dictionary i.e session_state={}, so we need to initialize it with some key-value pair before using it
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    # ----------------OR-----------------
    # Session State also supports the attribute based syntax
    # if 'login_type' not in st.session_state:
    #     st.session_state.login_type = 'value'


    # It is just like the switch statement of Java
    match st.session_state['login_type']:
        case 'teacher':
            # print("Teacher")
            teacher_screen()  # it will render the teacher screen

        case 'student':
            student_screen()  # it will render the student screen

        case None:
            home_screen()    # it will render the home screen


main()




# def main():
#     st.header("This is title")
#     name = st.text_input("Enter your name")

#     # st.button("Display my name", type='primary')
#     # st.button("Display my name", type='primary')  # it will show error
#     # If two buttons are of same name & of same type, then it will show error because streamlit got confused
#     # So we need to provide some different 'key' to each of these buttons to differentiate them
#     # st.button("Display my name", type='primary' , key="btn1")
#     # st.button("Display my name", type='primary', key="btn2")
#     # st.button("Display my name", type='secondary', key="btn3")

#     # All these buttons will be one after the another
#     if st.button("Hi", type='primary' , key="btn1", width=300):
#         print("hi,", name)

#     if st.button("Hi", type='primary' , key="btn2", width='stretch'):
#         print("hi,", name)

#     if st.button("Hi", type='primary' , key="btn3", width='content'):
#         print("hi,", name)

#     if st.button("Bye", type='secondary' , key="btn4", width='stretch'):
#         print("bye,", name)

#     # But we want more than 1 buttons to be in same row, we can make use of columns
#     # col1, col2 = st.columns(2)   # it will create two columns in the same row
#     # But if we want to change gap betweens these columns, we can use gap=""
#     col1, col2 = st.columns(2, gap="xlarge")   # it will create two columns in the same row


#     with col1:    # now this button will be under the col1 
#         if st.button("Hi", type='primary' , key="btn5", width='stretch'):
#             print("hi,", name)

#     with col2:    # now this button will be under the col2 
#         if st.button("bye", type='secondary' , key="btn6", width='stretch'):
#             print("bye,", name)


#     # It will show this text in markdown format & for this we can use '', or "" or """""".
#     st.markdown("""
#         Hi
#     """)

#     # In Streamlit, the st.markdown() function has an optional parameter called unsafe_allow_html.
#     # By default, Streamlit sanitizes Markdown so that raw HTML tags won’t render (to prevent injection issues). If you want to embed HTML directly, you need to set:
#     st.markdown(
#         "<h1 style='color:blue;'>Hello AttendifyX</h1>",
#         unsafe_allow_html=True
#     )

#     st.markdown("""
#         <div>
#                 <a href="#">Home</a>
#                 <h1>AttendifyX</h1>
#         </div>
#     """, unsafe_allow_html=True
#     )

#     # Using markdown, we can also provide custom styling to streamlit items like buttons, etc
#     st.markdown("""
#         <style>
#                 button {
#                     background-color: orange !important;
#                 }
#         </style>   
#     """,    # here this !important will override the streamlit styling with this custom styling
#     unsafe_allow_html=True
#     )


# main()



# Statefulness :-
# In Streamlit, statefulness refers to how the app remembers values or data across reruns.
# By default, Streamlit apps are stateless: every time a user interacts with a widget (like a button or slider), the script reruns from top to bottom, and variables reset. This makes apps simple but can be frustrating if you want to preserve information between interactions.

# How Streamlit Handles State :-
# Stateless reruns: Each interaction triggers a full rerun of the script.
# Session State: Streamlit provides st.session_state to store values that persist across reruns.
# Widget State: Widgets (like st.text_input, st.slider) automatically save their current value in st.session_state.

# Statefulness lets you build interactive apps that remember user choices, cache results, or maintain progress.


# Supabase :-
# We will use this as database here.
# Supabase is an open‑source backend platform built on PostgreSQL that provides developers with a ready‑to‑use database, authentication, APIs, storage, and real‑time features — essentially a Firebase alternative but powered by Postgres. 
# It’s designed to let you spin up a backend in minutes and scale to millions of users without managing servers.


# Core Features of Supabase :-
# Postgres Database  :- Every project comes with a full PostgreSQL instance, one of the most trusted relational databases.
# Authentication  :- Built‑in user sign‑ups and logins with support for email, OAuth, and Row Level Security (RLS).
# Instant APIs  :- Auto‑generated REST and GraphQL APIs for your database tables.
# Realtime Subscriptions  :- Enables live data sync for apps like chat, dashboards, or multiplayer games.
# Edge Functions  :- Serverless functions you can deploy without managing infrastructure.
# Storage  :- Manage and serve large files (images, videos, documents).
# Vector Embeddings  :- Store and query ML embeddings for AI applications (integrates with OpenAI, Hugging Face, LangChain).





# To run any streamlit application , we use this :-
# streamlit run your_script.py
# Here we will use this :- streamlit run app.py