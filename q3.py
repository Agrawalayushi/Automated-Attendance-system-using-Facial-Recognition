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

def register():
    registrationKey = randomString()
    print(f'Registration key generated is {registrationKey}')
    prn = int(input('Enter PRN of student: '))
    connection = establishConnection() 
    updateRegistrationDetails(registrationKey, date.today(), prn)

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

#Query 3 : A query to count the number of lectures attended by the student
def countLecturesAttended(prn, course_code):
    connection = establishConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT COUNT(PRN) FROM attends WHERE PRN = %s AND course_code = %s """%(prn, course_code))
    result = cursor.fetchone()
    print(result)
    cursor.close()
    connection.close()
    if(not result):
        return 0
    else:
        return result[0]

print("Enter the prn and course code : ")
prn = int(input("PRN : "))
cc = str(input("Course Code :"))
countLecturesAttended(prn,cc)