from datetime import datetime
from bson import ObjectId

class Movie:
    """Movie model for the application"""
    
    def __init__(self, db):
        self.collection = db.movies
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('imdb_id', unique=True)
        self.collection.create_index('title')
        self.collection.create_index('year')
        self.collection.create_index('production_house')
        self.collection.create_index('genre')
    
    def create_movie(self, movie_data):
        """Create or update a movie"""
        # Check if movie already exists
        existing = self.collection.find_one({'imdb_id': movie_data.get('imdb_id')})
        
        if existing:
            # Update existing movie
            self.collection.update_one(
                {'imdb_id': movie_data.get('imdb_id')},
                {'$set': {**movie_data, 'updated_at': datetime.utcnow()}}
            )
            return str(existing['_id'])
        
        # Create new movie
        movie_data['created_at'] = datetime.utcnow()
        movie_data['updated_at'] = datetime.utcnow()
        movie_data['ratings'] = []
        movie_data['reviews'] = []
        movie_data['view_count'] = 0
        
        result = self.collection.insert_one(movie_data)
        return str(result.inserted_id)
    
    def get_movie_by_id(self, movie_id):
        """Get movie by ID"""
        try:
            movie = self.collection.find_one({'_id': ObjectId(movie_id)})
            if movie:
                movie['_id'] = str(movie['_id'])
            return movie
        except:
            return None
    
    def get_movie_by_imdb_id(self, imdb_id):
        """Get movie by IMDb ID"""
        movie = self.collection.find_one({'imdb_id': imdb_id})
        if movie:
            movie['_id'] = str(movie['_id'])
        return movie
    
    def search_movies(self, query, skip=0, limit=20):
        """Search movies by title"""
        movies = list(self.collection.find(
            {'title': {'$regex': query, '$options': 'i'}}
        ).skip(skip).limit(limit))
        
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def get_movies_by_production_house(self, production_house, skip=0, limit=20, sort_by='year'):
        """Get movies by production house"""
        sort_order = -1 if sort_by == 'year' else -1
        
        movies = list(self.collection.find(
            {'production_house': production_house}
        ).sort(sort_by, sort_order).skip(skip).limit(limit))
        
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def get_movies_by_genre(self, genre, skip=0, limit=20):
        """Get movies by genre"""
        movies = list(self.collection.find(
            {'genre': {'$regex': genre, '$options': 'i'}}
        ).skip(skip).limit(limit))
        
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def get_trending_movies(self, limit=10):
        """Get trending movies (most viewed)"""
        movies = list(self.collection.find().sort('view_count', -1).limit(limit))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def get_top_rated_movies(self, limit=10):
        """Get top rated movies"""
        movies = list(self.collection.find().sort('imdb_rating', -1).limit(limit))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def filter_movies(self, filters, skip=0, limit=20):
        """Filter movies by multiple criteria"""
        query = {}
        
        if filters.get('production_house'):
            query['production_house'] = filters['production_house']
        
        if filters.get('genre'):
            query['genre'] = {'$regex': filters['genre'], '$options': 'i'}
        
        if filters.get('year_from') or filters.get('year_to'):
            query['year'] = {}
            if filters.get('year_from'):
                query['year']['$gte'] = filters['year_from']
            if filters.get('year_to'):
                query['year']['$lte'] = filters['year_to']
        
        if filters.get('rating_min'):
            query['imdb_rating'] = {'$gte': float(filters['rating_min'])}
        
        sort_by = filters.get('sort_by', 'year')
        sort_order = -1 if filters.get('sort_order', 'desc') == 'desc' else 1
        
        movies = list(self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit))
        
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies
    
    def increment_view_count(self, movie_id):
        """Increment movie view count"""
        self.collection.update_one(
            {'_id': ObjectId(movie_id)},
            {'$inc': {'view_count': 1}}
        )
    
    def add_rating(self, movie_id, user_id, rating):
        """Add user rating to movie"""
        self.collection.update_one(
            {'_id': ObjectId(movie_id)},
            {
                '$push': {
                    'ratings': {
                        'user_id': user_id,
                        'rating': rating,
                        'created_at': datetime.utcnow()
                    }
                }
            }
        )
    
    def add_review(self, movie_id, user_id, review_text):
        """Add user review to movie"""
        self.collection.update_one(
            {'_id': ObjectId(movie_id)},
            {
                '$push': {
                    'reviews': {
                        'user_id': user_id,
                        'review': review_text,
                        'created_at': datetime.utcnow()
                    }
                }
            }
        )
    
    def delete_movie(self, movie_id):
        """Delete a movie"""
        result = self.collection.delete_one({'_id': ObjectId(movie_id)})
        return result.deleted_count > 0
