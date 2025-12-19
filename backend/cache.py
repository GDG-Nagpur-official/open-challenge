import json
import logging
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

from config import Config

logger = logging.getLogger(__name__)


def _init_client() -> Optional[redis.Redis]:
    try:
        client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            password=Config.REDIS_PASSWORD,
            decode_responses=True,
        )
        client.ping()
        return client
    except RedisError as exc:
        logger.warning("Redis cache disabled: %s", exc)
        return None


redis_client = _init_client()


def cache_available() -> bool:
    return redis_client is not None


def build_user_prefix(user_id: str, namespace: str) -> str:
    return f"user:{user_id}:{namespace}"


def build_user_key(user_id: str, namespace: str, *parts: str) -> str:
    prefix = build_user_prefix(user_id, namespace)
    suffix = ":".join(filter(None, parts))
    return f"{prefix}:{suffix}" if suffix else prefix


def get_cached_json(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    try:
        payload = redis_client.get(key)
        return json.loads(payload) if payload else None
    except RedisError as exc:
        logger.warning("Redis GET failed for %s: %s", key, exc)
        return None


def set_cached_json(key: str, value: Any, ttl: Optional[int] = None) -> None:
    if not redis_client:
        return
    try:
        redis_client.setex(key, ttl or Config.CACHE_DEFAULT_TTL, json.dumps(value))
    except RedisError as exc:
        logger.warning("Redis SET failed for %s: %s", key, exc)


def invalidate_prefix(prefix: str) -> None:
    if not redis_client:
        return
    try:
        pattern = f"{prefix}*"
        for cache_key in redis_client.scan_iter(match=pattern):
            redis_client.delete(cache_key)
    except RedisError as exc:
        logger.warning("Redis invalidation failed for %s: %s", prefix, exc)


def invalidate_user_namespace(user_id: str, namespace: str) -> None:
    invalidate_prefix(build_user_prefix(user_id, namespace))
