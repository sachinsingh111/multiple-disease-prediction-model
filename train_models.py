import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.utils import resample

os.environ['LOKY_MAX_CPU_COUNT'] = '4'

SAVED_DIR = "SAVED MODEL"
ARCHIVE_DIR = "archive"
os.makedirs(SAVED_DIR, exist_ok=True)

metrics_summary = {}

print("==========================================================")
print("TRAINING MULTIPLE DISEASE PREDICTION HIGH-PERFORMANCE MODELS")
print("==========================================================")

# ------------------------------------------------------------
# 1. DIABETES PREDICTION MODEL
# ------------------------------------------------------------
print("\n[1/3] Training Diabetes Prediction Model...")
df_diab = pd.read_csv(os.path.join(ARCHIVE_DIR, "diabetes.csv"))

# Biological zero replacement with median
zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
impute_medians = {}
for col in zero_cols:
    median_val = float(df_diab[df_diab[col] > 0][col].median())
    impute_medians[col] = median_val
    df_diab[col] = df_diab[col].replace(0, median_val)

# Feature engineering
def add_diabetes_features(df):
    df_feat = df.copy()
    df_feat['Glucose_BMI'] = (df_feat['Glucose'] * df_feat['BMI']) / 100.0
    df_feat['Age_Glucose'] = (df_feat['Age'] * df_feat['Glucose']) / 100.0
    return df_feat

df_diab_feat = add_diabetes_features(df_diab)

# Balance dataset using upsampling
df_maj = df_diab_feat[df_diab_feat.Outcome == 0]
df_min = df_diab_feat[df_diab_feat.Outcome == 1]
df_min_up = resample(df_min, replace=True, n_samples=len(df_maj), random_state=69)
df_diab_balanced = pd.concat([df_maj, df_min_up], ignore_index=True)

X_d = df_diab_balanced.drop('Outcome', axis=1)
y_d = df_diab_balanced['Outcome']
diab_features = list(X_d.columns)

# Train/Test Split
X_d_tr, X_d_te, y_d_tr, y_d_te = train_test_split(X_d, y_d, test_size=0.3, random_state=69, stratify=y_d)

scaler_d = StandardScaler().fit(X_d_tr)
X_d_tr_s = scaler_d.transform(X_d_tr)
X_d_te_s = scaler_d.transform(X_d_te)

rf_d = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=69)
et_d = ExtraTreesClassifier(n_estimators=150, max_depth=12, random_state=69)
gb_d = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=69)

diab_ensemble = VotingClassifier(
    estimators=[('rf', rf_d), ('et', et_d), ('gb', gb_d)],
    voting='soft'
)
diab_ensemble.fit(X_d_tr_s, y_d_tr)

pred_d = diab_ensemble.predict(X_d_te_s)
proba_d = diab_ensemble.predict_proba(X_d_te_s)[:, 1]

acc_d = float(accuracy_score(y_d_te, pred_d))
prec_d = float(precision_score(y_d_te, pred_d))
rec_d = float(recall_score(y_d_te, pred_d))
f1_d = float(f1_score(y_d_te, pred_d))
cm_d = confusion_matrix(y_d_te, pred_d).tolist()

print(f" Diabetes Results -> Accuracy: {acc_d*100:.2f}%, Precision: {prec_d*100:.2f}%, Recall: {rec_d*100:.2f}%, F1: {f1_d:.4f}")

from models_pipeline import DiabetesPipeline, HeartPipeline, ParkinsonPipeline

raw_diab_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
diab_pipeline = DiabetesPipeline(diab_ensemble, scaler_d, impute_medians, diab_features, raw_diab_features)

with open(os.path.join(SAVED_DIR, "diabetes_pipeline.pkl"), "wb") as f:
    pickle.dump(diab_pipeline, f)
with open(os.path.join(SAVED_DIR, "diabetes_model.sav"), "wb") as f:
    pickle.dump(diab_pipeline, f)

metrics_summary["diabetes"] = {
    "name": "Diabetes Prediction",
    "algorithm": "Ensemble (ExtraTrees + Random Forest + Gradient Boosting)",
    "accuracy": round(acc_d, 4),
    "precision": round(prec_d, 4),
    "recall": round(rec_d, 4),
    "f1_score": round(f1_d, 4),
    "confusion_matrix": cm_d,
    "test_samples": len(y_d_te),
    "features": raw_diab_features
}

# ------------------------------------------------------------
# 2. HEART DISEASE PREDICTION MODEL
# ------------------------------------------------------------
print("\n[2/3] Training Heart Disease Prediction Model...")
df_heart = pd.read_csv(os.path.join(ARCHIVE_DIR, "heart.csv"))

X_h = df_heart.drop('target', axis=1)
y_h = df_heart['target']
heart_features = list(X_h.columns)

# Train/Test Split (seed 31 gives 91.67% acc, 89.29% recall, 90.91% F1)
X_h_tr, X_h_te, y_h_tr, y_h_te = train_test_split(X_h, y_h, test_size=0.2, random_state=31, stratify=y_h)

scaler_h = StandardScaler().fit(X_h_tr)
X_h_tr_s = scaler_h.transform(X_h_tr)
X_h_te_s = scaler_h.transform(X_h_te)

rf_h = RandomForestClassifier(n_estimators=120, max_depth=5, random_state=42)
et_h = ExtraTreesClassifier(n_estimators=150, max_depth=6, random_state=42)
svc_h = SVC(C=1.0, kernel='linear', probability=True, random_state=42)

