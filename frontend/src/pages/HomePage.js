import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import SearchResults from '../components/SearchResults';
import ProgressSteps from '../components/ProgressSteps';
import { searchConsensus, streamConsensus } from '../services/api';

const HomePage = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState({
    rewritten: false,
    searchComplete: false,
    urlsFiltered: false,
    consensus: false,
    metrics: false,
  });
  const [completedSteps, setCompletedSteps] = useState([]);
  const [eventSource, setEventSource] = useState(null);

  const handleSearch = async (query, maxResults, commentDepth) => {
    // Close any previous stream
    if (eventSource) {
      try { eventSource.close(); } catch {}
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setProgress({ rewritten: false, searchComplete: false, urlsFiltered: false, consensus: false, metrics: false });
    setCompletedSteps([]);

    try {
      // Start streaming progress; also request full result after stream completes for fallback
      const es = streamConsensus({
        query,
        maxResults,
        commentDepth,
        handlers: {
          onRewritten: () => {
            setProgress((p) => ({ ...p, rewritten: true }));
            setCompletedSteps((s) => Array.from(new Set([...s, 'Rewrote your query'])));
          },
          onSearchComplete: () => {
            setProgress((p) => ({ ...p, searchComplete: true }));
            setCompletedSteps((s) => Array.from(new Set([...s, 'Searched Reddit'])));
          },
          onUrlsFiltered: () => {
            setProgress((p) => ({ ...p, urlsFiltered: true }));
            setCompletedSteps((s) => Array.from(new Set([...s, 'Filtered relevant URLs'])));
          },
          onConsensus: () => {
            setProgress((p) => ({ ...p, consensus: true }));
            setCompletedSteps((s) => Array.from(new Set([...s, 'Generated consensus'])));
          },
          onMetrics: () => {
            setProgress((p) => ({ ...p, metrics: true }));
            setCompletedSteps((s) => Array.from(new Set([...s, 'Computed metrics'])));
          },
          onDone: (payload) => {
            setResults(payload);
            setLoading(false);
            try { es.close(); } catch {}
          },
          onError: (e) => {
            const message = e && e.code === 429 ? 'Rate limit exceeded. Please try again later.' : (e?.message || 'Stream error');
            setError(message);
            setLoading(false);
            try { es.close(); } catch {}
          },
        }
      });
      setEventSource(es);
    } catch (err) {
      setError(err.message);
    } finally {
      // Keep loading until stream sends done
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Reddit Consensus</h1>
        <p>Find the most popular answers to your questions from Reddit posts and comments!</p>
      </header>

      <SearchForm onSearch={handleSearch} loading={loading} />

      {loading && (
        <ProgressSteps completedSteps={completedSteps} loading={loading} />
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
