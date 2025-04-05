FROM python:3.9-slim

# Install Tor and tools
RUN apt-get update && apt-get install -y \
    tor curl build-essential && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy everything needed
COPY ./app /app/app
COPY requirements.txt /app/
COPY entrypoint.sh /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Default command
CMD ["sh", "entrypoint.sh"]

COPY ./worker /app/worker
