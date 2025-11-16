# 🚀 Deploy Login Fixes to Production

## Changes Made (Local)

We've fixed 3 critical issues in the local codebase:

1. ✅ **Token Response Format** - `backend/routes/auth.py`
2. ✅ **CORS Configuration** - `backend/config.py`  
3. ✅ **NewsAPI Key** - `backend/services/news_service.py`

## Current Status

- ✅ **Local Backend:** Fixed and running
- ⚠️ **Production Backend (Render):** Still has old code
- ✅ **Frontend (Netlify):** Already configured correctly

## Why Login Works Locally But Not in Production

The production backend on Render.com is still running the OLD code with the nested token format. We need to deploy our fixes.

---

## Option 1: Deploy via Git (Recommended)

If your Render backend is connected to a Git repository:

### Step 1: Initialize Git (if not done)
```bash
cd movie-platform
git init
git add .
git commit -m "Fix login token response and CORS configuration"
```

### Step 2: Push to Repository
```bash
# If you have a GitHub repo
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

### Step 3: Render Auto-Deploys
- Render will automatically detect the changes
- Wait 2-3 minutes for deployment
- Check logs in Render dashboard

---

## Option 2: Manual File Upload to Render

If you don't have Git setup:

### Files to Update on Render:

1. **backend/routes/auth.py** (Line 72-76)
```python
return jsonify({
    'user': user,
    'access_token': tokens['access_token'],
    'refresh_token': tokens['refresh_token']
}), 200
```

2. **backend/config.py** (Line 27-31)
```python
CORS_ORIGINS = [
    'http://localhost:3000', 
    'http://localhost:5173',
    'https://movie-platform-v1.netlify.app'
]
```

3. **backend/services/news_service.py** (Line 13-17)
```python
self.newsapi_key = '854b2e8293b54de1a12a4531162bcf15'
self.use_mock = False
```

### Steps:
1. Go to Render dashboard
2. Select your backend service
3. Go to "Shell" tab
4. Edit files using nano or vim
5. Restart the service

---

## Option 3: Redeploy from Render Dashboard

### Steps:
1. Go to https://dashboard.render.com
2. Select your backend service
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait for deployment to complete

---

## Option 4: Use Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy
render deploy
```

---

## Verification After Deployment

### Test 1: Check Health
```bash
curl https://movie-platform-api.onrender.com/api/health
```

### Test 2: Test Login
```bash
curl -X POST https://movie-platform-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

**Expected Response:**
```json
{
  "user": {...},
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### Test 3: Run Test Script
```bash
python movie-platform/test_production_login.py
```

**Expected Output:**
```
✅ LOGIN SUCCESSFUL!
✅ Access Token: eyJ...
✅ Refresh Token: eyJ...
✅ Admin access confirmed!
```

---

## Alternative: Test with Local Backend

If you can't deploy to production immediately, you can test everything locally:

### Step 1: Keep Local Backend Running
```bash
cd movie-platform/backend
python app.py
# Runs on http://localhost:5000
```

### Step 2: Update Frontend to Use Local API
Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

### Step 3: Run Frontend
```bash
cd movie-platform/frontend
npm run dev
# Opens on http://localhost:5173
```

### Step 4: Test Login
1. Go to http://localhost:5173
2. Login with admin/admin
3. Should work perfectly!

---

## Production Deployment Checklist

Before deploying to production:

- [ ] All changes committed to Git
- [ ] Tests passing locally
- [ ] Environment variables set on Render:
  - [ ] MONGO_URI
  - [ ] OMDB_API_KEY
  - [ ] NEWSAPI_KEY (optional)
  - [ ] JWT_SECRET_KEY
- [ ] CORS includes Netlify URL
- [ ] Admin account initialized
- [ ] Database accessible

After deployment:

- [ ] Health check passes
- [ ] Login returns tokens
- [ ] Admin can access protected endpoints
- [ ] Frontend can communicate with backend
- [ ] Data seeding works

---

## Troubleshooting

### Issue: Render shows "Build Failed"
**Solution:** Check build logs, ensure requirements.txt is correct

### Issue: "Module not found" errors
**Solution:** Verify all dependencies in requirements.txt

### Issue: Database connection fails
**Solution:** Check MONGO_URI environment variable

### Issue: CORS errors persist
**Solution:** Verify CORS_ORIGINS includes your Netlify URL

### Issue: Tokens still not returned
**Solution:** Ensure auth.py changes are deployed, check logs

---

## Quick Deploy Commands

```bash
# If using Git
cd movie-platform
git add .
git commit -m "Fix login and CORS"
git push origin main

# Wait 2-3 minutes, then test
python test_production_login.py
```

---

## Need Help?

1. Check Render logs for errors
2. Verify environment variables
3. Test endpoints individually
4. Check CORS headers in browser network tab
5. Ensure admin account exists

---

## Status

- ✅ **Local:** All fixes applied and tested
- ⏳ **Production:** Waiting for deployment
- ✅ **Frontend:** Already configured

**Next Step:** Deploy backend changes to Render!
