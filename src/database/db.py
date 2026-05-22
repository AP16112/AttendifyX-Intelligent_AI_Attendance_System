# In this db.py file, we will write all the queries required to call the database and to interact with the database in our project, so that we can keep all the database related code in one file and can easily import this file wherever we want to interact with the database in our project, so that we can keep our code clean and organized.

from src.database.config import supabase  # here we are importing the instance of supabase client, which we have created in the config.py file, so that we can use that client to interact with our supabase database in our project

import bcrypt   # it is used for hasing


def hash_pass(pwd):   # this 'pwd' is actually the password
    # here this bcrypt.hashpw() is used to hash the password using bcrypt library, so that we can store the hashed password in the database instead of the plain text password, which is more secure. 
    # The pwd.encode() is used to convert the password from string format to bytes format, because the bcrypt.hashpw() function expects the password to be in bytes format.
    # The bcrypt.gensalt() is used to generate a salt for the hashing process, which adds an additional layer of security to the hashed password. 
    # The .decode() is used to convert the hashed password from bytes to string format, so that we can store it in the database as a string.
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_password(pwd, hashed_pwd):
    # here this bcrypt.checkpw() is used to check whether the password entered by the user matches with the hashed password stored in the database for that teacher record, so we need to encode both the password entered by the user and the hashed password from the database to bytes format before passing them to this bcrypt.checkpw() function, because this function expects both the passwords to be in bytes format.
    return bcrypt.checkpw(pwd.encode(), hashed_pwd.encode())
    # Here this bcrypt.checkpw() fn will first hash the password entered by the user using the same salt and algorithm as the hashed password from the database, and then will compare the two hashed passwords, if they match then it will return true, otherwise it will return false.


def check_teacher_exists(username):
    # Check for unique username, & returns true when username is already taken
    # Here this "teachers" is the table name actually
    # This eq("username", username) is used to check whether the username already exists in the teachers table or not.
    # this .execute() is used to execute this query
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    # So now this response.data will contain the list of all the records which have the same username as the one we are trying to register, so if the length of this response.data is greater than 0, then it means that there is already a record with the same username in the teachers table, so we will return true, otherwise we will return false.
    return len(response.data) > 0


def create_teacher(username, password, name):
    # Here this hash_pass function is used to hash the password using bcrypt library, so that we can store the hashed password in the database instead of the plain text password, which is more secure.
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()

    return response.data  # it will return the data of the newly created teacher record


def teacher_login(username, password):
    # we are firstly checking this username teacher exists or not, if it doesn't exist then we will return false, otherwise we will check the password
    response = supabase.table("teachers").select("*").eq("username", username).execute()

    if response.data:   # if this response.data is not empty, then it means that there is a teacher record with the same username in the teachers table, so we will check the password
        teacher = response.data[0]   # since this response.data is a list of records, so we will take the first record from that list, which will be the teacher record with the same username as the one we are trying to login
        # Although there will be only one record with the same username in the teachers table, because we are checking for unique username while creating the teacher record, so there will be only one record with the same username in the teachers table, so we can safely take the first record from that list and check the password for that record.

        # Here this check_password function is used to check whether the password entered by the user matches with the hashed password stored in the database for that teacher record, so we need to pass the password entered by the user and the hashed password from the database to this check_password function, and this function will return true if the password is correct, otherwise it will return false.
        if check_password(password, teacher["password"]):
            return teacher  # if the password is correct, then we will return the teacher record

    return None 


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data  # it will return the list of all the student records from the students table in the database


# here this create_student() fn will actually create this new student & add it into the database
# here we are taking the default values for face and voice embedding to be None 
def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}

    response = supabase.table("students").insert(data).execute()    # it will add this current student into the students table in database
    return response.data    # it will return the data of the newly created student record



