from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def generate_tokens(user_id, role='user'):
        """Generate access and refresh tokens"""
        additional_claims = {'role': role}
        
        access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=user_id,
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def verify_admin(role):
        """Verify if user is admin"""
        return role == 'admin'
