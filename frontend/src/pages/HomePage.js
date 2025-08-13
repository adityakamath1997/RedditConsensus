import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import SearchResults from '../components/SearchResults';
import { searchConsensus } from '../services/api';

const HomePage = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (query, maxResults) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await searchConsensus(query, maxResults);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Reddit Consensus</h1>
        <p>Get the collective wisdom of Reddit on any topic</p>
      </header>

      <SearchForm onSearch={handleSearch} loading={loading} />

      {loading && (
        <div className="loading">
          <p>🔍 Analyzing Reddit posts...</p>
          <p>This make take more than a minute depending on the number of results. </p>
        </div>
      )}

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      <SearchResults results={results} />
    </div>
  );
};

export default HomePage;
