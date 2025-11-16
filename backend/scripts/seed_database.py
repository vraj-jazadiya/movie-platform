"""
Database Seeding Script
Run this script to populate the database with initial data
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from config import Config
from services.movie_seeder import MovieSeeder
from services.news_service import NewsService

def seed_database(seed_type='quick'):
    """
    Seed the database with movies and news
    
    Args:
        seed_type: 'quick' (20 movies), 'full' (100+ movies), or 'essential' (10 movies)
    """
    print("=" * 60)
    print("🎬 MOVIE PLATFORM - DATABASE SEEDING")
    print("=" * 60)
    print(f"\nSeed Type: {seed_type.upper()}")
    print(f"Database: {Config.DATABASE_NAME}")
    print("\n" + "=" * 60 + "\n")
    
    try:
        # Connect to MongoDB
        print("📡 Connecting to MongoDB...")
        client = MongoClient(Config.MONGO_URI)
        db = client
        print("✅ Connected successfully!\n")
        
        # Initialize services
        movie_seeder = MovieSeeder(db)
        news_service = NewsService(db)
        
        # Seed based on type
        if seed_type == 'full':
            print("🎬 FULL SEEDING - This will take several minutes...")
            print("   - Seeding 100+ movies from 10 production houses")
            print("   - Seeding trending movies")
            print("   - Seeding top-rated movies")
            print("   - Seeding news articles\n")
            
            # Seed all movies
            movie_seeder.seed_all_movies()
            
            # Seed trending
            movie_seeder.seed_trending_movies()
            
            # Seed top rated
            movie_seeder.seed_top_rated_movies()
            
        elif seed_type == 'essential':
            print("⚡ ESSENTIAL SEEDING - Quick setup with must-have movies")
            print("   - Seeding 10 essential movies")
            print("   - Seeding news articles\n")
            
            # Seed essential movies only
            essential_movies = [
                'The Shawshank Redemption', 'The Dark Knight', 'Inception',
                'Pulp Fiction', 'Forrest Gump', 'The Matrix', 'Interstellar',
                'Avengers: Endgame', 'Spirited Away', 'Parasite'
            ]
            
            added = 0
            for title in essential_movies:
                try:
                    existing = db[Config.DATABASE_NAME]['movies'].find_one({'title': title})
                    if not existing:
                        movie_data = movie_seeder.omdb_service.fetch_movie_by_title(title)
                        if movie_data:
                            movie_data['view_count'] = 100
                            movie_data['user_ratings'] = []
                            movie_data['reviews'] = []
                            db[Config.DATABASE_NAME]['movies'].insert_one(movie_data)
                            print(f"   ✅ Added: {title}")
                            added += 1
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
            
            print(f"\n✅ Added {added} essential movies")
            
        else:  # quick (default)
            print("⚡ QUICK SEEDING - Fast setup with popular movies")
            print("   - Seeding 20 popular movies")
            print("   - Seeding news articles\n")
            
            movie_seeder.quick_seed()
        
        # Seed news articles
        print("\n")
        news_service.seed_news()
        
        # Show final status
        print("\n" + "=" * 60)
        print("📊 FINAL STATUS")
        print("=" * 60)
        
        movie_status = movie_seeder.get_seeding_status()
        news_status = news_service.get_news_status()
        
        print(f"\n🎬 Movies:")
        print(f"   Total: {movie_status['total_movies']}")
        print(f"   Seeded: {movie_status['seeded_movies']}")
        print(f"   Trending: {movie_status['trending_movies']}")
        
        print(f"\n📰 News:")
        print(f"   Total: {news_status['total_articles']}")
        print(f"   Auto-fetched: {news_status['auto_fetched']}")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("=" * 60)
        print("\n🚀 You can now start the application:")
        print("   Backend: python app.py")
        print("   Frontend: npm run dev\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPlease check:")
        print("1. MongoDB connection string is correct")
        print("2. Internet connection is available")
        print("3. OMDb API key is valid\n")
        sys.exit(1)

if __name__ == '__main__':
    # Get seed type from command line argument
    seed_type = sys.argv[1] if len(sys.argv) > 1 else 'quick'
    
    if seed_type not in ['quick', 'full', 'essential']:
        print("❌ Invalid seed type. Use: quick, full, or essential")
        sys.exit(1)
    
    seed_database(seed_type)
