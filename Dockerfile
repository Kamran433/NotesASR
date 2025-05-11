# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Install system dependencies required for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential libffi-dev libpango-1.0-0 libpangocairo-1.0-0 \
    libcairo2 libgdk-pixbuf2.0-0 libjpeg-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]
