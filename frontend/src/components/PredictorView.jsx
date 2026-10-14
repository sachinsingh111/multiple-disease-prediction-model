import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, Activity, Heart, Brain, RefreshCw, Send, CheckCircle, Info } from 'lucide-react';
import DiagnosticCard from './DiagnosticCard';
import ReportModal from './ReportModal';

export default function PredictorView({ diseaseType, sampleProfiles, onPredict, loading, result }) {
  const [formData, setFormData] = useState({});
  const [isReportOpen, setIsReportOpen] = useState(false);
  const initializedRef = useRef(null);

  // Field definitions with clinical labels, helper units, and descriptions
  const fieldConfigs = {
    diabetes: {
      title: "Diabetes Risk Diagnostic",
      badgeText: "92.0% Accuracy • 96.0% Recall",
      badgeClass: "badge-diabetes",
      icon: Activity,
      desc: "Analyzes metabolic biomarkers and demographic indicators to predict the likelihood of Type 2 Diabetes Mellitus.",
      fields: [
        { name: 'Glucose', label: 'Blood Glucose Concentration', unit: 'mg/dL', type: 'number', step: '1', min: 0, max: 350, hint: 'Normal Fasting: 70-99 mg/dL' },
        { name: 'BMI', label: 'Body Mass Index (BMI)', unit: 'kg/m²', type: 'number', step: '0.1', min: 10, max: 70, hint: 'Healthy weight: 18.5 - 24.9' },
        { name: 'Age', label: 'Patient Age', unit: 'years', type: 'number', step: '1', min: 1, max: 120, hint: 'Adult reference cohort' },
        { name: 'BloodPressure', label: 'Diastolic Blood Pressure', unit: 'mm Hg', type: 'number', step: '1', min: 30, max: 200, hint: 'Normal diastolic: < 80 mm Hg' },
        { name: 'Insulin', label: '2-Hour Serum Insulin', unit: 'µU/mL', type: 'number', step: '1', min: 0, max: 900, hint: 'Normal: 16 - 166 µU/mL' },
        { name: 'Pregnancies', label: 'Number of Pregnancies', unit: 'count', type: 'number', step: '1', min: 0, max: 20, hint: 'Gestational history' },
        { name: 'SkinThickness', label: 'Triceps Skin Fold Thickness', unit: 'mm', type: 'number', step: '0.5', min: 0, max: 100, hint: 'Subcutaneous fat estimation' },
        { name: 'DiabetesPedigreeFunction', label: 'Diabetes Pedigree Score', unit: 'index', type: 'number', step: '0.01', min: 0, max: 3, hint: 'Genetic family risk index' }
      ]
    },
    heart: {
      title: "Heart Disease Cardiovascular Screening",
      badgeText: "90.0% Accuracy • 89.3% Recall",
      badgeClass: "badge-heart",
      icon: Heart,
      desc: "Evaluates coronary risk factors, hemodynamic response, resting ECG, and fluoroscopy markers.",
      fields: [
        { name: 'age', label: 'Patient Age', unit: 'years', type: 'number', step: '1', min: 1, max: 120, hint: 'Cardiovascular demographic' },
        { name: 'sex', label: 'Biological Sex', unit: 'category', type: 'select', options: [{ label: 'Male (1)', val: 1 }, { label: 'Female (0)', val: 0 }], hint: 'Statistical sex baseline' },
        { name: 'cp', label: 'Chest Pain Classification', unit: 'type', type: 'select', options: [
            { label: '0: Typical Angina', val: 0 },
            { label: '1: Atypical Angina', val: 1 },
            { label: '2: Non-Anginal Pain', val: 2 },
            { label: '3: Asymptomatic', val: 3 }
          ], hint: 'Subjective chest symptom' },
        { name: 'trestbps', label: 'Resting Blood Pressure', unit: 'mm Hg', type: 'number', step: '1', min: 80, max: 240, hint: 'Systolic blood pressure' },
        { name: 'chol', label: 'Serum Cholesterol', unit: 'mg/dL', type: 'number', step: '1', min: 100, max: 600, hint: 'Desirable: < 200 mg/dL' },
        { name: 'fbs', label: 'Fasting Blood Sugar > 120 mg/dL', unit: 'binary', type: 'select', options: [{ label: 'No (≤ 120 mg/dL)', val: 0 }, { label: 'Yes (> 120 mg/dL)', val: 1 }], hint: 'Pre-diabetic indicator' },
        { name: 'restecg', label: 'Resting ECG Interpretation', unit: 'result', type: 'select', options: [
            { label: '0: Normal', val: 0 },
            { label: '1: ST-T Wave Abnormality', val: 1 },
            { label: '2: Left Ventricular Hypertrophy', val: 2 }
          ], hint: 'Electrical cardiac baseline' },
        { name: 'thalach', label: 'Maximum Heart Rate Achieved', unit: 'bpm', type: 'number', step: '1', min: 60, max: 230, hint: 'Exercise chronotropic capacity' },
        { name: 'exang', label: 'Exercise-Induced Angina', unit: 'binary', type: 'select', options: [{ label: 'No (0)', val: 0 }, { label: 'Yes (1)', val: 1 }], hint: 'Ischemia under exertion' },
        { name: 'oldpeak', label: 'ST Depression Induced by Exercise', unit: 'mm', type: 'number', step: '0.1', min: 0, max: 8, hint: 'ECG ST slope deflection' },
        { name: 'slope', label: 'Peak Exercise ST Segment Slope', unit: 'type', type: 'select', options: [
            { label: '0: Upsloping', val: 0 },
            { label: '1: Flat', val: 1 },
            { label: '2: Downsloping', val: 2 }
          ], hint: 'Ischemic ST profile' },
        { name: 'ca', label: 'Vessels Colored by Fluoroscopy', unit: 'count', type: 'select', options: [
            { label: '0 Major Vessels', val: 0 },
            { label: '1 Major Vessel', val: 1 },
            { label: '2 Major Vessels', val: 2 },
            { label: '3 Major Vessels', val: 3 }
          ], hint: 'Coronary artery visibility' },
        { name: 'thal', label: 'Thallium Stress Scintigraphy', unit: 'status', type: 'select', options: [
            { label: '0: Normal Baseline', val: 0 },
            { label: '1: Fixed Defect', val: 1 },
            { label: '2: Reversible Defect', val: 2 },
            { label: '3: Other/Indeterminate', val: 3 }
          ], hint: 'Myocardial perfusion defect' }
      ]
    },
    parkinson: {
      title: "Parkinson's Phonatory Acoustic Analysis",
      badgeText: "94.9% Accuracy • 96.6% Recall",
      badgeClass: "badge-parkinson",
      icon: Brain,
      desc: "Quantifies vocal fold vibrations, frequency/amplitude perturbations, and nonlinear dynamical dysarthria markers.",
      fields: [
        { name: 'MDVP:Fo(Hz)', label: 'Average Vocal Fundamental Frequency', unit: 'Hz', type: 'number', step: '0.1', hint: 'Pitch baseline (fo)' },
        { name: 'MDVP:Fhi(Hz)', label: 'Maximum Vocal Fundamental Frequency', unit: 'Hz', type: 'number', step: '0.1', hint: 'Upper pitch limit' },
        { name: 'MDVP:Flo(Hz)', label: 'Minimum Vocal Fundamental Frequency', unit: 'Hz', type: 'number', step: '0.1', hint: 'Lower pitch limit' },
        { name: 'MDVP:Jitter(%)', label: 'Frequency Perturbation (Jitter %)', unit: '%', type: 'number', step: '0.0001', hint: 'Normal threshold: < 0.005' },
        { name: 'MDVP:Jitter(Abs)', label: 'Absolute Jitter Microseconds', unit: 'µs', type: 'number', step: '0.00001', hint: 'Cycle-to-cycle variance' },
        { name: 'MDVP:RAP', label: 'Relative Average Perturbation (RAP)', unit: 'ratio', type: 'number', step: '0.0001', hint: '3-point smoothing' },
        { name: 'MDVP:PPQ', label: 'Pitch Period Perturbation Quotient', unit: 'ratio', type: 'number', step: '0.0001', hint: '5-point smoothing' },
        { name: 'Jitter:DDP', label: 'Average Absolute Difference of Differences', unit: 'ratio', type: 'number', step: '0.0001', hint: 'Degradation metric' },
        { name: 'MDVP:Shimmer', label: 'Amplitude Perturbation (Shimmer)', unit: 'ratio', type: 'number', step: '0.001', hint: 'Normal threshold: < 0.03' },
        { name: 'MDVP:Shimmer(dB)', label: 'Shimmer Decibels', unit: 'dB', type: 'number', step: '0.01', hint: 'Loudness variation' },
        { name: 'Shimmer:APQ3', label: 'Amplitude Perturbation Quotient (3-pt)', unit: 'ratio', type: 'number', step: '0.001', hint: '3-period average' },
        { name: 'Shimmer:APQ5', label: 'Amplitude Perturbation Quotient (5-pt)', unit: 'ratio', type: 'number', step: '0.001', hint: '5-period average' },
        { name: 'MDVP:APQ', label: '11-Point Amplitude Perturbation (APQ)', unit: 'ratio', type: 'number', step: '0.001', hint: 'Sustained phonation stability' },
        { name: 'Shimmer:DDA', label: 'Average Absolute Difference of Shimmer', unit: 'ratio', type: 'number', step: '0.001', hint: 'Amplitude cycle variance' },
        { name: 'NHR', label: 'Noise-to-Harmonics Ratio', unit: 'ratio', type: 'number', step: '0.001', hint: 'Acoustic breathiness / noise' },
        { name: 'HNR', label: 'Harmonics-to-Noise Ratio', unit: 'dB', type: 'number', step: '0.1', hint: 'Normal speech: > 20 dB' },
        { name: 'RPDE', label: 'Recurrence Period Density Entropy', unit: 'score', type: 'number', step: '0.01', hint: 'Nonlinear dynamical complexity' },
        { name: 'DFA', label: 'Detrended Fluctuation Analysis', unit: 'alpha', type: 'number', step: '0.01', hint: 'Signal self-similarity scaling' },
        { name: 'spread1', label: 'Nonlinear Frequency Spread Measure 1', unit: 'score', type: 'number', step: '0.01', hint: 'Fundamental frequency variance' },
        { name: 'spread2', label: 'Nonlinear Frequency Spread Measure 2', unit: 'score', type: 'number', step: '0.01', hint: 'Dynamic trajectory spread' },
        { name: 'D2', label: 'Correlation Dimension', unit: 'dim', type: 'number', step: '0.01', hint: 'Vocal attractor complexity' },
        { name: 'PPE', label: 'Pitch Period Entropy', unit: 'score', type: 'number', step: '0.01', hint: 'Impaired pitch control index' }
      ]
    }
  };

  const config = fieldConfigs[diseaseType] || fieldConfigs.diabetes;
  const DiseaseIcon = config.icon;

  // Initialize form with healthy preset on disease switch (only once per disease type)
  useEffect(() => {
    if (sampleProfiles && sampleProfiles[diseaseType] && initializedRef.current !== diseaseType) {
      setFormData(sampleProfiles[diseaseType].healthy || {});
      initializedRef.current = diseaseType;
    }
  }, [diseaseType, sampleProfiles]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === '' ? '' : parseFloat(value)
    }));
  };

  const handleApplyPreset = (type) => {
    if (sampleProfiles && sampleProfiles[diseaseType] && sampleProfiles[diseaseType][type]) {
      setFormData(sampleProfiles[diseaseType][type]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(diseaseType, formData);
  };

  return (
    <div className="glass-panel">
      {/* Header */}
      <div className="predictor-header">
        <div className="disease-info">
          <div className="disease-title-row">
            <h2 className="disease-title">{config.title}</h2>
            <span className={`badge ${config.badgeClass}`}>{config.badgeText}</span>
          </div>
          <p className="disease-desc">{config.desc}</p>
        </div>

        {/* Presets Toolbar */}
        <div className="presets-bar">
          <span style={{ fontSize: '0.78rem', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>
            Instant Demo:
          </span>
          <button
            type="button"
            className="preset-btn healthy"
            onClick={() => handleApplyPreset('healthy')}
            title="Pre-fill standard healthy laboratory metrics"
          >
            <Sparkles size={14} color="#10b981" />
            <span>Healthy Sample</span>
          </button>
          <button
            type="button"
            className="preset-btn high-risk"
            onClick={() => handleApplyPreset('high_risk')}
            title="Pre-fill confirmed diagnostic risk metrics"
          >
            <Sparkles size={14} color="#f43f5e" />
            <span>High-Risk Sample</span>
          </button>
          <button
            type="button"
            className="preset-btn"
            onClick={() => setFormData({})}
            title="Reset all form inputs"
          >
            <RefreshCw size={13} />
            <span>Clear</span>
          </button>
        </div>
      </div>

      {/* Main Input Form */}
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-grid">
          {config.fields.map((field) => (
            <div key={field.name} className="input-card">
              <div className="input-header">
                <label className="input-label" htmlFor={field.name}>
                  {field.label}
                </label>
                <span className="input-unit">{field.unit}</span>
              </div>

              {field.type === 'select' ? (
                <select
                  id={field.name}
                  name={field.name}
                  value={formData[field.name] !== undefined ? formData[field.name] : ''}
                  onChange={handleInputChange}
                  className="select-field"
                  required
                >
                  {field.options.map((opt) => (
                    <option key={opt.val} value={opt.val}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  id={field.name}
                  type="number"
                  name={field.name}
                  step={field.step || 'any'}
                  min={field.min}
                  max={field.max}
                  value={formData[field.name] !== undefined ? formData[field.name] : ''}
                  onChange={handleInputChange}
                  className="input-field"
                  required
                />
              )}

              {field.hint && <div className="input-hint">{field.hint}</div>}
            </div>
          ))}
        </div>

        {/* Submit Action */}
        <div className="actions-row">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <RefreshCw size={18} className="spin" />
                <span>Computing AI Inference...</span>
              </>
            ) : (
              <>
                <Send size={18} />
                <span>Evaluate Patient Risk</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Diagnostic Evaluation Card */}
      {result && result.disease === diseaseType && (
        <DiagnosticCard result={result} onOpenReport={() => setIsReportOpen(true)} />
      )}

      {/* Printable Report Modal */}
      <ReportModal
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        result={result}
        diseaseName={config.title}
        inputData={formData}
      />
    </div>
  );
}
