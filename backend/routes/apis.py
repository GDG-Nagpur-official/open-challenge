from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import apis_collection
from models import API
from utils import serialize_doc, serialize_docs
from bson import ObjectId
from datetime import datetime, time
from pymongo import ASCENDING, DESCENDING

apis_bp = Blueprint('apis', __name__, url_prefix='/api/apis')

# NOTE:
# Use empty route '' instead of '/' with url_prefix to avoid
# Flask 308 redirects, which break CORS preflight (OPTIONS) requests.
@apis_bp.route('', methods=['GET'])
@jwt_required()
def get_apis():
    user_id = ObjectId(get_jwt_identity())
    args = request.args

    query = {'user_id': user_id}

    # Search (name + endpoint)
    if args.get('search'):
        query['$or'] = [
            {'name': {'$regex': args['search'], '$options': 'i'}},
            {'endpoint': {'$regex': args['search'], '$options': 'i'}}
        ]

    # Filters
    if args.get('method'):
        query['method'] = args['method']

    if args.get('status'):
        query['status'] = args['status']

    # Date Range Filter
    date_from = args.get('dateFrom')
    date_to = args.get('dateTo')
    date_field = args.get('dateField', 'created_at')
    
    # Validate date_field to prevent injection
    if date_field not in ['created_at', 'updated_at']:
        date_field = 'created_at'
    
    if date_from or date_to:
        date_query = {}
        
        if date_from:
            try:
                # Parse the date string (YYYY-MM-DD format)
                from_date = datetime.strptime(date_from, '%Y-%m-%d')
                from_date = datetime.combine(from_date.date(), time.min)
                date_query['$gte'] = from_date
            except ValueError:
                return jsonify({'error': 'Invalid dateFrom format. Use YYYY-MM-DD'}), 400
        
        if date_to:
            try:
                # Parse the date string (YYYY-MM-DD format)
                to_date = datetime.strptime(date_to, '%Y-%m-%d')
                to_date = datetime.combine(to_date.date(), time.max)
                date_query['$lte'] = to_date
            except ValueError:
                return jsonify({'error': 'Invalid dateTo format. Use YYYY-MM-DD'}), 400
        
        # Add the date filter to the query
        query[date_field] = date_query

    # Sorting - Accept both sortBy/sortOrder AND sort_by/sort_order
    sort_by = args.get('sortBy') or args.get('sort_by', 'created_at')
    sort_order_param = args.get('sortOrder') or args.get('sort_order', 'desc')
    
    # Validate sort_by field to prevent injection
    allowed_sort_fields = ['name', 'created_at', 'updated_at', 'usage_count', 'method', 'status']
    if sort_by not in allowed_sort_fields:
        sort_by = 'created_at'
    
    sort_order = DESCENDING if sort_order_param == 'desc' else ASCENDING

    # Pagination
    page = int(args.get('page', 1))
    limit = int(args.get('limit', 10))
    skip = (page - 1) * limit

    cursor = (
        apis_collection
        .find(query)
        .collation({"locale": "en", "strength": 2}) 
        .sort(sort_by, sort_order)
        .skip(skip)
        .limit(limit)
    )

    apis = list(cursor)
    total = apis_collection.count_documents(query)

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


# NOTE:
# Use empty route '' instead of '/' with url_prefix to avoid
# Flask 308 redirects, which break CORS preflight (OPTIONS) requests.
@apis_bp.route('', methods=['POST'])
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
