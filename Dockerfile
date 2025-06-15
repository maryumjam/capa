# Use official Python image with 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install system dependencies (add more if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Streamlit uses port 8501 by default
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
