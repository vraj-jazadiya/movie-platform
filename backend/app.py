from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config

# Import route initializers
from routes.auth import init_auth_routes
from routes.movies import init_movies_routes
from routes.profile import init_profile_routes
from routes.playlists import init_playlists_routes
from routes.news import init_news_routes
from routes.chat import init_chat_routes
from routes.contact import init_contact_routes
from routes.admin import init_admin_routes

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Connect to MongoDB
    try:
        client = MongoClient(Config.MONGO_URI)
        db = client[Config.DATABASE_NAME]
        print(f"Connected to MongoDB: {Config.DATABASE_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        raise
    
    # Register blueprints
    app.register_blueprint(init_auth_routes(db), url_prefix='/api/auth')
    app.register_blueprint(init_movies_routes(db), url_prefix='/api/movies')
    app.register_blueprint(init_profile_routes(db), url_prefix='/api/profile')
    app.register_blueprint(init_playlists_routes(db), url_prefix='/api/playlists')
    app.register_blueprint(init_news_routes(db), url_prefix='/api/news')
    app.register_blueprint(init_chat_routes(db), url_prefix='/api/chat')
    app.register_blueprint(init_contact_routes(db), url_prefix='/api/contact')
    app.register_blueprint(init_admin_routes(db), url_prefix='/api/admin')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Movie Platform API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'Welcome to Movie Platform API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'movies': '/api/movies',
                'profile': '/api/profile',
                'playlists': '/api/playlists',
                'news': '/api/news',
                'chat': '/api/chat',
                'contact': '/api/contact',
                'admin': '/api/admin'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is missing'}), 401
    
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
