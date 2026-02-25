#!/bin/bash
# Script to update Render environment variables using the Render API
# You need to get your API key from: https://dashboard.render.com/u/settings#api-keys

set -e

SERVICE_ID="srv-d6eo13dm5p6s73fqft6g"
RENDER_API_KEY="${RENDER_API_KEY:-}"

if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY environment variable not set"
    echo "Please get your API key from: https://dashboard.render.com/u/settings#api-keys"
    echo "Then run: export RENDER_API_KEY='your-api-key-here'"
    exit 1
fi

echo "🔧 Updating Render environment variables..."
echo "Service ID: $SERVICE_ID"
echo ""

# Function to update or create an environment variable
update_env_var() {
    local key=$1
    local value=$2
    
    echo "Setting: $key"
    
    curl -s -X PUT \
        "https://api.render.com/v1/services/$SERVICE_ID/env-vars/$key" \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"value\":\"$value\"}" > /dev/null
}

# Core Django Settings
update_env_var "SECRET_KEY" "cYG3+74E/HMQoiXhgkC4YqTequtJcVs2if+3jEP0XQQ="
update_env_var "DEBUG" "False"
update_env_var "DJANGO_SETTINGS_MODULE" "config.settings"
update_env_var "PYTHON_VERSION" "3.12.2"

# Allowed Hosts & CORS
update_env_var "ALLOWED_HOSTS" "cohort-backend-api.onrender.com,localhost,127.0.0.1,.onrender.com"
update_env_var "CORS_ALLOWED_ORIGINS" "https://cohort-summit-frontend-dpe.pages.dev,http://localhost:5173"
update_env_var "CSRF_TRUSTED_ORIGINS" "https://cohort-backend-api.onrender.com,https://*.onrender.com,https://cohort-summit-frontend-dpe.pages.dev"

# Supabase Database  
update_env_var "DATABASE_URL" "postgresql://postgres.fvsntw:snav64n86d5da6m@vgnzcacvguipindezvin.supabase.co:6543/postgres?sslmode=require&connect_timeout=10"

# Supabase Auth Keys
update_env_var "SUPABASE_URL" "https://fvsnacsacvguindezvin.supabase.co"
update_env_var "SUPABASE_ANON_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2c25hY3NhY3ZndWluZGV6dmluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk4MDY4NzYsImV4cCI6MjA1NTM4Mjg3Nn0.yGmAsrON9dZMgiEBMyGpUZAimv4xCE6MQFkNZUwM23Mtl/k/G0GZRkQZMI2ERu8u6YZRbqvo2G9M5u7qyy0h3ptBUc"
update_env_var "SUPABASE_SERVICE_ROLE_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2c25hY3NhY3ZndWluZGV6dmluIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTgwNjg3NiwiZXhwIjoyMDU1MzgyODc2fQ.NMZ5YKmqh2Z5M8mdCfGlMTc3M1TqyN2zMWcII2XNviIbyMDqsfaTA2MgoaTZJelVr5tgn0t/0aS598NgB6H9ISJ7r2ONDMIN5r6rp3BS_DetNE"
update_env_var "SUPABASE_JWT_SECRET" "5KdMurJ1xUozb0OtqpF+uZ7B1I5LHK0RRMTtU1nMA0AZzyiGfM7u/Qem1lmKroRf9YwBS0NiXjMmH1WirfTaggBVx+wQ=="

# JWT Configuration
update_env_var "JWT_SECRET_KEY" "Qsphh6x7bzzHTcNyuyc8DSXlva8y+0XGCE9m0znRdE4="
update_env_var "JWT_ALGORITHM" "HS256"
update_env_var "JWT_ACCESS_TOKEN_LIFETIME_MINUTES" "60"
update_env_var "JWT_REFRESH_TOKEN_LIFETIME_DAYS" "7"

# Email Configuration
update_env_var "EMAIL_BACKEND" "django.core.mail.backends.smtp.EmailBackend"
update_env_var "EMAIL_HOST" "smtp.gmail.com"
update_env_var "EMAIL_PORT" "587"
update_env_var "EMAIL_USE_TLS" "True"
update_env_var "EMAIL_HOST_USER" "cohortmailservices@gmail.com"
update_env_var "EMAIL_HOST_PASSWORD" "yfpl flst liox ichf"

# Static & Media Files
update_env_var "STATIC_URL" "/static/"
update_env_var "MEDIA_URL" "/media/"

echo ""
echo "✅ All environment variables updated successfully!"
echo ""
echo "⚠️  Important: You need to trigger a new deployment for changes to take effect"
echo "Run: render deploys create $SERVICE_ID --confirm"
