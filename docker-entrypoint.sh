#!/bin/sh
set -e

echo "🔄 Running database migrations..."
flask db upgrade

echo "🌱 Ensuring admin user exists..."
python create_admin.py

echo "🚀 Starting Flask server..."
exec python run.py