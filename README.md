# Movie & Entertainment Platform

A comprehensive full-stack web application for discovering, organizing, and managing movies, series, anime, and games.

## Features

### User Features
- 🎬 Browse movies from 37+ production houses
- 🔍 Search and filter movies by various criteria
- ⭐ Create and manage custom playlists
- 💝 Add movies to favorites and watchlist
- 📰 Read latest entertainment news
- 💬 Chat with administrators
- 📧 Contact form for inquiries
- 👤 User profiles with customization

### Admin Features
- 👥 User management
- 📝 News article management
- 💬 Chat management
- 📊 Dashboard with statistics
- ✅ Content approval system

### Technical Features
- 🔐 JWT authentication
- 🎨 Modern dark theme with neon accents
- 📱 Fully responsive design
- 🚀 Fast and optimized
- 🔄 Real-time updates
- 🎯 RESTful API

## Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB
- **Authentication**: JWT (Flask-JWT-Extended)
- **API Integration**: OMDb API
- **CORS**: Flask-CORS

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Custom CSS with CSS Variables

## Project Structure

```
movie-platform/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   ├── app.py           # Main Flask application
│   ├── config.py        # Configuration
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── public/          # Static files
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── styles/      # CSS files
│   │   ├── App.jsx      # Main App component
│   │   └── index.jsx    # Entry point
│   ├── package.json     # Node dependencies
│   └── vite.config.js   # Vite configuration
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (connection string provided)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd movie-platform/backend
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env if needed (MongoDB URI is already configured)
```

5. **Run the backend server**:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

6. **Initialize admin account**:
```bash
curl -X POST http://localhost:5000/api/auth/init-admin
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd movie-platform/frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Default Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin`

### Test User
You can register a new user through the registration page.

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user
- `POST /auth/refresh` - Refresh access token

### Movies Endpoints
- `GET /movies/search?q=query` - Search movies
- `GET /movies/fetch/<imdb_id>` - Fetch movie by IMDb ID
- `GET /movies/trending` - Get trending movies
- `GET /movies/top-rated` - Get top rated movies
- `GET /movies/production-house/<name>` - Get movies by studio

### Profile Endpoints
- `GET /profile/` - Get current user profile
- `PUT /profile/update` - Update profile
- `POST /profile/favorites/<movie_id>` - Add to favorites

### Playlists Endpoints
- `POST /playlists/` - Create playlist
- `GET /playlists/<id>` - Get playlist
- `POST /playlists/<id>/movies` - Add movie to playlist

### News Endpoints
- `GET /news/` - Get all news
- `GET /news/latest` - Get latest news
- `POST /news/` - Create news (admin only)

### Chat Endpoints
- `GET /chat/my-chat` - Get user's chat
- `POST /chat/<id>/message` - Send message

### Contact Endpoints
- `POST /contact/` - Submit contact form
- `GET /contact/all` - Get all contacts (admin only)

## Production Houses Supported

### Major Studios (27)
Marvel Studios, Warner Bros. Pictures, Universal Pictures, Paramount Pictures, 20th Century Studios, Columbia Pictures, Lionsgate Films, Walt Disney Pictures, Sony Pictures Animation, DreamWorks Pictures, New Line Cinema, A24 Films, Blumhouse Productions, Legendary Entertainment, MGM Studios, Dharma Productions, Yash Raj Films, Red Chillies Entertainment, T-Series, Eros International, Sajid Nadiadwala Productions, Phantom Films, Aamir Khan Productions, Studio Ghibli, Toho, Pathé, Wild Bunch

### Anime Studios (10)
Madhouse, Bones, Toei Animation, Kyoto Animation, Wit Studio, MAPPA, Trigger, Sunrise, Studio Pierrot, Silver Link

## Features in Detail

### Movie Discovery
- Search movies by title, year, genre
- Browse by production house
- Filter by IMDb rating, year range
- View trending and top-rated movies
- Automatic movie data fetching from OMDb API

### Playlist Management
- Create unlimited playlists
- Add/remove movies
- Sort by year, rating, or title
- Public/private playlist options
- Share playlists with others

### User Profiles
- Customizable bio and profile info
- Favorites collection
- Watchlist feature
- Watch history tracking
- View other users' public profiles

### News Section
- Latest entertainment news
- Category filtering (movies, series, anime, games)
- Search functionality
- Admin can create/edit/delete articles

### Chat System
- Direct messaging with admins
- Message history
- Unread message indicators
- Real-time updates

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

**Backend**:
```bash
# Set DEBUG=False in config.py
# Deploy to your preferred platform (Heroku, AWS, etc.)
```

**Frontend**:
```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel, Netlify, etc.
```

## Environment Variables

### Backend (.env)
```
MONGO_URI=mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
JWT_SECRET_KEY=your-secret-key
SECRET_KEY=your-flask-secret
DEBUG=True
OMDB_API_KEY=b5e04f10
```

## Troubleshooting

### Backend Issues
- **MongoDB Connection Error**: Check your internet connection and MongoDB URI
- **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Port Already in Use**: Change the port in `app.py`

### Frontend Issues
- **Cannot Connect to API**: Ensure backend is running on port 5000
- **Module Not Found**: Run `npm install` again
- **Build Errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@movieplatform.com or open an issue in the repository.

## Acknowledgments

- OMDb API for movie data
- MongoDB Atlas for database hosting
- All the amazing production houses and studios

---

**Built with ❤️ for movie enthusiasts**
