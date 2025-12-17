from flask import Blueprint, request, jsonify
from database import apis_collection, logs_collection
from models import Log
from utils import api_key_required
from bson import ObjectId
import requests
import time

execute_bp = Blueprint('execute', __name__, url_prefix='/api/execute')

@execute_bp.route('/<api_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@api_key_required
def execute_api(api_id):
    try:
        api = apis_collection.find_one({'_id': ObjectId(api_id)})
    except:
        return jsonify({'error': 'Invalid API ID'}), 400
    
    if not api:
        return jsonify({'error': 'API not found'}), 404
    
    if api['status'] != 'active':
        return jsonify({'error': 'API is not active'}), 403
    
    start_time = time.time()
    
    try:
        method = api['method']
        endpoint = api['endpoint']
        headers = api.get('headers', {})
        params = api.get('params', {})
        
        query_params = {**params, **request.args.to_dict()}
        request_body = request.get_json() if request.is_json else None
        
        response = requests.request(
            method=method,
            url=endpoint,
            headers=headers,
            params=query_params,
            json=request_body,
            timeout=30
        )
        
        response_time = (time.time() - start_time) * 1000
        
        log_data = Log.create(
            api_id=api_id,
            user_id=str(api['user_id']),
            method=method,
            endpoint=endpoint,
            status_code=response.status_code,
            response_time=response_time,
            request_data={'params': query_params, 'body': request_body},
            response_data=response.text[:1000]
        )
        
        logs_collection.insert_one(log_data)
        
        return jsonify({
            'status_code': response.status_code,
            'response': response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text,
            'response_time': round(response_time, 2)
        }), response.status_code
        
    except requests.exceptions.Timeout:
        response_time = (time.time() - start_time) * 1000
        
        log_data = Log.create(
            api_id=api_id,
            user_id=str(api['user_id']),
            method=api['method'],
            endpoint=api['endpoint'],
            status_code=408,
            response_time=response_time,
            error='Request timeout'
        )
        
        logs_collection.insert_one(log_data)
        
        return jsonify({'error': 'Request timeout'}), 408
        
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        
        log_data = Log.create(
            api_id=api_id,
            user_id=str(api['user_id']),
            method=api['method'],
            endpoint=api['endpoint'],
            status_code=500,
            response_time=response_time,
            error=str(e)
        )
        
        logs_collection.insert_one(log_data)
        
        return jsonify({'error': str(e)}), 500
