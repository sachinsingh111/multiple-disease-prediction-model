import React from 'react';

export default function RiskGauge({ score = 0, isPositive = false }) {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const clampedScore = Math.min(Math.max(score, 0), 100);
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  let strokeColor = '#10b981'; // emerald
  let glowColor = 'rgba(16, 185, 129, 0.4)';
  if (clampedScore >= 65 || isPositive) {
    strokeColor = '#f43f5e'; // rose
    glowColor = 'rgba(244, 63, 94, 0.5)';
  } else if (clampedScore >= 35) {
    strokeColor = '#f59e0b'; // amber
    glowColor = 'rgba(245, 158, 11, 0.4)';
  }

  return (
    <div className="gauge-wrapper" style={{ position: 'relative', width: 170, height: 170 }}>
      <svg className="gauge-svg" viewBox="0 0 170 170">
        <circle
          className="gauge-bg"
          cx="85"
          cy="85"
          r={radius}
        />
        <circle
          className="gauge-progress"
          cx="85"
          cy="85"
          r={radius}
          stroke={strokeColor}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          style={{
            filter: `drop-shadow(0 0 8px ${glowColor})`,
          }}
        />
      </svg>
      <div className="gauge-inner-text">
        <span className="gauge-score" style={{ color: strokeColor }}>
          {clampedScore.toFixed(1)}%
        </span>
        <span className="gauge-label">Risk Index</span>
      </div>
    </div>
  );
}
