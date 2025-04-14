# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    fi && \
    # Install PostgreSQL client tools
    apt-get update && apt-get install -y postgresql-client

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]