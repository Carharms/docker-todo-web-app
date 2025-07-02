# app/Dockerfile
# -- Build Stage --
FROM python:3.11 as build-stage
WORKDIR /app

COPY requirements.txt .
# This layer caches the pip install, improving subsequent builds
RUN pip install --no-cache-dir -r requirements.txt

# -- Runtime Stage --
FROM python:3.11-alpine

# Set working directory for the runtime stage
WORKDIR /app

# Install curl for health checks (Alpine uses apk, not apt-get)
RUN apk add --no-cache curl


COPY requirements.txt .

# Re-install Python dependencies in the runtime stage.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Container will listen to this port at runtime
EXPOSE 5000

# Define the command to run when the container starts.
CMD ["python", "app.py"]