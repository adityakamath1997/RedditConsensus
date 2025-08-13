# Reddit Consensus

## Get the most common opinions and advice from Reddit discussions. Search any topic, and get a clear summary of what Reddit thinks, backed by actual posts and comments.

## Features

- Rewrites your question into multiple search variations to find relevant discussions
- Searches and analyzes multiple Reddit posts at once
- Filters by date ranges (like "last 3 months", "this year")
- Shows all source posts so you can verify the consensus
- Explains why certain answers were chosen with upvote counts and comment quality
- Instant charts: Answer Frequency and Total Upvotes histograms rendered in the UI (server-side PNGs)

## Tech Stack

**Backend:**
- FastAPI
- OpenAI Agents SDK
- Tavily Search API
- PRAW (Reddit API)
- Matplotlib for charts
- Python 3.12+

**Frontend:**
- React
- Axios
- CSS3 with Flexbox/Grid

## Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- API keys for:
  - OpenAI
  - Tavily
  - Reddit (Client ID & Secret)

### Environment Variables
Create a `.env` file in the project root:
```env
TAVILY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=RedditConsensus/1.0
```

### Installation

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

### Running the Application

1. Start the backend server (from project root):
```bash
python -m uvicorn backend.app.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## What you get after a search

Along with the consensus and raw metrics, the API now returns two base64-encoded PNGs that the frontend displays as charts:

- `answer_frequency_png`: Histogram of how often each answer shows up
- `like_count_png`: Histogram of total upvotes per answer

These are generated server-side using Matplotlib’s Agg backend, so no GUI is required.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── services/     # Business logic
│   │   │   ├── agentlist/        # AI agents (rewriter, consensus, metrics)
│   │   │   ├── plot_service.py   # Server-side Matplotlib chart
│   │   │   ├── reddit_client.py  # Reddit fetching/formatting
│   │   │   ├── search_service.py # Orchestrates the full flow
│   │   │   └── tavily_client.py  # Web search client
│   │   └── schemas/      # Pydantic models
│   ├── main.py           # FastAPI app entry
│   └── tests/            # Backend tests
│       ├── test_search_service.py
│       └── test_endpoint.py
└── frontend/
    ├── public/
    └── src/
        ├── components/   # React components
        ├── pages/        # Page components
        └── services/     # API services
```

## How it works (flow)

```
User enters query
  ↓
Query Rewriter Agent
  ↓
Tavily Search (find relevant Reddit URLs; parallel over rewritten queries)
  ↓
Reddit Client (concurrent fetch of posts + top comments across URLs)
  ↓
┌─────────────────────────────── Parallel ───────────────────────────────┐
│                                                                       │
│  Consensus Agent                          Metrics Agent               │
│    → consensus answer                       → answer_frequency,        │
│      + reasons/caveats                        like_count               │
│                                             → Plot Service (Matplotlib)│
│                                               → base64 PNG charts      │
└───────────────────────────────────────────────────────────────────────┘
  ↓
FastAPI /search response (consensus + metrics + chart images + URLs)
  ↓
React frontend (render consensus, charts, and source links)
```

### Parallelism at a glance

- Tavily: searches multiple rewritten queries in one shot.
- Reddit client: fetches all posts concurrently.
- Agents: consensus and metrics run in parallel.

## Why this is better than “just ask ChatGPT for answers from Reddit posts”
- Posts pulled from the latest reddit submissions that very likely aren't in the LLM's pretraining data.
- All information is received through the Reddit API, no venturing into legal and ethical gray areas with web scraping.
- Real sources you can click: you can look at every Reddit URL used by the LLM to arrive at its answer.
- Breadth and depth: The application searches over several posts and aggregates over a large number of top comments in all those posts.
- The analysis doesn't just factor in the frequency of answers, but also their scores judging by the number of upvotes.
- Quantified output: frequency and total upvotes per answer, charted.
- Time scoped: you can limit your search to discussions pertaining to any timeframe.


## API Endpoints

- `POST /api/v1/search`
  - Accepts: Query string and max results per query
  - Returns: Consensus analysis with source URLs, metrics, and chart images
  - Response fields (high level):
    - `original_query`, `start_date`, `end_date`, `posts_analyzed`, `reddit_urls`
    - `consensus`: `{ consensus: str, additional_info: { reasons: str[], warnings: str[] } }`
    - `metrics`: `{ answer_frequency: Record<string, number>, like_count: Record<string, number>, reasoning?: string }`
    - `answer_frequency_png`: base64 PNG string
    - `like_count_png`: base64 PNG string

## Development

- Run backend from project root (PYTHONPATH must be set to root directory)
- Backend handles multiple Reddit searches in parallel
- Frontend built with modern React patterns
- API responses include source verification
- Chart images are generated server-side and sent as base64 to the frontend

## Tests

Run the backend tests:

```bash
python -m pytest -q backend/tests
```

## License

MIT
