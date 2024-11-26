# Save the model (run this in a separate script or in a Jupyter notebook)

from sklearn.linear_model import LinearRegression
import pickle
import numpy as np

# Sample data for training (hour, light intensity, air quality) and target (temperature)
X = np.array([[12, 350, 60], [13, 400, 55], [14, 300, 70], [15, 450, 65]])  # Example features
y = np.array([25.5, 26.0, 27.2, 28.1])  # Example target values (temperature)

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model to a file
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
