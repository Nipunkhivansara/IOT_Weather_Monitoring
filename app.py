# app.py

from flask import Flask, render_template, jsonify, request
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np
import pandas as pd
import os
import subprocess

app = Flask(__name__)
EXCEL_FILE = 'collected_data.xlsx'
MODEL_FILE = 'models/model.pkl'

# Load the model if it exists, otherwise initialize a new model
if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, 'rb') as model_file:
        model = pickle.load(model_file)

if not os.path.exists(EXCEL_FILE):
    # Initialize the DataFrame with the required columns and save it
    df = pd.DataFrame(columns=["Timestamp", "Hour", "Pressure", "Altitude", "Temperature", "Humidity"])
    df.to_excel(EXCEL_FILE, index=False)

# Route for the main page (Frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the model prediction (API endpoint for temperature, humidity, light intensity, air quality)
@app.route('/predict', methods=['GET'])
def predict():
    # Example: Get the data to predict from query params (for simplicity, we're hardcoding it)
    hour = int(request.args.get('hour', 12))  # Default hour to 12 if not provided
    pressure = float(request.args.get('pressure', 1013))  # Default pressure to 1013 hPa
    altitude = float(request.args.get('altitude', 100))  # Default altitude to 100 meters
    humidity = float(request.args.get('humidity', 60))

    # Use the trained model to predict temperature, humidity (you can extend this with other features)
    prediction = model.predict([[hour, pressure, altitude, humidity]])  # Example input data
    
    # Return predictions in JSON format
    return jsonify({
        'predicted_temp': prediction[0]  # Assuming the model predicts temperature
    })

@app.route('/train_model', methods=['GET'])
def train_model():
    try:
        # Call the train_model.py script
        subprocess.run(['python', 'train_model.py'], check=True)
        return jsonify({"message": "Model trained successfully!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error in training model: " + str(e)}), 500


# New route to insert data into Excel when it is provided by the client
@app.route('/api/data', methods=['GET'])
def insert_data():
    try:
        # Get the data from the query parameters
        timestamp = pd.Timestamp.now()
        hour = int(request.args.get('hour'))
        pressure = float(request.args.get('pressure'))
        altitude = float(request.args.get('altitude'))
        temperature = float(request.args.get('temperature'))
        humidity = float(request.args.get('humidity'))

        # Append the data to the Excel file
        new_data = {
            "Timestamp": timestamp,
            "Hour": hour,
            "Pressure": pressure,
            "Altitude": altitude,
            "Temperature": temperature,
            "Humidity": humidity
        }
        
        # Read the existing data from the Excel file
        df = pd.read_excel(EXCEL_FILE)
        df = df._append(new_data, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({"message": "Data inserted successfully", "data": new_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Route to fetch data for graphing
@app.route('/get_data_for_graphs', methods=['GET'])
def get_data_for_graphs():
    try:
        df = pd.read_excel(EXCEL_FILE)
        if df.empty:
            return jsonify({"error": "No data available in Excel"}), 400
        
        # Extract data for the graphs
        data = {
            "hour": df["Hour"].tolist(),
            "pressure": df["Pressure"].tolist(),
            "altitude": df["Altitude"].tolist(),
            "temperature": df["Temperature"].tolist(),
            "humidity": df["Humidity"].tolist(),
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
