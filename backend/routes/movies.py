from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.movie import Movie
from services.omdb_service import OMDbService
from config import Config

movies_bp = Blueprint('movies', __name__)

def init_movies_routes(db):
    """Initialize movies routes with database"""
    movie_model = Movie(db)
    omdb_service = OMDbService()
    
    @movies_bp.route('/search', methods=['GET'])
    def search_movies():
        """Search movies from OMDb API"""
        try:
            query = request.args.get('q', '')
            year = request.args.get('year')
            page = request.args.get('page', 1, type=int)
            
            if not query:
                return jsonify({'error': 'Search query is required'}), 400
            
            results = omdb_service.search_movies(query, year, page)
            
            return jsonify(results), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/fetch/<imdb_id>', methods=['GET'])
    def fetch_movie_by_imdb(imdb_id):
        """Fetch movie details from OMDb API by IMDb ID"""
        try:
            # Check if movie exists in database
            existing_movie = movie_model.get_movie_by_imdb_id(imdb_id)
            
            if existing_movie:
                return jsonify(existing_movie), 200
            
            # Fetch from OMDb API
            movie_data = omdb_service.fetch_movie_by_imdb_id(imdb_id)
            
            if not movie_data:
                return jsonify({'error': 'Movie not found'}), 404
            
            # Save to database
            movie_id = movie_model.create_movie(movie_data)
            movie_data['_id'] = movie_id
            
            return jsonify(movie_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/fetch-by-title', methods=['GET'])
    def fetch_movie_by_title():
        """Fetch movie details from OMDb API by title"""
        try:
            title = request.args.get('title')
            year = request.args.get('year')
            
            if not title:
                return jsonify({'error': 'Title is required'}), 400
            
            movie_data = omdb_service.fetch_movie_by_title(title, year)
            
            if not movie_data:
                return jsonify({'error': 'Movie not found'}), 404
            
            # Check if movie exists in database
            existing_movie = movie_model.get_movie_by_imdb_id(movie_data['imdb_id'])
            
            if existing_movie:
                return jsonify(existing_movie), 200
            
            # Save to database
            movie_id = movie_model.create_movie(movie_data)
            movie_data['_id'] = movie_id
            
            return jsonify(movie_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/<movie_id>', methods=['GET'])
    def get_movie(movie_id):
        """Get movie by ID from database"""
        try:
            movie = movie_model.get_movie_by_id(movie_id)
            
            if not movie:
                return jsonify({'error': 'Movie not found'}), 404
            
            # Increment view count
            movie_model.increment_view_count(movie_id)
            
            return jsonify(movie), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/production-house/<production_house>', methods=['GET'])
    def get_movies_by_production_house(production_house):
        """Get movies by production house"""
        try:
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', Config.ITEMS_PER_PAGE, type=int)
            sort_by = request.args.get('sort_by', 'year')
            
            movies = movie_model.get_movies_by_production_house(
                production_house, skip, limit, sort_by
            )
            
            return jsonify(movies), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/genre/<genre>', methods=['GET'])
    def get_movies_by_genre(genre):
        """Get movies by genre"""
        try:
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', Config.ITEMS_PER_PAGE, type=int)
            
            movies = movie_model.get_movies_by_genre(genre, skip, limit)
            
            return jsonify(movies), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/trending', methods=['GET'])
    def get_trending_movies():
        """Get trending movies"""
        try:
            limit = request.args.get('limit', 10, type=int)
            movies = movie_model.get_trending_movies(limit)
            
            return jsonify(movies), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/top-rated', methods=['GET'])
    def get_top_rated_movies():
        """Get top rated movies"""
        try:
            limit = request.args.get('limit', 10, type=int)
            movies = movie_model.get_top_rated_movies(limit)
            
            return jsonify(movies), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/filter', methods=['POST'])
    def filter_movies():
        """Filter movies by multiple criteria"""
        try:
            filters = request.get_json()
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', Config.ITEMS_PER_PAGE, type=int)
            
            movies = movie_model.filter_movies(filters, skip, limit)
            
            return jsonify(movies), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/<movie_id>/rate', methods=['POST'])
    @jwt_required()
    def rate_movie(movie_id):
        """Rate a movie"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            rating = data.get('rating')
            
            if not rating or not (0 <= float(rating) <= 10):
                return jsonify({'error': 'Rating must be between 0 and 10'}), 400
            
            movie_model.add_rating(movie_id, user_id, float(rating))
            
            return jsonify({'message': 'Rating added successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/<movie_id>/review', methods=['POST'])
    @jwt_required()
    def review_movie(movie_id):
        """Add a review to a movie"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            review = data.get('review')
            
            if not review:
                return jsonify({'error': 'Review text is required'}), 400
            
            movie_model.add_review(movie_id, user_id, review)
            
            return jsonify({'message': 'Review added successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @movies_bp.route('/production-houses', methods=['GET'])
    def get_production_houses():
        """Get list of all production houses"""
        return jsonify({'production_houses': Config.PRODUCTION_HOUSES}), 200
    
    return movies_bp
