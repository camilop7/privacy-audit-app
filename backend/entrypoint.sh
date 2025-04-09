#!/bin/sh

# Start Tor in the background
tor &

# Give Tor time to start
sleep 5

echo "⏳ Waiting for Postgres to be ready..."

# Wait for Postgres to accept connections
until nc -z db 5432; do
  echo "⏳ Waiting for database at db:5432..."
  sleep 2
done

echo "✅ Database is up!"

# Run initial DB setup (create tables + seed)
python /app/scripts/init_db.py

# Start the backend app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
