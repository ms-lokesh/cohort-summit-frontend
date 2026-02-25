#!/bin/bash

# Update Backend CORS Settings on Render
# This script updates the CORS_ALLOWED_ORIGINS environment variable to allow your Cloudflare Workers frontend

echo "🔧 Updating Backend CORS Settings on Render..."
echo "================================================"
echo ""

# Your Render service ID
SERVICE_ID="srv-d6eo13dm5p6s73fqft6g"

# Add your Cloudflare Workers domain to CORS allowed origins
CORS_ORIGINS="https://cohort-summit-frontend.events-408.workers.dev,https://head.cohort-summit-frontend.pages.dev,http://localhost:5173"

echo "Setting CORS_ALLOWED_ORIGINS to:"
echo "$CORS_ORIGINS"
echo ""

# Update the environment variable on Render
render services env-var set \
  --service-id "$SERVICE_ID" \
  --name "CORS_ALLOWED_ORIGINS" \
  --value "$CORS_ORIGINS"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ CORS settings updated successfully!"
  echo ""
  echo "🔄 Triggering new deployment to apply changes..."
  render deploys create "$SERVICE_ID" --confirm --output text
  echo ""
  echo "✅ Deployment triggered. The backend will restart with new CORS settings."
else
  echo ""
  echo "❌ Failed to update CORS settings."
  echo "Please update manually in Render Dashboard:"
  echo "   1. Go to https://dashboard.render.com"
  echo "   2. Open your 'cohort-backend-api' service"
  echo "   3. Go to Environment tab"
  echo "   4. Update CORS_ALLOWED_ORIGINS to:"
  echo "      $CORS_ORIGINS"
  echo "   5. Save changes (this will trigger a redeploy)"
fi
