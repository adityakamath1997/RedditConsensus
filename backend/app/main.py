from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.search import router as search_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Reddit Consensus API", version="1.0.0")

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