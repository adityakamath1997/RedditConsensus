import React, { useState } from 'react';

const SearchForm = ({ onSearch, loading }) => {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [commentDepth, setCommentDepth] = useState(10);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), maxResults, commentDepth);
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
          placeholder="e.g., Best budget mobile phones released this year, Best tv shows of the last decade..."
          disabled={loading}
        />
      </div>
      
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
