# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Command to run the collector
# This will execute collector.py. Ensure parser.py is importable.
CMD ["python", "collector.py"]
