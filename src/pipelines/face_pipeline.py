# Here in this pipelines folder, we will write the code for all the pipelines of our project like face recognition pipeline, voice recognition pipeline, etc.

# Here this is the face recognition pipeline for our project, so here we will write the code for face recognition pipeline which will be used for marking attendance of students using facial recognition, so here we will use the face_recognition library of python which is a simple and easy to use library for face recognition in python, so here we will write the code for face recognition pipeline using this library, so that we can use this pipeline in our project for marking attendance of students using facial recognition.

# Basec Face Recognition Pipeline steps :- 

# So here we will firstly take the Face Image as input
#                   |
#                   |
#                   V
#           Face Detector (using dlib)  --> it just draw the rectangular box around the face and then it will give the coordinates of that rectangular box, so that we can use those coordinates to crop the face from the image and then we can use that cropped face for further processing in the pipeline, so here we will use dlib library for face detection in our project, so here we will write the code for face detection using dlib library in this face_pipeline.py file, so that we can use that code for face detection in our project for marking attendance of students using facial recognition.
#                   |
#                   |   
#                   V
#           (sp) Shape Predictor (detecting 68 landmarks of face) --> landmarks of face like eyes, nose, mouth, etc.
#                   |
#                   |
#                   V
#           ResNet Model (facerec i.e face recognizer model - for generating the face embeddings)  --> embeddings (128D)   [feature extractor]
#           And this 128 dimension embeddings vector will be stored in the database for each student and then when student will take the attendance using facial recognition, then we will generate the embeddings vector for the image taken from camera input and then we will compare that embeddings vector with the embeddings vector stored in the database for each student and if we find a match, then we will mark the attendance of that student.
#                   |
#                   |
#                   V
#           128D embedding (face descriptor)
#                   |
#                   |
#                   V
#           SVM (classifier)  --> it will classify the face based on the embeddings vector and will give the output as the name of the student whose face is matched with the embeddings vector stored in the database, so here we will use SVM classifier for classifying the face based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
#                   |
#                   |
#                   V
#               Student ID


import dlib
import numpy as np
import face_recognition_models

from sklearn.svm import SVC 

import streamlit as st

# here we are importing all the students (i.e their faces), so that we can train our SVM classifier model on those
from src.database.db import get_all_students



# As this load_dlib_models() function will load the dlib models for face detection, shape prediction and face recognition, so it is a time consuming process, so we will use the @st.cache_resource decorator of streamlit to cache the output of this function, so that it will not load the dlib models again and again every time we call this function, instead it will load the dlib models only once and then it will cache the output of this function,
# so that when we call this function again, it will return the cached output instead of loading the dlib models again, which will save a lot of time and will improve the performance of our app.
@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()  # this will load the dlib's frontal face detector model, which is used for detecting the faces in the image, so here we will use this detector for detecting the faces in the image taken from camera input for facial recognition and attendance marking
    # so this detector will actually return the coordinates of the rectangular box drawn around the face detected in the image, so that we can use those coordinates to crop the face from the image and then we can use that cropped face for further processing in the pipeline, so here we will use this detector for detecting the faces in the image taken from camera input for facial recognition and attendance marking
    
    # here sp means shape predictor, which is used for detecting the landmarks of the face like eyes, nose, mouth, etc. and these landmarks are used for aligning the face before generating the embeddings vector for that face, so here we will load the shape predictor model of dlib library using this face_recognition_models package which provides pre-trained models for face recognition tasks, so here we will use the shape predictor model from this package for detecting the landmarks of the face in our project for marking attendance of students using facial recognition.
    sp = dlib.shape_predictor(       # this shape_predictor will actually requires a model for that we will use this pose_predictor_model_location() function of face_recognition_models which gives the location of the landmarks of our face.
        face_recognition_models.pose_predictor_model_location()
    )

    # here facerec means face recognizer model, which is used for generating the embeddings vector for the face, so here we will load the face recognizer model of dlib library using this face_recognition_models package which provides pre-trained models for face recognition tasks, so here we will use the face recognizer model from this package for generating the embeddings vector for the face in our project for marking attendance of students using facial recognition.
    facerec = dlib.face_recognition_model_v1(   # this face_recognition_model_v1() function will actually requires a model for that we will use this face_recognition_model_location() function of face_recognition_models which gives the location of the model for generating the embeddings vector for the face.
        face_recognition_models.face_recognition_model_location()  
    ) 
    # Although this dlib.face_recognition_model_v1() can work individually also but with this face_recognition_models package, it is more optimized and it will give better performance, so here we are using this face_recognition_model_v1() function from dlib library with the model from face_recognition_models package for generating the embeddings vector for the face in our project for marking attendance of students using facial recognition.

    return detector, sp, facerec




