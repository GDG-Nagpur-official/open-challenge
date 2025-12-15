import time
from pymongo import MongoClient, errors
from config import Config

client = None
db = None
users_collection = None
apis_collection = None
api_keys_collection = None
logs_collection = None


def connect_to_mongo(max_retries=5, initial_delay=1, backoff_factor=2):
    global client, db, users_collection, apis_collection, api_keys_collection, logs_collection

    if client is not None and db is not None:
        return

    delay = initial_delay
    for attempt in range(max_retries):
        try:
            client_local = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
            )
            client_local.admin.command("ping")
            db_local = client_local.get_database()
            client = client_local
            db = db_local
            users_collection = db["users"]
            apis_collection = db["apis"]
            api_keys_collection = db["api_keys"]
            logs_collection = db["logs"]
            return
        except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure):
            time.sleep(delay)
            delay *= backoff_factor

    raise RuntimeError("Could not connect to MongoDB after retries")


def init_indexes():
    if client is None or db is None:
        connect_to_mongo()

    users_collection.create_index("email", unique=True)
    users_collection.create_index("username", unique=True)
    api_keys_collection.create_index("key", unique=True)
    api_keys_collection.create_index("user_id")
    apis_collection.create_index("user_id")
    logs_collection.create_index([("timestamp", -1)])
    logs_collection.create_index("api_id")
