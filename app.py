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

from src.components.dialog_auto_enroll import auto_enroll_dialog


def main():
    st.set_page_config(
        page_title="AttendifyX : Intelligent AI Attendance System",     # page_title sets the browser tab title
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",        # small icon visible before this page_title
    )

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


    # st.query_params → gives you access to the query parameters in the app’s URL (like ?join-code=12345).
    # .get('join-code') → fetches the value associated with the key "join-code" if it exists.
    join_code = st.query_params.get('join-code')

    if join_code:   # it this exists, then it means that someone is trying to enroll in this subject using this URL
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        
        #  If the user is logged in and their role is 'student', automatically trigger the enrollment dialog using the join_code (extracted from the URL query parameters). This enables deep-link enrollment so students can join directly via a shared link.
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)


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

# Supabase itself is not a database but it provides the instance of p sql i.e (PostgreSQL) database to the developers, so that they can use that database for their projects without worrying about the backend part of it. It also provides some other features like authentication, APIs, storage, real-time features, etc which are required in the backend of any project, so that developers can focus on the frontend part of their project and can easily integrate this supabase with their frontend without worrying about the backend part of it.
# PostgreSQL and MySQL are almost same but PostgreSQL is more advanced and has more features than MySQL, so it is more preferred by developers. Supabase provides the instance of PostgreSQL database to the developers, so that they can use that database for their projects without worrying about the backend part of it. It also provides some other features like authentication, APIs, storage, real-time features, etc which are required in the backend of any project, so that developers can focus on the frontend part of their project and can easily integrate this supabase with their frontend without worrying about the backend part of it.


# Core Features of Supabase :-
# Postgres Database  :- Every project comes with a full PostgreSQL instance, one of the most trusted relational databases.
# Authentication  :- Built‑in user sign‑ups and logins with support for email, OAuth, and Row Level Security (RLS).
# Instant APIs  :- Auto‑generated REST and GraphQL APIs for your database tables.
# Realtime Subscriptions  :- Enables live data sync for apps like chat, dashboards, or multiplayer games.
# Edge Functions  :- Serverless functions you can deploy without managing infrastructure.
# Storage  :- Manage and serve large files (images, videos, documents).
# Vector Embeddings  :- Store and query ML embeddings for AI applications (integrates with OpenAI, Hugging Face, LangChain).


# JSONB format in PostgreSQL :-
# JSONB is a data type in PostgreSQL that allows you to store JSON (JavaScript Object Notation) data in a binary format. It provides efficient storage and querying capabilities for JSON data, making it ideal for applications that need to handle semi-structured or unstructured data. With JSONB, you can easily store and manipulate complex data structures without needing to define a rigid schema, while still benefiting from indexing and fast access.
# JSONB is a PostgreSQL data type that stores JSON (JavaScript Object Notation) data in a binary format rather than plain text.



# To run any streamlit application , we use this :-
# streamlit run your_script.py
# Here we will use this :- streamlit run app.py