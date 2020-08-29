from flask import Flask, jsonify, g
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
import random
import re
import json

from formMiddleware import FormMiddleware
from formMiddleware_ import hello_middleware, validate_register


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.debug = True

# app.wsgi_app = FormMiddleware(app.wsgi_app)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Visitor'}
    return render_template('index.html', title='Home', user=user)




@app.route('/test', methods=["POST"])
@hello_middleware
def test():
    return f"Hello Test\nTokens: \n{g.token}"

# @app.route('/test', methods=["POST"])
# def test():
#     # return "test"
#     temp = request.environ['test']
#     json_ = json.dumps(temp, indent = 4)
#     return json_


@app.route('/register', methods=["GET", "POST"])
@validate_register
def register():
    session.pop('TeamName', None)  # delete visits
    if request.method == 'POST':

        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        TeamName = request.form['teamname']
        name1 = request.form['name1']
        name2 = request.form['name2']
        name3 = request.form['name3']
        name4 = request.form['name4']
        name5 = request.form['name5']
        phone1 = request.form['phone1']
        phone2 = request.form['phone2']
        phone3 = request.form['phone3']
        phone4 = request.form['phone4']
        phone5 = request.form['phone5']
        inst1 = request.form['inst1']
        inst2 = request.form['inst2']
        inst3 = request.form['inst3']
        inst4 = request.form['inst4']
        inst5 = request.form['inst5']
        email = request.form['email']
        Password = request.form['password']
        RePassword = request.form['re-password']

        isName1Valid = validate(name1, "/^[A-Z][A-Za-z]+$/")

        # Checking whether TeamName is already taken
        cursor = conn.execute(
            'Select count(*) from Team where TeamName="%s"' % TeamName)

        # Redirects back to registration page if name already taken or password confirmation does not match
        if (Password != RePassword) or (cursor.fetchone()[0] > 0):
            return redirect(url_for('register'))

        # inserting team into team table, remaining 3 values are 0 by default
        cursor = conn.execute('Insert into Team values ("%s","%s","%s",0,0,0)' % (
            TeamName, sha256_crypt.hash(Password), email))

        # inserting participants into participant table
        cursor = conn.execute('Insert into Participant values ("%s","%s","%s", "%s")' % (
            name1, phone1, inst1, TeamName))
        cursor = conn.execute('Insert into Participant values ("%s","%s","%s", "%s")' % (
            name2, phone2, inst2, TeamName))
        cursor = conn.execute('Insert into Participant values ("%s","%s","%s", "%s")' % (
            name3, phone3, inst3, TeamName))
        cursor = conn.execute('Insert into Participant values ("%s","%s","%s", "%s")' % (
            name4, phone4, inst4, TeamName))
        cursor = conn.execute('Insert into Participant values ("%s","%s","%s", "%s")' % (
            name5, phone5, inst5, TeamName))
        conn.commit()
        conn.close()
        return redirect(url_for('success', title="registered"))
    return render_template('register.html')


@app.route('/success/<title>', methods=["GET", "POST"])
def success(title):
    return render_template('success.html', value=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('TeamName', None)  # delete visits
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            'Select * from Team where TeamName="%s" and isVerified=1' % request.form['username'])
        res = cursor.fetchone()
        conn.close()
        if res != None:
            if (res['TeamName'] == request.form['username'] and
                    sha256_crypt.verify(request.form['password'], res['Password'])):
                session['TeamName'] = request.form['username']
                return redirect(url_for('success', title="login"))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('TeamName', None)  # delete visits
    return redirect(url_for('success', title="logout"))


@app.route('/upload')
def upload():
    if 'TeamName' not in session:
        return redirect(url_for('index'))
    return render_template('upload.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    if 'TeamName' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            'Select * from Team where TeamName="%s"' % session['TeamName'])
        res = cursor.fetchone()
        attempts = res["DailyLimit"]
        if attempts == 5:
            return render_template('submission,html', attempts=5, accuracy=-1)
        conn.execute('update team set DailyLimit=%s where TeamName="%s"' %
                     (attempts+1, session['TeamName']))

        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)

        # find accuracy here
        accuracy = (random.random()*100)

        conn.execute('insert into Leaderboard values ("%s",%s,"%s")' %
                     (session['TeamName'], accuracy, filename))
        conn.commit()
        conn.close()
        return render_template('submission.html', attempts=(attempts+1), accuracy=accuracy)
    return redirect(url_for('index'))


@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    #results = conn.execute("SELECT ROW_NUMBER() OVER (ORDER BY Accuracy) AS Row, * FROM Leaderboard").fetchall()
    results = conn.execute(
        "SELECT ROW_NUMBER() OVER (ORDER BY Accuracy desc) AS Row, * FROM (select TeamName, Max(Accuracy) as Accuracy from Leaderboard group by TeamName)").fetchall()
    #
    conn.close()
    return render_template('leaderboard.html', result=results)


@app.route('/approve/<TeamName>')
def approve(TeamName):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    results = conn.execute(
        'Update Team set isVerified=1 where TeamName="%s"' % TeamName)
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'TeamName' in session:
        team = session['TeamName']
        unverified = None
        if (session['TeamName'] == 'admin'):
            user_type = 'admin'
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            unverified = conn.execute(
                'select * from Team where isVerified=0').fetchall()
            conn.close()
        else:
            user_type = 'team'
        return render_template('dashboard.html', user_type=user_type, team=team, result=unverified)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
