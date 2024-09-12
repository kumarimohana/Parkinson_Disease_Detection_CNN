import os
from flask import Flask, jsonify, session, url_for, current_app
from flask import Blueprint, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import requests
from models import create_healthform_table, create_users_table
import mysql.connector
import cv2
import numpy as np
from skimage.feature import hog
import openai

from werkzeug.utils import secure_filename
from website import create_app
from tensorflow.keras.models import load_model

openai.api_key = 'sk-proj-LsjYHSFwsQ2R5SmVuwUUT3BlbkFJdbZUh5t527pSJhTxI44l'

app = Flask(__name__)
# Define upload directory

UPLOAD_FOLDER = os.path.join('website\static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)






connection = mysql.connector.connect(host='localhost',port='3306',database='parkinson',
                                     user='root',password='system',auth_plugin='mysql_native_password')
db_cursor=connection.cursor()
'''
#db_cursor = db_connection.cursor()
# Configure MySQL connection
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'system'
app.config['MYSQL_DB'] = 'parkinson'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Use dictionary cursor for easier data access
mysql.init_app(app)
'''
# Create users table if it doesn't exist
with app.app_context():
    create_users_table()
    create_healthform_table()

app = create_app()
@app.route('/')
def index():
    return url_for('views.home')

# Define routes to render templates

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        password = request.form['password']
        db_cursor.execute("INSERT INTO users (username, email, date, password) VALUES (%s, %s, %s, %s)", (name, email, date, password))
        connection.commit()
        return render_template('login.html')

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = db_cursor.fetchone()
        print("details recived")
        if user:
            session['email'] = email
            print("user registred")
            return render_template('upload.html')
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method=="POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phonenumber']
        bp = request.form['bloodPressure']
        sugar = request.form['bloodSugar']
        histroy = request.form['healthHistory']
        db_cursor.execute("INSERT INTO healthform (name, age, gender, phonenumber, bloodPressure, bloodSugar,healthHistory ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, age, gender, phone, bp, sugar, histroy))
        connection.commit()
        return render_template('upload.html')  
    return render_template('main.html') 
model = load_model('parkinson_disease_detection.pkl')

# Define labels for predictions
labels = ['Healthy', 'Parkinson']
'''
def preprocess_image(image):
    # Resize image to match model input size
    image = cv2.resize(image, (128, 128))
    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Normalize pixel values
    image = image / 255.0
    # Expand dimensions to match model input shape
    image = np.expand_dims(image, axis=0)
    image = np.expand_dims(image, axis=-1)
    return image
'''
def preprocess_image(image_path):
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise Exception("Failed to read image")

        # Resize image
        image = cv2.resize(image, (128, 128))

        # Convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Normalize pixel values
        image = image / 255.0

        # Expand dimensions to match model input shape
        image = np.expand_dims(image, axis=0)
        image = np.expand_dims(image, axis=-1)

        return image
    except Exception as e:
        print("Error processing image:", e)
        return None

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Check if age is provided
        age = request.form.get('age')
        if not age:
            return render_template('upload.html', prediction='Please provide your age')
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('result.html', prediction='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('result.html', prediction='No selected file')

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        # Check if the person is older than 20
        age = int(age)
        if age <= 20:
            return render_template('result.html', prediction='You must be older than 20 to take the test',image_file=file.filename)


        # Preprocess image
        processed_image = preprocess_image(file_path)

        # Make prediction
        prediction = model.predict(processed_image)
        predicted_label = labels[np.argmax(prediction)]

        return render_template('result.html', prediction=predicted_label, image_file=file.filename)
    
@app.route('/suggestion_form')
def suggestion_form():
    # Render your suggestion_form.html template
    return render_template('suggestion_form.html')





if __name__ == '__main__':
    app.run(debug=True)

