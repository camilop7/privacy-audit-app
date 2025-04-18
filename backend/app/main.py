from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.api.routes import router as api_router
from app.core.config import settings  # assuming you store DB URL here
import time
import sys

app = FastAPI(title="Privacy Audit API")

allow_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://host.docker.internal:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


def wait_for_db(max_retries=10, delay=3):
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("✅ Database is ready!")
                return
        except OperationalError as e:
            print(f"⏳ Attempt {attempt}/{max_retries}: DB not ready yet. Retrying in {delay}s...")
            time.sleep(delay)

    print("❌ Could not connect to DB after several attempts.")
    sys.exit(1)


@app.on_event("startup")
def startup_events():
    print("🚀 App is starting...")
    wait_for_db()

    print("\n📍 Registered Routes:")
    for route in app.routes:
        print(f"➡️  {route.path} -> {route.name}")
