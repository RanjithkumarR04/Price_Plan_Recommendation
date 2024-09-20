import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset
file_path = 'CDR-Call-Details.csv'
df = pd.read_csv(file_path)

# Feature Engineering: Create additional features
df['Total Mins'] = df['Day Mins'] + df['Eve Mins'] + df['Night Mins'] + df['Intl Mins']
df['Total Calls'] = df['Day Calls'] + df['Eve Calls'] + df['Night Calls'] + df['Intl Calls']
df['Total Charge'] = df['Day Charge'] + df['Eve Charge'] + df['Night Charge'] + df['Intl Charge']

# Selecting relevant features for model training
feature_columns = ['Account Length', 'VMail Message', 'Total Mins', 'Total Calls', 'Total Charge', 'CustServ Calls']
X = df[feature_columns]
y = df['Churn'].astype(int)  # Using 'Churn' as the target variable

# Normalizing the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model Building: Train a RandomForestClassifier
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the model and scaler
joblib.dump(model, 'priceplan_recommendation/app/files/random_forest_model.pkl')
joblib.dump(scaler, 'priceplan_recommendation/app/files/scaler.pkl')

print("Model and scaler files have been saved.")
