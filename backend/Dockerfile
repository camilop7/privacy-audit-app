FROM python:3.9-slim

# Install netcat (openbsd), tor, curl, build tools
RUN apt-get update && apt-get install -y \
    netcat-openbsd tor curl build-essential && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy application files
COPY ./app /app/app
COPY ./worker /app/worker
COPY requirements.txt /app/
COPY entrypoint.sh /app/

# Copy Alembic files
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose backend port
EXPOSE 8000

# Default command
CMD ["sh", "entrypoint.sh"]
