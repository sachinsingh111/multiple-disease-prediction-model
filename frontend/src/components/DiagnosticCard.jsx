import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, FileText, Printer, ArrowRight } from 'lucide-react';
import RiskGauge from './RiskGauge';

export default function DiagnosticCard({ result, onOpenReport }) {
  if (!result) return null;

  const isAtRisk = result.prediction === 1 || result.risk_score >= 50;
  const severityClass = isAtRisk ? 'at-risk' : 'healthy';

  return (
    <div className="result-section">
      <div className={`result-card ${severityClass}`}>
        <RiskGauge score={result.risk_score} isPositive={isAtRisk} />

        <div className="result-details">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 10 }}>
            <span className={`status-badge ${isAtRisk ? 'high-risk' : 'healthy'}`}>
              {isAtRisk ? <AlertTriangle size={18} /> : <CheckCircle2 size={18} />}
              {result.status}
            </span>

            <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: 600 }}>
              Confidence Probability: {(result.probability * 100).toFixed(1)}%
            </span>
          </div>

          <h3 className="result-status-title" style={{ color: isAtRisk ? '#fb7185' : '#34d399' }}>
            {isAtRisk ? 'Pathological Risk Detected' : 'Normal Physiological Profile'}
          </h3>

          {result.risk_factors && result.risk_factors.length > 0 && (
            <div className="factors-list">
              <div className="factors-title">Identified Key Risk Indicators:</div>
              {result.risk_factors.map((f, idx) => (
                <div key={idx} className="factor-item">
                  <AlertCircle size={15} color="#f43f5e" style={{ flexShrink: 0 }} />
                  <span>{f}</span>
                </div>
              ))}
            </div>
          )}

          <div className="recommendation-box">
            <strong>Clinical Guidance: </strong>
            {result.recommendation}
          </div>

          <div style={{ display: 'flex', gap: 12, marginTop: 4 }}>
            <button className="btn-secondary" onClick={onOpenReport}>
              <Printer size={16} />
              <span>Print / Export Assessment</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
