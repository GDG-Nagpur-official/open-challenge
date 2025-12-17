from pymongo import MongoClient, errors
from config import Config

db = None

try:
    client = MongoClient(
        Config.MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )
    client.server_info()

    db_name = Config.MONGODB_URI.rsplit("/", 1)[-1]
    db = client[db_name]

    print("✅ MongoDB connected successfully")

except errors.ServerSelectionTimeoutError as e:
    print("❌ MongoDB connection failed")
    print(e)

# ✅ FIX IS HERE
if db is not None:
    users_collection = db['users']
    apis_collection = db['apis']
    api_keys_collection = db['api_keys']
    logs_collection = db['logs']
else:
    users_collection = None
    apis_collection = None
    api_keys_collection = None
    logs_collection = None


def init_indexes():
    if db is None:
        print("⚠️ MongoDB not connected. Skipping index creation.")
        return

    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    api_keys_collection.create_index('key', unique=True)
    api_keys_collection.create_index('user_id')
    apis_collection.create_index('user_id')
    logs_collection.create_index([('timestamp', -1)])
    logs_collection.create_index('api_id')