def get_face_embeddings(image_np):   # image_np means numpy image
    detector, sp, facerec = load_dlib_models()  # here we are loading the dlib models for face detection, shape prediction and face recognition using this load_dlib_models() function which we have defined above, so that we can use those models for generating the embeddings vector for the face in the image taken from camera input for facial recognition and attendance marking

    # here this detector() fn will detects the faces from this image_np and here it will only consider each face only once
    # if we increase this number from 1 to 2 or 3, then it will consider each face multiple times and it will give multiple coordinates for the same face, which will actually increase the processing time and will not give any significant improvement in the accuracy of face detection, so here we are keeping this number as 1, so that it will only consider each face only once and it will give the coordinates of that face only once, which will save a lot of processing time and will give good accuracy for face detection.
    faces = detector(image_np, 1)  

    encodings = []

    for face in faces:
        shape = sp(image_np, face) # here this shape_predictor will detect the landmarks of the face from the image using the coordinates of the face detected by the detector and then it will return the shape of the face which contains the coordinates of the landmarks of the face like eyes, nose, mouth, etc. and these landmarks are used for aligning the face before generating the embeddings vector for that face, so here we will use this shape predictor for detecting the landmarks of the face in the image taken from camera input for facial recognition and attendance marking
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)     # 128D embeddings     
        # here this 1 means that we want to upsample the image once before generating the embeddings vector for the face, which will actually improve the accuracy of face recognition, so here we are keeping this number as 1, so that it will upsample the image once before generating the embeddings vector for the face, which will give good accuracy for face recognition.

        # Here we are firstly converting this face_descriptor which is in dlib vector format into a numpy array format using np.array() function of numpy library, so that we can use that numpy array for further processing in the pipeline, so here we will convert this face_descriptor into a numpy array and then we will append that numpy array to the encoding list, so that we can use that encoding list for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
        # As mathematical operations are easier to perform on numpy arrays than on dlib vectors, so here we are converting this face_descriptor into a numpy array format using np.array() function of numpy library, so that we can use that numpy array for further processing in the pipeline, so here we will convert this face_descriptor into a numpy array and then we will append that numpy array to the encoding list, so that we can use that encoding list for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
        encodings.append(np.array(face_descriptor))

    return encodings  # it will return the list of embeddings vector for the faces detected in the image taken from camera input for facial recognition and attendance marking, so here we will use this list of embeddings vector for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.



# this fn will trained the model for all the students present in the database and then it will return the trained SVM classifier model which we can use for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
# this fn is also time consuming as it will train the model for all the students present in the database, so we will use the @st.cache_resource decorator of streamlit to cache the output of this function, so that it will not train the model again and again every time we call this function, instead it will train the model only once and then it will cache the output of this function, so that when we call this function again, it will return the cached output instead of training the model again, which will save a lot of time and will improve the performance of our app.
@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()  # here this get_all_students() function will fetch the list of all the student records from the students table in the database, so here we will use this function to fetch the list of all the student records from the database and then we will use that list of student records for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    if not student_db:
        return None  # if there is no student record in the database, then we will return None, which means that we cannot train the model as there is no student record in the database, so here we are checking that if there is no student record in the database, then we will return None, which means that we cannot train the model as there is no student record in the database.
    
    for student in student_db:
        embedding = student.get("face_embedding") # here this face_embedding field will contain the embeddings vector for the face of that student, which is generated when the student record is created in the database, so here we will fetch that embeddings vector from the database for each student and then we will use that embeddings vector for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

        if embedding:
            X.append(np.array(embedding))   # here we are appending this embeddings vector to the X list but in the form of numpy array, which will contain the list of all the embeddings vector for the faces of all the students present in the database, so here we will use this X list for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
            y.append(student.get('student_id'))  # here we are appending this student_id to the y list, which will contain the list of all the student_id for all the students present in the database, so here we will use this y list for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
            # so this y actually contains the labels for the embeddings vector in the X list, which will be used for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    if len(X) == 0:  # if no student embedding found i.e there is no student record in the database with the face_embedding field, then we will return None, which means that we cannot train the model as there is no student record in the database with the face_embedding field, so here we are checking that if there is no student record in the database with the face_embedding field, then we will return None, which means that we cannot train the model as there is no student record in the database with the face_embedding field.
        return 0


    classifier = SVC(kernel='linear', probability=True, class_weight='balanced')  # here we are creating an instance of SVC classifier with linear kernel and probability=True, which will allow us to get the probability of the prediction for each class, so here we will use this SVC classifier for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
    # here class_weight='balanced' is used to handle the class imbalance problem in our dataset, as there may be some students with more images of their faces in the database than other students, so by using class_weight='balanced', it will automatically adjust the weights of the classes based on the number of samples in each class, so that it will give more importance to the classes with less samples and less importance to the classes with more samples, which will help in improving the accuracy of our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
    # so even if one student have 100 images and other have 1 image, it will balance them by converting them into same scale, so that model doesn't get biased towards the student with more images in the database, which will help in improving the accuracy of our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    # here we are using try-catch because sometimes during model training, it may give some error due to some reason like if there is only one student record in the database with the face_embedding field, then it will give an error while training the SVM classifier model as SVM requires at least 2 classes for training, so here we are using try-catch to handle such errors and to print the error message in the console, so that we can debug the issue and fix it, so here we will use this try-catch block for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
    try:
        classifier.fit(X, y)  # here we are training this SVC classifier model on the X list which contains the embeddings vector for the faces of all the students present in the database and the y list which contains the student_id for all the students present in the database, so here we will use this trained SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
    except ValueError:
        pass   # if there is any error during model training, then we will just pass it and we will not do anything, as there may be some cases where we cannot train the model due to some reason like if there is only one student record in the database with the face_embedding field, then it will give an error while training the SVM classifier model as SVM requires at least 2 classes for training, so here we are using try-catch to handle such errors and to print the error message in the console, so that we can debug the issue and fix it, so here we will use this try-catch block for training our SVM classifier model for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.


    return {'clf': classifier, 'X': X, 'y': y}  # here we are returning this dictionary which contains the trained SVM classifier model in the 'clf' key and the X list which contains the embeddings vector for the faces of all the students present in the database in the 'X' key and the y list which contains the student_id for all the students present in the database in the 'y' key, so here we will use this dictionary for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.


