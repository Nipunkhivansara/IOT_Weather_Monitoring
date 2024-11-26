from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
import os

# Path to the Excel file
EXCEL_FILE = 'collected_data.xlsx'

def retrieve_data():
    """
    Retrieves all the data from the Excel file.
    """
    if not os.path.exists(EXCEL_FILE):
        print("No data file found.")
        return None, None

    try:
        df = pd.read_excel(EXCEL_FILE)
        if df.empty:
            print("The data file is empty.")
            return None, None

        # Extract features (X) and target (y)
        X = df[["Hour", "Pressure", "Altitude", "Humidity"]].values
        y = df["Temperature"].values if "Temperature" in df.columns else None

        if y is None:
            print("Temperature data not found in the Excel file.")
            return None, None

        return X, y
    except Exception as e:
        print("Error occurred while reading the Excel file:", str(e))
        return None, None

# Retrieve the data from the Excel file
X, y = retrieve_data()

if X is not None and y is not None:
    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Save the trained model to a file
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully.")
else:
    print("Model training failed due to missing or invalid data.")
