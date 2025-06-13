# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# ✅ Ensure sessions folder exists (important for Telethon)
RUN mkdir -p /app/sessions

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optional: expose port for dummy HTTP server
EXPOSE 8080

# Default command to run the bot
CMD ["python3", "reper_bot.py"]
