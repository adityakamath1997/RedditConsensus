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

  // 2-minute timeout
  const timeoutId = setTimeout(() => {
    try { es.close(); } catch {}
    onError && onError({ message: 'Request timed out after 2 minutes' });
  }, 120000);

  if (onRewritten) es.addEventListener('rewritten', (e) => onRewritten(JSON.parse(e.data)));
  if (onSearchComplete) es.addEventListener('search_complete', (e) => onSearchComplete(JSON.parse(e.data)));
  if (onUrlsFiltered) es.addEventListener('urls_filtered', (e) => onUrlsFiltered(JSON.parse(e.data)));
  if (onConsensus) es.addEventListener('consensus_generated', (e) => onConsensus(JSON.parse(e.data)));
  if (onMetrics) es.addEventListener('metrics_generated', (e) => onMetrics(JSON.parse(e.data)));
  if (onDone) es.addEventListener('done', (e) => {
    clearTimeout(timeoutId);
    onDone(JSON.parse(e.data));
  });

  es.addEventListener('error', (e) => {
    clearTimeout(timeoutId);
    // Attempt to detect rate limit (429) by probing the endpoint
    const controller = new AbortController();
    const probe = async () => {
      try {
        const resp = await fetch(url, {
          method: 'GET',
          headers: { 'Accept': 'text/event-stream' },
          cache: 'no-store',
          signal: controller.signal,
        });
        if (resp.status === 429) {
          onError && onError({ message: 'Rate limit exceeded. Please try again later.', code: 429 });
        } else {
          onError && onError({ message: 'Stream error' });
        }
      } catch (_) {
        onError && onError({ message: 'Stream error' });
      } finally {
        try { controller.abort(); } catch {}
      }
    };
    // Fire and forget; do not block UI
    probe();
    // Do not auto-close; let the caller decide. Some browsers fire 'error' on CORS retries.
  });

  return es;
};
