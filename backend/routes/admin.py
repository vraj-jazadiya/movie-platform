from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.movie_seeder import MovieSeeder
from services.news_service import NewsService

admin_bp = Blueprint('admin', __name__)

def init_admin_routes(db):
    """Initialize admin routes with database"""
    
    @admin_bp.route('/seed-movies', methods=['POST'])
    @jwt_required()
    def seed_movies():
        """Seed movies into database (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            # Get seed type from request
            data = request.get_json() or {}
            seed_type = data.get('type', 'quick')  # quick, full, trending, top_rated
            
            seeder = MovieSeeder(db)
            
            if seed_type == 'full':
                result = seeder.seed_all_movies()
            elif seed_type == 'trending':
                added = seeder.seed_trending_movies()
                result = {'success': True, 'total_added': added}
            elif seed_type == 'top_rated':
                added = seeder.seed_top_rated_movies()
                result = {'success': True, 'total_added': added}
            else:  # quick
                added = seeder.quick_seed()
                result = {'success': True, 'total_added': added}
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/seed-news', methods=['POST'])
    @jwt_required()
    def seed_news():
        """Seed news articles into database (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            news_service = NewsService(db)
            added = news_service.seed_news()
            
            return jsonify({
                'success': True,
                'articles_added': added
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/refresh-news', methods=['POST'])
    @jwt_required()
    def refresh_news():
        """Refresh news articles (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            news_service = NewsService(db)
            result = news_service.refresh_news()
            
            return jsonify({
                'success': True,
                'removed': result['removed'],
                'added': result['added']
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/data-status', methods=['GET'])
    @jwt_required()
    def get_data_status():
        """Get current data status (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            seeder = MovieSeeder(db)
            news_service = NewsService(db)
            
            movie_status = seeder.get_seeding_status()
            news_status = news_service.get_news_status()
            
            return jsonify({
                'movies': movie_status,
                'news': news_status
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/clear-movies', methods=['DELETE'])
    @jwt_required()
    def clear_movies():
        """Clear all seeded movies (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            movies_collection = db['movie_platform']['movies']
            result = movies_collection.delete_many({'seeded': True})
            
            return jsonify({
                'success': True,
                'deleted': result.deleted_count
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/clear-news', methods=['DELETE'])
    @jwt_required()
    def clear_news():
        """Clear all auto-fetched news (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            news_collection = db['movie_platform']['news']
            result = news_collection.delete_many({'auto_fetched': True})
            
            return jsonify({
                'success': True,
                'deleted': result.deleted_count
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @admin_bp.route('/seed-all', methods=['POST'])
    @jwt_required()
    def seed_all_data():
        """Seed both movies and news (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            # Get seed type
            data = request.get_json() or {}
            seed_type = data.get('type', 'quick')
            
            # Seed movies
            seeder = MovieSeeder(db)
            if seed_type == 'full':
                movie_result = seeder.seed_all_movies()
            else:
                added = seeder.quick_seed()
                movie_result = {'success': True, 'total_added': added}
            
            # Seed news
            news_service = NewsService(db)
            news_added = news_service.seed_news()
            
            return jsonify({
                'success': True,
                'movies': movie_result,
                'news': {'articles_added': news_added}
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return admin_bp
