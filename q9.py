import MySQLdb 
import mysql.connector as mc
import string 
import random 
from datetime import date

def establishConnection():
    return mc.connect(host='localhost', user='root', passwd='ayushi',db='attendance_management_system') 

#Query 1: Exeucte a query to update the registration key, date and semester fields of a particular student.
def updateRegistrationDetails( registrationKey, registrationDate, prn ):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""UPDATE student SET registration_key = '%s', registration_date = '%s', semester = semester + 1 WHERE prn = %s"""%(registrationKey, registrationDate, prn))
    cursor.execute("""SELECT prn, student_name, registration_key, registration_date, semester FROM student WHERE prn = %s  ; """%(prn) ) 
    result = cursor.fetchall()
    print("Update made into the database is-- ", result)
    cursor.close()
    connection.commit() 
    connection.close()

#Query 2: A query to check whether a student has registered for the new semester or not 
def hasStudentregisted(prn):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute( """SELECT registration_key, registration_date FROM student WHERE prn = %s """%(prn))

    result = cursor.fetchall() 
    
    if result:
        registration_key = result[0][0]
        registrationDate = result[0][1]
    else:
        return f"Student with PRN {prn} doesn't exist in the students table "

    if registration_key == None:
        print(f'Student with prn {prn} has not yet registered')
        return False
    else:
        print(f'Student with PRN {prn} has registered for the new semester on date {registrationDate}')
        return True 

    cursor.close()
    connection.close()

#Query 3 : A query to count the number of lectures attended by the student
def countLecturesAttended(prn, course_code):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT COUNT(PRN) FROM attends WHERE PRN = %s AND course_code = %s """%(prn, course_code))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if(not result):
        return 0
    else:
        return result[0]

#Query 4:  A query to retrieve the list of courses enrolled by a batch of students.
def coursesTakenByBatch(batch):
    connection = establishConnection()
    cursor = connection.cursor()
    
    cursor.execute("""SELECT class_id FROM class WHERE batch = '%s' """%(batch))
    class_id = cursor.fetchone()[0]
    cursor.execute("""SELECT course_name FROM course INNER JOIN takes_course ON course.course_code = takes_course.course_code WHERE class_id = %s  """ % (class_id) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    subjects = []
    for subject in result:
        subjects.append(subject[0])
    return subjects

#Query 5: A query to retrieve the names of courses assigned to a faculty in a given duration
def coursesAssignedToFaculty(faculty_name, start_date, end_date):
    connection = establishConnection()
    cursor = connection.cursor()
    
    cursor.execute("""SELECT emp_id FROM faculty WHERE faculty_name = '%s';"""%(faculty_name))
    faculty_id = cursor.fetchone()[0]

    cursor.execute("""SELECT course_name FROM course INNER JOIN assigned_to ON course.course_code = assigned_to.course_code WHERE emp_id = %s
                    AND start_date = '%s' and end_date = '%s' """%(faculty_id, start_date, end_date))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    subjects_assigned = []
    for course in courses:
        subjects_assigned.append(course[0])
    return subjects_assigned 

#Query 6: A query to retrieve the details of lectures missed by a student conducted by a faculty in a given duration
def detailsOfAbsentLectures( prn, start_date, end_date ):
    connection = establishConnection()
    cursor = connection.cursor()
    cursor.execute('SELECT division_id FROM student WHERE prn = %s'%(prn))
    division = cursor.fetchone()[0]
    print(division)
    cursor.execute(
        """
           SELECT conducts.date_time, conducts.classroom, conducts.course_code  FROM conducts
           NATURAL JOIN conducted_for_division 
           WHERE (conducts.date_time, conducts.classroom)
           NOT IN 
           (
            SELECT date_time, classroom FROM attends
            WHERE prn = %s
           )
           AND
            conducted_for_division.division_id = '%s' ;
        """%(prn, division) 
    )
    absent_lectures = cursor.fetchall()
    cursor.close()
    connection.close()
    missed_lectures = []
    for absent_lecture in absent_lectures:
        missed_lectures.append(absent_lecture)
    return missed_lectures 

#Query 7 : Update the start and end dates of course assigned to a faculty
def updateCourseStartEndDates(course_name, faculty_name, start_date, end_date):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT course_code FROM course WHERE course_name = '%s' """%(course_name))
    course_code = cursor.fetchone()

    cursor.execute("""SELECT emp_id FROM faculty WHERE faculty_name = '%s' """%(faculty_name))
    emp_id = cursor.fetchone()

    cursor.execute("""UPDATE assigned_to SET start_date = '%s' AND end_date = '%s' WHERE emp_id = %s AND course_code = %s  """%(start_date, end_date, emp_id, course_code))

    cursor.close()
    connection.close()

#Query 8: Return the list of courses with attendance less than 70%
def coursesWithLowAttendance(prn):
    connection = establishConnection()
    cursor = connection.cursor()
    cursor.execute("""SELECT class_id, division_id FROM student WHERE prn = %s"""%(prn))
    response = cursor.fetchall()
    class_id = response[0][0]
    division = response[0][1]
    cursor.execute("""SELECT course_code FROM takes_course NATURAL JOIN class WHERE class_id = %s"""%(class_id))
    courses = cursor.fetchall()
    result = []
    for course in courses:
        course_code = course[0]
        lectures_attended = countLecturesAttended(prn, course_code)
        lectures_conducted = cursor.execute("""SELECT COUNT(*) FROM conducts NATURAL JOIN conducted_for_division 
                                            WHERE course_code = %s AND division_id = '%s' """ % (course_code, division))
        percentage = ( lectures_attended / lectures_conducted ) * 100
        print(f'Course code = {course_code} , Lectures conducted = {lectures_conducted}, Lectures attended = {lectures_attended}, Percentage = {percentage}') 
        if percentage < 70 :
            result.append( (course_code, lectures_attended, lectures_conducted, percentage) )
    return result


#Query 9: Delete all records of students that passed out from the institute 
def deleteRecordsOfPassOutStudents(batch):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT class_id FROM class WHERE batch = '%s' """%(batch))

    r = cursor.fetchone()
    if not r :
        return 'Error: Batch does not exist'
    else:
        class_id = r[0] 

    cursor.execute("""DELETE FROM class WHERE class_id = %s """%(class_id))

    cursor.close()
    connection.commit()
    connection.close()





def randomString(stringLength = 6):
    '''Generate a random string for registration key of length 6'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=stringLength))

def register():
    registrationKey = randomString()
    print(f'Registration key generated is {registrationKey}')
    prn = int(input('Enter PRN of student: '))
    connection = establishConnection() 
    updateRegistrationDetails(registrationKey, date.today(), prn)



#print(coursesTakenByBatch("2017-21"))
#print(coursesAssignedToFaculty("Pooja Kamat", '2019-07-15', '2019-10-20'))
'''missed_lectures = detailsOfAbsentLectures(17070122016, "2019-07-11", "2019-08-11")
print("Date and time \t\t Classroom  Course Code")
for missed_lecture in missed_lectures:
    print(f"{str(missed_lecture[0]):<20} {missed_lecture[1]:>12} {missed_lecture[2]:>10}")
'''
#print(coursesWithLowAttendance(17070122016))

deleteRecordsOfPassOutStudents("2017-21")