# Here in this pipelines folder, we will write the code for all the pipelines of our project like face recognition pipeline, voice recognition pipeline, etc.

# Here this is the voice recognition pipeline for our project, so here we will write the code for voice recognition pipeline which will be used for marking attendance of students using voice recognition.

# Here we will use librosa and resemblyzer library for voice recognition in our project, so here we will import these libraries and then we will write the code for voice recognition pipeline using these libraries.
# So librosa is used for audio processing i.e editing the audio files, converting them into segments, noice reduction etc, while resemblyzer is used to convert the audio files into embeddings and then comparing those embeddings to check that two audio files are of same person or not, so both these libraries are used together for voice recognition in our project

from resemblyzer import VoiceEncoder, preprocess_wav
# Here this VoiceEncoder is used to convert the audio files into embeddings, which are basically numerical representations of the audio files, and then we can compare these embeddings to check that two audio files are of same person or not, while this preprocess_wav is used to preprocess the audio files before converting them into embeddings, it will do some basic preprocessing like resampling the audio file to a specific sample rate, converting it to mono channel etc, so that we can get better embeddings from the audio files.
# And this preprocess_wav() function will take the path of the audio file as input and will return the preprocessed audio file in the form of a numpy array, which we can then pass to the VoiceEncoder to get the embeddings of that audio file.

import numpy as np
import io  # it is used to convert the audio file into bytes format, so that we can pass it to the preprocess_wav() function, because this function expects the audio file to be in bytes format.
# this io performs the same task which pillow library does for image files, it converts the audio file into bytes format, so that we can pass it to the preprocess_wav() function, because this function expects the audio file to be in bytes format.

import librosa
import streamlit as st



# As load_voice_encoder() is a time consuming process, so we will use streamlit's cache_resource decorator to cache the result of this function, so that we don't have to load the voice encoder every time we want to use it, and it will improve the performance of our app.
@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()  # it will return the instance of the VoiceEncoder class, which we can use to convert the audio files into embeddings


# audio_bytes is the audio file in bytes format (i.e binary format), which we will get from the file uploader in streamlit, so we need to convert this audio file from bytes format to numpy array format, so that we can pass it to the preprocess_wav() function, because this function expects the audio file to be in bytes format.
def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()  # it will return the instance of the VoiceEncoder class, which we can use to convert the audio files into embeddings

        # librosa returns two things on loading the audio file, first is the audio time series and second is the sample rate of the audio file, so we will store these two things in two separate variables, so that we can use them later.
        # here this io.BytesIO(audio_bytes) is used to convert the audio file from bytes format to a file-like object, which we can then pass to the librosa.load() function to load the audio file, because this function expects the audio file to be in a file-like object format.
        # And this sr=16000 is used to resample the audio file to a sample rate of 16000, because this is the sample rate that the VoiceEncoder expects, so we need to resample the audio file to this sample rate before passing it to the VoiceEncoder.
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)  # here we are loading the audio file using librosa library, and we are resampling the audio file to a sample rate of 16000, because this is the sample rate that the VoiceEncoder expects, so we need to resample the audio file to this sample rate before passing it to the VoiceEncoder.

        # Now this wav actually represent the preprocessed audio file, which we will get after passing the loaded audio file to the preprocess_wav() function, and this wav will be in the form of a numpy array, which we can then pass to the VoiceEncoder to get the embeddings of that audio file.
        wav = preprocess_wav(audio)  # here we are preprocessing the audio file using the preprocess_wav() function, which will do some basic preprocessing like resampling the audio file to a specific sample rate, converting it to mono channel etc, so that we can get better embeddings from the audio files.
        
        embedding = encoder.embed_utterance(wav) # here we are converting the preprocessed audio file into embeddings using the embed_utterance() function of the VoiceEncoder class, which will return the embeddings of that audio file in the form of a numpy array.
        # here these embeddings are of size 256, which means that each audio file will be represented by a 256-dimensional vector, which is a numerical representation of that audio file, and we can compare these embeddings to check that two audio files are of same person or not.

        return embedding.tolist()  # here we are converting the embeddings from numpy array format to list format, because we will store these embeddings in the database in list format, so we need to convert them to list format before storing them in the database.
    except Exception as e:
        st.error("Voice recognition error")
        return None



