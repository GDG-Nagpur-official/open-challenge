import logging
import time
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError, ServerSelectionTimeoutError

from config import Config

logger = logging.getLogger(__name__)


class DatabaseUnavailableError(ConnectionFailure):
    """Raised when MongoDB cannot be reached after retry attempts."""


_client: Optional[MongoClient] = None
_db = None
_indexes_initialized = False


def _connect_with_retry() -> Optional[MongoClient]:
    """Attempt to connect to MongoDB with exponential backoff."""
    backoff = Config.MONGODB_BACKOFF_BASE
    for attempt in range(1, Config.MONGODB_MAX_RETRIES + 1):
        try:
            client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=Config.MONGODB_SERVER_SELECTION_TIMEOUT_MS,
            )
            client.admin.command('ping')
            logger.info("Connected to MongoDB on attempt %s", attempt)
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError) as exc:
            logger.warning(
                "MongoDB connection failed (attempt %s/%s): %s",
                attempt,
                Config.MONGODB_MAX_RETRIES,
                exc,
            )
            if attempt == Config.MONGODB_MAX_RETRIES:
                break
            time.sleep(backoff)
            backoff = min(backoff * 2, Config.MONGODB_BACKOFF_MAX)
    logger.error("MongoDB connection failed after %s attempts", Config.MONGODB_MAX_RETRIES)
    return None


def get_client() -> MongoClient:
    """Return a connected MongoClient or raise a DatabaseUnavailableError."""
    global _client, _db
    if _client is not None:
        return _client

    client = _connect_with_retry()
    if client is None:
        raise DatabaseUnavailableError("MongoDB is unavailable")

    _client = client
    _db = client.get_database()
    return _client


def get_db():
    """Return the database object, ensuring the connection is ready."""
    global _db
    if _db is not None:
        return _db

    client = get_client()
    _db = client.get_database()
    return _db


def get_collection(name: str):
    """Return a Mongo collection or raise a DatabaseUnavailableError."""
    try:
        database = get_db()
        return database[name]
    except PyMongoError as exc:
        logger.error("MongoDB access error: %s", exc)
        raise DatabaseUnavailableError("MongoDB is unavailable") from exc


def get_users_collection():
    return get_collection('users')


def get_apis_collection():
    return get_collection('apis')


def get_api_keys_collection():
    return get_collection('api_keys')


def get_logs_collection():
    return get_collection('logs')


def init_indexes():
    """Create indexes once per process."""
    global _indexes_initialized
    if _indexes_initialized:
        return

    users = get_users_collection()
    apis = get_apis_collection()
    api_keys = get_api_keys_collection()
    logs = get_logs_collection()

    users.create_index('email', unique=True)
    users.create_index('username', unique=True)
    api_keys.create_index('key', unique=True)
    api_keys.create_index('user_id')
    apis.create_index('user_id')
    logs.create_index([('timestamp', -1)])
    logs.create_index('api_id')

    _indexes_initialized = True
