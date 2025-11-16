from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.chat import Chat

chat_bp = Blueprint('chat', __name__)

def init_chat_routes(db):
    """Initialize chat routes with database"""
    chat_model = Chat(db)
    
    @chat_bp.route('/my-chat', methods=['GET'])
    @jwt_required()
    def get_my_chat():
        """Get or create chat for current user"""
        try:
            user_id = get_jwt_identity()
            chat = chat_model.get_chat_by_user_id(user_id)
            
            return jsonify(chat), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/<chat_id>', methods=['GET'])
    @jwt_required()
    def get_chat(chat_id):
        """Get chat by ID"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            role = claims.get('role', 'user')
            
            chat = chat_model.get_chat_by_id(chat_id)
            
            if not chat:
                return jsonify({'error': 'Chat not found'}), 404
            
            # Check authorization
            if role != 'admin' and chat['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            return jsonify(chat), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/all', methods=['GET'])
    @jwt_required()
    def get_all_chats():
        """Get all chats (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            chats = chat_model.get_all_chats(skip, limit)
            return jsonify(chats), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/<chat_id>/message', methods=['POST'])
    @jwt_required()
    def send_message(chat_id):
        """Send a message in chat"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            role = claims.get('role', 'user')
            data = request.get_json()
            
            message = data.get('message')
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            # Verify authorization
            chat = chat_model.get_chat_by_id(chat_id)
            if not chat:
                return jsonify({'error': 'Chat not found'}), 404
            
            if role != 'admin' and chat['user_id'] != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
            
            success = chat_model.add_message(chat_id, user_id, role, message)
            
            if success:
                return jsonify({'message': 'Message sent successfully'}), 200
            
            return jsonify({'error': 'Failed to send message'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/<chat_id>/read', methods=['POST'])
    @jwt_required()
    def mark_as_read(chat_id):
        """Mark all messages as read (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = chat_model.mark_messages_as_read(chat_id)
            
            if success:
                return jsonify({'message': 'Messages marked as read'}), 200
            
            return jsonify({'error': 'Failed to mark messages as read'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/<chat_id>/close', methods=['POST'])
    @jwt_required()
    def close_chat(chat_id):
        """Close a chat (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = chat_model.close_chat(chat_id)
            
            if success:
                return jsonify({'message': 'Chat closed successfully'}), 200
            
            return jsonify({'error': 'Failed to close chat'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/<chat_id>', methods=['DELETE'])
    @jwt_required()
    def delete_chat(chat_id):
        """Delete a chat (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = chat_model.delete_chat(chat_id)
            
            if success:
                return jsonify({'message': 'Chat deleted successfully'}), 200
            
            return jsonify({'error': 'Failed to delete chat'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/unread-count', methods=['GET'])
    @jwt_required()
    def get_unread_count():
        """Get count of unread chats (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            count = chat_model.get_unread_chats_count()
            return jsonify({'unread_count': count}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return chat_bp
