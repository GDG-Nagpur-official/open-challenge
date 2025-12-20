from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from config import Config
import sys

try:
    client = MongoClient(
        Config.MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )
    client.server_info()  # Force MongoDB connection
    db = client.get_database()
    print("✅ MongoDB connected successfully")
except ServerSelectionTimeoutError:
    print("❌ ERROR: Unable to connect to MongoDB. Please check MongoDB service or URI.")
    sys.exit(1)




users_collection = db['users']
apis_collection = db['apis']
api_keys_collection = db['api_keys']
logs_collection = db['logs']

def init_indexes():
    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    api_keys_collection.create_index('key', unique=True)
    api_keys_collection.create_index('user_id')
    apis_collection.create_index('user_id')
    logs_collection.create_index([('timestamp', -1)])
    logs_collection.create_index('api_id')
