# Here Inside this src folder, we write all our project source code actually
# This components folder will contains all the components required in our project

# Here this file contains the dialog for entering the voices of the classroom for voice attendance

import streamlit as st

from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project
from src.pipelines.voice_pipeline import process_bulk_audio
from src.components.dialog_attendance_results import show_attendance_result

import pandas as pd
from datetime import datetime


@st.dialog("Voice Attendance")   
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of students saying 'I am present'. Then AI will recognize the students")  

    audio_data = None     # at first we are assuming this audio data to be none

    audio_data = st.audio_input("Record classroom audio")    # it will take the classroom audio as input

    if st.button('Analyze Audio', width='stretch', type='primary'):
        # here we are adding this spinner till processing of these audio voices is happening
        with st.spinner("Processing Audio data..."):
            # it will give all the students enrolled in this current subject
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            # Query the 'subject_students' table and also join related data from the 'subjects' table.
            # select('*, subjects(*)') → fetches all columns from subject_students (*) and expands the subjects table (*) for each matching record
            # eq('subject_id', selected_subject_id) → filters rows so only those belonging to the given selected_subject_id are returned

            enrolled_students = enrolled_res.data    # it will give all the students enrolled in this subject

            if not enrolled_students:   # no students present for this subject
                st.warning("No students enrolled in this cource")
                return   # it will stop the further flow because no enrolled students found
            
            # But if enrolled students found for this subject, then we will create this dict
            # here in this dictionary, we are builing the lookup table of student IDs → voice embeddings.
            # here this "if s['students'].get('voice_embedding')" → ensures we only include those students who actually have a voice embedding stored or registered in database while student registration (avoids None values).
            candidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding'] for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidates_dict:   # it means that no enrolled student had registered their voice 
                st.error('No enrolled students have voice profiles registered')
                return   # to stop the flow
            
            # but if enrolled students have their voice registered, then we will take the audio bytes
            audio_bytes = audio_data.read()    # # Read the uploaded audio file into memory as raw ninary bytes. This will be used for further decoding or embedding extraction.

            # THis fn will be used to process the bulk audio file uploaded by the user, so here we will take the bulk audio file as input, and then we will split this bulk audio file into segments, and then we will get the embedding of each segment using the get_voice_embedding() function, and then we will return a list of embeddings for all the segments of the bulk audio file, so that we can compare these embeddings with the stored embeddings of the students in the database to find the students whose embeddings are closest to the embeddings of the segments of the bulk audio file, and then we can mark the attendance of those students.
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)      # here we are not passing the threshold value as we are taking the default threshold value here 

            # currently we are taking both to me empty
            results, attendance_to_log = [], []

            # it is used to mark the timestamp for attendace taken
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            # Here datetime.now() → gets the current local date and time.
            # And .strftime(...) → converts it into a formatted string.
            # %Y → 4‑digit year (e.g., 2026).
            # %m → 2‑digit month. And %d → 2‑digit day.
            # T → literal character T (common in ISO 8601 formats).
            # %H:%M:%S → hour, minute, second in 24‑hour format.

            for node in enrolled_students:
                # Each node represents an enrollment record for this subject.
                # The 'students' field inside node contains the actual student details.
                student = node['students']

                # Retrieve the detection score for this student_id.
                # Returns a float score if found, or 0.0 if the student was not detected.
                score = detected_scores.get(int(student['student_id']), 0.0)

                is_present = bool(score > 0)    # if score > 0, then it means that this student is present

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Source": score if is_present else "-",       #If the student was detected (is_present == True), it will show its audio score and If not detected, store a dash ("-") to indicate absence.
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })


            # Now we will store this result of voice attendance in a session state in the form of dataframe & also we will the store attendance_to_log in that state also in the form of tuple containing two values
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    # Now if we found this voice_attendance_results state inside the session state, then we will show the result
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        # now we will take the results & log out from this
        df_results, logs = st.session_state.voice_attendance_results

        show_attendance_result(df_results, logs)
              







