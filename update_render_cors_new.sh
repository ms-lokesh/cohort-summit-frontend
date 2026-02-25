#!/bin/bash

# Update Render Backend with New Environment Variables
# Based on CohortSummit (9).env configuration

echo "🔧 Updating Render Backend Environment Variables..."
echo "================================================"
echo ""

SERVICE_ID="srv-d6eo13dm5p6s73fqft6g"

# New CORS allowed origins including all Cloudflare Pages deployments
CORS_ORIGINS="https://cohort-summit-frontend-dpe.pages.dev,https://5e21de10.cohort-summit-frontend-dpe.pages.dev,https://e3732ddd.cohort-summit-frontend-dpe.pages.dev,http://localhost:5173,http://localhost:3000,https://73bc5164.cohort-summit-frontend-dpe.pages.dev"

# New allowed hosts
ALLOWED_HOSTS="cohortsummit.onrender.com,cohort-summit-frontend-dpe.pages.dev,5e21de10.cohort-summit-frontend-dpe.pages.dev,localhost,127.0.0.1,73bc5164.cohort-summit-frontend-dpe.pages.dev"

# CSRF trusted origins 
CSRF_ORIGINS="https://cohortsummit.onrender.com,https://*.onrender.com,https://cohort-summit-frontend-dpe.pages.dev"

echo "📋 Environment Variables to Update:"
echo ""
echo "1. CORS_ALLOWED_ORIGINS:"
echo "   $CORS_ORIGINS"
echo ""
echo "2. ALLOWED_HOSTS:"
echo "   $ALLOWED_HOSTS"
echo ""
echo "3. CSRF_TRUSTED_ORIGINS:"
echo "   $CSRF_ORIGINS"
echo ""
echo "================================================"
echo ""
echo "⚠️  The Render CLI doesn't support updating individual env vars."
echo "You need to update these manually in the Render Dashboard:"
echo ""
echo "1. Go to: https://dashboard.render.com"
echo "2. Open service: CohortSummit (srv-d6eo13dm5p6s73fqft6g)"
echo "3. Click: Environment tab"
echo "4. Update these variables:"
echo ""
echo "   CORS_ALLOWED_ORIGINS = $CORS_ORIGINS"
echo ""
echo "   ALLOWED_HOSTS = $ALLOWED_HOSTS"
echo ""
echo "   CSRF_TRUSTED_ORIGINS = $CSRF_ORIGINS"
echo ""
echo "5. Save changes (this will trigger automatic redeploy)"
echo ""
echo "================================================"
echo ""
echo "Or copy these values to paste directly:"
echo ""
echo "CORS_ALLOWED_ORIGINS:"
echo "$CORS_ORIGINS"
echo ""
echo "ALLOWED_HOSTS:"
echo "$ALLOWED_HOSTS"
echo ""
echo "CSRF_TRUSTED_ORIGINS:"
echo "$CSRF_ORIGINS"
echo ""
