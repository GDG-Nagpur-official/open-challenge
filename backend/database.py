from pymongo import MongoClient
from config import Config
from pymongo.errors import ServerSelectionTimeoutError


client = MongoClient(Config.MONGODB_URI)
db = client.get_database()

users_collection = db['users']
apis_collection = db['apis']
api_keys_collection = db['api_keys']
logs_collection = db['logs']

def is_db_connected():
    try:
        client.admin.command("ping")
        return True
    except ServerSelectionTimeoutError:
        return False
    except Exception:
        return False


def init_indexes():
    try:
        users_collection.create_index('email', unique=True)
        users_collection.create_index('username', unique=True)
        api_keys_collection.create_index('key', unique=True)
        api_keys_collection.create_index('user_id')
        apis_collection.create_index('user_id')
        logs_collection.create_index([('timestamp', -1)])
        logs_collection.create_index('api_id')
    except ServerSelectionTimeoutError:
        # MongoDB not available, skip index creation
        pass
    except Exception:
        # Any other DB-related issue, skip safely
        pass
