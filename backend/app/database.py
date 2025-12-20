from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.get_database()

users_collection = db['users']
apis_collection = db['apis']
api_keys_collection = db['api_keys']
logs_collection = db['logs']

def init_indexes():
    # Users
    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    # Password reset
    users_collection.create_index('reset_token')
    users_collection.create_index(
        'reset_token_expiry',
        expireAfterSeconds=0
    )
    # API keys
    api_keys_collection.create_index('key', unique=True)
    api_keys_collection.create_index('user_id')
    # APIs
    apis_collection.create_index('user_id')
    # Logs
    logs_collection.create_index([('timestamp', -1)])
    logs_collection.create_index('api_id')
