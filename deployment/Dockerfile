# Use a lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and script
COPY requirements.txt .
COPY polling.py .
COPY .env .
COPY docker-compose.yml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the script
CMD ["python3", "polling.py"]
