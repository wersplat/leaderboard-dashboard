# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN if ! python -c "import flask" &> /dev/null; then \
        echo "Flask is not installed. Installing Flask..." && \
        pip install Flask; \
    else \
        echo "Flask is already installed."; \
    fi && \
    if [ -f requirements.txt ]; then \
        pip freeze > installed.txt && \
        comm -23 <(sort requirements.txt) <(sort installed.txt) > to_install.txt && \
        if [ -s to_install.txt ]; then \
            pip install -r to_install.txt; \
        else \
            echo "All requirements are already installed."; \
        fi; \
    fi && \
    apt-get update && apt-get install -y sqlite3 && \
    sqlite3 leaderboard.db < schema.sql

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]