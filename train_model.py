import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load dataset
df = pd.read_csv("processed_credit_data.csv")

# Define features and target
X = df.drop(columns=["Credit Score"])
y = df["Credit Score"]

# Identify categorical and numerical features
categorical_features = ["Employment Type", "Bills Paid on Time", "Gender", "City", "Income Variability"]
numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
numerical_features = [col for col in numerical_features if col not in categorical_features]

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

# Model pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Save model
with open("credit_score_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training completed and saved as credit_score_model.pkl")