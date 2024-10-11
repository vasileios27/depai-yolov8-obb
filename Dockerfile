# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Update package lists and install dependencies
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    software-properties-common \
    wget \
    gcc \
    g++ \
    python3-dev \
    python3-pip \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Create directory for the application
RUN mkdir /object-detection

# Copy application files to the container
COPY . /object-detection/

# Set the working directory
WORKDIR /object-detection

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Set the working directory for the application
WORKDIR /object-detection

# Set the command to run the application
CMD ["python3", "serve.py"]