# this fn we will use when some new student record is added in the database with the face_embedding field, so that we can train our SVM classifier model again with the new student record added in the database, so here we will use this fn for training our SVM classifier model again with the new student record added in the database, so that we can classify the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
def train_classifier():
    st.cache_resource.clear()  # here we are clearing the cache of the get_trained_model() function, so that it will train the model again with the new student record added in the database, so that we can classify the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    model_data = get_trained_model()  # here we are calling this get_trained_model() function to train the SVM classifier model again with the new student record added in the database, so that we can classify the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    return bool(model_data)  # here we are returning the boolean value of the model_data, which will be True if the model is trained successfully and False if there is any error during model training, so here we will use this boolean value to check that if the model is trained successfully or not, so that we can classify the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.



# this fn will take the group photos of the students of class as numpy array input and then it will return the list of student_id for the students whose faces are detected in the group photo, so here we will use this fn for marking the attendance of students using facial recognition, so here we will take the group photos of the students of class as input and then we will use this fn to get the list of student_id for the students whose faces are detected in the group photo, so that we can mark the attendance of those students whose faces are detected in the group photo, so here we will use this fn for marking the attendance of students using facial recognition.
def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)  # here we are getting the list of embeddings vector for the faces detected in the group photo taken from camera input for facial recognition and attendance marking using this get_face_embeddings() function which we have defined above, so that we can use that list of embeddings vector for classifying the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    detected_student = {}

    model_data = get_trained_model()  # here we are getting the trained SVM classifier model using this get_trained_model() function which we have defined above, so that we can use that trained SVM classifier model for classifying the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    if not model_data:   # it means that there is no model data, which means that there is no student record in the database with the face_embedding field, so we cannot train the model and we cannot classify the faces based on the embeddings vector and then we cannot mark the attendance of that student whose face is matched with the embeddings vector stored in the database, so here we are checking that if there is no model data, which means that there is no student record in the database with the face_embedding field, then we will return an empty dictionary and an empty list and the total number of faces detected in the group photo, so that we can handle this case in the calling function and we can show a message to the user that there is no student record in the database with the face_embedding field, so we cannot mark the attendance of students using facial recognition, so here we are checking that if there is no model data, then we will return an empty dictionary and an empty list and the total number of faces detected in the group photo, so that we can handle this case in the calling function and we can show a message to the user that there is no student record in the database with the face_embedding field, so we cannot mark the attendance of students using facial recognition.
        return detected_student, [], len(encodings)   # if there is no model data, then we will return an empty dictionary i.e detected_student and an empty list and the total number of faces detected in the group photo i.e 0, so that we can handle this case in the calling function and we can show a message to the user that there is no student record in the database with the face_embedding field, so we cannot mark the attendance of students using facial recognition, so here we are checking that if there is no model data, then we will return an empty dictionary and an empty list and the total number of faces detected in the group photo, so that we can handle this case in the calling function and we can show a message to the user that there is no student record in the database with the face_embedding field, so we cannot mark the attendance of students using facial recognition.
    

    classifier = model_data['clf']  # here we are getting the trained SVM classifier model from the model_data dictionary which is returned by the get_trained_model() function, so that we can use that trained SVM classifier model for classifying the faces based on the embeddings vector and then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))  # here we are getting the list of all the unique student_id from the y_train list which contains the student_id for all the students present in the database, so here we will use this list of unique student_id for classifying the faces based on the embeddings vector and then we will mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

    for encoding in encodings:
        if len(all_students) >= 2:
            # here in this classifier.predict([encoding])[0], highest score is at index 0 because we are using linear kernel for SVM classifier, so here we are using this classifier.predict() function to predict the student_id for the face detected in the group photo based on the embeddings vector for that face, so here we will use this predicted student_id for marking the attendance of that student whose face is matched with the embeddings vector stored in the database.
            predicted_id = int(classifier.predict([encoding])[0])  # here we are using this trained SVM classifier model to predict the student_id for the face detected in the group photo based on the embeddings vector for that face, so here we will use this predicted student_id for marking the attendance of that student whose face is matched with the embeddings vector stored in the database.
            # here this classifier.predict() function will return the predicted student_id for the face detected in the group photo based on the embeddings vector for that face, so here we will use this predicted student_id for marking the attendance of that student whose face is matched with the embeddings vector stored in the database.
            # this .predict() fn will actually return score for each class but [0] will give the index of the class with the highest score, which will be the predicted student_id for that face detected in the group photo based on the embeddings vector for that face, so here we will use this predicted student_id for marking the attendance of that student whose face is matched with the embeddings vector stored in the database.
        else:     # if there is only one student record in the database with the face_embedding field
            predicted_id = int(all_students[0])  # student_id of that single student

        # now this predicted_id, we will find its corresponding embeddings
        # as we know that for a single student, both its embeddings and id will be present at the same index in the X_train and y_train list respectively, so here we will use this predicted_id to find its corresponding embeddings from the X_train list, so that we can calculate the distance between this embeddings vector and the embeddings vector for the face detected in the group photo, so that we can check that if the distance is less than a certain threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
        student_embedding = X_train[y_train.index(predicted_id)]  # here we are getting the embeddings vector for that predicted student_id from the X_train list which contains the embeddings vector for the faces of all the students present in the database, so here we will use this embeddings vector for calculating the distance between this embeddings vector and the embeddings vector for the face detected in the group photo, so that we can check that if the distance is less than a certain threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

        # As here from the classifier model, we are getting the predicted student_id for the face detected in the group photo based on the embeddings vector for that face, but we also need to check that if this predicted student_id is actually a match for that face detected in the group photo based on the embeddings vector for that face, so here we will calculate the distance between this embeddings vector and the embeddings vector for the face detected in the group photo using the L2 norm (Euclidean distance) which is calculated using np.linalg.norm() function of numpy library, so here we will use this distance to check that if the distance is less than a certain threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
        best_match_score = np.linalg.norm(student_embedding - encoding)  # here we are calculating the distance between this embeddings vector and the embeddings vector for the face detected in the group photo using the L2 norm (Euclidean distance) which is calculated using np.linalg.norm() function of numpy library, so here we will use this distance to check that if the distance is less than a certain threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

        resemblance_threshold = 0.6 # here we are setting this resemblance_threshold as 0.6, which means that if the distance between the embeddings vector for the face detected in the group photo and the embeddings vector for that predicted student_id is less than 0.6, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database, so here we will use this resemblance_threshold to check that if the distance is less than this threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
        # we take this as 0.6 because in general, the distance between the embeddings vector for the face detected in the group photo and the embeddings vector for that predicted student_id should be less than 0.6 for a good match, so here we are setting this resemblance_threshold as 0.6, which means that if the distance between the embeddings vector for the face detected in the group photo and the embeddings vector for that predicted student_id is less than 0.6, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database, so here we will use this resemblance_threshold to check that if the distance is less than this threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.

        if best_match_score < resemblance_threshold:  # here we are checking that if the distance between the embeddings vector for the face detected in the group photo and the embeddings vector for that predicted student_id is less than this resemblance_threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database, so here we will use this resemblance_threshold to check that if the distance is less than this threshold, then we can mark the attendance of that student whose face is matched with the embeddings vector stored in the database.
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)  # here we are returning this detected_student dictionary which contains the student_id for the students whose faces are detected in the group photo as keys and True as values and the all_students list which contains the list of all the unique student_id from the y_train list which contains the student_id for all the students present in the database and the total number of faces detected in the group photo i.e len(encodings), so that we can use this information for marking the attendance of students using facial recognition, so here we will use this information for marking the attendance of students using facial recognition.

