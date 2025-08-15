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
