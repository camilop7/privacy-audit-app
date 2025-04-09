FROM python:3.9-slim

# Install Tor and tools
RUN apt-get update && apt-get install -y \
    tor curl build-essential && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy application files
COPY ./app /app/app
COPY ./worker /app/worker
COPY requirements.txt /app/
COPY entrypoint.sh /app/

# Copy Alembic files
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the backend port
EXPOSE 8000

# Set default command
CMD ["sh", "entrypoint.sh"]
