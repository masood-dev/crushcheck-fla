#!/bin/bash

# Azure App Service startup script for Flask app
# This tells Azure how to start your application using Gunicorn

echo "Starting FLAMES application..."

# Start Gunicorn with configuration
# - bind 0.0.0.0:8000: Listen on all network interfaces, port 8000
# - workers 4: Number of worker processes (adjust based on your needs)
# - timeout 600: Request timeout in seconds
# - wsgi:app: Points to the wsgi.py file and the 'app' object
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 600 wsgi:app
