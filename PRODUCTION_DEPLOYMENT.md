# 🚀 Production Deployment Guide

## Production URLs

### Live Application
- **Frontend:** https://movie-platform-v1.netlify.app/
- **Backend API:** https://movie-platform-api.onrender.com
- **API Health Check:** https://movie-platform-api.onrender.com/api/health

### API Keys Configured
- **OMDb API:** b5e04f10
- **NewsAPI:** 854b2e8293b54de1a12a4531162bcf15

---

## 🎯 Quick Setup for Production

### Step 1: Seed Production Database

You can seed the production database using the admin dashboard or API calls:

#### Option A: Using Admin Dashboard (Recommended)
1. Go to https://movie-platform-v1.netlify.app/
2. Login with admin credentials:
   - Username: `admin`
   - Password: `admin`
3. Navigate to Admin Dashboard
4. Click "🎬 Seed All Data (Quick)"
5. Wait for confirmation (~30 seconds)
6. Refresh the home page

#### Option B: Using API Calls
```bash
# First, get admin token
curl -X POST https://movie-platform-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Copy the access_token from response, then:
curl -X POST https://movie-platform-api.onrender.com/api/admin/seed-all \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"type":"quick"}'
```

#### Option C: Using Local Script (Connect to Production DB)
```bash
cd movie-platform/backend
python scripts/seed_database.py quick
```

---

## 📊 What Gets Seeded

### Quick Seed (30 seconds)
- ✅ 20 popular movies from major studios
- ✅ 15 real entertainment news articles (via NewsAPI)
- ✅ Trending movies collection
- ✅ Top-rated movies collection

### Movies Include:
- Avengers: Endgame (Marvel)
- The Dark Knight (Warner Bros)
- Inception (Warner Bros)
- Interstellar (Paramount)
- Spirited Away (Studio Ghibli)
- The Matrix (Warner Bros)
- Pulp Fiction (Miramax)
- Forrest Gump (Paramount)
- And 12 more blockbusters!

### News Categories:
- 🎬 Movies
- 📺 TV Series
- 🎌 Anime
- 🎮 Gaming
- 🎭 Entertainment

---

## 🔧 Production Configuration

### Backend (Render)
```env
MONGO_URI=mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
OMDB_API_KEY=b5e04f10
NEWSAPI_KEY=854b2e8293b54de1a12a4531162bcf15
JWT_SECRET_KEY=your-production-secret
DEBUG=False
```

### Frontend (Netlify)
```env
VITE_API_URL=https://movie-platform-api.onrender.com
```

---

## 🎮 Admin Controls

### Available Actions

1. **Seed All Data**
   - Seeds movies + news in one click
   - Takes ~30 seconds
   - Adds 20 movies + 15 news articles

2. **Seed Movies Only**
   - Adds 20 popular movies
   - Takes ~20 seconds
   - Skips news

3. **Seed News**
   - Fetches latest entertainment news
   - Takes ~5 seconds
   - Uses real NewsAPI data

4. **Refresh News**
   - Removes old articles (7+ days)
   - Fetches fresh news
   - Takes ~5 seconds

5. **View Data Status**
   - Shows total movies
   - Shows total news articles
   - Shows seeded vs manual content

---

## 📈 Monitoring

### Health Checks

```bash
# Check API health
curl https://movie-platform-api.onrender.com/api/health

# Check data status (requires admin token)
curl https://movie-platform-api.onrender.com/api/admin/data-status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Expected Response
```json
{
  "movies": {
    "total_movies": 20,
    "seeded_movies": 20,
    "trending_movies": 10,
    "production_houses_covered": 10
  },
  "news": {
    "total_articles": 15,
    "auto_fetched": 15,
    "manual": 0
  }
}
```

---

## 🔄 Maintenance

### Daily Tasks
```bash
# Refresh news articles
curl -X POST https://movie-platform-api.onrender.com/api/admin/refresh-news \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Weekly Tasks
- Check API usage (OMDb: 1000/day, NewsAPI: 100/day)
- Review data quality
- Monitor error logs

