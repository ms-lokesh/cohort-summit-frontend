# Fix Cloudflare Pages Deployment

## 🚨 Current Issue
The deployment is failing with:
```
✘ [ERROR] Missing entry-point to Worker script or to assets directory
```

This happens because Cloudflare is running `wrangler deploy` instead of `wrangler pages deploy`.

## ✅ Solution: Update Cloudflare Pages Build Settings

### Step 1: Go to Cloudflare Pages Dashboard
1. Visit https://dash.cloudflare.com
2. Navigate to **Workers & Pages**
3. Click on your **cohort-summit-frontend** project

### Step 2: Update Build Configuration
1. Click **Settings** tab
2. Scroll to **Build & deployments**
3. Click **Edit configuration**
4. Update the following settings:

**Build command:**
```bash
npm run build
```

**Build output directory:**
```
dist
```

**Deploy command:** (Leave empty or remove if present)
```
(empty - don't use wrangler deploy)
```

### Step 3: Set Environment Variables
1. Still in **Settings** > **Environment variables**
2. Click **Add variable**
3. Add the following:

**Variable name:** `VITE_API_URL`  
**Value:** `https://cohortsummit.onrender.com/api`

**For Production environment:**
- Click **Production** tab
- Value: `https://cohortsummit.onrender.com/api`

**For Preview environments:**
- Click **Preview** tab  
- Value: `https://cohortsummit.onrender.com/api`

### Step 4: Retry Deployment
1. Go to **Deployments** tab
2. Find the failed deployment
3. Click **⋮** (three dots) → **Retry deployment**

**Or trigger a new deployment:**
```bash
git commit --allow-empty -m "Trigger Cloudflare rebuild"
git push frontend-repo main
```

## 🔧 Alternative: Use Direct Wrangler Deployment

If you prefer to deploy via CLI instead of GitHub integration:

```bash
# Build locally
npm run build

# Deploy to Cloudflare Pages
npx wrangler pages deploy dist --project-name=cohort-summit-frontend --branch=main

# Or use the npm script
npm run deploy:production
```

## ✅ Expected Result

After fixing, you should see:
```
✨ Success! Uploaded 5 files
Deployed cohort-summit-frontend
https://cohort-summit-frontend.pages.dev
```

## 📝 Environment Variables Summary

Make sure these are set in Cloudflare Pages dashboard:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://cohortsummit.onrender.com/api` |

## 🔗 Useful Links

- Cloudflare Pages Dashboard: https://dash.cloudflare.com
- Cloudflare Pages Docs: https://developers.cloudflare.com/pages/
- Wrangler CLI Docs: https://developers.cloudflare.com/workers/wrangler/
