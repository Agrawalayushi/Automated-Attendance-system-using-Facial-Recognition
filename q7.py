import MySQLdb 
import mysql.connector as mc
import string 
import random 
from datetime import date

def establishConnection():
    return mc.connect(host='localhost', user='root', passwd='ayushi',db='attendance_management_system') 

def randomString(stringLength = 6):
    '''Generate a random string for registration key of length 6'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=stringLength))
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

def register():
    registrationKey = randomString()
    print(f'Registration key generated is {registrationKey}')
    prn = int(input('Enter PRN of student: '))
    connection = establishConnection() 
    updateRegistrationDetails(registrationKey, date.today(), prn)

#Query 7 : Update the start and end dates of course assigned to a faculty
def updateCourseStartEndDates(course_name, faculty_name, start_date, end_date):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT course_code FROM course WHERE course_name = '%s' """%(course_name))
    r = cursor.fetchone()
    if not r:
        return 'Error: course name does not exist'
    else:
        course_code = r[0]

    cursor.execute("""SELECT emp_id FROM faculty WHERE faculty_name = '%s' """%(faculty_name))
    r = cursor.fetchone()

    if not r:
        return f'Faculty with name {faculty_name} does not exist in the database'
    else:
        emp_id = r[0]

    cursor.execute("""UPDATE assigned_to SET start_date = '%s' , end_date = '%s' WHERE emp_id = %s AND course_code = %s  """%(start_date, end_date, emp_id, course_code))

    cursor.close()
    connection.commit()
    connection.close()

course_name=str(input("Enter course name : "))
faculty_name=str(input("Enter Faculty name : "))
start_date=str(input("Enter start date: "))
end_date=str(input("Enter end date : "))
print("Updated!!")
