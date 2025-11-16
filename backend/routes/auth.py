from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user import User
from services.auth_service import AuthService
from config import Config
import bcrypt

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(db):
    """Initialize authentication routes with database"""
    user_model = User(db)
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Register a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'name']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Create user
            result, status = user_model.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                name=data['name'],
                bio=data.get('bio', ''),
                role='user'
            )
            
            if status == 201:
                # Generate tokens
                tokens = AuthService.generate_tokens(result['_id'], result['role'])
                result['tokens'] = tokens
                
                return jsonify(result), 201
            
            return jsonify(result), status
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Login user"""
        try:
            data = request.get_json()
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password are required'}), 400
            
            # Verify credentials
            user = user_model.verify_password(username, password)
            
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Generate tokens
            tokens = AuthService.generate_tokens(str(user['_id']), user['role'])
            
            # Remove password from response
            user.pop('password', None)
            user['_id'] = str(user['_id'])
            
            return jsonify({
                'user': user,
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token']
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @auth_bp.route('/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        """Get current user information"""
        try:
            user_id = get_jwt_identity()
            user = user_model.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify(user), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @auth_bp.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        """Refresh access token"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            role = claims.get('role', 'user')
            
            tokens = AuthService.generate_tokens(user_id, role)
            
            return jsonify(tokens), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @auth_bp.route('/init-admin', methods=['POST'])
    def init_admin():
        """Initialize admin account (should be called once)"""
        try:
            # Check if admin already exists
            admin = user_model.get_user_by_username(Config.ADMIN_USERNAME)
            
            if admin:
                return jsonify({'message': 'Admin already exists'}), 200
            
            # Create admin user
            result, status = user_model.create_user(
                username=Config.ADMIN_USERNAME,
                email='admin@movieplatform.com',
                password=Config.ADMIN_PASSWORD,
                name='Administrator',
                bio='Platform Administrator',
                role='admin'
            )
            
            if status == 201:
                return jsonify({'message': 'Admin account created successfully'}), 201
            
            return jsonify(result), status
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return auth_bp
