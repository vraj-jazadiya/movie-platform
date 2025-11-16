# Movie Platform - Complete Setup Guide

This guide will walk you through setting up and running the Movie & Entertainment Platform.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher** - [Download Node.js](https://nodejs.org/)
- **Git** (optional) - [Download Git](https://git-scm.com/)

## 🚀 Quick Start

### Step 1: Backend Setup

1. **Open a terminal and navigate to the backend directory:**
```bash
cd movie-platform/backend
```

2. **Create a virtual environment (recommended):**

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the backend server:**
```bash
python app.py
```

You should see output like:
```
Connected to MongoDB: movie_platform
 * Running on http://0.0.0.0:5000
```

5. **Initialize the admin account (in a new terminal):**

**On Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/auth/init-admin -Method POST
```

**On macOS/Linux or Windows (Git Bash):**
```bash
curl -X POST http://localhost:5000/api/auth/init-admin
```

You should see a success message indicating the admin account was created.

### Step 2: Frontend Setup

1. **Open a NEW terminal and navigate to the frontend directory:**
```bash
cd movie-platform/frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
```

This may take a few minutes to complete.

3. **Run the frontend development server:**
```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

4. **Open your browser and visit:**
```
http://localhost:3000
```

## 🎉 You're All Set!

The application should now be running with:
- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000

## 🔐 Login Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin`

### Creating a User Account
1. Click on "Register" in the navigation
2. Fill in your details
3. Login with your new credentials

## 📚 Testing the Application

### 1. Test Backend API

Visit http://localhost:5000 in your browser. You should see:
```json
{
  "message": "Welcome to Movie Platform API",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

### 2. Test Movie Search

Try searching for a movie using the OMDb API:
```
http://localhost:5000/api/movies/search?q=inception
```

### 3. Test Frontend

1. Open http://localhost:3000
2. Try registering a new user
3. Login with your credentials
4. Browse movies and create playlists

## 🛠️ Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError"**
```
Solution: Make sure you activated the virtual environment and installed dependencies:
pip install -r requirements.txt
```

**Problem: "MongoDB connection failed"**
```
Solution: Check your internet connection. The MongoDB URI is pre-configured to use MongoDB Atlas.
```

**Problem: "Port 5000 already in use"**
```
Solution: Either stop the process using port 5000, or change the port in app.py:
app.run(debug=Config.DEBUG, host='0.0.0.0', port=5001)
```

### Frontend Issues

**Problem: "Cannot connect to API"**
```
Solution: Make sure the backend is running on port 5000.
Check the console for CORS errors.
```

**Problem: "npm install fails"**
```
Solution: Try clearing npm cache:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem: "Port 3000 already in use"**
```
Solution: The Vite dev server will automatically try the next available port (3001, 3002, etc.)
```

## 📖 API Documentation

### Authentication Endpoints

**Register User:**
```bash
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Login:**
```bash
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

### Movie Endpoints

**Search Movies:**
```bash
GET http://localhost:5000/api/movies/search?q=avengers
```

**Get Trending Movies:**
```bash
GET http://localhost:5000/api/movies/trending?limit=10
```

**Get Movies by Production House:**
```bash
GET http://localhost:5000/api/movies/production-house/Marvel%20Studios
```

### More Endpoints

See the main README.md for complete API documentation.

## 🎨 Features to Try

1. **Search for Movies**: Use the search bar to find movies from OMDb
2. **Create Playlists**: Organize your favorite movies
3. **Browse by Studio**: Explore movies from 37+ production houses
4. **Read News**: Check out the latest entertainment news
5. **Chat with Admin**: Use the chat feature to communicate
6. **Contact Form**: Send feedback or inquiries

## 🔄 Stopping the Application

### Stop Backend:
Press `Ctrl + C` in the terminal running the backend

### Stop Frontend:
Press `Ctrl + C` in the terminal running the frontend

### Deactivate Virtual Environment:
```bash
deactivate
```

## 📦 Production Deployment

### Backend Deployment (Example: Heroku)

1. Create a `Procfile`:
```
web: python app.py
```

2. Deploy to Heroku:
```bash
heroku create movie-platform-api
git push heroku main
```

### Frontend Deployment (Example: Vercel)

1. Build the frontend:
```bash
npm run build
```

2. Deploy to Vercel:
```bash
vercel deploy
```

## 🆘 Getting Help

If you encounter any issues:

1. Check the console/terminal for error messages
2. Review the troubleshooting section above
3. Check the main README.md for more information
4. Ensure all prerequisites are installed correctly

## 🎯 Next Steps

Now that your application is running:

1. Explore the codebase
2. Customize the theme in `frontend/src/styles/theme.css`
3. Add more features
4. Deploy to production
5. Share with friends!

## 📝 Important Notes

- The MongoDB database is hosted on MongoDB Atlas (cloud)
- The OMDb API has a rate limit (1000 requests per day for free tier)
- Admin credentials should be changed in production
- JWT secret keys should be changed in production

---

**Happy Coding! 🚀**
