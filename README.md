# KafkaQuiz

KafkaQuiz is a simple Flask web application that collects user information and quiz answers related to Apache Kafka and Confluent. The application submits answers to a Kafka topic and retrieves results using ksqlDB.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Endpoints](#endpoints)
- [License](#license)

## Installation

### Prerequisites
- Python 3.x
- `pip` (Python package installer)
- `git` (version control system)
- `virtualenv` (Python virtual environment tool)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/dr3jitsu/KafkaQuiz.git
    cd KafkaQuiz
    ```

2. Create and activate a virtual environment:
    ```bash
    virtualenv -p python3 env
    source env/bin/activate
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

## Usage

Open a web browser and navigate to `http://localhost:5000` to access the quiz application. Fill in the form with the required information and quiz answers, then submit to see your results.

## Configuration

The following configuration parameters are used in the application:

- `SUBMISSION_URL`: URL to submit the quiz answers to Kafka.
- `SUBMISSION_URL_KSQLDB`: URL to fetch results from ksqlDB.
- `AUTH_HEADER`: Base64-encoded authorization header for Kafka submission.
- `AUTH_HEADER_KSQLDB`: Base64-encoded authorization header for ksqlDB queries.

## Deployment

### Google Compute Engine

To deploy this application on Google Compute Engine, use the provided `startup-script.sh`:

1. Create a Google Compute Engine instance.
2. Add the `startup-script.sh` as a startup script.
3. The script will:
   - Install necessary software (git, supervisor, python, pip, virtualenv).
   - Clone the repository.
   - Set up a Python virtual environment.
   - Install required Python packages.
   - Run the Flask application.

### Startup Script
```bash
#!/bin/bash

# Install or update needed software
sudo apt-get update
sudo apt-get install -yq git supervisor python3 python3-pip python3-venv gunicorn

# Fetch source code
mkdir -p $HOME/flask-app
cd $HOME/flask-app

git clone https://github.com/dr3jitsu/KafkaQuiz.git .

# Set ownership to newly created account
sudo chown -R $USER $HOME/flask-app

# Python environment setup
python3 -m venv $HOME/flask-app/env
source $HOME/flask-app/env/bin/activate
pip install -r requirements.txt

# Run the application
gunicorn -w 4 -b 0.0.0.0:90 app:app

