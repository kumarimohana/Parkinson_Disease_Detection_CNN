import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from skimage.feature import hog
import openai

from sklearn.decomposition import PCA
import pickle

# Create a blueprint for your views
views_bp = Blueprint('views', __name__)

# Define routes to render templates
@views_bp.route('/')
def home():
    return render_template('home.html')

@views_bp.route('/faq')
def faq():
    return render_template('faq.html')

@views_bp.route('/about')
def about():
    return render_template('about.html')

@views_bp.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@views_bp.route('/contact')
def contact():
    return render_template('contact.html')
'''
@views_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        
        # Get the file
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        
        # Check file extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            print("File saved at:", file_path)
            
            # Load the trained models
            logistic_regression_model_path = 'logistic_regression_model_second.pkl'
            random_forest_model_path = 'random_forest_model_second.pkl'

            print("Loading models...")

            with open(logistic_regression_model_path, 'rb') as f:
                logistic_regression = pickle.load(f)

            with open(random_forest_model_path, 'rb') as f:
                random_forest = pickle.load(f)

            print("Models loaded.")

            # Preprocess the uploaded image and extract features
            image_features = preprocess_image(file_path)

            print("Image features extracted.")

            # Apply PCA for dimensionality reduction
            pca = PCA(n_components=2)  # Adjust the number of components as needed
            image_features_reduced = pca.fit_transform([image_features])

            print("Dimensionality reduction completed.")

            # Predict using logistic regression
            logistic_regression_prediction = logistic_regression.predict(image_features_reduced)

            print("Logistic regression prediction:", logistic_regression_prediction)

            # Predict using random forest
            random_forest_prediction = random_forest.predict(image_features_reduced)

            print("Random forest prediction:", random_forest_prediction)

            # Combine predictions using average voting
            final_prediction = (logistic_regression_prediction + random_forest_prediction) / 2

            print("Final prediction:", final_prediction)

            # Determine the final prediction label
            prediction_label = 'Parkinson' if np.round(final_prediction)[0] == 1 else 'Healthy'

            print("Prediction label:", prediction_label)

            # Render the template with prediction result
            return render_template('prediction_result.html', prediction=prediction_label, filename=filename)

    return render_template('upload.html')
'''
@views_bp.route('/logout')
def logout():
    return render_template('logout.html')

@views_bp.route('/predict')
def predict():
    return render_template('predict.html')

# Function to preprocess the image and extract features
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, (128, 128))
    hog_features = hog(resized_image, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', feature_vector=True)
    return hog_features

# Function to check allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
