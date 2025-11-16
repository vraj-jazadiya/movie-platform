from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.news import News

news_bp = Blueprint('news', __name__)

def init_news_routes(db):
    """Initialize news routes with database"""
    news_model = News(db)
    
    @news_bp.route('/', methods=['GET'])
    def get_all_news():
        """Get all news articles"""
        try:
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            news_list = news_model.get_all_news(skip, limit)
            return jsonify(news_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/<news_id>', methods=['GET'])
    def get_news(news_id):
        """Get news article by ID"""
        try:
            news = news_model.get_news_by_id(news_id)
            
            if not news:
                return jsonify({'error': 'News not found'}), 404
            
            # Increment views
            news_model.increment_views(news_id)
            
            return jsonify(news), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/category/<category>', methods=['GET'])
    def get_news_by_category(category):
        """Get news by category"""
        try:
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            news_list = news_model.get_news_by_category(category, skip, limit)
            return jsonify(news_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/latest', methods=['GET'])
    def get_latest_news():
        """Get latest news articles"""
        try:
            limit = request.args.get('limit', 5, type=int)
            news_list = news_model.get_latest_news(limit)
            return jsonify(news_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/search', methods=['GET'])
    def search_news():
        """Search news articles"""
        try:
            query = request.args.get('q', '')
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            if not query:
                return jsonify({'error': 'Search query is required'}), 400
            
            news_list = news_model.search_news(query, skip, limit)
            return jsonify(news_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/', methods=['POST'])
    @jwt_required()
    def create_news():
        """Create a new news article (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            user_id = get_jwt_identity()
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['title', 'content', 'category']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            news = news_model.create_news(
                title=data['title'],
                content=data['content'],
                category=data['category'],
                author_id=user_id,
                image=data.get('image', '')
            )
            
            return jsonify(news), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/<news_id>', methods=['PUT'])
    @jwt_required()
    def update_news(news_id):
        """Update a news article (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            data = request.get_json()
            
            # Remove fields that shouldn't be updated directly
            data.pop('author_id', None)
            data.pop('_id', None)
            data.pop('views', None)
            
            updated_news = news_model.update_news(news_id, data)
            
            if not updated_news:
                return jsonify({'error': 'Failed to update news'}), 400
            
            return jsonify(updated_news), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @news_bp.route('/<news_id>', methods=['DELETE'])
    @jwt_required()
    def delete_news(news_id):
        """Delete a news article (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = news_model.delete_news(news_id)
            
            if success:
                return jsonify({'message': 'News deleted successfully'}), 200
            
            return jsonify({'error': 'Failed to delete news'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return news_bp
