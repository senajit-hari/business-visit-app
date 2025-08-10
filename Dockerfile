# Use official slim Python 3.11 image
FROM python:3.11-slim

# Install system dependencies needed for building pandas and Excel support
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the port (Render expects $PORT env var)
ENV PORT 10000
ENV FLASK_APP app.py

# Use gunicorn production server to run the app
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app
