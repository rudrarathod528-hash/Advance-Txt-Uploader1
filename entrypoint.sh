#!/bin/sh
# Use Railway's PORT variable, or default to 8000 if not set
PORT="${PORT:-8000}"

# Start Gunicorn and your background worker script
gunicorn --bind 0.0.0.0:$PORT app:app & python3 modules/main.py
