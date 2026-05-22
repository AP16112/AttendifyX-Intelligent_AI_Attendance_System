# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the subject card which we can use any no. of times

import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    # Triple quotes are SAFE here because we are just assigning to a variable.
    # Streamlit hasn't parsed anything yet — this is just a plain Python string assignment.
    html = f"""
        <div  style="background-color: white;  border-left: 8px solid #EB459E;  padding: 25px;  border-radius: 20px;  border: 1px solid black; margin-bottom:20px;">
            <h3 style="margin:0;  color: #1e293b; font-size: 1.5rem; ">{name}</h3>
            <p style="color: #64748b; margin: 10px 0;">
                Code :
                <span style="background-color: #E0E3FF; color: #5865F2; padding: 2px 8px; border-radius: 5px;">
                    {code}
                </span>
                | Section : {section}
            </p>
        """

    if stats:   # if stats exists
        # STREAMLIT MARKDOWN TRAP — Always use single-line strings with html +=
        # When you use triple quotes (""") with html +=, the indentation inside the triple quotes gets embedded mid-string, like this:
        #   html = "<div>...</div>
        #       <div style='flex'>    ← 4 leading spaces injected here!
        #   "
        # Streamlit's markdown parser sees those 4 leading spaces and treats
        # that line as a <code> block (standard Markdown rule: 4 spaces = code),
        # so your HTML tag gets displayed as raw text instead of being rendered.
        # WRONG — triple quotes on html += embed indentation → shows as code block:
        #   html += """
        #       <div style="display: flex;">   ← printed as text, not rendered!
        #   """
        # CORRECT — single-line strings have no leading whitespace → renders as HTML:
        #   html += '<div style="display: flex;">'
        html += '<div style="display: flex;  gap: 8px; flex-wrap: wrap;">'

        for icon, label, value in stats:
            html += f'<div style="background-color: #EB459E10; padding:5px 12px; border-radius: 12px; font-size: 0.9rem;">{icon} <b>{value}</b> {label} </div>'

        html += "</div>"

    html += "</div>"    #closes the outer card container


    # Now we are passing this html string to the markdown here, so that it will be rendered as html string and not normal string
    # so that after rendering, we will be able to see the content with proper html & not just the string like here
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()       # here we are actually rendering this footer_callback i.e we are calling it here
        # so this will actually call the share btn fn which will show the share btn actually