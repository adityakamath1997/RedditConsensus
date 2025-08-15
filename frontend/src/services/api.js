import axios from 'axios';

// Use deployed backend when provided, fallback to local dev
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchConsensus = async (query, maxResults = 10, commentDepth = 10) => {
  try {
    const response = await api.post('/search', {
      query,
      max_results: maxResults,
      comment_depth: commentDepth,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Search failed');
    } else if (error.request) {
      throw new Error('No response from server. Make sure the backend is running.');
    } else {
      throw new Error('Request failed');
    }
  }
};

export default api;

// Server-Sent Events streaming helper
export const streamConsensus = ({ query, maxResults = 10, commentDepth = 10, handlers = {} }) => {
  const { onRewritten, onSearchComplete, onUrlsFiltered, onConsensus, onMetrics, onDone, onError } = handlers;

  const url = `${API_BASE_URL}/search/stream?query=${encodeURIComponent(query)}&max_results=${encodeURIComponent(maxResults)}&comment_depth=${encodeURIComponent(commentDepth)}`;

  const es = new EventSource(url);

  if (onRewritten) es.addEventListener('rewritten', (e) => onRewritten(JSON.parse(e.data)));
  if (onSearchComplete) es.addEventListener('search_complete', (e) => onSearchComplete(JSON.parse(e.data)));
  if (onUrlsFiltered) es.addEventListener('urls_filtered', (e) => onUrlsFiltered(JSON.parse(e.data)));
  if (onConsensus) es.addEventListener('consensus_generated', (e) => onConsensus(JSON.parse(e.data)));
  if (onMetrics) es.addEventListener('metrics_generated', (e) => onMetrics(JSON.parse(e.data)));
  if (onDone) es.addEventListener('done', (e) => onDone(JSON.parse(e.data)));

  es.addEventListener('error', (e) => {
    try {
      const payload = e.data ? JSON.parse(e.data) : { message: 'Stream error' };
      onError && onError(payload);
    } catch {
      onError && onError({ message: 'Stream error' });
    }
    // Do not auto-close; let the caller decide. Some browsers fire 'error' on CORS retries.
  });

  return es;
};
