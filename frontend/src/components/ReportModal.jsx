import React from 'react';
import { X, Printer, ShieldCheck, Heart, Activity, Brain } from 'lucide-react';

export default function ReportModal({ isOpen, onClose, result, diseaseName, inputData }) {
  if (!isOpen || !result) return null;

  const handlePrint = () => {
    window.print();
  };

  const isAtRisk = result.prediction === 1 || result.risk_score >= 50;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: 14 }}>
          <div>
            <h2 style={{ fontSize: '1.4rem' }}>Clinical Health Assessment Report</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.82rem' }}>OmniHealth AI Diagnostic System • Date: {new Date().toLocaleDateString()}</p>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
            <X size={22} />
          </button>
        </div>

        <div style={{ marginBottom: 20, background: 'rgba(255,255,255,0.03)', padding: 18, borderRadius: 12, border: '1px solid rgba(255,255,255,0.08)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc' }}>
              Target Screening: {diseaseName.toUpperCase()}
            </span>
            <span style={{
              padding: '4px 12px',
              borderRadius: 20,
              fontSize: '0.8rem',
              fontWeight: 700,
              backgroundColor: isAtRisk ? 'rgba(244, 63, 94, 0.2)' : 'rgba(16, 185, 129, 0.2)',
              color: isAtRisk ? '#fb7185' : '#34d399',
              border: `1px solid ${isAtRisk ? 'rgba(244, 63, 94, 0.4)' : 'rgba(16, 185, 129, 0.4)'}`
            }}>
              {result.status}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Risk Index</span>
              <p style={{ fontSize: '1.4rem', fontWeight: 800, color: isAtRisk ? '#fb7185' : '#34d399' }}>{result.risk_score}%</p>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Severity Rating</span>
              <p style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc' }}>{result.severity || (isAtRisk ? 'High' : 'Low')}</p>
            </div>
          </div>
        </div>

        <div style={{ marginBottom: 20 }}>
          <h4 style={{ fontSize: '0.9rem', color: '#94a3b8', textTransform: 'uppercase', marginBottom: 10, letterSpacing: '0.04em' }}>
            Input Diagnostic Biometrics
          </h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: 8,
            maxHeight: 180,
            overflowY: 'auto',
            background: 'rgba(0,0,0,0.3)',
            padding: 12,
            borderRadius: 8
          }}>
            {Object.entries(inputData).map(([key, val]) => (
              <div key={key} style={{ fontSize: '0.8rem', borderBottom: '1px solid rgba(255,255,255,0.04)', paddingBottom: 4 }}>
                <span style={{ color: '#64748b' }}>{key}: </span>
                <span style={{ color: '#f8fafc', fontWeight: 600 }}>{typeof val === 'number' ? (Number.isInteger(val) ? val : val.toFixed(3)) : val}</span>
              </div>
            ))}
          </div>
        </div>

        {result.risk_factors && result.risk_factors.length > 0 && (
          <div style={{ marginBottom: 20 }}>
            <h4 style={{ fontSize: '0.9rem', color: '#fb7185', textTransform: 'uppercase', marginBottom: 8 }}>
              Identified Pathological Indicators
            </h4>
            <ul style={{ paddingLeft: 18, fontSize: '0.85rem', color: '#cbd5e1' }}>
              {result.risk_factors.map((rf, i) => (
                <li key={i} style={{ marginBottom: 4 }}>{rf}</li>
              ))}
            </ul>
          </div>
        )}

        <div style={{ background: 'rgba(14, 165, 233, 0.1)', borderLeft: '3px solid #0ea5e9', padding: '12px 16px', borderRadius: '0 8px 8px 0', fontSize: '0.88rem', color: '#bae6fd', marginBottom: 24 }}>
          <strong>Physician Notice: </strong> {result.recommendation}
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
          <button className="btn-secondary" onClick={onClose}>Close</button>
          <button className="btn-primary" onClick={handlePrint}>
            <Printer size={16} /> Print Report
          </button>
        </div>
      </div>
    </div>
  );
}
