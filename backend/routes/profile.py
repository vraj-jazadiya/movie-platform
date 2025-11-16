from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.playlist import Playlist

profile_bp = Blueprint('profile', __name__)

def init_profile_routes(db):
    """Initialize profile routes with database"""
    user_model = User(db)
    playlist_model = Playlist(db)
    
    @profile_bp.route('/', methods=['GET'])
    @jwt_required()
    def get_profile():
        """Get current user profile"""
        try:
            user_id = get_jwt_identity()
            user = user_model.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get user's playlists
            playlists = playlist_model.get_user_playlists(user_id)
            user['playlists'] = playlists
            
            return jsonify(user), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/<username>', methods=['GET'])
    def get_user_profile(username):
        """Get user profile by username"""
        try:
            user = user_model.get_user_by_username(username)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user.pop('password', None)
            user['_id'] = str(user['_id'])
            
            # Get user's public playlists
            playlists = playlist_model.get_user_playlists(user['_id'])
            public_playlists = [p for p in playlists if p.get('is_public', True)]
            user['playlists'] = public_playlists
            
            return jsonify(user), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/update', methods=['PUT'])
    @jwt_required()
    def update_profile():
        """Update user profile"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            
            # Remove fields that shouldn't be updated directly
            data.pop('username', None)
            data.pop('email', None)
            data.pop('password', None)
            data.pop('role', None)
            data.pop('_id', None)
            
            updated_user = user_model.update_user(user_id, data)
            
            if not updated_user:
                return jsonify({'error': 'Failed to update profile'}), 400
            
            return jsonify(updated_user), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/favorites', methods=['GET'])
    @jwt_required()
    def get_favorites():
        """Get user's favorite movies"""
        try:
            user_id = get_jwt_identity()
            user = user_model.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'favorites': user.get('favorites', [])}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/favorites/<movie_id>', methods=['POST'])
    @jwt_required()
    def add_to_favorites(movie_id):
        """Add movie to favorites"""
        try:
            user_id = get_jwt_identity()
            
            success = user_model.add_to_favorites(user_id, movie_id)
            
            if success:
                return jsonify({'message': 'Added to favorites'}), 200
            
            return jsonify({'error': 'Failed to add to favorites'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/favorites/<movie_id>', methods=['DELETE'])
    @jwt_required()
    def remove_from_favorites(movie_id):
        """Remove movie from favorites"""
        try:
            user_id = get_jwt_identity()
            
            success = user_model.remove_from_favorites(user_id, movie_id)
            
            if success:
                return jsonify({'message': 'Removed from favorites'}), 200
            
            return jsonify({'error': 'Failed to remove from favorites'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/watchlist', methods=['GET'])
    @jwt_required()
    def get_watchlist():
        """Get user's watchlist"""
        try:
            user_id = get_jwt_identity()
            user = user_model.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'watchlist': user.get('watchlist', [])}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/watchlist/<movie_id>', methods=['POST'])
    @jwt_required()
    def add_to_watchlist(movie_id):
        """Add movie to watchlist"""
        try:
            user_id = get_jwt_identity()
            
            success = user_model.add_to_watchlist(user_id, movie_id)
            
            if success:
                return jsonify({'message': 'Added to watchlist'}), 200
            
            return jsonify({'error': 'Failed to add to watchlist'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/watch-history', methods=['GET'])
    @jwt_required()
    def get_watch_history():
        """Get user's watch history"""
        try:
            user_id = get_jwt_identity()
            user = user_model.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'watch_history': user.get('watch_history', [])}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @profile_bp.route('/watch-history/<movie_id>', methods=['POST'])
    @jwt_required()
    def add_to_watch_history(movie_id):
        """Add movie to watch history"""
        try:
            user_id = get_jwt_identity()
            
            success = user_model.add_to_watch_history(user_id, movie_id)
            
            if success:
                return jsonify({'message': 'Added to watch history'}), 200
            
            return jsonify({'error': 'Failed to add to watch history'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return profile_bp
