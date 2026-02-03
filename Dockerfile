# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (build tools for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install uv
RUN pip install --upgrade pip && pip install uv

# Install torch CPU-only first using uv (faster and better memory management)
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies using uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
