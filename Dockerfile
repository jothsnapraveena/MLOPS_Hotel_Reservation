

# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Ensure that credentials are set inside the container
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Install dependencies
RUN pip install --no-cache-dir -e .

# Command to run the application
CMD ["python", "application.py"]
