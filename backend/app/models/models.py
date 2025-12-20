from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    @staticmethod
    def create(username, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return {
            'username': username,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

class API:
    @staticmethod
    def create(user_id, name, description, endpoint, method, headers=None, params=None):
        return {
            'user_id': ObjectId(user_id),
            'name': name,
            'description': description,
            'endpoint': endpoint,
            'method': method,
            'headers': headers or {},
            'params': params or {},
            'status': 'active',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

class APIKey:
    @staticmethod
    def create(user_id, name, key):
        return {
            'user_id': ObjectId(user_id),
            'name': name,
            'key': key,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'last_used': None
        }

class Log:
    @staticmethod
    def create(api_id, user_id, method, endpoint, status_code, response_time, request_data=None, response_data=None, error=None):
        return {
            'api_id': ObjectId(api_id) if api_id else None,
            'user_id': ObjectId(user_id),
            'method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time': response_time,
            'request_data': request_data,
            'response_data': response_data,
            'error': error,
            'timestamp': datetime.utcnow()
        }
