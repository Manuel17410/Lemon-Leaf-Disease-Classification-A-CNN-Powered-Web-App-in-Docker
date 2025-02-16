from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
import os

# Disable GPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)

# Load the model once when the server starts
model = tf.keras.models.load_model('model.keras')

# List of classes corresponding to the prediction index
classes = [
    "Anthracnose", 
    "Bacterial Blight", 
    "Citrus Canker", 
    "Curl Virus", 
    "Deficiency Leaf", 
    "Dry Leaf", 
    "Healthy Leaf", 
    "Sooty Mould", 
    "Spider Mites"
]

# Function to preprocess the image
def preprocess_input(input_image):
    img = image.load_img(input_image, target_size=(256, 256))  # Adjust size if needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize
    return img_array

# Define a route to upload the image via HTML form
@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML page

# Define a POST route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Read the file into a BytesIO stream
    img = BytesIO(file.read())

    # Preprocess the image and make prediction
    processed_image = preprocess_input(img)  # Preprocess the image
    prediction = model.predict(processed_image)  # Make prediction
    predicted_class = int(np.argmax(prediction, axis=1)[0])  # Get class index

    # Map the predicted index to the corresponding sickness name
    prediction_name = classes[predicted_class]

    # Render the result on a new page
    return render_template('result.html', prediction=prediction_name)

if __name__ == '__main__':
    app.run(debug=True)






