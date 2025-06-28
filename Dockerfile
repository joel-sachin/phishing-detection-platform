# --- Stage 1: Build the correct version of chromedriver using modern JSON endpoints ---
FROM alpine:latest AS builder

# Install curl, unzip, and jq (a tool for processing JSON)
RUN apk add --no-cache curl unzip jq

# Find the URL for the latest stable chromedriver for linux64 and download it
RUN CHROME_DRIVER_URL=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url') && \
    curl -sS -o /tmp/chromedriver.zip "${CHROME_DRIVER_URL}" && \
    # Add the -o option to overwrite files without prompting
    unzip -o -d /usr/local/bin/ /tmp/chromedriver.zip && \
    rm /tmp/chromedriver.zip

# --- Stage 2: Main application image ---
FROM python:3.11-slim

# Set the working directory in the container
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install system dependencies needed for Chrome and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libgbm1 \
    libxrandr2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Download and install a stable version of Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install; \
    rm google-chrome-stable_current_amd64.deb

# Copy the chromedriver we built in the first stage into the final image
COPY --from=builder /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Gunicorn will run on
EXPOSE 5000

# The command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "300", "app:app"]