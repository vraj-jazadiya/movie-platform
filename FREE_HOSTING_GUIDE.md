# 🆓 FREE Hosting Guide - Movie Platform

## Deploy Your Movie Platform for FREE!

This guide shows you how to host your entire movie platform completely free.

---

## 🎯 Best FREE Hosting Combination

### ✅ Recommended Setup (100% FREE)
- **Backend:** Render.com (Free tier)
- **Frontend:** Vercel (Free forever)
- **Database:** MongoDB Atlas (Already configured - Free 512MB)
- **Total Cost:** $0/month

---

## 📦 What You Need

1. GitHub account (free)
2. Render.com account (free)
3. Vercel account (free)
4. Your code pushed to GitHub

---

## 🚀 Step-by-Step Deployment

### STEP 1: Push Code to GitHub

```bash
cd movie-platform
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/movie-platform.git
git push -u origin main
```

---

### STEP 2: Deploy Backend to Render.com (FREE)

#### A. Prepare Backend Files

1. **Add Gunicorn to requirements.txt:**

Open `movie-platform/backend/requirements.txt` and add:
```
gunicorn==21.2.0
```

2. **Create render.yaml** in `backend/` folder:

```yaml
services:
  - type: web
    name: movie-platform-api
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: MONGODB_URI
        value: mongodb+srv://Cluster0:Cluster0@cluster0.20j3jkn.mongodb.net/?appName=Cluster0
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: OMDB_API_KEY
        value: b5e04f10
      - key: FLASK_ENV
        value: production
```

#### B. Deploy to Render

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with GitHub
4. Click **"New +"** → **"Web Service"**
5. Click **"Connect account"** to link GitHub
6. Select your **movie-platform** repository
7. Configure:
   - **Name:** movie-platform-api
   - **Region:** Oregon (US West)
   - **Branch:** main
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
8. Add Environment Variables:
   - `MONGODB_URI`: `mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`
   - `JWT_SECRET_KEY`: (click "Generate" for random value)
   - `OMDB_API_KEY`: `b5e04f10`
9. Click **"Create Web Service"**

⏳ **Wait 5-10 minutes** for deployment to complete.

✅ Your API will be live at: `https://movie-platform-api.onrender.com`

**Important Notes:**
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- Perfect for testing and personal projects

---

### STEP 3: Deploy Frontend to Vercel (FREE)

#### A. Prepare Frontend

1. **Update API URL** in `frontend/src/services/api.js`:

```javascript
// Replace the baseURL line with:
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://movie-platform-api.onrender.com';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

2. **Create `.env.production`** in `frontend/` folder:

```
VITE_API_URL=https://movie-platform-api.onrender.com
```

#### B. Deploy to Vercel

1. Go to **https://vercel.com**
2. Click **"Start Deploying"**
3. Sign up with GitHub
4. Click **"Add New..."** → **"Project"**
5. Import your **movie-platform** repository
6. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
7. Add Environment Variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://movie-platform-api.onrender.com`
8. Click **"Deploy"**

⏳ **Wait 2-3 minutes** for deployment.

✅ Your website will be live at: `https://your-project-name.vercel.app`

---

## 🎉 You're Live!

Your movie platform is now hosted for FREE!

### Your URLs:
- **Frontend:** `https://your-project-name.vercel.app`
- **Backend API:** `https://movie-platform-api.onrender.com`
- **Database:** MongoDB Atlas (already configured)

---

## 🔧 Alternative FREE Options

### Option 2: Netlify (Frontend)

1. Go to **https://netlify.com**
2. Sign up with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Select your repository
5. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
6. Add environment variable: `VITE_API_URL`
7. Deploy!

### Option 3: Railway (Backend - $5 free credit)

1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variables
6. Deploy!

### Option 4: Cyclic.sh (Backend - FREE)

1. Go to **https://cyclic.sh**
2. Sign up with GitHub
3. Click **"Link Your Own"**
4. Select repository
5. Configure environment variables
6. Deploy!

---

## 📝 Post-Deployment Checklist

### Test Your Deployment

1. ✅ Visit your Vercel URL
2. ✅ Check if homepage loads
3. ✅ Try registering a new user
4. ✅ Login with admin credentials (admin/admin)
5. ✅ Search for a movie
6. ✅ Test all pages (Profile, News, Chat, Contact)
7. ✅ Check admin dashboard

