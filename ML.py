import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

#Enter the right directory to run the program
print(os.getcwd())
os.chdir('ML2024')
print(os.getcwd())

# Load the dataset
data = pd.read_csv("weather_flights.csv")

# Create the binary target column
data['accident'] = (data['fat.'] > 0).astype(int)

# Select features and target variable
# Features: Weather indicators
features = ['DP1X', 'EMXP', 'PRCP']
# Target: 'accident' column
target = 'accident'

# Check for missing values and handle them
if data[features].isnull().any().any():
    data[features] = data[features].fillna(data[features].median())  # Fill missing values with median

# Split the data into training and testing sets
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save the trained model to a file
joblib.dump(model, "flight_accident_predictor.pkl")
print("Model saved as flight_accident_predictor.pkl")

# Example of loading the model (optional)
# loaded_model = joblib.load("flight_accident_predictor.pkl")

# Predict severity of flying in weather
import numpy as np

# Load the trained model (if already saved)
model = joblib.load('flight_accident_predictor.pkl')

def test(DP1X, EMXP, PRCP):
    # New input data for prediction
    new_input_df = pd.DataFrame([[DP1X, EMXP, PRCP]], columns=['DP1X', 'EMXP', 'PRCP'])

    # Make a prediction
    prediction = model.predict(new_input_df)

    # Output the predicted class
    print(f"Predicted class: {prediction[0]}")

    #Output description
    if prediction[0] == 0:
        print(f"It is predicted that a crash would be non-fatal given these conditions: DP1X={DP1X} EMXP={EMXP} PRCP={PRCP}\n")
    else:
        print(f"It is predicted that a crash would be fatal given these conditions: DP1X={DP1X} EMXP={EMXP} PRCP={PRCP}\n")

# New input data for prediction ex. (VCA incident with 0 fatalities)
test(DP1X=20.0, EMXP=106.7, PRCP=1813.4)
# New input data for prediction ex. (ARN incident with 5 fatalities) 0, 24, 397.1
test(DP1X=0, EMXP=24, PRCP=397.1)