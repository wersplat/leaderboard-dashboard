# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt && \
    apt-get update && apt-get install -y sqlite3 && \
    sqlite3 leaderboard.db < schema.sql

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]