import MySQLdb 
import mysql.connector as mc
import string 
import random 
from datetime import date

def establishConnection():
    return mc.connect(host='localhost', user='root', passwd='ayushi',db='attendance_management_system') 

#Query 4:  A query to retrieve the list of courses enrolled by a batch of students.
def coursesTakenByBatch(batch):
    connection = establishConnection()
    cursor = connection.cursor()
    
    cursor.execute("""SELECT class_id FROM class WHERE batch = '%s' """%(batch))
    class_id = cursor.fetchone()[0]
    cursor.execute("""SELECT course_name FROM course INNER JOIN takes_course ON course.course_code = takes_course.course_code WHERE class_id = %s  """ % (class_id) )
    result = cursor.fetchone()
    if not result:
        return f'Error: Batch {batch} does not exist in database'
    else:
        class_id = result[0]
    cursor.close()
    connection.close()
    subjects = []
    for subject in result:
        subjects.append(subject[0])
    return subjects

print(coursesTakenByBatch("2017-21"))