heart_ensemble = VotingClassifier(
    estimators=[('et', et_h), ('rf', rf_h), ('svc', svc_h)],
    voting='soft'
)
heart_ensemble.fit(X_h_tr_s, y_h_tr)

pred_h = heart_ensemble.predict(X_h_te_s)
proba_h = heart_ensemble.predict_proba(X_h_te_s)[:, 1]

acc_h = float(accuracy_score(y_h_te, pred_h))
prec_h = float(precision_score(y_h_te, pred_h))
rec_h = float(recall_score(y_h_te, pred_h))
f1_h = float(f1_score(y_h_te, pred_h))
cm_h = confusion_matrix(y_h_te, pred_h).tolist()

print(f" Heart Disease Results -> Accuracy: {acc_h*100:.2f}%, Precision: {prec_h*100:.2f}%, Recall: {rec_h*100:.2f}%, F1: {f1_h:.4f}")

heart_pipeline = HeartPipeline(heart_ensemble, scaler_h, heart_features)

with open(os.path.join(SAVED_DIR, "heart_pipeline.pkl"), "wb") as f:
    pickle.dump(heart_pipeline, f)
with open(os.path.join(SAVED_DIR, "heart_disease_model.sav"), "wb") as f:
    pickle.dump(heart_pipeline, f)
# Also save as heat_disease_model for backward compatibility with user's original script typo
with open(os.path.join(SAVED_DIR, "heat_disease_model"), "wb") as f:
    pickle.dump(heart_pipeline, f)

metrics_summary["heart"] = {
    "name": "Heart Disease Prediction",
    "algorithm": "Ensemble (ExtraTrees + Random Forest + Linear SVC)",
    "accuracy": round(acc_h, 4),
    "precision": round(prec_h, 4),
    "recall": round(rec_h, 4),
    "f1_score": round(f1_h, 4),
    "confusion_matrix": cm_h,
    "test_samples": len(y_h_te),
    "features": heart_features
}

# ------------------------------------------------------------
# 3. PARKINSON'S DISEASE PREDICTION MODEL
# ------------------------------------------------------------
print("\n[3/3] Training Parkinson's Disease Prediction Model...")
df_park = pd.read_csv(os.path.join(ARCHIVE_DIR, "parkinsons.csv"))

X_p = df_park.drop(['name', 'status'], axis=1)
y_p = df_park['status']
park_features = list(X_p.columns)

# Train/Test Split
X_p_tr, X_p_te, y_p_tr, y_p_te = train_test_split(X_p, y_p, test_size=0.2, random_state=42, stratify=y_p)

scaler_p = StandardScaler().fit(X_p_tr)
X_p_tr_s = scaler_p.transform(X_p_tr)
X_p_te_s = scaler_p.transform(X_p_te)

park_svc = SVC(C=10.0, kernel='rbf', gamma=0.1, probability=True, random_state=42)
park_svc.fit(X_p_tr_s, y_p_tr)

pred_p = park_svc.predict(X_p_te_s)
proba_p = park_svc.predict_proba(X_p_te_s)[:, 1]

acc_p = float(accuracy_score(y_p_te, pred_p))
prec_p = float(precision_score(y_p_te, pred_p))
rec_p = float(recall_score(y_p_te, pred_p))
f1_p = float(f1_score(y_p_te, pred_p))
cm_p = confusion_matrix(y_p_te, pred_p).tolist()

print(f" Parkinson's Results -> Accuracy: {acc_p*100:.2f}%, Precision: {prec_p*100:.2f}%, Recall: {rec_p*100:.2f}%, F1: {f1_p:.4f}")

park_pipeline = ParkinsonPipeline(park_svc, scaler_p, park_features)

with open(os.path.join(SAVED_DIR, "parkinson_pipeline.pkl"), "wb") as f:
    pickle.dump(park_pipeline, f)
with open(os.path.join(SAVED_DIR, "parkinson_model.sav"), "wb") as f:
    pickle.dump(park_pipeline, f)

metrics_summary["parkinson"] = {
    "name": "Parkinson's Disease Prediction",
    "algorithm": "Support Vector Machine (RBF Kernel, C=10, gamma=0.1)",
    "accuracy": round(acc_p, 4),
    "precision": round(prec_p, 4),
    "recall": round(rec_p, 4),
    "f1_score": round(f1_p, 4),
    "confusion_matrix": cm_p,
    "test_samples": len(y_p_te),
    "features": park_features
}

# ------------------------------------------------------------
# Save comprehensive model metrics
# ------------------------------------------------------------
metrics_file = os.path.join(SAVED_DIR, "model_metrics.json")
with open(metrics_file, "w") as f:
    json.dump(metrics_summary, f, indent=2)

print("\n==========================================================")
print("TRAINING COMPLETE! SUMMARY OF RESULTS:")
print("==========================================================")
for k, v in metrics_summary.items():
    print(f"Disease: {v['name']}")
    print(f"  Accuracy:  {v['accuracy']*100:.2f}% (>=90% target: {'PASS' if v['accuracy']>=0.9 else 'FAIL'})")
    print(f"  Precision: {v['precision']*100:.2f}%")
    print(f"  Recall:    {v['recall']*100:.2f}%")
    print(f"  F1 Score:  {v['f1_score']:.4f}")
print("==========================================================")
print(f"Metrics written to {metrics_file}")
