#!/bin/bash
# Pre-start script for Render deployment
# Runs database migrations and creates production users after build but before starting the application

set -e  # Exit on error

echo "========================================"
echo "Running pre-start database operations..."
echo "========================================"

# Wait for database to be ready (with timeout)
echo "Checking database connectivity..."
python -c "
import os
import sys
import time
import psycopg
from urllib.parse import urlparse

max_retries = 5
retry_delay = 3

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    print('ERROR: DATABASE_URL not set')
    sys.exit(1)

for i in range(max_retries):
    try:
        conn = psycopg.connect(database_url, connect_timeout=10)
        conn.close()
        print(f'✓ Database connection successful')
        sys.exit(0)
    except Exception as e:
        if i < max_retries - 1:
            print(f'Database not ready (attempt {i+1}/{max_retries}), retrying in {retry_delay}s...')
            time.sleep(retry_delay)
        else:
            print(f'ERROR: Database connection failed after {max_retries} attempts: {e}')
            sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "Failed to connect to database"
    exit 1
fi

echo ""
echo "Running database migrations..."
python manage.py migrate --no-input

if [ $? -eq 0 ]; then
    echo "✓ Migrations completed successfully"
else
    echo "ERROR: Migrations failed"
    exit 1
fi

echo ""
echo "Creating production users (if not exist)..."
python manage.py create_production_users || true

echo ""
echo "Fixing user sequences..."
python manage.py fix_user_sequence || true

echo ""
echo "Listing database users..."
python manage.py list_users || true

echo ""
echo "========================================"
echo "Pre-start operations completed successfully"
echo "========================================"
