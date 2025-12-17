import secrets
import string
import socket
from urllib.parse import urlparse
from functools import wraps
from datetime import datetime
from flask import request, jsonify
from database import api_keys_collection, rate_limits_collection
from bson import ObjectId

def generate_api_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def serialize_doc(doc):
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    for field in ['user_id', 'api_id']:
        if field in doc and isinstance(doc[field], ObjectId):
            doc[field] = str(doc[field])
    if 'password' in doc:
        del doc['password']
    return doc

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

def check_rate_limit(key, limit=60):
    """
    Simple MongoDB-based rate limiter.
    Allows 'limit' requests per minute per API key.
    """
    now = datetime.utcnow()
    # Count requests in the last 60 seconds for this key
    request_count = rate_limits_collection.count_documents({
        'key': key,
        'created_at': {'$gt': datetime.fromtimestamp(now.timestamp() - 60)}
    })
    
    if request_count >= limit:
        return False
        
    rate_limits_collection.insert_one({
        'key': key,
        'created_at': now
    })
    return True

def is_safe_url(url):
    """
    Prevents SSRF by blocking requests to local/private networks.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
        
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # block localhost explicitly
        if hostname in ['localhost', '127.0.0.1', '::1', '0.0.0.0']:
            return False

        # block private IP ranges (basic check)
        ip = socket.gethostbyname(hostname)
        if ip.startswith(('10.', '192.168.', '172.16.', '127.')):
            return False
            
        return True
    except:
        return False

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 401
        
        # Verify key exists and is active
        key_doc = api_keys_collection.find_one({'key': api_key, 'is_active': True})
        if not key_doc:
            return jsonify({'error': 'Invalid or inactive API key'}), 401
            
        # --- FIX: Rate Limiting Check ---
        if not check_rate_limit(api_key):
            return jsonify({'error': 'Rate limit exceeded (60 req/min)'}), 429
        
        request.user_id = str(key_doc['user_id'])
        return f(*args, **kwargs)
    
    return decorated_function