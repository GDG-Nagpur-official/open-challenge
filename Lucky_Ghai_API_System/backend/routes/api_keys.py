from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import api_keys_collection
from models import APIKey
from utils import serialize_doc, serialize_docs, generate_api_key
from bson import ObjectId
from datetime import datetime

api_keys_bp = Blueprint('api_keys', __name__, url_prefix='/api/keys')

@api_keys_bp.route('/', methods=['GET'])
@jwt_required()
def get_api_keys():
    user_id = get_jwt_identity()
    
    keys = list(api_keys_collection.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
    
    return jsonify({'keys': serialize_docs(keys)}), 200

@api_keys_bp.route('/', methods=['POST'])
@jwt_required()
def create_api_key():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name', 'Default Key')
    
    api_key = generate_api_key()
    
    key_data = APIKey.create(user_id, name, api_key)
    result = api_keys_collection.insert_one(key_data)
    
    key_data['_id'] = result.inserted_id
    
    return jsonify({
        'message': 'API key created successfully',
        'key': serialize_doc(key_data)
    }), 201

@api_keys_bp.route('/<key_id>', methods=['DELETE'])
@jwt_required()
def delete_api_key(key_id):
    user_id = get_jwt_identity()
    
    try:
        key = api_keys_collection.find_one({'_id': ObjectId(key_id), 'user_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid key ID'}), 400
    
    if not key:
        return jsonify({'error': 'API key not found'}), 404
    
    api_keys_collection.delete_one({'_id': ObjectId(key_id)})
    
    return jsonify({'message': 'API key deleted successfully'}), 200

@api_keys_bp.route('/<key_id>/toggle', methods=['PATCH'])
@jwt_required()
def toggle_api_key(key_id):
    user_id = get_jwt_identity()
    
    try:
        key = api_keys_collection.find_one({'_id': ObjectId(key_id), 'user_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid key ID'}), 400
    
    if not key:
        return jsonify({'error': 'API key not found'}), 404
    
    new_status = not key.get('is_active', True)
    
    api_keys_collection.update_one(
        {'_id': ObjectId(key_id)},
        {'$set': {'is_active': new_status}}
    )
    
    updated_key = api_keys_collection.find_one({'_id': ObjectId(key_id)})
    
    return jsonify({
        'message': f'API key {"activated" if new_status else "deactivated"} successfully',
        'key': serialize_doc(updated_key)
    }), 200
