import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # MongoDB Configuration
    # Using the original working MongoDB connection
    MONGO_URI = os.getenv(
        'MONGO_URI',
        'mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    )
    DATABASE_NAME = 'movie_platform'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '05b0769406dfd641c66c2605bbb43e22')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # OMDb API Configuration
    OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'b5e04f10')
    OMDB_API_URL = 'http://www.omdbapi.com/'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-flask-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # CORS Configuration
    CORS_ORIGINS = [
        'http://localhost:3000', 
        'http://localhost:5173',
        'https://movie-platform-v1.netlify.app'
    ]
    
    # Admin Configuration
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin'
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Production Houses
    PRODUCTION_HOUSES = [
        'Marvel Studios', 'Warner Bros. Pictures', 'Universal Pictures',
        'Paramount Pictures', '20th Century Studios', 'Columbia Pictures',
        'Lionsgate Films', 'Walt Disney Pictures', 'Sony Pictures Animation',
        'DreamWorks Pictures', 'New Line Cinema', 'A24 Films',
        'Blumhouse Productions', 'Legendary Entertainment', 'MGM Studios',
        'Dharma Productions', 'Yash Raj Films', 'Red Chillies Entertainment',
        'T-Series', 'Eros International', 'Sajid Nadiadwala Productions',
        'Phantom Films', 'Aamir Khan Productions', 'Studio Ghibli',
        'Toho', 'Pathé', 'Wild Bunch', 'Madhouse', 'Bones',
        'Toei Animation', 'Kyoto Animation', 'Wit Studio', 'MAPPA',
        'Trigger', 'Sunrise', 'Studio Pierrot', 'Silver Link'
    ]