# here this fn will be used to firstly find the embedding of the given audio file using the get_voice_embedding() function, and then it will compare this embedding with the embeddings of all the students in the database to find the student whose embedding is closest to the embedding of the given audio file, and then it will return the name of that student, so that we can mark the attendance of that student.
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    # here this threshold is used to set the minimum similarity score required to consider a match between the new embedding and the stored embeddings of the students, so if the similarity score is greater than or equal to this threshold, then we will consider it as a match and return the name of that student, otherwise we will return None, which means that we couldn't identify the speaker from the given audio file.
    if new_embedding is None or not candidates_dict:   # if the new_embedding is None, which means that there was an error in getting the embedding of the given audio file, or if the candidates_dict is empty, which means that there are no students in the database to compare with, then we will return None and a similarity score of 0.0, which means that we couldn't identify the speaker from the given audio file.
        return None, 0.0
    
    best_sid = None    # i.e best student id
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            # here this np.dot() is used to calculate the cosine similarity between the new embedding and the stored embedding of the student, which will give us a similarity score between -1 and 1, where 1 means that the two embeddings are exactly the same, 0 means that the two embeddings are orthogonal to each other, and -1 means that the two embeddings are opposite to each other, so the higher the similarity score, the more similar the two embeddings are, and we will consider it as a match if the similarity score is greater than or equal to the threshold that we have set.
            similarity =  np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    # Now if the best_score is greater than or equal to the threshold, then we will return the name of that student, which we can get from the candidates_dict using the best_sid, otherwise we will return None, which means that we couldn't identify the speaker from the given audio file.
    # so when we get the best_score >= threshold, then it means that we have found a match between the new embedding and the stored embedding of the student, which means that we have identified the speaker from the given audio file, so we will return the name of that student, which we can get from the candidates_dict using the best_sid, otherwise we will return None, which means that we couldn't identify the speaker from the given audio file.
    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score
    


