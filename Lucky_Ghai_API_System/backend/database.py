from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from config import Config
import sys
try:
    client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)

    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
    
    db = client.get_database()

    users_collection = db['users']
    apis_collection = db['apis']
    api_keys_collection = db['api_keys']
    logs_collection = db['logs']

except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    print(f"❌ CRITICAL ERROR: Could not connect to MongoDB. Details: {e}")
    db = None

def init_indexes():

    if db is not None:
        try:
            users_collection.create_index('email', unique=True)
            users_collection.create_index('username', unique=True)
            api_keys_collection.create_index('key', unique=True)
            api_keys_collection.create_index('user_id')
            apis_collection.create_index('user_id')
            logs_collection.create_index([('timestamp', -1)])
            logs_collection.create_index('api_id')
            print("✅ Indexes created successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not create indexes: {e}")