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

prn = int(input("Enter prn of student"))
start_date = str(input("Enter start  date"))
end_date = str(input("Enter end date"))

missed_lectures = detailsOfAbsentLectures(prn, start_date, end_date)
print("Date and time \t\t Classroom  Course Code")
for missed_lecture in missed_lectures:
    print(f"{str(missed_lecture[0]):<20} {missed_lecture[1]:>12} {missed_lecture[2]:>10}")
