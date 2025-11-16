from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models.contact import Contact

contact_bp = Blueprint('contact', __name__)

def init_contact_routes(db):
    """Initialize contact routes with database"""
    contact_model = Contact(db)
    
    @contact_bp.route('/', methods=['POST'])
    def submit_contact():
        """Submit a contact form"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'email', 'subject', 'message']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            contact = contact_model.create_contact(
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message']
            )
            
            return jsonify({
                'message': 'Contact form submitted successfully',
                'contact': contact
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/all', methods=['GET'])
    @jwt_required()
    def get_all_contacts():
        """Get all contact submissions (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            contacts = contact_model.get_all_contacts(skip, limit)
            return jsonify(contacts), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/pending', methods=['GET'])
    @jwt_required()
    def get_pending_contacts():
        """Get pending contact submissions (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            skip = request.args.get('skip', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            
            contacts = contact_model.get_pending_contacts(skip, limit)
            return jsonify(contacts), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/<contact_id>', methods=['GET'])
    @jwt_required()
    def get_contact(contact_id):
        """Get contact submission by ID (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            contact = contact_model.get_contact_by_id(contact_id)
            
            if not contact:
                return jsonify({'error': 'Contact not found'}), 404
            
            return jsonify(contact), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/<contact_id>/status', methods=['PUT'])
    @jwt_required()
    def update_contact_status(contact_id):
        """Update contact submission status (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            data = request.get_json()
            status = data.get('status')
            
            if not status:
                return jsonify({'error': 'Status is required'}), 400
            
            success = contact_model.update_contact_status(contact_id, status)
            
            if success:
                return jsonify({'message': 'Status updated successfully'}), 200
            
            return jsonify({'error': 'Failed to update status'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/<contact_id>/reply', methods=['POST'])
    @jwt_required()
    def mark_as_replied(contact_id):
        """Mark contact as replied (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = contact_model.mark_as_replied(contact_id)
            
            if success:
                return jsonify({'message': 'Marked as replied'}), 200
            
            return jsonify({'error': 'Failed to mark as replied'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @contact_bp.route('/<contact_id>', methods=['DELETE'])
    @jwt_required()
    def delete_contact(contact_id):
        """Delete a contact submission (admin only)"""
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            success = contact_model.delete_contact(contact_id)
            
            if success:
                return jsonify({'message': 'Contact deleted successfully'}), 200
            
            return jsonify({'error': 'Failed to delete contact'}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return contact_bp
