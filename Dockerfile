# Use a stable Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt first for better layer caching
COPY requirements.txt .

# Upgrade pip & install dependencies (numpy & pandas will come from requirements.txt)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run your app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
