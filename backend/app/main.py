from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.routers import router
from app.core.database import db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    db.init()
    await db.create_all()
    yield
    # Cleanup (if needed)

app = FastAPI(title="CRM MVP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "CRM MVP is running"}
