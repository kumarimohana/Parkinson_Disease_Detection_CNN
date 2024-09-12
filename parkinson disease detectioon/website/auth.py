from flask import Blueprint, Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import mysql.connector
from website import create_app
'''
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="system",
    database="parkinson"
)
db_cursor = db_connection.cursor()
'''
auth_bp = Blueprint('auth', __name__)
'''
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        date = request.form['date']
        password = request.form['password']
        print(name)
        db_cursor.execute("INSERT INTO user (username, email, date, password) VALUES (%s, %s, %s, %s)", (name, email, date, password))
        db_connection.commit()
        return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['loginUsername']
        password = request.form['loginPassword']
        db_cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = db_cursor.fetchone()
        print("details recived")
        if user:
            session['email'] = email
            print("user registred")
            return render_template('main.html')
    return render_template('login.html')
'''
'''
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # Extract data from the login form
        username = request.form['loginUsername']
        password = request.form['loginPassword']
    
        print("im getting here")
        # Connect to the database
        mysql = MySQL(create_app)
        cur = mysql.connection.cursor()

        # Query to check if the username and password match a record in the database
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        rows = cur.fetchall()

# Iterate over the rows and print each row
        for row in rows:
           print("Username:", row[0])
           print("Email:", row[1])
           print("Date:", row[2])
           print("Password:", row[3])
        # Close cursor
        cur.close()

        if user:
            # User exists, perform login actions
            # For example, set session variables or redirect to a dashboard
            return redirect(url_for('views.main'))
        else:
            # User does not exist or password is incorrect
            # Handle authentication failure (e.g., show error message)
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    print('sign up data entry started')
    if request.method == 'POST':
        # Extract data from the signup form
        print("enter to signup form")
        username = request.form['username']
        email = request.form['email']
        date = request.form['date']
        password = request.form['password']
        

        # Connect to the database
        mysql = MySQL(create_app)
        cur = mysql.connection.cursor()

        # Insert user data into the database
        cur.execute("INSERT INTO users (username, email, date, password) VALUES (%s, %s, %s, %s)", (username, email, date, password))
        mysql.connection.commit()
        

        # Close cursor
        cur.close()

        # Redirect to login page after successful signup
        return redirect(url_for('views.home'))


    return render_template('login.html')

'''

