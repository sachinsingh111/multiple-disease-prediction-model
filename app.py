# -*- coding: utf-8 -*-
"""
Flask Backend REST API for Multiple Disease Prediction System
Serves predictions, model metrics, and sample demo profiles.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from models_pipeline import DiabetesPipeline, HeartPipeline, ParkinsonPipeline

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "SAVED MODEL")

# Load models and pipelines
print("Loading trained machine learning models...")
with open(os.path.join(MODEL_DIR, "diabetes_pipeline.pkl"), 'rb') as f:
    diabetes_pipeline = pickle.load(f)
with open(os.path.join(MODEL_DIR, "heart_pipeline.pkl"), 'rb') as f:
    heart_pipeline = pickle.load(f)
with open(os.path.join(MODEL_DIR, "parkinson_pipeline.pkl"), 'rb') as f:
    parkinson_pipeline = pickle.load(f)

# Load metrics
with open(os.path.join(MODEL_DIR, "model_metrics.json"), 'r') as f:
    model_metrics = json.load(f)

print("All ML models and metrics loaded successfully!")

# Sample preset data for 1-click UI demos
SAMPLE_PROFILES = {
    "diabetes": {
        "healthy": {
            "Pregnancies": 1,
            "Glucose": 92.0,
            "BloodPressure": 68.0,
            "SkinThickness": 18.0,
            "Insulin": 65.0,
            "BMI": 22.4,
            "DiabetesPedigreeFunction": 0.24,
            "Age": 28
        },
        "high_risk": {
            "Pregnancies": 6,
            "Glucose": 168.0,
            "BloodPressure": 88.0,
            "SkinThickness": 35.0,
            "Insulin": 220.0,
            "BMI": 38.2,
            "DiabetesPedigreeFunction": 0.82,
            "Age": 52
        }
    },
    "heart": {
        "healthy": {
            "age": 42,
            "sex": 1,
            "cp": 1,
            "trestbps": 118,
            "chol": 195,
            "fbs": 0,
            "restecg": 0,
            "thalach": 168,
            "exang": 0,
            "oldpeak": 0.0,
            "slope": 2,
            "ca": 0,
            "thal": 2
        },
        "high_risk": {
            "age": 62,
            "sex": 1,
            "cp": 0,
            "trestbps": 160,
            "chol": 286,
            "fbs": 1,
            "restecg": 2,
            "thalach": 108,
            "exang": 1,
            "oldpeak": 2.8,
            "slope": 1,
            "ca": 3,
            "thal": 3
        }
    },
    "parkinson": {
        "healthy": {
            "MDVP:Fo(Hz)": 204.5,
            "MDVP:Fhi(Hz)": 234.2,
            "MDVP:Flo(Hz)": 182.1,
            "MDVP:Jitter(%)": 0.0028,
            "MDVP:Jitter(Abs)": 0.00001,
            "MDVP:RAP": 0.0012,
            "MDVP:PPQ": 0.0014,
            "Jitter:DDP": 0.0036,
            "MDVP:Shimmer": 0.014,
            "MDVP:Shimmer(dB)": 0.12,
            "Shimmer:APQ3": 0.007,
            "Shimmer:APQ5": 0.008,
            "MDVP:APQ": 0.011,
            "Shimmer:DDA": 0.021,
            "NHR": 0.004,
            "HNR": 26.5,
            "RPDE": 0.38,
            "DFA": 0.65,
            "spread1": -7.2,
            "spread2": 0.11,
            "D2": 1.95,
            "PPE": 0.11
        },
        "high_risk": {
            "MDVP:Fo(Hz)": 119.99,
            "MDVP:Fhi(Hz)": 157.30,
            "MDVP:Flo(Hz)": 74.99,
            "MDVP:Jitter(%)": 0.0078,
            "MDVP:Jitter(Abs)": 0.00007,
            "MDVP:RAP": 0.0037,
            "MDVP:PPQ": 0.0055,
            "Jitter:DDP": 0.0111,
            "MDVP:Shimmer": 0.0437,
            "MDVP:Shimmer(dB)": 0.426,
            "Shimmer:APQ3": 0.0218,
            "Shimmer:APQ5": 0.0313,
            "MDVP:APQ": 0.0297,
            "Shimmer:DDA": 0.0654,
            "NHR": 0.0221,
            "HNR": 21.03,
            "RPDE": 0.4147,
            "DFA": 0.8152,
            "spread1": -4.813,
            "spread2": 0.266,
            "D2": 2.301,
            "PPE": 0.284
        }
    }
}

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "service": "Multiple Disease Prediction API",
        "version": "2.0.0",
        "models_loaded": ["diabetes", "heart", "parkinson"]
    })

@app.route('/api/models-info', methods=['GET'])
def get_models_info():
    return jsonify({
        "metrics": model_metrics,
        "sample_profiles": SAMPLE_PROFILES
    })

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    disease = request.args.get('disease')
    if disease and disease in SAMPLE_PROFILES:
        return jsonify(SAMPLE_PROFILES[disease])
    return jsonify(SAMPLE_PROFILES)

@app.route('/api/predict/diabetes', methods=['POST'])
def predict_diabetes():
    try:
        data = request.json
        features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        row = {}
        for f in features:
            if f not in data:
                return jsonify({"error": f"Missing required parameter: {f}"}), 400
            row[f] = float(data[f])
        
        df_input = pd.DataFrame([row])
        pred = int(diabetes_pipeline.predict(df_input)[0])
        proba = float(diabetes_pipeline.predict_proba(df_input)[0][1])
        
        risk_score = round(proba * 100, 1)
        
        # Risk factors analysis
        risk_factors = []
        if row['Glucose'] >= 140:
            risk_factors.append(f"High Glucose: {row['Glucose']} mg/dL (Normal: < 100 fasting, < 140 postprandial)")
        elif row['Glucose'] >= 100:
            risk_factors.append(f"Borderline Impaired Glucose: {row['Glucose']} mg/dL")
            
        if row['BMI'] >= 30:
            risk_factors.append(f"Obese BMI range: {row['BMI']} kg/m² (Normal: 18.5 - 24.9)")
        elif row['BMI'] >= 25:
            risk_factors.append(f"Overweight BMI range: {row['BMI']} kg/m²")
            
        if row['BloodPressure'] >= 90:
            risk_factors.append(f"Elevated Diastolic BP: {row['BloodPressure']} mm Hg")
            
        if row['Insulin'] >= 160:
            risk_factors.append(f"Hyperinsulinemia / Insulin Resistance marker: {row['Insulin']} IU/mL")
            
        if row['Age'] >= 45:
            risk_factors.append(f"Age Risk Factor: {int(row['Age'])} years")

        if pred == 1 or risk_score >= 50:
            status = "High Risk / Positive"
            severity = "High" if risk_score >= 70 else "Moderate"
            recommendation = "Clinical markers strongly indicate diabetic risk. Immediate fasting plasma glucose, HbA1c test, and consultation with an endocrinologist are recommended."
        else:
            status = "Low Risk / Negative"
            severity = "Low"
            recommendation = "Patient metabolic metrics are well within baseline ranges. Continue healthy dietary habits, regular physical activity, and routine annual wellness checks."

        return jsonify({
            "disease": "diabetes",
            "prediction": pred,
            "status": status,
            "severity": severity,
            "risk_score": risk_score,
            "probability": round(proba, 4),
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "input_echo": row
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict/heart', methods=['POST'])
def predict_heart():
    try:
        data = request.json
        features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        row = {}
        for f in features:
            if f not in data:
                return jsonify({"error": f"Missing required parameter: {f}"}), 400
            row[f] = float(data[f])
            
        df_input = pd.DataFrame([row])
        pred = int(heart_pipeline.predict(df_input)[0])
        proba = float(heart_pipeline.predict_proba(df_input)[0][1])
        
        risk_score = round(proba * 100, 1)
        
        risk_factors = []
        if row['oldpeak'] >= 1.5:
            risk_factors.append(f"Significant ST depression during exercise: {row['oldpeak']}")
        if row['ca'] > 0:
            risk_factors.append(f"Major coronary vessel fluoroscopy score: {int(row['ca'])}")
        if row['exang'] == 1:
            risk_factors.append("Exercise-induced angina reported")
        if row['chol'] >= 240:
            risk_factors.append(f"Hypercholesterolemia: {row['chol']} mg/dL (Desirable: < 200)")
        if row['trestbps'] >= 140:
            risk_factors.append(f"Hypertension Stage 2: {row['trestbps']} mm Hg")
        if row['thalach'] < 120 and row['age'] < 65:
            risk_factors.append(f"Blunted chronotropic heart rate response: {row['thalach']} bpm")

        if pred == 1 or risk_score >= 50:
            status = "High Risk / Positive"
            severity = "High" if risk_score >= 70 else "Moderate"
            recommendation = "Cardiovascular biomarkers show high likelihood of ischemic heart disease. Urgent referral to a cardiologist for comprehensive ECG, echocardiogram, and stress test is strongly recommended."
        else:
            status = "Low Risk / Negative"
            severity = "Low"
            recommendation = "Cardiovascular markers indicate healthy arterial function and normal cardiac stress tolerance. Maintain aerobic exercise and heart-healthy Mediterranean diet."

        return jsonify({
            "disease": "heart",
            "prediction": pred,
            "status": status,
            "severity": severity,
            "risk_score": risk_score,
            "probability": round(proba, 4),
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "input_echo": row
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict/parkinson', methods=['POST'])
def predict_parkinson():
    try:
        data = request.json
        features = [
            'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
            'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
            'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
            'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
            'spread1', 'spread2', 'D2', 'PPE'
        ]
        
        row = {}
        for f in features:
            if f not in data:
                return jsonify({"error": f"Missing required parameter: {f}"}), 400
            row[f] = float(data[f])
            
        df_input = pd.DataFrame([row])
        pred = int(parkinson_pipeline.predict(df_input)[0])
        proba = float(parkinson_pipeline.predict_proba(df_input)[0][1])
        
        risk_score = round(proba * 100, 1)
        
        risk_factors = []
        if row['MDVP:Jitter(%)'] > 0.005:
            risk_factors.append(f"Elevated frequency perturbation (Jitter): {row['MDVP:Jitter(%)']:.4f}")
        if row['MDVP:Shimmer'] > 0.03:
            risk_factors.append(f"Elevated amplitude perturbation (Shimmer): {row['MDVP:Shimmer']:.4f}")
        if row['HNR'] < 20.0:
            risk_factors.append(f"Reduced Harmonics-to-Noise Ratio: {row['HNR']:.1f} dB (Normal: > 20 dB)")
        if row['spread1'] > -5.0:
            risk_factors.append(f"Nonlinear fundamental frequency variation: {row['spread1']:.2f}")
        if row['PPE'] > 0.22:
            risk_factors.append(f"High Pitch Period Entropy: {row['PPE']:.3f}")

        if pred == 1 or risk_score >= 50:
            status = "High Risk / Positive"
            severity = "High" if risk_score >= 70 else "Moderate"
            recommendation = "Phonatory acoustic analysis displays voice tremor and perturbations characteristic of hypokinetic dysarthria in Parkinson's. Neurological motor evaluation and UPDRS assessment are recommended."
        else:
            status = "Low Risk / Negative"
            severity = "Low"
            recommendation = "Acoustic voice metrics show smooth vocal cord vibration, high harmonic clarity, and normal dynamic stability."

        return jsonify({
            "disease": "parkinson",
            "prediction": pred,
            "status": status,
            "severity": severity,
            "risk_score": risk_score,
            "probability": round(proba, 4),
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "input_echo": row
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Multiple Disease Prediction Flask API on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
