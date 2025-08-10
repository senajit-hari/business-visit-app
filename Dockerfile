# Use Python 3.11.15 slim base image
FROM python:3.11.15-slim

# Set working directory inside container
WORKDIR /app

# Copy your app files to container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app will run on (Render default is 10000)
EXPOSE 10000

# Start your app using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
