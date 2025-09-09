import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os
import re

# A function to simulate feature extraction from code
def extract_features(code):
    num_lines = len(code.splitlines())
    num_if_statements = len(re.findall(r'\bif\b', code))
    num_vars = len(re.findall(r'(int|char|long|float|double|bool|string)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|;)', code))
    return [num_lines, num_if_statements, num_vars]

# --- Simulated Data Generation ---
# In a real project, this would be data from real codebases.
# We'll generate data points with features (lines, ifs, vars) and a quality label (0=bad, 1=good)
X = np.array([
    # "Good" code examples (low complexity, few issues)
    [20, 2, 5],
    [15, 1, 3],
    [30, 3, 10],
    [50, 5, 15],
    [45, 4, 12],
    [25, 2, 8],
    # "Bad" code examples (high complexity, more issues)
    [100, 20, 30],
    [80, 15, 25],
    [150, 30, 40],
    [90, 18, 28],
    [120, 25, 35],
])
y = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]) # 1 = Good, 0 = Bad

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2f}")

# Save the trained model to a file
model_path = os.path.join(os.path.dirname(__file__), 'quality_model.joblib')
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")

# A function to load the model and make a prediction
def predict_quality(code_string):
    features = extract_features(code_string)
    features_2d = np.array(features).reshape(1, -1)
    prediction = model.predict(features_2d)
    return prediction[0]