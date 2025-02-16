import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import xgboost as xgb

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

# Define XGBoost model
xgb_model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)

# Model pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", xgb_model)
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter tuning
param_grid = {
    "regressor__n_estimators": [100, 200],
    "regressor__learning_rate": [0.01, 0.1],
    "regressor__max_depth": [3, 5]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring="r2", verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Save the trained model
with open("credit_score_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("✅ Model training completed. Best parameters:", grid_search.best_params_)
print("📌 Model saved as credit_score_model.pkl")
