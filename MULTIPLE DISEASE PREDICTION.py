# -*- coding: utf-8 -*-
"""
Multiple Disease Prediction System (Streamlit App)
Predicts Diabetes, Heart Disease, and Parkinson's Disease using trained ML models.
"""

import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
from models_pipeline import DiabetesPipeline, HeartPipeline, ParkinsonPipeline

# Set page configuration
st.set_page_config(
    page_title="Multiple Disease Prediction System",
    page_icon="🩺",
    layout="wide"
)

# Resolve model directory relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "SAVED MODEL")

# Load trained pipelines
@st.cache_resource
def load_models():
    with open(os.path.join(MODEL_DIR, "diabetes_model.sav"), 'rb') as f:
        diabetes_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "heart_disease_model.sav"), 'rb') as f:
        heart_disease_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "parkinson_model.sav"), 'rb') as f:
        parkinson_model = pickle.load(f)
    return diabetes_model, heart_disease_model, parkinson_model

diabetes_model, heart_disease_model, parkinson_model = load_models()

# Navigation Sidebar
try:
    from streamlit_option_menu import option_menu
    with st.sidebar:
        selected = option_menu(
            'Multiple Disease Prediction System',
            ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinson Prediction'],
            icons=['activity', 'heart-pulse', 'person'],
            default_index=0
        )
except ImportError:
    with st.sidebar:
        st.title("Navigation")
        selected = st.selectbox(
            "Select Prediction System",
            ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinson Prediction']
        )

# ============================================================
# 1. DIABETES PREDICTION PAGE
# ============================================================
if selected == 'Diabetes Prediction':
    st.title("🩺 Diabetes Risk Prediction using ML")
    st.markdown("Enter the patient's diagnostic parameters below to assess diabetes risk.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=1, step=1)
        SkinThickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.47, step=0.01)
    with col2:
        Glucose = st.number_input("Glucose Level (mg/dL)", min_value=0.0, max_value=300.0, value=120.0, step=1.0)
        Insulin = st.number_input("Insulin Level (IU/mL)", min_value=0.0, max_value=900.0, value=80.0, step=1.0)
        Age = st.number_input("Age (years)", min_value=1, max_value=120, value=33, step=1)
    with col3:
        BloodPressure = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, max_value=200.0, value=70.0, step=1.0)
        BMI = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=70.0, value=25.5, step=0.1)

    if st.button("Predict Diabetes Risk", type="primary"):
        input_data = pd.DataFrame([{
            'Pregnancies': float(Pregnancies),
            'Glucose': float(Glucose),
            'BloodPressure': float(BloodPressure),
            'SkinThickness': float(SkinThickness),
            'Insulin': float(Insulin),
            'BMI': float(BMI),
            'DiabetesPedigreeFunction': float(DiabetesPedigreeFunction),
            'Age': float(Age)
        }])
        
        prediction = diabetes_model.predict(input_data)[0]
        proba = diabetes_model.predict_proba(input_data)[0][1]
        
        st.subheader("Diagnostic Result:")
        if prediction == 1:
            st.error(f"⚠️ Positive for Diabetes (Estimated Risk: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: Please consult an endocrinologist for HbA1c testing and lifestyle management.")
        else:
            st.success(f"✅ Negative for Diabetes (Estimated Risk: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: The patient metrics are within non-diabetic ranges. Continue maintaining a balanced diet and regular physical activity.")

# ============================================================
# 2. HEART DISEASE PREDICTION PAGE
# ============================================================
elif selected == 'Heart Disease Prediction':
    st.title("🫀 Heart Disease Risk Prediction using ML")
    st.markdown("Enter cardiovascular vital metrics below to predict coronary heart disease risk.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=55, step=1)
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80.0, max_value=250.0, value=130.0, step=1.0)
        restecg = st.selectbox("Resting ECG (0: Normal, 1: ST-T wave, 2: LV hypertrophy)", [0, 1, 2], index=0)
        slope = st.selectbox("Slope of Peak Exercise ST (0, 1, 2)", [0, 1, 2], index=1)
        thal = st.selectbox("Thalassemia (0: Normal, 1: Fixed defect, 2: Reversible defect, 3: Other)", [0, 1, 2, 3], index=2)
    with col2:
        sex = st.selectbox("Sex", ["Male (1)", "Female (0)"], index=0)
        chol = st.number_input("Serum Cholesterol (mg/dL)", min_value=100.0, max_value=600.0, value=240.0, step=1.0)
        thalach = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60.0, max_value=230.0, value=150.0, step=1.0)
        ca = st.selectbox("Major Vessels Colored by Fluoroscopy (0-3)", [0, 1, 2, 3], index=0)
    with col3:
        cp = st.selectbox("Chest Pain Type (0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic)", [0, 1, 2, 3], index=0)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No (0)", "Yes (1)"], index=0)
        exang = st.selectbox("Exercise Induced Angina", ["No (0)", "Yes (1)"], index=0)
        oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    if st.button("Predict Heart Disease Risk", type="primary"):
        sex_val = 1 if "1" in sex else 0
        fbs_val = 1 if "1" in fbs else 0
        exang_val = 1 if "1" in exang else 0
        
        input_data = pd.DataFrame([{
            'age': float(age), 'sex': float(sex_val), 'cp': float(cp),
            'trestbps': float(trestbps), 'chol': float(chol), 'fbs': float(fbs_val),
            'restecg': float(restecg), 'thalach': float(thalach), 'exang': float(exang_val),
            'oldpeak': float(oldpeak), 'slope': float(slope), 'ca': float(ca), 'thal': float(thal)
        }])
        
        prediction = heart_disease_model.predict(input_data)[0]
        proba = heart_disease_model.predict_proba(input_data)[0][1]
        
        st.subheader("Diagnostic Result:")
        if prediction == 1:
            st.error(f"⚠️ High Risk of Heart Disease Detected (Risk Probability: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: Prompt cardiology evaluation, ECG, and stress testing are strongly advised.")
        else:
            st.success(f"✅ Low Risk: Heart Appears Healthy (Risk Probability: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: Cardiovascular indicators are within standard baseline.")

