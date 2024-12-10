import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

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
