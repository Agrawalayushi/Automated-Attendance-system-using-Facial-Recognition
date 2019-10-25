import MySQLdb 
import mysql.connector as mc
import string 
import random 
from datetime import date

def establishConnection():
    return mc.connect(host='localhost', user='root', passwd='ayushi',db='attendance_management_system') 

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

faculty_name = str(input("Enter faculty name :"))
start_date = str(input("Enter start date : "))
end_date = str(input("Enter end date : "))

print(coursesAssignedToFaculty(faculty_name, start_date, end_date))
