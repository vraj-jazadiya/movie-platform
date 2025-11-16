import requests
import time
from services.omdb_service import OMDbService
from config import Config

class MovieSeeder:
    """Service for automatically seeding the database with movies"""
    
    def __init__(self, db):
        self.db = db
        self.omdb_service = OMDbService()
        self.movies_collection = db[Config.DATABASE_NAME]['movies']
        
        # Popular movies to seed for each production house
        self.seed_movies = {
            'Marvel Studios': [
                'Avengers: Endgame', 'Iron Man', 'Black Panther', 'Spider-Man: No Way Home',
                'Thor: Ragnarok', 'Guardians of the Galaxy', 'Captain America: Civil War',
                'Doctor Strange', 'Avengers: Infinity War', 'Black Widow'
            ],
            'Warner Bros. Pictures': [
                'The Dark Knight', 'Inception', 'Interstellar', 'The Matrix',
                'Harry Potter and the Sorcerer\'s Stone', 'Joker', 'Dunkirk',
                'Mad Max: Fury Road', 'The Batman', 'Dune'
            ],
            'Universal Pictures': [
                'Jurassic Park', 'Fast & Furious', 'E.T.', 'Jaws',
                'The Bourne Identity', 'Minions', 'Despicable Me', 'Back to the Future',
                'Jurassic World', 'The Fast and the Furious'
            ],
            'Paramount Pictures': [
                'Titanic', 'Forrest Gump', 'Mission: Impossible', 'Transformers',
                'Top Gun', 'Indiana Jones', 'Star Trek', 'The Godfather',
                'Top Gun: Maverick', 'A Quiet Place'
            ],
            '20th Century Studios': [
                'Avatar', 'Star Wars', 'Alien', 'Die Hard',
                'Planet of the Apes', 'X-Men', 'Deadpool', 'The Martian',
                'Avatar: The Way of Water', 'Bohemian Rhapsody'
            ],
            'Columbia Pictures': [
                'Spider-Man', 'Men in Black', 'Ghostbusters', 'The Social Network',
                'Zombieland', 'The Amazing Spider-Man', 'Bad Boys', 'Jumanji',
                'Spider-Man: Into the Spider-Verse', 'Venom'
            ],
            'Walt Disney Pictures': [
                'The Lion King', 'Frozen', 'Moana', 'Aladdin',
                'Beauty and the Beast', 'Toy Story', 'Finding Nemo', 'The Incredibles',
                'Coco', 'Encanto'
            ],
            'DreamWorks Pictures': [
                'Shrek', 'How to Train Your Dragon', 'Kung Fu Panda', 'Madagascar',
                'Megamind', 'The Prince of Egypt', 'Puss in Boots', 'Trolls',
                'The Boss Baby', 'Shrek 2'
            ],
            'Studio Ghibli': [
                'Spirited Away', 'My Neighbor Totoro', 'Princess Mononoke', 'Howl\'s Moving Castle',
                'Ponyo', 'The Wind Rises', 'Kiki\'s Delivery Service', 'Castle in the Sky',
                'Grave of the Fireflies', 'Nausicaä of the Valley of the Wind'
            ],
            'Legendary Entertainment': [
                'The Dark Knight', 'Inception', 'Godzilla', 'Pacific Rim',
                'Dune', 'Kong: Skull Island', 'Warcraft', 'Detective Pikachu',
                'Godzilla vs. Kong', 'Enola Holmes'
            ]
        }
    
    def seed_all_movies(self):
        """Seed movies from all production houses"""
        print("🎬 Starting movie seeding process...")
        total_added = 0
        total_skipped = 0
        
        for house, movies in self.seed_movies.items():
            print(f"\n📽️ Seeding movies for {house}...")
            added, skipped = self.seed_production_house(house, movies)
            total_added += added
            total_skipped += skipped
            
            # Rate limiting - wait between production houses
            time.sleep(2)
        
        print(f"\n✅ Seeding complete!")
        print(f"   Added: {total_added} movies")
        print(f"   Skipped: {total_skipped} movies (already exist)")
        
        return {
            'success': True,
            'total_added': total_added,
            'total_skipped': total_skipped
        }
    
    def seed_production_house(self, production_house, movie_titles):
        """Seed movies for a specific production house"""
        added = 0
        skipped = 0
        
        for title in movie_titles:
            try:
                # Check if movie already exists
                existing = self.movies_collection.find_one({'title': title})
                if existing:
                    print(f"   ⏭️  Skipped: {title} (already exists)")
                    skipped += 1
                    continue
                
                # Fetch movie data from OMDb
                movie_data = self.omdb_service.fetch_movie_by_title(title)
                
                if movie_data:
                    # Override production house if needed
                    if not movie_data.get('production_house'):
                        movie_data['production_house'] = production_house
                    
                    # Add metadata
                    movie_data['view_count'] = 0
                    movie_data['user_ratings'] = []
                    movie_data['reviews'] = []
                    movie_data['seeded'] = True
                    
                    # Insert into database
                    self.movies_collection.insert_one(movie_data)
                    print(f"   ✅ Added: {title}")
                    added += 1
                else:
                    print(f"   ❌ Failed: {title} (not found in OMDb)")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Error adding {title}: {str(e)}")
        
        return added, skipped
    
    def seed_trending_movies(self):
        """Seed currently trending movies"""
        print("🔥 Seeding trending movies...")
        
        trending_titles = [
            'Oppenheimer', 'Barbie', 'The Super Mario Bros. Movie',
            'Guardians of the Galaxy Vol. 3', 'Spider-Man: Across the Spider-Verse',
            'John Wick: Chapter 4', 'The Little Mermaid', 'Fast X',
            'Ant-Man and the Wasp: Quantumania', 'Scream VI'
        ]
        
        added = 0
        for title in trending_titles:
            try:
                existing = self.movies_collection.find_one({'title': title})
                if existing:
                    # Update view count to make it trending
                    self.movies_collection.update_one(
                        {'_id': existing['_id']},
                        {'$set': {'view_count': 1000 + (added * 100)}}
                    )
                    added += 1
                else:
                    movie_data = self.omdb_service.fetch_movie_by_title(title)
                    if movie_data:
                        movie_data['view_count'] = 1000 + (added * 100)
                        movie_data['user_ratings'] = []
                        movie_data['reviews'] = []
                        movie_data['trending'] = True
                        self.movies_collection.insert_one(movie_data)
                        added += 1
                
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print(f"✅ Added {added} trending movies")
        return added
    
    def seed_top_rated_movies(self):
        """Seed top-rated movies"""
        print("⭐ Seeding top-rated movies...")
        
        top_rated_titles = [
            'The Shawshank Redemption', 'The Godfather', 'The Dark Knight',
            'Pulp Fiction', 'Forrest Gump', 'Inception', 'Fight Club',
            'The Matrix', 'Goodfellas', 'The Lord of the Rings: The Return of the King'
        ]
        
        added = 0
        for title in top_rated_titles:
            try:
                existing = self.movies_collection.find_one({'title': title})
                if not existing:
                    movie_data = self.omdb_service.fetch_movie_by_title(title)
                    if movie_data:
                        movie_data['view_count'] = 500
                        movie_data['user_ratings'] = []
                        movie_data['reviews'] = []
                        movie_data['top_rated'] = True
                        self.movies_collection.insert_one(movie_data)
                        added += 1
                
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print(f"✅ Added {added} top-rated movies")
        return added
    
    def quick_seed(self):
        """Quick seed with essential movies only (faster)"""
        print("⚡ Quick seeding essential movies...")
        
        essential_movies = [
            'Avengers: Endgame', 'The Dark Knight', 'Inception', 'Interstellar',
            'Pulp Fiction', 'The Shawshank Redemption', 'Forrest Gump', 'The Matrix',
            'Spirited Away', 'Parasite', 'Joker', 'Spider-Man: No Way Home',
            'Dune', 'Top Gun: Maverick', 'Everything Everywhere All at Once',
            'The Batman', 'Avatar', 'Titanic', 'Jurassic Park', 'Star Wars'
        ]
        
        added = 0
        for title in essential_movies:
            try:
                existing = self.movies_collection.find_one({'title': title})
                if not existing:
                    movie_data = self.omdb_service.fetch_movie_by_title(title)
                    if movie_data:
                        movie_data['view_count'] = 100
                        movie_data['user_ratings'] = []
                        movie_data['reviews'] = []
                        self.movies_collection.insert_one(movie_data)
                        print(f"   ✅ Added: {title}")
                        added += 1
                
                time.sleep(0.3)
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print(f"✅ Quick seed complete! Added {added} movies")
        return added
    
    def get_seeding_status(self):
        """Get current seeding status"""
        total_movies = self.movies_collection.count_documents({})
        seeded_movies = self.movies_collection.count_documents({'seeded': True})
        trending_movies = self.movies_collection.count_documents({'view_count': {'$gte': 1000}})
        
        return {
            'total_movies': total_movies,
            'seeded_movies': seeded_movies,
            'trending_movies': trending_movies,
            'production_houses_covered': len(self.seed_movies)
        }
