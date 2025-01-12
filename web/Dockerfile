# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the web application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the web service
CMD ["python", "app.py"]