# here this create_subject() fn will actually create this new subject & add it into the database
def create_subject(sub_code, name, section, teacher_id):
    data = {"subject_code": sub_code, "name": name, "section": section, "teacher_id": teacher_id}

    response = supabase.table("subjects").insert(data).execute()    # it will add this current subject into the subject table in database
    return response.data    # it will return the data of the newly created subject record



# here this fn will give the list of all subjects of some particular teacher
def get_teacher_subjects(teacher_id):
    # Here this query is used to get the list of all subjects of some particular teacher with the count of students enrolled in each subject and also with the attendance logs for each subject, so that we can show this data in the manage subjects tab in the teacher dashboard, and also we can use this data to show the attendance records for each subject in the attendance records tab in the teacher dashboard.
    # so here these subject_students(count) and attendance_logs(timestamp) are the names of the relationships (i.e tables) which we have defined in the supabase database between the subjects table and the subject_students table and also between the subjects table and the attendance_logs table respectively, so that we can get the count of students enrolled in each subject and also get the attendance logs for each subject in this query itself, so that we don't have to make separate queries to get this data later when we want to show this data in the manage subjects tab in the teacher dashboard.
    # here this subject_students(count) is used to get the count of students enrolled in each subject, so here this count is actually an alias for the count of records in the subject_students table which are associated with that particular subject, so it will give us the count of students enrolled in each subject, and we can use this count to show the total number of students enrolled in each subject in the manage subjects tab in the teacher dashboard.
    response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()

    subjects = response.data  # it will return the list of all the subject records from the subjects table in the database which are associated with that particular teacher_id, and also each subject record will contain the count of students enrolled in that subject and also the attendance logs for that subject because we have defined the relationships between the tables in the supabase database.  

    for sub in subjects:
        # whenever we are using get(), we need to provide the fallbacks also, i.e in case there is no record in the subject_students table for that particular subject, then this sub.get("subject_students", [{}]) will return a list with an empty dictionary, and then we are taking the first element of that list which is an empty dictionary, and then we are trying to get the value of the "count" key from that empty dictionary, so it will return 0 as the default value if there is no record in the subject_students table for that particular subject, so this way we can avoid any error in case there is no record in the subject_students table for that particular subject.
        sub['total_students'] = sub.get("subject_students", [{}])[0].get("count", 0) if sub.get('subject_students') else 0    # here we are adding a new key 'total_students' in each subject record, which will contain the count of students enrolled in that subject, so that we can easily access this count when we want to show this data in the manage subjects tab in the teacher dashboard, and here we are using the get() method to avoid any error in case there is no record in the subject_students table for that particular subject, so if there is no record in the subject_students table for that particular subject, then this sub.get("subject_students", [{}]) will return a list with an empty dictionary, and then we are taking the first element of that list which is an empty dictionary, and then we are trying to get the value of the "count" key from that empty dictionary, so it will return 0 as the default value if there is no record in the subject_students table for that particular subject.
        # So here this line of code is used to add a new key 'total_students' in each subject record, which will contain the count of students enrolled in that subject, so that we can easily access this count when we want to show this data in the manage subjects tab in the teacher dashboard, and here we are using the get() method to avoid any error in case there is no record in the subject_students table for that particular subject, so if there is no record in the subject_students table for that particular subject, then this sub.get("subject_students", [{}]) will return a list with an empty dictionary, and then we are taking the first element of that list which is an empty dictionary, and then we are trying to get the value of the "count" key from that empty dictionary, so it will return 0 as the default value if there is no record in the subject_students table for that particular subject.
 
        attendance = sub.get('attendance_logs', [])   # here we are getting the attendance logs for that particular subject from the attendance_logs relationship which we have defined in the supabase database, so if there is no attendance log for that particular subject, then this sub.get('attendance_logs', []) will return an empty list as the default value, so that we can avoid any error in case there is no attendance log for that particular subject.
        unique_sessions = len(set(log['timestamp'] for log in attendance))   # here we are calculating the count of unique sessions for that particular subject by taking the timestamp of each attendance log for that subject and then converting it into a set to get the unique timestamps, and then we are taking the length of that set to get the count of unique sessions for that particular subject, so that we can show this count of unique sessions in the manage subjects tab in the teacher dashboard.
        # so here this line of code is used to calculate the count of unique sessions for that particular subject by taking the timestamp of each attendance log for that subject and then converting it into a set to get the unique timestamps, and then we are taking the length of that set to get the count of unique sessions for that particular subject, so that we can show this count of unique sessions in the manage subjects tab in the teacher dashboard, and here we are using the get() method to avoid any error in case there is no attendance log for that particular subject, so if there is no attendance log for that particular subject, then this sub.get('attendance_logs', []) will return an empty list as the default value, so that we can avoid any error in case there is no attendance log for that particular subject.
        # e.g if there are 5 attendance logs for that particular subject with the following timestamps: "2023-10-01 10:00:00", "2023-10-01 10:00:00", "2023-10-02 11:00:00", "2023-10-03 12:00:00", "2023-10-03 12:00:00", then this line of code will calculate the count of unique sessions for that particular subject as 3, because there are 3 unique timestamps in those attendance logs, which means that there were 3 unique sessions for that particular subject.

        sub['total_classes'] = unique_sessions

        sub.pop('subject_students', None)   # here we are removing this subject_students relationship from the subject record, because we have already extracted the count of students enrolled in that subject and stored it in the total_students key, so we don't need this subject_students relationship anymore in the subject record, so we are removing it to keep our data clean and organized.
        sub.pop('attendance_logs', None)    # here we are removing this attendance_logs relationship

    return subjects   # it will return the list of all the subject records from the subjects table in the database which are associated with that particular teacher_id, and also each subject record will contain the count of students enrolled in that subject and also the count of unique sessions for that subject, so that we can use this data to show in the manage subjects tab in the teacher dashboard.



