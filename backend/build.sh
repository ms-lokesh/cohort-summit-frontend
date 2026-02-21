#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️  Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Running migrations..."
python manage.py migrate

echo "👥 Creating default production users..."
python manage.py create_production_users

echo "✅ Build complete!"
