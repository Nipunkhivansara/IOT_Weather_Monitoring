import requests
import random
import time

# URL for the API endpoint
API_URL = "http://127.0.0.1:5000/api/data"

# Function to simulate sending data every 5 seconds
def simulate_data():
    while True:
        # Generate random values for hour, pressure, altitude, temperature, and humidity
        hour = random.randint(0, 23)  # Random hour between 0 and 23
        pressure = random.uniform(900, 1100)  # Random pressure between 900 and 1100 hPa
        altitude = random.uniform(0, 3000)  # Random altitude between 0 and 3000 meters
        temperature = random.uniform(-10, 40)  # Random temperature between -10 and 40 °C
        humidity = random.uniform(0, 100)  # Random humidity between 0 and 100%

        # Create the query parameters
        params = {
            'hour': hour,
            'pressure': pressure,
            'altitude': altitude,
            'temperature': temperature,
            'humidity': humidity
        }

        try:
            # Send a GET request to the Flask API endpoint
            response = requests.get(API_URL, params=params)

            # Print the response to check if it was successful
            if response.status_code == 200:
                print(f"Data inserted successfully: {params}")
            else:
                print(f"Failed to insert data: {response.text}")
        except Exception as e:
            print(f"Error during request: {e}")

        # Wait for 5 seconds before sending the next request
        time.sleep(5)

# Start the simulation
if __name__ == "__main__":
    simulate_data()
