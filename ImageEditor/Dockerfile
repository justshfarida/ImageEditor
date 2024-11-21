# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies, including Nginx
RUN apt-get update \
    && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy application source code
COPY . /app/

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Ensure static files are served from the correct directory
RUN mkdir -p /app/static /app/media

# Expose the port for Nginx (default 80)
EXPOSE 80

# Command to start the container: run Django migrations, collect static files, start Gunicorn and Nginx
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn myproject.wsgi:application --bind 127.0.0.1:8000 & nginx -g 'daemon off;'"]
