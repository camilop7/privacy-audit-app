import os
import sys
import time
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.exc import OperationalError
from alembic import context

from app.db.session import Base
target_metadata = Base.metadata

# Add your app to Python path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SQLAlchemy Base
from app.db.session import Base

# Explicitly import models so they register with metadata
from app.models.user import User
from app.models.ping_log import PingLog  # 👈 this line is KEY

# Load Alembic config
config = context.config

# Use .env or default DATABASE_URL
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:yourpassword@localhost:5432/privacy_audit")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Pass in your models' metadata
target_metadata = Base.metadata

# ---- Offline migrations ----
def run_migrations_offline() -> None:
    """Run migrations without a live DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---- Online migrations ----
def run_migrations_online() -> None:
    """Run migrations with a live DB connection."""
    connectable = None
    max_retries = 10
    delay = 3  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            connectable = engine_from_config(
                config.get_section(config.config_ini_section),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )
            with connectable.connect() as connection:
                print("✅ Connected to DB.")
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                    compare_type=True
                )
                with context.begin_transaction():
                    context.run_migrations()
                break  # success, exit the loop
        except OperationalError as e:
            print(f"⏳ DB not ready (attempt {attempt}/{max_retries}), retrying in {delay}s...")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

    else:
        print("❌ Could not connect to DB after multiple attempts.")
        raise RuntimeError("Database connection failed for migrations")


# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
