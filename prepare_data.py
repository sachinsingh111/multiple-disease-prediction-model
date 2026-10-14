import os
import zipfile
import urllib.request
import pandas as pd
import numpy as np

ARCHIVE_DIR = "archive"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

print("--- Preparing Datasets in archive/ ---")

# 1. Diabetes Dataset
diabetes_path = os.path.join(ARCHIVE_DIR, "diabetes.csv")
print("Fetching Diabetes dataset...")
diab_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
req = urllib.request.Request(diab_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    df_diab = pd.read_csv(resp, names=cols)
    df_diab.to_csv(diabetes_path, index=False)
    print(f"Saved {diabetes_path} (shape: {df_diab.shape})")

# 2. Heart Disease Dataset (from local zip if available, else download)
heart_path = os.path.join(ARCHIVE_DIR, "heart.csv")
print("Preparing Heart Disease dataset...")
zip_path = "C:/Users/Acer/Downloads/heart+disease.zip"
cols_heart = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        with z.open('processed.cleveland.data') as f:
            df_heart = pd.read_csv(f, names=cols_heart, na_values='?')
else:
    cleve_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    req = urllib.request.Request(cleve_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        df_heart = pd.read_csv(resp, names=cols_heart, na_values='?')

df_heart = df_heart.dropna()
# convert target > 0 to 1
df_heart['target'] = (df_heart['target'] > 0).astype(int)
df_heart.to_csv(heart_path, index=False)
print(f"Saved {heart_path} (shape: {df_heart.shape})")

# 3. Parkinson's Dataset
parkinson_path = os.path.join(ARCHIVE_DIR, "parkinsons.csv")
print("Fetching Parkinson's dataset...")
park_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data"
req = urllib.request.Request(park_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    df_park = pd.read_csv(resp)
    df_park.to_csv(parkinson_path, index=False)
    print(f"Saved {parkinson_path} (shape: {df_park.shape})")

print("All datasets successfully prepared!")
