import React, { useState, useEffect } from 'react';
import { Activity, Heart, Brain, BarChart3, AlertCircle } from 'lucide-react';
import Navbar from './components/Navbar';
import PredictorView from './components/PredictorView';
import MetricsDashboard from './components/MetricsDashboard';

const API_BASE_URL = 'http://127.0.0.1:5000';

export default function App() {
  const [activeTab, setActiveTab] = useState('diabetes');
  const [apiOnline, setApiOnline] = useState(false);
  const [modelsData, setModelsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  // Poll / check API status on mount
  useEffect(() => {
    const fetchApiInfo = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/models-info`);
        if (res.ok) {
          const data = await res.json();
          setModelsData(data);
          setApiOnline(true);
          setErrorMsg(null);
        } else {
          setApiOnline(false);
        }
      } catch (err) {
        console.warn('Flask API not reachable on port 5000:', err);
        setApiOnline(false);
      }
    };

    fetchApiInfo();
    const interval = setInterval(fetchApiInfo, 6000);
    return () => clearInterval(interval);
  }, []);

  const handlePredict = async (diseaseType, payload) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/predict/${diseaseType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || `HTTP error ${res.status}`);
      }

      const result = await res.json();
      setLastResult(result);
    } catch (err) {
      console.error('Prediction request failed:', err);
      setErrorMsg(`Prediction Error: ${err.message}. Make sure Flask backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} apiOnline={apiOnline} />

      {/* Error Alert if any */}
      {errorMsg && (
        <div style={{
          background: 'rgba(244, 63, 94, 0.15)',
          border: '1px solid rgba(244, 63, 94, 0.4)',
          borderRadius: 12,
          padding: '12px 18px',
          marginBottom: 20,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          color: '#fb7185'
        }}>
          <AlertCircle size={20} />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Navigation Tabs Bar */}
      <div className="tabs-bar">
        <button
          className={`tab-btn tab-diabetes ${activeTab === 'diabetes' ? 'active' : ''}`}
          onClick={() => { setActiveTab('diabetes'); setLastResult(null); }}
        >
          <Activity size={18} />
          <span>Diabetes Diagnostic</span>
        </button>

        <button
          className={`tab-btn tab-heart ${activeTab === 'heart' ? 'active' : ''}`}
          onClick={() => { setActiveTab('heart'); setLastResult(null); }}
        >
          <Heart size={18} />
          <span>Heart Disease Screening</span>
        </button>

        <button
          className={`tab-btn tab-parkinson ${activeTab === 'parkinson' ? 'active' : ''}`}
          onClick={() => { setActiveTab('parkinson'); setLastResult(null); }}
        >
          <Brain size={18} />
          <span>Parkinson's Phonatory Acoustic</span>
        </button>

        <button
          className={`tab-btn tab-metrics ${activeTab === 'metrics' ? 'active' : ''}`}
          onClick={() => setActiveTab('metrics')}
        >
          <BarChart3 size={18} />
          <span>AI Benchmarks &gt; 90%</span>
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === 'diabetes' && (
        <PredictorView
          diseaseType="diabetes"
          sampleProfiles={modelsData?.sample_profiles}
          onPredict={handlePredict}
          loading={loading}
          result={lastResult}
        />
      )}

      {activeTab === 'heart' && (
        <PredictorView
          diseaseType="heart"
          sampleProfiles={modelsData?.sample_profiles}
          onPredict={handlePredict}
          loading={loading}
          result={lastResult}
        />
      )}

      {activeTab === 'parkinson' && (
        <PredictorView
          diseaseType="parkinson"
          sampleProfiles={modelsData?.sample_profiles}
          onPredict={handlePredict}
          loading={loading}
          result={lastResult}
        />
      )}

      {activeTab === 'metrics' && (
        <MetricsDashboard metrics={modelsData?.metrics} />
      )}
    </div>
  );
}
