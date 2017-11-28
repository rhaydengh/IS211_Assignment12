
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 12, set up functions and templates, need to work in database connections and udpates"""

from flask import Flask, render_template, request, redirect, session, url_for, g, abort, flash, escape
from contextlib import closing
import sqlite3 as sql
import sys

app = Flask(__name__)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        session = request.form['username']
        return render_template('dashboard.html', username=username, password=password)
    else:
        print 'Invalid login'
        return render_template('index.html')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    return render_template('index.html')

@app.route('/student/add', methods = ['POST', 'GET'])
def addstudent():
    studentid = request.form['studentid']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    return render_template('dashboard.html', studentid=studentid, firstname=firstname, lastname=lastname)

@app.route('/quiz/add', methods = ['POST', 'GET'])
def addquiz():
    quizid = request.form['quizid']
    subject = request.form['subject']
    questions = request.form['questions']
    date = request.form['date']
    return render_template('dashboard.html', quizid=quizid, subject=subject, questions=questions, date=date)

@app.route('/results/add', methods = ['POST', 'GET'])
def addscore():
    student_id = request.form['student_id']
    quiz_id = request.form['quiz_id']
    score = request.form['score']
    return render_template('dashboard.html', student_id=student_id, quiz_id=quiz_id, score=score)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
