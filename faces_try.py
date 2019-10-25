import numpy as np
import cv2
import pickle
from datetime import datetime
import MySQLdb 
import mysql.connector as mc
import string 
import random 
from datetime import datetime, date

def establishConnection():
    return mc.connect(host='localhost', user='root', passwd='ayushi',db='attendance_management_system') 

def recordLecture(classroom, date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    connection = establishConnection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO lecture VALUES('%s', '%s')"%(date_time, classroom))
    lecture = (classroom, date_time)
    cursor.close()
    connection.commit()
    connection.close()
    return lecture


def recordLectureConductedByFaculty(lecture, faculty_name, course_name):
    connection = establishConnection()
    cursor = connection.cursor()
    cursor.execute(""" SELECT emp_id FROM faculty WHERE faculty_name = '%s' """ % (faculty_name))
    r = cursor.fetchone()
    if not r:
        return 'Error: Faculty name {faculty_name} not found in the database'
    else:
        emp_id = r[0]
    
    cursor.execute("""SELECT course_code FROM course WHERE course_name = '%s' """%(course_name))
    r = cursor.fetchone()
    if not r:
        return 'Error: Course name {course_name} not found in the database'
    else:
        course_code = r[0]

    cursor.execute("""INSERT INTO conducts VALUES('%s', '%s', %s, %s)"""%(lecture[1], lecture[0], emp_id, course_code))
    cursor.close()
    connection.commit()
    connection.close()
    return f"Lecture conducted by faculty {faculty_name} dated {lecture[1]} in classroom {lecture[0]} is recorded in the database."

def  markAttendance(prn, classroom, course_name, date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    connection = establishConnection()
    cursor = connection.cursor()
    cursor.execute("""SELECT course_code FROM course WHERE course_name = '%s'"""%(course_name))
    r = cursor.fetchone()
    if not r:
        print(f'Error: Course {course_name} does not exist in the database... Check spelling')
        return 'Failed: Unsuccessful in marking attendnace of student...'
    else:
        course_code = r[0]

    cursor.execute("""INSERT INTO attends VALUES(%s, '%s', '%s', %s) ; """ %(prn, date_time, classroom, course_code) )

    cursor.close()
    connection.commit()
    connection.close()
    return f"Attendance of student with PRN {prn} for course {course_name} dated on {date_time} in venue {classroom} is succesfully recorded!"

#TAKING INPUTS
print("-----------------ENTER FACULTY DETAILS-----------------")
classroom = str(input('Enter classroom at which lecture was held: '))
lecture = recordLecture(classroom)
faculty_name = str(input('Enter name of faculty who conducted the lecture: '))
course_name = str(input('Enter name of course for which lecture was conducted: '))
#recording faculty database
recordLectureConductedByFaculty(lecture, faculty_name, course_name)

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

def facerecognizer(name):
    prn = int(name)
    if prn!=0:
        return prn
    else:
        return -1
        

name =''
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
    	#print(x,y,w,h)
    	roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
    	roi_color = frame[y:y+h, x:x+w]

    	# recognize? deep learned model predict keras tensorflow pytorch scikit learn
    	id_, conf = recognizer.predict(roi_gray)
    	if conf>=4 and conf <= 85:
    		font = cv2.FONT_HERSHEY_SIMPLEX
    		name = labels[id_]
    		color = (255, 255, 255)
    		stroke = 2
    		cv2.putText(frame, name, (x,y), font, 1, color, stroke,cv2.LINE_AA)

    	color = (255, 0, 0) #BGR 0-255 
    	stroke = 2
    	end_cord_x = x + w
    	end_cord_y = y + h
    	cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    	#subitems = smile_cascade.detectMultiScale(roi_gray)
    	#for (ex,ey,ew,eh) in subitems:
    	#	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#marking present of detected student
prn = facerecognizer(name) 
print(prn)
markAttendance(prn,classroom,course_name)   


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

