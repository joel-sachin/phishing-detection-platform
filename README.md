# AIML-Based Phishing Detection Platform

This project is a comprehensive platform to monitor, identify, and alert on potential phishing domains targeting specific organizations. It was built as a solution to the AI Grand Challenge problem statement.

## Features

- **Continuous Monitoring:** An automated background worker scans for newly created domains using Certificate Transparency logs.
- **Multi-Factor Analysis:** Alerts are generated based on:
  - Domain Name Similarity (using Levenshtein distance)
  - WHOIS data (such as domain creation date)
  - Web Content Inspection for common phishing keywords.
- **Evidence Gathering:** Automatically takes screenshots of live, high-risk websites.
- **External Verification:** Integrates with the Google Safe Browse (Web Risk) API to check URLs against Google's blocklists.
- **Web Dashboard:** A Flask-based web interface to view and manage alerts in a clean, color-coded table.
- **Production Ready:** The entire application is containerized with Docker, including all dependencies like Google Chrome for screenshotting.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Configure the Application:**
    - Make a copy of the configuration template: `cp config.ini.template config.ini`
    - Open the new `config.ini` file and paste your Google Safe Browse API key into the `google_api_key` field.

3.  **Build and Run with Docker:**
    - Make sure you have Docker Desktop installed and running.
    - Build the Docker image:
      ```bash
      docker build -t phishing-detector .
      ```
    - Run the container:
      ```bash
      docker run --rm -p 8000:5000 -v "$(pwd)/alerts.db:/app/alerts.db" -v "$(pwd)/phishing_detector.log:/app/phishing_detector.log" -v "$(pwd)/screenshots:/app/screenshots" phishing-detector
      ```

4.  **Access the Application:**
    - Open your web browser and navigate to `http://localhost:8000`.