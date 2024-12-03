# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update \
    && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy application source code
COPY . /app/

# Ensure static files are served from the correct directory
RUN mkdir -p /app/static /app/media

# Expose the port for Gunicorn (default 8000)
EXPOSE 8000

# Command to start Gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn ImageEditor.wsgi:application --bind 0.0.0.0:8000"]
