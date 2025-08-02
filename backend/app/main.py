from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import router

app = FastAPI(title="CRM MVP")

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
