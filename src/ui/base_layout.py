# This ui folder will be used to store files in which we define the UI for this project
# So this 'base_layout.py' will contains the CSS custom styling which we want & we will override the streamlit default styling with this
# And it will contains all the UI which we want for this project & which will override the custom UI of streamlit


import streamlit as st


def style_background_home():

    # here we will define the custom css styling for our project
    st.markdown("""
        <style>
            .stApp {
                background: #5865F2 !important; 
            }
                
            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important
            }
                
        </style>
        """,
        unsafe_allow_html=True
    )
    # here this .stApp { ... } → Targets the main Streamlit app container (the root div of default streamlit).
    # background: #5865F2 !important; → Sets the background color to a custom shade (Discord‑like purple). The !important ensures it overrides Streamlit’s default styling.
    # .stApp → the root container of your Streamlit app.
    # div[data-testid="stColumn"] → selects any <div> element with the attribute data-testid="stColumn".
    # Streamlit internally uses data-testid attributes to mark components for testing and layout.
    # In this case, it marks each column created by st.columns().
    # So this selector lets you apply custom styles directly to columns in your layout.


def style_background_dashboard():

    # here we will define the custom css styling for our project
    st.markdown("""
        <style>
            /* Here this .stApp is actually the class name of the root container div of streamlit & here we are applying custom styling for that */
            .stApp {
                background: #E0E3FF !important; 
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():

    # here we will define the custom css styling for our project
    st.markdown("""
        <style>
            /*Here we are importing some font-style from google font to use in this project*/
            /*We will use this font for headings.*/
            @import url('https://fonts.googleapis.com/css2?family=Fugaz+One&display=swap');
            /*We will use this font for remaining body of our project.*/
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            /* Hide Top Bar of streamlit */
            #MainMenu, footer, header {
                visibility: hidden;
            }   
             
            .block-container {
                padding-top: 1.5rem !important;
            }
                
            /*Now for these deault h1 tags which are used in heading, we will use our custom font-style from google fonts*/
            /*In streamlit actually, st.title() uses <h1> tags internally, st.header("...") uses <h2> tag, st.subheader("...") uses <h3> tags actually*/
            
            /*Now we will override the font-style for default h3, h4, p, tags of streamlit*/
            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;
            }
                
            h1{
                font-family: 'Fugaz One', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important
                margin-bottom: 0rem !important;
            }
                
            h2 {
                font-family: 'Fugaz One', sans-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important
                margin-bottom: 0rem !important;
            }
                
                
            /*Now we will give custom styling for primary, secondary and tertiary type buttons of streamlit*/
            /*So to select the any type of default button of streamlit, we need to write this way i.e by using kind="" */
            /*  OR  button[kind="primary"] {  */
            button {             /* applies to ALL buttons */  
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important; 
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
                
            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important; 
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
                
            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: black !important; 
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
                
            button:hover {
                transform: scale(1.05);
            }
                
            div[data-testid="stSelectbox"] label {
                color: black !important;
            }
                
            /* Target the label of text_input */
            div[data-testid="stTextInput"] label {
                color: black !important;
            }
                
            /* Target the label above the camera input */
            div[data-testid="stCameraInput"] label {
                color: black !important;
            }

            /* Target the instruction text inside the camera input */
            div[data-testid="stCameraInput"] div[data-testid="stMarkdownContainer"] p {
                color: black !important;
            }
                        
        </style>
        """,
        unsafe_allow_html=True
    )
    # MainMenu, footer, header { visibility: hidden; } → Targets Streamlit’s built‑in UI elements:
    # MainMenu → the hamburger menu in the top‑right corner.
    # footer → the “Made with Streamlit” footer.
    # header → the default app header.
    # visibility: hidden; → Hides those elements from view but keeps their space reserved in the layout.
    # .block-container → This is the main content container class in Streamlit. Everything you render (titles, widgets, charts) sits inside this container.
