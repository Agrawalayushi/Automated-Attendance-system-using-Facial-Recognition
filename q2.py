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

prn = int(input("Enter prn od student to check whether he/she has registered or not"))
hasStudentregisted(prn)