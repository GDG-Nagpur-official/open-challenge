import secrets
import string
import bcrypt
from functools import wraps
from flask import request, jsonify
from bson import ObjectId
from database import api_keys_collection


# ---------------- PASSWORD & TOKEN ----------------

# def generate_reset_token():
#     return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# ---------------- API KEY ----------------

def generate_api_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# ---------------- SERIALIZERS ----------------

def serialize_doc(doc):
    if doc is None:
        return None

    doc['_id'] = str(doc['_id'])

    if 'user_id' in doc and isinstance(doc['user_id'], ObjectId):
        doc['user_id'] = str(doc['user_id'])

    if 'api_id' in doc and isinstance(doc['api_id'], ObjectId):
        doc['api_id'] = str(doc['api_id'])

    # Never expose password
    if 'password' in doc:
        del doc['password']

    return doc


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]


# ---------------- API KEY AUTH ----------------

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return jsonify({'error': 'API key is required'}), 401

        key_doc = api_keys_collection.find_one({
            'key': api_key,
            'is_active': True
        })

        if not key_doc:
            return jsonify({'error': 'Invalid or inactive API key'}), 401

        request.user_id = str(key_doc['user_id'])
        return f(*args, **kwargs)

    return decorated_function
