import os
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import re
from analyzer_wrapper import analyze_code as analyze_code_with_wrapper

app = Flask(__name__, template_folder='../frontend')

# Load the trained ML model
model_path = os.path.join(os.path.dirname(__file__), '../ml_models/quality_model.joblib')
try:
    quality_model = joblib.load(model_path)
except FileNotFoundError:
    quality_model = None
    print(f"Warning: Model file not found at {model_path}. ML predictions will be disabled.")

# A simple function to simulate feature extraction for ML prediction
def extract_features_for_ml(code):
    num_lines = len(code.splitlines())
    num_if_statements = len(re.findall(r'\bif\b', code))
    # This part is a simplified representation. In a real-world scenario, you'd
    # parse the code for a more accurate count.
    num_vars = len(re.findall(r'(int|char|long|float|double|bool|string)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|;)', code))
    return [num_lines, num_if_statements, num_vars]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'cpp')  # Get language, default to 'cpp'

    if not code:
        return jsonify({'report': 'No code provided.'}), 400

    # Run the appropriate static analysis based on the language
    static_report = analyze_code_with_wrapper(code, language)

    # Determine suggestions based on the static report
    suggestions = []
    if "Unused variable" in static_report:
        suggestions.append("Found unused variables. Consider removing them to improve code clarity and reduce potential bugs.")
    if "No issues found" in static_report:
        suggestions.append("Good job! Your code is free of any obvious static analysis issues.")

    # Make a prediction with the ML model
    quality_prediction = None
    quality_label = None
    if quality_model and language == 'cpp': # ML model is trained for C++
        try:
            features = extract_features_for_ml(code)
            prediction = quality_model.predict([features])[0]
            quality_prediction = float(quality_model.predict_proba([features])[0][1])  # Get probability of being good
            quality_label = "Good" if prediction == 1 else "Needs Improvement"

            if prediction == 0:
                suggestions.append("Based on our analysis, your code's complexity might be too high. Consider refactoring large functions into smaller, more manageable ones.")
        except Exception as e:
            quality_label = f"ML Prediction Error: {e}"

    response = {
        'static_report': static_report,
        'quality_score': quality_prediction,
        'quality_label': quality_label,
        'suggestions': suggestions
    }

    return jsonify(response)

if __name__ == '__main__':
    # Use a temporary port to avoid conflicts
    app.run(debug=True, port=5000)