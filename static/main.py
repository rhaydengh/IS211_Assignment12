
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 12, database doesn't update on dashboard until some data is entered,
still working on view and add grades"""

from flask import Flask, render_template, request, redirect, session, url_for, g, abort, flash, escape
from contextlib import closing
import sqlite3 as sql
import sys

DATABASE = 'hw12.db'
DEBUG = True
SECRET_KEY = "key"
USERNAME = "admin"
PASSWORD = "password"

app = Flask(__name__)
app.config.from_object(__name__)


conn = sql.connect("hw12.db", timeout=5)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS students;")
cursor.execute("CREATE TABLE students (studentid INTEGER PRIMARY KEY AUTOINCREMENT,"
               "firstname text not null,lastname text not null);")
cursor.execute("INSERT INTO students VALUES(1, 'John', 'Smith');")


cursor.execute("DROP TABLE IF EXISTS quizzes;")
cursor.execute("CREATE TABLE quizzes(quizid INTEGER PRIMARY KEY,"
               "subject text not null,questions INTEGER not null,date text not null)")
cursor.execute("INSERT INTO quizzes VALUES(1, 'Python Basics', 5, 'Feb. 5, 2015');")


cursor.execute("DROP TABLE IF EXISTS grades;")
cursor.execute("CREATE TABLE grades(student_id INTEGER not null,"
               "quiz_id INTEGER not null,score INTEGER not null)")
cursor.execute("INSERT INTO grades VALUES(1, 1, 85);")


conn.commit()

def connect_db():
    return sql.connect(app.config['DATABASE'])

@app.before_request
def before_request(t
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        ):
    g.db = connect_db()

@app.teardown_requesdb.close()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']@app.route('/results/add', methods=['GET', 'POST'])
def newgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    elif request.method == 'POST':
        g.db.execute('insert into grades (student_id, quiz_id, score) values (?, ?, ?)', 
                     [request.form['student_id'], request.form['quiz_id'], request.form['score']])
        g.db.commit()
    return redirect(url_for('dashboard'))
    if username == 'admin' and password == 'password':
        session = request.form['username']
        return render_template('dashboard.html', username=username, password=password)
    else:
        print 'Invalid login'
        return render_template('index.html')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    return render_template('index.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    conns = g.db.execute('select studentid, firstname, lastname from students')
    students = [dict(studentid = row[0], firstname = row[1], lastname = row[2])
                    for row in conns.fetchall()]
    connq = g.db.execute('select quizid, subject, questions, date from quizzes')
    quizzes = [dict(quizid=row[0], subject=row[1], questions=row[2], date=row[3])
               for row in connq.fetchall()]
    conng =  g.db.execute('select student_id, quiz_id, score from grades')
    grades = [dict(student_id=row[0], quiz_id=row[1], score=row[2])
               for row in conng.fetchall()]
    return render_template("dashboard.html", students = students, quizzes = quizzes, grades=grades)

@app.route('/student/add', methods=['GET', 'POST'])
    def newstudent():    
        if request.method == 'POST':        
            g.db.execute('insert into students (firstname, lastname) values (?, ?)',                 
                         [request.form['firstname'], request.form['lastname']])        
            g.db.commit()        
            return redirect(url_for('dashboard'))    
        return render_template("addstudent.html")
       
@app.route('/quiz/add', methods=['GET', 'POST'])
    def newquiz():    
        if request.method == 'POST':        
            g.db.execute('insert into quizzes (subject, questions, date) values (?, ?, ?)',                     
                         [request.form['subject'], request.form['questions'],request.form['date']])        
            g.db.commit()        
            return redirect(url_for('dashboard'))
        return render_template('addquiz.html')


@app.route('/results/add', methods=['GET', 'POST'])
    def newgrade():    
        if request.method == 'POST':        
            g.db.execute('insert into grades (student_id, quiz_id, score) values (?, ?, ?)',                     
                         [request.form['student_id'], request.form['quiz_id'], request.form['score']])        
            g.db.commit()        
            return redirect(url_for('dashboard'))    
        return render_template('addgrade.html')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
