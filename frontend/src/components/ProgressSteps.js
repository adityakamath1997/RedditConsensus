import React from 'react';

const STEP_LABELS = [
  'Rewrote your query',
  'Searched Reddit',
  'Filtered relevant URLs',
  'Generated consensus',
  'Computed metrics',
];

const ProgressSteps = ({ completedSteps = [], loading }) => {
  const total = STEP_LABELS.length;
  const completedCount = completedSteps.length;
  const percent = Math.round((completedCount / total) * 100);

  return (
    <div className="progress">
      <div className="progress-header">
        <div className="progress-title">Working on it…</div>
        <div className="progress-sub">This can take a minute depending on results.</div>
      </div>

      <div className="progress-bar">
        <div className="progress-bar-fill" style={{ width: `${percent}%` }} />
      </div>
      <div className="progress-bar-meta">{percent}% complete</div>

      <div className="progress-steps">
        {completedSteps.map((step, idx) => (
          <div className="step-item done" key={`${step}-${idx}`}>
            <span className="step-icon" aria-hidden>✔</span>
            <span className="step-label">{step}</span>
          </div>
        ))}

        {loading && completedCount < total && (
          <div className="step-item current">
            <span className="step-spinner" aria-hidden />
            <span className="step-label">{STEP_LABELS[completedCount]}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressSteps;


