# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the worker code
COPY . .

# Command to run the worker service (e.g., Celery worker)
CMD ["celery", "-A", "tasks", "worker"]