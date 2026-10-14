# -*- coding: utf-8 -*-
"""
Model Pipeline Classes for Multiple Disease Prediction System.
Separated into an importable module so pickle can serialize and deserialize across scripts.
"""

import numpy as np
import pandas as pd

class DiabetesPipeline:
    def __init__(self, model, scaler, medians, feature_names, raw_features):
        self.model = model
        self.scaler = scaler
        self.medians = medians
        self.feature_names = feature_names
        self.raw_features = raw_features
        self.classes_ = getattr(model, 'classes_', np.array([0, 1]))
        self.feature_names_in_ = np.array(raw_features)

    def preprocess(self, X_input):
        if isinstance(X_input, (list, np.ndarray)):
            df = pd.DataFrame(X_input, columns=self.raw_features)
        else:
            df = X_input.copy()
        
        for col, med in self.medians.items():
            if col in df.columns:
                df[col] = df[col].replace(0, med)
                df[col] = df[col].fillna(med)
        
        df['Glucose_BMI'] = (df['Glucose'] * df['BMI']) / 100.0
        df['Age_Glucose'] = (df['Age'] * df['Glucose']) / 100.0
        
        X_ordered = df[self.feature_names]
        return self.scaler.transform(X_ordered)

    def predict(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict(X_s)

    def predict_proba(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict_proba(X_s)


class HeartPipeline:
    def __init__(self, model, scaler, feature_names):
        self.model = model
        self.scaler = scaler
        self.feature_names = feature_names
        self.classes_ = getattr(model, 'classes_', np.array([0, 1]))
        self.feature_names_in_ = np.array(feature_names)

    def preprocess(self, X_input):
        if isinstance(X_input, (list, np.ndarray)):
            df = pd.DataFrame(X_input, columns=self.feature_names)
        else:
            df = X_input.copy()
        return self.scaler.transform(df[self.feature_names])

    def predict(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict(X_s)

    def predict_proba(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict_proba(X_s)


class ParkinsonPipeline:
    def __init__(self, model, scaler, feature_names):
        self.model = model
        self.scaler = scaler
        self.feature_names = feature_names
        self.classes_ = getattr(model, 'classes_', np.array([0, 1]))
        self.feature_names_in_ = np.array(feature_names)

    def preprocess(self, X_input):
        if isinstance(X_input, (list, np.ndarray)):
            df = pd.DataFrame(X_input, columns=self.feature_names)
        else:
            df = X_input.copy()
        return self.scaler.transform(df[self.feature_names])

    def predict(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict(X_s)

    def predict_proba(self, X_input):
        X_s = self.preprocess(X_input)
        return self.model.predict_proba(X_s)
