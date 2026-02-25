# Fix: Cloudflare Pages Changing URLs

## The Problem
Every commit creates a NEW preview URL:
- `https://73bc5164.cohort-summit-frontend-dpe.pages.dev/` ❌ (changes each time)

## The Solution
Use the **production URL** which stays the same:
- `https://cohort-summit-frontend.pages.dev/` ✅ (stable)

## Steps to Fix:

### 1. Configure Cloudflare Pages
Go to: https://dash.cloudflare.com/

1. **Select Project:** `cohort-summit-frontend`

2. **Settings > Builds & deployments**
   - Production branch: `main`
   - Build command: `npm run build`
   - Build output directory: `dist`

3. **Settings > Environment Variables** (MOST IMPORTANT!)
   Add this for **Production** environment:
   ```
   Name:  VITE_API_URL
   Value: https://cohortsummit.onrender.com/api
   ```

### 2. Redeploy
After setting the environment variable:
- Go to **Deployments** tab
- Find latest `main` branch deployment
- Click **"Retry deployment"**

OR just push a new commit to `main`:
```bash
git add .
git commit -m "Trigger production deployment"
git push origin main
```

### 3. Use Production URL
Your stable URL will be:
**https://cohort-summit-frontend.pages.dev/**

## Why This Happens

| Branch/Commit | URL Type | URL |
|---------------|----------|-----|
| `main` branch | **Production** (stable) | `cohort-summit-frontend.pages.dev` ✅ |
| Other commits | Preview (changes) | `xxxxx.cohort-summit-frontend.pages.dev` ❌ |

## Verify It Works
After redeployment, test:
```bash
curl -s https://cohort-summit-frontend.pages.dev | grep -i "vite"
```

The 404 errors you're seeing are because the preview URL doesn't have the `VITE_API_URL` environment variable set, so it's trying to connect to `localhost` instead of your Render backend.
