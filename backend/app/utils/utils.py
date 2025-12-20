import hashlib
import secrets
import string
from functools import wraps
from flask import request, jsonify
from app.database import api_keys_collection
from bson import ObjectId

def generate_api_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def serialize_doc(doc):
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    if 'user_id' in doc and isinstance(doc['user_id'], ObjectId):
        doc['user_id'] = str(doc['user_id'])
    if 'api_id' in doc and isinstance(doc['api_id'], ObjectId):
        doc['api_id'] = str(doc['api_id'])
    if 'password' in doc:
        del doc['password']
    return doc

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 401
        
        key_doc = api_keys_collection.find_one({'key': api_key, 'is_active': True})
        
        if not key_doc:
            return jsonify({'error': 'Invalid or inactive API key'}), 401
        
        request.user_id = str(key_doc['user_id'])
        return f(*args, **kwargs)
    
    return decorated_function

def generate_reset_token():
    raw_token = secrets.token_hex(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, hashed_token