# THis fn will be used to process the bulk audio file uploaded by the user, so here we will take the bulk audio file as input, and then we will split this bulk audio file into segments, and then we will get the embedding of each segment using the get_voice_embedding() function, and then we will return a list of embeddings for all the segments of the bulk audio file, so that we can compare these embeddings with the stored embeddings of the students in the database to find the students whose embeddings are closest to the embeddings of the segments of the bulk audio file, and then we can mark the attendance of those students.
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    # here we will use try except block to catch any error that may occur while processing the bulk audio file, because there can be many errors that can occur while processing the bulk audio file, like error in loading the audio file, error in splitting the audio file into segments, error in getting the embedding of the segments etc, so we will use try except block to catch these errors and display an error message to the user, so that they can understand that there was an error in processing the bulk audio file and they can try again with a different audio file or they can check their audio file for any issues.
    try:
        encoder = load_voice_encoder()  # it will return the instance of the VoiceEncoder class, which we can use to convert the audio files into embeddings

        # librosa returns two things on loading the audio file, first is the audio time series and second is the sample rate of the audio file, so we will store these two things in two separate variables, so that we can use them later.
        # here this io.BytesIO(audio_bytes) is used to convert the audio file from bytes format to a file-like object, which we can then pass to the librosa.load() function to load the audio file, because this function expects the audio file to be in a file-like object format.
        # And this sr=16000 is used to resample the audio file to a sample rate of 16000, because this is the sample rate that the VoiceEncoder expects, so we need to resample the audio file to this sample rate before passing it to the VoiceEncoder.
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)  # here we are loading the audio file using librosa library, and we are resampling the audio file to a sample rate of 16000, because this is the sample rate that the VoiceEncoder expects, so we need to resample the audio file to this sample rate before passing it to the VoiceEncoder.

        # Now as our audio is very large like audio of 50 students speaking together, so it will be difficult to get the embedding of the whole audio file at once, because the VoiceEncoder can only process audio files of a certain length, so we will split this bulk audio file into segments, and then we will get the embedding of each segment using the get_voice_embedding() function, and then we will return a list of embeddings for all the segments of the bulk audio file, so that we can compare these embeddings with the stored embeddings of the students in the database to find the students whose embeddings are closest to the embeddings of the segments of the bulk audio file, and then we can mark the attendance of those students.
        segments = librosa.effects.split(audio, top_db=30)  # here we are splitting the audio file into segments using the split() function of the librosa library, which will split the audio file into segments based on the silence in the audio file, so it will return a list of segments, where each segment is represented by a tuple of start and end time of that segment in the audio file, and we are using top_db=20 to set the threshold for silence detection, which means that any segment of the audio file that has a volume less than 20 dB will be considered as silence and will be used to split the audio file into segments.
        # top_db is a parameter that is used to set the threshold for silence detection, which means that any segment of the audio file that has a volume less than the value of top_db will be considered as silence and will be used to split the audio file into segments, so the higher the value of top_db, the more segments will be created from the audio file, and the lower the value of top_db, the fewer segments will be created from the audio file. Generally 30 is ideal range.

        identified_results = {}

        for start, end in segments:
            # if the segment is less than 0.5 seconds, then we will ignore that segment, because it will not contain enough information to get a good embedding of that segment, and it can also be a noise or a very short speech, which can lead to false positives in speaker identification, so we will ignore such short segments and we will only consider segments that are at least 0.5 seconds long, which means that they will contain enough information to get a good embedding of that segment and they will also be more likely to contain actual speech rather than noise or very short speech.
            if (end-start) < sr * 0.5: 
                continue   # here this (end-start) < sr * 0.5 means that if the duration of the segment is less than sample rate (sr) multiplied by 0.5 seconds, which means that the segment is less than 0.5 seconds long, then we will ignore that segment and we will continue to the next segment in the loop.

            segment_audio = audio[start:end]  # here we are extracting the audio of the segment from the original audio file using the start and end time of that segment, which we got from the segments list, so we will use these start and end time to slice the original audio file and get the audio of that segment, which we can then pass to the preprocess_wav() function to get the preprocessed audio of that segment, and then we can pass that preprocessed audio to the VoiceEncoder to get the embedding of that segment.
            wav = preprocess_wav(segment_audio)  # here we are preprocessing the audio of the segment using the preprocess_wav() function, which will do some basic preprocessing like resampling the audio file to a specific sample rate, converting it to mono channel etc, so that we can get better embeddings from the audio files.

            embedding = encoder.embed_utterance(wav) # here we are converting the preprocessed audio of the segment into embeddings using the embed_utterance() function of the VoiceEncoder class, which will return the embeddings of that segment in the form of a numpy array.

            sid, score = identify_speaker(embedding, candidates_dict, threshold)  # here we are identifying the speaker of that segment by comparing the embedding of that segment with the stored embeddings of the students in the database using the identify_speaker() function, which will return the name of the student whose embedding is closest to the embedding of that segment, and it will also return the similarity score between the embedding of that segment and the stored embedding of that student, so we can use this similarity score to check whether we have identified the speaker correctly or not, because if the similarity score is greater than or equal to the threshold that we have set, then we can consider it as a match and we can mark the attendance of that student, otherwise we will ignore that segment and we will not mark the attendance of any student for that segment.

            if sid:
                if sid not in identified_results or score > identified_results[sid]:  # here we are checking if the student id (sid) is not already in the identified_results dictionary, which means that we have not identified that student for any previous segment, or if the similarity score (score) for that student is greater than the previously stored similarity score for that student in the identified_results dictionary, which means that we have found a better match for that student in the current segment compared to the previous segments, then we will update the identified_results dictionary with the current student id (sid) and the current similarity score (score), so that we can keep track of the best match for each student across all the segments of the bulk audio file.
                    identified_results[sid] = score

        return identified_results  # here we are returning the identified_results dictionary, which will contain the student ids as keys and their corresponding similarity scores as values, which means that these are the students that we have identified from the bulk audio file along with their similarity scores, so we can use this information to mark the attendance of those students in our app.
    except Exception as e:
        st.error("Bulk process error")
        return {}
