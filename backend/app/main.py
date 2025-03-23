from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Privacy Audit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")  # THIS IS IMPORTANT ✅