# so this fn student will enroll a student in some subject
def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, 'subject_id': subject_id}

    # so it will add this data object to this 'subject_students' table which means that this student gets enrolled in this subject
    response = supabase.table('subject_students').insert(data).execute()

    response.data  # it will return the data of the newly created subject student record


# so this fn student will unenroll a student from some subject
def unenroll_student_from_subject(student_id, subject_id):
    # so it will delete that row from this 'subject_students' table which have this student id and subject id
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()

    response.data  # it will return the data of this deleted record


# this fn will return the list of all the subjects this particular student enrolled in
def get_student_subjects(student_id):
    # Query the 'subject_students' table and also join related data from the 'subjects' table.
    # select('*, subjects(*)') → fetches all columns from subject_students (*) and expands the subjects table (*) for each matching record
    # eq('student_id', student_id) → filters rows so only those belonging to the given student_id are returned
    # execute() → runs the query and returns the result (data + error if any)
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    # This query retrieves all subject enrollment records for a particular student from the subject_students table, and at the same time pulls in the full details of each subject from the subjects table. The result is a combined dataset showing which subjects the student is enrolled in along with the subject information itself.

    return response.data   # it will return the list of all subjects student enrolled in & also full details of each those subjects also


# that fn is designed to pull attendance records for each subject the student is enrolled in.
def get_student_attendance(student_id):
    # Query the 'attendance_logs' table and also join related data from the 'subjects' table.
    # select('*, subjects(*)') → fetches all columns from attendance_logs (*) and expands the subjects table (*) for each matching record
    # eq('student_id', student_id) → filters rows so only attendance records belonging to the given student_id are returned
    # execute() → runs the query and returns the result (data + error if any)
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()

    # This query retrieves all attendance records for a particular student from the attendance_logs table, and at the same time pulls in the full details of each subject from the subjects table.
    # The result is a combined dataset showing the student's attendance history along with subject information.
    return response.data   # returns a list of attendance records with full subject details