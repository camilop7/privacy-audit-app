#!/bin/sh

# Start Tor in the background
tor &

# Give Tor time to start
sleep 5

# Run the app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
