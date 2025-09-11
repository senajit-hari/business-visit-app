# Use a stable Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt first for better layer caching
COPY requirements.txt .

# Upgrade pip & install dependencies (no-cache to avoid old binaries)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Run your app with Gunicorn (3 workers for production concurrency)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
