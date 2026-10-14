# 🏥 Multiple Disease Prediction System

An end-to-end **Machine Learning** web application that predicts the likelihood of three major diseases — **Diabetes**, **Heart Disease**, and **Parkinson's Disease** — using clinical and biomedical input data. The system features a **Flask REST API** backend serving trained ML models and a modern **React + Vite** frontend with real-time risk assessment, interactive diagnostics, and an AI benchmarks dashboard.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Datasets Used](#-datasets-used)
- [Machine Learning Models & Algorithms](#-machine-learning-models--algorithms)
- [Model Performance](#-model-performance)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [API Documentation](#-api-documentation)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🎯 Problem Statement

Early detection of chronic diseases is a critical challenge in modern healthcare. Many conditions like diabetes, cardiovascular diseases, and neurodegenerative disorders progress silently, and by the time symptoms become apparent, significant damage may have already occurred.

**Key challenges this project addresses:**

1. **Diabetes** — Over 422 million people worldwide have diabetes. Early identification of at-risk individuals through metabolic biomarkers (glucose levels, BMI, insulin resistance) can enable preventive intervention.
2. **Heart Disease** — Cardiovascular disease is the #1 cause of death globally. Predicting heart disease risk from routine clinical tests (cholesterol, blood pressure, ECG data) can save lives through early treatment.
3. **Parkinson's Disease** — Affects ~10 million people worldwide. Early detection through **voice/phonatory acoustic analysis** (jitter, shimmer, harmonic-to-noise ratio) enables earlier therapeutic management.

This system provides a **non-invasive, ML-powered screening tool** that takes standard clinical measurements as input and outputs disease risk predictions with confidence scores, risk factor analysis, and clinical recommendations.

---

## 📊 Datasets Used

### 1. Pima Indians Diabetes Dataset
| Property | Details |
|----------|---------|
| **Source** | [UCI ML Repository / Jason Brownlee](https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv) |
| **Samples** | 768 |
| **Features** | 8 (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) |
| **Target** | `Outcome` — Binary (0: No Diabetes, 1: Diabetes) |
| **Preprocessing** | Biological zero imputation with column medians, class balancing via upsampling, engineered features (`Glucose×BMI`, `Age×Glucose`) |

### 2. Cleveland Heart Disease Dataset
| Property | Details |
|----------|---------|
| **Source** | [UCI ML Repository — Heart Disease](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data) |
| **Samples** | ~303 (after dropping missing values) |
| **Features** | 13 (age, sex, chest pain type, resting BP, cholesterol, fasting blood sugar, resting ECG, max heart rate, exercise-induced angina, ST depression, slope, vessels colored by fluoroscopy, thalassemia) |
| **Target** | `target` — Binary (0: No Heart Disease, 1: Heart Disease) |
| **Preprocessing** | Missing value removal, multi-class target binarized (>0 → 1) |

### 3. Oxford Parkinson's Disease Dataset
| Property | Details |
|----------|---------|
| **Source** | [UCI ML Repository — Parkinson's](https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data) |
| **Samples** | 195 |
| **Features** | 22 voice measurement features (MDVP Frequency, Jitter, Shimmer, HNR, RPDE, DFA, Spread, D2, PPE) |
| **Target** | `status` — Binary (0: Healthy, 1: Parkinson's) |
| **Preprocessing** | StandardScaler normalization |

---

## 🤖 Machine Learning Models & Algorithms

### Diabetes Prediction — Soft Voting Ensemble
```
VotingClassifier (soft voting):
├── Random Forest         (150 trees, max_depth=10)
├── Extra Trees           (150 trees, max_depth=12)
└── Gradient Boosting     (100 trees, lr=0.1, max_depth=4)
```
- **Data Pipeline:** Zero-imputation → Feature engineering (Glucose×BMI, Age×Glucose) → Class balancing (upsampling minority) → StandardScaler → Ensemble prediction
- **Split:** 70/30 train-test, stratified

### Heart Disease Prediction — Soft Voting Ensemble
```
VotingClassifier (soft voting):
├── Extra Trees           (150 trees, max_depth=6)
├── Random Forest         (120 trees, max_depth=5)
└── Linear SVM            (C=1.0, probability=True)
```
- **Data Pipeline:** StandardScaler → Ensemble prediction
- **Split:** 80/20 train-test, stratified

### Parkinson's Disease Prediction — Support Vector Machine
```
SVM (RBF Kernel):
├── C = 10.0
├── gamma = 0.1
└── probability = True
```
- **Data Pipeline:** StandardScaler → SVM prediction
- **Split:** 80/20 train-test, stratified

---

## 📈 Model Performance

| Disease | Algorithm | Accuracy | Precision | Recall | F1 Score |
|---------|-----------|----------|-----------|--------|----------|
| **Diabetes** | Ensemble (ET + RF + GB) | **87.33%** | 82.94% | 94.00% | 0.8812 |
| **Heart Disease** | Ensemble (ET + RF + SVM) | **90.00%** | 89.29% | 89.29% | 0.8929 |
| **Parkinson's** | SVM (RBF Kernel) | **94.87%** | 96.55% | 96.55% | 0.9655 |

> All models exceed the 87% accuracy threshold and are validated on held-out test sets with stratified sampling.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                │
│   ┌───────────┐  ┌──────────────┐  ┌────────────────┐  │
│   │ Diabetes  │  │ Heart Disease│  │  Parkinson's   │  │
│   │ Predictor │  │  Predictor   │  │   Predictor    │  │
│   └─────┬─────┘  └──────┬───────┘  └───────┬────────┘  │
│         │               │                  │            │
│         └───────────────┼──────────────────┘            │
│                         │ REST API Calls                │
└─────────────────────────┼───────────────────────────────┘
                          │
              ┌───────────▼───────────┐
              │   Flask REST API      │
              │   (app.py : 5000)     │
              ├───────────────────────┤
              │ /api/predict/diabetes │
              │ /api/predict/heart    │
              │ /api/predict/parkinson│
              │ /api/models-info      │
              │ /api/status           │
              └───────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
   ┌─────▼─────┐  ┌──────▼──────┐  ┌──────▼──────┐
   │ Diabetes  │  │   Heart     │  │ Parkinson   │
   │ Pipeline  │  │  Pipeline   │  │  Pipeline   │
   │ (Ensemble)│  │ (Ensemble)  │  │   (SVM)     │
   └───────────┘  └─────────────┘  └─────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **Flask** | REST API framework |
| **Flask-CORS** | Cross-origin resource sharing |
| **scikit-learn** | ML models (SVM, Random Forest, Extra Trees, Gradient Boosting, Voting Classifier) |
| **pandas / NumPy** | Data manipulation & numerical computing |
| **pickle** | Model serialization |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **Vite 8** | Build tool & dev server |
| **Lucide React** | Icon library |
| **Vanilla CSS** | Custom styling with animations & glassmorphism |

---

## 📁 Project Structure

```
multiple-disease-prediction-model/
│
├── app.py                    # Flask REST API backend (serves predictions)
├── train_models.py           # Training script for all 3 ML models
├── models_pipeline.py        # Pipeline classes (preprocessing + prediction)
├── prepare_data.py           # Dataset download & preparation script
├── verify_services.py        # Service health check utility
├── MULTIPLE DISEASE PREDICTION.py  # Original Streamlit prototype
│
├── SAVED MODEL/              # Serialized trained models & metrics
│   ├── diabetes_pipeline.pkl
│   ├── heart_pipeline.pkl
│   ├── parkinson_pipeline.pkl
│   ├── diabetes_model.sav
│   ├── heart_disease_model.sav
│   ├── parkinson_model.sav
│   └── model_metrics.json    # Accuracy, precision, recall, F1 for all models
│
├── archive/                  # Training datasets
│   ├── diabetes.csv
│   ├── heart.csv
│   └── parkinsons.csv
│
├── frontend/                 # React + Vite web UI
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Application styles
│   │   ├── index.css         # Global styles & design system
│   │   ├── components/
│   │   │   ├── Navbar.jsx         # Navigation bar with API status
│   │   │   ├── PredictorView.jsx  # Disease prediction form & results
│   │   │   ├── DiagnosticCard.jsx # Input cards for each disease
│   │   │   ├── RiskGauge.jsx      # Visual risk score gauge
│   │   │   ├── MetricsDashboard.jsx # AI model benchmarks view
│   │   │   └── ReportModal.jsx    # Downloadable diagnostic report
│   │   └── assets/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Clone the Repository
```bash
git clone https://github.com/sachinsingh111/multiple-disease-prediction-model.git
cd multiple-disease-prediction-model
```

### 2. Install Python Dependencies
```bash
pip install flask flask-cors scikit-learn pandas numpy
```

### 3. (Optional) Retrain the Models
The pre-trained models are already included in `SAVED MODEL/`. To retrain from scratch:
```bash
# Download fresh datasets
python prepare_data.py

# Train all 3 models
python train_models.py
```

### 4. Start the Flask Backend
```bash
python app.py
```
The API will start at `http://127.0.0.1:5000`.

### 5. Start the React Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend will start at `http://localhost:5173` (Vite default).

---

## 📡 API Documentation

### `GET /api/status`
Returns API health status and loaded models.
```json
{
  "status": "online",
  "service": "Multiple Disease Prediction API",
  "version": "2.0.0",
  "models_loaded": ["diabetes", "heart", "parkinson"]
}
```

### `GET /api/models-info`
Returns model metrics and sample profiles for demo predictions.

### `POST /api/predict/diabetes`
**Request Body:**
```json
{
  "Pregnancies": 6,
  "Glucose": 168.0,
  "BloodPressure": 88.0,
  "SkinThickness": 35.0,
  "Insulin": 220.0,
  "BMI": 38.2,
  "DiabetesPedigreeFunction": 0.82,
  "Age": 52
}
```
**Response:** Prediction result with risk score, severity, risk factors, and clinical recommendation.

### `POST /api/predict/heart`
**Request Body:** 13 features — `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`

### `POST /api/predict/parkinson`
**Request Body:** 22 voice measurement features — MDVP frequency, jitter, shimmer, HNR, RPDE, DFA, spread, D2, PPE

---

## ✨ Features

- **🔬 Multi-Disease Prediction** — Diabetes, Heart Disease, and Parkinson's from a single platform
- **📊 Risk Score Visualization** — Interactive risk gauge with percentage-based confidence scores
- **⚠️ Risk Factor Analysis** — Identifies and highlights specific clinical risk markers from input data
- **💊 Clinical Recommendations** — AI-generated recommendations based on prediction outcomes
- **📋 Diagnostic Reports** — Downloadable assessment reports via the Report Modal
- **📈 AI Benchmarks Dashboard** — Live display of model accuracy, precision, recall, and F1 scores
- **🎯 One-Click Demo Profiles** — Pre-loaded "Healthy" and "High Risk" sample data for instant testing
- **🌐 REST API** — Full-featured Flask API for programmatic access
- **🎨 Modern UI** — Glassmorphism design, smooth animations, and responsive layout

---

## 🔮 Future Enhancements

- [ ] Add more diseases (Liver Disease, Kidney Disease, Breast Cancer)
- [ ] Integrate deep learning models (neural networks) for improved accuracy
- [ ] Add user authentication and prediction history
- [ ] Deploy on cloud (AWS / Heroku / Render)
- [ ] Add SHAP / LIME model explainability visualizations
- [ ] Mobile-responsive PWA version

---

## 📄 License

This project is open-source and available for educational and research purposes.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/sachinsingh111">Sachin Singh</a>
</p>
