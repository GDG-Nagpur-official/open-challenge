from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import logs_collection

from bson import ObjectId

from app.utils.utils import serialize_docs

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@logs_bp.route('/', methods=['GET'])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit
    
    api_id = request.args.get('api_id')
    
    query = {'user_id': ObjectId(user_id)}
    
    if api_id:
        try:
            query['api_id'] = ObjectId(api_id)
        except:
            return jsonify({'error': 'Invalid API ID'}), 400
    
    logs = list(logs_collection.find(query).skip(skip).limit(limit).sort('timestamp', -1))
    total = logs_collection.count_documents(query)
    
    return jsonify({
        'logs': serialize_docs(logs),
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

@logs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    total_requests = logs_collection.count_documents({'user_id': ObjectId(user_id)})
    
    success_requests = logs_collection.count_documents({
        'user_id': ObjectId(user_id),
        'status_code': {'$gte': 200, '$lt': 300}
    })
    
    error_requests = logs_collection.count_documents({
        'user_id': ObjectId(user_id),
        'status_code': {'$gte': 400}
    })
    
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': None,
            'avg_response_time': {'$avg': '$response_time'}
        }}
    ]
    
    result = list(logs_collection.aggregate(pipeline))
    avg_response_time = result[0]['avg_response_time'] if result else 0
    
    return jsonify({
        'total_requests': total_requests,
        'success_requests': success_requests,
        'error_requests': error_requests,
        'avg_response_time': round(avg_response_time, 2)
    }), 200
