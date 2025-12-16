from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import users_collection
from utils import serialize_doc
from bson import ObjectId
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

DEFAULT_SETTINGS = {
    'theme': 'light',
    'email_notifications': True,
    'default_rate_limit': 1000
}

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Ensure settings exist (backward compatibility)
    user_settings = user.get('settings', {})
    final_settings = {**DEFAULT_SETTINGS, **user_settings}
    
    profile = {
        'username': user['username'],
        'email': user['email'],
        'created_at': user.get('created_at'),
        'updated_at': user.get('updated_at'),
        'settings': final_settings
    }
    
    return jsonify(profile), 200

@user_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Validate allowed fields
    allowed_fields = {'theme', 'email_notifications', 'default_rate_limit'}
    settings_update = {}
    
    for key, value in data.items():
        if key in allowed_fields:
            # Validation
            if key == 'theme' and value not in ['light', 'dark']:
                return jsonify({'error': 'Invalid theme. Must be light or dark'}), 400
            if key == 'email_notifications' and not isinstance(value, bool):
                return jsonify({'error': 'email_notifications must be a boolean'}), 400
            if key == 'default_rate_limit':
                try:
                    value = int(value)
                    if value < 0:
                        return jsonify({'error': 'default_rate_limit must be positive'}), 400
                except (ValueError, TypeError):
                    return jsonify({'error': 'default_rate_limit must be an integer'}), 400
            
            settings_update[f'settings.{key}'] = value
            
    if not settings_update:
        return jsonify({'message': 'No valid settings to update'}), 200
        
    settings_update['updated_at'] = datetime.utcnow()
    
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': settings_update}
    )
    
    return jsonify({'message': 'Settings updated successfully'}), 200
