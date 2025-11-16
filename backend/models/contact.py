from datetime import datetime
from bson import ObjectId

class Contact:
    """Contact model for the application"""
    
    def __init__(self, db):
        self.collection = db.contacts
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('email')
        self.collection.create_index('created_at')
    
    def create_contact(self, name, email, subject, message):
        """Create a new contact submission"""
        contact_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'status': 'pending',
            'replied': False,
            'created_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(contact_data)
        contact_data['_id'] = str(result.inserted_id)
        
        return contact_data
    
    def get_contact_by_id(self, contact_id):
        """Get contact submission by ID"""
        try:
            contact = self.collection.find_one({'_id': ObjectId(contact_id)})
            if contact:
                contact['_id'] = str(contact['_id'])
            return contact
        except:
            return None
    
    def get_all_contacts(self, skip=0, limit=20):
        """Get all contact submissions"""
        contacts = list(self.collection.find().sort('created_at', -1).skip(skip).limit(limit))
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
        return contacts
    
    def get_pending_contacts(self, skip=0, limit=20):
        """Get pending contact submissions"""
        contacts = list(self.collection.find(
            {'status': 'pending'}
        ).sort('created_at', -1).skip(skip).limit(limit))
        
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
        return contacts
    
    def update_contact_status(self, contact_id, status):
        """Update contact submission status"""
        result = self.collection.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'status': status}}
        )
        
        return result.modified_count > 0
    
    def mark_as_replied(self, contact_id):
        """Mark contact as replied"""
        result = self.collection.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'replied': True, 'status': 'resolved'}}
        )
        
        return result.modified_count > 0
    
    def delete_contact(self, contact_id):
        """Delete a contact submission"""
        result = self.collection.delete_one({'_id': ObjectId(contact_id)})
        return result.deleted_count > 0
