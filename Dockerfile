# Base image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optional: expose port if needed
# EXPOSE 8080

# Default run command (auto-start script)
CMD ["python3", "reper.py"]
