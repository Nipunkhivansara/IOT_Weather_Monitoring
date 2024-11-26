# app.py

from flask import Flask, render_template, jsonify
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np

app = Flask(__name__)

# Load the model (for simplicity, assume the model is already trained and saved as 'model.pkl')
with open('models/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Route for the main page (Frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the model prediction (API endpoint for temperature, humidity, light intensity, air quality)
@app.route('/predict', methods=['GET'])
def predict():
    # Example: Get the data to predict from query params (for simplicity, we're hardcoding it)
    hour = 12  # Assume 12 PM as an example input
    light_intensity = 350
    air_quality = 60
    print("here")
    # Use the trained model to predict temperature, humidity (you can extend this with other features)
    prediction = model.predict([[hour, light_intensity, air_quality]])  # Example input data
    
    # Return predictions in JSON format
    return jsonify({
        'predicted_temp': prediction[0]  # Assuming the model predicts temperature
    })

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
