from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import apis_collection
from models import API
from utils import serialize_doc, serialize_docs
from bson import ObjectId
from datetime import datetime

apis_bp = Blueprint('apis', __name__, url_prefix='/api/apis')

@apis_bp.route('/', methods=['GET'])
@jwt_required()
def get_apis():
    user_id = get_jwt_identity()
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    skip = (page - 1) * limit
    
    apis = list(apis_collection.find({'user_id': ObjectId(user_id)}).skip(skip).limit(limit).sort('created_at', -1))
    total = apis_collection.count_documents({'user_id': ObjectId(user_id)})
    
    return jsonify({
        'apis': serialize_docs(apis),
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

@apis_bp.route('/<api_id>', methods=['GET'])
@jwt_required()
def get_api(api_id):
    user_id = get_jwt_identity()
    
    try:
        api = apis_collection.find_one({'_id': ObjectId(api_id), 'user_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid API ID'}), 400
    
    if not api:
        return jsonify({'error': 'API not found'}), 404
    
    return jsonify({'api': serialize_doc(api)}), 200

@apis_bp.route('/', methods=['POST'])
@jwt_required()
def create_api():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    endpoint = data.get('endpoint')
    method = data.get('method', 'GET')
    headers = data.get('headers', {})
    params = data.get('params', {})
    
    if not all([name, endpoint]):
        return jsonify({'error': 'Name and endpoint are required'}), 400
    
    if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
        return jsonify({'error': 'Invalid HTTP method'}), 400
    
    api_data = API.create(user_id, name, description, endpoint, method, headers, params)
    result = apis_collection.insert_one(api_data)
    
    api_data['_id'] = result.inserted_id
    
    return jsonify({
        'message': 'API created successfully',
        'api': serialize_doc(api_data)
    }), 201

@apis_bp.route('/<api_id>', methods=['PUT'])
@jwt_required()
def update_api(api_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        api = apis_collection.find_one({'_id': ObjectId(api_id), 'user_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid API ID'}), 400
    
    if not api:
        return jsonify({'error': 'API not found'}), 404
    
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'endpoint' in data:
        update_data['endpoint'] = data['endpoint']
    if 'method' in data:
        if data['method'] not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            return jsonify({'error': 'Invalid HTTP method'}), 400
        update_data['method'] = data['method']
    if 'headers' in data:
        update_data['headers'] = data['headers']
    if 'params' in data:
        update_data['params'] = data['params']
    if 'status' in data:
        update_data['status'] = data['status']
    
    update_data['updated_at'] = datetime.utcnow()
    
    apis_collection.update_one({'_id': ObjectId(api_id)}, {'$set': update_data})
    
    updated_api = apis_collection.find_one({'_id': ObjectId(api_id)})
    
    return jsonify({
        'message': 'API updated successfully',
        'api': serialize_doc(updated_api)
    }), 200

@apis_bp.route('/<api_id>', methods=['DELETE'])
@jwt_required()
def delete_api(api_id):
    user_id = get_jwt_identity()
    
    try:
        api = apis_collection.find_one({'_id': ObjectId(api_id), 'user_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid API ID'}), 400
    
    if not api:
        return jsonify({'error': 'API not found'}), 404
    
    apis_collection.delete_one({'_id': ObjectId(api_id)})
    
    return jsonify({'message': 'API deleted successfully'}), 200
