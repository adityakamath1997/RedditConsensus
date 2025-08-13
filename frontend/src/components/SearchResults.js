import React from 'react';

const SearchResults = ({ results }) => {
  if (!results) return null;

  const { original_query, consensus, reddit_urls_found, posts_analyzed, start_date, end_date, answer_frequency_png, like_count_png } = results;

  return (
    <div className="results">
      <h2>Reddit Consensus for: "{original_query}"</h2>
      
      <div className="consensus">
        <div className="consensus-text">
          {consensus.consensus}
        </div>
      </div>

      {consensus.additional_answers && consensus.additional_answers.length > 0 && (
        <div className="consensus">
          <h4>Alternative Viewpoints:</h4>
          <ul>
            {consensus.additional_answers.map((answer, index) => (
              <li key={index}>{answer}</li>
            ))}
          </ul>
        </div>
      )}
      
      <div className="additional-info">
        <div className="info-section">
          <h4>Why This Consensus?</h4>
          <ul>
            {consensus.additional_info.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </div>
        
        <div className="info-section">
          <h4>Important Caveats</h4>
          <ul>
            {consensus.additional_info.caveats.map((caveat, index) => (
              <li key={index}>{caveat}</li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="meta-info">
        <span>📋 {posts_analyzed} posts analyzed</span>
        {start_date && end_date && (
          <span>📅 {start_date} to {end_date}</span>
        )}
      </div>

      {(answer_frequency_png || like_count_png) && (
        <div className="histograms">
          <h3>Metrics</h3>
          <div className="charts">
            {answer_frequency_png && (
              <div className="chart">
                <h4>Answer Frequency</h4>
                <img
                  src={`data:image/png;base64,${answer_frequency_png}`}
                  alt="Answer Frequency Histogram"
                  style={{ maxWidth: '100%', height: 'auto', border: '1px solid #eee', borderRadius: 6 }}
                />
              </div>
            )}
            {like_count_png && (
              <div className="chart">
                <h4>Total Upvotes</h4>
                <img
                  src={`data:image/png;base64,${like_count_png}`}
                  alt="Total Upvotes Histogram"
                  style={{ maxWidth: '100%', height: 'auto', border: '1px solid #eee', borderRadius: 6 }}
                />
              </div>
            )}
          </div>
        </div>
      )}
      {results.reddit_urls && results.reddit_urls.length > 0 && (
  <div className="reddit-sources">
    <h4>📰 Source Posts Analyzed:</h4>
    <div className="url-list">
      {results.reddit_urls.map((url, index) => (
        <a 
          key={index} 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="reddit-link"
        >
          {url.replace('https://www.reddit.com', '').substring(0, 60)}...
        </a>
      ))}
    </div>
  </div>
)}
    </div>
  );
};

export default SearchResults;
