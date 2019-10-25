#import module from tkinter for UI
import cv2
import connection 
from tkinter import * 
from playsound import playsound
import os
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

#creating instance of TK
root=Tk()
root.configure(background="white")

#function to take attendance for DBMS Lecture
def attend_dbms():
    import faces_try
    

def function5():
    os.startfile(os.getcwd()+"/developers/diet1frame1first.html")
   
def function6():
    root.destroy()
    
def function7():
    exit()

def attend():
    os.startfile(os.getcwd()+"/firebase/attendance_files/attendance"+str(datetime.now().date())+'.xls')

def query1():
    import q1
def query2():
    import q2
def query3():
    import q3
def query5():
    import q5
def query6():
    import q6
def query7():
    import q7
def query8():
    import q8
def query9():
    import q9
def f1():
    import func1

def query():
    r=Tk()
    r.configure(background="white")

    r.title("QUERIES")
    Label(r, text="QUERIES",font=("times new roman",15),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(r,text="Exeucte a query to update the registration key, date and semester fields of a particular student.",font=("times new roman",15),bg="#0D47A1",fg='white',command=query1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    Button(r,text="A query to check whether a student has registered for the new semester or not",font=('times new roman',15),bg="#0D47A1",fg="white",command=query2).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(r,text="A query to count the number of lectures attended by the student",font=('times new roman',15),bg="#0D47A1",fg="white",command=query3).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    #Button(r,text="A query to retrieve the list of courses enrolled by a batch of students.",font=('times new roman',15),bg="#0D47A1",fg="white",command=query3).grid(row=6,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(r,text="A query to retrieve the names of courses assigned to a faculty in a given duration",font=('times new roman',15),bg="#0D47A1",fg="white",command=query5).grid(row=7,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
   
    Button(r,text="A query to retrieve the details of lectures missed by a student conducted by a faculty in a given duration",font=('times new roman',15),bg="#0D47A1",fg="white",command=query6).grid(row=8,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(r,text="Update the start and end dates of course assigned to a faculty",font=('times new roman',15),bg="#0D47A1",fg="white",command=query7).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    #Button(r,text="Return the list of courses with attendance less than 70%",font=('times new roman',15),bg="#0D47A1",fg="white",command=query8).grid(row=10,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    #Button(r,text="Delete all records of students that passed out from the institute",font=('times new roman',15),bg="#0D47A1",fg="white",command=query9).grid(row=11,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(r,text="EXIT",font=('times new roman',20),bg="maroon",fg="white",command=r.destroy).grid(row=13,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    r.mainloop()



def func():
    froot = Tk()
    froot.configure(background="white")
    froot.title("Queries by Functions")

    Label(froot, text="Functions",font=("times new roman",15),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(froot,text="Attendance of a Student for a particular course",font=("times new roman",15),bg="#0D47A1",fg='white',command=f1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    Button(froot,text="Overall attendace of student (till date)",font=('times new roman',15),bg="#0D47A1",fg="white",command=function7).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(froot,text="No of lectures conducted by a faculty for course in a month",font=('times new roman',15),bg="#0D47A1",fg="white",command=function7).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(froot,text="Count of students in particular class that registered on registration day",font=('times new roman',15),bg="#0D47A1",fg="white",command=function7).grid(row=6,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(froot,text="Count of faculty members to teach particular course in a given duration",font=('times new roman',15),bg="#0D47A1",fg="white",command=function7).grid(row=7,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
   
    Button(froot,text="EXIT",font=('times new roman',20),bg="maroon",fg="white",command=froot.destroy).grid(row=13,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    froot.mainloop()

def proc():
    pr=Tk()
    pr.configure(background="white")

    pr.title("PROCEDURES")
    Label(pr, text="PROCEDURES",font=("times new roman",15),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="Update Registration key and Date to NULL",font=("times new roman",15),bg="#0D47A1",fg='white',command=function6).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    Button(pr,text="Successfully Registered Students",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="Late Registrations",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="List of CNG(Course not granted) Students",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=6,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="List of TNG(Term not granted) Students",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=7,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
   
    Button(pr,text="Details of lectures attended by Student in given duration ",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=8,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="Details of lectures conducted by Faculty in given duration",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="Details of lectures attended by a Student conducted by a given faculty",font=('times new roman',15),bg="#0D47A1",fg="white",command=function6).grid(row=10,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    Button(pr,text="EXIT",font=('times new roman',20),bg="maroon",fg="white",command=pr.destroy).grid(row=13,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

    pr.mainloop()


#stting title for the window
root.title("AUTOMATIC ATTENDANCE MANAGEMENT USING FACE RECOGNITION")

#creating a text label
Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM",font=("times new roman",20),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

#creating first button
#Button(root,text="Train Dataset",font=("times new roman",20),bg="#0D47A1",fg='white',command=function1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
#creating second button
Button(root,text="TAKE ATTENDANCE",font=("times new roman",20),bg="#0D47A1",fg='white',command=attend_dbms).grid(row=4,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)


Button(root,text="Queries",font=('times new roman',20),bg="#0D47A1",fg="white",command=query).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root,text="Functions",font=('times new roman',20),bg="#0D47A1",fg="white",command=func).grid(row=10,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root,text="Procedures",font=('times new roman',20),bg="#0D47A1",fg="white",command=proc).grid(row=11,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root,text="Exit",font=('times new roman',20),bg="maroon",fg="white",command=root.destroy).grid(row=13,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

root.mainloop()
