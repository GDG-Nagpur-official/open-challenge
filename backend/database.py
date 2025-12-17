from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.get_database()

users_collection = db['users']
apis_collection = db['apis']
api_keys_collection = db['api_keys']
logs_collection = db['logs']
# New collection for rate limiting
rate_limits_collection = db['rate_limits']

def init_indexes():
    """
    Creates indexes efficiently. 
    Should be called once at application startup, not per request.
    """
    # Unique constraints
    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    api_keys_collection.create_index('key', unique=True)
    
    # Performance indexes
    api_keys_collection.create_index('user_id')
    apis_collection.create_index('user_id')
    logs_collection.create_index([('timestamp', -1)])
    logs_collection.create_index('api_id')
    
    # TTL Index for rate limiting (auto-expire records after 60 seconds)
    rate_limits_collection.create_index('created_at', expireAfterSeconds=60)