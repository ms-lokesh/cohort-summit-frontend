#!/bin/bash
# Quick fix to update DATABASE_URL on Render service

SERVICE_ID="srv-d6eo13dm5p6s73fqft6g"
RENDER_API_KEY="${RENDER_API_KEY:-}"

if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY environment variable not set"
    echo ""
    echo "📋 Manual Fix Instructions:"
    echo "1. Go to: https://dashboard.render.com/web/$SERVICE_ID"
    echo "2. Click 'Environment' in the left sidebar"
    echo "3. Find DATABASE_URL and click 'Edit'"
    echo "4. Update to: postgresql://postgres:Events%23sns%4034565@db.vkgycspcsybpgdsxjnnn.supabase.co:5432/postgres?sslmode=require"
    echo "5. Click 'Save Changes'"
    echo "6. Redeploy the service"
    echo ""
    echo "OR set your API key and run this script:"
    echo "export RENDER_API_KEY='your-api-key-here'"
    echo "./fix_database_url.sh"
    exit 1
fi

echo "🔧 Updating DATABASE_URL on Render..."

# Update DATABASE_URL
curl -X PUT \
    "https://api.render.com/v1/services/$SERVICE_ID/env-vars/DATABASE_URL" \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"value":"postgresql://postgres:Events%23sns%4034565@db.vkgycspcsybpgdsxjnnn.supabase.co:5432/postgres?sslmode=require"}'

echo ""
echo "✅ DATABASE_URL updated!"
echo "Now trigger a new deployment:"
echo "render deploys create $SERVICE_ID --confirm"
