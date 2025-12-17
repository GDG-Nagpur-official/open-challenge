from flask import Blueprint, request, jsonify
from database import apis_collection, logs_collection
from models import Log
from utils import api_key_required, is_safe_url
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
    
    if not api or api.get('status') != 'active':
        return jsonify({'error': 'API not found or inactive'}), 404
    
    # --- FIX: SSRF Protection ---
    if not is_safe_url(api['endpoint']):
        return jsonify({'error': 'Security blocked: Invalid or private endpoint URL'}), 403
    
    start_time = time.time()
    
    try:
        # Prepare request
        method = api['method']
        endpoint = api['endpoint']
        headers = api.get('headers', {})
        params = api.get('params', {})
        
        # Merge stored params with incoming request params
        query_params = {**params, **request.args.to_dict()}
        request_body = request.get_json() if request.is_json else None
        
        response = requests.request(
            method=method,
            url=endpoint,
            headers=headers,
            params=query_params,
            json=request_body,
            timeout=15  # Reduced timeout from 30s to 15s for safety
        )
        
        response_time = (time.time() - start_time) * 1000
        
        # Async logging is better, but keeping sync for "Internal cleanup" scope
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
        
        # Handle content type safely
        is_json = response.headers.get('Content-Type', '').startswith('application/json')
        resp_data = response.json() if is_json else response.text
        
        return jsonify({
            'status_code': response.status_code,
            'response': resp_data,
            'response_time': round(response_time, 2)
        }), response.status_code
        
    except requests.exceptions.Timeout:
        return _log_and_error(api, api_id, 408, start_time, 'Request timeout')
    except Exception as e:
        return _log_and_error(api, api_id, 500, start_time, str(e))

def _log_and_error(api, api_id, status_code, start_time, error_msg):
    """Helper to reduce code duplication in error handling"""
    response_time = (time.time() - start_time) * 1000
    log_data = Log.create(
        api_id=api_id,
        user_id=str(api['user_id']),
        method=api['method'],
        endpoint=api['endpoint'],
        status_code=status_code,
        response_time=response_time,
        error=error_msg
    )
    logs_collection.insert_one(log_data)
    return jsonify({'error': error_msg}), status_code