# ============================================================
# 3. PARKINSON'S PREDICTION PAGE
# ============================================================
elif selected == 'Parkinson Prediction':
    st.title("🧠 Parkinson's Disease Acoustic Prediction using ML")
    st.markdown("Enter vocal frequency and acoustic measurements to screen for Parkinson's disease.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fo = st.number_input("MDVP:Fo(Hz) - Fundamental Freq", value=154.2, step=0.1)
        fhi = st.number_input("MDVP:Fhi(Hz) - Max Vocal Freq", value=197.1, step=0.1)
        flo = st.number_input("MDVP:Flo(Hz) - Min Vocal Freq", value=116.3, step=0.1)
        jitter_pct = st.number_input("MDVP:Jitter(%)", value=0.006, format="%.5f")
        jitter_abs = st.number_input("MDVP:Jitter(Abs)", value=0.00004, format="%.6f")
        rap = st.number_input("MDVP:RAP", value=0.003, format="%.5f")
        ppq = st.number_input("MDVP:PPQ", value=0.003, format="%.5f")
        ddp = st.number_input("Jitter:DDP", value=0.009, format="%.5f")
    with col2:
        shimmer = st.number_input("MDVP:Shimmer", value=0.029, format="%.5f")
        shimmer_db = st.number_input("MDVP:Shimmer(dB)", value=0.28, step=0.01)
        apq3 = st.number_input("Shimmer:APQ3", value=0.015, format="%.5f")
        apq5 = st.number_input("Shimmer:APQ5", value=0.017, format="%.5f")
        apq = st.number_input("MDVP:APQ", value=0.024, format="%.5f")
        dda = st.number_input("Shimmer:DDA", value=0.046, format="%.5f")
        nhr = st.number_input("NHR - Noise-to-Harmonics", value=0.024, format="%.5f")
    with col3:
        hnr = st.number_input("HNR - Harmonics-to-Noise", value=21.8, step=0.1)
        rpde = st.number_input("RPDE - Nonlinear Complexity", value=0.49, step=0.01)
        dfa = st.number_input("DFA - Signal Fractal Scaling", value=0.71, step=0.01)
        spread1 = st.number_input("spread1 - Nonlinear Measure 1", value=-5.68, step=0.1)
        spread2 = st.number_input("spread2 - Nonlinear Measure 2", value=0.22, step=0.01)
        d2 = st.number_input("D2 - Correlation Dimension", value=2.38, step=0.01)
        ppe = st.number_input("PPE - Pitch Period Entropy", value=0.20, step=0.01)

    if st.button("Predict Parkinson's Risk", type="primary"):
        input_data = pd.DataFrame([{
            'MDVP:Fo(Hz)': fo, 'MDVP:Fhi(Hz)': fhi, 'MDVP:Flo(Hz)': flo,
            'MDVP:Jitter(%)': jitter_pct, 'MDVP:Jitter(Abs)': jitter_abs,
            'MDVP:RAP': rap, 'MDVP:PPQ': ppq, 'Jitter:DDP': ddp,
            'MDVP:Shimmer': shimmer, 'MDVP:Shimmer(dB)': shimmer_db,
            'Shimmer:APQ3': apq3, 'Shimmer:APQ5': apq5, 'MDVP:APQ': apq,
            'Shimmer:DDA': dda, 'NHR': nhr, 'HNR': hnr, 'RPDE': rpde,
            'DFA': dfa, 'spread1': spread1, 'spread2': spread2,
            'D2': d2, 'PPE': ppe
        }])
        
        prediction = parkinson_model.predict(input_data)[0]
        proba = parkinson_model.predict_proba(input_data)[0][1]
        
        st.subheader("Diagnostic Result:")
        if prediction == 1:
            st.error(f"⚠️ Acoustic Markers Consistent with Parkinson's (Risk: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: Neurological motor examination and specialist consultation are recommended.")
        else:
            st.success(f"✅ Acoustic Markers are Normal (Risk: {proba*100:.1f}%)")
            st.markdown("- **Recommendation**: Vocal patterns exhibit normal acoustic stability and harmonic properties.")
