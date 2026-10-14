import React from 'react';
import { Activity, Heart, Brain, BarChart3, ShieldCheck } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, apiOnline }) {
  return (
    <header className="navbar">
      <div className="brand">
        <div className="brand-icon">
          <Activity size={26} strokeWidth={2.4} />
        </div>
        <div>
          <h1 className="brand-title">OmniHealth AI</h1>
          <p className="brand-subtitle">Multi-Disease Predictive Diagnostic Engine</p>
        </div>
      </div>

      <div className="nav-status">
        <span className="pulse-dot" style={{ backgroundColor: apiOnline ? '#10b981' : '#f43f5e' }}></span>
        <span>{apiOnline ? 'AI Models Live (Port 5000)' : 'Connecting to API...'}</span>
        <ShieldCheck size={16} style={{ marginLeft: 4, color: apiOnline ? '#10b981' : '#f43f5e' }} />
      </div>
    </header>
  );
}
