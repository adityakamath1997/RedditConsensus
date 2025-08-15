import React from 'react';

const HowItWorksPage = ({ onBackToHome }) => {
  return (
    <div className="container">
      <header className="header">
        <h1>How Reddit Consensus Works</h1>
      </header>

      <section className="how-intro">
      </section>

      <section className="how-grid">
        <div className="how-card">
          <h3>Rewrite your query</h3>
          <p>
            Your question is expanded into smart variations and an optional date range to
            capture the different ways Redditors phrase the same idea.
          </p>
        </div>
        <div className="how-card">
          <h3>Find relevant threads</h3>
          <p>
            We search Reddit for each rewritten query to surface the most on‑topic
            discussions.
          </p>
        </div>
        <div className="how-card">
          <h3>Collect posts + top comments</h3>
          <p>
            We pull thread content and top comments to find the most popular answers to your question.
          </p>
        </div>
        <div className="how-card">
          <h3>Build a consensus</h3>
          <p>
            A synthesis step produces a clear, readable answer, and surfaces
            alternative viewpoints when they matter. The number of mentions as well as the associated score/upvotes
            are considered when doing this!
          </p>
        </div>
        <div className="how-card">
          <h3>Measure the crowd</h3>
          <p>
            We compute answer frequencies and upvote totals, then render simple charts so
            you can see how strong the community leans.
          </p>
        </div>
        <div className="how-card">
          <h3>Return sources + metrics</h3>
          <p>
            You get a concise answer, direct links to the threads, and two histograms:
            answer frequency and total upvotes.
          </p>
        </div>
      </section>

      <section className="how-why">
        <h2>Why this (probably) beats “just ask ChatGPT to get answers from Reddit, bro!”</h2>
        <ul>
          <li><strong>Real Reddit access</strong>: ChatGPT usually doesn't have live Reddit API access, and is restricted to its knowledge cutoff date. This uses the official Reddit API, so you’re not getting guesses.</li>
          <li><strong>No web scraping</strong>: Everything comes through approved endpoints.</li>
          <li><strong>You set the scope</strong>: You choose how many threads to scan and how deep to go into the top comments. The analysis takes a few seconds, but it's well worth the wait!</li>
          <li><strong>Increased relevance</strong>: Off-topic threads are filtered out before the analysis so the summary stays focused.</li>
          <li><strong>You can see the numbers</strong>: Metrics to look at how the most popular answers compare to each other.</li>
        </ul>


      </section>

      <section className="how-flow">
        <h2 className="how-flow-title">Flowchart</h2>
        <div className="flowchart">
          <svg viewBox="0 0 560 700" role="img" aria-label="How Reddit Consensus flowchart" preserveAspectRatio="xMidYMid meet">
            <defs>
              <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto" markerUnits="strokeWidth">
                <path d="M0,0 L0,8 L8,4 z" fill="var(--accent)" />
              </marker>
            </defs>

            <rect x="40" y="20" rx="10" ry="10" width="480" height="70" className="flow-node" />
            <text x="280" y="60" textAnchor="middle" className="flow-label">User question</text>

            <line x1="280" y1="90" x2="280" y2="120" className="flow-arrow" markerEnd="url(#arrow)" />

            <rect x="40" y="120" rx="10" ry="10" width="480" height="70" className="flow-node" />
            <text x="280" y="160" textAnchor="middle" className="flow-label">Rewrite queries (+ optional date range)</text>

            <line x1="280" y1="190" x2="280" y2="220" className="flow-arrow" markerEnd="url(#arrow)" />

            <rect x="40" y="220" rx="10" ry="10" width="480" height="70" className="flow-node" />
            <text x="280" y="260" textAnchor="middle" className="flow-label">Search Reddit for relevant threads</text>

            <line x1="280" y1="290" x2="280" y2="320" className="flow-arrow" markerEnd="url(#arrow)" />

            <rect x="40" y="320" rx="10" ry="10" width="480" height="70" className="flow-node" />
            <text x="280" y="360" textAnchor="middle" className="flow-label">Fetch posts + top comments</text>

            {/* Split to consensus and metrics in parallel */}
            <line x1="280" y1="390" x2="280" y2="400" className="flow-arrow" />

            {/* Side nodes first so they don't cover arrows */}
            {/* Left: consensus */}
            <rect x="30" y="420" rx="10" ry="10" width="240" height="80" className="flow-node" />
            <text x="150" y="450" textAnchor="middle" className="flow-label">
              <tspan x="150" dy="0">Synthesize consensus</tspan>
              <tspan x="150" dy="18">+ alternatives</tspan>
            </text>

            {/* Right: metrics */}
            <rect x="290" y="420" rx="10" ry="10" width="240" height="80" className="flow-node" />
            <text x="410" y="450" textAnchor="middle" className="flow-label">
              <tspan x="410" dy="0">Compute metrics</tspan>
              <tspan x="410" dy="18">(frequency, upvotes)</tspan>
            </text>

            {/* Now draw split arrows to sit on top */}
            <line x1="280" y1="400" x2="150" y2="420" className="flow-arrow" markerEnd="url(#arrow)" />
            <line x1="280" y1="400" x2="410" y2="420" className="flow-arrow" markerEnd="url(#arrow)" />

            {/* Bottom node first, then merging arrows on top */}
            <rect x="40" y="600" rx="10" ry="10" width="480" height="70" className="flow-node" />

            {/* Merge down to final answer */}
            <line x1="150" y1="500" x2="280" y2="600" className="flow-arrow" markerEnd="url(#arrow)" />
            <line x1="410" y1="500" x2="280" y2="600" className="flow-arrow" markerEnd="url(#arrow)" />

            <text x="280" y="640" textAnchor="middle" className="flow-label">Return answer + sources + charts</text>
          </svg>
        </div>
        <div style={{ marginTop: 24 }}>
          <button type="button" className="submit-btn" onClick={onBackToHome}>
            Try it now
          </button>
        </div>
      </section>


    </div>
  );
};

export default HowItWorksPage;


