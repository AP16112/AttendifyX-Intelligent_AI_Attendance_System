# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for sharing the subject class link for the students to join

import streamlit as st

import segno   # it is used for generating QR code actually
import io   # it is used to handle the binary data
# segno is a Python library used for generating QR codes.
# io is a built-in Python module that provides tools for handling streams of data — especially binary data and text streams
# The io module gives you classes like:-
#- io.StringIO → behaves like a file but stores text in memory (useful for temporary text buffers).
#- io.BytesIO → behaves like a file but stores binary data in memory (great for images, QR codes, PDFs, etc.).

# so we can generate data (like a QR code image) and keep it in memory without writing to disk. Perfect for web apps (e.g., Streamlit, Flask, Django) where you want to send a file directly to the browser without saving it first.


@st.dialog("Share Class Link")   # here this st.dialog() is used to create a dialog box with the title "Share Class Link"
def share_subject_dialog(subject_name, subject_code):   
    app_domain = "attendifyX-main.streamlit.app"    # it means that this is our app URL or link
    join_url = f"{app_domain}/?join-code={subject_code}"    # this is the main URL or link for joining the current subject class

    # st.header("Scan to Join")     # it just uses the default h2 tag 
    # ---------OR------------
    st.markdown(f"""
        <div style='display: flex;  align-items: center;  justify-content: center;'>
            <h2 style='color: #1e1e1e;  text-align: center'>Scan to Join</h2>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    # Generate a QR code object from the given URL/string
    qr = segno.make(join_url)

    # Create an in‑memory binary stream (acts like a file, but stored in RAM)
    out = io.BytesIO()

    # Save the QR code into the binary stream as a PNG image
    # - kind='png' → output format is PNG
    # - scale=10   → controls the size (each QR module is 10 pixels)
    # - border=1   → sets the border thickness around the QR code
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')

        # Show the join_url value inside a styled code block
        # language="text" ensures it is displayed as plain text without syntax highlighting
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    with col2:
        st.markdown('### Scan to Join')
        # Display the QR code image in the Streamlit app
        # out.getvalue() retrieves the raw PNG bytes from the in‑memory buffer (BytesIO)
        # width='stretch' makes the image scale to fit the column/container width
        # caption adds a descriptive label below the image
        st.image(out.getvalue(), width='stretch', caption='QR CODE for class joining')





