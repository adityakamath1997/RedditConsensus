# Reddit Consensus

## Get the most common opinions and advice from Reddit discussions. Search any topic, and get a clear summary of what Reddit thinks, backed by actual posts and comments.

## Features

- Rewrites your question into multiple search variations to find relevant discussions
- Searches and analyzes multiple Reddit posts at once
- Filters by date ranges (like "last 3 months", "this year")
- Shows all source posts so you can verify the consensus
- Explains why certain answers were chosen with upvote counts and comment quality

## Tech Stack

**Backend:**
- FastAPI
- OpenAI Agents SDK
- Tavily Search API
- PRAW (Reddit API)
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

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── services/     # Business logic
│   │   │   ├── agentlist/    # AI agents
│   │   │   ├── tavily_client.py
│   │   │   └── reddit_client.py
│   │   └── schemas/      # Pydantic models
│   └── tests/            # Backend tests
└── frontend/
    ├── public/
    └── src/
        ├── components/   # React components
        ├── pages/        # Page components
        └── services/     # API services
```

## API Endpoints

- `POST /api/v1/search`
  - Accepts: Query string and max results per query
  - Returns: Consensus analysis with source URLs

## Development

- Run backend from project root (PYTHONPATH must be set to root directory)
- Backend handles multiple Reddit searches in parallel
- Frontend built with modern React patterns
- API responses include source verification

## License

MIT
