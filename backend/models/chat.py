from datetime import datetime
from bson import ObjectId

class Chat:
    """Chat model for the application"""
    
    def __init__(self, db):
        self.collection = db.chats
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('user_id')
        self.collection.create_index('created_at')
    
    def create_chat(self, user_id):
        """Create a new chat conversation"""
        chat_data = {
            'user_id': user_id,
            'messages': [],
            'is_active': True,
            'unread_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(chat_data)
        chat_data['_id'] = str(result.inserted_id)
        
        return chat_data
    
    def get_chat_by_id(self, chat_id):
        """Get chat by ID"""
        try:
            chat = self.collection.find_one({'_id': ObjectId(chat_id)})
            if chat:
                chat['_id'] = str(chat['_id'])
            return chat
        except:
            return None
    
    def get_chat_by_user_id(self, user_id):
        """Get or create chat for a user"""
        chat = self.collection.find_one({'user_id': user_id})
        
        if chat:
            chat['_id'] = str(chat['_id'])
            return chat
        
        # Create new chat if doesn't exist
        return self.create_chat(user_id)
    
    def get_all_chats(self, skip=0, limit=20):
        """Get all chats (admin only)"""
        chats = list(self.collection.find().sort('updated_at', -1).skip(skip).limit(limit))
        for chat in chats:
            chat['_id'] = str(chat['_id'])
        return chats
    
    def add_message(self, chat_id, sender_id, sender_role, message_text):
        """Add a message to chat"""
        message = {
            'sender_id': sender_id,
            'sender_role': sender_role,
            'message': message_text,
            'is_read': False,
            'timestamp': datetime.utcnow()
        }
        
        update_data = {
            '$push': {'messages': message},
            '$set': {'updated_at': datetime.utcnow()}
        }
        
        # Increment unread count if message is from user
        if sender_role == 'user':
            update_data['$inc'] = {'unread_count': 1}
        
        result = self.collection.update_one(
            {'_id': ObjectId(chat_id)},
            update_data
        )
        
        return result.modified_count > 0
    
    def mark_messages_as_read(self, chat_id):
        """Mark all messages as read"""
        result = self.collection.update_one(
            {'_id': ObjectId(chat_id)},
            {
                '$set': {
                    'messages.$[].is_read': True,
                    'unread_count': 0,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    def close_chat(self, chat_id):
        """Close/deactivate a chat"""
        result = self.collection.update_one(
            {'_id': ObjectId(chat_id)},
            {
                '$set': {
                    'is_active': False,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    def delete_chat(self, chat_id):
        """Delete a chat"""
        result = self.collection.delete_one({'_id': ObjectId(chat_id)})
        return result.deleted_count > 0
    
    def get_unread_chats_count(self):
        """Get count of chats with unread messages"""
        return self.collection.count_documents({'unread_count': {'$gt': 0}})