### Monthly Tasks
- Add new movies if needed
- Update production house lists
- Review user feedback

---

## 🚨 Troubleshooting

### Issue: No movies showing
**Solution:**
1. Check if backend is running: https://movie-platform-api.onrender.com/api/health
2. Login as admin and seed data
3. Check browser console for errors

### Issue: News not loading
**Solution:**
1. Click "Seed News" in admin dashboard
2. Check NewsAPI key is valid
3. Verify API quota not exceeded

### Issue: Slow loading
**Solution:**
1. Render free tier may sleep after inactivity
2. First request wakes up the server (~30 seconds)
3. Subsequent requests are fast

### Issue: Admin can't login
**Solution:**
1. Ensure admin account is initialized
2. Use correct credentials (admin/admin)
3. Check JWT token in localStorage

---

## 📊 Performance

### Expected Metrics
- **Page Load:** 2-3 seconds (first load)
- **API Response:** <500ms (after warmup)
- **Seeding Time:** 30 seconds (quick mode)
- **News Refresh:** 5 seconds

### Optimization Tips
1. Use CDN for images
2. Enable caching
3. Implement lazy loading
4. Optimize database queries

---

## 🔒 Security

### Implemented
- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS configuration
- ✅ Admin role checking
- ✅ Input validation
- ✅ Rate limiting (API level)

### Best Practices
- Change default admin password
- Rotate JWT secret regularly
- Monitor API usage
- Keep dependencies updated
- Use HTTPS only

---

## 📱 Features Live

### User Features
- ✅ Browse 20+ movies
- ✅ Search functionality
- ✅ Read entertainment news
- ✅ View by production house
- ✅ Trending section
- ✅ Top-rated section
- ✅ User registration
- ✅ Create playlists
- ✅ Add favorites

### Admin Features
- ✅ One-click data seeding
- ✅ News management
- ✅ User management
- ✅ Data statistics
- ✅ Content moderation

---

## 🎉 Success Checklist

After deployment, verify:
- ✅ Frontend loads at https://movie-platform-v1.netlify.app/
- ✅ Backend responds at https://movie-platform-api.onrender.com/api/health
- ✅ Admin can login
- ✅ Data seeding works
- ✅ Movies display on home page
- ✅ News articles show
- ✅ Search functionality works
- ✅ Production houses listed
- ✅ User registration works
- ✅ All pages accessible

---

## 📞 Support

### Common Commands

```bash
# Get admin token
curl -X POST https://movie-platform-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Seed all data
curl -X POST https://movie-platform-api.onrender.com/api/admin/seed-all \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"quick"}'

# Get data status
curl https://movie-platform-api.onrender.com/api/admin/data-status \
  -H "Authorization: Bearer TOKEN"

# Refresh news
curl -X POST https://movie-platform-api.onrender.com/api/admin/refresh-news \
  -H "Authorization: Bearer TOKEN"
```

---

## 🚀 Next Steps

1. **Seed the database** using admin dashboard
2. **Test all features** on production
3. **Monitor performance** for first few days
4. **Gather user feedback**
5. **Plan enhancements** based on usage

---

## 📈 Future Enhancements

- [ ] Scheduled auto-refresh (cron jobs)
- [ ] More production houses
- [ ] Movie trailers integration
- [ ] Social features
- [ ] Mobile app
- [ ] Advanced search filters
- [ ] User recommendations
- [ ] Email notifications

---

**🎬 Your production movie platform is ready!**

**Live URLs:**
- Frontend: https://movie-platform-v1.netlify.app/
- Backend: https://movie-platform-api.onrender.com

**Admin Credentials:**
- Username: admin
- Password: admin

**Next Action:** Login and click "Seed All Data" to populate your platform! 🚀
