from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    """User model for the application"""
    
    def __init__(self, db):
        self.collection = db.users
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('username', unique=True)
        self.collection.create_index('email', unique=True)
    
    def create_user(self, username, email, password, name, bio='', role='user'):
        """Create a new user"""
        # Check if user already exists
        if self.collection.find_one({'username': username}):
            return {'error': 'Username already exists'}, 400
        
        if self.collection.find_one({'email': email}):
            return {'error': 'Email already exists'}, 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'name': name,
            'bio': bio,
            'role': role,
            'profile_picture': '',
            'cover_photo': '',
            'playlists': [],
            'favorites': [],
            'watchlist': [],
            'watch_history': [],
            'followers': [],
            'following': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        user_data.pop('password')
        
        return user_data, 201
    
    def get_user_by_username(self, username):
        """Get user by username"""
        user = self.collection.find_one({'username': username})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
                user.pop('password', None)
            return user
        except:
            return None
    
    def verify_password(self, username, password):
        """Verify user password"""
        user = self.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return self.get_user_by_id(user_id)
        return None
    
    def delete_user(self, user_id):
        """Delete a user"""
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0
    
    def get_all_users(self, skip=0, limit=20):
        """Get all users (admin only)"""
        users = list(self.collection.find().skip(skip).limit(limit))
        for user in users:
            user['_id'] = str(user['_id'])
            user.pop('password', None)
        return users
    
    def add_to_favorites(self, user_id, movie_id):
        """Add movie to user's favorites"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'favorites': movie_id}}
        )
        return result.modified_count > 0
    
    def remove_from_favorites(self, user_id, movie_id):
        """Remove movie from user's favorites"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'favorites': movie_id}}
        )
        return result.modified_count > 0
    
    def add_to_watchlist(self, user_id, movie_id):
        """Add movie to user's watchlist"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'watchlist': movie_id}}
        )
        return result.modified_count > 0
    
    def add_to_watch_history(self, user_id, movie_id):
        """Add movie to user's watch history"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$push': {
                    'watch_history': {
                        'movie_id': movie_id,
                        'watched_at': datetime.utcnow()
                    }
                }
            }
        )
        return result.modified_count > 0
