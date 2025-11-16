from datetime import datetime
from bson import ObjectId

class Playlist:
    """Playlist model for the application"""
    
    def __init__(self, db):
        self.collection = db.playlists
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('user_id')
        self.collection.create_index('name')
    
    def create_playlist(self, user_id, name, description='', is_public=True):
        """Create a new playlist"""
        playlist_data = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'is_public': is_public,
            'movies': [],
            'likes': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(playlist_data)
        playlist_data['_id'] = str(result.inserted_id)
        
        return playlist_data
    
    def get_playlist_by_id(self, playlist_id):
        """Get playlist by ID"""
        try:
            playlist = self.collection.find_one({'_id': ObjectId(playlist_id)})
            if playlist:
                playlist['_id'] = str(playlist['_id'])
            return playlist
        except:
            return None
    
    def get_user_playlists(self, user_id):
        """Get all playlists for a user"""
        playlists = list(self.collection.find({'user_id': user_id}))
        for playlist in playlists:
            playlist['_id'] = str(playlist['_id'])
        return playlists
    
    def get_public_playlists(self, skip=0, limit=20):
        """Get all public playlists"""
        playlists = list(self.collection.find({'is_public': True}).skip(skip).limit(limit))
        for playlist in playlists:
            playlist['_id'] = str(playlist['_id'])
        return playlists
    
    def update_playlist(self, playlist_id, update_data):
        """Update playlist information"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return self.get_playlist_by_id(playlist_id)
        return None
    
    def add_movie_to_playlist(self, playlist_id, movie_data):
        """Add a movie to playlist"""
        movie_entry = {
            'movie_id': movie_data.get('movie_id'),
            'imdb_id': movie_data.get('imdb_id'),
            'title': movie_data.get('title'),
            'year': movie_data.get('year'),
            'poster': movie_data.get('poster'),
            'added_at': datetime.utcnow()
        }
        
        result = self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {
                '$push': {'movies': movie_entry},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0
    
    def remove_movie_from_playlist(self, playlist_id, movie_id):
        """Remove a movie from playlist"""
        result = self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {
                '$pull': {'movies': {'movie_id': movie_id}},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0
    
    def delete_playlist(self, playlist_id):
        """Delete a playlist"""
        result = self.collection.delete_one({'_id': ObjectId(playlist_id)})
        return result.deleted_count > 0
    
    def like_playlist(self, playlist_id, user_id):
        """Like a playlist"""
        result = self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {'$addToSet': {'likes': user_id}}
        )
        return result.modified_count > 0
    
    def unlike_playlist(self, playlist_id, user_id):
        """Unlike a playlist"""
        result = self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {'$pull': {'likes': user_id}}
        )
        return result.modified_count > 0
    
    def sort_playlist_movies(self, playlist_id, sort_by='year', order='desc'):
        """Sort movies in a playlist"""
        playlist = self.get_playlist_by_id(playlist_id)
        if not playlist:
            return None
        
        movies = playlist.get('movies', [])
        reverse = order == 'desc'
        
        if sort_by == 'year':
            movies.sort(key=lambda x: x.get('year', 0), reverse=reverse)
        elif sort_by == 'title':
            movies.sort(key=lambda x: x.get('title', ''), reverse=reverse)
        elif sort_by == 'added_at':
            movies.sort(key=lambda x: x.get('added_at', datetime.min), reverse=reverse)
        
        self.collection.update_one(
            {'_id': ObjectId(playlist_id)},
            {'$set': {'movies': movies, 'updated_at': datetime.utcnow()}}
        )
        
        return self.get_playlist_by_id(playlist_id)
