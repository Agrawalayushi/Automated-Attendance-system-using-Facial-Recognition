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

def randomString(stringLength = 6):
    '''Generate a random string for registration key of length 6'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=stringLength))
def register():
    registrationKey = randomString()
    print(f'Registration key generated is {registrationKey}')
    prn = int(input('Enter PRN of student: '))
    connection = establishConnection() 
    updateRegistrationDetails(registrationKey, date.today(), prn)

register()