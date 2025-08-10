# Use Python 3.11 slim base image (valid tag)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
