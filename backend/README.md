# Movie Platform Backend API

Flask-based REST API for the Movie & Entertainment Platform.

## Features

- User authentication with JWT
- Movie data fetching from OMDb API
- User profiles and playlists
- News management
- Chat system (user-admin)
- Contact form
- Admin dashboard

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: MongoDB
- **Authentication**: JWT (Flask-JWT-Extended)
- **API Integration**: OMDb API

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run the application**:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/init-admin` - Initialize admin account

### Movies
- `GET /api/movies/search?q=query` - Search movies
- `GET /api/movies/fetch/<imdb_id>` - Fetch movie by IMDb ID
- `GET /api/movies/<movie_id>` - Get movie details
- `GET /api/movies/production-house/<name>` - Get movies by production house
- `GET /api/movies/trending` - Get trending movies
- `GET /api/movies/top-rated` - Get top rated movies
- `POST /api/movies/filter` - Filter movies
- `POST /api/movies/<movie_id>/rate` - Rate a movie
- `POST /api/movies/<movie_id>/review` - Review a movie

### Profile
- `GET /api/profile/` - Get current user profile
- `GET /api/profile/<username>` - Get user profile by username
- `PUT /api/profile/update` - Update profile
- `GET /api/profile/favorites` - Get favorites
- `POST /api/profile/favorites/<movie_id>` - Add to favorites
- `DELETE /api/profile/favorites/<movie_id>` - Remove from favorites
- `GET /api/profile/watchlist` - Get watchlist
- `POST /api/profile/watchlist/<movie_id>` - Add to watchlist

### Playlists
- `POST /api/playlists/` - Create playlist
- `GET /api/playlists/<playlist_id>` - Get playlist
- `PUT /api/playlists/<playlist_id>` - Update playlist
- `DELETE /api/playlists/<playlist_id>` - Delete playlist
- `POST /api/playlists/<playlist_id>/movies` - Add movie to playlist
- `DELETE /api/playlists/<playlist_id>/movies/<movie_id>` - Remove movie
- `POST /api/playlists/<playlist_id>/like` - Like playlist
- `POST /api/playlists/<playlist_id>/sort` - Sort playlist

### News
- `GET /api/news/` - Get all news
- `GET /api/news/<news_id>` - Get news by ID
- `GET /api/news/category/<category>` - Get news by category
- `GET /api/news/latest` - Get latest news
- `POST /api/news/` - Create news (admin)
- `PUT /api/news/<news_id>` - Update news (admin)
- `DELETE /api/news/<news_id>` - Delete news (admin)

### Chat
- `GET /api/chat/my-chat` - Get user's chat
- `GET /api/chat/<chat_id>` - Get chat by ID
- `GET /api/chat/all` - Get all chats (admin)
- `POST /api/chat/<chat_id>/message` - Send message
- `POST /api/chat/<chat_id>/read` - Mark as read (admin)
- `POST /api/chat/<chat_id>/close` - Close chat (admin)

### Contact
- `POST /api/contact/` - Submit contact form
- `GET /api/contact/all` - Get all contacts (admin)
- `GET /api/contact/pending` - Get pending contacts (admin)
- `PUT /api/contact/<contact_id>/status` - Update status (admin)
- `POST /api/contact/<contact_id>/reply` - Mark as replied (admin)

## Admin Credentials

- **Username**: admin
- **Password**: admin

Initialize admin account by calling:
```bash
POST /api/auth/init-admin
```

## Production Houses

The platform supports 37 production houses including:
- Marvel Studios, Warner Bros., Universal Pictures
- Disney, Paramount, Columbia Pictures
- Anime studios: Studio Ghibli, MAPPA, Kyoto Animation
- And many more...

## Environment Variables

- `MONGO_URI` - MongoDB connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `SECRET_KEY` - Flask secret key
- `DEBUG` - Debug mode (True/False)
- `OMDB_API_KEY` - OMDb API key

## Development

Run in development mode:
```bash
python app.py
```

The API will reload automatically on code changes when DEBUG=True.
