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
update_env_var "CORS_ALLOWED_ORIGINS" "https://head.cohort-summit-frontend.pages.dev,http://localhost:5173"
update_env_var "CSRF_TRUSTED_ORIGINS" "https://cohort-backend-api.onrender.com,https://*.onrender.com,https://head.cohort-summit-frontend.pages.dev"

# Supabase Database  
update_env_var "DATABASE_URL" "postgresql://postgres.yfoopcuwdyotlukbkoej:Cohort_db%40123@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

# Supabase Auth Keys
update_env_var "SUPABASE_URL" "https://yfoopcuwdyotlukbkoej.supabase.co"
update_env_var "SUPABASE_ANON_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmb29wY3V3ZHlvdGx1a2Jrb2VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MDA4NDEsImV4cCI6MjA4NTM3Njg0MX0.YK5uw24Grhc2TPYnF98i0eORgZHNHLJMdd5akenvKRs"
update_env_var "SUPABASE_SERVICE_ROLE_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmb29wY3V3ZHlvdGx1a2Jrb2VqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTgwMDg0MSwiZXhwIjoyMDg1Mzc2ODQxfQ.57FMzdhavCWYdp2-yjiWrtt7ZrEHq3Aq6YyChihx1sc"
update_env_var "SUPABASE_JWT_SECRET" "zy/392pVFfUBs/+wzZmA9Y8/B+R9tCjSLHZMaubjIiv6NUzu4yMtQtbmNYCFuz7ZVQZHlpAHZ4DHzJqb/Frjcg=="

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