### Common Issues & Fixes

#### Issue 1: API Not Responding
**Solution:** 
- Wait 60 seconds (Render free tier wakes up)
- Check Render logs for errors
- Verify environment variables are set

#### Issue 2: CORS Errors
**Solution:**
- Ensure Flask-CORS is installed
- Check backend allows your Vercel domain
- Update CORS settings in `app.py` if needed

#### Issue 3: Database Connection Failed
**Solution:**
- Verify MongoDB URI is correct
- Check MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
- Test connection string locally first

#### Issue 4: Frontend Can't Reach Backend
**Solution:**
- Verify `VITE_API_URL` environment variable in Vercel
- Check API URL in `api.js` is correct
- Test backend URL directly in browser

---

## 🎨 Custom Domain (Optional - FREE)

### Add Your Own Domain to Vercel

1. Buy a domain (or use free subdomain from Freenom)
2. Go to Vercel project settings
3. Click **"Domains"**
4. Add your domain
5. Update DNS records as instructed
6. Wait for SSL certificate (automatic)

**Free Domain Options:**
- Freenom.com (free .tk, .ml, .ga domains)
- Vercel subdomain (yourapp.vercel.app)
- Netlify subdomain (yourapp.netlify.app)

---

## 📊 Free Tier Limitations

### Render.com (Backend)
- ✅ 750 hours/month (enough for 1 app)
- ✅ Sleeps after 15 min inactivity
- ✅ 512MB RAM
- ✅ Shared CPU
- ⚠️ Cold start: 30-60 seconds

### Vercel (Frontend)
- ✅ Unlimited bandwidth
- ✅ 100GB bandwidth/month
- ✅ Automatic SSL
- ✅ Global CDN
- ✅ Instant deployments

### MongoDB Atlas (Database)
- ✅ 512MB storage
- ✅ Shared cluster
- ✅ Enough for thousands of users
- ✅ Automatic backups

---

## 🚀 Upgrade Options (When You Need More)

### When to Upgrade?

Upgrade when you experience:
- Slow cold starts (backend sleeping)
- Need more database storage
- Want custom domain with email
- Need better performance

### Paid Plans:
- **Render:** $7/month (no sleep, better performance)
- **Vercel:** Free forever for personal projects
- **MongoDB Atlas:** $9/month (dedicated cluster)

---

## 💡 Pro Tips

### 1. Keep Backend Awake
Use a free service like **UptimeRobot** to ping your backend every 5 minutes:
- Go to https://uptimerobot.com
- Add your Render URL
- Set check interval to 5 minutes
- Backend stays awake!

### 2. Optimize Images
- Use WebP format
- Compress images before upload
- Use lazy loading

### 3. Enable Caching
- Cache movie search results
- Use localStorage for user preferences
- Reduce API calls

### 4. Monitor Performance
- Use Vercel Analytics (free)
- Check Render logs regularly
- Monitor MongoDB usage

---

## 🎯 Quick Deploy Commands

### Update Backend
```bash
cd movie-platform/backend
git add .
git commit -m "Update backend"
git push origin main
# Render auto-deploys!
```

### Update Frontend
```bash
cd movie-platform/frontend
git add .
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys!
```

---

## 📞 Support & Resources

### Documentation
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- MongoDB Atlas: https://docs.atlas.mongodb.com

### Community
- Render Discord: https://discord.gg/render
- Vercel Discord: https://discord.gg/vercel

### Troubleshooting
1. Check deployment logs
2. Test locally first
3. Verify environment variables
4. Check CORS settings
5. Monitor database connections

---

## 🎉 Congratulations!

Your movie platform is now live and accessible worldwide - completely FREE!

**Share your website:**
- Frontend: `https://your-app.vercel.app`
- Show it to friends and family
- Add it to your portfolio
- Share on social media

**Next Steps:**
1. Test all features thoroughly
2. Add your own branding
3. Customize the design
4. Add more features
5. Monitor usage and performance

---

## 📋 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] Database connection working
- [ ] All pages loading correctly
- [ ] Authentication working
- [ ] Movie search functional
- [ ] Admin dashboard accessible
- [ ] Mobile responsive
- [ ] SSL certificate active
- [ ] Custom domain added (optional)

---

**🎬 Your Movie Platform is Live! Enjoy! 🚀**
