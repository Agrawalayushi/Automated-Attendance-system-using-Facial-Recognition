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