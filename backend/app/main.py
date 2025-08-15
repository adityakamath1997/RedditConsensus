from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from app.api.search import router as search_router
from app.core.limiter import limiter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Reddit Consensus API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)


@app.get("/")
async def root():
    return {"message": "Reddit Consensus API"}
