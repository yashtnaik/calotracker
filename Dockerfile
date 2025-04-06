# Use official Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy dependency definitions
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and templates into the container
COPY app.py .
COPY templates ./templates
COPY static /app/static

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
