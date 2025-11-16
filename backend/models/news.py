from datetime import datetime
from bson import ObjectId

class News:
    """News model for the application"""
    
    def __init__(self, db):
        self.collection = db.news
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better query performance"""
        self.collection.create_index('created_at')
        self.collection.create_index('category')
    
    def create_news(self, title, content, category, author_id, image=''):
        """Create a new news article"""
        news_data = {
            'title': title,
            'content': content,
            'category': category,
            'author_id': author_id,
            'image': image,
            'views': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(news_data)
        news_data['_id'] = str(result.inserted_id)
        
        return news_data
    
    def get_news_by_id(self, news_id):
        """Get news article by ID"""
        try:
            news = self.collection.find_one({'_id': ObjectId(news_id)})
            if news:
                news['_id'] = str(news['_id'])
            return news
        except:
            return None
    
    def get_all_news(self, skip=0, limit=20):
        """Get all news articles"""
        news_list = list(self.collection.find().sort('created_at', -1).skip(skip).limit(limit))
        for news in news_list:
            news['_id'] = str(news['_id'])
        return news_list
    
    def get_news_by_category(self, category, skip=0, limit=20):
        """Get news by category"""
        news_list = list(self.collection.find(
            {'category': category}
        ).sort('created_at', -1).skip(skip).limit(limit))
        
        for news in news_list:
            news['_id'] = str(news['_id'])
        return news_list
    
    def get_latest_news(self, limit=5):
        """Get latest news articles"""
        news_list = list(self.collection.find().sort('created_at', -1).limit(limit))
        for news in news_list:
            news['_id'] = str(news['_id'])
        return news_list
    
    def update_news(self, news_id, update_data):
        """Update news article"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'_id': ObjectId(news_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return self.get_news_by_id(news_id)
        return None
    
    def delete_news(self, news_id):
        """Delete a news article"""
        result = self.collection.delete_one({'_id': ObjectId(news_id)})
        return result.deleted_count > 0
    
    def increment_views(self, news_id):
        """Increment news article views"""
        self.collection.update_one(
            {'_id': ObjectId(news_id)},
            {'$inc': {'views': 1}}
        )
    
    def search_news(self, query, skip=0, limit=20):
        """Search news by title or content"""
        news_list = list(self.collection.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'content': {'$regex': query, '$options': 'i'}}
            ]
        }).sort('created_at', -1).skip(skip).limit(limit))
        
        for news in news_list:
            news['_id'] = str(news['_id'])
        return news_list
