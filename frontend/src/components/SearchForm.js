import React, { useState } from 'react';

const SearchForm = ({ onSearch, loading }) => {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [commentDepth, setCommentDepth] = useState(10);
  const [searchType, setSearchType] = useState('regular');
  const [showParams, setShowParams] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      const model = searchType === 'regular' ? 'gpt-4.1-mini' : 'gpt-4.1';
      onSearch(query.trim(), maxResults, commentDepth, model);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="query">What do you want to know? 😊 Your question may include a timeframe!</label>
        <input
          id="query"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="'Best tv shows to binge-watch', 'Predictions for the next 10 years. Find posts from 2010 to 2015'"
          disabled={loading}
        />
      </div>
      
      <button
        type="button"
        className="params-toggle"
        onClick={() => setShowParams((v) => !v)}
        disabled={loading}
        aria-expanded={showParams}
        aria-controls="params-panel"
      >
        {showParams ? 'Hide search parameters' : 'Show search parameters'}
      </button>

      {showParams && (
        <div id="params-panel" className="params-panel">
          <div className="form-group">
            <label htmlFor="maxResults">Max results per query (1-20)</label>
            <input
              id="maxResults"
              type="number"
              min="1"
              max="20"
              value={maxResults}
              onChange={(e) => setMaxResults(parseInt(e.target.value))}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="commentDepth">Max top comments per post</label>
            <select
              id="commentDepth"
              value={commentDepth}
              onChange={(e) => setCommentDepth(parseInt(e.target.value))}
              disabled={loading}
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={15}>15</option>
              <option value={20}>20</option>
              <option value={25}>25</option>
            </select>
          </div>

        </div>
      )}

      <div className="form-note">
        <p>
          Increasing <strong>Max results</strong> and <strong>Max top comments</strong> includes more opinions and can improve coverage,
          but may significantly increase processing time.
        </p>
      </div>
      
      <button 
        type="submit" 
        className="submit-btn" 
        disabled={loading || !query.trim()}
      >
        {loading ? 'Searching...' : 'Get Reddit Consensus'}
      </button>
    </form>
  );
};

export default SearchForm;
