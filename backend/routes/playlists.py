from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.playlist import Playlist

playlists_bp = Blueprint('playlists', __name__)

def init_playlists_routes(db):
    """Initialize playlists routes with database"""
    playlist_model = Playlist(db)
    
    @playlists_bp.route('/', methods=['POST'])
    @jwt_required()
    def create_playlist():
        """Create a new playlist"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            
            name = data.get('name')
            if not name:
                return jsonify({'error': 'Playlist name is required'}), 400
            
            playlist = playlist_model.create_playlist(
                user_id=user_id,
                name=name,
                description=data.get('description', ''),
                is_public=data.get('is_public', True)
            )
            
            return jsonify(playlist), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>', methods=['GET'])
    def get_playlist(playlist_id):
        """Get playlist by ID"""
        try:
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            
            if not playlist:
                return jsonify({'error': 'Playlist not found'}), 404
            
            return jsonify(playlist), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/user/<user_id>', methods=['GET'])
    def get_user_playlists(user_id):
        """Get all playlists for a user"""
        try:
            playlists = playlist_model.get_user_playlists(user_id)
            return jsonify(playlists), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/public', methods=['GET'])
    def get_public_playlists():
        """Get all public playlists"""
        try:
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            playlists = playlist_model.get_public_playlists(skip, limit)
            return jsonify(playlists), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>', methods=['PUT'])
    @jwt_required()
    def update_playlist(playlist_id):
        """Update playlist"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            
            # Verify ownership
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            if not playlist or playlist['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            # Remove fields that shouldn't be updated directly
            data.pop('user_id', None)
            data.pop('movies', None)
            data.pop('_id', None)
            
            updated_playlist = playlist_model.update_playlist(playlist_id, data)
            
            if not updated_playlist:
                return jsonify({'error': 'Failed to update playlist'}), 400
            
            return jsonify(updated_playlist), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>/movies', methods=['POST'])
    @jwt_required()
    def add_movie_to_playlist(playlist_id):
        """Add a movie to playlist"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            
            # Verify ownership
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            if not playlist or playlist['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            # Validate movie data
            required_fields = ['movie_id', 'imdb_id', 'title']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            success = playlist_model.add_movie_to_playlist(playlist_id, data)
            
            if success:
                return jsonify({'message': 'Movie added to playlist'}), 200
            
            return jsonify({'error': 'Failed to add movie'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>/movies/<movie_id>', methods=['DELETE'])
    @jwt_required()
    def remove_movie_from_playlist(playlist_id, movie_id):
        """Remove a movie from playlist"""
        try:
            user_id = get_jwt_identity()
            
            # Verify ownership
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            if not playlist or playlist['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            success = playlist_model.remove_movie_from_playlist(playlist_id, movie_id)
            
            if success:
                return jsonify({'message': 'Movie removed from playlist'}), 200
            
            return jsonify({'error': 'Failed to remove movie'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>', methods=['DELETE'])
    @jwt_required()
    def delete_playlist(playlist_id):
        """Delete a playlist"""
        try:
            user_id = get_jwt_identity()
            
            # Verify ownership
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            if not playlist or playlist['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            success = playlist_model.delete_playlist(playlist_id)
            
            if success:
                return jsonify({'message': 'Playlist deleted'}), 200
            
            return jsonify({'error': 'Failed to delete playlist'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>/like', methods=['POST'])
    @jwt_required()
    def like_playlist(playlist_id):
        """Like a playlist"""
        try:
            user_id = get_jwt_identity()
            
            success = playlist_model.like_playlist(playlist_id, user_id)
            
            if success:
                return jsonify({'message': 'Playlist liked'}), 200
            
            return jsonify({'error': 'Failed to like playlist'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>/unlike', methods=['POST'])
    @jwt_required()
    def unlike_playlist(playlist_id):
        """Unlike a playlist"""
        try:
            user_id = get_jwt_identity()
            
            success = playlist_model.unlike_playlist(playlist_id, user_id)
            
            if success:
                return jsonify({'message': 'Playlist unliked'}), 200
            
            return jsonify({'error': 'Failed to unlike playlist'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @playlists_bp.route('/<playlist_id>/sort', methods=['POST'])
    @jwt_required()
    def sort_playlist(playlist_id):
        """Sort movies in a playlist"""
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            
            # Verify ownership
            playlist = playlist_model.get_playlist_by_id(playlist_id)
            if not playlist or playlist['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            sort_by = data.get('sort_by', 'year')
            order = data.get('order', 'desc')
            
            sorted_playlist = playlist_model.sort_playlist_movies(playlist_id, sort_by, order)
            
            if sorted_playlist:
                return jsonify(sorted_playlist), 200
            
            return jsonify({'error': 'Failed to sort playlist'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return playlists_bp
