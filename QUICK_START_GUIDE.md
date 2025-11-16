# 🚀 Quick Start Guide - Movie Platform with Auto Data Fetching

## Overview
This guide will help you set up and run the movie platform with automatic data fetching enabled.

---

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Internet connection (for fetching movie data)
- MongoDB Atlas connection (already configured)

---

## 🎬 Quick Setup (5 Minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd movie-platform/backend

# Install Python dependencies
pip install -r requirements.txt

# Initialize admin account
python -c "from pymongo import MongoClient; from config import Config; from models.user import User; client = MongoClient(Config.MONGO_URI); db = client; user_model = User(db); user_model.create_admin()"
```

### Step 2: Seed Database with Movies & News

**Option A: Quick Seed (Recommended - 20 movies)**
```bash
python scripts/seed_database.py quick
```

**Option B: Essential Seed (10 must-have movies)**
```bash
python scripts/seed_database.py essential
```

**Option C: Full Seed (100+ movies - takes 5-10 minutes)**
```bash
python scripts/seed_database.py full
```

### Step 3: Start Backend Server

```bash
python app.py
```

Backend will run on: `http://localhost:5000`

### Step 4: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd movie-platform/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:5173`

---

## 🎯 Using the Platform

### 1. Access the Website
Open your browser and go to: `http://localhost:5173`

### 2. Login as Admin
- Username: `admin`
- Password: `admin`

### 3. Seed Data from Admin Dashboard
Once logged in:
1. Go to Admin Dashboard
2. Click "🎬 Seed All Data (Quick)" button
3. Wait for confirmation message
4. Refresh the home page to see movies!

---

## 🔄 Automatic Data Fetching Features

### Movies
- ✅ **Auto-populated** from 10 major production houses
- ✅ **Trending movies** with view counts
- ✅ **Top-rated classics** 
- ✅ **Search functionality** via OMDb API
- ✅ **Production house collections**

### News
- ✅ **Auto-generated** entertainment news
- ✅ **Multiple categories** (Movies, TV, Anime, Gaming)
- ✅ **Refresh functionality** to get latest articles
- ✅ **Auto-cleanup** of old articles

### Admin Controls
- 🎬 Seed all data at once
- 🎥 Seed movies only
- 📰 Seed news only
- 🔄 Refresh news articles
- 📊 View data statistics

---

## 📊 What Gets Seeded

### Quick Seed (Default)
- **20 popular movies** including:
  - Avengers: Endgame
  - The Dark Knight
  - Inception
  - Interstellar
  - Spirited Away
  - And 15 more blockbusters!
- **12 news articles** across all categories

### Full Seed
- **100+ movies** from:
  - Marvel Studios (10 movies)
  - Warner Bros (10 movies)
  - Universal Pictures (10 movies)
  - Paramount Pictures (10 movies)
  - 20th Century Studios (10 movies)
  - Columbia Pictures (10 movies)
  - Walt Disney Pictures (10 movies)
  - DreamWorks (10 movies)
  - Studio Ghibli (10 movies)
  - Legendary Entertainment (10 movies)
- **Trending movies** collection
- **Top-rated movies** collection
- **15 news articles**

---

## 🛠️ API Endpoints for Data Management

### Admin Endpoints (Requires Admin Token)

```bash
# Seed all data (quick)
POST http://localhost:5000/api/admin/seed-all
Body: { "type": "quick" }

# Seed movies only
POST http://localhost:5000/api/admin/seed-movies
Body: { "type": "quick" }

# Seed news only
POST http://localhost:5000/api/admin/seed-news

# Refresh news
POST http://localhost:5000/api/admin/refresh-news

# Get data status
GET http://localhost:5000/api/admin/data-status

# Clear seeded movies
DELETE http://localhost:5000/api/admin/clear-movies

# Clear auto-fetched news
DELETE http://localhost:5000/api/admin/clear-news
```

---

## 🔧 Troubleshooting

### Issue: No movies showing up
**Solution:**
1. Check if backend is running (`http://localhost:5000/api/health`)
2. Run seeding script: `python scripts/seed_database.py quick`
3. Check MongoDB connection in `config.py`
4. Refresh the frontend

### Issue: Seeding takes too long
**Solution:**
- Use `quick` seed instead of `full`
- Check internet connection
- Verify OMDb API key is valid

### Issue: News not loading
**Solution:**
1. Click "Seed News" in Admin Dashboard
2. Or run: `python scripts/seed_database.py quick`
3. News uses mock data by default (no API key needed)

### Issue: "Admin access required" error
**Solution:**
1. Make sure you're logged in as admin
2. Username: `admin`, Password: `admin`
3. Check JWT token in browser localStorage

---

## 📝 Environment Variables (Optional)

Create `.env` file in backend directory:

```env
# MongoDB (already configured)
MONGO_URI=mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

# OMDb API (already configured)
OMDB_API_KEY=b5e04f10

# NewsAPI (optional - for real news)
NEWSAPI_KEY=your_newsapi_key_here

# JWT Secret (optional)
JWT_SECRET_KEY=your-secret-key

# Flask
DEBUG=True
SECRET_KEY=your-flask-secret
```

---

## 🎉 Success Checklist

After setup, you should have:
- ✅ Backend running on port 5000
- ✅ Frontend running on port 5173
- ✅ Admin account created
- ✅ Database seeded with movies
- ✅ News articles populated
- ✅ Home page showing trending movies
- ✅ Search functionality working
- ✅ Production houses listed
- ✅ Admin dashboard accessible

---

## 🚀 Next Steps

1. **Explore the Platform**
   - Browse movies by production house
   - Search for your favorite movies
   - Read entertainment news
   - Create playlists

2. **Customize**
   - Add more movies via search
   - Create news articles
   - Manage users
   - Configure production houses

3. **Deploy**
   - Backend: Render, Heroku, or AWS
   - Frontend: Vercel or Netlify
   - Database: MongoDB Atlas (already set up)

---

## 📞 Support

If you encounter issues:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure MongoDB connection is working
4. Check that ports 5000 and 5173 are available

---

## 🎬 Demo Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin`

**Test User (Create via Register):**
- Any username/email
- Any password

---

**Enjoy your fully automated movie platform! 🎉**
