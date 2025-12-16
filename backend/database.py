from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from config import Config

client = None
db = None

try:
    client = MongoClient(
        Config.MONGODB_URI,
        serverSelectionTimeoutMS=2000
    )
    client.server_info()  # force connection check
    db = client.get_database()
except ServerSelectionTimeoutError:
    # MongoDB is not running – allow app to start
    client = None
    db = None


# Collections (safe even if db is None)
users_collection = db['users'] if db else None
apis_collection = db['apis'] if db else None
api_keys_collection = db['api_keys'] if db else None
logs_collection = db['logs'] if db else None


def init_indexes():
    if not db:
        return  # skip index creation if DB unavailable

    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    api_keys_collection.create_index('key', unique=True)
    api_keys_collection.create_index('user_id')
    apis_collection.create_index('user_id')
    logs_collection.create_index([('timestamp', -1)])
    logs_collection.create_index('api_id')
